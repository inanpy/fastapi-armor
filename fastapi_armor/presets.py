PRESETS = {
    "strict": {
        "Content-Security-Policy": "default-src 'self';",
        "X-Frame-Options": "DENY",
        "Strict-Transport-Security": ("max-age=63072000; includeSubDomains; preload"),
        "X-Content-Type-Options": "nosniff",
        "Referrer-Policy": "no-referrer",
        "Permissions-Policy": "geolocation=(), microphone=()",
        "X-DNS-Prefetch-Control": "off",
        "Expect-CT": "max-age=86400, enforce",
        "Origin-Agent-Cluster": "?1",
        "Cross-Origin-Embedder-Policy": "require-corp",
        "Cross-Origin-Opener-Policy": "same-origin",
        "Cross-Origin-Resource-Policy": "same-origin",
    },
    "relaxed": {
        "Content-Security-Policy": "default-src *;",
        "X-Frame-Options": "SAMEORIGIN",
        "Strict-Transport-Security": "max-age=86400",
        "X-Content-Type-Options": "nosniff",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    },
    "none": {},
}
