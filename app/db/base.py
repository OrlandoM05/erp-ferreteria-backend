from app.db.registry import Base

from app.modules.users.models import User  # noqa
from app.modules.users.roles_models import Role, Permission  # noqa
from app.modules.products.models import Product, Category  # noqa
from app.modules.inventory.models import Inventory, InventoryMovement  # noqa
from app.modules.suppliers.models import Supplier, ProductSupplier  # noqa
from app.modules.purchases.models import PurchaseOrder, PurchaseOrderItem  # noqa
from app.modules.finance.models import Payable  # noqa

