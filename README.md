# ✈️ IndiGo Agent Gatekeeper

### AI Agent Permission, Booking Authorization and Customer Trust Management System

**Company:** IndiGo Airlines  

---

## 1. Project Overview

IndiGo Agent Gatekeeper is a Python-based prototype designed to manage permissions granted to personal AI agents acting on behalf of airline customers.

As customers increasingly use AI agents to perform activities such as searching flight fares and making bookings, companies need a system to verify agent permissions and protect customers from unauthorized actions.

This project acts as a permission-checking layer between customers, AI agents and airline services.

## 2. Problem Statement

Personal AI agents may perform actions such as booking flights, changing reservations and requesting refunds on behalf of customers.

Without proper authorization and monitoring, these actions can create risks related to customer consent, financial transactions and accountability.

The proposed Gatekeeper evaluates each request before allowing an AI agent to proceed.

## 3. Project Objectives

- Register and manage customer AI agents.
- Verify whether an AI agent is authorized.
- Control booking permissions based on transaction limits.
- Require customer approval for sensitive activities.
- Revoke AI agent permissions when necessary.
- Maintain an audit log of permission decisions.
- Improve customer trust, security and accountability.

## 4. Key Features

- **Agent Registration:** Register customer AI agents.
- **Permission Verification:** Check agent status before processing requests.
- **Booking Authorization:** Evaluate booking amounts against the permitted limit.
- **Customer Approval:** Flag sensitive transactions for customer confirmation.
- **Agent Revocation:** Revoke permissions and block future requests.
- **Audit Log:** Maintain records of requests, decisions and reasons.
- **Dashboard:** Display system statistics and agent activity.

## 5. Permission Rules

| Rule | Condition | Decision |
|---|---|---|
| R1 | Unknown or unregistered agent | BLOCK |
| R2 | Revoked agent | BLOCK |
| R3 | Viewing flight fares | ALLOW |
| R4 | Booking within ₹10,000 | ALLOW |
| R5 | Booking above ₹10,000 | ASK CUSTOMER |
| R6 | Changing an existing booking | ASK CUSTOMER |
| R7 | Requesting a refund | ASK CUSTOMER |
| R8 | Unsupported action | BLOCK |

## 6. Technology Stack

- Python
- Streamlit
- JSON for agent records
- CSV for audit logging
- GitHub for version control and project hosting

## 7. Project Structure

```text
IndiGo-Agent-Gatekeeper/
│
├── app.py
├── gatekeeper.py
├── rules.py
├── agents.json
├── audit_log.csv
├── requirements.txt
├── PROMPTS.md
└── README.md
```

## 9. Testing

The prototype was evaluated using scenarios involving:

1. Registered agent viewing flight fares.
2. Unregistered agent attempting a booking.
3. Booking within the permitted amount.
4. Booking exceeding the permitted amount.
5. Revoked agent attempting a new booking.
6. Booking change requiring customer approval.
7. Refund requiring customer approval.
8. Unsupported cancellation action.

The application displays the corresponding permission decision and reason.

## 10. Business Value

The IndiGo Agent Gatekeeper prototype demonstrates how airlines can introduce an authorization layer for AI-powered customer interactions.

Its potential business benefits include:

- Reduced risk of unauthorized bookings.
- Better customer control over AI agents.
- Improved transaction accountability.
- Greater transparency through audit records.
- Increased customer confidence in AI-assisted services.

## 11. Important Note

This is an academic prototype developed for demonstration and educational purposes. It simulates permission decisions only. No real flight booking, payment, refund or cancellation is executed.


**GitHub Repository:**  
https://github.com/diwanshi2003/IndiGo-Agent-Gatekeeper
