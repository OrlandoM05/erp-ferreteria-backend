from sqlalchemy.orm import Session

from app.modules.inventory.models import Inventory, InventoryMovement


def get_inventory_by_product(db: Session, product_id: int):
    return db.query(Inventory).filter(Inventory.product_id == product_id).first()


def create_inventory(db: Session, inventory: Inventory):
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory


def update_inventory(db: Session, inventory: Inventory):
    db.commit()
    db.refresh(inventory)
    return inventory


def create_movement(db: Session, movement: InventoryMovement):
    db.add(movement)
    db.commit()
    return movement
