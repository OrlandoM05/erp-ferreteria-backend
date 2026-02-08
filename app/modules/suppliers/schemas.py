from pydantic import BaseModel


class SupplierCreate(BaseModel):
    name: str
    credit_days: int = 0
    delivery_days: int = 0


class SupplierResponse(BaseModel):
    id: int
    name: str
    credit_days: int
    delivery_days: int

    class Config:
        from_attributes = True


class ProductSupplierCreate(BaseModel):
    product_id: int
    supplier_id: int
    supplier_sku: str
    price: float
    credit_days: int
    delivery_days: int
