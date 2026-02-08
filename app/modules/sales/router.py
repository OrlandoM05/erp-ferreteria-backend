from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.modules.sales import service
from app.modules.sales.schemas import SaleCreate, SaleResponse

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.post("", response_model=SaleResponse)
def create_sale(
    data: SaleCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    sale = service.process_sale(
        db=db,
        items=data.items,
        user_id=user.id,
    )
    return sale
