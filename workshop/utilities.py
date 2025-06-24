"""Workshop utilities for Springfield Nuclear Power Plant migration"""
import time
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Callable
from collections import defaultdict
from azure.mgmt.resource import ResourceManagementClient
from azure.core.paging import ItemPaged


class ProgressTracker:
    """Track progress of bulk operations"""
    def __init__(self, total_items: int, callback: Optional[Callable] = None):
        self.total = total_items
        self.completed = 0
        self.failed = 0
        self.errors = []
        self.callback = callback
        self.start_time = time.time()
        
    def update(self, success: bool = True, error: Optional[str] = None):
        """Update progress"""
        if success:
            self.completed += 1
        else:
            self.failed += 1
            if error:
                self.errors.append(error)
        
        if self.callback:
            self.callback(self)
    
    @property
    def percentage(self) -> float:
        """Get completion percentage"""
        processed = self.completed + self.failed
        return (processed / self.total) * 100 if self.total > 0 else 0
    
    @property
    def elapsed_time(self) -> float:
        """Get elapsed time in seconds"""
        return time.time() - self.start_time


class WorkshopUtilities:
    """Utilities for workshop scenarios"""
    
    @staticmethod
    def bulk_create_resources(client: ResourceManagementClient, 
                            resources_data: List[Dict[str, Any]],
                            progress_callback: Optional[Callable] = None) -> ProgressTracker:
        """Bulk create resources with progress tracking"""
        # First, create all unique resource groups
        resource_groups = set(r['resource_group'] for r in resources_data)
        for rg_name in resource_groups:
            try:
                if not client.resource_groups.check_existence(rg_name):
                    client.resource_groups.create_or_update(
                        rg_name,
                        {"location": "uksouth", "tags": {"created_by": "bulk_migration"}}
                    )
            except Exception as e:
                print(f"Warning: Could not create resource group {rg_name}: {e}")
        # Now create resources
        tracker = ProgressTracker(len(resources_data), progress_callback)
        for i, resource_data in enumerate(resources_data):
            try:
                # Parse resource type safely
                if '/' in resource_data['resource_type']:
                    provider_namespace, resource_type = resource_data['resource_type'].split('/', 1)
                else:
                    provider_namespace = 'Microsoft.Resources'
                    resource_type = resource_data['resource_type']
                # Create resource
                client.resources.create_or_update(
                    resource_group_name=resource_data['resource_group'],
                    resource_provider_namespace=provider_namespace,
                    parent_resource_path='',
                    resource_type=resource_type,
                    resource_name=resource_data['name'],
                    parameters={
                        'location': resource_data['location'],
                        'tags': resource_data.get('tags', {}),
                        'properties': resource_data.get('properties', {})
                    }
                )
                tracker.update(True)
            except Exception as e:
                tracker.update(False, str(e))
            # Batch delay every 50 resources
            if (i + 1) % 50 == 0:
                time.sleep(0.5)
        return tracker
    
    @staticmethod
    def find_resources_by_owner(client: ResourceManagementClient, owner: str) -> List[Any]:
        """Find all resources owned by a specific user"""
        owned_resources = []
        
        for resource in client.resources.list():
            if resource.tags and resource.tags.get('owner', '').lower() == owner.lower():
                owned_resources.append(resource)
        
        return owned_resources
    
    @staticmethod
    def transfer_ownership(client: ResourceManagementClient, 
                         from_owner: str, 
                         to_owner: str,
                         progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Transfer ownership of all resources"""
        # Find resources to transfer
        resources_to_transfer = WorkshopUtilities.find_resources_by_owner(client, from_owner)
        tracker = ProgressTracker(len(resources_to_transfer), progress_callback)
        transferred_resources = []
        for resource in resources_to_transfer:
            try:
                # Update tags directly on the resource object
                if not resource.tags:
                    resource.tags = {}
                resource.tags['owner'] = to_owner
                resource.tags['previous_owner'] = from_owner
                resource.tags['ownership_transferred'] = datetime.now(timezone.utc).isoformat()
                # Use the tags operation to persist the change
                client.tags.create_or_update_at_scope(
                    scope=resource.id,
                    parameters={
                        'properties': {
                            'tags': resource.tags
                        }
                    }
                )
                transferred_resources.append(resource)
                tracker.update(True)
            except Exception as e:
                tracker.update(False, str(e))
        return {
            'total_resources': len(resources_to_transfer),
            'successfully_transferred': tracker.completed,
            'failed_transfers': tracker.failed,
            'transferred_resources': transferred_resources,
            'errors': tracker.errors,
            'duration_seconds': tracker.elapsed_time
        }
    
    @staticmethod
    def generate_compliance_report(client: ResourceManagementClient) -> Dict[str, Any]:
        """Generate compliance report for all resources"""
        report = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'total_resources': 0,
            'resources_by_owner': defaultdict(int),
            'resources_by_environment': defaultdict(int),
            'resources_by_location': defaultdict(int),
            'resources_by_type': defaultdict(int),
            'untagged_resources': [],
            'non_compliant_resources': []
        }
        
        # Business rules
        valid_locations = ['uksouth']
        valid_owners = ['Homer', 'Marge', 'Lisa']
        valid_environments = ['dev', 'prod', 'test']
        
        for resource in client.resources.list():
            report['total_resources'] += 1
            
            # Analyze tags
            tags = resource.tags or {}
            owner = tags.get('owner', 'unassigned')
            environment = tags.get('environment', 'untagged')
            
            report['resources_by_owner'][owner] += 1
            report['resources_by_environment'][environment] += 1
            report['resources_by_location'][resource.location] += 1
            report['resources_by_type'][resource.type] += 1
            
            # Check compliance
            compliance_issues = []
            
            if not tags:
                report['untagged_resources'].append(resource.name)
                compliance_issues.append('No tags')
            
            if resource.location not in valid_locations:
                compliance_issues.append(f'Invalid location: {resource.location}')
            
            if owner not in valid_owners and owner != 'unassigned':
                compliance_issues.append(f'Unauthorized owner: {owner}')
            
            if environment not in valid_environments and environment != 'untagged':
                compliance_issues.append(f'Invalid environment: {environment}')
            
            if compliance_issues:
                report['non_compliant_resources'].append({
                    'resource_id': resource.id,
                    'resource_name': resource.name,
                    'resource_type': resource.type,
                    'issues': compliance_issues
                })
        
        # Convert defaultdicts to regular dicts
        for key in ['resources_by_owner', 'resources_by_environment', 
                   'resources_by_location', 'resources_by_type']:
            report[key] = dict(report[key])
        
        return report
