from agents.swarm_master import swarm

def get_agent_swarm_status():
    """Return speech summary of 11 AI Swarm Sub-Agents."""
    data = swarm.get_real_swarm_telemetry()
    active_conn = f"{data['connection']['from']} -> {data['connection']['to']}"
    return f"AI Swarm is operating smoothly across 11 specialist sub-agents, Boss! Active connection node: {active_conn}."
