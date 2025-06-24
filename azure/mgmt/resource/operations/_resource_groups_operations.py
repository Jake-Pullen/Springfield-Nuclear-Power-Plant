"""Resource Groups operations"""
import time
import random
from typing import Dict, Any, Optional
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError, HttpResponseError
from azure.core.paging import ItemPaged
from ..models import ResourceGroup


class ResourceGroupsOperations:
    """Operations for Resource Groups"""
    
    def __init__(self, client):
        self._client = client
        self._store = client._resource_groups_store
        
    def create_or_update(self, resource_group_name: str, parameters: Dict[str, Any]) -> ResourceGroup:
        """Create or update a resource group"""
        # Simulate network delay
        time.sleep(random.uniform(0.5, 1.5))
        
        # Validate parameters
        if 'location' not in parameters:
            raise HttpResponseError("Location is required for resource group")
        
        # Simulate occasional failures
        if random.random() < 0.05:  # 5% failure rate
            raise HttpResponseError("Service temporarily unavailable", 503)
        
        rg = ResourceGroup(
            id=f"/subscriptions/{self._client.subscription_id}/resourceGroups/{resource_group_name}",
            name=resource_group_name,
            location=parameters['location'],
            tags=parameters.get('tags'),
            properties={'provisioningState': 'Succeeded'}
        )
        
        self._store[resource_group_name] = rg
        return rg
    
    def get(self, resource_group_name: str) -> ResourceGroup:
        """Get a resource group"""
        time.sleep(random.uniform(0.1, 0.3))
        
        if resource_group_name not in self._store:
            raise ResourceNotFoundError(f"Resource group '{resource_group_name}' not found")
        
        return self._store[resource_group_name]
    
    def delete(self, resource_group_name: str) -> None:
        """Delete a resource group"""
        time.sleep(random.uniform(1, 2))
        
        if resource_group_name not in self._store:
            raise ResourceNotFoundError(f"Resource group '{resource_group_name}' not found")
        
        # Delete all resources in the group
        resources_to_delete = []
        for resource_id, resource in self._client._resource_store.items():
            if f"/resourceGroups/{resource_group_name}/" in resource_id:
                resources_to_delete.append(resource_id)
        
        for resource_id in resources_to_delete:
            del self._client._resource_store[resource_id]
        
        del self._store[resource_group_name]
    
    def list(self) -> ItemPaged[ResourceGroup]:
        """List all resource groups"""
        return ItemPaged(list(self._store.values()))
    
    def check_existence(self, resource_group_name: str) -> bool:
        """Check if resource group exists"""
        time.sleep(random.uniform(0.05, 0.1))
        return resource_group_name in self._store
