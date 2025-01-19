from fastapi import  APIRouter , Depends , File , UploadFile , status
from fastapi.responses import JSONResponse
import aiofiles
from models import ResponseMessage
from helpers.config import get_settings , Settings

from controllers import DataController , ProjectController
import logging

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(prefix="/api/v1/data", tags=["data"], responses={404: {"description": "Not found"}})

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str , file: UploadFile = File(...) , app_settings: Settings  = Depends(get_settings)):
    
    
    data_controller = DataController()

    isvalid , response_message= data_controller.validate_uploaded_file(file)

    if not isvalid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": response_message
        })
    
    file_path =  data_controller.generate_unique_file_name(file_name=file.filename,project_id= project_id)


    try :
        async with aiofiles.open(file_path, 'wb') as buffer:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await buffer.write(chunk)   
    except Exception as e:
        logger.error(f"Error while uploading file: {e}")
        
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": ResponseMessage.FILEUPLOADFAILED.value})
    

    return JSONResponse(content={"message": ResponseMessage.FILEUPLOADSUCCESS.value})
