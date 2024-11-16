from fastapi import FastAPI
from api.v1 import users
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(debug=True)
app.include_router(users.router, prefix="/api/v1/users")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
