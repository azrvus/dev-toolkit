from dev_toolkit.pagination import paginate


def test_paginate_basic():
    items = list(range(25))
    result = paginate(items, page=1, page_size=10)

    assert result["page"] == 1
    assert result["page_size"] == 10
    assert result["total_items"] == 25
    assert result["total_pages"] == 3
    assert result["has_next"] is True
    assert result["has_prev"] is False
    assert result["items"] == list(range(10))


def test_paginate_edge_cases():
    items = [1, 2, 3]
    result = paginate(items, page=5, page_size=2)

    assert result["page"] == 5
    assert result["items"] == []
    assert result["has_next"] is False
    assert result["has_prev"] is True
