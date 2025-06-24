#!/usr/bin/env python3
"""
Springfield Nuclear Power Plant - Azure Migration Data Generator
Generates realistic Azure resource data with intentional quality issues for workshop
"""

import csv
import random
from datetime import datetime, timedelta
from faker import Faker
import uuid

# Initialize Faker with seed for reproducible results
fake = Faker()
Faker.seed(42)  # Ensures consistent data across workshop runs
random.seed(42)

# Workshop Configuration
TOTAL_RESOURCES = 2500
OUTPUT_FILE = 'springfield_azure_resources.csv'

# Azure Subscription IDs (realistic format)
SUBSCRIPTION_IDS = [
    'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
    'b2c3d4e5-f6g7-8901-bcde-f12345678901',
    'c3d4e5f6-g7h8-9012-cdef-123456789012'
]

# Springfield Characters & Their Roles
SPRINGFIELD_OWNERS = {
    'Homer': {'role': 'Senior Engineer', 'environments': ['prod'], 'weight': 25},
    'Marge': {'role': 'DevOps Lead', 'environments': ['dev', 'staging'], 'weight': 30},
    'Lisa': {'role': 'Junior Developer', 'environments': ['test'], 'weight': 20},
    'Bart': {'role': 'Intern', 'environments': [], 'weight': 8},  # Unauthorized
    'Ned': {'role': 'Former Employee', 'environments': [], 'weight': 7},  # Should be removed
    'Apu': {'role': 'Contractor', 'environments': [], 'weight': 5},  # Should be removed
    'Milhouse': {'role': 'Temp', 'environments': [], 'weight': 5}  # Should be removed
}

# Intentional Data Quality Issues
MESSY_LOCATIONS = [
    'uksouth', 'eastus', 'westus',  # Correct Azure regions
    'Springfield', 'Shelbyville',   # Fictional locations (data quality issue)
    'uk-south', 'east-us',          # Wrong format
    'UK South', 'East US'           # Wrong format with spaces
]

INCONSISTENT_ENVIRONMENTS = [
    'dev', 'prod', 'test', 'staging',  # Correct
    'Dev', 'PROD', 'Test', 'STAGING',  # Case issues
    'development', 'production',        # Non-standard names
    'qa', 'uat'                        # Additional environments
]

# Azure Resource Types
AZURE_RESOURCE_TYPES = [
    'Microsoft.Compute/virtualMachines',
    'Microsoft.Storage/storageAccounts',
    'Microsoft.Sql/servers',
    'Microsoft.Web/sites',
    'Microsoft.Network/virtualNetworks',
    'Microsoft.Network/networkSecurityGroups',
    'Microsoft.Network/loadBalancers',
    'Microsoft.KeyVault/vaults',
    'Microsoft.ContainerInstance/containerGroups',
    'Microsoft.DocumentDB/databaseAccounts'
]

# VM SKUs with intentional inconsistencies
VM_SKUS = [
    'Standard_D2s_v3', 'Standard_D4s_v3', 'Standard_B1s', 'Standard_B2s',
    'STANDARD_D2S_V3', 'standard_d4s_v3',  # Case issues
    'Standard_D8s_v3', 'Standard_F4s_v2'
]

STORAGE_SKUS = ['Standard_LRS', 'Standard_GRS', 'Premium_LRS', 'standard_lrs']
DATABASE_SKUS = ['Basic', 'Standard', 'Premium', 'GeneralPurpose']

# Migration Waves
MIGRATION_WAVES = ['Wave 1', 'Wave 2', 'Wave 3', 'Wave 4', 'wave1', 'WAVE 2']

def get_weighted_owner():
    """Select owner based on weights defined in SPRINGFIELD_OWNERS"""
    owners = list(SPRINGFIELD_OWNERS.keys())
    weights = [SPRINGFIELD_OWNERS[owner]['weight'] for owner in owners]
    return random.choices(owners, weights=weights)[0]

