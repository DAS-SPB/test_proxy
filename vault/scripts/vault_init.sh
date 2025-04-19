#!/usr/bin/env sh
set -e

VAULT_ADDR="http://vault:8200"
VAULT_TOKEN="${VAULT_DEV_ROOT_TOKEN_ID}"
export VAULT_ADDR VAULT_TOKEN

# 1) waiting fot vault to start
until vault status -format=json >/dev/null 2>&1; do
  sleep 1
done

# 2) app1 secrets
vault kv put secret/app1 \
    token_secret_key="${APP1_TOKEN_SECRET_KEY}" \
    token_algorithm="${APP1_TOKEN_ALG}" \
    token_issuer="${APP1_TOKEN_ISSUER}" \
    token_audience="${APP1_TOKEN_AUD}" \
    token_expiration_time="${APP1_TOKEN_EXPIRATION}" \
    api_key="${APP1_API_KEY}" \
    app2_api_key="${APP1_APP2_API_KEY}" \
    app2_url="${APP1_APP2_URL}"

# 3) proxy secrets
vault kv put secret/proxy \
    app2_url="${PROXY_APP2_URL}"

# 4) app2 secrets
vault kv put secret/app2 \
    api_key="${APP2_API_KEY}"
