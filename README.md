# 🌦️ Agentic AI Weather Application

## 📌 Overview

This project is an **Agentic AI-based Weather Application** that dynamically fetches real-time weather information for any given location using a **multi-step reasoning workflow powered by LLMs and tools**.

Instead of directly calling APIs, the system uses an **AI agent that decides when and how to use external tools**, making it a practical example of **Agentic AI + Tool Calling + Workflow Orchestration**.

---

## ❗ Problem Statement

Traditional weather apps:
- Require direct API calls with predefined logic
- Lack flexibility in handling natural language queries
- Do not demonstrate intelligent reasoning or modular workflows

**Goal of this project:**
Build an intelligent system that:
1. Understands user queries in natural language  
2. Dynamically extracts location  
3. Converts location → coordinates  
4. Fetches real-time weather using those coordinates  
5. Returns structured and meaningful output  

---

## 🚀 Key Features

-  **Agentic AI Workflow**
-  **Tool Calling (Geocoding + Weather APIs)**
-  **Multi-step reasoning (Location → Coordinates → Weather)**
-  **Structured Outputs using Pydantic**
-  **Real-time API Integration**
-  **Observability using Logfire**

---

## 🏗️ Architecture
               User Query
                  ↓
             AI Agent (LLM)
                  ↓
      [Tool 1] Geocoding API → Get Latitude & Longitude
                  ↓
      [Tool 2] Weather API → Fetch Weather Data
                  ↓
      Structured Output (Temperature + Description)



---

## ⚙️ Tech Stack

- **LLM Framework**: PydanticAI  
- **Models Used**: Mistral / Groq / Gemini  
- **APIs**:
  - Geocoding API (maps.co)
  - Weather API (Tomorrow.io)
- **HTTP Client**: httpx  
- **Observability**: Logfire  
- **Language**: Python  

---

## 🧩 Implementation Details

### 1. Agent Design

The system uses a **single intelligent agent** with:
- Defined **tools**
- Structured **dependencies**
- Typed **outputs**

---

### 2. Tools Used

#### 📍 Geocode Tool
- Converts location → latitude & longitude  
- Uses Geocoding API  

#### 🌤️ Weather Tool
- Takes coordinates  
- Fetches real-time weather data  
- Maps weather codes → human-readable descriptions  

---

### 3. Data Models


    class weather_responses(BaseModel):
         temperature: float
         description: str


✅ Ensures

- Clean output  
- Type safety  
- Better debugging  

---

🔄 Workflow Logic

🧑‍💻 User Input

### ⚙️ Agent Execution

- Extracts location  
- Calls `extract_geocode`  
- Calls `extract_weather`  

### 📤 Response


    {
    "temperature": "32 °C",
    "description": "Partly Cloudy"
    }



### ⚙️ Agent Execution

- Extracts location  
- Calls `extract_geocode`  
- Calls `extract_weather`  

### 📤 Response


    {
    "temperature": "32 °C",
    "description": "Partly Cloudy"
    }

## 🌍 Use Cases

-  Smart assistants (chatbots with real-world data)  
-  AI-powered travel apps  
-  Location-based recommendation systems  
-  Learning Agentic AI & tool usage  
-  Prototype for autonomous AI systems  

---

## ⚠️ Challenges Faced

- Handling API response structures  
- Mapping weather codes to readable text  
- Ensuring correct tool invocation by LLM  
- Managing dependencies cleanly across agents  

---

## 🔮 Future Improvements

-  Add support for multiple cities in one query  
-  Add weather forecast (next 7 days)  
-  Voice-based input integration  
-  Use advanced reasoning models (GPT-4 / Claude)  
-  Streaming responses  
-  UI Dashboard (Streamlit / React)  
-  Add caching for repeated queries  
-  Error handling & fallback mechanisms  

---

## 📚 Resources

- PydanticAI Documentation  
- Tomorrow.io Weather API  
- Maps.co Geocoding API  
- Logfire Observability  

---

## 💡 Key Learnings

- How **Agentic AI** differs from traditional pipelines  
- Importance of **tool calling in LLM systems**  
- Designing **modular and scalable AI workflows**  
- Using **structured outputs with Pydantic**  
- Integrating **real-world APIs into AI systems**  

---

## 🏁 Conclusion

This project demonstrates how to move from:

➡️ Simple API calls  
➡️ To intelligent, autonomous AI agents  

It serves as a strong foundation for building real-world AI systems that can reason, act, and interact with external tools.
