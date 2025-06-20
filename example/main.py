from fastapi import FastAPI
from fastapi_armor.middleware import ArmorMiddleware

app = FastAPI()

app.add_middleware(
    ArmorMiddleware,
    content_security_policy="default-src 'self'; img-src *;",
    frame_options="DENY",
    hsts="max-age=31536000; includeSubDomains",
    x_content_type_options="nosniff",
    referrer_policy="strict-origin-when-cross-origin",
    permissions_policy="geolocation=(), microphone=()",
    dns_prefetch_control="off",
    expect_ct="max-age=86400, enforce",
    origin_agent_cluster="?1",
    cross_origin_embedder_policy="require-corp",
    cross_origin_opener_policy="same-origin",
    cross_origin_resource_policy="same-origin",
)


@app.get("/")
async def read_root():
    return {"message": "FastAPI with Armor Middleware is running!"}
