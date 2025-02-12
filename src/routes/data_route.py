from fastapi import  APIRouter , Depends , File , UploadFile , status,Request
from fastapi.responses import JSONResponse
import aiofiles
from models import ResponseMessage
from helpers.config import get_settings , Settings
from .schemas.data_schema import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel

from controllers import DataController  , ProcessController
from models.db_schemas import DataChunk
import logging



logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(prefix="/api/v1/data", tags=["data"], responses={404: {"description": "Not found"}})




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
    

    return JSONResponse(content={"message": ResponseMessage.FILEUPLOADSUCCESS.value , "file_id": file_id })



@data_router.post("/process/{project_id}")
async def process_data(request:Request , project_id :str, process_request: ProcessRequest):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    chunk_overlap = process_request.chunk_overlap
    do_reset = process_request.do_reset

    data_base = request.app.database

    project_model =await ProjectModel.create_instance(db_client=data_base)
    project = await project_model.get_or_create_project(project_id=project_id)


                                                         

    process_controler = ProcessController(project_id = project_id)

    file_content = process_controler.get_file_content(file_id)

    file_chunks = process_controler.process_file_content(file_content=file_content , chunk_size=chunk_size , chunk_overlap=chunk_overlap)

    if not file_chunks or len(file_chunks) == 0:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": ResponseMessage.FILEPROCESSINGFAILED.value})
    

    chunk_model = await ChunkModel.create_instance(db_client=data_base)
    
    if do_reset:
        await chunk_model.delete_chunk_by_project_id(project_id=project.id)

 
    data_chunks = [ DataChunk(chunk_project_id=project.id,chunk_index=i,chunk_metadata=chunk.metadata, chunk_text=chunk.page_content) for i, chunk in enumerate(file_chunks)]


    no_records = await chunk_model.insert_many_chunks(data_chunks)

    return JSONResponse(content={"message": ResponseMessage.FILEPROCESSINGSUCCESS.value , "inserted_chunks": no_records})



