from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agent import WaterIntakeAgent
from src.database import log_intake, get_intake_history
from src.logger import log_message

app = FastAPI()
agent = WaterIntakeAgent()

class WaterIntakeRequest(BaseModel):
    user_id: str
    intake_ml : int 

@app.post("/log-intake")
async def log_water_intake(request: WaterIntakeRequest):
    # Save to database first
    success = log_intake(request.user_id, request.intake_ml)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to log water intake to database")
    
    log_message(f"user {request.user_id} logged {request.intake_ml}ml")
    
    # Get AI analysis (don't fail if this errors)
    try:
        analysis = agent.analyze_intake(request.intake_ml)
        return {"message": "Water intake logged successfully", "analysis": analysis}
    except Exception as e:
        log_message(f"Error getting AI analysis: {e}")
        return {"message": "Water intake logged successfully", "analysis": "Analysis temporarily unavailable"}

@app.get("/history/{user_id}")
async def get_water_history(user_id: str):
    history = get_intake_history(user_id)
    return {"user_id" : user_id, "history" : history}

