#!/usr/bin/env python3
"""Télécharge les photos libres des produits agricoles et des noix de SM888."""
import json
import os
import sys
import time

from telecharger_images import CARTE, HERO, chercher, choisir, convertir, get

# Libellé de crédit, format, recherches Wikimedia Commons (du plus précis au plus large).
IMAGES = {
    "hero-produits-agricoles": ("En-tête Produits agricoles", HERO, ["agriculture harvest Burkina Faso", "West African grain harvest", "African agriculture field"]),
    "hero-noix": ("En-tête Noix", HERO, ["shea nuts Burkina Faso", "cashew nuts West Africa", "shea fruit harvest"]),
    "mil": ("Mil", CARTE, ["pearl millet grain", "millet grain"]),
    "sorgho": ("Sorgho", CARTE, ["sorghum grain", "sorghum panicle"]),
    "mais": ("Maïs", CARTE, ["maize kernels", "corn cobs"]),
    "riz": ("Riz", CARTE, ["paddy rice grain", "rice grains"]),
    "fonio": ("Fonio", CARTE, ["fonio grain Digitaria exilis", "fonio grain"]),
    "arachide": ("Arachide", CARTE, ["peanuts in shell", "groundnuts harvest"]),
    "soja": ("Soja", CARTE, ["soybean pods", "soybean seeds"]),
    "sesame": ("Sésame", CARTE, ["sesame seeds", "sesame plant seeds"]),
    "anacarde": ("Anacarde", CARTE, ["cashew nuts in shell", "cashew apple fruit"]),
    "noix-karite": ("Noix de karité", CARTE, ["shea nuts seeds", "shea fruit nuts"]),
    "noix-cajou": ("Noix de cajou", CARTE, ["cashew nuts raw", "cashew nuts in shell"]),
    "noix-coco": ("Noix de coco", CARTE, ["coconut whole fruit", "coconut fruit"]),
    "noix-palmiste": ("Noix de palmiste", CARTE, ["palm kernel nuts", "oil palm fruit"]),
}


def charger_credits(path):
    """Lit les crédits existants pour conserver ceux des images non modifiées."""
    with open(path, encoding="utf-8") as fichier:
        contenu = fichier.read()
    _, separateur, donnees = contenu.partition("=")
    if not separateur:
        raise ValueError("Format invalide dans js/credits.js")
    return json.loads(donnees.strip().removesuffix(";"))


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    dossier_images = os.path.join(base, "assets", "img")
    os.makedirs(dossier_images, exist_ok=True)

    demandes = sys.argv[1:]
    noms = [nom for nom in IMAGES if not demandes or any(nom.startswith(demande) for demande in demandes)]
    if not noms:
        sys.exit("Aucun nom ne correspond. Noms valides : " + ", ".join(IMAGES))

    fichier_credits = os.path.join(base, "js", "credits.js")
    credits = charger_credits(fichier_credits)
    utilises = {credit["titre"] for nom, credit in credits.items() if nom not in noms}
    reussies = 0

    for nom in noms:
        label, format_image, recherches = IMAGES[nom]
        print("->", nom, end=" ... ", flush=True)
        choix = None
        for recherche in recherches:
            choix = choisir(chercher(recherche, format_image), utilises, format_image)
            time.sleep(1)
            if choix:
                break

        donnees = get(choix["url"]) if choix else None
        if not donnees:
            print("image introuvable ou téléchargement impossible (fichier actuel conservé)")
            continue
        try:
            octets = convertir(donnees, format_image)
        except Exception as erreur:
            print("conversion impossible : %s (fichier actuel conservé)" % erreur)
            continue

        with open(os.path.join(dossier_images, nom + ".webp"), "wb") as fichier:
            fichier.write(octets)
        utilises.add(choix["titre"])
        choix["label"] = label
        credits[nom] = choix
        reussies += 1
        print("OK (%d Ko) - %s" % (len(octets) // 1024, choix["licence"]))
        time.sleep(1)

    with open(fichier_credits, "w", encoding="utf-8") as fichier:
        fichier.write("/* Généré par telecharger_images_agricoles.py — ne pas modifier à la main. */\n"
                      "window.CREDITS = " + json.dumps(credits, ensure_ascii=False, indent=1) + ";\n")

    if not reussies:
        print("Aucune image téléchargée : vérifiez la connexion internet et le certificat SSL de Python.")
    print("Terminé : %d/%d images." % (reussies, len(noms)))


if __name__ == "__main__":
    main()
