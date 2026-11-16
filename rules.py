
# IndiGo Agent Gatekeeper
# Permission and Authorization Rules

ENROLMENT_NUMBER = "65110"
COMPANY_NAME = "IndiGo Airlines"

BOOKING_LIMIT = 10000

RULES = {
    "R1": "Unknown AI agents are blocked.",
    "R2": "Revoked AI agents are always blocked.",
    "R3": "Registered agents can view flight fares.",
    "R4": "Bookings up to Rs. 10,000 are allowed.",
    "R5": "Bookings above Rs. 10,000 require customer approval.",
    "R6": "Changes to existing bookings require customer approval.",
    "R7": "Refund requests require customer approval.",
    "R8": "Unsupported actions are blocked."
}


def evaluate_request(customer, agent_name, action, amount, agent_status):
    """
    Evaluate an AI agent request and return
    ALLOW, ASK CUSTOMER or BLOCK with a rule number.
    """

    action = action.strip().lower().replace(" ", "_")
    amount = float(amount or 0)

    # Rule 1: Unknown agents are blocked
    if agent_status == "unknown":
        return {
            "decision": "BLOCK",
            "rule": "R1",
            "reason": "This AI agent is not registered."
        }

    # Rule 2: Revoked agents are blocked
    if agent_status == "revoked":
        return {
            "decision": "BLOCK",
            "rule": "R2",
            "reason": "This AI agent's permission has been revoked."
        }

    # Rule 3: Registered agents can view fares
    if action == "view_fares":
        return {
            "decision": "ALLOW",
            "rule": "R3",
            "reason": "Read-only flight fare viewing is permitted."
        }

    # Rule 4 and 5: Booking amount restrictions
    if action == "book":
        if amount <= 0:
            return {
                "decision": "BLOCK",
                "rule": "R8",
                "reason": "Booking amount must be greater than zero."
            }

        if amount <= BOOKING_LIMIT:
            return {
                "decision": "ALLOW",
                "rule": "R4",
                "reason": "Booking is within the permitted amount limit."
            }

        return {
            "decision": "ASK CUSTOMER",
            "rule": "R5",
            "reason": "Booking exceeds Rs. 10,000. Customer confirmation is required."
        }

    # Rule 6: Booking changes need approval
    if action == "change":
        return {
            "decision": "ASK CUSTOMER",
            "rule": "R6",
            "reason": "Customer approval is required to change a booking."
        }

    # Rule 7: Refunds need approval
    if action == "refund":
        return {
            "decision": "ASK CUSTOMER",
            "rule": "R7",
            "reason": "Customer approval is required for a refund."
        }

    # Rule 8: Unsupported actions are blocked
    return {
        "decision": "BLOCK",
        "rule": "R8",
        "reason": "This action is not supported by the Gatekeeper."
    }
