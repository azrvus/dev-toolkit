from dev_toolkit.crypto_utils import generate_token, md5_hash, sha256_hash


def test_generate_token():
    token = generate_token(16)
    assert isinstance(token, str)
    assert len(token) == 32


def test_sha256_hash():
    h = sha256_hash("hello")
    assert len(h) == 64


def test_md5_hash():
    h = md5_hash("hello")
    assert len(h) == 32
