import requests
import threading

class VaultAPI:
    URL = "https://auth.idp.hashicorp.com/oauth2/token"
    lock_instance = threading.Lock()
    instance = None

    @classmethod
    def get_instance(cls):
        with cls.lock_instance:
            if not cls.instance:
                cls.instance = VaultAPI()
        return cls.instance

    def get_hcp_api_token(self,client_id:str, client_secret:str):
        """
        Retrieve HCP API Token
        :param client_id: The Client ID
        :param client_secret:  The Client Secret
        :return: (str) The retrieved HCP API Token
        """

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
            "audience": "https://api.hashicorp.cloud"
        }

        response = requests.post(self.URL, headers=headers, data=data, timeout=5)

        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise Exception(f"Failed to get HCP API token: {response.status_code} - {response.text}")


    def fetch_secrets(self,api_token:str, organization_id:str, project_id:str, app_name:str):
        """
        Fetch secrets using the HCP API Token
        :param api_token: HCP API token
        :param organization_id: organization ID
        :param project_id: project ID
        :param app_name: application name
        :return: (dict) dictionary of secrets
        """

        url = f"https://api.cloud.hashicorp.com/secrets/2023-11-28/organizations/{organization_id}/projects/{project_id}/apps/{app_name}/secrets:open"
        headers = {"Authorization": f"Bearer {api_token}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch secrets from {url}: {response.status_code} - {response.text}")
