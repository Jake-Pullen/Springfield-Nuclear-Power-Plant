"""Tags operations"""
import time
import random
from typing import Dict, Any, Optional
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError


class TagsOperations:
    """Operations for Tags"""
    
    def __init__(self, client):
        self._client = client
    
    def create_or_update_at_scope(self, scope: str, 
                                 parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Create or update tags at scope"""
        # Simulate API delay
        time.sleep(random.uniform(0.05, 0.15))
        
        # Find resource by scope (resource ID)
        if scope in self._client._resource_store:
            resource = self._client._resource_store[scope]
            
            # Update tags
            new_tags = parameters.get('properties', {}).get('tags', {})
            if resource.tags:
                resource.tags.update(new_tags)
            else:
                resource.tags = new_tags.copy()
            
            return {
                'properties': {
                    'tags': resource.tags
                }
            }
        else:
            raise ResourceNotFoundError(f"Resource with scope '{scope}' not found")
    
    def get_at_scope(self, scope: str) -> Dict[str, Any]:
        """Get tags at scope"""
        if scope in self._client._resource_store:
            resource = self._client._resource_store[scope]
            return {
                'properties': {
                    'tags': resource.tags or {}
                }
            }
        else:
            raise ResourceNotFoundError(f"Resource with scope '{scope}' not found")
    
    def delete_at_scope(self, scope: str) -> None:
        """Delete all tags at scope"""
        if scope in self._client._resource_store:
            resource = self._client._resource_store[scope]
            resource.tags = {}
        else:
            raise ResourceNotFoundError(f"Resource with scope '{scope}' not found")
