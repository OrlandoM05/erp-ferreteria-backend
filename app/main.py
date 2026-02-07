from fastapi import FastAPI
from app.core.config import settings
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router



app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
app.include_router(auth_router)
app.include_router(users_router)