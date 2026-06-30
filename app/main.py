from fastapi import FastAPI

app = FastAPI(
    title="Employee Leave Management System",
    version="1.0.0",
)

@app.get("/")
async def root():
    return {
        "message": "Employee Leave Management System API"
    }