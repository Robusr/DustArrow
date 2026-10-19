# Couverture médiatique : Young Edison saison 8, Tomorrow’s World

<p align="center">
  <a href="../en/media_coverage.md">English</a> |
  <a href="../zh-CN/media_coverage.md">中文</a> |
  <a href="media_coverage.md">Français</a>
</p>

Cette note rassemble les informations publiques sur le sujet consacré à DustArrow
dans l’émission de science pour la jeunesse *Young Edison* saison 8, *Tomorrow’s
World*, diffusée par la télévision de Shanghai. Elle sépare le récit télévisé des
fichiers de conception, du code et des résultats de vérification du dépôt.
L’émission est une source narrative, pas un journal de télémétrie ni un rapport
d’essai.

## 1. Émission et diffusion

| Élément | Détail |
|---|---|
| Émission | *Young Edison* saison 8, *Tomorrow’s World* |
| Production et diffusion | Commission municipale des sciences et technologies de Shanghai, commission municipale de l’éducation, Shanghai Media Group ; chaîne d’information STV et application Kankan News |
| Aperçu Guo Mohan | 2024-01-25 19:53, Kankan News |
| Page de l’épisode | 2024-01-27 23:09, Kankan News |
| Présentation de la saison | 2024-02-25 10:28, Kankan News |
| Contexte de la saison | Première diffusion le 2024-01-20 ; 16 équipes de plus de 40 pays et régions |
| Conseillers scientifiques | Chen Kaixian, Ni Minjing, Tao Hu, Jia Yang, David Evans, Wang Jingya et d’autres |

Les pages ne donnent pas le même horaire : l’aperçu annonce 19 h 45 le 27 janvier,
la présentation indique le samedi à 20 h 30. Les deux sont conservés ; l’heure
exacte n’est pas traitée comme vérifiée.

Pages officielles :

- Aperçu : <https://www.kankanews.com/detail/ELwxNKJWGy9>
- Épisode : <https://www.kankanews.com/detail/LMwVGm9WB2z>
- Présentation : <https://www.kankanews.com/detail/boy4AKjBxQ1>

## 2. Enregistrement vidéo local

| Propriété | Valeur |
|---|---|
| Fichier | `F:\Desktop\Robusr\《少年爱迪生》郭沫晗.mp4` |
| Durée | 19:43.02 |
| Résolution | 640 × 360 |
| Fréquence d’images | 25 i/s |
| Vidéo | H.264 Main, environ 447 kb/s |
| Audio | AAC LC, 44,1 kHz, stéréo, environ 65 kb/s |
| Taille | 76 333 836 octets, environ 72,8 Mo |
| SHA-256 | `27854a95a43206bc7dd3ea3188fd81b3f9bddbf61c9e64516de09805426529c9` |

La vidéo est une production télévisée tierce et n’est **pas** copiée dans ce
dépôt. Seules de courtes citations et des repères temporels sont conservés ; la
vidéo complète, les sous-titres complets et les images fixes ne sont pas
rediffusés.

### Note de transcription

L’audio a été transcrit localement avec `faster-whisper small`, puis corrigé
manuellement pour les noms et les homophones évidents. Ce n’est pas une
transcription officielle et les repères temporels sont approximatifs. Les
sous-titres chinois incrustés ont servi de contrôle. La transcription machine
complète reste hors du dépôt et n’est pas versionnée.

## 3. Ce que l’épisode documente

### 3.1 Trois générations et le nom

| Moment | Déclaration diffusée |
|---|---|
| 2023-02 | La première génération est terminée ; elle mesure l’attitude et renvoie les données au logiciel sol |
| Ensuite | La deuxième génération introduit la conception modulaire |
| Troisième génération | Nommée **DustArrow X** ; « X signifie des possibilités infinies » |
| Structure de la troisième génération | L’émission parle de « quatre parties au total, assemblables librement » ; le capteur de poussière peut être réuni au capteur de gaz pour former une section à trois capteurs |
| Objectif modulaire | Pour le sable, la pluie acide ou d’autres phénomènes, remplacer le module concerné plutôt que toute la cellule |

