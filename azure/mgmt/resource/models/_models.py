"""Azure Resource Management models"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Optional, Any
from enum import Enum


class ProvisioningState(str, Enum):
    """Resource provisioning states"""
    CREATING = "Creating"
    UPDATING = "Updating"
    DELETING = "Deleting"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    CANCELED = "Canceled"


@dataclass
class Sku:
    """Resource SKU"""
    name: str
    tier: Optional[str] = None
    size: Optional[str] = None
    family: Optional[str] = None
    capacity: Optional[int] = None


@dataclass
class Plan:
    """Resource plan"""
    name: str
    publisher: str
    product: str
    promotion_code: Optional[str] = None


@dataclass
class Identity:
    """Resource identity"""
    principal_id: Optional[str] = None
    tenant_id: Optional[str] = None
    type: Optional[str] = None


@dataclass
class Resource:
    """Base Azure resource"""
    id: str
    name: str
    type: str
    location: str
    tags: Optional[Dict[str, str]] = None


@dataclass
class GenericResource(Resource):
    """Generic Azure resource with additional properties"""
    kind: Optional[str] = None
    managed_by: Optional[str] = None
    sku: Optional[Sku] = None
    plan: Optional[Plan] = None
    identity: Optional[Identity] = None
    properties: Optional[Dict[str, Any]] = None
    provisioning_state: Optional[str] = None
    created_time: Optional[datetime] = field(default_factory=lambda: datetime.now(timezone.utc))
    changed_time: Optional[datetime] = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ResourceGroup:
    """Azure resource group"""
    id: str
    name: str
    location: str
    tags: Optional[Dict[str, str]] = None
    properties: Optional[Dict[str, Any]] = None
    managed_by: Optional[str] = None
