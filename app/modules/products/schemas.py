from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    margin: float | None = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    margin: float | None

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str
    category_id: int
    barcode: str | None = None
    margin: float | None = None


class ProductResponse(BaseModel):
    id: int
    sku: str
    name: str
    barcode: str | None
    margin: float | None
    category_id: int

    class Config:
        from_attributes = True
