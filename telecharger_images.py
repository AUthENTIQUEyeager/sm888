#!/usr/bin/env python3
"""
Télécharge automatiquement une photo de chaque engin / équipement et l'enregistre
dans assets/img/ sous le nom attendu par le site : la bonne image apparaît alors
automatiquement à la bonne place (aucune modification du site nécessaire).

Source : Wikimedia Commons, uniquement des photos sous licence libre (Creative Commons
ou domaine public). Les crédits sont écrits dans js/credits.js et affichés sur credits.html.

Utilisation (internet nécessaire) :
    pip install pillow
    python telecharger_images.py                  -> toutes les machines
    python telecharger_images.py bulldozer foreuse -> seulement celles-ci
"""
import html, io, json, os, re, sys, time, urllib.parse, urllib.request

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow est requis : tapez  pip install pillow  puis relancez ce script.")

# Wikimedia demande un contact dans le User-Agent : mettez votre vraie adresse e-mail.
CONTACT = "contact@exemple.com"
UA = "SM888-site-images/1.0 (%s)" % CONTACT

# nom du fichier (sans .webp) -> recherches essayées dans l'ordre (en anglais : plus précis sur Commons)
# Pour changer le type d'image d'une machine, modifiez simplement ses mots-clés ici.
MACHINES = {
    "pelle-hydraulique": ["hydraulic excavator", "crawler excavator"],
    "chargeuse": ["wheel loader", "front end loader"],
    "tombereau": ["articulated dump truck", "mining haul truck", "dump truck"],
    "bulldozer": ["bulldozer", "crawler dozer"],
    "foreuse": ["blast hole drill rig", "mining drill rig", "rotary drill rig"],
    "camion-citerne": ["water tanker truck", "tanker truck"],
    "concasseur": ["jaw crusher", "stone crusher"],
    "broyeur": ["ball mill grinding", "ball mill"],
    "trommel": ["trommel screen", "rotary trommel"],
    "table-vibrante": ["shaking table gold", "gravity concentration shaking table", "Wilfley table"],
    "pompe-eau": ["centrifugal water pump", "diesel water pump", "engine water pump"],
    "batees-accessoires": ["gold pan", "gold panning"],
}
LICENCES_OK = re.compile(r"^(CC0|CC BY \d|CC BY-SA \d|Public domain|PD)", re.I)
MOTS_EXCLUS = re.compile(r"diagram|drawing|schema|scale model|toy|lego|logo|icon|\bmap\b|miniature|painting|accident|crash|burn|fire", re.I)


def get(url):
    """Télécharge une URL (3 essais, pauses croissantes)."""
    for t in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except Exception:
            time.sleep(2 * (t + 1))
    return None


def chercher(q):
    p = {"action": "query", "format": "json", "generator": "search", "gsrsearch": q + " filetype:bitmap",
         "gsrnamespace": 6, "gsrlimit": 25, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 1000}
    d = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p))
    if not d:
        return []
    pages = json.loads(d).get("query", {}).get("pages", {}).values()
    return sorted(pages, key=lambda x: x.get("index", 0))  # ordre de pertinence


def choisir(pages, utilises):
    """Premier résultat pertinent : licence libre, assez grand, format paysage, pas déjà utilisé."""
    for pg in pages:
        if "imageinfo" not in pg:
            continue
        ii = pg["imageinfo"][0]
        m = ii.get("extmetadata", {})
        val = lambda k: html.unescape(re.sub(r"<[^>]+>", "", m.get(k, {}).get("value", ""))).strip()
        titre, lic, w, h = pg.get("title", ""), val("LicenseShortName"), ii.get("width", 0), ii.get("height", 0)
        if titre in utilises or not LICENCES_OK.match(lic) or MOTS_EXCLUS.search(titre):
            continue
        if val("NonFree").lower() in ("true", "1", "yes") or not ii.get("thumburl"):
            continue
        if w < 800 or h < 500 or not 1.1 <= w / h <= 2.2:
            continue
        return {"titre": titre, "url": ii["thumburl"], "page": ii.get("descriptionurl", ""),
                "auteur": val("Artist") or "Auteur inconnu", "licence": lic}
    return None


def convertir(data):
    """Recadre en 800 × 600 et enregistre en WebP de moins de 80 Ko (léger pour la 3G)."""
    im = ImageOps.exif_transpose(Image.open(io.BytesIO(data))).convert("RGB")
    im = ImageOps.fit(im, (800, 600), Image.LANCZOS, centering=(0.5, 0.5))
    for q in (78, 70, 62, 54, 46):
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=q, method=6)
        if buf.tell() <= 80 * 1024:
            break
    return buf.getvalue()


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    dossier = os.path.join(base, "assets", "img")
    os.makedirs(dossier, exist_ok=True)
    noms = sys.argv[1:] or list(MACHINES)
    inconnus = [n for n in noms if n not in MACHINES]
    if inconnus:
        sys.exit("Nom inconnu : %s\nNoms valides : %s" % (", ".join(inconnus), ", ".join(MACHINES)))
    fichier_credits, credits = os.path.join(base, "js", "credits.js"), {}
    try:  # on conserve les crédits des machines non retraitées
        credits = json.loads(open(fichier_credits, encoding="utf-8").read().split("=", 1)[1].rstrip().rstrip(";"))
    except Exception:
        pass
    utilises = {c["titre"] for k, c in credits.items() if k not in noms}
    for nom in noms:
        print("->", nom, end=" ... ", flush=True)
        choix = None
        for q in MACHINES[nom]:
            choix = choisir(chercher(q), utilises)
            time.sleep(1)
            if choix:
                break
        data = get(choix["url"]) if choix else None
        if not data:
            print("introuvable (image actuelle conservée)")
            continue
        try:
            octets = convertir(data)
        except Exception:
            print("image illisible (image actuelle conservée)")
            continue
        with open(os.path.join(dossier, nom + ".webp"), "wb") as f:
            f.write(octets)
        utilises.add(choix["titre"])
        credits[nom] = choix
        print("OK (%d Ko) - %s" % (len(octets) // 1024, choix["licence"]))
        time.sleep(1)
    with open(fichier_credits, "w", encoding="utf-8") as f:
        f.write("/* Généré par telecharger_images.py — ne pas modifier à la main. */\nwindow.CREDITS = "
                + json.dumps(credits, ensure_ascii=False, indent=1) + ";\n")
    print("Terminé. Vérifiez le résultat en ouvrant engins.html et credits.html.")


if __name__ == "__main__":
    main()
