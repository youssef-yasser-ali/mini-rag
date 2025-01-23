from pydantic import BaseModel ,Field,  field_validator
from typing import List, Optional
from bson.objectid import ObjectId

class project(BaseModel):
    _id :  Optional[ObjectId]
    project_id : str = Field(...,  min_length=1)



    @field_validator('project_id')
    def project_id_validator(cls, v):
        if not v.isalnum():
            raise ValueError('project_id must be alphanumeric')
        return v



    class config:
        arbitary_types_allowed = True

