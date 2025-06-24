"""Resources operations"""
import time
import random
from typing import Dict, Any, Optional
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError, HttpResponseError
from azure.core.paging import ItemPaged
from ..models import GenericResource, ProvisioningState
from datetime import datetime, timezone


class ResourcesOperations:
    """Operations for Resources"""
    
    def __init__(self, client):
        self._client = client
        self._store: Dict[str, GenericResource] = self._client._resource_store
    
    def create_or_update(self, resource_group_name: str, 
                        resource_provider_namespace: str,
                        parent_resource_path: str,
                        resource_type: str,
                        resource_name: str,
                        parameters: Dict[str, Any],
                        api_version: str = "2021-04-01") -> GenericResource:
        """Create or update a resource"""
        # Simulate API delay
        time.sleep(random.uniform(0.1, 0.3))
        
        # Validate resource group exists
        if resource_group_name not in self._client._resource_groups_store:
            raise ResourceNotFoundError(f"Resource group '{resource_group_name}' not found")
        
        # Build resource ID
        resource_id = (f"/subscriptions/{self._client.subscription_id}"
                      f"/resourceGroups/{resource_group_name}"
                      f"/providers/{resource_provider_namespace}"
                      f"/{resource_type}/{resource_name}")
        
        # Enhanced failure simulation
        failure_scenarios = [
            (0.02, "QuotaExceeded", 429),
            (0.01, "InvalidLocation", 400), 
            (0.015, "AuthorizationFailed", 403),
            (0.005, "InternalServerError", 500)
        ]
        for probability, error_msg, status_code in failure_scenarios:
            if random.random() < probability:
                raise HttpResponseError(f"{error_msg}: {resource_name}", status_code)
        # Simulate occasional failures (5% failure rate)
        if random.random() < 0.05:
            raise HttpResponseError(f"Failed to create resource '{resource_name}' - Rate limited", 429)
        
        # Create resource
        resource = GenericResource(
            id=resource_id,
            name=resource_name,
            type=f"{resource_provider_namespace}/{resource_type}",
            location=parameters.get('location', 'uksouth'),
            tags=parameters.get('tags', {}),
            properties=parameters.get('properties', {}),
            provisioning_state=ProvisioningState.SUCCEEDED,
            created_time=datetime.now(timezone.utc),
            changed_time=datetime.now(timezone.utc)
        )
        
        self._store[resource_id] = resource
        return resource
    
    def get(self, resource_group_name: str,
            resource_provider_namespace: str,
            parent_resource_path: str,
            resource_type: str,
            resource_name: str,
            api_version: str = "2021-04-01") -> GenericResource:
        """Get a resource"""
        resource_id = (f"/subscriptions/{self._client.subscription_id}"
                      f"/resourceGroups/{resource_group_name}"
                      f"/providers/{resource_provider_namespace}"
                      f"/{resource_type}/{resource_name}")
        
        if resource_id not in self._store:
            raise ResourceNotFoundError(f"Resource '{resource_name}' not found")
        
        return self._store[resource_id]
    
    def delete(self, resource_group_name: str,
               resource_provider_namespace: str,
               parent_resource_path: str,
               resource_type: str,
               resource_name: str,
               api_version: str = "2021-04-01") -> None:
        """Delete a resource"""
        resource_id = (f"/subscriptions/{self._client.subscription_id}"
                      f"/resourceGroups/{resource_group_name}"
                      f"/providers/{resource_provider_namespace}"
                      f"/{resource_type}/{resource_name}")
        
        if resource_id not in self._store:
            raise ResourceNotFoundError(f"Resource '{resource_name}' not found")
        
        # Simulate deletion delay
        time.sleep(random.uniform(0.2, 0.5))
        del self._store[resource_id]
    
    def list(self, filter: Optional[str] = None) -> ItemPaged[GenericResource]:
        """List all resources in subscription"""
        resources = list(self._store.values())
        
        # Apply filter if provided
        if filter:
            # Simple tag-based filtering
            if "tagName eq" in filter:
                tag_filter = filter.split("'")[1] if "'" in filter else ""
                resources = [r for r in resources if r.tags and tag_filter in r.tags]
        
        return ItemPaged(resources)
    
    def list_by_resource_group(self, resource_group_name: str,
                              filter: Optional[str] = None) -> ItemPaged[GenericResource]:
        """List resources in a resource group"""
        resources = []
        for resource in self._store.values():
            if f"/resourceGroups/{resource_group_name}/" in resource.id:
                resources.append(resource)
        
        return ItemPaged(resources)
