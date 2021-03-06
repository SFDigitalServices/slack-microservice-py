# pylint: disable=redefined-outer-name
"""Tests for microservice"""
import json
from unittest.mock import patch
import jsend
import pytest
from falcon import testing
import service.microservice
import tests.mocks as mocks


CLIENT_HEADERS = {
    "ACCESS_KEY": "123456"
}

@pytest.fixture()
def client():
    """ client fixture """
    return testing.TestClient(app=service.microservice.start_service(), headers=CLIENT_HEADERS)

@pytest.fixture
def mock_env_access_key(monkeypatch):
    """ mock environment access key """
    monkeypatch.setenv("ACCESS_KEY", CLIENT_HEADERS["ACCESS_KEY"])

@pytest.fixture
def mock_env_no_access_key(monkeypatch):
    """ mock environment with no access key """
    monkeypatch.delenv("ACCESS_KEY", raising=False)

def test_welcome(client, mock_env_access_key):
    # pylint: disable=unused-argument
    # mock_env_access_key is a fixture and creates a false positive for pylint
    """Test welcome message response"""
    response = client.simulate_get('/welcome')
    assert response.status_code == 200

    expected_msg = jsend.success({'message': 'Welcome'})
    assert json.loads(response.content) == expected_msg

    # Test welcome request with no ACCESS_KEY in header
    client_no_access_key = testing.TestClient(service.microservice.start_service())
    response = client_no_access_key.simulate_get('/welcome')
    assert response.status_code == 403

def test_welcome_no_access_key(client, mock_env_no_access_key):
    # pylint: disable=unused-argument
    # mock_env_no_access_key is a fixture and creates a false positive for pylint
    """Test welcome request with no ACCESS_key environment var set"""
    response = client.simulate_get('/welcome')
    assert response.status_code == 403

def test_slack(client, mock_env_access_key):
    # pylint: disable=unused-argument
    """ test on_post"""
    with patch('service.resources.slack.requests.post') as mock_slack:
        mock_slack.return_value.status_code = 100
        mock_slack.return_value.json_data = lambda: {"ok": True, "channel": "C0190TZ0TS9"}
        response = client.simulate_post(
            '/slack-notification',
            json=mocks.SUBMISSION_POST_DATA
        )
        assert response.status_code == 200

def test_slack_exception(client, mock_env_access_key):
    # pylint: disable=unused-argument
    """ test on_post exceptions """
    with patch('service.resources.slack.requests.post') as mock_slack:
        mock_slack.return_value.json = {"ok": False, "error": "Failed"}
        response = client.simulate_post(
            '/slack-notification',
            json=mocks.SUBMISSION_POST_DATA
        )
        assert response.status_code == 400
