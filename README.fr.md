<p align="center">
  <img src="./media/photos/project/banner.png" alt="Rendu de l’assemblage complet DustArrow X" width="800"/>
</p>

<h1 align="center">DustArrow X · 沙尘利«箭»</h1>

<p align="center">
  <strong>Système de télémétrie modulaire pour fusée-sonde météorologique de 40 mm</strong>
  <br>
  Chaîne de capteurs RP2040, liaison descendante LoRa et prototype de station au sol PyQt5
</p>

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="Licence : MIT"></a>
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white" alt="Python 3.11">
  <img src="https://img.shields.io/badge/PyQt5-station_au_sol-41CD52?logo=qt&logoColor=white" alt="PyQt5">
  <img src="https://img.shields.io/badge/SolidWorks-CAO-e63946" alt="SolidWorks">
  <img src="https://img.shields.io/badge/%C3%89tat-prototype-f59e0b" alt="État : prototype">
  <br>
  <a href="./README.md">English</a> |
  <a href="./README.zh-CN.md">中文</a> |
  <a href="./README.fr.md">Français</a>
</p>

---

## Origine du nom

Le nom chinois « 沙尘利箭 » associe « 沙尘 » (poussière de sable) et « 利箭 »
(flèche acérée). Il désigne à la fois la fusée-sonde et l’idée d’une action utile
contre les tempêtes de poussière. Le nom anglais **DustArrow** en est la
traduction directe. La structure modulaire s’inspire des armoires expérimentales
de la station spatiale chinoise. La troisième génération ajoute **X** ; dans le
sujet télévisé de janvier 2024, l’auteur explique que X signifie « des
possibilités infinies ».

## À propos du projet

DustArrow X est la troisième génération documentée du projet étudiant « 沙尘利箭 »,
après Theta et Beta. Le projet a été présenté au concours national chinois
d’innovation scientifique et technologique pour les jeunes. Il vise à mesurer le
profil vertical de l’atmosphère pendant les épisodes de poussière avec une
fusée-sonde à faible coût.

La cellule mesure 40 mm de diamètre et comporte dix sections fonctionnelles. Les
modules sont reliés par des contacts à doigts dorés ; un circuit imprimé flexible
assure le routage interne. L’électronique de bord repose sur un RP2040, un
MPU6050, un BMP280, un ATGM336H, un modem LoRa A39C, un capteur de poussière
GP2Y1014AU0F et des capteurs de gaz MQ. La station au sol est une interface
Python/PyQt5. Le projet a été présenté dans *Young Edison* saison 8 sur la
télévision de Shanghai en janvier 2024.

Le dépôt contient la CAO mécanique, les Gerber, la nomenclature, le code de la
station au sol, le rapport original, la présentation et les médias. Il ne contient
**pas** le firmware de vol, les journaux de vol, l’étalonnage des capteurs ni les
essais de portée. La station archivée est un prototype d’interface : les courbes
sont factices et les boutons ne sont pas reliés à une chaîne de transmission.
Voir les [errata](docs/errata.md).

## Caractéristiques principales

- **Cellule modulaire de 40 mm** : dix sections, contacts à doigts dorés et FPC,
  pièces imprimées remplaçables individuellement.
- **Chaîne de capteurs RP2040** : IMU six axes, baromètre, GNSS, poussière et gaz.
- **Liaison descendante LoRa** : modem série A39C-T400A22D1a reçu à 9600 bauds.
- **Prototype de station au sol PyQt5** : six courbes, cube d’attitude 3D et six
  boutons de commande.
- **Fichiers de fabrication ouverts** : sources SolidWorks, STL, STEP, Gerber,
  nomenclature et sérigraphies.
- **Vérification traçable** : seize errata et 32 tests Python, sans masquer les
  échecs.

## Architecture du système

<p align="center">
  <img src="./media/photos/project/system_architecture.svg" alt="Architecture du système DustArrow X" width="900"/>
  <br>
  <em>Architecture du système. Les traits pointillés représentent la liaison radio ; la voie de commande n’est pas implémentée dans le code archivé.</em>
</p>

- **Mécanique** : ogive et baie de parachute, baies de télémétrie, de données,
  d’alimentation, trois baies de capteurs, baie de commande principale, baie
  canard et baie de propulsion/empennage. Le parachute utilise un servo à grande
  ouverture ; les canards forment un mécanisme à deux canaux.
- **Électronique** : neuf nomenclatures et dix archives Gerber. Les cartes
  principales s’articulent autour du RP2040, du MPU6050, du BMP280, de
  l’ATGM336H et de l’A39C.
- **Liaison descendante** : flux texte libre à 9600 bauds, 8-N-1. L’expression
  régulière archivée n’a ni en-tête, ni longueur, ni somme de contrôle ; une
  trame binaire avec CRC-16 est recommandée.
- **Station au sol** : PyQt5, Matplotlib et OpenGL. Dans la version archivée, les
  six courbes sont factices, le widget OpenGL est commenté et les boutons ne
  transmettent rien.

