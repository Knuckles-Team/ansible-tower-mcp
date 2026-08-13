import asyncio
import inspect
import json
import os
import re
import runpy
import sys
from unittest.mock import ANY, MagicMock, patch

import pytest

import ansible_tower_mcp
from ansible_tower_mcp.api_client import Api

# ==========================================
# 1. Test Lazy Imports & init
# ==========================================


def test_lazy_imports():
    # Test __dir__
    d = dir(ansible_tower_mcp)
    assert len(d) > 0

    # Test attributes
    assert ansible_tower_mcp._MCP_AVAILABLE is True
    assert ansible_tower_mcp._AGENT_AVAILABLE is True

    # Clear optional module cache and globals/sys.modules to trigger the raw lazy load attribute return path
    import sys

    sys.modules.pop("ansible_tower_mcp.mcp.mcp_server", None)
    ansible_tower_mcp._loaded_optional_modules.pop(
        "ansible_tower_mcp.mcp.mcp_server", None
    )
    ansible_tower_mcp.__dict__.pop("register_inventory_tools", None)
    ansible_tower_mcp.__dict__.pop("mcp_server", None)

    # Lazy load and retrieve an optional module member to cover return getattr(module, name) (line 69)
    mcp_server_fn = ansible_tower_mcp.register_inventory_tools
    assert mcp_server_fn is not None

    # Test AttributeError
    with pytest.raises(AttributeError):
        _ = ansible_tower_mcp.non_existent_attribute_xyz

    # Test missing module (mock ImportError)
    with patch(
        "importlib.import_module", side_effect=ImportError("mocked import error")
    ):
        from ansible_tower_mcp import _import_module_safely

        assert _import_module_safely("non_existent_module_name") is None

        # Bypass caching dynamically by testing __getattr__ directly on False paths
        with patch.dict(ansible_tower_mcp.OPTIONAL_MODULES, {}, clear=True):
            assert ansible_tower_mcp.__getattr__("_MCP_AVAILABLE") is False
            assert ansible_tower_mcp.__getattr__("_AGENT_AVAILABLE") is False


# ==========================================
# 2. Test Agent Server CLI & Entry Points
# ==========================================


def test_agent_server_cli():
    with patch("sys.argv", ["agent_server.py", "--debug"]):
        with patch("agent_utilities.create_agent_server") as mock_server:
            with (
                patch("agent_utilities.initialize_workspace"),
                patch(
                    "agent_utilities.load_identity", return_value={"name": "Test Agent"}
                ),
            ):
                runpy.run_module("ansible_tower_mcp.agent_server", run_name="__main__")
                mock_server.assert_called_once()
                assert mock_server.call_args[1]["debug"] is True

    with patch("sys.argv", ["ansible_tower_mcp"]):
        with patch("ansible_tower_mcp.agent_server.agent_server") as mock_agent_server:
            runpy.run_module("ansible_tower_mcp.__main__", run_name="__main__")
            mock_agent_server.assert_called_once()


# ==========================================
# 3. Test Authentication Flows
# ==========================================


