import json
import sys
sys.path.insert(0, ".")

from src.app.schemas import TicketRequest, CustomerTier
from src.app.service import process_ticket


def run_evals():
    with open("evals/tickets.jsonl") as f:
        tickets = [json.loads(line) for line in f]

    results = []
    action_correct = 0
    category_correct = 0
    policy_failures = 0

    print(f"Running {len(tickets)} tickets...\n")

    for t in tickets:
        request = TicketRequest(
            ticket_id=t["ticket_id"],
            customer_tier=CustomerTier(t["customer_tier"]),
            subject=t["subject"],
            message=t["message"]
        )

        response = process_ticket(request)

        action_match = response.action.value == t["expected_action"]
        category_match = response.category.value == t["expected_category"]

        # Policy compliance check
        policy_fail = False
        if t["expected_action"] == "escalate" and t["expected_category"] == "auth":
            if response.action.value != "escalate":
                policy_fail = True
                policy_failures += 1

        if action_match:
            action_correct += 1
        if category_match:
            category_correct += 1

        results.append({
            "ticket_id": t["ticket_id"],
            "action_correct": action_match,
            "category_correct": category_match,
            "policy_fail": policy_fail,
            "expected_action": t["expected_action"],
            "got_action": response.action.value,
            "expected_category": t["expected_category"],
            "got_category": response.category.value,
        })

        status = "PASS" if action_match else "FAIL"
        print(f"{status} {t['ticket_id']} | action: {t['expected_action']} -> {response.action.value} | category: {t['expected_category']} -> {response.category.value}")

    total = len(tickets)
    print(f"\nResults:")
    print(f"Action accuracy:   {action_correct}/{total} ({round(action_correct/total*100)}%)")
    print(f"Category accuracy: {category_correct}/{total} ({round(category_correct/total*100)}%)")
    print(f"Policy failures:   {policy_failures} (must be 0)")

    with open("evals/results.json", "w") as f:
        json.dump({
            "total": total,
            "action_accuracy": round(action_correct/total, 3),
            "category_accuracy": round(category_correct/total, 3),
            "policy_failures": policy_failures,
            "details": results
        }, f, indent=2)

    print(f"\nFull results saved to evals/results.json")


if __name__ == "__main__":
    run_evals()