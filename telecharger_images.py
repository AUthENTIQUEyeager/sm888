#!/usr/bin/env python3
"""
Télécharge automatiquement les photos du site (diaporama et en-têtes, or, engins, équipements,
céréales) et les enregistre dans assets/img/ sous le nom attendu par le site : chaque image
apparaît automatiquement à la bonne place.

Source : Wikimedia Commons, uniquement des photos sous licence libre. Les crédits sont écrits
dans js/credits.js et affichés sur credits.html.

Utilisation (internet nécessaire ; sur Mac : python3) :
    python3 -m pip install pillow
    python3 telecharger_images.py              -> toutes les images
    python3 telecharger_images.py hero mil     -> seulement celles dont le nom commence ainsi
"""
import html, io, json, os, re, sys, time, urllib.parse, urllib.request

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow est requis : tapez  python3 -m pip install pillow  puis relancez ce script.")

# Wikimedia demande un contact dans le User-Agent : mettez votre vraie adresse e-mail.
CONTACT = "contact@exemple.com"
UA = "SM888-site-images/1.0 (%s)" % CONTACT

CARTE = (800, 600, 80)    # largeur, hauteur, poids maximum en Ko (cartes produits)
HERO = (1600, 900, 120)   # images d'en-tête et diaporama

# nom du fichier (sans .webp) : (libellé pour les crédits, format, recherches essayées dans l'ordre)
# Pour changer une image, modifiez ses mots-clés (en anglais : plus précis) et relancez pour elle seule.
MACHINES = {
    "hero-accueil-1": ("Diaporama accueil : or", HERO, ["gold nuggets", "native gold", "gold dust"]),
    "hero-accueil-2": ("Diaporama accueil : engins", HERO, ["open pit mine machinery", "mining haul truck", "mining excavator"]),
    "hero-accueil-3": ("Diaporama accueil : céréales", HERO, ["millet field Africa", "sorghum field", "millet harvest"]),
    "hero-or": ("En-tête page Or", HERO, ["gold bars", "gold bullion", "gold ingots"]),
    "hero-engins": ("En-tête page Engins", HERO, ["bulldozer construction site", "hydraulic excavator working", "quarry machinery"]),
    "hero-cereales": ("En-tête page Céréales", HERO, ["sorghum harvest", "grain field Burkina Faso", "cereal crop field Africa"]),
    "or-image": ("Photo d’or (page Or)", CARTE, ["gold nugget", "alluvial gold", "gold ore"]),
    "pelle-hydraulique": ("Pelle hydraulique", CARTE, ["hydraulic excavator", "crawler excavator"]),
    "chargeuse": ("Chargeuse", CARTE, ["wheel loader", "front end loader"]),
    "tombereau": ("Tombereau", CARTE, ["articulated dump truck", "mining haul truck", "dump truck"]),
    "bulldozer": ("Bulldozer", CARTE, ["bulldozer", "crawler dozer"]),
    "foreuse": ("Foreuse", CARTE, ["blast hole drill rig", "mining drill rig", "rotary drill rig"]),
    "camion-citerne": ("Camion-citerne", CARTE, ["water tanker truck", "tanker truck"]),
    "concasseur": ("Concasseur", CARTE, ["jaw crusher", "stone crusher"]),
    "broyeur": ("Broyeur", CARTE, ["ball mill grinding", "ball mill"]),
    "trommel": ("Trommel", CARTE, ["trommel screen", "rotary trommel"]),
    "table-vibrante": ("Table vibrante", CARTE, ["shaking table gold", "gravity concentration shaking table", "Wilfley table"]),
    "pompe-eau": ("Pompe à eau", CARTE, ["centrifugal water pump", "diesel water pump", "engine water pump"]),
    "batees-accessoires": ("Batées et accessoires", CARTE, ["gold pan", "gold panning"]),
    "mil": ("Mil", CARTE, ["pearl millet", "millet grain"]),
    "sorgho": ("Sorgho", CARTE, ["sorghum grain", "sorghum panicle"]),
    "mais": ("Maïs", CARTE, ["maize cobs", "corn kernels"]),
    "riz": ("Riz", CARTE, ["paddy rice", "rice grain"]),
    "fonio": ("Fonio", CARTE, ["fonio", "Digitaria exilis"]),
}
LICENCES_OK = re.compile(r"^(CC0|CC BY \d|CC BY-SA \d|Public domain|PD)", re.I)
MOTS_EXCLUS = re.compile(r"diagram|drawing|schema|scale model|toy|lego|logo|icon|\bmap\b|miniature|painting|accident|crash|burn|fire"
                         r"|bread|porridge|soup|salad|cake|beer|bowl|dish|plate|cooked|recipe|chocolate|jewel", re.I)


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


