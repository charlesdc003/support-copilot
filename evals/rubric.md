# Evaluation Rubric

## What we're measuring
For each ticket, we check three things:
1. **Action** — did the system choose the right action (auto_reply, escalate, needs_info)?
2. **Category** — did the system classify the ticket correctly (billing, auth, bug, feature_request, general)?
3. **Policy compliance** — did the policy engine override the LLM when it should have?

## Scoring

### Action (primary metric)
- Correct: 1 point
- Wrong but understandable: 0.5 points
- Wrong and clearly incorrect: 0 points

### Category (secondary metric)
- Correct: 1 point
- Wrong: 0 points

### Policy compliance (binary)
- Auth tickets must always be escalate — any other action is a failure
- Enterprise bug tickets must always be escalate — any other action is a failure

## What good looks like
- Action accuracy above 80% on the full dataset
- Policy compliance 100% — no exceptions
- Category accuracy above 70%

## Known failure modes
- Small local model (llama3.2) sometimes returns general instead of the correct category
- Low confidence tickets correctly route to needs_info even when action would be correct
- Draft replies are sometimes generic — acceptable for this version