from langchain.agents import tool
from .tools import query_medgemma, call_emergency
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from .config import GROQ_API_KEY

@tool
def ask_mental_health_specialist(query: str) -> str:
    """
    Generate a therapeutic response using the MedGemma model.
    Use this for all general user queries, mental health questions, emotional concerns,
    or to offer empathetic, evidence-based guidance in a conversational tone.
    """
    return query_medgemma(query)

@tool
def emergency_call_tool() -> None:
    """
    Place an emergency call to the safety helpline's phone number via Twilio.
    Use this only if the user expresses suicidal ideation, intent to self-harm,
    or describes a mental health emergency requiring immediate help.
    """
    call_emergency()

@tool
def find_nearby_therapists_by_location(location: str) -> str:
    """
    Finds and returns a list of licensed therapists near the specified location.

    Args:
        location (str): The name of the city or area in which the user is seeking therapy support.

    Returns:
        str: A newline-separated string containing therapist names and contact info.
    """
    return (
        f"Here are some therapists near {location}, {location}:\n"
        "- Dr. Ayesha Kapoor - +1 (555) 123-4567\n"
        "- Dr. James Patel - +1 (555) 987-6543\n"
        "- MindCare Counseling Center - +1 (555) 222-3333"
    )


# Step1: Create an AI Agent & Link to backend



tools = [ask_mental_health_specialist, emergency_call_tool, find_nearby_therapists_by_location]
llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0.2, api_key=GROQ_API_KEY)
graph = create_react_agent(llm, tools=tools)

SYSTEM_PROMPT = """
You are an AI engine supporting mental health conversations with warmth and vigilance.
You have access to three tools:

1. `ask_mental_health_specialist`: Use this tool to answer all emotional or psychological queries with therapeutic guidance.
2. `locate_therapist_tool`: Use this tool if the user asks about nearby therapists or if recommending local professional help would be beneficial.
3. `emergency_call_tool`: Use this immediately if the user expresses suicidal thoughts, self-harm intentions, or is in crisis.

Always take necessary action. Respond kindly, clearly, and supportively.
"""



def parse_response(stream):
    tool_called_name = "None"
    final_response = None

    for s in stream:
        # Check if agent made a tool call
        agent_data = s.get('agent')
        if agent_data:
            messages = agent_data.get('messages')
            if messages and isinstance(messages, list):
                for msg in messages:
                    # Get tool name from tool_calls
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        tool_called_name = msg.tool_calls[0]['name']
                    # Get content if no tool calls (final response)
                    elif hasattr(msg, 'content') and msg.content:
                        final_response = msg.content

        # Check if a tool returned a response
        tool_data = s.get('tools')
        if tool_data:
            tool_messages = tool_data.get('messages')
            if tool_messages and isinstance(tool_messages, list):
                for msg in tool_messages:
                    # Get the tool response content
                    if hasattr(msg, 'content') and msg.content:
                        final_response = msg.content

    return tool_called_name, final_response


# def parse_response(stream):
#     tool_called_name = "None"
#     final_response = None

#     for s in stream:
#         # Check if a tool was called
#         tool_data = s.get('agent')
#         if tool_data:
#             tool_messages = tool_data.get('messages')
#             if tool_messages and isinstance(tool_messages, list):
#                 for msg in tool_messages:
#                     tool_called_name = getattr(msg, 'name', 'None')

#         # Check if agent returned a message
#         agent_data = s.get('tools')
#         if agent_data:
#             messages = agent_data.get('messages')
#             if messages and isinstance(messages, list):
#                 for msg in messages:
#                     if msg.content:
#                         final_response = msg.content

#     return tool_called_name, final_response


# if __name__ == "__main__":
#     while True:
#         user_input = input("User: ")
#         print(f"Received user input: {user_input[:200]}...")
#         inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", user_input)]}
#         stream = graph.stream(inputs, stream_mode="updates")
#         # for s in stream:
#         #     print(s)
#         tool_called_name, final_response = parse_response(stream)
#         print("TOOL CALLED: ", tool_called_name)
#         print("ANSWER: ", final_response)




# {'tools': 
#     {'messages': 
#         [ToolMessage(
#             content='Here are some therapists near Kathmandu, Kathmandu:\n- Dr. Ayesha Kapoor - +1 (555) 123-4567\n- Dr. James Patel - +1 (555) 987-6543\n- MindCare Counseling Center - +1 (555) 222-3333', 
#             name='find_nearby_therapists_by_location', 
#             id='80561005-8915-4bb9-9eed-065260df5571', 
#             tool_call_id='87fv8y75s')
#         ]
#     }
# }





# {'agent': 
#     {'messages': 
#         [AIMessage(content='',
#             additional_kwargs={'tool_calls': [{
#                 'id': '87fv8y75s', 
#                 'function': {'arguments': '{"location":"Kathmandu"}', 'name': 'find_nearby_therapists_by_location'}, 
#                 'type': 'function'
#             }]},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 24, 
#                     'prompt_tokens': 697, 
#                     'total_tokens': 721, 
#                     'completion_time': 0.027685511, 
#                     'prompt_time': 0.060204939, 
#                     'queue_time': 0.18703179, 
#                     'total_time': 0.08789045
#                 }, 
#                 'model_name': 'llama-3.1-8b-instant', 
#                 'system_fingerprint': 'fp_510c177af0', 
#                 'service_tier': 'on_demand', 
#                 'finish_reason': 'tool_calls', 
#                 'logprobs': None
#             },
#             id='run--6271b7d6-aea0-4119-be6a-d31825e71cd0-0', 
#             tool_calls=[{'name': 'find_nearby_therapists_by_location', 'args': {'location': 'Kathmandu'}, 'id': '87fv8y75s', 'type': 'tool_call'}], 
#             usage_metadata={'input_tokens': 697, 'output_tokens': 24, 'total_tokens': 721}
#         )]
#     }
# }
