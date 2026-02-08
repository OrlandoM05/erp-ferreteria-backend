from datetime import timedelta, date
from sqlalchemy.orm import Session

from app.modules.finance.models import Payable
from app.modules.purchases.models import PurchaseOrder


def create_payable_from_order(
    db: Session,
    order: PurchaseOrder,
    amount: float,
    credit_days: int,
):
    due_date = date.today() + timedelta(days=credit_days)

    payable = Payable(
        supplier_id=order.supplier_id,
        purchase_order_id=order.id,
        amount=amount,
        due_date=due_date,
    )

    db.add(payable)
    db.commit()
    return payable


def update_status(payable: Payable):
    if payable.status == "PAGADO":
        return payable.status

    if date.today() > payable.due_date:
        payable.status = "VENCIDO"
    else:
        payable.status = "PENDIENTE"

    return payable.status
