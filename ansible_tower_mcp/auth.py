#!/usr/bin/python
"""Ansible Tower Authentication Module.

Authentication priority:
1. **OIDC Delegation** — If ``ENABLE_DELEGATION`` is active, exchanges
   the IdP-issued user token for a downstream Ansible Tower access token
   via RFC 8693 Token Exchange.
2. **OAuth Client Credentials** — If ``ANSIBLE_CLIENT_ID`` and
   ``ANSIBLE_CLIENT_SECRET`` are set, uses the existing
   ``_authenticate_oauth()`` method on the Api class.
3. **Username / Password** — Falls back to ``ANSIBLE_USERNAME`` and
   ``ANSIBLE_PASSWORD`` with the native token-based auth.

See ``docs/guides/oauth_sso.md`` in agent-utilities for full details.
"""

import os
import threading

from agent_utilities.base_utilities import get_logger, to_boolean

local = threading.local()
from ansible_tower_mcp.api_client import Api

logger = get_logger(__name__)


def get_client():
    """Create an Ansible Tower API client with the best available auth method.

    Returns a new client on each call (no singleton) because Ansible Tower
    sessions may expire and tools run in independent request contexts.
    """
    from agent_utilities.mcp.delegated_auth import (
        get_delegated_token,
        get_user_identity,
        is_delegation_enabled,
    )

    base_url = os.environ.get("ANSIBLE_BASE_URL")
    verify = to_boolean(os.environ.get("ANSIBLE_VERIFY", "False"))

    # --- Path 1: OIDC Delegation (RFC 8693 Token Exchange) ---
    if is_delegation_enabled():
        try:
            delegated_token = get_delegated_token(
                audience=os.getenv("AUDIENCE", base_url),
                scopes=os.getenv("DELEGATED_SCOPES", "api"),
                verify=verify,
            )
            identity = get_user_identity()
            logger.info(
                "Using OIDC delegated token for Ansible Tower API",
                extra={
                    "user_email": identity.get("email"),
                    "base_url": base_url,
                },
            )
            return Api(
                base_url=base_url,
                token=delegated_token,
                verify=verify,
            )
        except Exception as e:
            logger.warning(f"OIDC delegation failed, falling back to credentials: {e}")

    # --- Path 2: OAuth Client Credentials ---
    client_id = os.environ.get("ANSIBLE_CLIENT_ID")
    client_secret = os.environ.get("ANSIBLE_CLIENT_SECRET")
    if client_id and client_secret:
        logger.info("Using OAuth client credentials for Ansible Tower API")
        return Api(
            base_url=base_url,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )

    # --- Path 3: Username / Password ---
    username = os.environ.get("ANSIBLE_USERNAME")
    password = os.environ.get("ANSIBLE_PASSWORD")
    logger.info("Using username/password credentials for Ansible Tower API")
    return Api(
        base_url=base_url,
        username=username,
        password=password,
        verify=verify,
    )
