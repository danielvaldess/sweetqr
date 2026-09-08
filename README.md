# SweetQR

Generador de códigos QR web y de terminal, en español. Sin servidor de por medio: el QR se genera al instante en tu navegador.

## Web app

Todo el código es estático (HTML + JS + la librería `qrcodejs` incluida en `vendor/`). Funciona con cualquier servidor de archivos.

### Probar en local

```bash
python3 server.py              # abre http://127.0.0.1:8080
# o sin instalar nada:
python3 -m http.server 8080
```

### Características

- Vista previa en vivo mientras escribes la URL.
- Modo URL (agrega `https://` solo) o texto libre.
- Niveles de corrección de error (L / M / Q / H).
- Colores de fondo y de QR personalizables, con botón para intercambiarlos.
- Tamaño ajustable y descarga en PNG de 1024 px.
- Copia el QR al portapapeles.
- `noindex` para que los buscadores no lo indexen.

## CLI (terminal)

```bash
python3 -m pip install qrcode pillow
python3 cli/sweetqr.py
```

Los archivos generados se guardan en `generados/`.

## Desplegar en SweetCode con cloudflared

Dentro de la red/VPN de SweetCode, en el servidor:

```bash
# 1) Clona o copia el proyecto
git clone https://github.com/TU_USUARIO/sweetqr.git /opt/sweetqr
cd /opt/sweetqr

# 2) Sirve la app solo en localhost (puerto 8080)
nohup python3 server.py --host 127.0.0.1 --port 8080 &

# 3) Túnel cloudflared hacia localhost:8080 (nombrado, sin indexación)
cloudflared tunnel run --url http://127.0.0.1:8080
```

Para un hostname fijo y no indexable, usa un túnel con nombre:

```bash
cloudflared tunnel create sweetqr
cloudflared tunnel route dns sweetqr sweetqr.sweetcode.studio
cloudflared tunnel run sweetqr
```

con un `config.yml` como:

```yaml
tunnel: sweetqr
credentials-file: /root/.cloudflared/<tunnel-id>.json
ingress:
  - hostname: sweetqr.sweetcode.studio
    service: http://127.0.0.1:8080
  - service: http_status:404
```

Solo quien tenga el enlace podrá usarla; el HTML lleva `noindex, nofollow`.

## Estructura

```
sweetqr/
├── index.html        # app web gráfica
├── server.py         # servidor estático simple
├── vendor/
│   └── qrcode.min.js # librería QR (qrcodejs)
└── cli/
    └── sweetqr.py    # versión terminal
```

Hecho con ♥ en SweetCode.