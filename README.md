# SweetQR

A QR code generator (web + CLI) in English, with no backend: the QR is generated instantly in your browser.

## Web app

The whole app is static (HTML + JS + the `qrcodejs` library bundled in `vendor/`). It works with any static file server.

### Run locally

```bash
python3 server.py              # open http://127.0.0.1:8080
# or with zero installs:
python3 -m http.server 8080
```

### Features

- Live QR preview while you type.
- URL mode (auto-adds `https://` if missing) or free text.
- Error correction levels (L / M / Q / H).
- Custom background and QR colors, with a swap button.
- Adjustable size and high-res PNG download (1024 px).
- Copy the QR to the clipboard.
- `noindex` + `robots.txt` so search engines never index it.

### Live demo

The app is published for free on GitHub Pages:

**https://danielvaldess.github.io/sweetqr/**

## CLI (terminal)

```bash
python3 -m pip install qrcode pillow
python3 cli/sweetqr.py
```

Generated files are saved in `generados/`.

## Deploy with cloudflared

Inside the SweetCode network/VPN, on the server:

```bash
# 1) Clone or copy the project
git clone https://github.com/danielvaldess/sweetqr.git /opt/sweetqr
cd /opt/sweetqr

# 2) Serve the app on localhost only (port 8080)
nohup python3 server.py --host 127.0.0.1 --port 8080 &

# 3) cloudflared tunnel to localhost:8080 (named, no indexing)
cloudflared tunnel run --url http://127.0.0.1:8080
```

For a fixed, non-indexable hostname, use a named tunnel:

```bash
cloudflared tunnel create sweetqr
cloudflared tunnel route dns sweetqr sweetqr.sweetcode.studio
cloudflared tunnel run sweetqr
```

with a `config.yml` like:

```yaml
tunnel: sweetqr
credentials-file: /root/.cloudflared/<tunnel-id>.json
ingress:
  - hostname: sweetqr.sweetcode.studio
    service: http://127.0.0.1:8080
  - service: http_status:404
```

Only people with the link can use it; the HTML carries `noindex, nofollow`.

## Security & privacy

- No tracking, no analytics, no data leaves the browser. The QR is generated client-side.
- No external CDNs: the QR library is vendored locally (`vendor/`).
- The app binds to `127.0.0.1` by default; expose it only through a tunnel.

## Structure

```
sweetqr/
├── index.html        # graphical web app
├── server.py         # minimal static server
├── favicon.svg       # cherry favicon
├── robots.txt        # blocks search engines
├── vendor/
│   ├── qrcode.min.js # QR library (qrcodejs, MIT)
│   └── LICENSE       # qrcodejs license
└── cli/
    └── sweetqr.py    # terminal version
```

Made with ♥ at SweetCode.