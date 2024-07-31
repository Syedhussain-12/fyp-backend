import dataclasses
from datetime import datetime
# import imp
import json
from urllib import response
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# import mysqlx
from .models import User
from .serializer import UserLoginSerializer, UserSerializer

from django.db import connections

# from rest_framework.views import APIView

from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
import io
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from time import gmtime, strftime
# Create your views here.

from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import GmailToolkit
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import wandb_tracing_enabled
from langchain.llms import OpenAI
from langchain_community.agent_toolkits import GmailToolkit
from langchain_google_calendar_tools.utils import build_resource_service, get_oauth_credentials
from langchain_google_calendar_tools.tools.create_new_event.tool import CreateNewEvent
from langchain_google_calendar_tools.tools.list_events.tool import ListEvents
from langchain_google_calendar_tools.tools.update_exist_event.tool import UpdateExistEvent

from langchain_google_calendar_tools.helper_tools.get_current_datetime import GetCurrentDatetime

#combined agents
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import wandb_tracing_enabled
from langchain.llms import OpenAI

from langchain_google_calendar_tools.utils import build_resource_service, get_oauth_credentials
from langchain_google_calendar_tools.tools.create_new_event.tool import CreateNewEvent
from langchain_google_calendar_tools.tools.list_events.tool import ListEvents
from langchain_google_calendar_tools.tools.update_exist_event.tool import UpdateExistEvent

from langchain_google_calendar_tools.helper_tools.get_current_datetime import GetCurrentDatetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from rest_framework import status
from .models import Chat
from .serializer import ChatSerializer

CALENDAR_CREDENTIALS= ''
load_dotenv()

@api_view(['GET','POST'])
def user(request):
    print('cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc',request)
    print('testttt')
    
    if request.method == "GET":
        user = User.objects.all()
        serializer = UserSerializer(user , many=True)
        return Response(serializer.data)

    if request.method == "POST":
        print('hfgfhf')
        # user123 = User.objects.raw("select * from user")
        # user12 = User.objects.raw("select * from user")
        # print(user123,user12)
        pythondata = JSONParser().parse(request)
        
        signupserializer = UserSerializer(data=pythondata)
        # print(pythondata['username'])
        username=str(pythondata['username'])
        password=str(pythondata['password'])
        loginserializer = UserLoginSerializer(data=pythondata)
        # print(222222222222222222)
        # print(loginserializer)
        # print(222222222222222222)
        check_login=False
        check_signup=False
        cursor = connections['default'].cursor()
        if signupserializer.is_valid():
        
            # user = User.objects.raw("select * from User where username =%s" , [username])
            user = User.objects.filter(username=username)
            if user:
                print("username already exist")
                check_signup = True
                return Response("username already exist")
            
            if check_signup == False:
                print('yes')
                user = User(first_name=signupserializer.data['first_name'], last_name=signupserializer.data['last_name'], email=signupserializer.data['email'], username=signupserializer.data['username'], password=signupserializer.data['password'])
                # user.save()
                # user_instance = signupserializer.save()
                er_instance = user.save()

                # cursor.execute("INSERT INTO User(first_name,last_name,email,username,password) VALUES( %s , %s, %s, %s, %s  )"
                # , [signupserializer.data['first_name'],signupserializer.data['last_name'],signupserializer.data['email'],signupserializer.data['username'],signupserializer.data['password']])
                print('yesssssss')
                
            
                return Response("account create successfully")
            
        if loginserializer.is_valid():            
            print(loginserializer.data['username'])
            # user = User.objects.raw("select * from User")
            user = User.objects.filter(username=username , password=password)
            # user1 = User.objects.raw("select * from User where username =%s AND password =%s" , [username,password])

            if user:
                print("aaaaaaaaaaaaa")
                check_login = True
                return Response("proceed")
            
            if check_login == False:
                print("bbbbbbbbb")
                return Response("Wrong Credentials")
            
@api_view(['GET','POST'])
def assistant(request):
    print("test")
    toolkit = GmailToolkit(redirect_url="http://localhost:58111/")
    credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
    )

    api_resource = build_resource_service(credentials=credentials)
    toolkit = GmailToolkit(api_resource=api_resource)
    tools = toolkit.get_tools()
    # tool
    load_dotenv()   
    instructions = """You are an assistant."""
    base_prompt = hub.pull("langchain-ai/openai-functions-template")
    prompt = base_prompt.partial(instructions=instructions)
    llm = ChatOpenAI(temperature=0)
    agent = create_openai_functions_agent(llm, toolkit.get_tools(), prompt)
    agent_executor = AgentExecutor(
    agent=agent,
    tools=toolkit.get_tools(),
    # This is set to False to prevent information about my email showing up on the screen
    # Normally, it is helpful to have it set to True however.
    verbose=False,
    )
    print("befor invoke")
    return Response(  agent_executor.invoke(
    {"input": "what is my last email? what is the title and description?"}
    ))
  
    
    
