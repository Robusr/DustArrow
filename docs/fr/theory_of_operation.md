# Principe de fonctionnement

## Portée

Ce document présente les mathématiques d’attitude et de télémétrie du prototype
DustArrow X. Le rapport original ne contient qu’une courte démonstration ; ce
texte explicite les conventions, délimite leur validité et relie chaque
correction à `../errata.md` et `../verification.md`.

## Statut des preuves

| Élément | Statut | Source |
|---|---|---|
| Diamètre de la cellule : 40,0 mm | Mesuré | Boîte englobante STL, `scripts/verify_theory/test_geometry.py` |
| Carte d’alimentation : 25,0 × 25,1 mm | Mesuré | Contour Gerber |
| Roulis et tangage à partir de la gravité | Dérivé | Ce document, vérifié numériquement |
| Pondérations du filtre complémentaire | Texte du rapport, incomplet | Rapport original, section 2 |
| Lacet avec le seul MPU6050 | Non observable | IMU 6 axes sans magnétomètre |
| Télémétrie kilométrique | Objectif non vérifié | Aucun bilan de liaison ni essai de portée dans l’archive |
| Commande PID de vol | Non implémentée | Le rapport indique un algorithme encore exploratoire |

## Convention de repère

Le rapport définit le roulis autour de $x$, le tangage autour de $y$ et le
lacet autour de $z$, sans préciser le sens des axes ni le montage du capteur.
La suite de vérification adopte la convention suivante :

- Repère du corps : $x$ vers l’avant, $y$ vers la droite, $z$ vers le haut,
  main droite.
- Repère inertiel : horizontal local, $z$ vers le haut.
- Le quaternion $q$ effectue la rotation du repère du corps vers le repère
  inertiel.
- La gravité inertielle vaut $\mathbf{g}_i = [0, 0, g]^T$, avec
  $g = 9,80665\ \mathrm{m/s^2}$.

Si la carte de vol utilise un autre montage, tous les signes ci-dessous doivent
être revérifiés. Ce point est marqué `[待确认]` dans les errata.

## Attitude statique à partir de la gravité

À l’arrêt et sans accélération, l’accéléromètre mesure la réaction à la gravité :

$$
\mathbf{a}_b = R(q)^T \mathbf{g}_i .
$$

Avec le roulis $\phi$ et le tangage $\theta$, les composantes sont

$$
a_x = -g \sin\theta, \qquad
a_y = g \sin\phi \cos\theta, \qquad
a_z = g \cos\phi \cos\theta .
$$

On en déduit

$$
\phi = \mathrm{atan2}(a_y, a_z),
$$

$$
\theta = \mathrm{atan2}\left(-a_x,\sqrt{a_y^2+a_z^2}\right).
$$

Le rapport écrit $\phi = \arctan(a_y/a_z)$. Cette forme perd le quadrant et
n’est pas définie lorsque $a_z = 0$. Pour $\phi = 150^\circ$, elle renvoie
$-30^\circ$. Les errata remplacent la formule par `atan2` ; le test numérique
reproduit l’erreur.

Le rapport montre aussi une équation de tangage de la forme
$\sin\theta = a_x/\sqrt{a_y^2+a_z^2}$. Elle n’est équivalente à l’expression
ci-dessus qu’après fixation des signes d’axes. Elle est marquée `[待确认]`, car
le montage n’est pas documenté.

## Filtre complémentaire

Le rapport donne

$$
\theta_k = k\,\theta_{\mathrm{acc},k} + (1-k)\,\theta_{\mathrm{gyro},k},
\qquad
\theta_{\mathrm{gyro},k} = \theta_{k-1} + \omega_y \Delta t .
$$

Il s’agit d’un filtre complémentaire du premier ordre. Le texte ne précise ni
$\Delta t$, ni la fréquence d’échantillonnage, ni la condition initiale, ni le
biais du gyroscope. Une forme reproductible utilise une constante de temps
$\tau$ :

