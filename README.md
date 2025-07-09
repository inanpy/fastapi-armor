<p align="center">
  <img src="https://raw.githubusercontent.com/inanpy/fastapi-armor/main/assets/fastapi-armor.png" alt="fastapi-armor logo" width="600"/>
</p>

<p align="center">
Secure your FastAPI apps with a single line of code 🛡️
</p>

`fastapi-armor` is a security middleware that sets modern HTTP security headers for every response. It provides presets for common configurations (`strict`, `relaxed`, `none`) and allows overrides for full customization.

---
<p align="center">
<a href="https://pypi.org/project/fastapi-armor/"><img src="https://img.shields.io/pypi/v/fastapi-armor?color=blue" alt="PyPI version"></a>
<a href="https://pepy.tech/project/fastapi-armor">
  <img src="https://static.pepy.tech/badge/fastapi-armor" alt="Total downloads">
</a>

</p>

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

## 🦩 Header Parameter Mapping

This table shows how to customize headers in the middleware by mapping FastAPI-Armor's parameter names to actual HTTP header fields:

| Middleware Parameter | Header Set | Example Value |
|----------------------|------------|--------------|
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

Use these parameter names when configuring the middleware. For example, `permissions_policy="geolocation=()"` will set the `Permissions-Policy` HTTP header.

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



## 📚 Standards References

For more details on these headers and their standard definitions, refer to the following official resources:

### Official Standards & Specifications

- [W3C: Content Security Policy Level 3](https://www.w3.org/TR/CSP3/) - The official W3C specification for CSP
- [RFC 6797: HTTP Strict Transport Security](https://datatracker.ietf.org/doc/html/rfc6797) - IETF standard for HSTS
- [RFC 7034: HTTP Header Field X-Frame-Options](https://datatracker.ietf.org/doc/html/rfc7034) - Official IETF specification
- [Permissions Policy Specification](https://w3c.github.io/webappsec-permissions-policy/) - W3C specification
- [Fetch Metadata Request Headers](https://www.w3.org/TR/fetch-metadata/) - W3C document on Cross-Origin headers

### Security Organizations & Best Practices

- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/) - Comprehensive guide by the Open Web Application Security Project
- [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security) - Mozilla's authoritative security recommendations
- [NIST SP 800-95: Guide to Secure Web Services](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-95.pdf) - National Institute of Standards and Technology official guidance

### Documentation & Practical Implementation

- [MDN Web Docs: HTTP Security Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers#security) - Detailed documentation on security headers
- [Content Security Policy Quick Reference Guide](https://content-security-policy.com/) - Comprehensive reference for CSP directives and implementation

These resources represent officially accepted standards, specifications, and industry best practices for implementing security headers in modern web applications.

---

## 👥 Contributors

Special thanks to the following contributors who have helped improve this project:

- [Stéphane Brunner](https://github.com/sbrunner) - Enhanced middleware to skip headers when parameter is None

If you'd like to contribute, please feel free to submit a pull request!

---

## 📄 License

This project is licensed under the MIT License.
© 2025 Inan Delibas