def test_auth_flows():
    orig_delegated_auth = sys.modules.get("agent_utilities.mcp.delegated_auth")
    mock_delegated_auth = MagicMock()
    sys.modules["agent_utilities.mcp.delegated_auth"] = mock_delegated_auth

    try:
        from ansible_tower_mcp.auth import get_client

        # Path 1: OIDC Delegation
        mock_delegated_auth.is_delegation_enabled.return_value = True
        mock_delegated_auth.get_delegated_token.return_value = "example_delegated_token"
        mock_delegated_auth.get_user_identity.return_value = {"email": "user@test.com"}

        with patch.dict(
            os.environ, {"ANSIBLE_BASE_URL": "http://test", "ENABLE_DELEGATION": "True"}
        ):
            with patch("ansible_tower_mcp.auth.Api") as mock_api_class:
                _ = get_client()
                mock_api_class.assert_called_once_with(
                    base_url="http://test",
                    token="example_delegated_token",
                    tls_profile=ANY,
                )

        # Path 1 Failure Fallback to Username/Password
        mock_delegated_auth.is_delegation_enabled.return_value = True
        mock_delegated_auth.get_delegated_token.side_effect = Exception(
            "Delegation failed"
        )

        with patch.dict(
            os.environ,
            {
                "ANSIBLE_BASE_URL": "http://test",
                "ENABLE_DELEGATION": "True",
                "ANSIBLE_USERNAME": "test_user",
                "ANSIBLE_PASSWORD": "test_password",
            },
        ):
            with patch("ansible_tower_mcp.auth.Api") as mock_api_class:
                _ = get_client()
                mock_api_class.assert_called_once_with(
                    base_url="http://test",
                    username="test_user",
                    password="test_password",
                    tls_profile=ANY,
                )

        # Path 2: OAuth Client Credentials
        mock_delegated_auth.is_delegation_enabled.return_value = False

        with patch.dict(
            os.environ,
            {
                "ANSIBLE_BASE_URL": "http://test",
                "ANSIBLE_CLIENT_ID": "client_id_123",
                "ANSIBLE_CLIENT_SECRET": "example_client_secret",
            },
        ):
            with patch("ansible_tower_mcp.auth.Api") as mock_api_class:
                _ = get_client()
                mock_api_class.assert_called_once_with(
                    base_url="http://test",
                    client_id="client_id_123",
                    client_secret="example_client_secret",
                    tls_profile=ANY,
                )

        # Path 3: Username / Password Fallback
        mock_delegated_auth.is_delegation_enabled.return_value = False

        with patch.dict(
            os.environ,
            {
                "ANSIBLE_BASE_URL": "http://test",
                "ANSIBLE_USERNAME": "test_user",
                "ANSIBLE_PASSWORD": "test_password",
            },
        ):
            with patch("ansible_tower_mcp.auth.Api") as mock_api_class:
                _ = get_client()
                mock_api_class.assert_called_once_with(
                    base_url="http://test",
                    username="test_user",
                    password="test_password",
                    tls_profile=ANY,
                )
    finally:
        if orig_delegated_auth is not None:
            sys.modules["agent_utilities.mcp.delegated_auth"] = orig_delegated_auth
        else:
            sys.modules.pop("agent_utilities.mcp.delegated_auth", None)


# ==========================================
# 4. Test API Client Base Edge Cases
# ==========================================


