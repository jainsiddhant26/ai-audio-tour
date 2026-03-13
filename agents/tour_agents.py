import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# Load environment variables
load_dotenv()

# Configure native CrewAI LLM with Groq
groq_api_key = os.getenv("GROQ_API_KEY") or (st.secrets.get("GROQ_API_KEY") if "GROQ_API_KEY" in st.secrets else None)
tavily_api_key = os.getenv("TAVILY_API_KEY") or (st.secrets.get("TAVILY_API_KEY") if "TAVILY_API_KEY" in st.secrets else None)

# Ensure keys are in environment for other tools
if groq_api_key: os.environ["GROQ_API_KEY"] = groq_api_key
if tavily_api_key: os.environ["TAVILY_API_KEY"] = tavily_api_key

groq_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=groq_api_key
)

class TourAgents:
    def __init__(self, location, topics, duration):
        self.location = location
        self.topics = topics
        self.duration = duration
        self.llm = groq_llm

    def planner_agent(self):
        return Agent(
            role='Tour Planner',
            goal=f'Create a word count allocation plan for a {self.duration} minute tour of {self.location} covering {", ".join(self.topics)}.',
            backstory="You are an expert tour guide planner. You know that people speak at about 130 words per minute. You allocate time and word counts to topics based on the total tour duration to ensure a balanced and engaging experience.",
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

    def history_agent(self):
        return Agent(
            role='History Expert',
            goal=f'Write a history section about {self.location} using the allocated word count.',
            backstory="You are a historian who explains events in simple, everyday English. You avoid complex jargon and use short, punchy sentences that are easy to listen to while walking.",
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

    def architecture_agent(self):
        return Agent(
            role='Architecture Guide',
            goal=f'Write an architecture section about {self.location} using the allocated word count.',
            backstory="You are an architect who loves explaining buildings to people who aren't experts. You use simple language to describe styles and structures, making them easy to visualize.",
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

    def culture_agent(self):
        return Agent(
            role='Culture Specialist',
            goal=f'Write a culture and traditions section about {self.location} using the allocated word count.',
            backstory="You are a local culture expert. You explain traditions, food, and local life in a warm, simple way that makes visitors feel like they belong.",
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

    def orchestrator_agent(self):
        return Agent(
            role='Tour Orchestrator',
            goal='Combine all sections into a single, flowing, and natural audio tour script.',
            backstory="You are the lead tour guide. You take individual segments and stitch them together with smooth transitions. You ensure the tone remains simple and friendly throughout. You add a warm welcome at the start and a friendly goodbye at the end.",
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

def run_tour_agents(location, topics, duration):
    agents = TourAgents(location, topics, duration)
    
    # Define Agents
    planner = agents.planner_agent()
    historian = agents.history_agent()
    architect = agents.architecture_agent()
    culturalist = agents.culture_agent()
    orchestrator = agents.orchestrator_agent()

    # Define Tasks
    plan_task = Task(
        description=f"Based on a {duration} minute duration (approx 130 words per min), allocate word counts for: {', '.join(topics)}. Location: {location}. Output format: 'Topic: X words'.",
        expected_output="A list of topics and their assigned word counts.",
        agent=planner
    )

    # We'll create specialized tasks for each topic, only if they are requested
    topic_tasks = []
    
    if "History" in topics:
        history_task = Task(
            description=f"Write the history of {location}. Use simple English and short sentences. Follow the word count from the plan.",
            expected_output="A historical overview in simple English.",
            agent=historian,
            context=[plan_task]
        )
        topic_tasks.append(history_task)

    if "Architecture" in topics:
        arch_task = Task(
            description=f"Describe the architecture of {location}. Use simple English and visual descriptions. Follow the word count from the plan.",
            expected_output="An architectural description in simple English.",
            agent=architect,
            context=[plan_task]
        )
        topic_tasks.append(arch_task)

    if "Culture" in topics:
        culture_task = Task(
            description=f"Explain the culture and traditions surrounding {location}. Use simple English. Follow the word count from the plan.",
            expected_output="A cultural overview in simple English.",
            agent=culturalist,
            context=[plan_task]
        )
        topic_tasks.append(culture_task)

    orchestration_task = Task(
        description="Join all the written sections into one smooth tour script. Add a warm 'Welcome to this audio tour' line at the start and a 'Hope you enjoyed the tour' sign-off. Ensure transitions between history, architecture, and culture are natural.",
        expected_output="A complete, cohesive audio tour script in simple language.",
        agent=orchestrator,
        context=topic_tasks
    )

    # Create Crew
    crew = Crew(
        agents=[planner, historian, architect, culturalist, orchestrator],
        tasks=[plan_task] + topic_tasks + [orchestration_task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()
    return str(result)
