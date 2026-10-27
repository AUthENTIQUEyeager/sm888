# Site SM888 — SAANÉM · LA MÉÉBO 888

Site vitrine statique : pas de serveur, pas de base de données. Pour le voir, double-cliquez sur `index.html`.

## 1. Changer le numéro WhatsApp, les téléphones, l’adresse, l’e-mail
Ouvrez `js/config.js` avec le Bloc-notes. Modifiez uniquement ce qui est entre guillemets :
- `WHATSAPP_NUMBER` : numéro au format international **sans le +** (exemple : `"22670000000"`). La valeur actuelle est **provisoire**.
- `PHONE_1`, `PHONE_2`, `ADRESSE`.
- `EMAIL` : laissez `""` pour ne pas afficher d’e-mail.
- `MESSAGES` : les textes pré-remplis dans WhatsApp.

Tous les boutons du site (WhatsApp, appel, barre mobile, pied de page) se mettent à jour automatiquement.

## 2. Ajouter ou modifier une machine
Ouvrez `js/catalogue.js`. Chaque machine est une ligne entre accolades `{ ... }`.
Pour en ajouter une : copiez une ligne, collez-la en dessous (sans oublier la virgule à la fin de la ligne précédente), puis changez `id`, `nom`, `categorie` (`"engin"` ou `"equipement"`), `mode` (`["location"]`, `["vente"]` ou les deux), `etat` (`"neuf"`, `"occasion"` ou `"sur demande"`), `description`, `utilite`, `image` et `prix` (laissez `"Sur devis"` si le prix n’est pas fixé). La page « Engins & équipements » se met à jour seule.

## 3. Remplacer les images et le logo
- **Photos des machines** : mettez vos photos dans `assets/img/` en gardant **exactement le même nom** que le placeholder (ex. `pelle-hydraulique.webp`). Taille conseillée : 800 × 600 px, format WebP, moins de 80 Ko. Pour une nouvelle machine, indiquez le nom du fichier dans le champ `image`.
- **Image de partage** (`assets/img/og.webp`) : 1200 × 630 px. Après la mise en ligne, mettez l’adresse complète du site dans la balise `og:image` de chaque page.
- **Logo** : remplacez `assets/logo.svg` par le logo officiel. S’il est en PNG, déposez-le dans `assets/` puis changez `LOGO = 'assets/logo.svg'` en haut de `js/main.js`. Remplacez aussi `assets/favicon.svg` (petite icône de l’onglet).

## 4. Compléter les informations manquantes
Rien n’a été inventé. Dans `or.html` et `apropos.html`, cherchez « À COMPLÉTER » : renseignez le numéro d’agrément, le RCCM, l’IFU, l’année de création, etc., puis supprimez le mot `hidden` de la liste concernée pour l’afficher.

## 5. Menu, pied de page, boutons flottants
Ils sont définis une seule fois dans `js/main.js` (section « En-tête, pied de page… ») et apparaissent sur toutes les pages.

## 6. Mettre le site en ligne
1. Envoyez **tout le dossier** (pages, `css`, `js`, `assets`, `sitemap.xml`, `robots.txt`) chez un hébergeur statique : Netlify, Cloudflare Pages, GitHub Pages, ou un hébergement classique par FTP.
2. Dans `sitemap.xml` et `robots.txt`, remplacez `www.exemple.com` par l’adresse réelle du site.
3. Testez sur un téléphone : boutons WhatsApp, appels, formulaire, menu.

## 7. Télécharger automatiquement les photos des engins
Le script `telecharger_images.py` remplace les images provisoires par de vraies photos de chaque machine, sans rien toucher au site.
1. Installez Python 3 (python.org), puis tapez une fois : `pip install pillow`
2. Dans `telecharger_images.py`, remplacez `contact@exemple.com` par votre e-mail (demandé par Wikimedia).
3. Dans le dossier du site, lancez : `python telecharger_images.py` (ou `python telecharger_images.py bulldozer` pour une seule machine).
4. Ouvrez `engins.html` : les photos sont à leur place. Si l’une ne convient pas, changez ses mots-clés dans `MACHINES` (en haut du script) et relancez pour cette machine seulement.

Les photos viennent de Wikimedia Commons, uniquement sous licence libre. Les auteurs sont crédités automatiquement dans `credits.html` (lien dans le pied de page) : ne retirez pas cette page tant que ces photos sont utilisées. Si une machine n’est pas trouvée, l’image provisoire est conservée. Quand vous aurez vos propres photos, remplacez les fichiers dans `assets/img/` et retirez la phrase « crédits photos » de `engins.html`.

## 8. Produits agricoles, noix, diaporama et couleurs
- **Produits agricoles** (`produits-agricoles.html`) : le catalogue est dans `js/produits-agricoles.js`. Il comprend céréales, arachide, soja, sésame et anacarde. L’ancienne adresse `cereales.html` redirige vers cette page.
- **Noix** (`noix.html`) : le catalogue est dans `js/noix.js` (karité, cajou, coco et palmiste).
- **Photos agricoles et noix** : lancez `python3 telecharger_images_agricoles.py` pour télécharger les images des deux catalogues et leurs en-têtes. Pour une seule image, ajoutez son nom (ex. `python3 telecharger_images_agricoles.py arachide`). Le script demande Pillow (`python3 -m pip install pillow`) et utilise l’adresse de contact configurée dans `telecharger_images.py`. Sur Mac, si Python signale une erreur de certificat SSL, lancez `Install Certificates.command` depuis le dossier Python. Les crédits Wikimedia sont conservés dans `js/credits.js`.
- **Autres photos** : `python3 telecharger_images.py` télécharge les images du diaporama, de l’or et des engins. Pour un groupe : `python3 telecharger_images.py hero` ; pour une seule : `python3 telecharger_images.py bulldozer`.
- **Accueil** : le diaporama utilise `hero-accueil-1/2/3.webp`. Les pages Or et Engins ont leur image d’en-tête (`hero-or`, `hero-engins`). Les pages Produits agricoles et Noix utilisent `hero-produits-agricoles` et `hero-noix`. La page Or a aussi un emplacement `or-image.webp`.
- **Couleurs vives** : modifiez `--vif-or`, `--vif-orange`, `--vif-vert` au début de `css/style.css`.
