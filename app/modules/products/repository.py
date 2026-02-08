from sqlalchemy.orm import Session

from app.modules.products.models import Product, Category


def create_category(db: Session, category: Category):
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def create_product(db: Session, product: Product):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
