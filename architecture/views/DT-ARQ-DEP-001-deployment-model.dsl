workspace "System Deployment Model" {
    model {
        sys = softwareSystem "System Software" {
            mobile_app = container "Frontend App" "Field touch execution and offline synchronization (TR-002, TR-007)." ".NET MAUI Blazor Hybrid" "Mobile"
            loto_watchdog = container "LOTO Watchdog" "Continuous safety heartbeat monitoring (TR-010)." "Background Thread (C#)" "ComponentShape"
            local_db = container "Local DB" "Local encrypted offline persistence on mobile device." "SQLite (sqlite-net-pcl)" "Database"
            scada_engine = container "Sensor Emulator" "Instrumentation gateway; emulates and transmits sensor readings via MQTT." "SCADA Engine (C# / Python)" "ComponentShape"
            admin_portal = container "Web Admin Portal" "Web administrative interface for HSEQ supervision, WOs, and KPI dashboards." "Blazor Web App" "WebBrowser"
            iot_hub = container "Azure IoT Hub" "Managed broker for asynchronous high-frequency telemetry ingestion." "Azure IoT Hub Service" "Broker"
            nginx_proxy = container "Nginx Reverse Proxy" "TLS 1.3 termination, reverse routing, and static web delivery." "Nginx (Alpine Linux)" "ComponentShape"
            backend_api = container "Backend API Monolith" "Modular monolith with DDD business logic and domain services." ".NET 10 Web API Monolith" "ComponentShape"
            postgres_db = container "PostgreSQL Master" "Relational master store, immutable audit (ADR-003), and time series." "PostgreSQL 18 + TimescaleDB" "Database"
            redis_cache = container "Redis Cache" "Distributed in-memory datastore for idempotency caching keys (ADR-007)." "Redis 7.x" "Database"
        }

        # Relationships
        mobile_app -> local_db "Local offline transactional read and write (TR-002, TR-007)." "Direct IPC (Local File) - AES-256"
        loto_watchdog -> local_db "Write of Fail-Safe Preventive Security Lockout status." "Direct IPC (Local File) - AES-256"
        mobile_app -> nginx_proxy "REST API synchronization transactions (local queues, JSON data)." "HTTPS (Port 443) - TLS 1.3 / AES-256"
        loto_watchdog -> nginx_proxy "Persistent safety Heartbeat channel (ping every 2s) for LOTO (TR-010)." "WSS (Port 443) - WebSockets TLS 1.3"
        scada_engine -> iot_hub "Continuous publication of real process telemetry from the plant." "MQTT (Port 8883) - TLS 1.3"
        iot_hub -> backend_api "Asynchronous and reliable consumption of queued industrial telemetry." "AMQP (Port 5671) - TLS 1.3"
        admin_portal -> nginx_proxy "Download of Blazor/.NET static resources and JSON API requests." "HTTPS (Port 443) - TLS 1.3"
        admin_portal -> nginx_proxy "Real-time channel for telemetry updates and KPI Dashboard." "WSS (Port 443) - WebSockets TLS 1.3"
        nginx_proxy -> backend_api "Internal routing of API requests and terminated WebSocket traffic." "HTTP (Docker Net) - Isolated Internal Net"
        backend_api -> postgres_db "Persistence operations via EF Core under Unit of Work pattern." "TCP/IP (Port 5432) - SSL / Private Net"
        backend_api -> redis_cache "Millisecond-latency idempotency key validation (SETNX) to prevent duplicate transactions." "TCP (RESP) (Port 6379) - TLS / Private Net"

        # Deployment Environment
        production = deploymentEnvironment "Production" {
            mobile_node = deploymentNode "Mobile Device" "" "Edge Node (Android / iOS Device)" {
                mobile_app_inst = containerInstance mobile_app
                loto_watchdog_inst = containerInstance loto_watchdog
                local_db_inst = containerInstance local_db
            }
            scada_node = deploymentNode "Local Control Station" "" "Edge Gateway (Industrial PC / SCADA)" {
                scada_engine_inst = containerInstance scada_engine
            }
            workstation_node = deploymentNode "Workstation" "" "Client Node (Desktop PC / Web Browser)" {
                admin_portal_inst = containerInstance admin_portal
            }
            azure_cloud = deploymentNode "Azure Cloud Platform" "" "Managed Cloud Service (Azure Tenant)" {
                iot_hub_inst = containerInstance iot_hub
            }
            cloud_host = deploymentNode "Cloud Host Server" "" "Execution Environment (Linux VPS)" {
                docker_engine = deploymentNode "Docker Engine" "" "Docker Runtime" {
                    nginx_proxy_inst = containerInstance nginx_proxy
                    backend_api_inst = containerInstance backend_api
                }
            }
            db_server = deploymentNode "Database Server" "" "Database Node (Managed DB / Container)" {
                postgres_db_inst = containerInstance postgres_db
            }
            cache_server = deploymentNode "Cache Server" "" "In-Memory Node" {
                redis_cache_inst = containerInstance redis_cache
            }
        }
    }

    views {
        deployment sys "Production" "DeploymentDiagram" {
            include *
            autoLayout tb
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