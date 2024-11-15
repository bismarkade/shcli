from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from auth.login_model import LoginModel


class LoginAuth:

    _TOKEN_URL = "https://services.sentinel-hub.com/auth/realms/main/protocol/openid-connect/token"
    
    def __init__(self, login_parameters: LoginModel):
        self.login_parameters = login_parameters
        self.oauth_session: OAuth2Session | None = None 
        self.token: dict | None = None 

    def get_token(self) -> dict:
        """ 
        Fetch access token 
        """
        client = BackendApplicationClient(client_id=self.login_parameters.client_id)
        self.oauth_session = OAuth2Session(client=client)

        # Register Complaince Hook--> recommended in the API documentation
        self.oauth_session.register_compliance_hook("access_token_response", self.sentinelhub_compliance_hook)
        
        self.token = self.oauth_session.fetch_token(
            token_url=self._TOKEN_URL,
            client_secret=self.login_parameters.client_secret,
            include_client_id=True
        )

        return self.token


    def sentinelhub_compliance_hook(self, response):
        """ 
        Recommended compliance Hook to handle Error -> Src API documentation
        """
        response.raise_for_status()
        return response
    
    