import requests
from enum import Enum

class VaultFields(Enum):
    USER = "name"
    PASSWORD = "version"

class VaultAPI:
    credentials_dict = {}
    URL = "https://auth.idp.hashicorp.com/oauth2/token"
    HCP_CLIENT_ID = "cTpBXF0Bq52Mn1K5FWL9bY3cHrHDKk9P"
    ORGANIZATION_ID = "7e48578e-e4a2-443d-9cad-d61f13e0ad87"
    PROJECT_ID = "c15a31a9-fc11-4532-bf85-82a98804f390"
    APP_NAME = "sample-app"

    def get_hcp_api_token(self, client_secret):

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "client_id": self.HCP_CLIENT_ID,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
            "audience": "https://api.hashicorp.cloud"
        }

        response = requests.post(self.URL, headers=headers, data=data)

        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise Exception(f"Failed to get HCP API token: {response.status_code} - {response.text}")

    # Step 2: Fetch secrets using the HCP API Token
    def fetch_secrets(self,api_token, organization_id, project_id, app_name):
        url = f"https://api.cloud.hashicorp.com/secrets/2023-11-28/organizations/{organization_id}/projects/{project_id}/apps/{app_name}/secrets:open"
        headers = {"Authorization": f"Bearer {api_token}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch secrets: {response.status_code} - {response.text}")

    def retrieve_secrets(self,secret_key):
        try:
            print("Getting HCP API token and secrets")
            hcp_api_token = self.get_hcp_api_token(client_secret=secret_key)
            secrets = self.fetch_secrets(
                api_token=hcp_api_token,
                organization_id=self.ORGANIZATION_ID,
                project_id=self.PROJECT_ID,
                app_name=self.APP_NAME)

            users_passwords_dict = {}
            for user_data in secrets:
                # Filtering the relevant fields from the vault response.
                users_passwords_dict[user_data[VaultFields.USER.value]] = {
                    field.value: user_data[field.value]
                }
            self.credentials_dict.update(users_passwords_dict)

        except Exception as e:
            print(f"An error occurred: {e}")

    def get_credentials(self, user_enum):
        username = user_enum.value
        password = self.credentials_dict[username][VaultFields.PASSWORD.value]>