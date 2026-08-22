---
name: secure-api-review
description: Review an API for trust-boundary failures across authentication, object authorization, input and output handling, resource abuse, side effects, integrations, error behavior, and security regression coverage.
---
# Secure API Review

Use when reviewing a new or changed HTTP, GraphQL, RPC, webhook, streaming, or service API that accepts untrusted callers or data.

## Procedure
1. Inventory the exposed operations, callers, trust boundaries, sensitive data, privileged actions, side effects, and upstream/downstream systems touched by the API.
2. Verify authentication at the appropriate boundary and authorization for the specific action and resource. Check object identifiers, nested resources, batch operations, filters, exports, and tenant boundaries rather than reviewing only route-level roles.
3. Review input contracts for type, length, shape, allowed values, encoding, file/content handling, and fields callers are permitted to set. Reject unexpected privilege-bearing or server-owned fields rather than binding arbitrary input directly into domain objects.
4. Trace untrusted data into interpreters and sinks such as databases, templates, command execution, URLs, filesystem paths, parsers, deserializers, redirects, and downstream APIs. Ensure the consuming layer uses the correct safe parameterization or validation model for that sink.
5. Review outbound requests and webhook behavior for destination control, redirect handling, DNS/network boundaries, credential forwarding, timeout limits, and whether attacker-controlled URLs can reach internal or privileged resources.
6. Review response data for unnecessary sensitive fields, cross-tenant leakage, verbose internal errors, secrets, stack traces, authorization or existence side channels, and cache behavior that could expose personalized data.
7. Review state-changing operations for idempotency, replay, duplicate submission, concurrency, transaction boundaries, and safe retry behavior. Confirm partial failures cannot silently produce inconsistent privilege or financial/data state.
8. Review resource-abuse controls appropriate to the operation: request/body limits, pagination bounds, query complexity, upload limits, expensive filters, concurrency, rate controls, and bounded fan-out to downstream systems.
9. Review browser-facing APIs for cross-origin and ambient-credential behavior appropriate to the architecture. Do not use permissive cross-origin settings or CSRF assumptions without understanding which credentials the browser sends automatically.
10. Verify observability captures security-relevant events and request correlation without logging secrets or unnecessarily sensitive payloads.
11. Add negative security tests for unauthorized object access, malformed and boundary input, privilege-bearing fields, duplicate/replayed requests, cross-tenant attempts, dangerous external destinations, oversized/expensive requests, and error paths relevant to the API.

## Decision rules
- Validate for the sink and domain invariant, not from a generic list of forbidden characters.
- Authentication at an endpoint is not proof of object-level authorization.
- Input validation does not make dangerous interpreters safe when proper parameterization or isolation is available.
- Rate limiting is one abuse control, not a substitute for bounding the cost of individual operations.
- Security review should follow the actual protocol and trust model rather than forcing every API into REST-specific assumptions.

## Quality gate
The API review is complete when callers and protected resources are mapped, authn/authz hold at object and tenant boundaries, untrusted data is safe at every sensitive sink, side effects and resource costs are bounded, responses avoid sensitive leakage, and regression tests prove the material abuse cases.