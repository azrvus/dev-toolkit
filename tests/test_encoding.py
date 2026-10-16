from dev_toolkit.encoding import base64_decode, base64_encode


def test_base64_roundtrip():
    original = "Hello, Dev Toolkit!"
    encoded = base64_encode(original)
    decoded = base64_decode(encoded)
    assert decoded == original
