from backend.tools.idea_classifier import classify_idea


def test_classifies_saas():
    assert classify_idea("A B2B analytics dashboard for sales teams") == "saas"


def test_classifies_marketplace():
    assert classify_idea("A marketplace connecting buyers and sellers of used furniture") == "marketplace"


def test_defaults_to_saas_when_unclear():
    assert classify_idea("Something completely generic") == "saas"