def test_api_client_base_edge_cases():
    from ansible_tower_mcp.api.api_client_base import BaseApiClient

    # 1. Base URL is required validation
    with pytest.raises(ValueError, match="base_url is required"):
        BaseApiClient(base_url=None)

    # 2. Runtime transport profile is applied to the session.
    tls_profile = MagicMock()
    client_profile = BaseApiClient(
        base_url="http://test", token="abc", tls_profile=tls_profile
    )
    assert client_profile.tls_profile is tls_profile
    tls_profile.configure_requests_session.assert_called_once_with(
        client_profile._session
    )

    # 3. Missing auth credentials validation
    with pytest.raises(ValueError, match="Must provide either a token"):
        BaseApiClient(base_url="http://test")

    # 4. OAuth authentication fail flow
    client_oauth = BaseApiClient(
        base_url="http://test", client_id="id", client_secret="secret"
    )
    mock_resp_fail = MagicMock()
    mock_resp_fail.status_code = 400
    mock_resp_fail.text = "invalid_client"
    with patch.object(client_oauth._session, "post", return_value=mock_resp_fail):
        with pytest.raises(Exception, match="OAuth authentication failed"):
            client_oauth._authenticate_oauth()

    # 5. OAuth authentication success flow
    mock_resp_oauth_ok = MagicMock()
    mock_resp_oauth_ok.status_code = 200
    mock_resp_oauth_ok.json.return_value = {"access_token": "oauth_token_123"}
    with patch.object(client_oauth._session, "post", return_value=mock_resp_oauth_ok):
        client_oauth._authenticate_oauth()
        assert client_oauth.token == "oauth_token_123"

    # 6. OAuth success flow but empty token response check
    mock_resp_oauth_empty = MagicMock()
    mock_resp_oauth_empty.status_code = 200
    mock_resp_oauth_empty.json.return_value = {}
    with patch.object(
        client_oauth._session, "post", return_value=mock_resp_oauth_empty
    ):
        with pytest.raises(Exception, match="No access_token received"):
            client_oauth._authenticate_oauth()

    # 7. get_token with cookie check
    client_pw = BaseApiClient(base_url="http://test", username="user", password="pw")
    client_pw._session.cookies.update({"csrftoken": "session_csrf"})

    mock_login_cookie = MagicMock()
    mock_login_cookie.cookies = {"csrftoken": "cookie_csrf"}

    mock_token_created = MagicMock()
    mock_token_created.status_code = 201
    mock_token_created.json.return_value = {"token": "dynamic_token_1"}

    with (
        patch.object(client_pw._session, "get", return_value=mock_login_cookie),
        patch.object(client_pw._session, "post", return_value=mock_token_created),
    ):
        token = client_pw.get_token()
        assert token == "dynamic_token_1"
        assert client_pw.token == "dynamic_token_1"

    # 8. get_token with regex fallback and token creation failure
    mock_login_regex = MagicMock()
    mock_login_regex.cookies = {}
    mock_login_regex.text = 'name="csrfmiddlewaretoken" value="regex_csrf"'

    mock_token_fail = MagicMock()
    mock_token_fail.status_code = 400
    mock_token_fail.text = "creation failed"

    with (
        patch.object(client_pw._session, "get", return_value=mock_login_regex),
        patch.object(client_pw._session, "post") as mock_post_fail,
    ):
        mock_login_post = MagicMock()
        mock_login_post.status_code = 200

        mock_post_fail.side_effect = [mock_login_post, mock_token_fail]

        with pytest.raises(Exception, match="Token creation failed"):
            client_pw.get_token()

    # 9. get_token with login failure (HTTP >= 400)
    mock_login_fail = MagicMock()
    mock_login_fail.cookies = {"csrftoken": "csrf"}
    mock_login_fail.status_code = 403
    mock_login_fail.text = "forbidden"

    with (
        patch.object(client_pw._session, "get", return_value=mock_login_fail),
        patch.object(client_pw._session, "post", return_value=mock_login_fail),
    ):
        with pytest.raises(Exception, match="Login failed"):
            client_pw.get_token()

    # 10. get_token missing CSRF token exception
    mock_login_no_csrf = MagicMock()
    mock_login_no_csrf.cookies = {}
    mock_login_no_csrf.text = "nothing here"

    with patch.object(client_pw._session, "get", return_value=mock_login_no_csrf):
        with pytest.raises(Exception, match="Could not obtain CSRF token"):
            client_pw.get_token()

    # 11. Headers generation triggering get_token/oauth logic
    client_pw_headers = BaseApiClient(
        base_url="http://test", username="user", password="pw"
    )
    with patch.object(client_pw_headers, "get_token") as mock_get_token:
        _ = client_pw_headers.get_headers()
        mock_get_token.assert_called_once()

    client_oauth_headers = BaseApiClient(
        base_url="http://test", client_id="id", client_secret="sec"
    )
    with patch.object(client_oauth_headers, "_authenticate_oauth") as mock_auth_oauth:
        _ = client_oauth_headers.get_headers()
        mock_auth_oauth.assert_called_once()

    # 12. request method with HTTP >= 400 error raise
    client_req = BaseApiClient(base_url="http://test", token="abc")
    mock_req_fail = MagicMock()
    mock_req_fail.status_code = 500
    mock_req_fail.text = "internal error"
    with patch.object(client_req._session, "request", return_value=mock_req_fail):
        with pytest.raises(Exception, match="Ansible API error"):
            client_req.request("GET", "/some/endpoint")

    # 13. request method with status 204 (No Content)
    mock_req_204 = MagicMock()
    mock_req_204.status_code = 204
    with patch.object(client_req._session, "request", return_value=mock_req_204):
        res = client_req.request("GET", "/some/endpoint")
        assert res == {"status": "success"}

    # 14. request method with empty text response
    mock_req_empty = MagicMock()
    mock_req_empty.status_code = 200
    mock_req_empty.text = "   "
    with patch.object(client_req._session, "request", return_value=mock_req_empty):
        res = client_req.request("GET", "/some/endpoint")
        assert res == {"status": "success", "message": "Empty response"}

    # 15. request method with JSONDecodeError fallback
    mock_req_nonjson = MagicMock()
    mock_req_nonjson.status_code = 200
    mock_req_nonjson.text = "plain text message"
    mock_req_nonjson.headers = {"Content-Type": "text/plain"}
    mock_req_nonjson.json.side_effect = json.JSONDecodeError("Not JSON", "", 0)
    with patch.object(client_req._session, "request", return_value=mock_req_nonjson):
        res = client_req.request("GET", "/some/endpoint")
        assert res["status"] == "success"
        assert res["content_type"] == "text/plain"
        assert res["text"] == "plain text message"

    # 16. handle_pagination with multi-page loop
    client_pag = BaseApiClient(base_url="http://test", token="abc")

    mock_page1 = MagicMock()
    mock_page1.status_code = 200
    mock_page1.json.return_value = {"results": [{"id": 1}], "next": "http://test/page2"}

    mock_page2 = MagicMock()
    mock_page2.status_code = 200
    mock_page2.json.return_value = {"results": [{"id": 2}], "next": None}

    with patch.object(client_pag, "request") as mock_req_method:
        mock_req_method.side_effect = [mock_page1.json(), mock_page2.json()]
        results = client_pag.handle_pagination("/api/v2/items/")
        assert results == [{"id": 1}, {"id": 2}]
        assert mock_req_method.call_count == 2

    # Break pagination when 'results' is not present
    with patch.object(client_pag, "request", return_value={"no_results": []}):
        results = client_pag.handle_pagination("/api/v2/items/")
        assert results == []


