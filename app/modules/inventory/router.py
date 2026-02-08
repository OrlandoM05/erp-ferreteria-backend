from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user, require_role
from app.modules.inventory import service
from app.modules.inventory.models import Inventory
from app.modules.inventory.schemas import (
    InventoryCreate,
    InventoryResponse,
    InventoryMovementCreate,
)

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.post("", response_model=InventoryResponse)
def create_inventory_endpoint(
    data: InventoryCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("Admin", "Almacen")),
):
    inventory = Inventory(
        product_id=data.product_id,
        min_quantity=data.min_quantity,
        quantity=0,
    )
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory


@router.post("/in", response_model=InventoryResponse)
def add_stock_endpoint(
    data: InventoryMovementCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    inventory = service.add_stock(
        db=db,
        product_id=data.product_id,
        quantity=data.quantity,
        user_id=user.id,
        reason=data.reason,
    )
    return inventory


@router.post("/out", response_model=InventoryResponse)
def remove_stock_endpoint(
    data: InventoryMovementCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    inventory = service.remove_stock(
        db=db,
        product_id=data.product_id,
        quantity=data.quantity,
        user_id=user.id,
        reason=data.reason,
    )
    return inventory
