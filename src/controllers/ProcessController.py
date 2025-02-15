from .BaseController import BaseController 
from .ProjectControllers import ProjectController
import os 
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from models import ProcessingEnums


class ProcessController(BaseController):

    def __init__(self , project_id: str):
        super().__init__()
        self.project_id = project_id

        self.project_path =  ProjectController().get_project_path(self.project_id)


    def get_file_extension(self,file_id: str):
        return os.path.splitext(file_id)[-1]
    

    def get_file_loader(self,file_id: str ):

        file_path = os.path.join(self.project_path , file_id)

        if not os.path.exists(file_path):
            return None

        file_extension = self.get_file_extension(file_id)

        if file_extension in ProcessingEnums.TEXT_EXTENSIONS.value:
            return TextLoader(file_path=file_path , encoding="utf-8")
        elif file_extension in ProcessingEnums.PDF_EXTENSIONS.value:
            return PyMuPDFLoader(file_path=file_path , encoding="utf-8")
        else:
            return None
        

    def get_file_content(self,file_id: str):
        loader = self.get_file_loader(file_id)

        if loader :
            return loader.load()
        
        return None 
    

    def process_file_content(self,file_content: str , chunk_size: int , chunk_overlap: int ):

        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size , chunk_overlap=chunk_overlap , length_function=len)
        
        file_content_text = [
            rec.page_content for rec in file_content
        ]

        file_content_meta_data = [
            rec.metadata for rec in file_content
        ]

        chunks = splitter.create_documents(texts=file_content_text
                                           , metadatas=file_content_meta_data)


        return chunks
    
    
    




        
    
        
    
    
