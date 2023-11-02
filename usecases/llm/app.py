import chainlit as cl
import os
from langchain.prompts import  PromptTemplate
from langchain.chains import LLMChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import HumanMessage
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


### Dozer

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

    
    return [id,name,income,age,dependents,credit_amt,repay_status,util_ratio,address, prob]



#user_env = user_session.get(".env")
OPEN_API_KEY = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENV = os.environ.get("PINE_ENV")
 # platform.openai.com
model_name = 'text-embedding-ada-002'


embed = OpenAIEmbeddings(
    model=model_name,
    openai_api_key=OPEN_API_KEY
)

# find ENV (cloud region) next to API key in console
index_name = 'langchain-retrieval-agent'
pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENV
)


#embeddings = OpenAIEmbeddings()


text_field = "Answer"
index = pinecone.Index('langchain-retrieval-agent')
# switch back to normal index for langchain
#index = pinecone.Index(index_name)

vectorstore = Pinecone(
    index, embed.embed_query, text_field
)

llm = ChatOpenAI(
    openai_api_key = OPEN_API_KEY,
    model_name='gpt-4',
    temperature=0.0
)

conversational_memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True
)
# retrieval qa chain
chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

def setName(userName):
    global name
    name = userName

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


    return ( f"ID = {id} ,name = {name1} ,age = {age}, income = {income}, dependents = {dependents},repay_status={repay_status}, credit utilisation ratio ={util_ratio} ,address={address}, available credit={credit_amt}, probability of default = {prob} ")

    
tools = [
    Tool(
        name='Knowledge Base',
        func=chain.run,
        description=(
            "Useful when you need general information about bank policies and bank offerings. "\
            'use this tool when answering general knowledge queries to get '\
            'more information about the topic'
        )
    ),
    Tool(
        name = 'Customer Data',
        func = customerProfile,
        description=(
            "Useful when you need customer data to decide eligibility for a particular credit card. "
            "Use to check the probability of default and available balance to use it for eligibility"
        )
    )
]


agent = initialize_agent(
    agent='chat-conversational-react-description',
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=5,
    early_stopping_method='generate',
    memory=conversational_memory
)


global res
@cl.on_chat_start

async def start():
    intro = "Hi there, I am an assistant for Bank A. I am here to assist you with all your banking needs! Please enter your id:  "
    
    res = await cl.AskUserMessage(content=intro,timeout=45,raise_on_timeout=True).send()
    
    id = int(res['content'])
    greeting = f"Hi {res['content']}. What brings you here?"
    await cl.Message(content=greeting).send()
    setName(res['content'])
    # global credit 
    # credit = getCredit(int(res['content']))
    global customerinfo
    customerinfo = customerProfile(int(res['content']) )
    print(customerinfo)
    
    agent = ConversationalChatAgent.from_llm_and_tools(
        llm=llm,
        tools=tools,
        system_message = f"You have customer info of a customer which is as follows {customerinfo}. You have to use this information along with Knowledge base to decide if the customer is eligible for a credit card or not.",
        verbose=True,
        max_iterations=5,
        early_stopping_method='generate',
        memory=conversational_memory

    )

    global agent_chain
    agent_chain = AgentExecutor.from_agent_and_tools(
        agent = agent,
        tools = tools, 
        verbose = True,
        max_iterations = 5,
        early_stopping_method = 'generate',
        memory = conversational_memory

    )
    cl.user_session.set("chain", agent_chain)



@cl.on_message
async def main(message: str):
    agent_chain = cl.user_session.get("chain") 
    response = await cl.make_async(agent_chain.run)(message.content)

    await cl.Message(
        content=response,
    ).send()