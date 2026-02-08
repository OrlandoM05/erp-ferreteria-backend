from alembic import op
import sqlalchemy as sa

revision = "cbebe1f73d95"
down_revision = "91a20350df00"
branch_labels = None
depends_on = None


def upgrade():
    # 1️⃣ agregar columna permitiendo NULL
    op.add_column(
        "users",
        sa.Column("branch_id", sa.Integer(), nullable=True),
    )

    # 2️⃣ asignar sucursal Matriz a usuarios existentes
    op.execute(
        "UPDATE users SET branch_id = 1"
    )

    # 3️⃣ ahora sí NOT NULL
    op.alter_column(
        "users",
        "branch_id",
        nullable=False,
    )

    # 4️⃣ foreign key
    op.create_foreign_key(
        "users_branch_fk",
        "users",
        "branches",
        ["branch_id"],
        ["id"],
    )


def downgrade():
    op.drop_constraint("users_branch_fk", "users", type_="foreignkey")
    op.drop_column("users", "branch_id")
