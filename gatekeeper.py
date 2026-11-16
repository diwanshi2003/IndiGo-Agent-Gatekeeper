
# IndiGo Agent Gatekeeper
# Agent Registration, Revocation and Audit Logging

import json
import csv
from pathlib import Path
from datetime import datetime

from rules import evaluate_request


BASE_DIR = Path(__file__).resolve().parent
AGENTS_FILE = BASE_DIR / "agents.json"
AUDIT_FILE = BASE_DIR / "audit_log.csv"


def current_time():
    """Return local date and time with timezone."""
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load_agents():
    """Load all registered agents."""

    if not AGENTS_FILE.exists():
        return {}

    try:
        with open(AGENTS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def save_agents(agents):
    """Save agent records to JSON."""

    with open(AGENTS_FILE, "w", encoding="utf-8") as file:
        json.dump(agents, file, indent=4)


def initialize_audit_log():
    """Create audit CSV with column headings."""

    headers = [
        "timestamp",
        "customer",
        "agent_name",
        "action",
        "amount",
        "decision",
        "rule",
        "reason"
    ]

    if not AUDIT_FILE.exists() or AUDIT_FILE.stat().st_size == 0:
        with open(AUDIT_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)


def register_agent(customer, agent_name):
    """Register a new AI agent for a customer."""

    agents = load_agents()
    agent_id = agent_name.strip().lower()

    if not customer.strip() or not agent_id:
        return {
            "success": False,
            "message": "Customer and agent name are required."
        }

    if agent_id in agents and agents[agent_id]["status"] == "active":
        return {
            "success": False,
            "message": "This agent is already registered."
        }

    agents[agent_id] = {
        "customer": customer.strip(),
        "agent_name": agent_name.strip(),
        "status": "active",
        "registered_at": current_time(),
        "revoked_at": None
    }

    save_agents(agents)

    return {
        "success": True,
        "message": "AI agent registered successfully.",
        "agent": agents[agent_id]
    }


def revoke_agent(agent_name):
    """Revoke an agent and save its revocation timestamp."""

    agents = load_agents()
    agent_id = agent_name.strip().lower()

    if agent_id not in agents:
        return {
            "success": False,
            "message": "Agent not found."
        }

    if agents[agent_id]["status"] == "revoked":
        return {
            "success": False,
            "message": "Agent permission is already revoked."
        }

    agents[agent_id]["status"] = "revoked"
    agents[agent_id]["revoked_at"] = current_time()

    save_agents(agents)

    log_request(
        customer=agents[agent_id]["customer"],
        agent_name=agents[agent_id]["agent_name"],
        action="revoke_agent",
        amount=0,
        decision="REVOKED",
        rule="R2",
        reason="Customer revoked this AI agent's permission."
    )

    return {
        "success": True,
        "message": "Agent permission revoked successfully.",
        "revoked_at": agents[agent_id]["revoked_at"]
    }


def get_agent_status(agent_name):
    """Check whether an agent is active, revoked or unknown."""

    agents = load_agents()
    agent_id = agent_name.strip().lower()

    if agent_id not in agents:
        return "unknown"

    return agents[agent_id]["status"]


def log_request(customer, agent_name, action, amount,
                decision, rule, reason):
    """Store each request and decision in the audit CSV."""

    initialize_audit_log()

    with open(AUDIT_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            current_time(),
            customer,
            agent_name,
            action,
            amount,
            decision,
            rule,
            reason
        ])


def process_request(customer, agent_name, action, amount=0):
    """Evaluate a request and automatically record the decision."""

    status = get_agent_status(agent_name)

    result = evaluate_request(
        customer=customer,
        agent_name=agent_name,
        action=action,
        amount=amount,
        agent_status=status
    )

    log_request(
        customer=customer,
        agent_name=agent_name,
        action=action,
        amount=amount,
        decision=result["decision"],
        rule=result["rule"],
        reason=result["reason"]
    )

    return result


# Initialize the audit log when the module loads.
initialize_audit_log()
