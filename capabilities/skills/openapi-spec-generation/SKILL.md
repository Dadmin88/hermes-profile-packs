---
name: openapi-spec-generation
description: Generate and maintain OpenAPI 3.1 specifications from code, design-first specs, and validation patterns. Use when creating API documentation, generating SDKs, or ensuring API contract compliance.
version: 1.0.0
author: Seth Hobson
license: MIT
---

# OpenAPI Spec Generation

Comprehensive patterns for creating, maintaining, and validating OpenAPI 3.1 specifications for RESTful APIs.

## When to Use This Skill

- Creating API documentation from scratch
- Generating OpenAPI specs from existing code
- Designing API contracts (design-first approach)
- Validating API implementations against specs
- Generating client SDKs from specs
- Setting up API documentation portals

## Core Concepts

### 1. OpenAPI 3.1 Structure

```yaml
openapi: 3.1.0
info:
  title: API Title
  version: 1.0.0
servers:
  - url: https://api.example.com/v1
paths:
  /resources:
    get: ...
components:
  schemas: ...
  securitySchemes: ...
```

### 2. Design Approaches

| Approach         | Description                  | Best For            |
| ---------------- | ---------------------------- | ------------------- |
| **Design-First** | Write spec before code       | New APIs, contracts |
| **Code-First**   | Generate spec from code      | Existing APIs       |
| **Hybrid**       | Annotate code, generate spec | Evolving APIs       |

## Templates and detailed worked examples

Full template library and detailed worked examples live in `references/details.md`. Read that file when you need the concrete templates.

## Best Practices

### Do's

- **Use $ref** - Reuse schemas, parameters, responses
- **Add examples** - Real-world values help consumers
- **Document errors** - All possible error codes
- **Version your API** - In URL or header
- **Use semantic versioning** - For spec changes

### Don'ts

- **Don't use generic descriptions** - Be specific
- **Don't skip security** - Define all schemes
- **Model null explicitly** - In OpenAPI 3.1, use a JSON Schema union such as `type: [string, "null"]`
- **Don't mix styles** - Consistent naming throughout
- **Don't hardcode URLs** - Use server variables


## Verify the client and server contract

1. Follow the project's existing source of truth and OpenAPI version. Use [worked examples](references/details.md) and [code-first patterns](references/code-first-and-tooling.md) only where they fit the stack.
2. Check request validation, success and error bodies, authentication and authorization, pagination, and any behavior older clients depend on. Examples must use synthetic data.
3. Run the project's pinned linter or use an installed Redocly CLI for a local spec with local references and a reviewed config. Review custom rules, preprocessors and plugins as project code. For a standalone file, `REDOCLY_TELEMETRY=off redocly lint openapi.yaml` is a local check.
4. Compare at least one success and one relevant failure against the actual dev API and its consuming client. Schema lint alone does not exercise the implementation. Regenerate a client only when the repository already uses that workflow or the assignment calls for it.
