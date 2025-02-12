from pydantic import BaseModel, Field, ConfigDict
from bson.objectid import ObjectId
from typing import Optional


class DataChunk(BaseModel):

    id :  Optional[ObjectId] = Field(None, alias='_id')
    chunk_text : str = Field(...,  min_length=1)
    chunk_metadata : dict
    chunk_index : int 
    chunk_project_id : ObjectId

    @classmethod
    def get_indexing(cls):

        return [
            {"key": [("chunk_project_id", 1)], "name": "chunk_project_id_index", "unique": False}
        ]
        



    model_config = ConfigDict(arbitrary_types_allowed=True)
