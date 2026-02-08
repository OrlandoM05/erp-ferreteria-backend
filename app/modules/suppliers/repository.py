from sqlalchemy.orm import Session
from app.modules.suppliers.models import Supplier, ProductSupplier


def create_supplier(db: Session, supplier: Supplier):
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


def create_product_supplier(db: Session, ps: ProductSupplier):
    db.add(ps)
    db.commit()
    db.refresh(ps)
    return ps