## Théorie et conception

Au repos, l’accéléromètre mesure la réaction à la gravité. Avec \(x\) vers
l’avant, \(y\) vers la droite et \(z\) vers le haut :

\[
\phi = \operatorname{atan2}(a_y, a_z),
\qquad
\theta = \operatorname{atan2}\!\left(-a_x,\sqrt{a_y^2+a_z^2}\right).
\]

La forme discrète du filtre complémentaire du premier ordre est

\[
\alpha = \frac{\tau}{\tau+\Delta t},
\qquad
\theta_k = \alpha\,\theta_{\mathrm{acc},k}
+ (1-\alpha)\left(\theta_{k-1} + \omega_y \Delta t\right).
\]

Le rapport utilise \(\arctan(a_y/a_z)\), sans quadrant : à \(150^\circ\), cette
forme renvoie \(-30^\circ\). Une IMU six axes ne peut pas observer le lacet. La
démonstration complète, les limites et les conventions de quaternion se trouvent
dans [Principe de fonctionnement](docs/fr/theory_of_operation.md) ; les
corrections sont détaillées dans les [errata](docs/errata.md).

## Structure du dépôt

```text
DustArrow/
├── BOM/                     # consolidated bill of materials
├── electronics/
│   ├── datasheets/          # manufacturer datasheets
│   ├── output/              # Gerber, BOM, silkscreen, PCB 3D
│   └── source/              # legacy EasyEDA project
├── mechanical/
│   ├── output/              # STL, STEP, reprint files
│   └── source/              # SolidWorks drafts, formal parts, reprints
├── simulation/cfd/          # CFD project and animations
├── software/ground_station/ # archived PyQt5 dashboard
├── firmware/                # status note only
├── docs/                    # trilingual docs, errata, verification, archive
├── media/                   # photos, GIFs, videos
├── scripts/verify_theory/   # reproducible tests
└── .github/                 # issue and PR templates
```

Les sources mécaniques conservent leurs noms chinois, car les assemblages
SolidWorks les référencent. Les sorties STL ont été renommées en anglais et
accompagnées de `part_name_mapping.csv`. La correspondance complète figure dans
[MIGRATION_NOTES.md](MIGRATION_NOTES.md).

## Nomenclature

| Indicateur | Valeur |
|---|---:|
| Modules PCB | 9 |
| Lignes de nomenclature | 48 |
| Pièces | 57 |
| Coût connu | 31,44 CNY |
| Lignes sans prix | 16 |

Le coût connu ne couvre que les lignes renseignées ; seize lignes, dont le
RP2040/Pico, le LoRa, le GNSS et les capteurs MQ, n’ont pas de prix. Le total de
31,44 CNY est donc une borne inférieure historique. Détails dans
[BOM/bill_of_materials.csv](BOM/bill_of_materials.csv) et
[BOM/README.md](BOM/README.md).

## Démarrage

**Station au sol** (Python 3.11) :

```bash
cd software/ground_station
python -m pip install -r requirements.txt
python appMain.py
```

Sélectionner le port série et l’ouvrir à 9600 bauds. Le code archivé analyse les
champs `X`, `Y`, `GX`, `GY`, `GZ` et écrit `data.txt` ; les six courbes et le cube
3D ne sont pas des données en direct. Voir
[software/ground_station/README.md](software/ground_station/README.md).

**Mécanique et électronique** : ouvrir les assemblages dans
[mechanical/source/formal/](mechanical/source/formal/) ou utiliser directement les
STL de [mechanical/output/3dp/](mechanical/output/3dp/). Les fichiers de
fabrication PCB sont dans [electronics/output/gerber/](electronics/output/gerber/).
La procédure est décrite dans le [guide de reproduction](docs/fr/replication_guide.md).

**Vérification** :

```bash
python scripts/verify_theory/run_verification.py
```

## Démonstration et tests

<p align="center">
  <img src="./media/photos/project/cfd_demo.gif" alt="Démonstration CFD de l’ogive de von Kármán et des canards" width="800"/>
  <br>
  <em>Démonstration CFD. Les vidéos originales sont dans media/videos/.</em>
</p>

<p align="center">
  <img src="./media/photos/project/canard_deployment.gif" alt="Animation du déploiement des canards et de la séparation de l’ogive" width="800"/>
  <br>
  <em>Animation du mécanisme : séparation de l’ogive, déploiement des canards et récupération.</em>
</p>

<p align="center">
  <img src="./media/photos/project/ground_station_ui.png" alt="Interface archivée de la station au sol" width="800"/>
  <br>
  <em>Interface archivée. Les six courbes affichent y = x² ; ce ne sont pas des mesures.</em>
</p>

Résultat de vérification : 32 tests réussis, couvrant les formules d’attitude, le
filtre complémentaire, les quaternions, l’analyse de trame, la courbe de von
Kármán, la géométrie STL, le contour Gerber et le coût de la nomenclature.
L’inventaire et l’échec corrigé du premier passage sont consignés dans
[Vérification](docs/verification.md).

