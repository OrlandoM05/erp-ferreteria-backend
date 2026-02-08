"""inventory multi branch

Revision ID: 91a20350df00
Revises: 60e2aaedbf32
Create Date: 2026-02-07
"""

from alembic import op
import sqlalchemy as sa

# 🔹 IDs de Alembic (OBLIGATORIOS)
revision = "91a20350df00"
down_revision = "60e2aaedbf32"
branch_labels = None
depends_on = None


def upgrade():
    # 1️⃣ crear tabla branches
    op.create_table(
        "branches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False, unique=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )

    # 2️⃣ insertar sucursal por defecto
    op.execute(
        "INSERT INTO branches (name, is_active) VALUES ('Matriz', true)"
    )

    # 3️⃣ agregar branch_id PERMITIENDO NULL
    op.add_column(
        "inventory",
        sa.Column("branch_id", sa.Integer(), nullable=True),
    )

    # 4️⃣ asignar branch_id = 1 a inventario existente
    op.execute(
        "UPDATE inventory SET branch_id = 1"
    )

    # 5️⃣ ahora sí hacerlo NOT NULL
    op.alter_column(
        "inventory",
        "branch_id",
        nullable=False,
    )

    # 6️⃣ foreign key
    op.create_foreign_key(
        "inventory_branch_fk",
        "inventory",
        "branches",
        ["branch_id"],
        ["id"],
    )

    # 7️⃣ unique constraint
    op.create_unique_constraint(
        "uq_inventory_branch_product",
        "inventory",
        ["branch_id", "product_id"],
    )


def downgrade():
    op.drop_constraint("uq_inventory_branch_product", "inventory", type_="unique")
    op.drop_constraint("inventory_branch_fk", "inventory", type_="foreignkey")
    op.drop_column("inventory", "branch_id")
    op.drop_table("branches")
