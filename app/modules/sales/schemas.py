from pydantic import BaseModel


class SaleItemCreate(BaseModel):
    barcode: str
    quantity: int


class SaleCreate(BaseModel):
    items: list[SaleItemCreate]


class SaleResponse(BaseModel):
    id: int
    total: float

    class Config:
        from_attributes = True
