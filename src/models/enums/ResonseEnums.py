from enum import Enum

class ResponseMessage(Enum):
    FILETYPENOTSUPPORTED = "File type not supported"
    FILEUPLOADSUCCESS = "File uploaded successfully"
    FILEUPLOADFAILED = "File upload failed"
    FILESIZEEXCEEDED = "File size exceeded"
    FileNotFoundError = "File not found"
    FILEPROCESSINGFAILED = "File processing failed"
    FILEPROCESSINGSUCCESS = "File processing success"
    PROJECTCREATED = "Project created successfully"
    PROJECTNOTFOUND = "Project not found"
    PROJECTDELETED = "Project deleted successfully"
    PROJECTUPDATED = "Project updated successfully"
    NOFILEERROR = "No file uploaded"
    FILENOTEXIST = "File does not exist"
    INSERTINTOVECTORDBERROR = "Insert into vector db error"
    INSERTINTOVECTORDBSUCCESS = "Insert into vector db success"
    VECTORDB_COLLECTION_RETRIEVED = "vectordb_collection_retrieved"
    VECTORDB_SEARCH_ERROR = "vectordb_search_error"
    VECTORDB_SEARCH_SUCCESS = "vectordb_search_success"
    RAG_ANSWER_ERROR = "rag_answer_error"
    RAG_ANSWER_SUCCESS = "rag_answer_success"




