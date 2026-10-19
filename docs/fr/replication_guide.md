# Guide de reproduction

## Ce qui peut être reproduit

| Élément | Reproductible | Remarques |
|---|---|---|
| CAO mécanique | Oui | Sources SolidWorks et exports STL inclus |
| Fabrication des PCB | Oui | Archives Gerber et nomenclatures incluses |
| Interface de la station au sol | Partiellement | Le code démarre, mais les courbes et commandes sont factices |
| Firmware de vol | Non | Absent de l’archive |
| Données de vol | Non | Aucun journal, étalonnage ou essai de portée |
| Portée de la liaison | Non | L’objectif kilométrique n’est pas vérifié |

## Prérequis

- SolidWorks 2021 ou ultérieur, ou une visionneuse `.SLDPRT` / `.SLDASM`.
- Une imprimante 3D FDM et un logiciel de découpe.
- Un fabricant de PCB acceptant les archives Gerber.
- Python 3.11 pour la station au sol.
- Un adaptateur série 3,3 V pour les essais au banc.

## 1. Vérifier la révision mécanique

Commencer par `mechanical/source/formal/`. Les assemblages sont
`装配/整体装配.SLDASM` et `装配/分体装配.SLDASM`. Conserver les noms chinois des
pièces et des dossiers : les assemblages s’y réfèrent. En cas de renommage,
réparer la référence dans SolidWorks.

Les exports STL se trouvent dans `mechanical/output/3dp/` ; la seconde série
d’impression est dans `mechanical/output/reprint/`. Les paramètres d’impression
ne sont pas documentés. Choisir matériau, hauteur de couche et remplissage selon
les charges réelles, puis les consigner dans le journal de fabrication.

## 2. Fabriquer l’électronique

1. Envoyer les neuf archives Gerber de `electronics/output/gerber/` à un
   fabricant.
2. Commander les pièces depuis `BOM/bill_of_materials.csv`. Seize lignes n’ont
   ni prix ni référence fournisseur ; les compléter avant commande.
3. Vérifier les contours des cartes par rapport aux baies imprimées. Les
   dimensions mesurées figurent dans `docs/fr/system_design.md`.
4. Inspecter les bords à doigts dorés et les connecteurs FPC avant soudure.

## 3. Assembler et tester au banc

1. Empiler les baies sans colle et contrôler l’alignement.
2. Vérifier la continuité de chaque contact à doigts dorés.
3. Alimenter avec une source limitée en courant avant de brancher la batterie.
4. Confirmer le rail 3,3 V et les adresses I2C des capteurs.
5. Ne pas installer de moteur ni de dispositif énergétique pendant les essais.

## 4. Lancer la station au sol

```bash
cd software/ground_station
python -m pip install -r requirements.txt
python appMain.py
```

Sélectionner le port série, l’ouvrir à 9600 bauds et démarrer le flux. Le code
archivé analyse les champs `X`, `Y`, `GX`, `GY`, `GZ` et écrit `data.txt`. Les six
courbes affichent `y = x^2` ; ce ne sont pas des données en direct. Le cube
OpenGL est désactivé.

## 5. Vérifier le logiciel

```bash
python scripts/verify_theory/run_verification.py
```

La suite couvre les formules d’attitude, le filtre complémentaire, la trame
proposée, les conventions de quaternion, le profil de von Kármán et la géométrie
mesurée. Elle ne teste ni l’interface graphique ni le matériel.

## 6. Ce qui manque encore pour un vol

- Un firmware RP2040 avec ordonnancement à période fixe.
- La trame décrite dans `media/photos/project/telemetry_frame.svg`.
- Un enregistreur horodaté et un outil de rejeu.
- Un bilan de liaison, le choix d’antenne et un essai de portée.
- Une machine d’état d’armement, des contrôles de continuité et une liste de
  lancement.
- Un plan d’essai approuvé par un responsable sécurité qualifié.

## Sécurité

Ce dépôt documente un projet étudiant. Il ne contient ni formulation de
propergol, ni circuit d’allumage, ni procédure de lancement. Ne pas tenter de vol
sans supervision qualifiée, autorisation légale et pas de tir adapté.
