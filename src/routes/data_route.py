from fastapi import  APIRouter , Depends , File , UploadFile , status
from fastapi.responses import JSONResponse
import aiofiles

import os 
from helpers.config import get_settings , Settings
from controllers import DataController , ProjectController
from models import ResponseMessage



data_router = APIRouter(prefix="/api/v1/data", tags=["data"], responses={404: {"description": "Not found"}})

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str , file: UploadFile = File(...) , app_settings: Settings  = Depends(get_settings)):
    
    
    data_controller = DataController()

    isvalid , ResponseMessage= data_controller.validate_uploaded_file(file)

    if not isvalid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": ResponseMessage
        })
    
    file_path =  data_controller.generate_unique_file_name(file_name=file.filename,project_id= project_id)

    async with aiofiles.open(file_path, 'wb') as buffer:
        while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
            await buffer.write(chunk)   


    return JSONResponse(content={"message": ResponseMessage})
