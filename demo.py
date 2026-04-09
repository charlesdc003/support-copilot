import streamlit as st
from src.app.schemas import TicketRequest, CustomerTier
from src.app.service import process_ticket

st.set_page_config(page_title="Support Copilot", layout="centered")

st.title("Support Copilot")
st.caption("AI-powered ticket triage with policy engine. Built with FastAPI, pgvector, and Ollama.")

with st.form("ticket_form"):
    ticket_id = st.text_input("Ticket ID", value="demo-001")
    customer_tier = st.selectbox("Customer Tier", ["free", "pro", "enterprise"])
    subject = st.text_input("Subject", placeholder="Brief description of the issue")
    message = st.text_area("Message", placeholder="Full description of the issue...", height=150)
    submitted = st.form_submit_button("Analyze Ticket")

if submitted:
    if not subject or not message:
        st.error("Subject and message are required.")
    else:
        with st.spinner("Analyzing..."):
            try:
                request = TicketRequest(
                    ticket_id=ticket_id,
                    customer_tier=CustomerTier(customer_tier),
                    subject=subject,
                    message=message
                )
                result = process_ticket(request)

                action_colors = {
                    "escalate": "red",
                    "auto_reply": "green",
                    "needs_info": "orange"
                }
                color = action_colors.get(result.action.value, "gray")

                st.markdown(f"### :{color}[{result.action.value.upper().replace('_', ' ')}]")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Confidence", f"{round(result.confidence * 100)}%")
                with col2:
                    st.metric("Category", result.category.value.replace("_", " ").title())

                st.markdown("**Draft Reply**")
                st.info(result.draft_reply)

                st.markdown("**Justification**")
                st.caption(result.justification)

            except Exception as e:
                st.error(f"Error: {e}")

st.divider()
st.caption("Policy engine: auth tickets always escalate. Enterprise bugs always escalate. Confidence below 0.4 routes to needs_info.")