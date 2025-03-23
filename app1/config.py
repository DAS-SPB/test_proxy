import os
import hvac


# to read vault token from Docker secrets
def get_vault_token() -> str:
    try:
        with open("/run/secrets/vault_token", "r") as f:
            return f.read().strip()
    except Exception as e:
        raise Exception("Unable to read vault token from /run/secrets/vault_token") from e


VAULT_URL = os.getenv("VAULT_URL", "http://vault:8200")
VAULT_TOKEN = get_vault_token()
VAULT_PATH = "app1"


def load_config() -> dict:
    client = hvac.Client(url=VAULT_URL, token=VAULT_TOKEN)
    secret_response = client.secrets.kv.v2.read_secret_version(path=VAULT_PATH)
    return secret_response["data"]["data"]


CONFIG = load_config()
