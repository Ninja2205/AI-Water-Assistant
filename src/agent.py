import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

OPEN_API_KEY = os.getenv("OPEN_API_KEY")
llm = ChatOpenAI(api_key=OPEN_API_KEY, model="gpt-4o-mini", temperature=0.5)

class WaterIntakeAgent:
    def __init__(self):
        self.history = []

    def analyze_intake(self, intake_ml):
        prompt = f"""
        you are a hydration assistant. The user has consumed {intake_ml} ml of water today.
        provide a hydration status and suggest if they need to drink more water.
        """

        response = llm.invoke([HumanMessage(content=prompt)])

        return response.content

if __name__ == "__main__":
    agent = WaterIntakeAgent()
    intake = 1500
    feedback = agent.analyze_intake(intake)
    print(f"Hydration Analysis: {feedback}")
