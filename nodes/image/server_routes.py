"""
Server routes pour SmartImageLoader
À ajouter dans __init__.py ou dans un fichier séparé importé par __init__.py
"""
import server
import os
import secrets
import tempfile
import ipaddress
from aiohttp import web

# --- Token secret généré au démarrage du serveur ---------------------------
TOO_ACCESS_TOKEN = secrets.token_hex(32)
_TOKEN_FILE = os.path.join(tempfile.gettempdir(), "too_pack_access_token.txt")
try:
    with open(_TOKEN_FILE, "w") as f:
        f.write(TOO_ACCESS_TOKEN)
    os.chmod(_TOKEN_FILE, 0o600)
except OSError:
    pass  # pas bloquant : le token reste utilisable via la variable en mémoire

print(f"TOO-Pack: token d'accès généré, disponible dans {_TOKEN_FILE}")


def strip_path(path):
    """Retire les guillemets et espaces"""
    path = path.strip()
    if path.startswith('"') and path.endswith('"'):
        path = path[1:-1]
    return path


def is_safe_path(path):
    """Vérifie que le chemin est sûr (pas de ..)"""
    try:
        abs_path = os.path.abspath(path)
        # Vérifier qu'on ne remonte pas dans l'arborescence
        return os.path.exists(abs_path)
    except:
        return False


def _get_client_ip(request):
    """Récupère l'IP réelle du pair TCP (pas les headers, spoofables)."""
    peername = request.transport.get_extra_info("peername") if request.transport else None
    if peername:
        # peername est un tuple (ip, port, ...) pour IPv4/IPv6
        return peername[0]
    return request.remote


def _is_localhost(ip):
    if not ip:
        return False
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return addr.is_loopback


def check_local_and_token(request):
    """
    Vérifie que la requête vient de localhost ET porte le bon token.
    Retourne une web.Response(403) si refusé, None si autorisé.
    """
    client_ip = _get_client_ip(request)
    if not _is_localhost(client_ip):
        return web.Response(status=403, text="Forbidden: localhost only")

    query = request.rel_url.query
    provided_token = request.headers.get("X-TOO-Token") or query.get("token")
    if not provided_token or not secrets.compare_digest(provided_token, TOO_ACCESS_TOKEN):
        return web.Response(status=403, text="Forbidden: invalid or missing token")

    return None


@server.PromptServer.instance.routes.get("/too/view/token")
async def get_access_token(request):
    """
    Distribue le token au frontend. Réservé à localhost uniquement
    (pas de check de token ici, sinon problème de l'oeuf et la poule).
    Comme le frontend tourne dans le navigateur local qui a de toute façon
    accès au filesystem local via ComfyUI, ça n'ouvre rien de nouveau.
    """
    client_ip = _get_client_ip(request)
    if not _is_localhost(client_ip):
        return web.Response(status=403, text="Forbidden: localhost only")
    return web.json_response({"token": TOO_ACCESS_TOKEN})


@server.PromptServer.instance.routes.get("/too/view/image")
async def view_image(request):
    """Route pour afficher les images avec type=path"""
    auth_error = check_local_and_token(request)
    if auth_error is not None:
        return auth_error

    query = request.rel_url.query

    if "filename" not in query:
        return web.Response(status=400, text="Missing filename parameter")

    filename = query["filename"]
    file_type = query.get("type", "output")

    if file_type == "path":
        # Chemin absolu - cas spécial
        filepath = strip_path(filename)

        if not is_safe_path(filepath):
            return web.Response(status=403, text="Invalid or unsafe path")

        if not os.path.isfile(filepath):
            return web.Response(status=404, text="File not found")

        # Retourner le fichier
        return web.FileResponse(filepath)

    else:
        # Utiliser la route standard de ComfyUI
        return web.Response(status=400, text="Only type=path is supported")


print("TOO-Pack: Custom image view route registered at /too/view/image (localhost + token required)")