# ==========================================
# 5. Test API Client Validation Edge Cases
# ==========================================


def test_api_client_validation_edge_cases():
    # Instantiate Api client for testing specific exception raising logic
    api = Api(base_url="http://test", token="abc")

    # api_client_credentials.py JSON checks
    with pytest.raises(ValueError, match="Invalid JSON"):
        api.create_credential(
            name="test", credential_type_id=1, organization_id=1, inputs="invalid_json"
        )
    with pytest.raises(ValueError, match="Invalid JSON"):
        api.update_credential(credential_id=1, inputs="invalid_json")

    # api_client_groups.py JSON checks
    with pytest.raises(ValueError, match="Invalid JSON"):
        api.create_group(name="test", inventory_id=1, variables="invalid_json")
    with pytest.raises(ValueError, match="Invalid JSON"):
        api.update_group(group_id=1, variables="invalid_json")

    # api_client_hosts.py JSON checks
    with pytest.raises(ValueError, match="Invalid JSON"):
        api.create_host(name="test", inventory_id=1, variables="invalid_json")
    with pytest.raises(ValueError, match="Invalid JSON"):
        api.update_host(host_id=1, variables="invalid_json")

    # api_client_schedules.py JSON checks
    with pytest.raises(ValueError, match="Invalid JSON"):
        api.create_schedule(
            name="test",
            rrule="DTSTART:20300101T000000Z RRULE:FREQ=DAILY",
            unified_job_template_id=1,
            extra_data="invalid_json",
        )
    with pytest.raises(ValueError, match="Invalid JSON"):
        api.update_schedule(schedule_id=1, extra_data="invalid_json")

    # api_client_templates.py JSON checks
    with pytest.raises(ValueError, match="Invalid JSON"):
        api.create_job_template(
            name="test",
            inventory_id=1,
            project_id=1,
            playbook="site.yml",
            extra_vars="invalid_json",
        )
    with pytest.raises(ValueError, match="Invalid JSON"):
        api.update_job_template(template_id=1, extra_vars="invalid_json")

    # api_client_jobs.py validations
    with pytest.raises(ValueError, match="Invalid format"):
        api.get_job_stdout(job_id=1, format="invalid_format")

    # stdout json path
    with patch.object(api, "request") as mock_req:
        api.get_job_stdout(job_id=1, format="json")
        mock_req.assert_called_once_with("GET", "/api/v2/jobs/1/stdout/?format=json")

    # stdout html/txt path using session.get
    mock_resp = MagicMock()
    mock_resp.text = "stdout_text"
    with patch.object(api._session, "get", return_value=mock_resp):
        res = api.get_job_stdout(job_id=1, format="txt")
        assert res["stdout"] == "stdout_text"

    # launch_job JSON validation
    with pytest.raises(ValueError, match="Invalid JSON"):
        api.launch_job(template_id=1, extra_vars="invalid_json")

    # run_ad_hoc_command verbosity
    with pytest.raises(ValueError, match="Verbosity must be between 0 and 4"):
        api.run_ad_hoc_command(
            inventory_id=1,
            credential_id=1,
            module_name="ping",
            module_args="",
            verbosity=5,
        )

    # cancel_ad_hoc_command exception handling: Path A (DELETE works)
    with (
        patch.object(api, "request") as mock_req_method,
        patch.object(api, "get_ad_hoc_command", return_value={"status": "pending"}),
    ):
        # Primary post cancel fails
        mock_req_method.side_effect = [
            Exception("POST cancel failed"),
            {"status": "success"},
        ]
        res = api.cancel_ad_hoc_command(command_id=1)
        assert "cancelled via DELETE" in res["message"]

    # cancel_ad_hoc_command exception handling: Path B (cannot cancel in current status)
    with (
        patch.object(api, "request", side_effect=Exception("POST cancel failed")),
        patch.object(api, "get_ad_hoc_command", return_value={"status": "successful"}),
    ):
        with pytest.raises(
            Exception, match="Failed both cancel methods.*Cannot cancel command"
        ):
            api.cancel_ad_hoc_command(command_id=1)

    # cancel_ad_hoc_command exception handling: Path C (subsequent call also throws)
    with (
        patch.object(api, "request", side_effect=Exception("POST cancel failed")),
        patch.object(
            api, "get_ad_hoc_command", side_effect=Exception("GET info failed")
        ),
    ):
        with pytest.raises(
            Exception, match="Failed both cancel methods.*GET info failed"
        ):
            api.cancel_ad_hoc_command(command_id=1)

    # launch_workflow JSON validation
    with pytest.raises(ValueError, match="Invalid JSON"):
        api.launch_workflow(template_id=1, extra_vars="invalid_json")

    # api_client_teams.py list_teams organization_id=None branch coverage
    with patch.object(api, "handle_pagination") as mock_handle_pag:
        api.list_teams(organization_id=None)
        mock_handle_pag.assert_called_once_with("/api/v2/teams/", {"page_size": 100})

    # api_client_projects.py validations
    with pytest.raises(ValueError, match="Invalid SCM type"):
        api.create_project(name="test", organization_id=1, scm_type="invalid_scm")
    with pytest.raises(ValueError, match="SCM URL is required"):
        api.create_project(name="test", organization_id=1, scm_type="git", scm_url="")
    with pytest.raises(ValueError, match="Invalid SCM type"):
        api.update_project(project_id=1, scm_type="invalid_scm")

    # Cover list_hosts with inventory_id=None (api_client_hosts.py line 16)
    with patch.object(api, "handle_pagination") as mock_handle_pag:
        api.list_hosts(inventory_id=None)
        mock_handle_pag.assert_called_once_with("/api/v2/hosts/", {"page_size": 100})

    # Cover update_schedule with all fields (api_client_schedules.py lines 58, 60, 62)
    with patch.object(api, "request") as mock_req:
        api.update_schedule(
            schedule_id=1,
            name="updated_name",
            rrule="DTSTART:20300101T000000Z",
            description="updated_desc",
            extra_data='{"foo": "bar"}',
        )
        mock_req.assert_called_once_with(
            "PATCH",
            "/api/v2/schedules/1/",
            data={
                "name": "updated_name",
                "rrule": "DTSTART:20300101T000000Z",
                "description": "updated_desc",
                "extra_data": '{"foo": "bar"}',
            },
        )


