from __future__ import annotations

from typing import Any

__all__ = ["paginate"]


def paginate(items: list[Any], page: int = 1, page_size: int = 10) -> dict[str, Any]:
    """Paginate a list of items and return items with metadata."""
    page = max(page, 1)
    page_size = max(page_size, 1)

    total_items = len(items)
    total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1

    start = (page - 1) * page_size
    end = start + page_size

    paginated_items = items[start:end]

    return {
        "items": paginated_items,
        "page": page,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }
