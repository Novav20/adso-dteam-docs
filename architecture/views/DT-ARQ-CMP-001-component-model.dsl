workspace "System Component Model" {

    model {
        # External Systems and Clients
        mobile_app = softwareSystem "Mobile App" "Offline-first field client for touch execution." "Mobile"
        web_admin = softwareSystem "Web Admin Portal" "HSEQ supervision, planning, and dashboards." "WebBrowser"
        local_db = softwareSystem "SQLite Offline DB" "Offline-first relational store (SQLCipher encrypted)." "Database"
        loto_watchdog = softwareSystem "LOTO Safety Watchdog" "Real-time verification of Zero Energy thresholds on the mobile client." "External"
        object_storage = softwareSystem "Azure Blob Storage" "Binary evidence persistence for ISO 14224 photographs." "External"
        db_postgres = softwareSystem "PostgreSQL Master" "Master relational store (PostgreSQL 18 + TimescaleDB)." "Database"
        azure_iot = softwareSystem "Azure IoT Hub" "Managed broker for asynchronous telemetry ingestion." "Broker"
        redis_cache = softwareSystem "Redis Cache" "Distributed cache for idempotency keys." "Database"
        scada_node = softwareSystem "SCADA Control Station" "Local control station (Edge Node) sending industrial telemetry to Azure IoT." "External"

        monolith = softwareSystem "Modular Monolith" "Sistema Central de Mantenimiento y LOTO (.NET 10)" {
            appContainer = container "Backend Web API" "Modular Monolith Runtime" ".NET 10" {
                group "Driving Adapters" {
                    idempotency_filter = component "Idempotency Filter" "Intercepts requests with the Idempotency-Key header; prevents reprocessing critical transitions resent after reconnection (TR-007)." "IActionFilter" "ComponentShape"
                    api_controllers = component "REST API Controllers" "Exposes HTTPS endpoints; handles optimistic concurrency control using row version marks (RowVersion/ETag)." "Minimal APIs" "ComponentShape"
                    signalr_hub = component "SignalR Hub" "Persistent bidirectional channel over WebSockets (WSS); degrades to polling if the industrial network fails." "SignalR.Hub" "ComponentShape"
                    telemetry_listener = component "Telemetry Listener (IoT)" "Asynchronous consumer (AMQP) of the Azure IoT Hub broker; injects telemetry to the LOTO port." "IHostedService" "ComponentShape"
                    sync_worker = component "Background Sync Worker" "Asynchronously and idempotently processes offline queues transmitted from mobile clients after recovering connection (TR-007)." "IHostedService" "ComponentShape"
                }
                group "Application Core" {
                    tax_port = component "Taxonomy Port" "Manages the ISO 14224 hierarchy (asset registration, decommissioning, re-parenting, and cycle validation)." "ITaxonomyService" "ComponentShape"
                    mtto_port = component "Maintenance Port" "Backlog administration, priority calculations, preventive scheduling, and failure reporting." "IWorkOrderService" "ComponentShape"
                    inv_port = component "Inventory Port" "Warehouse transactions, critical stock control, and physical equipment rotation (Asset Swap)." "IInventoryService" "ComponentShape"
                    loto_port = component "Safety & LOTO Port" "Secure job authorization: permit approval, physical lockouts, and Zero Energy condition." "ILotoService" "ComponentShape"
                    sec_port = component "Security Port" "IAM governance: authentication, session renewal, RBAC validations, and immutable auditing." "ISecurityService" "ComponentShape"
                    rime_calc = component "RIME Calculator" "Encapsulates the RIME prioritization calculation using the Strategy pattern (ADR-002)." "IRimeCalculator" "ComponentShape"
                    event_bus = component "Event Bus Port" "Decouples internal logic between monolith modules via in-memory domain events." "IEventBus" "Broker"
                    telemetry_bus = component "Telemetry Stream Bus" "Internal pub/sub channel for high-frequency safety telemetry streams." "ITelemetryBus" "Broker"
                    idempotency_repo = component "Idempotency Repository" "Abstracts relational persistence of the IdempotencyLog to join the Domain's Unit of Work (ADR-007)." "IIdempotencyRepository" "ComponentShape"
                    media_repo = component "Media Repository" "Manages SAS token issuance for external evidence storage (ADR-008)." "IMediaRepository" "ComponentShape"
                    asset_repo = component "Asset Repository Port" "Persistence interface for the master catalog (FunctionalLocation, EquipmentUnit)." "IEquipmentRepository" "ComponentShape"
                    mtto_repo = component "Maintenance Repository Port" "Persistence interface for transactional entities (WorkOrder, FailureRecord)." "IWorkOrderRepository" "ComponentShape"
                    inv_repo = component "Inventory Repository Port" "Persistence interface for material control and safety inventories." "IInventoryRepository" "ComponentShape"
                    sec_repo = component "Audit Repository Port" "Persistence interface for user accounts, security roles, sessions, and AuditLog." "ISecurityRepository" "ComponentShape"
                    notify_port = component "Notification Port" "Synchronous broadcast of safety alerts and LOTO status to the outside." "INotificationPort" "ComponentShape"
                    telemetry_repo = component "Telemetry Repository Port" "Persistence interface for historical time-series data." "ITelemetryRepository" "ComponentShape"
                }
                group "Driven Adapters" {
                    telemetry_ef_adapter = component "Telemetry EF Adapter" "Unit of Work; optimized bulk-inserts into TimescaleDB." "TelemetryDbContext" "ComponentShape"
                    tax_ef_adapter = component "Taxonomy EF Adapter" "Unit of Work for Taxonomy domain schema." "TaxonomyDbContext" "ComponentShape"
                    mtto_ef_adapter = component "Maintenance EF Adapter" "Unit of Work for Maintenance domain schema." "MaintenanceDbContext" "ComponentShape"
                    inv_ef_adapter = component "Inventory EF Adapter" "Unit of Work for Inventory domain schema." "InventoryDbContext" "ComponentShape"
                    sec_ef_adapter = component "Security EF Adapter" "Unit of Work; persists AuditLog to append-only table." "SecurityDbContext" "ComponentShape"
                    signalr_broadcaster = component "SignalR Broadcaster" "Broadcasts data to SignalR channels filtering by authorized role." "IHubContext<T>" "ComponentShape"
                }
            }
        }

        # Relationships
        mobile_app -> api_controllers "Transmits offline mutation queue upon recovering network connection." "HTTPS / JSON"
        web_admin -> signalr_hub "Subscribes to real-time events for KPIs and LOTO status." "WSS (WebSockets)"
        telemetry_listener -> loto_port "Routes incoming IoT readings to evaluate Zero Energy thresholds." "In-Process Method Call"
        api_controllers -> tax_port "Invokes asset structure registration and graph validations." "In-Process Method Call"
        api_controllers -> mtto_port "Routes backlog admission and work order status transition requests." "In-Process Method Call"
        api_controllers -> inv_port "Routes warehouse transactions and physical asset rotation operations." "In-Process Method Call"
        api_controllers -> loto_port "Routes safety validations and physical lockout confirmations." "In-Process Method Call"
        api_controllers -> sec_port "Validates JWT token and RBAC matrix before processing requests." "In-Process Method Call"
        mtto_port -> rime_calc "Computes deterministic backlog priority scoring via Strategy pattern." "In-Process Method Call"
        tax_port -> asset_repo "Abstraction for taxonomy graph persistence operations." "C# Interface (DI)"
        mtto_port -> mtto_repo "Abstraction for work order and failure record persistence." "C# Interface (DI)"
        inv_port -> inv_repo "Abstraction for inventory transactions and stock levels." "C# Interface (DI)"
        sec_port -> sec_repo "Abstraction for identity management and chained hash audit logging." "C# Interface (DI)"
        loto_port -> notify_port "Abstraction for broadcasting critical safety alerts." "C# Interface (DI)"
        asset_repo -> tax_ef_adapter "Implements persistence via TaxonomyDbContext." "C# Class Inheritance"
        mtto_repo -> mtto_ef_adapter "Implements persistence via MaintenanceDbContext." "C# Class Inheritance"
        inv_repo -> inv_ef_adapter "Implements persistence via InventoryDbContext." "C# Class Inheritance"
        sec_repo -> sec_ef_adapter "Implements persistence via SecurityDbContext." "C# Class Inheritance"
        notify_port -> signalr_broadcaster "Implements broadcast via Microsoft.AspNetCore.SignalR." "C# Class Inheritance"
        tax_ef_adapter -> db_postgres "Executes transactional relational commands." "TCP/IP (SQL)"
        mtto_ef_adapter -> db_postgres "Executes transactional relational commands." "TCP/IP (SQL)"
        inv_ef_adapter -> db_postgres "Executes transactional relational commands." "TCP/IP (SQL)"
        sec_ef_adapter -> db_postgres "Executes transactional relational commands." "TCP/IP (SQL)"
        scada_node -> azure_iot "Transmits raw industrial telemetry to the cloud broker." "MQTT / AMQP"
        azure_iot -> telemetry_listener "Pushes high-frequency telemetry events to the backend consumer." "AMQP"
        mobile_app -> idempotency_filter "Sends sync payloads containing idempotency keys in headers." "HTTPS"
        idempotency_filter -> redis_cache "Queries and sets idempotency keys (SETNX) to prevent duplicate transactions." "TCP (RESP)"
        idempotency_filter -> idempotency_repo "Delegates durable logging (Stage 2) into the domain transaction." "In-Process Method Call"
        idempotency_repo -> db_postgres "Executes ACID transaction inserting the IdempotencyLog record." "TCP/IP (SQL)"
        mobile_app -> object_storage "Uploads binary failure evidence directly via Valet Key (pre-signed SAS token)." "HTTPS / REST"
        mtto_port -> media_repo "Requests SAS tokens for multimedia persistence." "In-Process Method Call"
        media_repo -> object_storage "Authenticates via Managed Identity to generate and issue SAS tokens." "HTTPS / Azure SDK"
        sync_worker -> mtto_port "Routes dequeued offline work orders to the maintenance domain." "In-Process Method Call"
        mtto_port -> event_bus "Publishes domain events (e.g., WorkOrderClosed) for cross-module orchestration." "In-Process Method Call"
        loto_port -> telemetry_bus "Subscribes to real-time safety condition streams." "In-Process Method Call"
        telemetry_listener -> telemetry_bus "Publishes live sensor readings to the hot path bus." "In-Process Method Call"
        telemetry_listener -> telemetry_repo "Dispatches historical sensor readings to the cold path." "C# Interface (DI)"
        telemetry_repo -> telemetry_ef_adapter "Implements time-series persistence via EF Core." "C# Class Inheritance"
        telemetry_ef_adapter -> db_postgres "Executes optimized bulk inserts into TimescaleDB chunks." "TCP/IP (SQL)"
        mobile_app -> local_db "Persists transactional queue and master data for offline-first execution." "SQLite P/Invoke"
        loto_watchdog -> local_db "Writes emergency lockout states directly to local storage upon connection loss." "SQLite P/Invoke"
        loto_watchdog -> signalr_hub "Maintains continuous heartbeat to verify safety perimeter integrity." "WSS (WebSockets)"
        web_admin -> api_controllers "Executes administrative commands and fetches master data." "HTTPS / JSON"
    }

    views {
        component appContainer "ComponentDiagram" {
            include *
            include mobile_app
            include web_admin
            include local_db
            include loto_watchdog
            include object_storage
            include db_postgres
            include azure_iot
            include redis_cache
            include scada_node
            autoLayout lr
        }
        styles {
            element "Database" {
                shape Cylinder
            }
            element "Mobile" {
                shape MobileDevicePortrait
            }
            element "WebBrowser" {
                shape WebBrowser
            }
            element "Broker" {
                shape Pipe
            }
            element "ComponentShape" {
                shape Component
            }
            element "Element" {
                metadata false
            }
        }
        theme default
    }
}