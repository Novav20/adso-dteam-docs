---
id: MTTO-023
nombre: "Usage or Telemetry-Based Preventive Maintenance Scheduling"
priority: MUST
points: 8
role: Maintenance Planner
epic: MTTO
observations: This story enables predictive/preventive maintenance based on the actual usage of the equipment unit. It consumes usage counter data (hour meters, cycles, gallons) that can be updated manually or through data ingestion from the auxiliary SCADA/IoT system.
applicable_trs:
  - "[[TR-005]]"
  - "[[TR-006]]"
  - "[[TR-008]]"
  - "[[TR-010]]"
---

# MTTO-023: Usage or Telemetry-Based Preventive Maintenance Scheduling

## Story Description

| Role | Action | Benefit |
|---|---|---|
| Maintenance Planner | I want to schedule preventive work orders based on accumulated usage limits (hour meters or cycle counters) linked to the equipment unit's telemetry. | So that I can guarantee that critical equipment receives maintenance according to its actual wear and not just elapsed calendar time. |

## Acceptance Criteria
| Scenario | Given (Context) | When (Action) | Then (Result) |
|---|---|---|---|
| Usage-based plan creation | Given the Planner is authenticated and the equipment unit has a configured usage sensor. | When they define a preventive plan setting an activation threshold (e.g., every 1000 operating hours). | Then the system saves the plan and displays the current counter value alongside the target activation value. |
| Work order generation via telemetry | Given an active preventive plan is configured to trigger at 5000 operating hours. | When the Plant SCADA/IoT transmits a reading that meets or exceeds the threshold. | Then the system automatically generates the preventive Work Order and updates the target for the next intervention. |
| Inconsistent reading alert | Given the system receives real-time telemetry readings. | When a usage reading lower than the historical accumulated value is received (counter decrement). | Then the system rejects the reading, generates a data inconsistency alert, and maintains the counter at its last valid value. |

## Functional Requirements (FR)
| ID | Description | ISO 25010 Category | Priority | Source |
|---|---|---|---|---|
| FR-583 | The system shall allow the configuration of preventive plans associated with cumulative usage variables (e.g., hour meters, cycle counters, processed volume). | Functional Suitability | High | ISO 14224:2016, Annex E — Usage Metrics |
| FR-584 | The system shall provide an API interface (REST endpoint) to receive external counter readings originating from SCADA systems or IoT devices. | Functional Suitability | High | RESTful API Design Patterns |
| FR-585 | The system shall calculate the cumulative usage value and automatically trigger the creation of a Work Order when telemetry reaches or exceeds the configured threshold. | Functional Suitability | High | Reliability-Centered Maintenance (RCM) Principles |
| FR-586 | The system shall block the processing of usage readings presenting values lower than the historical cumulative of the Equipment Unit to prevent misadjustments due to incorrect resets. | Functional Suitability | High | Data Validation Best Practices (Monotonicity Checks) |
| FR-587 | The Planner may manually record counter readings from the Equipment Unit's technical record as a fallback mechanism against telemetry failures. | Functional Suitability | Medium | Graceful Degradation Patterns |
| FR-590 | The system shall maintain the precision of cumulative counters using high-precision data types to prevent rounding errors in massive operations. | Functional Suitability | High | IEEE 754 (Floating-Point Arithmetic) |

## Non-Functional Requirements (NFR)
| ID | Description | ISO 25010 Category | Priority | Source |
|---|---|---|---|---|
| NFR-588 | The processing of the telemetry frame and the evaluation of Work Order trigger rules must not exceed 3 seconds from ingestion. | Performance Efficiency | High | ISO/IEC 25010:2023 — Performance Efficiency (Time behavior) |
| NFR-589 | The IoT data reception channel must implement authentication and TLS 1.3 encryption to prevent the injection of malicious telemetry data. | Security | High | NIST SP 800-52 (TLS 1.3 Guidelines) / OWASP IoT Top 10 |

## Source
- Automatically generated from `user-stories.csv`, `gherkin.csv` and `srs.csv`.
