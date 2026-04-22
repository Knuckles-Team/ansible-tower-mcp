from ansible_tower_mcp.ansible_tower_api import Api

def test_api_init():
    api = Api(base_url="http://localhost", token="test")
    assert api.base_url == "http://localhost"
    assert api.token == "test"
