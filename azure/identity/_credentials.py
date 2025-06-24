import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class AccessToken:
    """Access token for Azure authentication"""
    token: str = field(default_factory=lambda: f"eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6I...{uuid.uuid4()}")
    expires_on: float = field(default_factory=lambda: time.time() + 3600)


class DefaultAzureCredential:
    """Default credential for Azure authentication"""
    def __init__(self):
        self.authenticated = True
        
    def get_token(self, *scopes: str) -> AccessToken:
        """Get an access token for the specified scopes"""
        if not self.authenticated:
            from azure.core.exceptions import ClientAuthenticationError
            raise ClientAuthenticationError("Authentication failed")
        return AccessToken()
