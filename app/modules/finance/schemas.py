from datetime import date
from pydantic import BaseModel


class PayableResponse(BaseModel):
    id: int
    supplier_id: int
    purchase_order_id: int
    amount: float
    due_date: date
    status: str

    class Config:
        from_attributes = True