@api_view(['GET','POST'])
def test(request):
    if request.method == "GET":
        user = User.objects.all()
        serializer = UserSerializer(user , many=True)
        return Response(serializer.data)
    
    
    
@api_view(['GET','POST'])
def calendar(request):
    load_dotenv()
    credentials = get_oauth_credentials(
    client_secrets_file="creds.json"
)

    api_resource = 'build_resource_sehttps://accounts.google.com/o/oauth2/auth?response_type=code&client_id=656243832850-g38gef1u1g56503dvvtqaf91546r7dml.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A60085%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar.events&state=4Myn531FDNwons9tTMVetEyppgyaDq&access_type=offlinervice(credentials=credentials)'
    agent = initialize_agent(
    tools=[
        ListEvents(api_resource=api_resource),
        CreateNewEvent(api_resource=api_resource),
        UpdateExistEvent(api_resource=api_resource),
        GetCurrentDatetime(),
    ],
    llm=OpenAI(temperature=0),
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)
    
    # with wandb_tracing_enabled():
    return Response (
        agent.run(
        "Find the event scheduled on 2023-11-14 at 10:00 has summary 'test' and update its summary to 'test and change summary'"
    ))

    # print(output)

def get_oauth_credentials(client_secrets_file):
    scopes = ['https://www.googleapis.com/auth/calendar.events']
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes=scopes)
    creds = flow.run_local_server(port=51010)
    print('4444444444444444444444')
    return creds

@api_view(['GET','POST'])
def combineAgent(request):
    toolkit = GmailToolkit(redirect_url="http://localhost:51010/")
    
    from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
    print('1111111111')
# Can review scopes here https://developers.google.com/gmail/api/auth/scopes
# For instance, readonly scope is 'https://www.googleapis.com/auth/gmail.readonly'
    credentials = get_gmail_credentials(
        token_file="token.json",
        scopes=["https://mail.google.com/"],
        client_secrets_file="credentials.json",
    )
    print('222222222222222')
    api_resource = build_resource_service(credentials=credentials)
    toolkit = GmailToolkit(api_resource=api_resource)
    tools = toolkit.get_tools()
  
    print('3333333333333')
    instructions = """You are an assistant."""
    base_prompt = hub.pull("langchain-ai/openai-functions-template")
    prompt = base_prompt.partial(instructions=instructions)
    llm = ChatOpenAI(temperature=0)
    # load_dotenv()


    def build_resource_service(credentials):
        service = build('calendar', 'v3', credentials=credentials)
        print('5555555555555')
        return service
    global CALENDAR_CREDENTIALS
    if CALENDAR_CREDENTIALS=='':
        
        CALENDAR_CREDENTIALS = get_oauth_credentials(client_secrets_file="credentials.json")
    print("testttttttt",credentials)
    api_resource = build_resource_service(credentials=CALENDAR_CREDENTIALS)
    combined_tools = toolkit.get_tools() + [ListEvents(api_resource=api_resource),
        CreateNewEvent(api_resource=api_resource),
        UpdateExistEvent(api_resource=api_resource),
        GetCurrentDatetime(),
    ]
    agent = create_openai_functions_agent(llm, combined_tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=combined_tools,
        # This is set to False to prevent information about my email showing up on the screen
        # Normally, it is helpful to have it set to True however.
        verbose=True,
        handle_parsing_errors=True
    )
    # with wandb_tracing_enabled():
        # output = agent_executor.invoke(
        # {'input':"Find the event scheduled on 2023-11-14 at 10:00 has summary 'test', returned html link and event summary."}
        # )
    data1 = request.data
    input = data1.get('user_input')
    output = agent_executor.invoke(
        {'input':input}
    )
    return Response(output)         
    
    
#gfhghf


