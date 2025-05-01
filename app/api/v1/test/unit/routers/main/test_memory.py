from unittest.mock import patch, MagicMock

def test_memory_with_valid_auth(client, valid_auth_headers):
    """Test memory endpoint with valid authentication"""
    with patch('psutil.Process') as mock_process:
        # Mock memory info
        mock_memory = MagicMock()
        mock_memory.rss = 1024 * 1024 * 1024  # 1GB
        mock_memory.vms = 2 * 1024 * 1024 * 1024  # 2GB
        
        mock_process_instance = MagicMock()
        mock_process_instance.memory_info.return_value = mock_memory
        mock_process.return_value = mock_process_instance

        response = client.get("/memory", headers=valid_auth_headers)
        assert response.status_code == 200
        
        memory_data = response.json()["memory"]
        assert "rss" in memory_data
        assert "vms" in memory_data
        assert isinstance(memory_data["rss"], float)
        assert isinstance(memory_data["vms"], float)

def test_memory_without_auth(client):
    """Test memory endpoint without authentication"""
    response = client.get("/memory")
    assert response.status_code == 401
    data = response.json()["detail"]
    assert data["message"] == "You don't have permission to access this resource"
    assert data["status"] == "error"