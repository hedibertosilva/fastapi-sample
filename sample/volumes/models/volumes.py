from pydantic import BaseModel, ConfigDict


class VolumeModel(BaseModel):
    id: int
    name: str
    size: int

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Volume 1",
                "size": 10,
            }
        }
    )