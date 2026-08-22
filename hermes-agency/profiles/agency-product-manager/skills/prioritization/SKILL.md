---
name: prioritization
description: Prioritize competing product work using explicit outcomes, evidence, urgency, confidence, effort and opportunity cost without treating scoring frameworks as objective truth.
---
# Prioritization

Use when deciding what product work should be done first, deferred, reduced, researched, or rejected under limited time and capacity.

## Procedure
1. Define the decision horizon and objective before ranking items. A priority list for today's incident response is not the same decision as a quarterly product portfolio.
2. Normalize each candidate into the problem or outcome it addresses, affected users/customers, evidence, expected value, urgency or deadline, confidence, dependencies, risk, and rough cost or capacity demand.
3. Separate non-negotiable constraints from discretionary prioritization. Safety/security fixes, contractual commitments, regulatory obligations, critical incidents, or hard external deadlines may constrain the choice before scoring begins.
4. Compare candidates on criteria that actually matter for this product. Useful dimensions can include reach, severity, user value, strategic value, revenue/cost impact, learning value, confidence, reversibility, effort, technical risk, and opportunity cost.
5. Use RICE, impact/effort, weighted scoring, cost of delay, or another framework only when it clarifies the decision. Make inputs and assumptions visible; do not convert weak estimates into false precision merely by multiplying them.
6. Account for dependencies and enabling work. A lower-value item may deserve earlier sequencing when it unlocks several higher-value outcomes, while a high-scoring item may remain premature if a critical assumption is untested.
7. Distinguish execution from discovery. When value or feasibility confidence is too low for a large commitment, prioritize a bounded research, prototype, or validation step instead of pretending uncertainty can be scored away.
8. Review the proposed order against capacity and work already in progress. Frequent priority churn has a real switching cost; change committed work when the new evidence or urgency justifies that cost.
9. Record the chosen order with concise rationale, important assumptions, deferred/rejected items, and the evidence or event that should trigger re-prioritization.

## Decision rules
- Framework scores support judgment; they do not replace it.
- The loudest request is evidence of urgency for someone, not automatic evidence of broad value.
- Effort estimates should come from the people capable of assessing the implementation, not be invented by Product Manager.
- Prioritize outcomes and learning, not backlog age or feature count.
- Explicitly say no or not now when work does not justify its opportunity cost.

## Quality gate
Prioritization is ready when candidates are compared against an explicit objective and real constraints, evidence and uncertainty are visible, dependencies and capacity are accounted for, any scoring method is interpretable rather than magical, and the final order has a rationale strong enough to explain both what is being done and what is not.