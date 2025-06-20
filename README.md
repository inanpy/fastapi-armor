# fastapi-armor

`fastapi-armor` is a lightweight, production-ready middleware for FastAPI that automatically adds secure HTTP headers to every response. It helps protect your application from common web vulnerabilities like XSS, clickjacking, insecure content loading, and more — all with a single line of middleware configuration.

---

## 🚀 Features

- 📦 Simple plug-and-play integration with FastAPI
- 🛡️ Protects your app with modern HTTP security headers
- ⚙️ Fully customizable settings
- 🧱 Built on top of Starlette and fully async
- 🧩 Inspired by Helmet.js (Node.js) and Django SecurityMiddleware

---

## 🛡️ Included Headers & Their Purpose

By default or optionally, `ArmorMiddleware` can apply the following headers:

| Header | Description |
|--------|-------------|
| `Content-Security-Policy` | Mitigates XSS and data injection attacks by specifying allowed content sources. |
| `X-Frame-Options` | Prevents clickjacking by disallowing rendering inside `<iframe>`. |
| `Strict-Transport-Security` | Forces use of HTTPS for future requests, helping prevent man-in-the-middle attacks. |
| `X-Content-Type-Options` | Disables MIME-type sniffing to avoid content-type confusion. |
| `Referrer-Policy` | Controls the `Referer` header sent in requests — reduces accidental info leakage. |
| `Permissions-Policy` | Limits access to browser APIs like geolocation, camera, microphone, etc. |
| `X-DNS-Prefetch-Control` | Prevents browsers from resolving DNS of external domains before user interaction. |
| `Expect-CT` | Ensures valid Certificate Transparency logs for HTTPS connections. |
| `Origin-Agent-Cluster` | Provides context isolation for enhanced privacy and safety. |
| `Cross-Origin-Embedder-Policy (COEP)` | Blocks loading resources unless they explicitly allow being embedded. |
| `Cross-Origin-Opener-Policy (COOP)` | Helps isolate browsing contexts to prevent cross-window attacks. |
| `Cross-Origin-Resource-Policy (CORP)` | Restricts which origins can load resources from your site. |

> All headers are optional and fully configurable at the middleware level.

---

## 📦 Installation

Install via pip:

```bash
pip install fastapi-armor
```

---

## ⚙️ Usage Example

Here’s how to use `ArmorMiddleware` in a FastAPI application:

```python
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
    cross_origin_resource_policy="same-origin"
)

@app.get("/")
async def read_root():
    return {"message": "FastAPI with Armor Middleware is running!"}
```

---

## ▶️ Running the App

To run this FastAPI app locally using `uvicorn`, first install the required packages:

```bash
pip install fastapi uvicorn
```

Then start the app:

```bash
uvicorn example.main:app --reload
```

Visit your app at [http://127.0.0.1:8000](http://127.0.0.1:8000)

You can inspect the HTTP headers in the browser or via curl:

```bash
curl -I http://127.0.0.1:8000
```

---

## 📄 License

This project is licensed under the MIT License.
© 2025 Inan Delibas
