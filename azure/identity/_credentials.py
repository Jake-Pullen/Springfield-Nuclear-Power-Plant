"""Mock Azure Identity credentials"""
import time
import random
from azure.core.exceptions import ClientAuthenticationError


class DefaultAzureCredential:
    """Mock default Azure credential"""
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self._authenticated = False
    
    def get_token(self, *scopes, **kwargs):
        """Get an access token"""
        # Simulate authentication delay
        time.sleep(random.uniform(0.1, 0.3))
        # Simulate occasional auth failures (2% rate)
        if random.random() < 0.02:
            raise ClientAuthenticationError("Authentication failed - invalid credentials")
        self._authenticated = True
        # Return mock token
        return MockAccessToken()


class MockAccessToken:
    """Mock access token"""
    def __init__(self):
        self.token = "mock_token_" + str(random.randint(100000, 999999))
        self.expires_on = time.time() + 3600  # 1 hour from now