## Couverture médiatique

En janvier 2024, l’émission de science pour la jeunesse *Young Edison* saison 8,
*Tomorrow’s World*, diffusée par la télévision de Shanghai, a consacré un sujet au
projet. L’épisode suit un essai en vol près de Guyuan à la fin de l’automne ou au
début de l’hiver 2023 : l’allumage à distance échoue, l’équipe passe à un allumage
filaire, la fusée quitte le rail, la section des capteurs est récupérée tandis que
la baie de parachute et le module de propulsion sont perdus. L’élève estime le
taux de récupération à 80 %. L’émission parle de « succès » ; le dépôt décrit donc
une récupération partielle, pas une récupération complète de la cellule.

L’épisode indique aussi que X signifie « des possibilités infinies » et que la
station au sol lit un fichier texte pour un retour d’attitude simple, ce qui
correspond au prototype archivé. Il ne fournit ni journal de télémétrie ni données
quantitatives. La vidéo n’est pas rediffusée dans ce dépôt.

- [Couverture détaillée](docs/fr/media_coverage.md)
- Pages officielles : [aperçu](https://www.kankanews.com/detail/ELwxNKJWGy9),
  [épisode](https://www.kankanews.com/detail/LMwVGm9WB2z),
  [présentation de la saison](https://www.kankanews.com/detail/boy4AKjBxQ1)

## Spécifications de conception

| Paramètre | Valeur | Source / statut |
|---|---|---|
| Diamètre de la cellule | 40,0 mm | Mesuré, boîte englobante STL |
| Profil de l’ogive | Courbe de von Kármán | Formule du rapport, vérifiée numériquement |
| Contour Command A | 30 × 40 mm | Mesuré, contour Gerber |
| Contour Power | 25,0 × 25,1 mm | Mesuré, contour Gerber |
| Contour Data | 32 × 101 mm | Mesuré, contour Gerber |
| Contour Exploration | 32 × 76 mm | Mesuré, contour Gerber |
| Microcontrôleur | RP2040 | Nomenclature / rapport |
| IMU | MPU6050 | Nomenclature |
| Baromètre | BMP280 | Nomenclature ; le rapport indique BMP-180, [à confirmer] |
| GNSS | ATGM336H-5N | Rapport |
| Liaison descendante | A39C-T400A22D1a | Rapport / nomenclature |
| Capteur de poussière | GP2Y1014AU0F | Nomenclature |
| Capteurs de gaz | MQ-2, MQ-135 | Nomenclature |
| Port série de la station | 9600, 8-N-1 | Code source |
| Portée de la liaison | Kilométrique | Objectif non vérifié |
| Essai en vol | Un vol documenté par la télévision fin automne/début hiver 2023 ; section capteurs récupérée, baie de parachute et propulsion perdues ; aucun journal de télémétrie | Preuve télévisée, récupération partielle |
| Masse totale | Non consignée | Non disponible |

## Errata et problèmes connus

- La formule de roulis est remplacée par `atan2(a_y, a_z)` pour corriger le
  quadrant.
- Une IMU six axes n’observe pas le lacet ; le « cube 3D » ne montre que le
  roulis et le tangage.
- L’expression régulière archivée ne gère ni fragmentation ni concaténation ;
  une trame avec longueur et CRC-16 est proposée mais non implémentée dans le
  firmware.
- Le dépôt ne contient ni firmware, ni données de vol, ni étalonnage, ni bilan de
  liaison.

Liste complète dans les [errata](docs/errata.md), limites dans la
[Vérification](docs/verification.md).

## Feuille de route

1. Écrire le firmware RP2040 avec la trame binaire CRC-16 et la voie de commande.
2. Remplacer les courbes factices par un affichage temps réel, un journal
   horodaté et un outil de rejeu.
3. Réaliser les essais au banc, le bilan de liaison et l’essai de portée, puis
   publier des données anonymisées.

## Contribution

Voir [CONTRIBUTING.md](CONTRIBUTING.md). Ne pas ajouter de formulation de
propergol, de procédure d’allumage ou d’instruction de lancement.

## Licence

Le code, la documentation et les médias originaux de l’auteur sont sous
[MIT](LICENSE). Les fiches techniques tierces et le logo du concours ne relèvent
pas de cette licence ; voir [Références](docs/references/README.md).

## Remerciements

Merci au lycée n° 1 de Guyuan (Ningxia) et au concours national chinois
d’innovation scientifique et technologique pour les jeunes. Merci à Shanghai
Media Group et à l’équipe de *Young Edison* pour le reportage. Le projet utilise
SolidWorks, EasyEDA, Python, PyQt5, Matplotlib, PySerial et OpenGL. Le rapport
original, la présentation et l’ancien code sont conservés dans
[docs/archive/](docs/archive/).
