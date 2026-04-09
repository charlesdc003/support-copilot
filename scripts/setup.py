import sys
sys.path.insert(0, ".")

from src.app.retrieval import setup_database, ingest

def seed_knowledge_base():
    print("Setting up database...")
    setup_database()

    print("Ingesting knowledge base...")

    ingest(
        "Enterprise customers experiencing authentication failures must be escalated immediately to the on-call engineering team. Never attempt to resolve enterprise auth outages through standard support channels. Response time SLA is 15 minutes.",
        {"source": "policy", "category": "auth", "tier": "enterprise"}
    )

    ingest(
        "Pro and Free tier authentication issues should be directed to the self-service password reset flow at reset.example.com. If the issue persists after reset, escalate to tier 2 support.",
        {"source": "policy", "category": "auth", "tier": "pro_free"}
    )

    ingest(
        "Billing disputes for Enterprise customers must be reviewed by the account management team within 4 hours. Do not issue refunds without account manager approval.",
        {"source": "policy", "category": "billing", "tier": "enterprise"}
    )

    ingest(
        "Refunds up to $50 for Pro tier customers can be approved without manager sign-off. Refunds above $50 require manager approval. Process refunds through the billing portal.",
        {"source": "policy", "category": "billing", "tier": "pro"}
    )

    ingest(
        "Free tier customers are not eligible for refunds. Direct them to the upgrade page if they are dissatisfied with service limitations.",
        {"source": "policy", "category": "billing", "tier": "free"}
    )

    ingest(
        "Feature requests should be logged in the product feedback portal at feedback.example.com. Acknowledge the request and thank the customer. Do not make promises about roadmap timelines.",
        {"source": "policy", "category": "feature_request"}
    )

    ingest(
        "Bug reports should include steps to reproduce, expected behavior, and actual behavior. Ask the customer for this information if not provided. Escalate confirmed bugs affecting multiple users immediately.",
        {"source": "policy", "category": "bug"}
    )

    print("Knowledge base ready. Documents ingested.")

if __name__ == "__main__":
    seed_knowledge_base()