# Conception du système

## Cellule

DustArrow X est une cellule de fusée-sonde modulaire de 40,0 mm de diamètre. Les
sources mécaniques sont organisées par révision :

- `mechanical/source/draft/` : concepts initiaux, dont une baie d’imagerie et
  une étude de gouvernes canard à quatre canaux.
- `mechanical/source/launch_revision/` : modifications avant lancement.
- `mechanical/source/formal/` : baies et assemblages finaux.
- `mechanical/source/reprint_models/` : huit pièces révisées pour une seconde
  impression.

La cellule finale comporte dix sections fonctionnelles :

1. Ogive et baie de parachute
2. Baie de télémétrie
3. Baie de données
4. Baie d’alimentation
5. Baie du capteur de poussière
6. Baie du capteur de gaz
7. Baie du capteur de fumée
8. Baie de commande principale
9. Baie des plans canard
10. Baie de propulsion et d’empennage

Les sorties d’impression comprennent 28 fichiers STL dans
`mechanical/output/3dp/` et 15 STL de réimpression dans
`mechanical/output/reprint/`. Le profil de l’ogive suit la formule de von Kármán
conservée dans `docs/references/von_karman_formula.txt`.

## Interfaces mécaniques

- Les modules sont empilés le long de l’axe du corps et reliés par des contacts
  à doigts dorés.
- Dans chaque baie, un circuit imprimé flexible achemine les signaux vers le
  connecteur.
- La baie de parachute utilise un servo et une trappe à grand angle ; la baie
  canard utilise un mécanisme de gouvernail à deux canaux.
- Les pièces sont conçues pour l’impression FDM. Le rapport ne précise ni le
  matériau, ni le taux de remplissage, ni la hauteur de couche, ni la durée
  d’impression ; ces valeurs ne sont pas inventées ici.

## Électronique

L’archive contient neuf nomenclatures de modules, dix archives Gerber et un
ancien projet EasyEDA. Les contours des cartes ont été mesurés sur la couche de
contour Gerber.

| Module | Contour | Composants clés | Fonction |
|---|---|---|---|
| Command A | 30 × 40 mm | Connecteur FPC, embase GNSS, 2× carte à carte | Commande et interface GNSS |
| Command B | non mesuré | MPU6050, BMP280, embase MCU, FPC | Mesure et commande |
| Data | 32 × 101 mm | Modem LoRa A39C-T400A22D1a, alimentation JST | Liaison descendante |
| Power | 25 × 25,1 mm | IP5306, USB, LED de charge | Gestion d’alimentation |
| Exploration | 32 × 76 mm | Raspberry Pi Pico, interrupteur, LED | Carte contrôleur / expérimentation |
| DustSensor Up | non mesuré | GP2Y1014AU0F, connecteurs ZH1.5 | Mesure de poussière |
| DustSensor Down | 25 × 25 mm | MQ-2, MQ-135 | Mesure de gaz |
| GasSensorHAT | non mesuré | MQ-135, connecteur à doigts dorés | Extension capteur de gaz |
| ServoHAT | 25 × 25,9 mm | Broche servo, trois LED | Servo canard / parachute |
| COSensorHAT | Gerber seul | aucune nomenclature | Extension capteur de CO |

La nomenclature consolidée compte 48 lignes et 57 pièces. Seize lignes n’ont pas
de prix ; le total connu de 31,44 CNY est une borne inférieure historique.

## Station au sol

L’application archivée est un prototype PyQt5 :

```
port série (9600, 8-N-1)
        │
        ▼
analyse par expression régulière  X...Y...GX...GY...GZ...
        │
        ├── data.txt (écrasé à chaque trame)
        ├── six canevas Matplotlib (courbe factice y = x²)
        └── cube OpenGL (désactivé dans le code archivé)
```

Les six courbes prévues sont l’altitude, la pression, la température, l’humidité,
la visibilité et les PM1.0. Les six boutons de commande sont le parachute
d’urgence, la demande de coordonnées, l’échantillonnage en altitude, la
calibration d’attitude, le rafraîchissement des données et l’autotest. Aucun
bouton n’est relié à une chaîne de transmission.

## Flux de données et protocole

La liaison descendante est un flux texte libre à 9600 bauds. La trame de
remplacement proposée est binaire, avec une longueur sur un octet et un
CRC-16/CCITT-FALSE. Elle peut être reconstruite à partir de fragments série
arbitraires et rejette les charges utiles corrompues. Voir
`media/photos/project/telemetry_frame.svg` et
`scripts/verify_theory/test_protocol.py`.

## Alimentation et sécurité

La baie d’alimentation utilise un contrôleur IP5306 avec charge USB et une
batterie Li-ion à cellule unique. L’archive ne contient ni modèle de batterie, ni
capacité, ni essai de décharge, ni revue de protection. La section de propulsion
n’est qu’un support pour un moteur solide du commerce ; aucune spécification de
moteur, aucun circuit d’allumage et aucune procédure de lancement ne sont
inclus. Tout vol exige une supervision qualifiée et le respect des règles de
sécurité du pas de tir.
