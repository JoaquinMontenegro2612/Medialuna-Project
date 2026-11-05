#!/usr/bin/env python3
"""Servidor estático del plan de trabajo.

Uso:  python3 tools/serve.py [puerto]     (por defecto 8080, escucha en 0.0.0.0)

Diferencias con `python3 -m http.server`, y por qué:
  - Los .md se sirven como texto plano UTF-8, así se abren en el navegador en vez
    de descargarse (los botones "Leer" de index.html apuntan a ellos).
  - Los .csv se sirven como texto plano, por el mismo motivo.
  - Sin caché agresiva: al editar un archivo y recargar, se ve el cambio.
  - Escucha en 0.0.0.0 para que funcione detrás del proxy del preview.
"""
import os
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OVERLOADS = {
    ".md": "text/plain; charset=utf-8",
    ".csv": "text/plain; charset=utf-8",
}


class Handler(SimpleHTTPRequestHandler):
    def guess_type(self, path):
        ext = os.path.splitext(str(path))[1].lower()
        if ext in OVERLOADS and not str(path).endswith((".html", ".htm")):
            return OVERLOADS[ext]
        return super().guess_type(path)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    handler = partial(Handler, directory=ROOT)
    with ThreadingHTTPServer(("0.0.0.0", port), handler) as httpd:
        print(f"Sirviendo {ROOT} en http://0.0.0.0:{port}", flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
