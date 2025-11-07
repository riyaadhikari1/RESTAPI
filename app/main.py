from fastapi import FastAPI
from app.server.app import app as fastapi_app

app = fastapi_app

# Local testing
if __name__ == "__main__":
    import uvicorn
  
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
