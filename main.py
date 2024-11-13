from fastapi import FastAPI
from api.v1 import users
import uvicorn

app = FastAPI(debug=True)
app.include_router(users.router, prefix="/api/v1/users")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
