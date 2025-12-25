from google.adk.agents import Agent
from google.adk.tools import AgentTool

def create_router_agent(model, reflection_agent: Agent, planning_agent: Agent) -> Agent:
    reflection_tool = AgentTool(agent=reflection_agent)
    planning_tool = AgentTool(agent=planning_agent)

    return Agent(
        name="router_agent",
        model=model,
        tools=[reflection_tool, planning_tool],
        instruction="""You are the main interface for the Bullet Journal Assistant.
Your job is to understand the user's request and route it to the appropriate specialist agent.
- If the user wants to look back, review, or reflect, use the Reflection Agent.
- If the user wants to look forward, plan, or schedule, use the Planning Agent.
If the request is general, you can answer it yourself or ask for clarification.
"""
    )
