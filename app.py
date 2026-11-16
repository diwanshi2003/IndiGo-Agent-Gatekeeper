
import streamlit as st
import pandas as pd
import json

from pathlib import Path
from rules import ENROLMENT_NUMBER, COMPANY_NAME, BOOKING_LIMIT
from gatekeeper import (
    register_agent,
    revoke_agent,
    process_request,
    load_agents,
    AUDIT_FILE
)

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="IndiGo Agent Gatekeeper",
    page_icon="✈️",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
.main {
    background-color: #f5f8fc;
}
.title {
    color: #003b71;
    font-size: 32px;
    font-weight: 800;
}
.subtitle {
    color: #53677d;
    font-size: 15px;
}
div[data-testid="stMetric"] {
    background: white;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #dce5ef;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown(
    '<div class="title">✈️ IndiGo Agent Gatekeeper</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI Agent Permission, Booking Authorization '
    'and Customer Trust Management System'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    f"Company: {COMPANY_NAME} | "
    f"Enrolment Number: {ENROLMENT_NUMBER} | "
    f"Booking Limit: ₹{BOOKING_LIMIT:,}"
)

# ---------------- DASHBOARD DATA ----------------

agents = load_agents()

total_agents = len(agents)
active_agents = sum(
    1 for a in agents.values()
    if a.get("status") == "active"
)
revoked_agents = sum(
    1 for a in agents.values()
    if a.get("status") == "revoked"
)

audit_df = pd.DataFrame()

if Path(AUDIT_FILE).exists():
    try:
        audit_df = pd.read_csv(AUDIT_FILE)
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        audit_df = pd.DataFrame()

total_requests = len(audit_df)

# ---------------- METRICS ----------------

st.subheader("System Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Agents", total_agents)
c2.metric("Active Agents", active_agents)
c3.metric("Revoked Agents", revoked_agents)
c4.metric("Total Requests", total_requests)

st.divider()

# ---------------- NAVIGATION ----------------

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Dashboard",
    "➕ Register Agent",
    "🚫 Revoke Agent",
    "🔐 Check Permission",
    "📋 Audit Log"
])

# ---------------- TAB 1: DASHBOARD ----------------

with tab1:

    st.subheader("Welcome to the IndiGo Gatekeeper")

    st.write(
        "This system evaluates requests made by personal AI "
        "agents on behalf of airline customers."
    )

    st.markdown("### Decision Categories")

    a, b, c = st.columns(3)

    a.success("ALLOW\n\nThe requested action is permitted.")
    b.warning("ASK CUSTOMER\n\nCustomer confirmation is required.")
    c.error("BLOCK\n\nThe requested action is prohibited.")

    st.markdown("### Permission Rules")

    rules = {
        "R1": "Unknown agents are blocked.",
        "R2": "Revoked agents are always blocked.",
        "R3": "Registered agents can view flight fares.",
        "R4": "Bookings up to ₹10,000 are allowed.",
        "R5": "Bookings above ₹10,000 require customer approval.",
        "R6": "Booking changes require customer approval.",
        "R7": "Refund requests require customer approval.",
        "R8": "Unsupported actions are blocked."
    }

    for number, description in rules.items():
        st.write(f"**{number}:** {description}")

# ---------------- TAB 2: REGISTER AGENT ----------------

with tab2:

    st.subheader("Register a Customer AI Agent")

    with st.form("register_form"):

        customer = st.text_input(
            "Customer Name",
            placeholder="Enter customer name"
        )

        agent_name = st.text_input(
            "AI Agent Name",
            placeholder="Example: TravelBot"
        )

        submitted = st.form_submit_button(
            "Register AI Agent",
            use_container_width=True
        )

        if submitted:

            if not customer.strip() or not agent_name.strip():
                st.error("Please fill in both fields.")

            else:
                result = register_agent(customer, agent_name)

                if result["success"]:
                    st.success(result["message"])
                    st.json(result["agent"])

                else:
                    st.warning(result["message"])

# ---------------- TAB 3: REVOKE AGENT ----------------

with tab3:

    st.subheader("Revoke AI Agent Permission")

    agents = load_agents()

    active_names = [
        a["agent_name"]
        for a in agents.values()
        if a.get("status") == "active"
    ]

    if active_names:

        selected_agent = st.selectbox(
            "Select AI Agent",
            active_names
        )

        st.warning(
            "Revoking an agent will prevent it from "
            "performing further actions."
        )

        if st.button("Revoke Agent Permission", type="primary"):

            result = revoke_agent(selected_agent)

            if result["success"]:
                st.success(result["message"])
                st.write(
                    "Revocation timestamp:",
                    result["revoked_at"]
                )
                st.rerun()

            else:
                st.error(result["message"])

    else:
        st.info("No active AI agents available.")

# ---------------- TAB 4: CHECK PERMISSION ----------------

with tab4:

    st.subheader("Evaluate an AI Agent Request")

    with st.form("request_form"):

        customer = st.text_input(
            "Customer Name",
            key="request_customer"
        )

        agent_name = st.text_input(
            "AI Agent Name",
            placeholder="Enter registered or unknown agent",
            key="request_agent"
        )

        action = st.selectbox(
            "Select Requested Action",
            [
                "view_fares",
                "book",
                "change",
                "refund",
                "cancel",
                "other"
            ]
        )

        amount = st.number_input(
            "Booking / Transaction Amount (₹)",
            min_value=0.0,
            value=0.0,
            step=500.0
        )

        check = st.form_submit_button(
            "Check Permission",
            use_container_width=True
        )

        if check:

            if not customer.strip() or not agent_name.strip():
                st.error("Enter customer and agent details.")

            else:

                result = process_request(
                    customer=customer,
                    agent_name=agent_name,
                    action=action,
                    amount=amount
                )

                st.markdown("### Gatekeeper Decision")

                if result["decision"] == "ALLOW":
                    st.success("✅ ALLOW")

                elif result["decision"] == "ASK CUSTOMER":
                    st.warning("⚠️ ASK CUSTOMER")

                else:
                    st.error("🚫 BLOCK")

                st.write("**Rule Number:**", result["rule"])
                st.write("**Reason:**", result["reason"])

                st.caption(
                    "This is a simulated permission decision. "
                    "No real booking or payment is executed."
                )

# ---------------- TAB 5: AUDIT LOG ----------------

with tab5:

    st.subheader("System Audit History")

    if Path(AUDIT_FILE).exists():

        try:
            log_df = pd.read_csv(AUDIT_FILE)

            if not log_df.empty:

                st.dataframe(
                    log_df,
                    use_container_width=True,
                    hide_index=True
                )

                st.download_button(
                    "Download Audit Log CSV",
                    data=log_df.to_csv(index=False),
                    file_name="indigo_audit_log.csv",
                    mime="text/csv"
                )

            else:
                st.info("No activity recorded yet.")

        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            st.info("Audit log is currently empty.")

    else:
        st.info("Audit log has not been created yet.")

# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "IndiGo Agent Gatekeeper | Academic Prototype | "
    "Enrolment No: 65110 | Not affiliated with IndiGo Airlines."
)
