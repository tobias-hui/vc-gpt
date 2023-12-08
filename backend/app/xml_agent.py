from app.config import Settings
from app.agent.agent_tools import generate_bp_pdf

settings = Settings()

from typing import List, Tuple

from langchain.pydantic_v1 import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.tools.render import render_text_description
from langchain.agents import load_tools
from langchain.schema import AIMessage, HumanMessage
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents import AgentExecutor
from langchain.tools import DuckDuckGoSearchRun, Tool
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.agents.openai_functions_agent.agent_token_buffer_memory import AgentTokenBufferMemory
from app.agent.prompts import conversational_prompt, parse_output
# import langchain
# langchain.debug = True

def _format_chat_history(chat_history: List[Tuple[str, str]]):
    buffer = []
    for human, ai in chat_history:
        buffer.append(HumanMessage(content=human))
        buffer.append(AIMessage(content=ai))
    return buffer

def _format_intermediate_steps(intermediate_steps: List[str]):
    buffer = []
    for step in intermediate_steps:
        buffer.append(AIMessage(content=step))
    return buffer

memory_key = "history"
llm = ChatOpenAI(api_key=settings.openai_api_key, temperature=0, model_name = "gpt-4", streaming=True)
search = DuckDuckGoSearchRun()
memory = AgentTokenBufferMemory(llm=llm, memory_key=memory_key)

tools = load_tools(["dalle-image-generator", "llm-math"], llm=llm)
tools = tools + [
    Tool(
        name = "search",
        func = search.run,
        description = "useful for when you need to answer questions about current events",
    ),
    Tool.from_function(
        name = "generate_bp_pdf",
        func = generate_bp_pdf.run,
        description = "generate business plan pdf",
    )
]

#prompt = hub.pull("hwchase17/react-json")
prompt = conversational_prompt
prompt = prompt.partial(
    tools = render_text_description(tools),
    tool_names = ", ".join([t.name for t in tools]),
)

llm_with_stop = llm.bind(stop = ["\nObservation"])

agent = (
    {
        "question": lambda x: x["question"],
        "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
        "chat_history": lambda x: _format_chat_history(x["chat_history"]),
        #"intermediate_steps": lambda x: _format_intermediate_steps(x["intermediate_steps"]),
    }
    | prompt
    | llm_with_stop
    | parse_output
)

class AgentInput(BaseModel):
    question: str
    chat_history: List[Tuple[str, str]] = Field(..., extra={"widget": {"type": "chat"}})
    intermediate_steps: List[str] = Field([], extra={"widget": {"type": "hidden"}})

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, callbacks=[StreamingStdOutCallbackHandler()]).with_types(input_type=AgentInput)

agent_executor = agent_executor | (lambda x: x["output"])

