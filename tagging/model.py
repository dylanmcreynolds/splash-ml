from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Extra, Field
from typing import Dict, List, Optional

LABEL_NAME = "label"

# https://www.mongodb.com/blog/post/building-with-patterns-the-schema-versioning-pattern
SCHEMA_VERSION = "1.0"


class Persistable(BaseModel):
    uid: Optional[str]


class ModelInfo(BaseModel):
    label_index: Optional[Dict[str, float]]


      
class TagSource(Persistable):

    schema_version: str = SCHEMA_VERSION
    model_info: Optional[ModelInfo]
    type: str
    name: Optional[str] = Field(description="optional name of model that produces tags")

    class Config:
        extra = Extra.forbid


class TaggingEvent(Persistable):
    schema_version: str = SCHEMA_VERSION
    tagger_id: str
    run_time: datetime
    accuracy: Optional[float] = Field(ge=0.0, le=1.0)

    class Config:
        extra = Extra.forbid


class Tag(BaseModel):
    name: str
    value: str
    confidence: Optional[float]
    event_id: Optional[str] = None


class DatasetType(str, Enum):
    dbroker = "dbroker"
    file = "file"
    web = "web"



    assets: List[str]
    models: Dict[str, int] # model and the quality of that model when run against a model


class Dataset(Persistable):
    schema_version: str = SCHEMA_VERSION
    type: DatasetType
    uri: str
    location_kwargs: Optional[Dict[str, str]]
    sample_id: Optional[str]
    tags: Optional[List[Tag]]

    class Config:
        extra = Extra.forbid


class FileDataset(Dataset):
    type = DatasetType.file

