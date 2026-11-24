# Reading HTTP traffic: DevTools, HTTP Toolkit, mitmproxy

The page you see is only part of what the server sends. A tester who reads the traffic between the browser (or a phone) and the API finds what the UI hides:
- fields the page never shows;
- data that belongs to someone else;
- a price the client is trusted with;
- an error the page swallows.

This guide shows four tools, from the one you already have to the ones that also work for a phone.

**Practice ground.** BooKing Lab has a page for this: **UI lab → Sniffer** (`/lab/sniffer`, sign in first). It has six small exercises, and each hides your personal code somewhere in the traffic. Chrome DevTools is enough for all six. Answers are checked on the course site only; on the local copy the exercises work but checking says it is unavailable.

**Two URL switches help too** (they stay on for the browser tab until you open `?chaos=off`):
- `?chaos=slow`: lists load in 1–3 s, so you can watch skeletons and requests in flight.
- `?chaos=error`: the hotel search answers 503, so you can see how the page handles a server error without any proxy.

> Only ever intercept traffic of apps you are allowed to test: your own, a training app like this one, or with written permission.

## 1. Chrome DevTools

Open DevTools (`F12`, or `Cmd+Option+I` on macOS) and go to the **Network** panel.

| Task | How |
| --- | --- |
| See every request | Reload with Network open. Filter by **Fetch/XHR** to see only API calls. Type `api/v1` in the filter box. |
| Read a request | Click it: **Headers** (URL, method, status, request and response headers), **Payload** (query string and JSON body), **Preview** / **Response** (the body), **Cookies**, **Timing**. |
| Keep requests across page loads and redirects | Tick **Preserve log**. Without it the list is cleared on every navigation. |
| Slow network | The throttling menu (**No throttling** → **Slow 4G**, **3G**, or a custom profile). Click a submit button twice on a slow network: does the page send two requests? |
| Offline | Throttling → **Offline**. What does the page say when the API cannot be reached? |
| Block one request | Right-click a request → **Block request URL** (or **Block request domain**). Reload and see how the page copes. Turn it off in the **Request blocking** drawer. |
| Replay a request outside the browser | Right-click → **Copy** → **Copy as cURL** (or **Copy as fetch**). Paste into a terminal, Postman (**Import → Raw text**) or the Console, change a value, send it again. |
| Change a response | Right-click a response → **Override content**. Pick a folder for overrides once and allow access. Edit the JSON, save, reload: the page now gets your version. **Override headers** does the same for response headers. Remove overrides in **Sources → Overrides** when you are done. |
| Find a value anywhere | `Ctrl+F` / `Cmd+F` inside the Network panel searches all headers and bodies. |
| Cookies and storage | **Application** panel → **Cookies**, **Local storage**, **Session storage**. Cookies marked **HttpOnly** are invisible to page scripts (`document.cookie`) but visible here. |

**Useful habits:**
- Compare what the page shows with what the response carries.
- Compare the request the UI sends with what the API documentation (`/docs`) says it needs.
- Every response has an `X-Request-Id` header: put it in your bug reports.

## 2. HTTP Toolkit (desktop)

