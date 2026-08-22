---
name: networking
description: Design, change, or diagnose infrastructure networking from explicit traffic flows through naming, routing, filtering, encryption, discovery, load balancing, and path validation.
---
# Networking

Use when services or nodes must communicate reliably and securely across local, private, public, container, overlay, or cloud networks.

## Procedure
1. Write the required traffic flows first: source identity/network, destination, protocol, ports, direction, expected name, encryption requirement, and whether the connection is long-lived, bidirectional, or latency-sensitive.
2. Trace each flow through name resolution, routing, gateways/NAT, firewalls or security groups, proxies/load balancers, overlay or tunnel boundaries, and the destination listener.
3. Define address and naming ownership. Avoid hardcoding addresses where stable discovery or names are the intended contract, and understand TTL/cache behavior when names can move.
4. Apply least-access filtering at meaningful boundaries without creating hidden duplicate policy layers that operators cannot reason about.
5. Define TLS or other transport security at the correct endpoints, including certificate identity, trust roots, renewal, and where plaintext is permitted if anywhere.
6. Account for failure and protocol details relevant to the path: timeouts, connection reuse, keepalive, retries, MTU/fragmentation, IPv4/IPv6 behavior, proxy headers, source-address preservation, and asymmetric routing when applicable.
7. For load-balanced or discovered services, define health checks, drain behavior, connection stickiness only when required, and what happens when membership changes.
8. Validate from both ends using the actual name/protocol and representative path. Inspect DNS, route, listener, handshake, filtering, and packet/connection evidence at the narrowest useful layer.
9. Record the resulting flow and policy so future operators can distinguish intended exposure from accidental reachability.

## Decision rules
- Start from required communication, not from opening ports until something works.
- A successful ping does not prove the application path, and a failed ping does not prove the application path is unavailable.
- Prefer stable identity and discovery contracts over machine-specific addresses when orchestration can move workloads.
- Network policy and application authorization are separate controls; one does not replace the other.

## Quality gate
Networking is ready when required flows work through the intended names and security boundaries, unnecessary exposure is absent, failure and membership behavior are understood, and another operator can trace the path without reverse-engineering undocumented rules.