"""Example: Bulk migration of Springfield resources"""
import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from workshop.utilities import WorkshopUtilities


def main():
    # Initialize Azure client
    credential = DefaultAzureCredential()
    client = ResourceManagementClient(credential, "springfield-sub-12345")
    
    # Load CSV data
    df = pd.read_csv("springfield_azure_resources.csv")
    
    # Create resource groups first
    resource_groups = df['resource_group_name'].unique()
    for rg_name in resource_groups:
        try:
            client.resource_groups.create_or_update(
                rg_name,
                {"location": "uksouth", "tags": {"migration": "springfield"}}
            )
            print(f"✓ Created resource group: {rg_name}")
        except Exception as e:
            print(f"✗ Failed to create {rg_name}: {e}")
    
    # Prepare resources for bulk creation
    resources_data = []
    for _, row in df.iterrows():
        resources_data.append({
            'name': row['resource_name'],
            'resource_type': row['resource_type'],
            'resource_group': row['resource_group_name'],
            'location': 'uksouth',  # Standardized location
            'tags': {
                'owner': row['owner'],
                'environment': row['environment'],
                'migration_wave': str(row['migration_wave'])
            }
        })
    
    # Bulk create resources
    print(f"\nCreating {len(resources_data)} resources...")
    
    def progress_callback(tracker):
        print(f"\rProgress: {tracker.percentage:.1f}% "
              f"({tracker.completed} completed, {tracker.failed} failed)", 
              end='', flush=True)
    
    tracker = WorkshopUtilities.bulk_create_resources(
        client, 
        resources_data, 
        progress_callback
    )
    
    print(f"\n\nMigration complete!")
    print(f"Total time: {tracker.elapsed_time:.2f} seconds")
    print(f"Success rate: {(tracker.completed/tracker.total)*100:.1f}%")
    
    if tracker.errors:
        print(f"\nErrors encountered:")
        for error in tracker.errors[:5]:  # Show first 5 errors
            print(f"  - {error}")


if __name__ == "__main__":
    main()