$$
\alpha = \frac{\tau}{\tau+\Delta t},
$$

$$
\theta_k = \alpha\,\theta_{\mathrm{acc},k} +
(1-\alpha)\left(\theta_{k-1} + \omega_y \Delta t\right).
$$

Le filtre fait confiance à l’accéléromètre en basse fréquence et au gyroscope en
haute fréquence. Il ne rend pas l’accéléromètre valide pendant la poussée. Avec
$\alpha = \tau/(\tau+\Delta t)$, un biais constant $b$ produit une faible
erreur statique $b\,\Delta t^2/\tau$, alors qu’une intégration gyroscopique
pure dérive de $b t$. La suite de vérification contrôle les deux
comportements et montre qu’un $k$ fixe déplace la fréquence de coupure lorsque
$\Delta t$ change.

## Lacet et limites d’une IMU 6 axes

La gravité ne contient aucune information de cap. Une rotation de lacet laisse
$\mathbf{a}_b = [0,0,g]^T$ inchangé : le roulis et le tangage sont observables,
le lacet ne l’est pas. Le MPU6050 n’a pas de magnétomètre. Le cube de la station
au sol est donc un indicateur de roulis et de tangage, pas un affichage
d’attitude 3D complète. Un cap exige un magnétomètre, le cap GNSS, ou un lacet
initial connu propagé par gyroscope avec surveillance de la dérive.

## Accélération dynamique

Pendant la combustion, l’accéléromètre mesure la poussée et la gravité. Pour un
véhicule horizontal soumis à une poussée axiale de 20 m/s², la formule statique
donne environ $-64^\circ$ au lieu de $0^\circ$. Le filtre complémentaire
atténue les transitoires courts mais ne supprime pas une accélération durable.
L’archive ne contient aucune donnée d’accélération en vol ; l’erreur réelle n’est
donc pas quantifiée.

## Trame de télémétrie

La station au sol archivée utilise l’expression régulière
`X(.+)Y(.+)GX(.+)GY(.+)GZ(.+)`. Elle n’a ni en-tête, ni longueur, ni somme de
contrôle. Une trame coupée entre deux lectures série est perdue ; deux trames
collées sont mal interprétées à cause du `.+` glouton.

La trame de remplacement vérifiée est :

```
0x24 | LEN (1 octet) | PAYLOAD (0..64 octets) | CRC-16/CCITT-FALSE (2 octets) | 0x2A
```

Elle se resynchronise sur l’en-tête, accepte une livraison octet par octet,
rejette un CRC incorrect et gère plusieurs trames par lecture. Le parseur et les
tests se trouvent dans `../../scripts/verify_theory/test_protocol.py`. Il s’agit
d’une recommandation, pas d’une description du firmware archivé.

## Quaternions

Le rapport n’utilise pas de quaternions. L’implémentation de référence
`../../scripts/verify_theory/quaternion.py` fixe les conventions du dépôt :

- Produit de Hamilton.
- Scalaire en premier, $q = [w,x,y,z]$.
- Rotation active du repère du corps vers le repère inertiel.
- Normalisation après chaque pas d’intégration.
- Erreur d’attitude mesurée par l’angle géodésique
  $2\arccos(|\langle q_1,q_2\rangle|)$, jamais par une différence de
  composantes.

Les tests couvrent l’identité, les rotations de 90° et 180°, l’ordre de
composition, l’inverse, l’orthonormalité de la matrice, l’aller-retour d’Euler,
l’équivalence $q \equiv -q$ et l’intégration à vitesse angulaire constante.
Ils préparent un estimateur d’attitude complet ; ils ne prétendent pas que le
firmware d’origine utilisait des quaternions.

## Vérification

Exécuter :

```bash
python scripts/verify_theory/run_verification.py
```

Le nombre exact de tests, l’attente de test corrigée et les points encore non
confirmés sont consignés dans `../verification.md` et `../errata.md`.
