from app.db.registry import Base

# Users & Auth
from app.modules.users.models import User  # noqa
from app.modules.users.roles_models import Role, Permission  # noqa

# Core business
from app.modules.branches.models import Branch  # noqa

# Products & Inventory
from app.modules.products.models import Product, Category  # noqa
from app.modules.inventory.models import Inventory, InventoryMovement  # noqa

# Suppliers & Purchases
from app.modules.suppliers.models import Supplier, ProductSupplier  # noqa
from app.modules.purchases.models import PurchaseOrder, PurchaseOrderItem  # noqa

# Finance
from app.modules.finance.models import Payable  # noqa

# Sales
from app.modules.sales.models import Sale, SaleItem  # noqa