def generate_resource_name(resource_type, environment):
    """Generate realistic Azure resource names"""
    type_prefix = {
        'Microsoft.Compute/virtualMachines': 'vm',
        'Microsoft.Storage/storageAccounts': 'sa',
        'Microsoft.Sql/servers': 'sql',
        'Microsoft.Web/sites': 'app',
        'Microsoft.Network/virtualNetworks': 'vnet',
        'Microsoft.Network/networkSecurityGroups': 'nsg',
        'Microsoft.Network/loadBalancers': 'lb',
        'Microsoft.KeyVault/vaults': 'kv',
        'Microsoft.ContainerInstance/containerGroups': 'ci',
        'Microsoft.DocumentDB/databaseAccounts': 'cosmos'
    }
    
    prefix = type_prefix.get(resource_type, 'res')
    
    # Mix of naming conventions (some good, some inconsistent)
    naming_styles = [
        f"{prefix}-{environment}-{fake.word()}-{random.randint(1, 999):03d}",
        f"{prefix}{environment}{fake.word()}{random.randint(1, 99)}",  # No separators
        f"springfield-{prefix}-{fake.word()}-{environment}",
        f"{fake.company().replace(' ', '').lower()}-{prefix}-{random.randint(1, 999)}"
    ]
    
    return random.choice(naming_styles)

def generate_resource_group_name(environment, owner):
    """Generate resource group names with some inconsistencies"""
    patterns = [
        f"rg-{environment}-{owner.lower()}",
        f"RG-{environment.upper()}-{owner.upper()}",
        f"resourcegroup-{environment}-{fake.word()}",
        f"{owner}-{environment}-rg",
        f"springfield-{environment}-resources"
    ]
    return random.choice(patterns)

def get_sku_for_resource_type(resource_type):
    """Return appropriate SKU based on resource type"""
    if 'virtualMachines' in resource_type:
        return random.choice(VM_SKUS)
    elif 'storageAccounts' in resource_type:
        return random.choice(STORAGE_SKUS)
    elif 'servers' in resource_type:
        return random.choice(DATABASE_SKUS)
    else:
        return random.choice(['Standard', 'Premium', 'Basic'])

def generate_monthly_cost(resource_type, sku, environment):
    """Generate realistic monthly costs based on resource type and environment"""
    base_costs = {
        'Microsoft.Compute/virtualMachines': (50, 500),
        'Microsoft.Storage/storageAccounts': (10, 100),
        'Microsoft.Sql/servers': (100, 2000),
        'Microsoft.Web/sites': (20, 200),
        'Microsoft.Network/virtualNetworks': (5, 50),
        'Microsoft.Network/networkSecurityGroups': (0, 10),
        'Microsoft.Network/loadBalancers': (25, 300),
        'Microsoft.KeyVault/vaults': (5, 30),
        'Microsoft.ContainerInstance/containerGroups': (30, 400),
        'Microsoft.DocumentDB/databaseAccounts': (50, 1000)
    }
    
    min_cost, max_cost = base_costs.get(resource_type, (10, 100))
    
    # Production resources cost more
    if environment.lower() in ['prod', 'production']:
        min_cost *= 2
        max_cost *= 3
    
    # Premium SKUs cost more
    if 'Premium' in sku or 'Standard_D' in sku:
        min_cost *= 1.5
        max_cost *= 2
    
    return round(random.uniform(min_cost, max_cost), 2)

def generate_boolean_with_inconsistency():
    """Generate boolean values with format inconsistencies"""
    boolean_formats = ['true', 'false', 'True', 'False', 'yes', 'no', '1', '0', 'enabled', 'disabled']
    return random.choice(boolean_formats)

def generate_compliance_status():
    """Generate compliance status with inconsistencies"""
    statuses = ['Compliant', 'Non-Compliant', 'compliant', 'UNKNOWN', 'NonCompliant', 'N/A', '']
    return random.choice(statuses)

