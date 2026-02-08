from fastapi import FastAPI
from app.core.config import settings
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.db.session import SessionLocal
from app.db.seeds.initial_data import run_seeds



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