def chercher(q, fmt):
    p = {"action": "query", "format": "json", "generator": "search", "gsrsearch": q + " filetype:bitmap",
         "gsrnamespace": 6, "gsrlimit": 25, "prop": "imageinfo", "iiprop": "url|size|extmetadata",
         "iiurlwidth": min(2000, fmt[0] * 5 // 4)}
    d = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p))
    if not d:
        return []
    pages = json.loads(d).get("query", {}).get("pages", {}).values()
    return sorted(pages, key=lambda x: x.get("index", 0))  # ordre de pertinence


def choisir(pages, utilises, fmt):
    """Premier résultat pertinent : licence libre, assez grand, bon format, pas déjà utilisé."""
    hero = fmt[0] > 800
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
        if w < (1400 if hero else 800) or h < 500 or not (1.4 if hero else 1.1) <= w / h <= (2.4 if hero else 2.2):
            continue
        return {"titre": titre, "url": ii["thumburl"], "page": ii.get("descriptionurl", ""),
                "auteur": val("Artist") or "Auteur inconnu", "licence": lic}
    return None


def convertir(data, fmt):
    """Recadre au format voulu et enregistre en WebP léger (adapté à la 3G)."""
    im = ImageOps.exif_transpose(Image.open(io.BytesIO(data))).convert("RGB")
    im = ImageOps.fit(im, (fmt[0], fmt[1]), Image.LANCZOS, centering=(0.5, 0.5))
    for q in (78, 70, 62, 54, 46, 38):
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=q, method=6)
        if buf.tell() <= fmt[2] * 1024:
            break
    return buf.getvalue()


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    dossier = os.path.join(base, "assets", "img")
    os.makedirs(dossier, exist_ok=True)
    args = sys.argv[1:]
    noms = [n for n in MACHINES if not args or any(n.startswith(a) for a in args)]
    if not noms:
        sys.exit("Aucun nom ne correspond. Noms valides : " + ", ".join(MACHINES))
    fichier_credits, credits = os.path.join(base, "js", "credits.js"), {}
    try:  # on conserve les crédits des images non retraitées
        credits = json.loads(open(fichier_credits, encoding="utf-8").read().split("=", 1)[1].rstrip().rstrip(";"))
    except Exception:
        pass
    utilises = {c["titre"] for k, c in credits.items() if k not in noms}
    reussies = 0
    for nom in noms:
        label, fmt, requetes = MACHINES[nom]
        print("->", nom, end=" ... ", flush=True)
        choix = None
        for q in requetes:
            choix = choisir(chercher(q, fmt), utilises, fmt)
            time.sleep(1)
            if choix:
                break
        data = get(choix["url"]) if choix else None
        if not data:
            print("introuvable (image actuelle conservée)")
            continue
        try:
            octets = convertir(data, fmt)
        except Exception:
            print("image illisible (image actuelle conservée)")
            continue
        with open(os.path.join(dossier, nom + ".webp"), "wb") as f:
            f.write(octets)
        utilises.add(choix["titre"])
        choix["label"] = label
        credits[nom] = choix
        reussies += 1
        print("OK (%d Ko) - %s" % (len(octets) // 1024, choix["licence"]))
        time.sleep(1)
    with open(fichier_credits, "w", encoding="utf-8") as f:
        f.write("/* Généré par telecharger_images.py — ne pas modifier à la main. */\nwindow.CREDITS = "
                + json.dumps(credits, ensure_ascii=False, indent=1) + ";\n")
    if not reussies:
        print("Aucune image téléchargée : vérifiez la connexion internet (Mac : lancez « Install Certificates.command » du dossier Python).")
    print("Terminé : %d/%d images. Vérifiez index.html, or.html, engins.html, cereales.html et credits.html." % (reussies, len(noms)))


if __name__ == "__main__":
    main()
