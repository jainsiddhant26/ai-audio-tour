# 🎧 AI Audio Tour Guide

> A multi-agent AI app that generates a personalized, narrated audio tour of any landmark in the world — in seconds.

Built with **CrewAI**, **Groq (Llama 3.3 70B)**, **Edge-TTS**, and **Streamlit**.

---

## 🌍 Live Demo

🔗 Coming Soon

---

## 📸 Screenshots

**Home Screen**
![Home Screen](assets/Home%20screen.png)

**Filled Form**
![Filled Form](assets/Filled%20form.png)

**Generating Tour**
![Generating](assets/Generating.png)

**Result — Script + Audio**
![Result](assets/Result.png)

---

## 🧠 How It Works

This app uses a **5-agent CrewAI pipeline** where each agent has a specific role:

| Agent | Role |
|---|---|
| 🗓️ Planner | Allocates word count per topic based on duration |
| 📜 History Agent | Writes the historical narrative in simple English |
| 🏛️ Architecture Agent | Describes design and structure in plain language |
| 🎭 Culture Agent | Covers local traditions and heritage simply |
| 🎙️ Orchestrator | Joins all sections and converts script to audio |

---

## ⚙️ Tech Stack

| Layer | Tool | Cost |
|---|---|---|
| Multi-Agent Framework | CrewAI | Free |
| LLM | Groq — Llama 3.3 70B | Free |
| Text to Speech | Edge-TTS (en-US-JennyNeural) | Free |
| UI | Streamlit | Free |
| Hosting | Streamlit Community Cloud | Free |

**Total cost: ₹0**

---

## 🚀 Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/jainsiddhant26/ai-audio-tour.git
cd ai-audio-tour
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
pip install litellm
```

### 4. Add API keys
Create a `.env` file in the root:
```
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
```
- Get Groq API key free at → [console.groq.com](https://console.groq.com)
- Get Tavily API key free at → [app.tavily.com](https://app.tavily.com)

### 5. Run the app
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
ai-audio-tour/
├── app.py                  # Streamlit UI
├── tts.py                  # Edge-TTS audio generation
├── agents/
│   ├── __init__.py
│   └── tour_agents.py      # CrewAI 5-agent pipeline
├── outputs/                # Generated audio files
├── assets/                 # Screenshots
├── requirements.txt
└── .env                    # API keys (not committed)
```

---

## 👤 Author

Built by [Siddhant Jain](https://github.com/jainsiddhant26) as part of an AI PM Portfolio.