L’émission parle de « quatre parties » vers 08:08, alors que la CAO finale divise
la cellule en dix baies fonctionnelles. Les deux descriptions ne sont pas
forcément contradictoires : l’émission regroupe quatre fonctions, la CAO détaille
dix baies fabricables. L’écart est marqué comme à confirmer par l’auteur.

### 3.2 Essai en vol

L’ouverture situe le vol « un jour de la fin de l’automne ou du début de l’hiver
2023 », sur un « site de Gobi à la périphérie de Guyuan ».

1. Le programme d’allumage à distance échoue. L’émission l’attribue à une
   protection de l’entrée/sortie de la carte de développement ; le plan initial
   est abandonné.
2. L’équipe passe à un allumage filaire et le teste avec succès à 7,5 m.
3. Un rail de lancement temporaire est installé, suivi d’un compte à rebours et du
   lancement.
4. La fusée vole et est récupérée. L’émission déclare : « la baie de parachute et
   le module de propulsion ont tous deux été perdus », « la partie capteurs, la
   plus importante, a été conservée », et « le taux de récupération a atteint
   80 % ».
5. L’élève dit que le résultat est « bien meilleur que prévu » ; l’émission
   affiche le mot « succès ».

Un résumé prudent est donc : **la fusée a quitté le rail et une partie du
véhicule a été récupérée. La section des capteurs a été retrouvée, mais la baie de
parachute et le module de propulsion ont été perdus ; la récupération de la
cellule est donc incomplète.** Les 80 % sont une estimation de l’élève sur place,
pas une mesure indépendante.

### 3.3 Station au sol et liaison de données

Vers 08:47, l’émission indique que le segment sol « lit des données dans un
fichier texte et effectue quelques tâches simples de retour d’attitude ». Cela
correspond au code archivé : l’expression régulière série écrit `data.txt`, les six
courbes sont factices et le widget OpenGL est désactivé.

Vers 18:04, l’élève décrit deux voies de données envisagées :

- un enregistreur sur carte SD ;
- un dispositif de télémétrie à distance dans la section de commande principale ;
- « en théorie, les données peuvent être renvoyées en temps réel ».

Ce sont des intentions de conception, pas des résultats démontrés. L’émission ne
montre ni journal de télémétrie, ni données de carte SD, ni liaison descendante en
direct.

### 3.4 Philosophie de conception

- Modulaire et récupérable ; plusieurs fusées pourraient être lancées dans un même
  plan pour une analyse tridimensionnelle d’un épisode de poussière.
- Les capteurs de poussière du commerce sont surtout analogiques et entachés
  d’erreur ; l’élève souhaite des capteurs plus professionnels et plus précis.
- Le projet est passé de la curiosité personnelle à un outil de surveillance de la
  poussière dans sa région natale.

## 4. Ce que l’épisode ne fournit pas

L’émission ne donne **pas** :

- l’altitude, la vitesse, l’accélération, l’attitude, la pression, la température
  ou l’humidité en vol ;
- les concentrations de poussière ou de gaz, ni l’étalonnage des capteurs ;
- la portée de communication, le RSSI, le taux d’erreur ou la marge de liaison ;
- l’altitude de déploiement du parachute, la vitesse d’impact ou le lieu de
  récupération ;
- la masse totale, la poussée, le centre de masse ou l’inertie.

L’émission ne remplace donc ni un journal de vol, ni un étalonnage, ni un bilan de
liaison. Elle prouve qu’un essai a eu lieu et qu’une partie du véhicule a été
récupérée ; elle ne prouve ni une télémétrie kilométrique ni des mesures
météorologiques quantitatives.

## 5. Terminologie et différences de version

