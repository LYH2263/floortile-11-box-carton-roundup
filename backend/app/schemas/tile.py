from pydantic import BaseModel, Field


class TileBoxSizeUpdate(BaseModel):
    box_size: int = Field(..., gt=0, description="每箱片数 N，必须为正整数")
