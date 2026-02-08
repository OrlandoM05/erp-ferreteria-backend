from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import require_role
from app.modules.finance import repository, service
from app.modules.finance.models import Payable
from app.modules.finance.schemas import PayableResponse
from fastapi import HTTPException

router = APIRouter(prefix="/finance", tags=["Finance"])


@router.get("/payables", response_model=list[PayableResponse])
def list_payables(
    db: Session = Depends(get_db),
    user=Depends(require_role("Admin", "Gerente")),
):
    payables = repository.list_payables(db)
    for p in payables:
        service.update_status(p)
    db.commit()
    return payables


@router.post("/payables/{payable_id}/pay")
def pay_payable(
    payable_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("Admin", "Gerente")),
):
    payable = db.get(Payable, payable_id)

    if not payable:
        raise HTTPException(
            status_code=404,
            detail="Payable not found"
        )

    # 🔒 Regla ERP: no se puede pagar dos veces
    if payable.status == "PAGADO":
        raise HTTPException(
            status_code=400,
            detail="Payable already paid"
        )

    payable.status = "PAGADO"
    db.commit()

    return {"status": "paid"}
