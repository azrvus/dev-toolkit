from dev_toolkit.masking import mask_email, mask_secret_string, sanitize_dict


def test_mask_email():
    masked = mask_email("developer@example.com")
    assert masked == "de*******@example.com"


def test_mask_secret_string():
    masked = mask_secret_string("super-secret-api-key-1234")
    assert masked.endswith("1234")


def test_sanitize_dict():
    payload = {
        "username": "alice",
        "email": "alice@example.com",
        "api_key": "secret_token_9999",
        "nested": {"password": "mypassword123"},
    }
    cleaned = sanitize_dict(payload)
    assert cleaned["username"] == "alice"
    assert cleaned["email"] == "al***@example.com"
    # Length of "secret_token_9999" is 17. 17 - 4 = 13 asterisks.
    assert cleaned["api_key"] == "*************9999"
    assert cleaned["nested"]["password"].endswith("d123")
