from src.analytics import get_zone


def test_zone_1():
    assert get_zone(119) == "Zone 1"


def test_zone_2():
    assert get_zone(120) == "Zone 2"
    assert get_zone(139) == "Zone 2"


def test_zone_3():
    assert get_zone(140) == "Zone 3"
    assert get_zone(154) == "Zone 3"


def test_zone_4():
    assert get_zone(155) == "Zone 4"
    assert get_zone(169) == "Zone 4"


def test_zone_5():
    assert get_zone(170) == "Zone 5"