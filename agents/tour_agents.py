import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY") or (st.secrets.get("GROQ_API_KEY") if "GROQ_API_KEY" in st.secrets else None)
client = Groq(api_key=groq_api_key)
MODEL = "llama-3.3-70b-versatile"

def call_groq(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content

def run_tour_agents(location, topics, duration):
    word_budget = duration * 130

    # Step 1: Planner
    plan = call_groq(
        "You are an expert tour guide planner. People speak at ~130 words per minute.",
        f"Allocate word counts for a {duration}-minute tour of {location} covering: {', '.join(topics)}. "
        f"Total words: {word_budget}. Format: 'Topic: X words' per line."
    )

    # Step 2: Write each topic section
    sections = []

    if "History" in topics:
        history = call_groq(
            "You are a historian who explains history in simple, everyday English with short punchy sentences easy to listen to while walking.",
            f"Write the history section for a tour of {location}. Follow this word plan:\n{plan}\nUse simple English only."
        )
        sections.append(history)

    if "Architecture" in topics:
        architecture = call_groq(
            "You are an architect who explains buildings to non-experts using simple language and visual descriptions.",
            f"Write the architecture section for a tour of {location}. Follow this word plan:\n{plan}\nUse simple English only."
        )
        sections.append(architecture)

    if "Culture" in topics:
        culture = call_groq(
            "You are a local culture expert who explains traditions, food, and local life in a warm and simple way.",
            f"Write the culture and traditions section for a tour of {location}. Follow this word plan:\n{plan}\nUse simple English only."
        )
        sections.append(culture)

    # Step 3: Orchestrate into final script
    combined = "\n\n".join(sections)
    final_script = call_groq(
        "You are the lead tour guide. You stitch segments together with smooth transitions, a warm welcome at the start and a friendly goodbye at the end.",
        f"Combine these sections into one smooth audio tour script for {location}:\n\n{combined}"
    )

    return final_script