def generate_migration_status():
    """Generate migration status"""
    statuses = ['NotStarted', 'InProgress', 'Complete', 'Failed', 'not started', 'IN PROGRESS', 'completed']
    return random.choice(statuses)

def generate_tags(owner, environment, cost_center):
    """Generate realistic Azure tags with some inconsistencies"""
    tag_sets = [
        f"Environment={environment},Owner={owner},CostCenter={cost_center}",
        f"env={environment.lower()},owner={owner.lower()},department=nuclear",
        f"Environment:{environment};Owner:{owner};Project:Migration",
        f"owner={owner},env={environment},cost_center={cost_center},backup=required",
        ""  # Some resources have no tags (data quality issue)
    ]
    return random.choice(tag_sets)

def generate_csv_data():
    """Generate the complete dataset"""
    print(f"Generating {TOTAL_RESOURCES} Azure resources for Springfield Nuclear Power Plant...")
    
    resources = []
    
    # Track some statistics for realistic distribution
    homer_resources = 0
    
    for i in range(TOTAL_RESOURCES):
        if i % 500 == 0:
            print(f"Generated {i} resources...")
        
        # Basic resource info
        resource_type = random.choice(AZURE_RESOURCE_TYPES)
        environment = random.choice(INCONSISTENT_ENVIRONMENTS)
        owner = get_weighted_owner()
        
        # Track Homer for crisis scenario
        if owner == 'Homer':
            homer_resources += 1
        
        # Generate resource details
        resource_name = generate_resource_name(resource_type, environment)
        location = random.choice(MESSY_LOCATIONS)
        cost_center = random.choice(['CC001', 'CC002', 'CC003', 'nuclear-ops', 'NUCLEAR_OPS', ''])
        
        # Azure-specific fields
        subscription_id = random.choice(SUBSCRIPTION_IDS)
        resource_group_name = generate_resource_group_name(environment, owner)
        resource_id = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/{resource_type}/{resource_name}"
        sku = get_sku_for_resource_type(resource_type)
        
        # Operational metadata
        status = random.choice(['Running', 'Stopped', 'Failed', 'Updating', 'running', 'STOPPED'])
        provisioning_state = random.choice(['Succeeded', 'Failed', 'InProgress', 'succeeded'])
        
        # Dates
        created_date = fake.date_between(start_date='-2y', end_date='-1m')
        last_modified_date = fake.date_between(start_date=created_date, end_date='today')
        
        # Cost and governance
        monthly_cost = generate_monthly_cost(resource_type, sku, environment)
        compliance_status = generate_compliance_status()
        backup_enabled = generate_boolean_with_inconsistency()
        monitoring_enabled = generate_boolean_with_inconsistency()
        
        # Security
        security_group = f"nsg-{environment}-{random.randint(1, 10)}" if random.random() > 0.2 else ""
        public_ip_enabled = generate_boolean_with_inconsistency()
        encryption_status = random.choice(['Enabled', 'Disabled', 'enabled', 'Not Configured', ''])
        identity_type = random.choice(['SystemAssigned', 'UserAssigned', 'None', 'system-assigned'])
        
        # Migration-specific
        migration_wave = random.choice(MIGRATION_WAVES)
        migration_status = generate_migration_status()
        on_premises_server = f"SPNF-{fake.word().upper()}-{random.randint(1, 999):03d}" if random.random() > 0.3 else ""
        
        # Dependencies (some resources have dependencies)
        dependencies = ""
        if random.random() > 0.7:  # 30% have dependencies
            dep_count = random.randint(1, 3)
            deps = [f"res-{fake.word()}-{random.randint(1, 999)}" for _ in range(dep_count)]
            dependencies = ",".join(deps)
        
        # Tags
        tags = generate_tags(owner, environment, cost_center)
        
        # Managed by (some resources managed by other services)
        managed_by = ""
        if resource_type in ['Microsoft.Compute/virtualMachines', 'Microsoft.Storage/storageAccounts']:
            if random.random() > 0.8:  # 20% managed by other services
                managed_by = random.choice([f"{owner}-automation", "Azure-Backup", "azure-site-recovery", ""])
        
        resource = {
            'resource_name': resource_name,
            'resource_type': resource_type,
            'location': location,
            'owner': owner,
            'environment': environment,
            'cost_center': cost_center,
            'created_date': created_date.strftime('%Y-%m-%d'),
            'last_modified_date': last_modified_date.strftime('%Y-%m-%d'),
            'tags': tags,
            'subscription_id': subscription_id,
            'resource_group_name': resource_group_name,
            'resource_id': resource_id,
            'sku': sku,
            'status': status,
            'provisioning_state': provisioning_state,
            'managed_by': managed_by,
            'monthly_cost': monthly_cost,
            'compliance_status': compliance_status,
            'backup_enabled': backup_enabled,
            'monitoring_enabled': monitoring_enabled,
            'security_group': security_group,
            'public_ip_enabled': public_ip_enabled,
            'encryption_status': encryption_status,
            'identity_type': identity_type,
            'migration_wave': migration_wave,
            'migration_status': migration_status,
            'on_premises_server': on_premises_server,
            'dependencies': dependencies
        }
        
        resources.append(resource)
    
    print(f"\nDataset Statistics:")
    print(f"Total Resources: {len(resources)}")
    print(f"Homer's Resources: {homer_resources} (will need transfer during crisis)")
    
    # Count by environment
    env_counts = {}
    for resource in resources:
        env = resource['environment'].lower()
        env_counts[env] = env_counts.get(env, 0) + 1
    
    print(f"Environment Distribution:")
    for env, count in sorted(env_counts.items()):
        print(f"  {env}: {count}")
    
    return resources

