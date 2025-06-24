"""Azure Resource Management Client"""
import time
import random
from typing import Dict, Optional
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ClientAuthenticationError
from azure.mgmt.resource.operations import ResourceGroupsOperations, ResourcesOperations, TagsOperations


class ResourceManagementClient:
    """Client for Azure Resource Management"""
    
    def __init__(self, credential: DefaultAzureCredential, subscription_id: str, 
                 api_version: str = "2021-04-01"):
        self.credential = credential
        self.subscription_id = subscription_id
        self.api_version = api_version
        
        # In-memory storage for workshop
        self._resource_store: Dict = {}
        self._resource_groups_store: Dict = {}
        
        # Initialize operations
        self.resource_groups = ResourceGroupsOperations(self)
        self.resources = ResourcesOperations(self)
        self.tags = TagsOperations(self)
        
        # Authenticate
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Azure"""
        try:
            self.credential.get_token("https://management.azure.com/.default")
        except Exception as e:
            raise ClientAuthenticationError(f"Failed to authenticate: {str(e)}")
    
    def close(self):
        """Close the client"""
        pass
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