| Sujet | Émission | Dépôt | Traitement |
|---|---|---|---|
| Type de projet | Fusée de surveillance du climat | Fusée-sonde météorologique, système de télémétrie modulaire | Même objet ; le dépôt emploie le terme technique |
| Structure de la troisième génération | Quatre parties assemblables | Dix baies fonctionnelles | Regroupement fonctionnel contre découpage CAO ; à confirmer |
| Fin de la première génération | 2023-02 | Rapport et nomenclature datés de 2023-08 | Non contradictoire : première génération en février, dossier de concours en août |
| Récupération | « Succès », 80 % | Aucun journal de vol dans l’archive | « Récupération partielle » ; 80 % marqué comme estimation |
| Liaison de données | « En théorie, retour en temps réel » | Aucun journal de télémétrie | Intention, pas mesure |
| Prix | Le profil SkillsMP revendique un deuxième prix national | Le dépôt indique seulement la participation au concours national | Liste officielle non retrouvée ; marqué `[unverified]` |

À propos du prix : un profil tiers SkillsMP indique un deuxième prix au 37e
Concours national d’innovation scientifique et technologique pour la jeunesse en
août 2023. Aucune pièce officielle n’a été retrouvée ; le fait n’est donc pas
écrit comme certain ni ajouté aux spécifications principales du README.

## 6. Tableau de vérification

| Affirmation | Preuve | Statut |
|---|---|---|
| Un essai en vol a eu lieu | Épisode 00:27–17:24 ; page Kankan | Confirmé par la diffusion |
| Échec de l’allumage à distance ; allumage filaire | Épisode 11:30–12:23 | Confirmé par la diffusion |
| Allumage filaire réussi à 7,5 m | Épisode 12:21–12:23 | Confirmé par la diffusion |
| Section capteurs récupérée ; baie de parachute et propulsion perdues | Épisode 17:09–17:24 | Confirmé par la diffusion |
| Taux de récupération de 80 % | Épisode 17:16–17:19 | Estimation de l’élève, non mesurée |
| Station sol lisant un fichier texte et retour d’attitude simple | Épisode 08:47–08:49 ; code archivé | Confirmé, prototype |
| Retour de données en temps réel | Épisode 18:20–18:22 | Intention, non démontré |
| Liaison kilométrique | Rapport | Non vérifié |
| Deuxième prix national | Profil SkillsMP | `[unverified]` ; aucune liste officielle |
| X signifie possibilités infinies | Épisode 08:02–08:05 | Confirmé par la diffusion |
| Vol fin automne/début hiver 2023 | Épisode 00:27–00:32 | Déclaration diffusée ; date exacte inconnue |

## 7. Citation, droits et limites

- L’émission est protégée par le droit d’auteur de Shanghai Media Group et de ses
  producteurs. Kankan News interdit la reproduction sans autorisation.
- Ce dépôt ne contient ni vidéo complète, ni sous-titres complets, ni images de
  l’émission ; seulement de courtes citations, des repères temporels et un résumé
  factuel.
- Citation suggérée : Shanghai Media Group, *Young Edison* saison 8, *Tomorrow’s
  World*, sujet Guo Mohan, 2024-01-27 ; SHA-256 du fichier local ci-dessus.
- Les propos de l’élève sont des récits personnels. Les chiffres de performance
  issus de l’émission doivent être cités comme « déclaration diffusée », non comme
  « mesure ».

## 8. Effet sur les informations du dépôt

- Les trois README gagnent une section de couverture médiatique et l’origine du X.
- Le tableau des spécifications remplace « aucun essai en vol dans l’archive » par
  un essai documenté par la télévision, avec récupération partielle et sans
  journal de télémétrie.
- L’errata E-16 consigne la portée et les limites de la preuve télévisée.
- Aucune théorie, nomenclature, CAO ou vérification n’est modifiée ; la diffusion
  n’est pas utilisée comme source quantitative.