def write_csv(resources, filename):
    """Write resources to CSV file"""
    print(f"\nWriting {len(resources)} resources to {filename}...")
    
    fieldnames = [
        'resource_name', 'resource_type', 'location', 'owner', 'environment', 
        'cost_center', 'created_date', 'last_modified_date', 'tags',
        'subscription_id', 'resource_group_name', 'resource_id', 'sku',
        'status', 'provisioning_state', 'managed_by', 'monthly_cost',
        'compliance_status', 'backup_enabled', 'monitoring_enabled',
        'security_group', 'public_ip_enabled', 'encryption_status', 'identity_type',
        'migration_wave', 'migration_status', 'on_premises_server', 'dependencies'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(resources)
    
    print(f"✅ CSV file generated successfully: {filename}")
    print(f"File size: ~{len(resources) * 200 / 1024:.1f} KB")

def main():
    """Main execution function"""
    print("🏭 Springfield Nuclear Power Plant - Azure Migration Data Generator")
    print("=" * 70)
    
    # Generate the data
    resources = generate_csv_data()
    
    # Write to CSV
    write_csv(resources, OUTPUT_FILE)
    
    print("\n📋 Workshop Data Quality Issues Included:")
    print("✓ Mixed location formats (Springfield, uksouth, UK South)")
    print("✓ Inconsistent environment naming (dev, Dev, PROD)")
    print("✓ Unauthorized owners (Bart, Ned, Apu, Milhouse)")
    print("✓ Mixed boolean formats (true, True, yes, 1)")
    print("✓ Inconsistent compliance status formats")
    print("✓ Missing tags and empty fields")
    print("✓ Case sensitivity issues in multiple fields")
    
    print(f"\n🎯 Workshop Scenarios Ready:")
    print(f"✓ Scale demonstration with {TOTAL_RESOURCES} resources")
    print("✓ Data cleansing challenges across multiple fields")
    print("✓ Homer crisis scenario with realistic resource distribution")
    print("✓ Cost analysis and governance reporting capabilities")
    print("✓ Security audit scenarios (public IPs, encryption)")
    
    print(f"\n🚀 Ready for Springfield Cloud Migration Workshop!")
    print(f"Load '{OUTPUT_FILE}' to begin the automation adventure!")

if __name__ == "__main__":
    main()