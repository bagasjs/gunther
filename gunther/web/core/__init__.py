from pydantic import BaseModel as PydanticBaseModel, ConfigDict, Field as DTOField
from gunther.web.core.db import gunther_sessionmaker, Model as BaseDBModel

class BaseDTOModel(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)
