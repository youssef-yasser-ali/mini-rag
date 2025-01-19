from enum import Enum

class ResponseMessage(Enum):
    FILETYPENOTSUPPORTED = "File type not supported"
    FILEUPLOADSUCCESS = "File uploaded successfully"
    FILEUPLOADFAILED = "File upload failed"
    FILESIZEEXCEEDED = "File size exceeded"
    FileNotFoundError = "File not found"



