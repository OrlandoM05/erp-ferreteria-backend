from pydantic import BaseModel


class PurchaseItemCreate(BaseModel):
    product_id: int
    supplier_sku: str
    price: float
    quantity: int


class PurchaseOrderCreate(BaseModel):
    supplier_id: int
    items: list[PurchaseItemCreate]


class PurchaseReceiveItem(BaseModel):
    item_id: int
    quantity_received: int
