"""
Canonical repository configuration, SSoT paths, WORM tables, stub allowlists, and aliases.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

VALID_SCOPES: tuple[str, ...] = (
    "all",
    "domain",
    "erd",
    "contracts",
    "ui",
    "uc",
    "nav",
    "rbac",
    "arch",
    "api",
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
    dm_puml: str = "domain-models/class/DT-DM-001.puml"
    erd_doc: str = "domain-models/entity-relationship/DT-ERD-DOC-001.md"
    erd_sql: str = "domain-models/entity-relationship/DT-ERD-001.sql"
    erd_dbml: str = "domain-models/entity-relationship/DT-ERD-001.dbml"
    uc_trc_doc: str = "domain-models/use-cases/DT-UC-TRC-001.md"
    ui_ds_doc: str = "ui-ux/DT-UI-DS-DOC-001.md"
    ui_svg_doc: str = "ui-ux/DT-UI-SVG-DOC-001.md"
    ui_nav_doc: str = "ui-ux/DT-UI-NAV-DOC-001.md"
    ui_ctr_doc: str = "ui-ux/contracts/DT-UI-CTR-001.md"
    arq_cmp_doc: str = "architecture/views/DT-ARQ-CMP-DOC-001.md"
    arq_cmp_dsl: str = "architecture/views/DT-ARQ-CMP-001-component-model.dsl"
    arq_dep_doc: str = "architecture/views/DT-ARQ-DEP-DOC-001.md"
    arq_dep_dsl: str = "architecture/views/DT-ARQ-DEP-001-deployment-model.dsl"
    arq_db_doc: str = "architecture/DT-ARQ-DB-DOC-001.md"
    arq_tech: str = "architecture/DT-ARQ-TECH-001.md"
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
            "DT-DM-001.puml": self.dm_puml,
            "DT-ERD-DOC-001.md": self.erd_doc,
            "DT-ERD-001.sql": self.erd_sql,
            "DT-ERD-001.dbml": self.erd_dbml,
            "DT-UC-TRC-001.md": self.uc_trc_doc,
            "DT-UI-DS-DOC-001.md": self.ui_ds_doc,
            "DT-UI-SVG-DOC-001.md": self.ui_svg_doc,
            "DT-UI-NAV-DOC-001.md": self.ui_nav_doc,
            "DT-UI-CTR-001.md": self.ui_ctr_doc,
            "DT-ARQ-CMP-DOC-001.md": self.arq_cmp_doc,
            "DT-ARQ-CMP-001-component-model.dsl": self.arq_cmp_dsl,
            "DT-ARQ-DEP-DOC-001.md": self.arq_dep_doc,
            "DT-ARQ-DEP-001-deployment-model.dsl": self.arq_dep_dsl,
            "DT-ARQ-DB-DOC-001.md": self.arq_db_doc,
            "DT-ARQ-TECH-001.md": self.arq_tech,
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

# Planned artifact IDs referenced in SSoT docs whose diagram/file is scheduled post-MVP
PLANNED_ARTIFACT_STUBS: frozenset[str] = frozenset(
    {
        "DT-ERD-LOG-001",
    }
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
    "RbacModule": "RolePermission.module",
    "RolePermissionAction": "RolePermission.action",
    "RbacAction": "RolePermission.action",
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
    "StandardUnitOfMeasure": frozenset({"EA", "SET", "L", "KG", "M"}),
    "TelemetryAlarmSeverity": frozenset({"NONE", "WARNING_P2", "CRITICAL_P1"}),
    "ZeroEnergyState": frozenset({"ENERGIZED", "UNCERTAIN", "ZERO_ENERGY_VERIFIED"}),
}

# Screen-local UI presentation/filter/dock enums (not persisted domain vocabularies)
UI_LOCAL_ENUM_ALLOWLIST: frozenset[str] = frozenset(
    {
        "AuditDockTab",
        "AuditExportFormat",
        "AuditKpiFilterCategory",
        "BacklogDockTab",
        "BacklogExportFormat",
        "BoundaryConflictType",
        "BoundaryDockTab",
        "BoundaryValidationState",
        "BoundaryViewMode",
        "CatalogExportFormat",
        "CatalogValidationSeverity",
        "IsoFunctionalLocationLevel",
        "KardexDockTab",
        "KardexExportFormat",
        "KardexKpiFilterCategory",
        "KardexMovementFilterType",
        "MasterCardMode",
        "MaterialAvailabilityStatus",
        "PartMasterDockTab",
        "PartMasterKpiFilter",
        "RbacDockTab",
        "RbacMatrixExportFormat",
        "RbacRoleFilterCategory",
        "RbacRoleLifecycleFilter",
        "RimePriorityBand",
        "StockPolicyAlertType",
        "TaxonomyConflictType",
        "TaxonomyDockTab",
        "TaxonomyExportFormat",
        "TaxonomyInspectorMode",
        "UserDockTab",
        "UserKpiFilterCategory",
        "UserLifecycleActionType",
        "ValidationConflictType",
    }
)

# Canonical RBAC roles approved across SCR-ADM-013, DT-UI-NAV-DOC-001, and UC-* specs
APPROVED_RBAC_ROLES: frozenset[str] = frozenset(
    {
        "Technician",
        "Maintenance Technician",
        "Field Technician",
        "Supervisor",
        "Maintenance Supervisor",
        "Planner",
        "Maintenance Planner",
        "Reliability Eng.",
        "Reliability Engineer",
        "Reliability Engineering",
        "Warehouse Manager",
        "HSEQ",
        "HSEQ Inspector",
        "Administrator",
        "System Administrator",
        "Auditor",
        "Manager",
        "Plant Manager",
        "Plant Operations Manager",
        "Project Engineer",
        "Plant Operator",
        "Scheduler",
        "Contractor",
        "All Roles",
    }
)

# Valid non-human system/service actors allowed in UC secondary_actors
APPROVED_SYSTEM_ACTORS: frozenset[str] = frozenset(
    {
        "System (Digital Twin Engine)",
        "Task Planning Service",
        "Audit Log Service",
        "Notification Service",
        "Telemetry Ingestion Service",
        "LOTO Safety Watchdog",
        "Offline Sync Worker",
        "SCADA Engine",
        "SCADA / Historian",
        "SCADA / Historian Module",
        "IoT Hub",
    }
)

# Canonical Segregation-of-Duties codes and safety constants in DT-DM-DOC-001 §5
CANONICAL_SOD_CODES: tuple[str, ...] = (
    "SOD-SAF-01",
    "SOD-INV-01",
    "SOD-MTTO-01",
    "SOD-SYS-01",
)

CANONICAL_SAFETY_THRESHOLDS: tuple[str, ...] = (
    "0.0 V",
    "0.5 psig",
    "15 m",
    "13 m",
    "5 m",
)

# Approved color palette hex codes (DT-UI-DS-DOC-001 v2.2 / v2.3)
APPROVED_COLOR_PALETTE: frozenset[str] = frozenset(
    {
        "#11141A", "#16191F", "#1E222B", "#2A2F3D", "#353B4D", "#3A4154",
        "#5C667A", "#6B7280", "#6E7A92", "#7E8B9B", "#8A98AA", "#AAB1BD",
        "#B8C0CC", "#D8DBE0", "#E5E8EC", "#F4F5F7", "#FAFBFC", "#FCFDFD",
        "#FFFFFF", "#FDFEFE", "#C2CBD6", "#4B5563", "#1F2937", "#111827",
        "#E63946", "#AC5E04", "#D97706", "#F4A261", "#2563EB", "#4881A4",
        "#457B9D", "#0B857A", "#0D9488", "#2A9D8F", "#9CA3AF", "#4A5263",
        "#BAE6FD", "#0369A1",
        "#0A0E15", "#0D1117", "#131923", "#18202C", "#1E2736", "#222B3A", "#2B3648",
        "#607089", "#8B9BB2", "#94A3B8", "#F1F5F9",
        "#0F172A", "#475569", "#526075", "#64748B", "#BCC5D1", "#CBD5E1", "#CFD6DF",
        "#E1E6EC", "#ECEFF3", "#F0F3F7", "#F7F9FB",
        "#B45309", "#60A5FA",
        "#A21CAF", "#E879F9",
    }
)

# Approved MVP Use Case and Screen catalogs (plus dynamic discovery checks)
MVP_APPROVED_UCS: frozenset[str] = frozenset(
    {
        "UC-VIS-008", "UC-VIS-009", "UC-VIS-010", "UC-VIS-011", "UC-VIS-033",
        "UC-MTTO-001", "UC-MTTO-002", "UC-MTTO-023", "UC-MTTO-026", "UC-MTTO-029",
        "UC-INV-005", "UC-INV-006", "UC-INV-007", "UC-INV-025", "UC-INV-027", "UC-INV-031",
        "UC-ADM-013", "UC-ADM-014", "UC-ADM-032",
    }
)

MVP_APPROVED_SCREENS: frozenset[str] = frozenset(
    {
        "SCR-VIS-001", "SCR-VIS-002", "SCR-VIS-003",
        "SCR-VIS-008", "SCR-VIS-011", "SCR-VIS-033",
        "SCR-MTTO-001", "SCR-MTTO-002", "SCR-MTTO-003", "SCR-MTTO-004", "SCR-MTTO-005",
        "SCR-MTTO-023", "SCR-MTTO-026", "SCR-MTTO-029",
        "SCR-INV-001", "SCR-INV-002", "SCR-INV-003", "SCR-INV-004", "SCR-INV-005",
        "SCR-INV-006", "SCR-INV-025", "SCR-INV-027", "SCR-INV-031",
        "SCR-ADM-001", "SCR-ADM-002", "SCR-ADM-003",
        "SCR-ADM-013", "SCR-ADM-014", "SCR-ADM-032",
    }
)
