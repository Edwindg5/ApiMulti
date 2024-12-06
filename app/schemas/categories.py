from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    nombre_categoria: str
    descripcion_categoria: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id_categoria: Optional[int] = None	

    class Config:
        orm_mode = True
