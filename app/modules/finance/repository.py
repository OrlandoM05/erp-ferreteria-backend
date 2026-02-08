from sqlalchemy.orm import Session
from app.modules.finance.models import Payable


def create_payable(db: Session, payable: Payable):
    db.add(payable)
    db.commit()
    db.refresh(payable)
    return payable


def list_payables(db: Session):
    return db.query(Payable).all()
