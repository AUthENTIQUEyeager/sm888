/* CATALOGUE DES ENGINS ET ÉQUIPEMENTS — pour ajouter une machine, copiez une ligne et modifiez-la.
   categorie : "engin" ou "equipement" | mode : ["location"], ["vente"] ou ["location","vente"]
   etat : "neuf", "occasion" ou "sur demande" | prix : "Sur devis" (ne jamais inventer de prix)
   image : fichier placé dans assets/img/ — taille recommandée : 800 × 600 px, WebP, moins de 80 Ko.
   Les images actuelles sont des placeholders : remplacez-les par vos photos en gardant le même nom. */
window.CATALOGUE = [
{id:"pelle-hydraulique",nom:"Pelle hydraulique",categorie:"engin",mode:["location","vente"],etat:"sur demande",description:"Engin polyvalent d’excavation et de chargement.",utilite:"Creuser, charger et déplacer la terre ou le minerai.",image:"pelle-hydraulique.webp",prix:"Sur devis"},
{id:"chargeuse",nom:"Chargeuse",categorie:"engin",mode:["location","vente"],etat:"sur demande",description:"Chargement rapide des matériaux sur site.",utilite:"Charger les camions et alimenter les installations.",image:"chargeuse.webp",prix:"Sur devis"},
{id:"tombereau",nom:"Tombereau",categorie:"engin",mode:["location","vente"],etat:"sur demande",description:"Transport de gros volumes de terre et de minerai.",utilite:"Évacuer les matériaux entre extraction et stockage.",image:"tombereau.webp",prix:"Sur devis"},
{id:"bulldozer",nom:"Bulldozer",categorie:"engin",mode:["location","vente"],etat:"sur demande",description:"Engin puissant pour pousser, niveler et dégager.",utilite:"Préparer les sites, ouvrir des pistes, niveler.",image:"bulldozer.webp",prix:"Sur devis"},
{id:"foreuse",nom:"Foreuse",categorie:"engin",mode:["location","vente"],etat:"sur demande",description:"Forage pour l’exploration et l’exploitation.",utilite:"Réaliser les trous de forage selon les besoins du site.",image:"foreuse.webp",prix:"Sur devis"},
{id:"camion-citerne",nom:"Camion-citerne",categorie:"engin",mode:["location","vente"],etat:"sur demande",description:"Transport d’eau ou de carburant sur site.",utilite:"Approvisionner les chantiers et les installations.",image:"camion-citerne.webp",prix:"Sur devis"},
{id:"concasseur",nom:"Concasseur",categorie:"equipement",mode:["vente"],etat:"sur demande",description:"Réduit la roche en fragments plus petits.",utilite:"Préparer le minerai avant le broyage.",image:"concasseur.webp",prix:"Sur devis"},
{id:"broyeur",nom:"Broyeur",categorie:"equipement",mode:["vente"],etat:"sur demande",description:"Réduit le minerai concassé en fine poudre.",utilite:"Libérer l’or contenu dans le minerai.",image:"broyeur.webp",prix:"Sur devis"},
{id:"trommel",nom:"Trommel",categorie:"equipement",mode:["vente"],etat:"sur demande",description:"Tambour rotatif de lavage et de tri.",utilite:"Séparer et classer les matériaux par taille.",image:"trommel.webp",prix:"Sur devis"},
{id:"table-vibrante",nom:"Table vibrante",categorie:"equipement",mode:["vente"],etat:"sur demande",description:"Séparation des particules fines par gravité.",utilite:"Récupérer l’or grâce à sa densité.",image:"table-vibrante.webp",prix:"Sur devis"},
{id:"pompe-eau",nom:"Pompe à eau",categorie:"equipement",mode:["vente"],etat:"sur demande",description:"Pompage pour l’alimentation et l’assèchement.",utilite:"Fournir l’eau aux installations ou assécher un site.",image:"pompe-eau.webp",prix:"Sur devis"},
{id:"batees-accessoires",nom:"Batées et accessoires",categorie:"equipement",mode:["vente"],etat:"sur demande",description:"Matériel d’orpaillage manuel et accessoires.",utilite:"Prospecter et laver les sédiments pour isoler l’or.",image:"batees-accessoires.webp",prix:"Sur devis"}
];
