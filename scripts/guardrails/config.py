"""
Canonical repository configuration, SSoT paths, WORM tables, stub allowlists, and aliases.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

VALID_SCOPES: tuple[str, ...] = (
    "all",
    "seam1",
    "seam2",
    "seam3",
    "seam4",
    "erd",
    "ui",
    "uc",
    "links",
    "ul",
    "tokens",
    "srs",
)

IGNORED_DIR_NAMES: frozenset[str] = frozenset(
    {
        ".git",
        ".venv",
        "venv",
        "node_modules",
        "temp",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
    }
)


@dataclass(frozen=True, slots=True)
class SSoTPaths:
    """Canonical relative paths for all Single-Source-of-Truth repository artifacts."""

    ul_doc: str = "domain-models/ubiquitous-language/DT-UL-DOC-001.md"
    dm_class_doc: str = "domain-models/class/DT-DM-DOC-001.md"
    dm_state_doc: str = "domain-models/class/DT-DM-DOC-002.md"
    erd_doc: str = "domain-models/entity-relationship/DT-ERD-DOC-001.md"
    erd_sql: str = "domain-models/entity-relationship/DT-ERD-001.sql"
    erd_dbml: str = "domain-models/entity-relationship/DT-ERD-001.dbml"
    ui_ds_doc: str = "ui-ux/DT-UI-DS-DOC-001.md"
    ui_svg_doc: str = "ui-ux/DT-UI-SVG-DOC-001.md"
    ui_nav_doc: str = "ui-ux/DT-UI-NAV-DOC-001.md"
    ui_ctr_doc: str = "ui-ux/contracts/DT-UI-CTR-001.md"
    arq_cmp_doc: str = "architecture/views/DT-ARQ-CMP-DOC-001.md"
    arq_db_doc: str = "architecture/DT-ARQ-DB-DOC-001.md"
    adr_003: str = "architecture/adr/ADR-003.md"
    adr_006: str = "architecture/adr/ADR-006.md"
    tokens_css: str = "ui-ux/assets/tokens.css"
    icons_svg: str = "ui-ux/assets/icons.svg"
    todo_md: str = "TODO.md"
    srs_csv: str = "requirements/data/srs.csv"

    def as_dict(self) -> dict[str, str]:
        return {
            "DT-UL-DOC-001.md": self.ul_doc,
            "DT-DM-DOC-001.md": self.dm_class_doc,
            "DT-DM-DOC-002.md": self.dm_state_doc,
            "DT-ERD-DOC-001.md": self.erd_doc,
            "DT-ERD-001.sql": self.erd_sql,
            "DT-ERD-001.dbml": self.erd_dbml,
            "DT-UI-DS-DOC-001.md": self.ui_ds_doc,
            "DT-UI-SVG-DOC-001.md": self.ui_svg_doc,
            "DT-UI-NAV-DOC-001.md": self.ui_nav_doc,
            "DT-UI-CTR-001.md": self.ui_ctr_doc,
            "DT-ARQ-CMP-DOC-001.md": self.arq_cmp_doc,
            "DT-ARQ-DB-DOC-001.md": self.arq_db_doc,
            "ADR-003.md": self.adr_003,
            "ADR-006.md": self.adr_006,
            "tokens.css": self.tokens_css,
            "icons.svg": self.icons_svg,
            "TODO.md": self.todo_md,
            "srs.csv": self.srs_csv,
        }

    def resolve(self, root: Path, key: str) -> Path:
        rel = self.as_dict()[key]
        return root / rel


SSOT_PATHS = SSoTPaths()

# Append-only / WORM tables governed by ADR-003, TR-001, and Timescale/partitioning rules
WORM_TABLES: frozenset[str] = frozenset(
    {
        "adm.audit_logs",
        "inv.inventory_transactions",
        "vis.telemetry_signals",
        "mtto.work_order_histories",
        "adm.audit_retention_partitions",
    }
)

# Known planned artifact stub regexes (exempt from broken-target link errors unless strict)
PLANNED_STUBS: tuple[str, ...] = (
    r"assets/SCR-.*-wireframe\.svg$",
    r"assets/SCR-VIS-.*\.svg$",
    r"views/DT-ARQ-.*\.drawio$",
)

# SQL CHECK enum lookup aliases (table.column -> canonical domain key in DT-DM-DOC-001 §4)
ENUM_ALIASES: dict[str, str] = {
    "maintenance_plan_crafts.craft": "maintenance_plans.required_specialty",
}

# C# enum type name -> canonical Entity.property key in DT-DM-DOC-001 §4
CSHARP_ENUM_ALIASES: dict[str, str] = {
    "EquipmentHealthStatus": "EquipmentUnit.healthStatus",
    "EquipmentLifecycleStatus": "EquipmentUnit.lifecycleStatus",
    "EquipmentMaintenanceStatus": "EquipmentUnit.maintenanceStatus",
    "EquipmentOperationalStatus": "EquipmentUnit.operationalStatus",
    "OperationalStatus": "EquipmentUnit.operationalStatus",
    "EnvironmentalExposureLevel": "FunctionalLocation.environmentalExposure",
    "MaintainableItemStatus": "MaintainableItem.status",
    "BacklogItemStatus": "BacklogItem.status",
    "DetectionMethod": "FailureRecord.detectionMethod",
    "OperationalCondition": "FailureRecord.operationalCondition",
    "OperationalImpact": "FailureRecord.operationalImpact",
    "FailureRecordStatus": "FailureRecord.status",
    "MaintenanceFrequencyType": "MaintenancePlan.frequencyType",
    "MaintenanceIntervalUnit": "MaintenancePlan.intervalUnit",
    "MaintenanceMethod": "MaintenancePlan.maintenanceMethod",
    "WorkOrderType": "WorkOrder.maintenanceMethod",
    "TelemetrySignalType": "TelemetrySignal.signalType",
    "MaintenanceCraft": "MaintenancePlan.requiredSpecialty",
    "MaintenancePlanStatus": "MaintenancePlan.status",
    "MediaAttachmentFileType": "MediaAttachment.fileType",
    "WorkOrderCriticality": "WorkOrder.criticality",
    "WorkOrderStatus": "WorkOrder.currentStatus",
    "WorkRequestStatus": "WorkRequest.status",
    "InventoryTransactionType": "InventoryTransaction.transactionType",
    "SparePartStatus": "SparePart.status",
    "StockPolicy": "SparePart.stockPolicy",
    "IsolationType": "IsolationPoint.isolationType",
    "MeshMappingStatus": "MeshMapping.mappingStatus",
    "VisualLayerStatus": "VisualLayer.status",
    "IsolationStatus": "WorkOrderIsolation.isolationStatus",
    "PhysicalVerificationMethod": "WorkOrderIsolation.tryOutMethod",
    "TryOutMethod": "WorkOrderIsolation.tryOutMethod",
    "PermitType": "WorkPermit.permitType",
    "WorkPermitStatus": "WorkPermit.status",
    "AuditActionType": "AuditLog.actionType",
    "AuthTokenPurpose": "AuthToken.purpose",
    "IdempotencyStatus": "IdempotencyLog.status",
    "RolePermissionModule": "RolePermission.module",
    "UserStatus": "User.status",
    "WorkOrderRole": "WorkOrderAssignment.roleInWork",
}

# Screen-specific subset projections of canonical DT-DM-DOC-001 §4 enums
CSHARP_SUBSET_ENUM_ALIASES: dict[str, str] = {
    "CalendarIntervalUnit": "MaintenancePlan.intervalUnit",
    "TelemetryMeasurementUnit": "MaintenancePlan.intervalUnit",
}

# Validated composite UI presentation projection enums
PRESENTATION_PROJECTION_ENUMS: dict[str, frozenset[str]] = {
    "DismountDestinationStatus": frozenset({"IN_REPAIR", "IN_STORAGE", "DAMAGED"}),
    "TelemetryAlarmSeverity": frozenset({"NONE", "WARNING_P2", "CRITICAL_P1"}),
    "ZeroEnergyState": frozenset({"ENERGIZED", "UNCERTAIN", "ZERO_ENERGY_VERIFIED"}),
}
