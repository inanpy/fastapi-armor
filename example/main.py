from fastapi import FastAPI
from fastapi_armor.middleware import ArmorMiddleware

app = FastAPI()

app.add_middleware(
    ArmorMiddleware,
    preset="strict",
    permissions_policy="geolocation=(), microphone=()",  # override example
)


@app.get("/")
async def read_root():
    return {"message": "FastAPI with Armor Middleware is running!"}
