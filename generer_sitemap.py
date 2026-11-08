#!/usr/bin/env python3
"""
Génère sitemap.xml et robots.txt à partir des pages .html présentes dans ce dossier,
avec VOTRE vrai nom de domaine. Utilisation :

    python3 generer_sitemap.py https://www.votre-domaine.com

À relancer chaque fois que vous ajoutez ou supprimez une page. Les pages marquées « noindex »
et les fichiers de vérification Google (google....html) sont ignorés.
"""
import datetime, html, os, sys, urllib.parse


def main():
    if len(sys.argv) != 2 or not sys.argv[1].startswith(("http://", "https://")):
        sys.exit("Utilisation : python3 generer_sitemap.py https://www.votre-domaine.com")
    base = sys.argv[1].rstrip("/")
    if "exemple.com" in base:
        sys.exit("Indiquez votre vrai nom de domaine (pas exemple.com).")
    dossier = os.path.dirname(os.path.abspath(__file__))
    pages = []
    for f in sorted(os.listdir(dossier)):
        if not f.endswith(".html") or f.startswith(("google", "404")):
            continue
        chemin = os.path.join(dossier, f)
        contenu = open(chemin, encoding="utf-8", errors="ignore").read().lower()
        if not contenu.strip() or "noindex" in contenu or 'http-equiv="refresh"' in contenu:
            continue  # page vide, exclue de Google ou simple redirection
        pages.append(f)
    pages.sort(key=lambda f: f != "index.html")  # l'accueil en premier
    lignes = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for f in pages:
        loc = base + "/" + ("" if f == "index.html" else urllib.parse.quote(f))
        date = datetime.date.fromtimestamp(os.path.getmtime(os.path.join(dossier, f))).isoformat()
        lignes.append("<url><loc>%s</loc><lastmod>%s</lastmod></url>" % (html.escape(loc), date))
    lignes.append("</urlset>")
    with open(os.path.join(dossier, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as s:
        s.write("\n".join(lignes) + "\n")
    with open(os.path.join(dossier, "robots.txt"), "w", encoding="utf-8", newline="\n") as r:
        r.write("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % base)
    print("sitemap.xml et robots.txt créés avec %d pages :" % len(pages))
    for f in pages:
        print("  ", f)
    print("Envoyez tout le dossier en ligne, puis soumettez %s/sitemap.xml dans Google Search Console." % base)


if __name__ == "__main__":
    main()
