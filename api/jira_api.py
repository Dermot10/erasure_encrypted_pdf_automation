import os
import requests


class JiraAPI:  
    def __init__(self):
        self.base_url = os.environ.get('JIRA_BASE_URL')
        self.username = os.environ.get('JIRA_USERNAME')
        self.api_key = os.environ.get('JIRA_API_KEY')
        self.auth = (self.username, self.api_key)
        self.headers = {
            'Accept': 'application/json',
            'X-Atlassian-Token': 'no-check'
        }
        self.endpoint_and_jql_query = """/rest/api/2/search?jql= project = "ERASURE" AND "ServiceNow Ticket - Status[Dropdown]" = "To Start" AND "Request Type[Dropdown]" is not EMPTY ORDER BY created ASC"""

    def connect_to_Jira(self) -> requests.Response:
        """Helper function to connect to the Jira API and return HTTP response."""
        

        try:
            # Send the GET request with the JQL query payload, headers, and authentication
            response = requests.get(f"{self.base_url}{self.endpoint_and_jql_query}", headers=self.headers, auth=self.auth)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def get_jira_data(self) -> list:
        """Function to get ERASURE BOARD in-progress data for further file processing"""
        response = self.connect_to_Jira()

        if response and response.status_code == 200:
            data = response.json()  # Get the JSON response data
            print("Successful API request, data retrieved")
            return data.get("issues", [])
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []

    def get_current_user(self): 
        """Function to get current user and assign to the Jira ticket"""
        try:
            # Send the GET request with the JQL query payload, headers, and authentication
            response = requests.get(f"{self.base_url}/rest/api/2/myself", headers=self.headers, auth=self.auth)
            if response and response.status_code == 200:
                data = response.json()  # Get the JSON response data
                print("Successful API request, data retrieved")
                return data.get("displayName")
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return 
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def post_protected_file(self, issue_id, file_path): 
        """Function to post password protected file to Jira"""
        auth=(self.username, self.api_key)
        headers = self.headers
        protected_file = {"file": (os.path.basename(file_path), open(file_path, 'rb'), "application/pdf")} #the pdf name from JSON response needed for file name
        print(protected_file)
        

        try:
            response =  requests.post(f"{self.base_url}/rest/api/2/issue/{issue_id}/attachments", headers=headers, auth=auth, files=protected_file) 
            if response.status_code == 200:
                print(f"PDF attached to Jira issue {issue_id} successfully.")
            else:
                print(f"Error attaching PDF to Jira issue {issue_id}. Status Code: {response.status_code}")
                print(response.text)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

