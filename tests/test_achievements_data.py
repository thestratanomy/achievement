from src.achievements_data import get_facts, CATEGORIES


def test_categories_contains_all_required():
    """Test that CATEGORIES contains all required sectors."""
    required = {"Infrastructure", "Economy", "Industries", "Law & Order", "Health", "Education", "Agriculture"}
    assert required.issubset(set(CATEGORIES))


def test_get_facts_single_category():
    """Test retrieving facts from a single category."""
    facts = get_facts(["Infrastructure"])
    assert len(facts) > 0
    assert all(isinstance(f, str) for f in facts)


def test_get_facts_multiple_categories():
    """Test retrieving facts from multiple categories."""
    facts = get_facts(["Economy", "Industries"])
    assert len(facts) >= 2


def test_get_facts_empty_returns_all():
    """Test that empty category list returns all facts."""
    all_facts = get_facts([])
    assert len(all_facts) > 10
