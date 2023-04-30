from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import openai
import os
from langchain.agents import Tool
from langchain.document_loaders import WebBaseLoader
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain import LLMChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish
import re

app = FastAPI()

load_dotenv()
# openai.api_key= os.environ.get("OPENAI_API_KEY")
openai_api_key = os.environ.get("OPENAI_API_KEY")

@app.get("/")
async def root():
    return {"message": "Hello World"}

origins = [
    "http://localhost:3000/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/website")
async def user_input(data: dict):
    print(data['webName'])
    print(data['prodName'])
    print(data['api'])
    openai_api_key = data['api']
    openai.api_key = openai_api_key

    # Using ChatOpenAI for lower usage fees, but you can use OpenAI. ChatOpenAI works fine as well 
    llm = ChatOpenAI(temperature=0)

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    embeddings = OpenAIEmbeddings()

    # Loading contexts from web page 
    loader = WebBaseLoader(data['webName'])
    docs = loader.load()
    texts = text_splitter.split_documents(docs)
    db = FAISS.from_documents(texts, embeddings)
    product = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db.as_retriever())
    
    # Define tools that you want to use. For ex, you can use SerpAPI for Google Search
    tools = [
        Tool(
        name = "Information",
        func=product.run,
        description="useful for when you need to get information about the product."
        ),
    ]

    # Set up the base template
    template = """Create an advertising post for a product that the user inputs. You have access to the following toolkits:
    {tools}
    Use the following format:
    Product: the input product you must advertise
    Thought: think about creating an advertising post 
    Action: the action to take, ask questions using [{tools}] to get relevant product information
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    Begin! Remember advertise the product accustomed to Twitter. Be concise and use hashtags.
    Product: {input}
    {agent_scratchpad}"""

    # Set up a prompt template
    class CustomPromptTemplate(StringPromptTemplate):
        # The template to use
        template: str
        # The list of tools available
        tools: List[Tool]
        
        def format(self, **kwargs) -> str:
            # Get the intermediate steps (AgentAction, Observation tuples)
            # Format them in a particular way
            intermediate_steps = kwargs.pop("intermediate_steps")
            thoughts = ""
            for action, observation in intermediate_steps:
                thoughts += action.log
                thoughts += f"\nObservation: {observation}\nThought: "
            # Set the agent_scratchpad variable to that value
            kwargs["agent_scratchpad"] = thoughts
            # Create a tools variable from the list of tools provided
            kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
            # Create a list of tool names for the tools provided
            kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
            return self.template.format(**kwargs)

    prompt = CustomPromptTemplate(
        template=template,
        tools=tools,
        # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
        # This includes the `intermediate_steps` variable because that is needed
        input_variables=["input", "intermediate_steps"]
    )

    class CustomOutputParser(AgentOutputParser):
        
        def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
            # Check if agent should finish
            if "Final Answer:" in llm_output:
                return AgentFinish(
                    # Return values is generally always a dictionary with a single `output` key
                    # It is not recommended to try anything else at the moment :)
                    return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                    log=llm_output,
                )
            # Parse out the action and action input
            regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
            match = re.search(regex, llm_output, re.DOTALL)
            if not match:
                raise ValueError(f"Could not parse LLM output: `{llm_output}`")
            
            action_input = match.group(1)
            # Use appropriate tools that the chain needs to use 
            return AgentAction(tool="Information", tool_input=action_input.strip(" ").strip('"'), log=llm_output)
        
    output_parser = CustomOutputParser()

    llm_chain = LLMChain(llm=llm, prompt=prompt)
    tool_names = [tool.name for tool in tools]
    agent = LLMSingleActionAgent(
        llm_chain=llm_chain, 
        output_parser=output_parser,
        stop=["\nObservation: "], 
        allowed_tools=tool_names
    )
    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)
    response = agent_executor.run("Create a marketing post about " + data['prodName'])
    print("Response is: ", response)
    return {"message": response}
    # return {"message": "data loading"}
