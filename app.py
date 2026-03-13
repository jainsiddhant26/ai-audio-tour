import os
import streamlit as st
from dotenv import load_dotenv
from agents.tour_agents import run_tour_agents
from tts import generate_audio

# Load environment variables
load_dotenv()

# Check for API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or (st.secrets.get("GROQ_API_KEY") if "GROQ_API_KEY" in st.secrets else None)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY") or (st.secrets.get("TAVILY_API_KEY") if "TAVILY_API_KEY" in st.secrets else None)


# Set page configuration
st.set_page_config(
    page_title="AI Audio Tour Guide",
    page_icon="🎧",
    layout="centered"
)

# Custom CSS for a cleaner look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Page Title and Subtitle
st.title("AI Audio Tour Guide 🎧")
st.markdown("### Discover the hidden stories of any landmark in minutes.")

# Input Section
st.divider()
location = st.text_input("Enter a location or landmark", placeholder="e.g., Eiffel Tower, Taj Mahal, Grand Canyon")

# Selection Section
st.write("What would you like to focus on?")
col1, col2, col3 = st.columns(3)
with col1:
    history = st.checkbox("History", value=True)
with col2:
    architecture = st.checkbox("Architecture", value=True)
with col3:
    culture = st.checkbox("Culture", value=True)

# Duration Section
duration = st.slider("Tour duration (minutes)", min_value=5, max_value=30, value=10)

# Generate Button
if st.button("Generate Tour"):
    if not location:
        st.warning("Please enter a location first.")
    else:
        # Collect selected topics
        topics = []
        if history: topics.append("History")
        if architecture: topics.append("Architecture")
        if culture: topics.append("Culture")
        
        if not topics:
            st.warning("Please select at least one topic.")
        else:
            with st.spinner(f"Generating your personalized tour of {location}..."):
                try:
                    # Run the agents
                    tour_script = run_tour_agents(location, topics, duration)
                    st.session_state['tour_script'] = tour_script
                    
                    # Generate Audio
                    with st.spinner("Converting script to audio..."):
                        output_file = "outputs/tour.mp3"
                        audio_path = generate_audio(tour_script, output_file)
                        if audio_path:
                            st.session_state['audio_path'] = audio_path
                    
                    st.success("Tour generated!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            
# Results Section
st.divider()

st.subheader("Your Tour Script")
current_script = st.session_state.get('tour_script', "Your tour script will appear here...")
st.text_area("Script", value=current_script, height=400, label_visibility="collapsed")

st.subheader("Listen to Your Tour")
if 'audio_path' in st.session_state and os.path.exists(st.session_state['audio_path']):
    st.audio(st.session_state['audio_path'])
    # Add a download button for convenience
    with open(st.session_state['audio_path'], "rb") as file:
        st.download_button(
            label="Download Audio Tour",
            data=file,
            file_name="ai_audio_tour.mp3",
            mime="audio/mpeg"
        )
elif 'tour_script' in st.session_state:
    st.info("Audio is being generated or encountered an issue.")
else:
    st.info("Your audio will appear here...")

# Footer
st.markdown("---")
st.caption("Powered by CrewAI, Groq, and Edge-TTS")