# ==========================================
# 6. Test MCP Server Tools All Action Branches
# ==========================================


def test_mcp_server_tools_all_actions():
    from fastmcp import FastMCP

    from ansible_tower_mcp.mcp.mcp_server import (
        get_mcp_instance,
        mcp_server,
        register_ad_hoc_commands_tools,
        register_credentials_tools,
        register_groups_tools,
        register_hosts_tools,
        register_inventory_tools,
        register_job_templates_tools,
        register_jobs_tools,
        register_organizations_tools,
        register_projects_tools,
        register_schedules_tools,
        register_system_tools,
        register_teams_tools,
        register_users_tools,
        register_workflow_jobs_tools,
        register_workflow_templates_tools,
    )

    mcp = FastMCP("test_coverage_mcp")

    # Register all tools into the dummy mcp server
    register_inventory_tools(mcp)
    register_hosts_tools(mcp)
    register_groups_tools(mcp)
    register_job_templates_tools(mcp)
    register_jobs_tools(mcp)
    register_projects_tools(mcp)
    register_credentials_tools(mcp)
    register_organizations_tools(mcp)
    register_teams_tools(mcp)
    register_users_tools(mcp)
    register_ad_hoc_commands_tools(mcp)
    register_workflow_templates_tools(mcp)
    register_workflow_jobs_tools(mcp)
    register_schedules_tools(mcp)
    register_system_tools(mcp)

    mock_client = MagicMock()
    from unittest.mock import AsyncMock

    mock_ctx = MagicMock()
    mock_ctx.info = AsyncMock()

    async def run_async_test():
        # List all tools and call every action branch dynamically!
        tool_objs = mcp.list_tools()
        if (
            inspect.iscoroutine(tool_objs)
            or asyncio.iscoroutine(tool_objs)
            or hasattr(tool_objs, "__await__")
        ):
            tool_objs = await tool_objs
        for tool in tool_objs:
            sig = inspect.signature(tool.fn)  # type: ignore
            action_param = sig.parameters.get("action")
            if not action_param or not hasattr(action_param.default, "description"):
                continue

            desc = action_param.default.description
            actions = re.findall(r"'([^']+)'", desc)
            if not actions:
                continue

            print(f"Testing tool {tool.name} with actions: {actions}")
            for act in actions:
                # Call valid action path
                res = await tool.fn(  # type: ignore
                    action=act, params_json="{}", client=mock_client, ctx=mock_ctx
                )
                assert isinstance(res, (dict, list, MagicMock))

            # Call invalid action path to cover ValueError / fallback raise
            with pytest.raises(ValueError, match="Unknown action"):
                await tool.fn(  # type: ignore
                    action="invalid_coverage_action_xyz",
                    params_json="{}",
                    client=mock_client,
                    ctx=mock_ctx,
                )

            # Call invalid params_json to cover exception handling block
            err_res = await tool.fn(  # type: ignore
                action=actions[0],
                params_json="invalid json string {",
                client=mock_client,
                ctx=mock_ctx,
            )
            assert "error" in err_res

    asyncio.run(run_async_test())

    # Cover get_mcp_instance health_check & middlewares
    with patch.dict(
        os.environ,
        {
            "INVENTORYTOOL": "True",
            "HOSTSTOOL": "True",
            "GROUPSTOOL": "True",
            "JOB_TEMPLATESTOOL": "True",
            "JOBSTOOL": "True",
            "PROJECTSTOOL": "True",
            "CREDENTIALSTOOL": "True",
            "ORGANIZATIONSTOOL": "True",
            "TEAMSTOOL": "True",
            "USERSTOOL": "True",
            "AD_HOC_COMMANDSTOOL": "True",
            "WORKFLOW_TEMPLATESTOOL": "True",
            "WORKFLOW_JOBSTOOL": "True",
            "SCHEDULESTOOL": "True",
            "SYSTEMTOOL": "True",
        },
    ):
        mcp_srv, args, mws = get_mcp_instance()
        assert mcp_srv is not None

        # Call the health check route dynamically to cover line 633 of mcp_server.py
        routes = getattr(mcp_srv, "routes", [])
        if not routes and hasattr(mcp_srv, "app"):
            routes = getattr(mcp_srv.app, "routes", [])
        if not routes and hasattr(mcp_srv, "_additional_http_routes"):
            routes = getattr(mcp_srv, "_additional_http_routes", [])
        for route in routes:
            if getattr(route, "path", None) == "/health":
                res = asyncio.run(route.endpoint(MagicMock()))
                assert res is not None

    # Cover mcp_server stdio run option block
    mock_args = MagicMock()
    mock_args.transport = "stdio"
    mock_args.auth_type = "none"
    with patch(
        "ansible_tower_mcp.mcp.mcp_server.get_mcp_instance",
        return_value=(mock_client, mock_args, []),
    ):
        mcp_server()
        mock_client.run.assert_called_once_with(transport="stdio")

    # Cover mcp_server streamable-http run option block
    mock_args.transport = "streamable-http"
    mock_args.host = "127.0.0.1"
    mock_args.port = 8000
    mock_client.reset_mock()
    with patch(
        "ansible_tower_mcp.mcp.mcp_server.get_mcp_instance",
        return_value=(mock_client, mock_args, []),
    ):
        mcp_server()
        mock_client.run.assert_called_once_with(
            transport="streamable-http", host="127.0.0.1", port=8000
        )

    # Cover sse option block
    mock_args.transport = "sse"
    mock_client.reset_mock()
    with patch(
        "ansible_tower_mcp.mcp.mcp_server.get_mcp_instance",
        return_value=(mock_client, mock_args, []),
    ):
        mcp_server()
        mock_client.run.assert_called_once_with(
            transport="sse", host="127.0.0.1", port=8000
        )

    # Cover invalid transport option block
    mock_args.transport = "invalid_transport"
    mock_client.reset_mock()
    with (
        patch(
            "ansible_tower_mcp.mcp.mcp_server.get_mcp_instance",
            return_value=(mock_client, mock_args, []),
        ),
        pytest.raises(SystemExit),
    ):
        mcp_server()


# ==========================================
# 7. Test MCP Server __main__ and Import Fallbacks
# ==========================================


def test_mcp_server_main():
    with (
        patch("sys.argv", ["mcp_server.py", "--transport", "stdio"]),
        patch("fastmcp.FastMCP.run") as mock_run,
    ):
        runpy.run_module("ansible_tower_mcp.mcp_server", run_name="__main__")
        runpy.run_module("ansible_tower_mcp.mcp.mcp_server", run_name="__main__")
        assert mock_run.call_count >= 2


def test_mcp_server_import_warning_fallback():
    import importlib
    import sys

    import requests.exceptions

    has_warning = hasattr(requests.exceptions, "RequestsDependencyWarning")
    if has_warning:
        orig_warning = requests.exceptions.RequestsDependencyWarning
        delattr(requests.exceptions, "RequestsDependencyWarning")
    try:
        mcp_module = sys.modules.get("ansible_tower_mcp.mcp.mcp_server")
        if mcp_module:
            importlib.reload(mcp_module)
    finally:
        if has_warning:
            setattr(requests.exceptions, "RequestsDependencyWarning", orig_warning)
