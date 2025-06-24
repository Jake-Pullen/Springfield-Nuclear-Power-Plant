# Springfield Cloud Migration Project - Team Brief

We're creating a hands-on workshop that demonstrates the critical need for infrastructure automation through a realistic, large-scale cloud migration scenario.

## The Story: Springfield Nuclear Power Plant's Azure Migration

### **Context**
Springfield Nuclear Power Plant is migrating thousands of resources to Azure. Their infrastructure data is messy, and they'll face operational crises that can only be solved through automation.

### **Workshop Objectives**
- Show students why manual cloud management doesn't scale
- Demonstrate real-world data quality challenges
- Teach bulk operations and emergency response procedures
- Build confidence in automation tools

## Technical Requirements

### **Mock Azure SDK Implementation**
- Create realistic classes that mimic `azure-mgmt-resource` behavior
- No actual Azure connectivity required
- Focus on ResourceManagementClient, ResourceGroups, Resources, Tags
- Include realistic error scenarios and response times

### **CSV Data Specifications**
- **Scale**: 2000-3000 resources (near GitHub file size limit)
- **Resource Types**: VMs, storage accounts, databases, web apps, etc.
- **Columns**: resource_name, resource_type, location, owner, environment, cost_center, created_date, tags

### **Data Quality Issues (Intentional)**
```
Locations: uksouth, Springfield, Shelbyville, eastus, westus
Owners: Homer, Marge, Lisa, Bart, Ned, Apu, Milhouse
Environments: dev, prod, test, staging, Dev, PROD
```

---

## Workshop Flow & Scenarios

### **Phase 1: Data Discovery (2 min)**
- Load massive CSV file
- Students see the scale problem immediately
- Identify data quality issues

### **Phase 2: Data Cleansing (3 min)**
**Business Rules:**
- All locations → `uksouth`
- Remove unauthorized owners: `Bart`, `Ned`, `Apu`, `Milhouse`
- Environment-based ownership:
  - `dev` → `Marge`
  - `prod` → `Homer`
  - `test` → `Lisa`
  - `staging` → `Marge`

### **Phase 3: Mass Resource Creation (2 min)**
- Batch create thousands of resources
- Show progress indicators
- Handle creation failures realistically

### **Phase 4: The Homer Crisis (2 min)**
**Scenario**: Homer caused a production outage and was terminated
**Urgent Task**: 
- Find all Homer's resources (hundreds)
- Transfer ownership to Marge
- Update all related tags and metadata
- Generate compliance report

### **Phase 5: Reporting (1 min)**
- Resource distribution by owner
- Cost analysis by environment
- Compliance dashboard

---

## Key Automation Demonstrations

1. **Scale**: Manual management of 2000+ resources is impossible
2. **Data Quality**: Automated validation and cleansing
3. **Bulk Operations**: Process hundreds of resources in seconds
4. **Emergency Response**: Rapid organizational changes
5. **Governance**: Automated compliance and reporting

---

## Character Roles & Permissions

| Character | Role | Environments | Notes |
|-----------|------|--------------|--------|
| Homer | Senior Engineer | prod | Gets fired mid-workshop |
| Marge | DevOps Lead | dev, staging | Takes over Homer's resources |
| Lisa | Junior Developer | test | Learning environment |
| Bart | Intern | none | Unauthorized access |

---

## Technical Implementation Notes

### **Mock SDK Structure**
```python
class MockResourceManagementClient:
    def __init__(self, credential, subscription_id):
        self.resource_groups = MockResourceGroupsOperations()
        self.resources = MockResourcesOperations()
        self.tags = MockTagsOperations()
```

### **Progress Tracking**
- Show realistic timing (2-3 seconds per batch of 50 resources)
- Include failure scenarios (5-10% failure rate)
- Progress bars and status updates

### **Data Persistence**
- Use in-memory dictionaries to simulate Azure's resource store
- Maintain state throughout workshop scenarios
- Enable realistic queries and updates

## Success Metrics

Students should leave understanding:
- Why automation is non-negotiable at scale
- How to handle real-world data quality issues
- Bulk operations patterns and best practices
- Emergency response procedures
- The business impact of infrastructure automation


## Team Assignments

**Please assign tasks based on your team's expertise:**

1. **CSV Generation**: Create realistic 2000+ resource dataset with intentional quality issues
2. **Mock SDK Development**: Build azure-mgmt-resource simulator with realistic behavior
3. **Workshop Documentation**: Step-by-step guide with code examples
4. **Progress/UI Components**: Visual feedback for bulk operations
5. **Scenario Scripting**: Homer crisis workflow and compliance reporting

**Timeline**: Workshop should be deliverable and testable within the development cycle.

---

This brief provides the foundation for creating an engaging, educational experience that demonstrates real-world automation challenges and solutions. The Springfield theme keeps it memorable while the technical challenges mirror actual enterprise scenarios.