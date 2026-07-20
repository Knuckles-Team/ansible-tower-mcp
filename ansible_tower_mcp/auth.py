#!/usr/bin/python
"""Ansible Tower Authentication Module.

CONCEPT:AT-OS.identity.resolve-best-authentication-client: Authentication Layer (OIDC, OAuth, Username/Password).

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

import threading

from agent_utilities.base_utilities import get_logger
from agent_utilities.core.config import setting
from agent_utilities.core.transport_security import resolve_configured_tls_profile

local = threading.local()
from ansible_tower_mcp.api_client import Api

logger = get_logger(__name__)


def get_client():
    """Create an Ansible Tower API client with the best available auth method.

    CONCEPT:AT-OS.identity.resolve-best-authentication-client: Resolve the best authentication client based on OIDC, OAuth, or username/password credentials.

    Returns a new client on each call (no singleton) because Ansible Tower
    sessions may expire and tools run in independent request contexts.
    """
    from agent_utilities.mcp.delegated_auth import (
        get_delegated_token,
        is_delegation_enabled,
    )

    base_url = setting("ANSIBLE_BASE_URL")
    tls_profile = resolve_configured_tls_profile(
        "ANSIBLE_TOWER",
        profile_name=setting("ANSIBLE_TOWER_TLS_PROFILE"),
    )

    # --- Path 1: OIDC Delegation (RFC 8693 Token Exchange) ---
    if is_delegation_enabled():
        try:
            delegated_token = get_delegated_token(
                audience=setting("AUDIENCE", base_url),
                scopes=setting("DELEGATED_SCOPES", "api"),
            )
            logger.info("Using OIDC delegated token for Ansible Tower API")
            return Api(
                base_url=base_url,
                token=delegated_token,
                tls_profile=tls_profile,
            )
        except Exception:
            logger.warning(
                "OIDC delegation failed; trying the configured credential fallback"
            )

    # --- Path 2: OAuth Client Credentials ---
    client_id = setting("ANSIBLE_CLIENT_ID")
    client_secret = setting("ANSIBLE_CLIENT_SECRET")
    if client_id and client_secret:
        logger.info("Using OAuth client credentials for Ansible Tower API")
        return Api(
            base_url=base_url,
            client_id=client_id,
            client_secret=client_secret,
            tls_profile=tls_profile,
        )

    # --- Path 3: Username / Password ---
    username = setting("ANSIBLE_USERNAME")
    password = setting("ANSIBLE_PASSWORD")
    logger.info("Using username/password credentials for Ansible Tower API")
    return Api(
        base_url=base_url,
        username=username,
        password=password,
        tls_profile=tls_profile,
    )
