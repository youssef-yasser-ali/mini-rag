from fastapi import  APIRouter , Depends , File , UploadFile , status,Request
from fastapi.responses import JSONResponse
import aiofiles
import os
from models import ResponseMessage , AssetsEnums
from helpers.config import get_settings , Settings
from .schemas.data_schema import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.AssetModel import AssetModel
 

from controllers import DataController  , ProcessController
from models.db_schemas import DataChunk , Asset
import logging



logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(prefix="/api/v1/data", tags=["data", 'api_v1'], responses={404: {"description": "Not found"}})




@data_router.post("/upload/{project_id}")
async def upload_data(request:Request , project_id: str , file: UploadFile = File(...) , app_settings: Settings  = Depends(get_settings)):
    

    data_base = request.app.database
    project_model =await ProjectModel.create_instance(db_client=data_base)
    project = await project_model.get_or_create_project(project_id=project_id)



    data_controller = DataController()
    isvalid , response_message= data_controller.validate_uploaded_file(file)

    if not isvalid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": response_message
        })
    
    file_path , file_id =  data_controller.generate_unique_file_path(file_name=file.filename,project_id= project_id)


    try :
        async with aiofiles.open(file_path, 'wb') as buffer:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await buffer.write(chunk)   
    except Exception as e:
        logger.error(f"Error while uploading file: {e}")
        
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": ResponseMessage.FILEUPLOADFAILED.value})
    


    asset_model = await AssetModel.create_instance(db_client=data_base)
    asset_resource = Asset(asset_project_id=project.id , asset_name=file_id, asset_type=AssetsEnums.ASSET_TYPE_FILE.value  , asset_size=os.path.getsize(file_path) , asset_config={})

    asset_record = await asset_model.create_asset(asset_resource)


    return JSONResponse(content={"message": ResponseMessage.FILEUPLOADSUCCESS.value , "file_id": str(asset_record.id) })



@data_router.post("/process/{project_id}")
async def process_data(request:Request , project_id :str, process_request: ProcessRequest):
    
    chunk_size = process_request.chunk_size
    chunk_overlap = process_request.chunk_overlap
    do_reset = process_request.do_reset

    data_base = request.app.database

    project_model =await ProjectModel.create_instance(db_client=data_base)
    asset_model = await AssetModel.create_instance(db_client=data_base)
    project = await project_model.get_or_create_project(project_id=project_id)


                                                         

    project_file_ids = {}

    if process_request.file_id : 

        asset_record = await asset_model.get_asset_record(asset_project_id=project.id , asset_name=process_request.file_id)

        if not asset_record:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": ResponseMessage.FILENOTEXIST.value})

        project_file_ids[asset_record.id] = asset_record.asset_name
    else:

        project_assets = await asset_model.get_all_project_asset(asset_project_id=project.id , asset_type=AssetsEnums.ASSET_TYPE_FILE.value)

        project_file_ids = {asset.id : asset.asset_name for asset in project_assets}


    if len(project_file_ids) == 0:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": ResponseMessage.NOFILEERROR.value})
    
    

    chunk_model = await ChunkModel.create_instance(db_client=data_base)

    if do_reset:
        await chunk_model.delete_chunk_by_project_id(project_id=project.id)


    process_controler = ProcessController(project_id = project_id)


    no_files = 0
    no_records = 0

    for asset_id , file_id in project_file_ids.items():

        file_content = process_controler.get_file_content(file_id)


        if file_content is None:
            logger.error(f"Error while processing file: {file_id}")
            continue



        file_chunks = process_controler.process_file_content(file_content=file_content , chunk_size=chunk_size , chunk_overlap=chunk_overlap)

        if not file_chunks or len(file_chunks) == 0:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": ResponseMessage.FILEPROCESSINGFAILED.value})
        

        


    
        data_chunks = [ DataChunk(chunk_project_id=project.id,chunk_index=i, chunk_asset_id= asset_id ,chunk_metadata=chunk.metadata, chunk_text=chunk.page_content) for i, chunk in enumerate(file_chunks) ]


        no_records += await chunk_model.insert_many_chunks(data_chunks)
        no_files += 1

    return JSONResponse(content={"message": ResponseMessage.FILEPROCESSINGSUCCESS.value , "inserted_chunks": no_records , "processed_files": no_files})



