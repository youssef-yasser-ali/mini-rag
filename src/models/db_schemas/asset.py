from pydantic import BaseModel, Field, ConfigDict
from bson.objectid import ObjectId
from typing import Optional
from datetime import datetime

class Asset(BaseModel):
    id :  Optional[ObjectId] = Field(None, alias='_id')
    asset_project_id : ObjectId
    asset_type : str = Field(...,  min_length=1)
    asset_name : str = Field(...,  min_length=1)
    asset_size : int = Field(ge= 0 , default= None )
    asset_pushed_at : datetime = Field(default=datetime.utcnow()) 
    asset_config : dict = Field(default={})


    @classmethod
    def get_indexing(cls):

        return [
            {"key": [("asset_project_id", 1)], "name": "asset_project_id_index", "unique": False} , 
            {"key": [('asset_project_id', 1),("asset_name", 1)], "name": "asset_project_id_name_index", "unique": True}
        ]
         

    model_config = ConfigDict(arbitrary_types_allowed=True)
