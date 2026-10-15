from dev_toolkit.random_utils import generate_uuid, random_string


def test_random_string():
    s = random_string(12)
    assert len(s) == 12


def test_generate_uuid():
    uid = generate_uuid()
    assert len(uid) == 32
