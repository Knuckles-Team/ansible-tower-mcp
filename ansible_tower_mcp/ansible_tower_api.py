#!/usr/bin/env python
# coding: utf-8

import json
import requests
from typing import Dict, List, Optional
from urllib.parse import urljoin
import re
import urllib3

__version__ = "1.2.25"


class Api:
    def __init__(
        self,
        base_url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        verify: bool = False,
        proxies: Optional[Dict[str, str]] = None,
    ):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = token
        self.client_id = client_id
        self.client_secret = client_secret
        self._session = requests.Session()
        self._session.verify = verify
        self.proxies = proxies

        if proxies:
            self._session.proxies = proxies

        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if token:
            self.token = token
        elif client_id and client_secret:
            self._authenticate_oauth()
        elif username and password:
            self.get_token()
        else:
            raise ValueError(
                "Must provide either a token, or (username and password), or (client_id and client_secret) for authentication."
            )

        # Validate authentication
        try:
            self.request("GET", "/api/v2/ping/")
        except Exception as e:
            raise Exception(f"Authentication validation failed: {str(e)}")

    def _authenticate_oauth(self):
        """Authenticate using OAuth 2.0."""
        auth_url = urljoin(self.base_url, "/api/o/token/")
        grant_type = (
            "password" if self.username and self.password else "client_credentials"
        )
        payload = {
            "grant_type": grant_type,
            "username": self.username,
            "password": self.password,
            "scope": "write",
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = self._session.post(
            url=auth_url,
            data=payload,
            headers=headers,
            auth=(self.client_id, self.client_secret),
        )

        if response.status_code != 200:
            raise Exception(
                f"OAuth authentication failed: {response.status_code} - {response.text}"
            )

        token_info = response.json()
        self.token = token_info.get("access_token")
        if not self.token:
            raise Exception("No access_token received from OAuth response")

    def get_token(self) -> str:
        """Authenticate and get token using web session approach."""
        # Step 1: Get the CSRF token
        login_page = self._session.get(f"{self.base_url}/api/login/")

        # Get CSRF token from cookies
        csrf_token = None
        if "csrftoken" in login_page.cookies:
            csrf_token = login_page.cookies["csrftoken"]
        else:
            # Try to find it in the content
            match = re.search(
                r'name="csrfmiddlewaretoken" value="([^"]+)"', login_page.text
            )
            if match:
                csrf_token = match.group(1)

        if not csrf_token:
            raise Exception("Could not obtain CSRF token")

        # Step 2: Perform login
        headers = {"Referer": f"{self.base_url}/api/login/", "X-CSRFToken": csrf_token}

        login_data = {
            "username": self.username,
            "password": self.password,
            "next": "/api/v2/",
        }

        login_response = self._session.post(
            f"{self.base_url}/api/login/", data=login_data, headers=headers
        )

        if login_response.status_code >= 400:
            raise Exception(
                f"Login failed: {login_response.status_code} - {login_response.text}"
            )

        # Step 3: Generate API token
        token_headers = {
            "Content-Type": "application/json",
            "Referer": f"{self.base_url}/api/v2/",
        }

        # Use the updated CSRF token
        if "csrftoken" in self._session.cookies:
            token_headers["X-CSRFToken"] = self._session.cookies["csrftoken"]

        token_data = {
            "description": "MCP Server Token",
            "application": None,
            "scope": "write",  # Using write scope for full access
        }

        token_response = self._session.post(
            f"{self.base_url}/api/v2/tokens/", json=token_data, headers=token_headers
        )

        if token_response.status_code == 201:
            token_data = token_response.json()
            self.token = token_data.get("token")
            return self.token
        else:
            raise Exception(
                f"Token creation failed: {token_response.status_code} - {token_response.text}"
            )

    def get_headers(self) -> Dict[str, str]:
        """Get request headers with authorization."""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def request(
        self, method: str, endpoint: str, params: Dict = None, data: Dict = None
    ) -> Dict:
        """Make a request to the Ansible API."""
        if endpoint.startswith("http"):
            url = endpoint
        else:
            url = urljoin(self.base_url, endpoint)

        headers = self.get_headers()

        response = self._session.request(
            method=method, url=url, headers=headers, params=params, json=data
        )

        if response.status_code >= 400:
            error_message = (
                f"Ansible API error: {response.status_code} - {response.text}"
            )
            raise Exception(error_message)

        if response.status_code == 204:
            return {"status": "success"}

        if not response.text.strip():
            return {"status": "success", "message": "Empty response"}

        try:
            return response.json()
        except json.JSONDecodeError:
            return {
                "status": "success",
                "content_type": response.headers.get("Content-Type", "unknown"),
                "text": response.text[:1000],
            }

    def handle_pagination(self, endpoint: str, params: Dict = None) -> List[Dict]:
        """Handle paginated results from Ansible API."""
        results = []
        next_url = urljoin(self.base_url, endpoint)
        first_request = True

        while next_url:
            if first_request:
                response = self.request("GET", next_url, params=params)
                first_request = False
            else:
                response = self.request("GET", next_url)
            if "results" in response:
                results.extend(response["results"])
                next_url = response.get("next")
            else:
                break
        return results

    # Inventory Management
    def list_inventories(self, page_size: int = 100) -> List[Dict]:
        params = {"page_size": page_size}
        return self.handle_pagination("/api/v2/inventories/", params)

    def get_inventory(self, inventory_id: int) -> Dict:
        return self.request("GET", f"/api/v2/inventories/{inventory_id}/")

    def create_inventory(
        self, name: str, organization_id: int, description: str = ""
    ) -> Dict:
        data = {
            "name": name,
            "description": description,
            "organization": organization_id,
        }
        return self.request("POST", "/api/v2/inventories/", data=data)

    def update_inventory(
        self, inventory_id: int, name: str = None, description: str = None
    ) -> Dict:
        data = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        return self.request("PATCH", f"/api/v2/inventories/{inventory_id}/", data=data)

    def delete_inventory(self, inventory_id: int) -> Dict:
        self.request("DELETE", f"/api/v2/inventories/{inventory_id}/")
        return {"status": "success", "message": f"Inventory {inventory_id} deleted"}

    # Host Management
    def list_hosts(self, inventory_id: int = None, page_size: int = 100) -> List[Dict]:
        params = {"page_size": page_size}
        if inventory_id:
            endpoint = f"/api/v2/inventories/{inventory_id}/hosts/"
        else:
            endpoint = "/api/v2/hosts/"
        return self.handle_pagination(endpoint, params)

    def get_host(self, host_id: int) -> Dict:
        return self.request("GET", f"/api/v2/hosts/{host_id}/")

    def create_host(
        self, name: str, inventory_id: int, variables: str = "{}", description: str = ""
    ) -> Dict:
        try:
            json.loads(variables)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON in variables")
        data = {
            "name": name,
            "inventory": inventory_id,
            "variables": variables,
            "description": description,
        }
        return self.request("POST", "/api/v2/hosts/", data=data)

    def update_host(
        self,
        host_id: int,
        name: str = None,
        variables: str = None,
        description: str = None,
    ) -> Dict:
        if variables:
            try:
                json.loads(variables)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON in variables")
        data = {}
        if name:
            data["name"] = name
        if variables:
            data["variables"] = variables
        if description:
            data["description"] = description
        return self.request("PATCH", f"/api/v2/hosts/{host_id}/", data=data)

    def delete_host(self, host_id: int) -> Dict:
        self.request("DELETE", f"/api/v2/hosts/{host_id}/")
        return {"status": "success", "message": f"Host {host_id} deleted"}

    # Group Management
    def list_groups(self, inventory_id: int, page_size: int = 100) -> List[Dict]:
        params = {"page_size": page_size}
        return self.handle_pagination(
            f"/api/v2/inventories/{inventory_id}/groups/", params
        )

    def get_group(self, group_id: int) -> Dict:
        return self.request("GET", f"/api/v2/groups/{group_id}/")

    def create_group(
        self, name: str, inventory_id: int, variables: str = "{}", description: str = ""
    ) -> Dict:
        try:
            json.loads(variables)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON in variables")
        data = {
            "name": name,
            "inventory": inventory_id,
            "variables": variables,
            "description": description,
        }
        return self.request("POST", "/api/v2/groups/", data=data)

    def update_group(
        self,
        group_id: int,
        name: str = None,
        variables: str = None,
        description: str = None,
    ) -> Dict:
        if variables:
            try:
                json.loads(variables)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON in variables")
        data = {}
        if name:
            data["name"] = name
        if variables:
            data["variables"] = variables
        if description:
            data["description"] = description
        return self.request("PATCH", f"/api/v2/groups/{group_id}/", data=data)

    def delete_group(self, group_id: int) -> Dict:
        self.request("DELETE", f"/api/v2/groups/{group_id}/")
        return {"status": "success", "message": f"Group {group_id} deleted"}

    def add_host_to_group(self, group_id: int, host_id: int) -> Dict:
        data = {"id": host_id}
        return self.request("POST", f"/api/v2/groups/{group_id}/hosts/", data=data)

    def remove_host_from_group(self, group_id: int, host_id: int) -> Dict:
        data = {"id": host_id, "disassociate": True}
        self.request("POST", f"/api/v2/groups/{group_id}/hosts/", data=data)
        return {
            "status": "success",
            "message": f"Host {host_id} removed from group {group_id}",
        }

    # Job Template Management
    def list_job_templates(self, page_size: int = 100) -> List[Dict]:
        params = {"page_size": page_size}
        return self.handle_pagination("/api/v2/job_templates/", params)

    def get_job_template(self, template_id: int) -> Dict:
        return self.request("GET", f"/api/v2/job_templates/{template_id}/")

    def create_job_template(
        self,
        name: str,
        inventory_id: int,
        project_id: int,
        playbook: str,
        credential_id: int = None,
        description: str = "",
        extra_vars: str = "{}",
    ) -> Dict:
        try:
            json.loads(extra_vars)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON in extra_vars")
        data = {
            "name": name,
            "inventory": inventory_id,
            "project": project_id,
            "playbook": playbook,
            "description": description,
            "extra_vars": extra_vars,
            "job_type": "run",
            "verbosity": 0,
        }
        if credential_id:
            data["credential"] = credential_id
        return self.request("POST", "/api/v2/job_templates/", data=data)

    def update_job_template(
        self,
        template_id: int,
        name: str = None,
        inventory_id: int = None,
        playbook: str = None,
        description: str = None,
        extra_vars: str = None,
    ) -> Dict:
        if extra_vars:
            try:
                json.loads(extra_vars)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON in extra_vars")
        data = {}
        if name:
            data["name"] = name
        if inventory_id:
            data["inventory"] = inventory_id
        if playbook:
            data["playbook"] = playbook
        if description:
            data["description"] = description
        if extra_vars:
            data["extra_vars"] = extra_vars
        return self.request("PATCH", f"/api/v2/job_templates/{template_id}/", data=data)

    def delete_job_template(self, template_id: int) -> Dict:
        self.request("DELETE", f"/api/v2/job_templates/{template_id}/")
        return {"status": "success", "message": f"Job template {template_id} deleted"}

    def launch_job(self, template_id: int, extra_vars: str = None) -> Dict:
        if extra_vars:
            try:
                json.loads(extra_vars)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON in extra_vars")
        data = {}
        if extra_vars:
            data["extra_vars"] = extra_vars
        return self.request(
            "POST", f"/api/v2/job_templates/{template_id}/launch/", data=data
        )

    # Job Management
    def list_jobs(self, status: str = None, page_size: int = 100) -> List[Dict]:
        params = {"page_size": page_size}
        if status:
            params["status"] = status
        return self.handle_pagination("/api/v2/jobs/", params)

    def get_job(self, job_id: int) -> Dict:
        return self.request("GET", f"/api/v2/jobs/{job_id}/")

    def cancel_job(self, job_id: int) -> Dict:
        return self.request("POST", f"/api/v2/jobs/{job_id}/cancel/")

    # Job Management
    def get_job_events(self, job_id: int, page_size: int = 100) -> List[Dict]:
        params = {"page_size": page_size}
        return self.handle_pagination(f"/api/v2/jobs/{job_id}/job_events/", params)

    def get_job_stdout(self, job_id: int, format: str = "txt") -> Dict:
        if format not in ["txt", "html", "json", "ansi"]:
            raise ValueError("Invalid format")
        url = f"/api/v2/jobs/{job_id}/stdout/?format={format}"
        if format == "json":
            return self.request("GET", url)
        else:
            response = self._session.get(
                urljoin(self.base_url, url), headers=self.get_headers()
            )
            response.raise_for_status()
            return {"status": "success", "stdout": response.text}

    # Project Management
    def list_projects(self, page_size: int = 100) -> List[Dict]:
        params = {"page_size": page_size}
        return self.handle_pagination("/api/v2/projects/", params)

    def get_project(self, project_id: int) -> Dict:
        return self.request("GET", f"/api/v2/projects/{project_id}/")

    def create_project(
        self,
        name: str,
        organization_id: int,
        scm_type: str,
        scm_url: str = None,
        scm_branch: str = None,
        credential_id: int = None,
        description: str = "",
    ) -> Dict:
        if scm_type not in ["", "git", "hg", "svn", "manual"]:
            raise ValueError("Invalid SCM type. Must be one of: git, hg, svn, manual")
        if scm_type != "manual" and not scm_url:
            raise ValueError("SCM URL is required for non-manual SCM types")
        data = {
            "name": name,
            "organization": organization_id,
            "scm_type": scm_type,
            "description": description,
        }
        if scm_url:
            data["scm_url"] = scm_url
        if scm_branch:
            data["scm_branch"] = scm_branch
        if credential_id:
            data["credential"] = credential_id
        return self.request("POST", "/api/v2/projects/", data=data)

    def update_project(
        self,
        project_id: int,
        name: str = None,
        scm_type: str = None,
        scm_url: str = None,
        scm_branch: str = None,
        description: str = None,
    ) -> Dict:
        if scm_type and scm_type not in ["", "git", "hg", "svn", "manual"]:
            raise ValueError("Invalid SCM type. Must be one of: git, hg, svn, manual")
        data = {}
        if name:
            data["name"] = name
        if scm_type:
            data["scm_type"] = scm_type
        if scm_url:
            data["scm_url"] = scm_url
        if scm_branch:
            data["scm_branch"] = scm_branch
        if description:
            data["description"] = description
        return self.request("PATCH", f"/api/v2/projects/{project_id}/", data=data)

    def delete_project(self, project_id: int) -> Dict:
        self.request("DELETE", f"/api/v2/projects/{project_id}/")
        return {"status": "success", "message": f"Project {project_id} deleted"}

    def sync_project(self, project_id: int) -> Dict:
        return self.request("POST", f"/api/v2/projects/{project_id}/update/")

    # Credential Management
    def list_credentials(self, page_size: int = 100) -> List[Dict]:
        params = {"page_size": page_size}
        return self.handle_pagination("/api/v2/credentials/", params)

    def get_credential(self, credential_id: int) -> Dict:
        return self.request("GET", f"/api/v2/credentials/{credential_id}/")

    # Credential Management
    def list_credential_types(self, page_size: int = 100) -> List[Dict]:
        params = {"page_size": page_size}
        return self.handle_pagination("/api/v2/credential_types/", params)

    def create_credential(
        self,
        name: str,
        credential_type_id: int,
        organization_id: int,
        inputs: str,
        description: str = "",
    ) -> Dict:
        try:
            inputs_dict = json.loads(inputs)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON in inputs")
        data = {
            "name": name,
            "credential_type": credential_type_id,
            "organization": organization_id,
            "inputs": inputs_dict,
            "description": description,
        }
        return self.request("POST", "/api/v2/credentials/", data=data)

    def update_credential(
        self,
        credential_id: int,
        name: str = None,
        inputs: str = None,
        description: str = None,
    ) -> Dict:
        data = {}
        if name:
            data["name"] = name
        if inputs:
            try:
                inputs_dict = json.loads(inputs)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON in inputs")
            data["inputs"] = inputs_dict
        if description:
            data["description"] = description
        return self.request("PATCH", f"/api/v2/credentials/{credential_id}/", data=data)

    def delete_credential(self, credential_id: int) -> Dict:
        self.request("DELETE", f"/api/v2/credentials/{credential_id}/")
        return {"status": "success", "message": f"Credential {credential_id} deleted"}

    # Organization Management
    def list_organizations(self, page_size: int = 100) -> List[Dict]:
        params = {"page_size": page_size}
        return self.handle_pagination("/api/v2/organizations/", params)

    def get_organization(self, organization_id: int) -> Dict:
        return self.request("GET", f"/api/v2/organizations/{organization_id}/")

    def create_organization(self, name: str, description: str = "") -> Dict:
        data = {"name": name, "description": description}
        return self.request("POST", "/api/v2/organizations/", data=data)

    def update_organization(
        self, organization_id: int, name: str = None, description: str = None
    ) -> Dict:
        data = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        return self.request(
            "PATCH", f"/api/v2/organizations/{organization_id}/", data=data
        )

    def delete_organization(self, organization_id: int) -> Dict:
        self.request("DELETE", f"/api/v2/organizations/{organization_id}/")
        return {
            "status": "success",
            "message": f"Organization {organization_id} deleted",
        }

    # Team Management
    def list_teams(
        self, organization_id: int = None, page_size: int = 100
    ) -> List[Dict]:
        params = {"page_size": page_size}
        if organization_id:
            endpoint = f"/api/v2/organizations/{organization_id}/teams/"
        else:
            endpoint = "/api/v2/teams/"
        return self.handle_pagination(endpoint, params)

    def get_team(self, team_id: int) -> Dict:
        return self.request("GET", f"/api/v2/teams/{team_id}/")

    def create_team(
        self, name: str, organization_id: int, description: str = ""
    ) -> Dict:
        data = {
            "name": name,
            "organization": organization_id,
            "description": description,
        }
        return self.request("POST", "/api/v2/teams/", data=data)

    def update_team(
        self, team_id: int, name: str = None, description: str = None
    ) -> Dict:
        data = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        return self.request("PATCH", f"/api/v2/teams/{team_id}/", data=data)

    def delete_team(self, team_id: int) -> Dict:
        self.request("DELETE", f"/api/v2/teams/{team_id}/")
        return {"status": "success", "message": f"Team {team_id} deleted"}

    # User Management
    def list_users(self, page_size: int = 100) -> List[Dict]:
        params = {"page_size": page_size}
        return self.handle_pagination("/api/v2/users/", params)

    def get_user(self, user_id: int) -> Dict:
        return self.request("GET", f"/api/v2/users/{user_id}/")

    def create_user(
        self,
        username: str,
        password: str,
        first_name: str = "",
        last_name: str = "",
        email: str = "",
        is_superuser: bool = False,
        is_system_auditor: bool = False,
    ) -> Dict:
        data = {
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "is_superuser": is_superuser,
            "is_system_auditor": is_system_auditor,
        }
        return self.request("POST", "/api/v2/users/", data=data)

    def update_user(
        self,
        user_id: int,
        username: str = None,
        password: str = None,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        is_superuser: bool = None,
        is_system_auditor: bool = None,
    ) -> Dict:
        data = {}
        if username:
            data["username"] = username
        if password:
            data["password"] = password
        if first_name is not None:
            data["first_name"] = first_name
        if last_name is not None:
            data["last_name"] = last_name
        if email:
            data["email"] = email
        if is_superuser is not None:
            data["is_superuser"] = is_superuser
        if is_system_auditor is not None:
            data["is_system_auditor"] = is_system_auditor
        return self.request("PATCH", f"/api/v2/users/{user_id}/", data=data)

    def delete_user(self, user_id: int) -> Dict:
        self.request("DELETE", f"/api/v2/users/{user_id}/")
        return {"status": "success", "message": f"User {user_id} deleted"}

    # Ad Hoc Commands
    def run_ad_hoc_command(
        self,
        inventory_id: int,
        credential_id: int,
        module_name: str,
        module_args: str,
        limit: str = "",
        verbosity: int = 0,
    ) -> Dict:
        if verbosity not in range(5):
            raise ValueError("Verbosity must be between 0 and 4")
        data = {
            "inventory": inventory_id,
            "credential": credential_id,
            "module_name": module_name,
            "module_args": module_args,
            "verbosity": verbosity,
        }
        if limit:
            data["limit"] = limit
        return self.request("POST", "/api/v2/ad_hoc_commands/", data=data)

    def get_ad_hoc_command(self, command_id: int) -> Dict:
        return self.request("GET", f"/api/v2/ad_hoc_commands/{command_id}/")

    def cancel_ad_hoc_command(self, command_id: int) -> Dict:
        try:
            return self.request("POST", f"/api/v2/ad_hoc_commands/{command_id}/cancel/")
        except Exception as e:
            try:
                response = self.get_ad_hoc_command(command_id)
                status = response.get("status")
                if status in ["pending", "waiting", "running"]:
                    self.request("DELETE", f"/api/v2/ad_hoc_commands/{command_id}/")
                    return {
                        "status": "success",
                        "message": f"Ad hoc command {command_id} cancelled via DELETE",
                    }
                else:
                    raise ValueError(f"Cannot cancel command in status: {status}")
            except Exception as inner_e:
                raise Exception(
                    f"Failed both cancel methods: {str(e)}, then: {str(inner_e)}"
                )

    # Workflow Templates
    def list_workflow_templates(self, page_size: int = 100) -> List[Dict]:
        params = {"page_size": page_size}
        return self.handle_pagination("/api/v2/workflow_job_templates/", params)

    def get_workflow_template(self, template_id: int) -> Dict:
        return self.request("GET", f"/api/v2/workflow_job_templates/{template_id}/")

    def launch_workflow(self, template_id: int, extra_vars: str = None) -> Dict:
        if extra_vars:
            try:
                json.loads(extra_vars)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON in extra_vars")
        data = {}
        if extra_vars:
            data["extra_vars"] = extra_vars
        return self.request(
            "POST", f"/api/v2/workflow_job_templates/{template_id}/launch/", data=data
        )

    # Workflow Jobs
    def list_workflow_jobs(
        self, status: str = None, page_size: int = 100
    ) -> List[Dict]:
        params = {"page_size": page_size}
        if status:
            params["status"] = status
        return self.handle_pagination("/api/v2/workflow_jobs/", params)

    def get_workflow_job(self, job_id: int) -> Dict:
        return self.request("GET", f"/api/v2/workflow_jobs/{job_id}/")

    def cancel_workflow_job(self, job_id: int) -> Dict:
        return self.request("POST", f"/api/v2/workflow_jobs/{job_id}/cancel/")

    # Schedule Management
    def list_schedules(
        self, unified_job_template_id: int = None, page_size: int = 100
    ) -> List[Dict]:
        params = {"page_size": page_size}
        if unified_job_template_id:
            params["unified_job_template"] = unified_job_template_id
        return self.handle_pagination("/api/v2/schedules/", params)

    def get_schedule(self, schedule_id: int) -> Dict:
        return self.request("GET", f"/api/v2/schedules/{schedule_id}/")

    def create_schedule(
        self,
        name: str,
        unified_job_template_id: int,
        rrule: str,
        description: str = "",
        extra_data: str = "{}",
    ) -> Dict:
        try:
            extra_data_dict = json.loads(extra_data)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON in extra_data")
        data = {
            "name": name,
            "unified_job_template": unified_job_template_id,
            "rrule": rrule,
            "description": description,
            "extra_data": extra_data_dict,
        }
        return self.request("POST", "/api/v2/schedules/", data=data)

    def update_schedule(
        self,
        schedule_id: int,
        name: str = None,
        rrule: str = None,
        description: str = None,
        extra_data: str = None,
    ) -> Dict:
        data = {}
        if name:
            data["name"] = name
        if rrule:
            data["rrule"] = rrule
        if description:
            data["description"] = description
        if extra_data:
            try:
                extra_data_dict = json.loads(extra_data)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON in extra_data")
            data["extra_data"] = extra_data_dict
        return self.request("PATCH", f"/api/v2/schedules/{schedule_id}/", data=data)

    def delete_schedule(self, schedule_id: int) -> Dict:
        self.request("DELETE", f"/api/v2/schedules/{schedule_id}/")
        return {"status": "success", "message": f"Schedule {schedule_id} deleted"}

    # System Information
    def get_ansible_version(self) -> Dict:
        return self.request("GET", "/api/v2/ping/")

    def get_dashboard_stats(self) -> Dict:
        return self.request("GET", "/api/v2/dashboard/")

    def get_metrics(self) -> Dict:
        try:
            return self.request("GET", "/api/v2/metrics/")
        except Exception:
            url = urljoin(self.base_url, "/api/v2/metrics/")
            response = self._session.get(url, headers=self.get_headers())
            response.raise_for_status()
            return {"status": "success", "raw_data": response.text[:1000]}