@api_view(['GET','POST'])
def insert_and_fetch_chats(request):
    # if request.method == 'GET':
    #     print("test")
    #     chats = Chat.objects.all()
    #     chat_serializer = ChatSerializer(chats, many=True)
    #     return Response(chat_serializer.data, status=status.HTTP_201_CREATED)
    # pythondata = JSONParser().parse(request)
        # print(pythondata)
    

    if request.method == 'POST':
        ##gmail_cal api call
        toolkit = GmailToolkit(redirect_url="http://localhost:51010/")
        
        from langchain_community.tools.gmail.utils import (
        build_resource_service,
        get_gmail_credentials,
    )
        print('1111111111')
    # Can review scopes here https://developers.google.com/gmail/api/auth/scopes
    # For instance, readonly scope is 'https://www.googleapis.com/auth/gmail.readonly'
        credentials = get_gmail_credentials(
            token_file="token.json",
            scopes=["https://mail.google.com/"],
            client_secrets_file="credentials.json",
        )
        print('222222222222222')
        api_resource = build_resource_service(credentials=credentials)
        toolkit = GmailToolkit(api_resource=api_resource)
        tools = toolkit.get_tools()
        load_dotenv()
        print('3333333333333')
        instructions = """You are an assistant."""
        base_prompt = hub.pull("langchain-ai/openai-functions-template")
        prompt = base_prompt.partial(instructions=instructions)
        llm = ChatOpenAI(temperature=0)
        load_dotenv()
        # def get_oauth_credentials(client_secrets_file):
        #     scopes = ['https://www.googleapis.com/auth/calendar.events']
        #     flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes=scopes)
        #     creds = flow.run_local_server(port=51010)
        #     print('4444444444444444444444')
        #     return creds

        def build_resource_service(credentials):
            service = build('calendar', 'v3', credentials=credentials)
            print('5555555555555')
            return service
        
        global CALENDAR_CREDENTIALS
        if CALENDAR_CREDENTIALS=='':
            
            CALENDAR_CREDENTIALS = get_oauth_credentials(client_secrets_file="credentials.json")
        print("testttttttt",credentials)
        api_resource = build_resource_service(credentials=CALENDAR_CREDENTIALS)
        combined_tools = toolkit.get_tools() + [ListEvents(api_resource=api_resource),
            CreateNewEvent(api_resource=api_resource),
            UpdateExistEvent(api_resource=api_resource),
            GetCurrentDatetime(),
        ]
        agent = create_openai_functions_agent(llm, combined_tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=combined_tools,
            # This is set to False to prevent information about my email showing up on the screen
            # Normally, it is helpful to have it set to True however.
            verbose=True,
            handle_parsing_errors=True
        )
        # with wandb_tracing_enabled():
            # output = agent_executor.invoke(
            # {'input':"Find the event scheduled on 2023-11-14 at 10:00 has summary 'test', returned html link and event summary."}
            # )
       

        # request_data = request.data
        # response= Response (
        #         agent_executor.invoke(
        #     {'input':request_data['user_input']}
        #     ))
        data1 = request.data
        input = data1.get('user_input')
        output = agent_executor.invoke(
            {'input':input}
        )
        response= Response(output)   
            
        response_data = response.data

# Now you can access the 'output' key
        output_value = response_data.get('output')
        
        
        
       
        data1['ai_response']= output_value
        
        # Insert new chat record
        serializer = ChatSerializer(data=data1)
        if serializer.is_valid():
            serializer.save()
            email = data1.get('email')
            if email:
                chats = Chat.objects.filter(email=email)
                chat_serializer = ChatSerializer(chats, many=True)
                return Response(chat_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": False}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def get_chat_data(request):
    print('request1',request)

    pythondata = JSONParser().parse(request)
        # print(pythondata)
    email = pythondata.get("email",None)
    print('email', email)
    if email:
 
        chats = Chat.objects.filter(email=email)
        if chats.exists():
            chat_serializer = ChatSerializer(chats, many=True)
            return Response(chat_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"status": False}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"detail": "Email query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)


# filter api

@api_view(['GET','POST'])
def fetch_chats_by_date_and_email(request):
    pythondata = JSONParser().parse(request)
    email = pythondata.get("email",None)
    date_str = pythondata.get("date",None)
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
    print("..........",email,date_str)
    # if not email:
    #     return Response({"error": "Email is required."}, status=400) 2024-07-06

    chats = Chat.objects.filter(email=email, timestamp__date=date)
    if chats:
        if chats.exists():
            chat_serializer = ChatSerializer(chats, many=True)
            return Response({'status':True, 'response' : chat_serializer.data } , status=status.HTTP_200_OK)
        else:
            return Response({"status": False}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"status": False}, status=status.HTTP_400_BAD_REQUEST)
    
    
# @api_view(['GET','POST'])
# def test(request):
#     return Response (
#         agent_executor.invoke(
#         {'input':"Find the event scheduled on 2023-11-14 at 10:00 has summary 'test', returned html link and event summary."}
#         ))