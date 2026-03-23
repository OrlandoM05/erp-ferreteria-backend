from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.inventory.models import Inventory, InventoryMovement


def add_stock(
    db: Session,
    product_id: int,
    branch_id: int,
    quantity: int,
    user_id: int,
    reason: str,
):
    inventory = db.query(Inventory).filter_by(
        product_id=product_id,
        branch_id=branch_id,
    ).first()

    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    inventory.quantity += quantity

    movement = InventoryMovement(
        product_id=product_id,
        user_id=user_id,
        type="IN",
        quantity=quantity,
        reason=reason,
    )

    db.add(movement)
    db.commit()
    db.refresh(inventory)
    return inventory


def remove_stock(
    db: Session,
    product_id: int,
    branch_id: int,
    quantity: int,
    user_id: int,
    reason: str,
):
    inventory = db.query(Inventory).filter_by(
        product_id=product_id,
        branch_id=branch_id,
    ).first()

    if not inventory:
        raise HTTPException(
            status_code=404,
            detail="Inventory not found",
        )

    if inventory.quantity < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock",
        )

    inventory.quantity -= quantity

    movement = InventoryMovement(
        product_id=product_id,
        user_id=user_id,
        type="OUT",
        quantity=quantity,
        reason=reason,
    )

    db.add(movement)
    db.commit()
    db.refresh(inventory)
    return inventory