from pydantic import BaseModel


class InventoryCreate(BaseModel):
    product_id: int
    branch_id: int
    min_quantity: int = 0


class InventoryResponse(BaseModel):
    product_id: int
    branch_id: int
    quantity: int
    min_quantity: int

    class Config:
        from_attributes = True


class InventoryMovementCreate(BaseModel):
    product_id: int
    branch_id: int
    quantity: int
    reason: str