[HTTP Toolkit](https://httptoolkit.com) is a free, open-source proxy with a friendly UI. It is the easiest way to *change* traffic on the fly, not just read it.

1. Install it and start it.
2. **Intercept → Chrome** (or Fresh Chrome). A separate Chrome window opens, already set up to trust HTTP Toolkit. Open BooKing Lab in that window.
3. **View** shows every request with headers and bodies.
4. **Modify** lets you add rules:
   - pause a request before it is sent (a *breakpoint*), edit its body or headers, then let it go;
   - pause a response and edit it before the page gets it;
   - always answer a URL with a status of your choice, for example 503 for `/api/v1/hotels`.

Ideas to try:
- Pause `POST /api/v1/bookings`, change a value in the body and resume. Then check what the server stored with `GET /bookings/{id}`.
- Make the search answer 500 or 503, or answer it slowly, and watch the page.
- Remove a field from a response and see whether the page breaks.

## 3. A phone over Wi-Fi

Use this to test the website, or a mobile app, on a real phone. The computer runs the proxy; the phone sends its traffic through it.

1. **Same network.** The phone and the computer must be on the same Wi-Fi. Find the computer's local IP address (macOS: **System Settings → Wi-Fi → Details**; Windows: `ipconfig`). It looks like `192.168.1.23`.
2. **Start the proxy on the computer.**
   - In HTTP Toolkit, choose **Android device via QR code** (Android). For iOS, use **Anything → Manual setup**: it shows the port, usually `8000`.
   - In mitmproxy, run `mitmweb`: it listens on port `8080`.
   - Allow incoming connections if the firewall asks.
3. **Set the proxy on the phone.**
   - **Android:** Settings → Network & internet → Wi-Fi → your network → edit (pencil) → Advanced → Proxy → **Manual**. Enter the computer's IP as the host and the proxy port. Save.
   - **iOS:** Settings → Wi-Fi → (i) next to your network → **Configure Proxy** → **Manual**. Enter the server (the computer's IP) and the port. Save.
4. **Install the proxy's CA certificate** so the phone trusts HTTPS through the proxy.
   - Open `http://mitm.it` in the phone's browser (mitmproxy), or follow HTTP Toolkit's instructions for your device.
   - **Android:**
     1. Download the certificate.
     2. Install it: Settings → Security → Encryption & credentials → **Install a certificate → CA certificate**.
     3. Android warns you; confirm.
   - Android apps you did not build ignore user certificates since Android 7; Chrome on the phone still works. For your own app, its developers can allow user certificates in a debug build (`network_security_config`).
   - **iOS:**
     1. Download the profile.
     2. Install it: Settings → **Profile Downloaded** → Install.
     3. **Also trust it:** Settings → General → About → **Certificate Trust Settings** → turn on full trust for the proxy's certificate. Without this step HTTPS still fails.
5. Open BooKing Lab on the phone. Requests appear on the computer.

**After the course, undo everything.** A trusted proxy certificate lets whoever holds its key read the phone's HTTPS traffic.
- Proxy: set it back to **Off** (iOS) or **None** (Android).
- Certificate on Android: Settings → Security → Encryption & credentials → **User credentials** → remove it.
- Certificate on iOS: Settings → General → **VPN & Device Management** → the profile → **Remove Profile**.

## 4. mitmproxy (free, scriptable)

[mitmproxy](https://mitmproxy.org) is free and open source and comes with three front ends:
- `mitmproxy`, in the terminal;
- `mitmweb`, in the browser;
- `mitmdump`, for scripts.

```bash
pip install mitmproxy        # or: brew install mitmproxy
mitmweb                      # proxy on :8080, UI on http://127.0.0.1:8081
```

Point a browser at it:
- Start Chrome with `--proxy-server=127.0.0.1:8080`, or set the system proxy.
- Install the certificate from `http://mitm.it`, the same way as on the phone.

In `mitmweb`:
- **Intercept** pauses matching flows. For example, `~u /api/v1/bookings & ~m POST` pauses new bookings.
- Edit a paused flow, then **Resume**.
- **Replay** sends a request again.

A script makes a change repeatable:

```python
# slow_search.py — run with: mitmdump -s slow_search.py
from mitmproxy import http

def response(flow: http.HTTPFlow) -> None:
    if flow.request.path.startswith("/api/v1/hotels") and flow.request.method == "GET":
        flow.response.status_code = 503
        flow.response.text = '{"error":"service_unavailable","message":"Down","details":[],"request_id":"mitm"}'
```

## What to look for

- **What the UI hides:**
  - fields in a response the page never shows;
  - other users' personal data;
  - internal values that belong to the business, not to the client.
- **What the client controls:**
  - values in a request body or query that the server should compute or check itself: prices, totals, ids of other users' objects, roles;
  - change them and see whether the server notices.
- **What happens when things go wrong:** a 5xx, a timeout or no network. Does the page show an error and a way to retry, or nothing at all?
- **Repeated requests:** a double click on a slow network, or a replayed request. Does the server create the same thing twice? Look for an `Idempotency-Key` header.
- **Headers and cookies:** cache headers on private data, cookies without `HttpOnly` or `Secure`, tokens in URLs.

Write each finding as a bug report with the request and response as evidence: copy as cURL, or attach the HAR file (Network → **Export HAR**). Remove tokens and passwords from what you attach.
