from fastapi import FastAPI

app = FastAPI(title="AgentFlow API", description="Backend API for AgentFlow Multi-agent Simulation Framework")

@app.get("/")
async def root():
    return {"message": "Welcome to AgentFlow API"}
