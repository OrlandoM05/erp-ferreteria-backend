import uuid

from app.modules.products.models import Product, Category


def generate_sku() -> str:
    return f"SKU-{uuid.uuid4().hex[:8].upper()}"


def resolve_margin(product: Product) -> float | None:
    if product.margin is not None:
        return product.margin
    if product.category and product.category.margin is not None:
        return product.category.margin
    return None
