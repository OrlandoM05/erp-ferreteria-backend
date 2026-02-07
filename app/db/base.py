from app.db.registry import Base

# importar modelos para que Alembic los detecte
from app.modules.users.models import User  # noqa
