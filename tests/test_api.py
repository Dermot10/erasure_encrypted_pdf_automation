import os
import sys
import pytest
import io
import requests
import tempfile
import json
from unittest.mock import MagicMock, patch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from api.jira_api import JiraAPI
import requests_mock



@pytest.fixture
def jira_api():
    api = JiraAPI()
    return api

@pytest.fixture
def mock_post():
    with patch('requests.post') as mock:
        yield mock

def test_connect_to_Jira_success(jira_api):
    """Test successful connection to Jira API"""
    with requests_mock.Mocker() as m:
        m.get(requests_mock.ANY, status_code=200)
        response = jira_api.connect_to_Jira()
        assert response.status_code == 200

def test_connect_to_Jira_failure(jira_api):
    """Test unsuccessful connection to Jira API"""
    with requests_mock.Mocker() as m:
        m.get(requests_mock.ANY, status_code=404)
        response = jira_api.connect_to_Jira()
        assert response.status_code == 404

def test_get_jira_data_success(jira_api):
    """Test correct data retrieved from Jira endpoint"""
    with requests_mock.Mocker() as m:
        mock_data = {"issues": [{"key": "ERASURE-0001", "fields": {}}]}
        m.get(requests_mock.ANY, status_code=200, json=mock_data)
        result = jira_api.get_jira_data()
        assert isinstance(result, list)
        assert len(result) == 1

def test_get_jira_data_failure(jira_api):
    """Test failed server response from api call"""
    with requests_mock.Mocker() as m:
        m.get(requests_mock.ANY, status_code=500)
        result = jira_api.get_jira_data()
        assert isinstance(result, list)
        assert len(result) == 0

def test_get_current_user_success(jira_api):
    """Test successful call to separate endpoint retrieving the user for ticket signature"""
    with requests_mock.Mocker() as m:
        mock_data = {"displayName": "Test Author"}
        m.get(requests_mock.ANY, status_code=200, json=mock_data)
        result = jira_api.get_current_user()
        assert result == "Test Author"

def test_get_current_user_failure(jira_api):
    """Test unsuccessful call to separate endpoint retrieving the user for ticket signature"""
    with requests_mock.Mocker() as m:
        m.get(requests_mock.ANY, status_code=500)
        result = jira_api.get_current_user()
        assert result is None

@patch('requests.post')
def test_post_request(mock_post):
    """Test to mock post request"""
    mock_response_data = {"response_key": "response_value"}
    expected_headers = {'Content-Type': 'application/json'}
    headers={'Content-Type': 'application/json'}

    # Simulate the POST request and response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_response_data

    # Assign the MagicMock to the return_value of mock_post
    mock_post.return_value = mock_response

    # Perform the actual POST request
    response = requests.post("www.someurl.com", data=json.dumps({}), headers=headers)

    # Assert the expected request data
    mock_post.assert_called_with("www.someurl.com", data=json.dumps({}), headers=headers)
    assert response.status_code == 200
    assert mock_post.call_args[1]['headers'] == expected_headers
    assert response.json() == mock_response_data

    
