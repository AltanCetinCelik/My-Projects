# Architecture

This is a public-safe demo architecture, not the full production architecture.

```text
+----------------------+       +----------------------+       +------------------+
| Synthetic machine    |       | Edge Gateway Demo    |       | FastAPI Backend  |
| data / STM32-style   +------>+ UART/CAN parser      +------>+ API + rule engine|
| bridge frames        | HTTP  | sanitized converter  | HTTP  | in-memory state  |
+----------------------+       +----------------------+       +---------+--------+
                                                                         |
                                                                         v
                                                              +------------------+
                                                              | Browser Dashboard|
                                                              | machine cards    |
                                                              | alarms           |
                                                              +------------------+
```

## Why this is safe for public GitHub

- Data is synthetic.
- CAN payload mapping is fake and generic.
- Health scoring is a simple demo rule engine.
- No secrets are included.
- No production ML model is included.
- No real customer/factory data is included.
- No private MACİT Cloud business logic is included.

## Production gaps intentionally omitted

A production industrial system would need authentication, authorization, database persistence, audit logs, signed device identity, broker hardening, fail-safe behavior, watchdog processes, real machine protocol documentation, deployment scripts, monitoring and backups.
