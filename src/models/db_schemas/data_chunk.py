from pydantic import BaseModel , Field
from bson.objectid import ObjectId
from typing import Optional


class data_chunk(BaseModel):
    _id :  Optional[ObjectId]
    chunk_text : str = Field(...,  min_length=1)
    chunk_metadata : dict 
    chunk_index : int = Field(...,  gt=0)
    chunk_project_id : ObjectId 
    



    


    class config:
        arbitary_types_allowed = True