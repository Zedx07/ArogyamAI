import os
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams, StdioServerParameters
from google.adk.agents import Agent


MCP_SERVER_PATH = "C:/ShubhamWorkspace/Dev/Hackathon/आरोग्यमAI/MCP/dist/index.js"

root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about user details. Get users details, search user by id, and filter users"
    ),
    instruction=(
        "You are a helpful agent who can answer questions related to users."
    ),
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='node',
                    args=[
                        os.path.abspath(MCP_SERVER_PATH),
                    ],
                ),
            ),
            # Optional: Filter specific tools if needed
            # tool_filter=['get_users', 'search_users', 'get_user_by_id', 'filter_users', 'get_companies']
        )
        ],
    
)