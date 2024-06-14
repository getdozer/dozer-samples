import chainlit as cl
import os
from langchain.prompts import  PromptTemplate
from langchain.chains import LLMChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import HumanMessage
from time import sleep
## For Vector DB
import pinecone
import uuid
from langchain.vectorstores import Pinecone
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import RetrievalQA
from langchain.agents import Tool
#from langchain import PromptTemplate, HuggingFaceHub, LLMChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.agents import initialize_agent
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.prompts.chat import ChatPromptTemplate,HumanMessagePromptTemplate,SystemMessagePromptTemplate
from chainlit import user_session
import os
from pydozer.api import ApiClient
from langchain.agents import ConversationalChatAgent, AgentExecutor
import re
import json

def show_json(obj):
    display(json.loads(obj.model_dump_json()))


def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        sleep(0.5)
    return run
### Dozer
from openai import OpenAI
client = OpenAI()
DOZER_CLOUD_HOST = "data.getdozer.io:443"

def get_api_client(app_id=None, token=None):
    return ApiClient("financial_profile", url=DOZER_CLOUD_HOST, app_id=app_id,
                     secure=True, token=token) if app_id else ApiClient("financial_profile", url="localhost:80")


customer_client = get_api_client(app_id=os.environ.get("DOZER_APP_ID"), token=os.environ.get("DOZER_TOKEN"))

def getCustomerData(input):
    data = customer_client.query({"$filter": {"id":input}})
    rec = data.records[0].record
    id = rec.values[0].int_value
    name = rec.values[1].string_value
    income = rec.values[2].int_value
    age = rec.values[3].int_value
    dependents = rec.values[4].int_value
    address = rec.values[5].string_value
    prob = rec.values[6].float_value
    credit_amt = rec.values[7].int_value
    repay_status = rec.values[8].float_value
    util_ratio = rec.values[9].float_value

    
    return [id,name,income,age,dependents, address, prob,credit_amt,repay_status,util_ratio ]



#user_env = user_session.get(".env")
OPEN_API_KEY = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENV = os.environ.get("PINE_ENV")
 # platform.openai.com
model_name = 'text-embedding-ada-002'



# find ENV (cloud region) next to API key in console
index_name = 'langchain-retrieval-agent'
pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENV
)


#embeddings = OpenAIEmbeddings()


text_field = "Answer"
index = pinecone.Index('langchain-retrieval-agent')

file = client.files.create(
  file=open("/home/mrunmay/Desktop/Dozer/dozer-samples/usecases/llm/data/BankFAQs.csv", "rb"),
  purpose='assistants'
)

# switch back to normal index for langchain
#index = pinecone.Index(index_name)


def customerProfile(input):
    data = getCustomerData(int(input))
    id  = data[0]
    name1 = data[1]
    income = data[2]
    age= data[3]
    dependents= data[4]
    address= data[5]
    prob = data[6]
    credit_amt= data[7]
    repay_status= data[8]
    util_ratio= data[9]

    profile = {
        "id": id,
        "name": name1,
        "age": age,
        "income": income,
        "dependents": dependents,
        "address": address,
        "prob": prob,
        "credit_amt": credit_amt,
        "repay_status": repay_status,
        "util_ratio": util_ratio


    }
    return json.dumps(profile)

tools = [
    {
        "type": "function",
        "function": {
            "name": "customerProfile",
            "description": "Useful when you need customer data to decide eligibility for a particular credit card. Use to check the probability of default and available balance to use it for eligibility",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {"type": "number"}

        },
        "required": ["id"]

    }},

        
    }, 
    {
        "type": "code_interpreter",
    }
]
assistant = client.beta.assistants.create(
    name="Bank Assistant",
    instructions="You are a bank chat bot. Help the client with all their banking needs. Calculate if the client is eligible for a credit card or not depending upon their customer profile",
    tools=tools,
    model="gpt-4-1106-preview",
    file_ids=[file.id]
    
)


def setName(userName):
    global name
    name = userName


    

global res
@cl.on_chat_start

async def start():
    intro = "Hi there, I am an assistant for Bank A. I am here to assist you with all your banking needs! Please enter your id:  "
    
    res = await cl.AskUserMessage(content=intro,timeout=200,raise_on_timeout=True).send()
    global id
    id = int(res['content'])
    greeting = f"Hi {res['content']}. What brings you here?"
    await cl.Message(content=greeting).send()
    setName(res['content'])
    # global credit 
    # credit = getCredit(int(res['content']))
    global customerinfo
    customerinfo = customerProfile(int(res['content']) )


    #print(customerinfo)
    thread = client.beta.threads.create()
    cl.user_session.set("chain", thread)



@cl.on_message
async def main(text_rep: str):
    thread = cl.user_session.get("chain") 

    #print(text_rep.content)
    #print(thread.id, thread)
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"{text_rep.content}"
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        model="gpt-4-1106-preview",
        instructions=f"Please help the user according to his ID: {id} ",
        tools = tools,

    )  

    wait_on_run(run, thread)
    if run.status == "requires_action":

        tool_id = run.required_action.submit_tool_outputs.tool_calls
        run = client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread.id,
        run_id=run.id,
        tool_outputs=[
            {
            "tool_id": tool_id[0].id,
            "output": customerinfo,
        }
        ]

        )

        
    

    wait_on_run(run, thread)



    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    obj_string = str(messages)
    pattern = re.compile(
    r"ThreadMessage\(id='(?P<id>[^']*)', assistant_id='(?P<assistant_id>[^']*)', content=\[MessageContentText\(text=Text\((annotations=\[.*?\], )?value=\"(?P<content>.*?)\"\), type='(?P<message_content_text_type>[^']*)'\)\], created_at=(?P<created_at>\d+), file_ids=\[(?P<file_ids>.*?)\], metadata=\{(?P<metadata>.*?)\}, object='(?P<object>[^']*)', role='(?P<role>[^']*)', run_id='(?P<run_id>[^']*)', thread_id='(?P<thread_id>[^']*)'\)"
    )
    matches = pattern.finditer(obj_string)
    for match in matches:
        text_rep = match.group('content').replace('\\n', '\n').replace('\\"', '"')


    #print(content)
    await cl.Message(
        content=text_rep ,
    ).send()