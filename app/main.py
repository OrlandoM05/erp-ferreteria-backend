from fastapi import FastAPI
from app.core.config import settings
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.db.session import SessionLocal
from app.db.seeds.initial_data import run_seeds
from app.modules.products.router import router as products_router
from app.modules.inventory.router import router as inventory_router
from app.modules.suppliers.router import router as suppliers_router
from app.modules.purchases.router import router as purchases_router
from app.modules.finance.router import router as finance_router
from app.modules.sales.router import router as sales_router
from app.modules.reports.router import router as reports_router


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": False
    }
)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
app.include_router(auth_router)
app.include_router(users_router)

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        run_seeds(db)
    finally:
        db.close()

app.include_router(products_router)
app.include_router(inventory_router)
app.include_router(suppliers_router)
app.include_router(purchases_router)
app.include_router(finance_router)
app.include_router(sales_router)
app.include_router(reports_router)
#PASO NUMERO 79