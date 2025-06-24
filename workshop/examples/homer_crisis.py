"""Example: Homer Crisis - Emergency ownership transfer"""
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from workshop.utilities import WorkshopUtilities


def main():
    # Initialize Azure client
    credential = DefaultAzureCredential()
    client = ResourceManagementClient(credential, "springfield-sub-12345")
    
    print("🚨 EMERGENCY: Homer Simpson terminated - initiating ownership transfer")
    print("=" * 60)
    
    # Find Homer's resources
    print("\nSearching for Homer's resources...")
    homer_resources = WorkshopUtilities.find_resources_by_owner(client, "Homer")
    print(f"Found {len(homer_resources)} resources owned by Homer")
    
    # Show breakdown by type
    resource_types = {}
    for resource in homer_resources:
        resource_type = resource.type.split('/')[-1]
        resource_types[resource_type] = resource_types.get(resource_type, 0) + 1
    
    print("\nResource breakdown:")
    for rtype, count in resource_types.items():
        print(f"  - {rtype}: {count}")
    
    # Transfer ownership
    print(f"\nTransferring ownership to Marge...")
    
    def progress_callback(tracker):
        print(f"\rProgress: {tracker.percentage:.1f}% "
              f"({tracker.completed}/{tracker.total})", 
              end='', flush=True)
    
    result = WorkshopUtilities.transfer_ownership(
        client,
        from_owner="Homer",
        to_owner="Marge",
        progress_callback=progress_callback
    )
    
    print(f"\n\nTransfer complete!")
    print(f"  - Total resources: {result['total_resources']}")
    print(f"  - Successfully transferred: {result['successfully_transferred']}")
    print(f"  - Failed transfers: {result['failed_transfers']}")
    print(f"  - Duration: {result['duration_seconds']:.2f} seconds")
    
    # Generate audit report
    print("\nGenerating compliance report...")
    report = WorkshopUtilities.generate_compliance_report(client)
    
    print("\nPost-crisis ownership distribution:")
    for owner, count in report['resources_by_owner'].items():
        print(f"  - {owner}: {count} resources")


if __name__ == "__main__":
    main()
