# fastapi-armor

<p align="center">
  <img src="https://github.com/inanpy/fastapi-armor/blob/main/assets/fastapi-armor.png" alt="fastapi-armor logo" width="600"/>
</p>

Secure your FastAPI apps with a single line of code 🛡️

`fastapi-armor` is a security middleware that sets modern HTTP security headers for every response. It provides presets for common configurations (`strict`, `relaxed`, `none`) and allows overrides for full customization.

---

## 🚀 Features

- 📦 Simple plug-and-play integration with FastAPI
- 🛡️ Protects your app with modern HTTP security headers
- ⚙️ Fully customizable settings
- 🧱 Built on top of Starlette and fully async

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
    preset="strict",  # apply secure default set
    permissions_policy="geolocation=(), microphone=()"  # optionally override specific header
)

@app.get("/")
async def read_root():
    return {"message": "FastAPI with Armor Middleware is running!"}
```

---

## 🎛️ Available Presets

You can use built-in presets to quickly apply a set of secure headers. These presets are designed for different use cases:

| Preset | Description |
|--------|-------------|
| `strict` | Applies all recommended security headers with strict values for maximum protection. |
| `relaxed` | Applies a lighter set of headers suitable for more flexible or development environments. |
| `none` | Disables all headers. Useful for debugging or local development where security is not a concern. |

You can also override any individual header even when using a preset:

```python
app.add_middleware(
    ArmorMiddleware,
    preset="strict",
    permissions_policy="geolocation=(), microphone=()"
)
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

---

## 🧩 Header Parameter Mapping

| Middleware Parameter | Header Set | Example Value |
|----------------------|------------|---------------|
| `content_security_policy` | `Content-Security-Policy` | `"default-src 'self'; img-src *;"` |
| `frame_options` | `X-Frame-Options` | `"DENY"` or `"SAMEORIGIN"` |
| `hsts` | `Strict-Transport-Security` | `"max-age=63072000; includeSubDomains; preload"` |
| `x_content_type_options` | `X-Content-Type-Options` | `"nosniff"` |
| `referrer_policy` | `Referrer-Policy` | `"no-referrer"` or `"strict-origin"` |
| `permissions_policy` | `Permissions-Policy` | `"geolocation=(), microphone=()"` |
| `dns_prefetch_control` | `X-DNS-Prefetch-Control` | `"off"` or `"on"` |
| `expect_ct` | `Expect-CT` | `"max-age=86400, enforce"` |
| `origin_agent_cluster` | `Origin-Agent-Cluster` | `"?1"` or `"?0"` |
| `cross_origin_embedder_policy` | `Cross-Origin-Embedder-Policy` | `"require-corp"` |
| `cross_origin_opener_policy` | `Cross-Origin-Opener-Policy` | `"same-origin"` or `"unsafe-none"` |
| `cross_origin_resource_policy` | `Cross-Origin-Resource-Policy` | `"same-origin"`, `"same-site"`, or `"cross-origin"` |

---



## 📚 Standards References

For more details on these headers and their standard definitions, refer to the following official resources:

- [MDN Web Docs: HTTP Headers Reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)
- [RFC 7231: Hypertext Transfer Protocol (HTTP/1.1)](https://tools.ietf.org/html/rfc7231)
- [IETF RFC Index](https://www.rfc-editor.org/search/rfc_search_detail.php?title=header&pubstatus%5B%5D=Any&stream_name=Any&sortkey=Number&sortorder=Ascending)

These are part of widely accepted standards and best practices in modern web application security.

---

## 📄 License

This project is licensed under the MIT License.
© 2025 Inan Delibas
