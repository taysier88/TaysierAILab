from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import os
import requests

app = FastAPI(title="Taysier AI Lab - Web Agent Core")

# 1. نماذج البيانات (Data Models)
class TaskRequest(BaseModel):
    agent_id: String
    prompt: String
    is_complex: Optional[bool] = False

# 2. سجل شخصيات الوكلاء الخمسة (Agent Registry)
AGENT_PERSONAS = {
    "manager_agent": "You are the Master Orchestrator of Taysier AI Lab™. Coordinate tasks and direct workflows.",
    "research_agent": "You are the Market Research Expert. Analyze trends, products, and target audiences.",
    "marketing_agent": "You are the Creative Marketing Director. Design growth strategies and content architectures.",
    "sales_agent": "You are the Conversion Specialist. Optimize e-commerce paths, sales copies, and revenue.",
    "operations_agent": "You are the Operations Officer. Integrate workflows and handle process automation."
}

# مفتاح Gemini المجاني (يتم قراءته من إعدادات السيرفر الآمنة)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_FREE_GEMINI_API_KEY_HERE")

@app.get("/")
def home():
    return {"status": "AetherOS Web Engine Running", "free_tier": True}

@app.post("/workflow/execute")
async def execute_workflow(task: TaskRequest):
    if task.agent_id not in AGENT_PERSONAS:
        raise HTTPException(status_code=404, detail="Agent identity not found")
    
    system_instruction = AGENT_PERSONAS[task.agent_id]
    
    # صياغة النص النهائي المدمج بالشخصية والسياق
    final_prompt = f"[SYSTEM INSTRUCTION]: {system_instruction}\n[USER TASK]: {task.prompt}"
    
    # استدعاء API جيميناي المجاني سحابياً (بدون استهلاك 1 ميجا من رام جهازك)
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": final_prompt}]
        }]
    }
    
    try:
        response = requests.post(gemini_url, json=payload, headers=headers)
        response_data = response.json()
        
        # استخراج النص المولد من الإجابة
        ai_response = response_data['candidates'][0]['content']['parts'][0]['text']
        
        return {
            "agent": task.agent_id,
            "status": "COMPLETED",
            "execution_route": "CLOUD_FREE_TIER",
            "output": ai_response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")
      
