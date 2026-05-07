Documentation développeur

API OpenData Tisséo version 2

Date de création : mercredi  9 mai 2012
Date de dernière mise à jour : lundi 7 mars 2022
Référence : DOCUMENTATION_DEVELOPPEUR_API_2_FR

Documentation développeur

Version API : 2
Date : 21/05/2025

                        HISTORIQUE DE L’API

Version  Date

Auteur

V0.1
V0.2
V0.3

09/05/2012  Xavier Raffin
07/08/2012  Xavier Raffin
02/10/2012  Xavier Raffin

V0.4

04/02/2013  Xavier Raffin

V0.5
V0.6
V1.0

02/07/2013  Xavier Raffin
19/07/2013  Xavier Raffin
15/10/2014  Xavier Raffin

V1.1

23/07/2015  Xavier Raffin

V1.2

15/01/2016  Xavier Raffin

Objet de la modification
Première version de l’API
Modifications XSD, et mise en places de nouvelles fonctionnalités
Ajout de la couleur de la ligne dans le service « stops_schedules » et de la
date d’expiration dans chaque résultat.
Précisions sur les arguments de place list
Ajout de filtre sur stopPointsId format de date et lien fichiers Trident et GTFS
Ajout des WebService de messages et de perturbation
Corrections mineures
Mise à jour majeure RestFULL
-  Changements d’URL et améliorations techniques
-  Ajout du calcul d’itinéraire, densité de service, networks, …
-  Ajout de possibilités sur prochains passages
Réorganisation de la documentation et ajout d’une version anglaise
Ajout de la recherche par zone géographique sur « places »
Ajout de paramètres sur « stop_areas »
Ajout d’un paramètre datetime sur « stop_schedules »
Ajout de l’info d’accessibilité sur « stop_points »
Indication de la limitation du nombre de résultat du calcul d’itinéraire
Ajout des paramètres maxDays et firstAndLastOfDay sur le service de
prochain passage

V2

03/03/2022  Sylvain Bonnet  Modification des identifiants, ajustements divers suite au changement de

V2

21/05/2025  Sylvain Bonnet  Mise à jour API lines

plateforme

Open Data : API Tisséo

Page : 2/38

Documentation développeur

Version API : 2
Date : 21/05/2025

TABLE DES MATIERES

1.

INTRODUCTION......................................................................................................... 4

1.1
1.2

OBJET DE L’API ............................................................................................................. 4
ORGANISATION DU DOCUMENT .......................................................................................... 4

2.  MODES ET CONDITIONS D’UTILISATION ................................................................. 5

2.1
2.2
2.3
2.4
2.5
2.6
2.7

MODE DE MISE EN ŒUVRE ET FORMATS ................................................................................ 5
CLES D’ACCES ............................................................................................................... 5
QUOTAS D’UTILISATION ET PARTAGE DES RESSOURCES............................................................. 6
LICENCE ...................................................................................................................... 6
PROPRIETE INTELLECTUELLE ET USAGE DE LA MARQUE TISSEO ................................................... 6
CREDIT OPENSTREETMAP ................................................................................................ 6
INTEGRATION WEB ET INTRANET ....................................................................................... 6

3.  CONCEPTS GENERAUX ............................................................................................... 7

PERIMETRE GEOGRAPHIQUE DES DONNEES ............................................................................ 7
3.1
PERIMETRE TEMPOREL DES DONNEES ................................................................................... 7
3.2
LIGNES TISSEO DISPONIBLES ............................................................................................ 7
3.3
SRID ......................................................................................................................... 8
3.4
BOUNDING BOX ............................................................................................................. 8
3.5
GEOMETRIES WKT ......................................................................................................... 8
3.6
ACCESSIBILITE .............................................................................................................. 9
3.7
DATE & TIME ............................................................................................................... 9
3.8
3.9
IDENTIFIANTS ............................................................................................................. 10
3.10  VERSION COMPRESSEE .................................................................................................. 11
3.11  OBJETS NOMMABLES ..................................................................................................... 12

4.  OBJETS ET SERVICES .............................................................................................. 13

MODELE DE DONNEES ................................................................................................... 13
4.1
STOP_AREAS : ZONES D’ARRETS ................................................................................... 14
4.2
STOP_POINTS : ARRETS (POTEAUX D’ARRETS) ................................................................. 16
4.3
PLACES : RECHERCHE DE LIEUX ET GEOCODAGE ................................................................. 18
4.4
NETWORKS : RESEAUX DE TRANSPORT DISPONIBLES .......................................................... 22
4.5
LINES : LES LIGNES COMMERCIALES ................................................................................ 23
4.6
STOPS_SCHEDULES : PROCHAINS PASSAGES ................................................................... 26
4.7
ROLLING_STOCKS : MODES DE TRANSPORTS .................................................................. 30
4.8
JOURNEYS : CALCUL D’ITINERAIRES ............................................................................... 31
4.9
4.10  MESSAGES : MESSAGES D’INFORMATION ......................................................................... 36

Open Data : API Tisséo

Page : 3/38

Documentation développeur

Version API : 2
Date : 21/05/2025

1.

 INTRODUCTION

1.1  OBJET DE L’API

L’API OpenData Tisséo permet d’obtenir en temps réel des informations sur le réseau de transport urbain
de l’agglomération toulousaine, Tisséo, et d’effectuer des calculs liés au transport public.

L’API vous permet par exemple :

  de connaitre les prochains passages des véhicules à un arrêt
  de calculer un itinéraire en transport en commun
  de connaitre les informations de perturbation
  de récupérer des objets (lignes, arrêts, lieux public, rue, …) suivant différents critères
  d’effectuer d’autres calculs plus spécifiques

Voir le chapitre 4 pour la liste complète et détaillée des services offerts.

1.2  ORGANISATION DU DOCUMENT

Le chapitre 2 indique les conditions d’utilisation, les limitations et les possibilités de l’API.

Le chapitre 3 décrit les périmètres des données de l’API, ainsi que les concepts généraux valables sur la
plupart des services.

Le chapitre 4 détaille le fonctionnement de chaque service, ainsi que les objets manipulés (arrêts, lignes,
…) et leur représentation dans l’API.

Open Data : API Tisséo

Page : 4/38

Documentation développeur

Version API : 2
Date : 21/05/2025

2.  MODES ET CONDITIONS D’UTILISATION

2.1  MODE DE MISE EN ŒUVRE ET FORMATS

L’API Tisséo est un webservice de type REST en « lecture seule ».  REST est un style d’architecture qui
repose sur le protocole HTTP : on accède à une ressource par son URI unique. Seule les requêtes http
de type GET sont acceptée par l’API

Le point d’entrée de l’api est : api.tisseo.fr
L’API  est  versionnée,  et  la  version  courante  est  v2.  Des  changements  importants  ont  eu  lieu  entre  la
v1.X et la v2. La version 2 n’est pas entièrement compatible v1.

Les appels à l’API sont de la forme :

https://api.tisseo.fr/v2/<nom du service>.<format>?<paramètres>&key=<votre_clé>

Le protocole d’appel de l’API est https.

Retrouvez la liste des services et leurs paramètres au chapitre 4.
Les formats de réponses sont : XML ou JSON, le type mime renvoyé sera adapté en fonction.
Vous devez passer une clé « key » à chaque appel (voir paragraphe suivant.)

L’encodage supporté est UTF-8 .

Outils de développement
Lors du développement d’une application, il vous sera utile de tester l’API avec votre navigateur Web.

Comme les réponses JSON de l’API sont compressées (voir section 3.10), nous vous recommandons
d’utiliser un plugin de présentation comme JSONView sous Firefox ou Chrome ou un client REST
complet comme Postman.

2.2  CLES D’ACCES

L’appel  à  l’API  est  soumis  à  l’utilisation  d’une  clé  attribuée  à  chaque  demandeur.  Cette  clé  doit  être
transmise lors de chaque appel.

Pour obtenir une clé, merci d’envoyer un mail à opendata@tisseo.fr en indiquant :





vos références : nom, prénom et/ou entreprise
votre mail (pourra être utilisé pour communiquer des informations sur les API)
vos utilisations prévues (nom de projet ? objectifs ?)

Pour  des  raisons  de  simplification,  les  exemples  de  liens  fournis  dans  cette  documentation n’indiquent
pas le paramètre key, qui est pourtant systématiquement nécessaire.

Open Data : API Tisséo

Page : 5/38

Documentation développeur

Version API : 2
Date : 21/05/2025

2.3  QUOTAS D’UTILISATION ET PARTAGE DES RESSOURCES

L’API OpenData Tisséo connait un succès grandissant.
Les services délivrés par l’API sont assurés par des infrastructures informatiques mises à disposition par
Tisséo.
Afin de maintenir un bon niveau de service, Tisséo surveille le taux d’utilisation de son infrastructure pour
chaque clé délivrée.

S’il  s’avérait  nécessaire  d’accroitre  notablement  les  capacités  de  l’infrastructure  en  raison  de
sollicitations accrues, Tisséo pourrait être amené à mettre en place un système de limitation des
usages gratuits, impliquant une participation financière au dela de certains seuils.
Le contrôle sera effectué par clé et par période.

2.4  LICENCE

Les  données  accessibles  via  notre  API  sont  sous  licence  ODBL  (https://data.toulouse-metropole.fr/la-
licence).

2.5  PROPRIETE INTELLECTUELLE ET USAGE DE LA MARQUE TISSEO

L’utilisation de l’API oblige au strict respect du Code de la propriété intellectuelle (articles L.335-2 ) et des
mentions légales TISSEO (http://www.tisseo.fr/mentions-legales).
A ce titre, toute utilisation abusive dans le nom d’une application du terme « TISSEO», (qui est une
marque déposée et protégée dont l'usage exclusif est la propriété de TISSEO) est proscrite.

2.6  CREDIT OPENSTREETMAP

Les informations routières  (noms  de  rues, numéros  de rues, …) fournies par l’API TISSEO proviennent
du projet OpenStreetMap (http://www.openstreetmap.org/).

Certaines rues ou certains numéros de rues ne sont pas encore connus d’OpenStreetMap et seront donc
inaccessibles  via  notre  API.  C’est  pourquoi  nous  encourageons  vivement  les  utilisateurs  de  l’API  à
contribuer à l’amélioration des données OpenStreetMap.
Nous réalisons des mises à jour quotidiennes qui contiendront vos contributions.
Dans  le  détail,  nous  n’importons  les  numéros  de  rues  que  sur  des  nodes  (addr:housenumber)  et  les
nodes en relation à une rue (associatedStreet) et non pas sur les buildings.

2.7  INTEGRATION WEB ET INTRANET

Il  vous est possible  d’utiliser  non seulement l’API OpenData  pour des  applications  natives (mobiles, ou
client lourd), mais aussi dans des sites Web ou intranet.
Dans ce  cas,  vous  pourrez  effectuer des requêtes « cross-domain »  directement en Javascript (c’est-à-
dire depuis votre site web vers api.tisseo.fr).
En  effet,  l’API  Tisséo  renvoit  les  header  CORS  qui  indiquent  au  navigateur  que  ces  requêtes  sont
autorisées.

Dans le cas d’un site Web, votre clé d’API sera exposée au public.
Nous ne considérons pas cela comme un problème puisque les clés sont disponibles sans restriction et
gratuitement sur simple demande (voir 2.2).

Nous sommes prêts à vous transmettre une  nouvelle clé en  cas d’utilisation  abusive  de la  votre par un
tiers.

Open Data : API Tisséo

Page : 6/38

Documentation développeur

Version API : 2
Date : 21/05/2025

3.  CONCEPTS GENERAUX

3.1  PERIMETRE GEOGRAPHIQUE DES DONNEES

Les données de l’API couvrent le perimètre de l’aire urbaine dans sa définition INSEE 2010 ainsi que la
Haute-Garonne.

3.2  PERIMETRE TEMPOREL DES DONNEES

Les  données  Transport  Tisséo  sont  mises  à  jour  quotidiennement  voire  en  temps  réel  (horaires  de
passages bus et tram équipés de GPS).
L’horizon temporel des données est de 30 jours, mais nous préconisons un usage à 15 jours car l’offre à
30 jours peut changer avant application.

Toutes  les  réponses  de  l’API  contiennent  un  paramètre  « expirationDate »  qui  indique  jusqu’à  quand
l’information récupérée reste valable.
Il  est  fortement  recommandé  d’utiliser  ce  paramètre  pour  gérer  la  durée  du  cache  de  vos
applications.

3.3  LIGNES TISSEO DISPONIBLES

Toutes les lignes Tisséo sont disponibles dans l’API excepté :




les lignes scolaires
les navettes sportives : Wallon et Stadium
Cependant, les infos réseau couvrent ces lignes (voir 4.10)

Open Data : API Tisséo

Page : 7/38

Documentation développeur

Version API : 2
Date : 21/05/2025

3.4  SRID

Un  identifiant  de  référence  spatiale  ou  SRID  (  Spatial  Reference  Identifier)  est  un  identifiant  unique
associé à un système de coordonnées. En effet, il existe de nombreuses techniques de projections de la
terre sur un plan et en fonction du choix de la projection, le système de coordonnées diffère.
(Plus d’info : https://en.wikipedia.org/wiki/SRID,
http://fr.wikipedia.org/wiki/Système_de_coordonnées_cartographie)

Le SRID  par  défaut  dans  l’API  est  4326  ce  qui  correspond  au  système  WGS84,  utilisé  notamment
par le système GPS.

L’API  Tisséo  supporte  la  plupart  des  systèmes  de  coordonnées  existants  et  en  particulier  les  plus
répandus : Lambert 2, Google Spherical Mercator, …
Si vous passez un SRID aux services, il sera à la fois utilisé pour interpréter vos paramètres (par exemple
« bbox » de la section suivante) et pour écrire la réponse (XY d’arrêts par exemple).

3.5  BOUNDING BOX

Plusieurs services permettent de rechercher des objets par zone géographique ou « bounding box ».

Le  format  attendu pour  une  « bbox »  est  :  « longitude  pt  A,  latitude  pt  A,  longitude  point  B,  latitude
point B », où A et B sont positionnés comme sur le schéma suivant :

Représentation d’une bbox sur un fond cartographique

Les  coordonnées  de  la  « bbox »  doivent  être  exprimées  dans  le  système  de  coordonnées  définit  par  le
srid passé en paramètre (voir section précédente).
Exemple en WGS84 (SRID 4326) :

Exemple en Google Spherical Mercator (SRID 900913) :

bbox=1.4338121,43.5944292,1.4538121,43.6144292

bbox=138755.178369,5395670.788034,181368.821631,5413060.211966

3.6  GEOMETRIES WKT

Les tracés géométriques filaires renvoyés par les services (lignes, calcul d’itinéraire) sont en WKT (Well
Know Text) exprimés dans le SRID passé en paramètre (voir plus haut)
Exemple en WGS84 (SRID 4326) :

LINESTRING (1.44210 43.57988, 1.44250 43.58040, 1.44265 43.5805)

Open Data : API Tisséo

Page : 8/38

Documentation développeur

Version API : 2
Date : 21/05/2025

3.7   ACCESSIBILITE

L’accessibilité aux PMR (Personnes à Mobilité Réduite) est une préoccupation majeure des opérateurs
de transport comme Tisséo.
La notion d’accessibilité disponible dans l’API signifie : accessible aux personnes en fauteuil roulant.

L’accessibilité s’applique aux arrêts, aux véhicules et aux entrées de stations de métro (les ascenseurs
peuvent tomber en panne ou être en maintenance).

Dans la version actuelle de l’API vous retrouverez l’accessibilité :

  Sur les StopPoints avec le champ handicappedCompliance (voir 4.3)
  Sur le calcul d’itinéraire avec le paramètre roadMode=wheelchair

Les informations de disponibilité des ascenceurs sont prises en compte dans le calcul
d’itinéraire.

Vous retrouverez aussi l’information d’accessibilité des arrêts dans notre fichier statique au format GTFS
disponible sur le portail OpenData de Toulouse Métropole.

3.8  DATE & TIME

L’heure de l’API est l’heure de Paris.

Les dates en entrée comme en sortie s’expriment de la façon suivante :

YYYY-MM-DD

Les « datetime » qui expriment la date et l’heure s’expriment soit :

YYYY-MM-DD hh:mm

soit :

YYYY-MM-DD hh:mm:ss

Exemple :

« 2022-01-16 14:25 »

Open Data : API Tisséo

Page : 9/38

Documentation développeur

Version API : 2
Date : 21/05/2025

3.9  IDENTIFIANTS

3.9.1

Unicité et type

Les  identifiants  « id »  sont  des  chaines  de  caractères  uniques  qui  définissent  tous  les  objets  du
référentiel.
Un  identifiant  est  unique  même  entre  des  objets  de  types  différents  (une  ligne  et  un  arrêt  ne  peuvent
pas avoir le même id).

3.9.2

Validité dans le temps

Les identifiants restent valides dans le temps.
Exemples :



l’arrêt logique « Esquirol » aura toujours l’id « stop_area:SA_1033 »
la ligne « T1 » aura toujours l’identifiant « line:38 »

Cette propriété de durabilité des identifiants est utilisée pour assurer la correspondance avec les fichiers
OpenData (voir section ci-dessous). Cela permet aussi une synchronisation de données efficace.

3.9.3

Cohérence des ID avec les fichiers OpenData

En  plus  de  l’API  temps  réel,  Tisséo  fourni  des  fichiers  descriptifs  de  son  offre  transport  sur  le  portail
OpenData de Toulouse Métropole.
Ces  fichiers  sont  disponibles  aux  formats  standard  Trident  et  GTFS  sous  la  même  licence  ODBL  (voir
paragraphe 2.4).
Voici les URL pour récupérer ces fichiers :

  Format GTFS :

https://data.toulouse-metropole.fr/explore/dataset/tisseo-gtfs/information/

  Format Trident :

https://data.toulouse-metropole.fr/explore/dataset/tisseo-offre-de-transport-neptune/information/

Les fichiers sont mis à jour tous les lundis.

Afin d’étendre les possibilités d’utilisation de l’API, les identifiants GTFS sont identiques à ceux de
l’API.

Ainsi par exemple, vous pourrez récupérer les tracés cartographiques des lignes dans le fichier GTFS et
faire un affichage cartographique des lignes avec les informations temps réel de l’API.
Vous  pouvez  également  charger  en  cache  dans  vos  applications  tous  les  horaires  théoriques  via  les
fichiers et faire une correction temps réel de ces horaires avec l’API.

Open Data : API Tisséo

Page : 10/38

Documentation développeur

Version API : 2
Date : 21/05/2025

3.10 VERSION COMPRESSEE

La compression est un concept de l’API.

En effet, si nos sorties JSON ne contiennent déjà pas d’espaces ni de retour chariot afin d’en diminuer la
taille, les noms des champs et certaines valeurs peuvent êtres longues.

Afin d’augmenter encore la performance de l’API, nous avons introduit des  champs « compressés » qui
minimisent le nombre de caractères.

Pour le moment, seule la requête place en bénéficie, mais d’autres services suivront.

3.10.1

 Type des lieux publics

Les  types  de  lieux  publics  sont  décrits  par  une  ou  deux  lettres  suivant  la  table  de  correspondance
suivante :

typeCompressed
a
b
c
d
e
fd
fe
ff
g
h
i
j
k
l
m
n
o
p
qa
qb
qc
r
s
t
u
v

Type
Administration
Poste
Enseignement
Hôpital
Police
Eglise
Mosquée
Synagogue
Cimetière
Gare routière
Gare ferroviaire
Aéroport
VélôToulouse
Parking
Parc relais
Agence Tisséo
Commerçants partenaires
Faculté
Stade de football
Stade de rugby
Autre installation sportive
Loisirs, culture
Jardin public
Citiz
Parc à vélo
Station de covoiturage

Open Data : API Tisséo

Page : 11/38

Documentation développeur

Version API : 2
Date : 21/05/2025

3.11  OBJETS NOMMABLES

Pour identifier un objet de  l’API (arrêt, rue, lieux public, …) il est possible  de le faire par nom (avec la
commune), ou par XY.

Ainsi  par  exemple,  vous  pouvez  lancer  un  itinéraire  depuis  une  position  vers  un  lieu  nommé  « Capitole
TOULOUSE ».

Le mécanisme de correspondance entre un nom (ou XY) et un objet est toujours le même dans tous les
services de l’API.
Le service d’autocomplétion/géocodage « place » vous permet de voir quel est l’objet trouvé pour ce XY
ou ce nom en regardant le meilleur résultat (voir 4.4).

Par exemple « esquir » est passé comme point de départ d’un calcul d’itinéraire (ou comme point central
pour service_density), alors le point de départ véritablement utilisé sera l’objet renvoyé par « place » soit
le StopArea Esquirol.
De même un XY comme point de départ peut être un peu éloigné de la voirie, et c’est un appel a places
qui sera effectué dans les autres services pour retrouver un objet de l’API avant de lancer un calcul.

Il peut arriver que le nom d’un objet ne soit pas unique (ex : Voie dans nom, parking, …) dans ce cas le
comportement n’est pas défini.
Si vous lancez un calcul d’itinéraire depuis un tel point, vous devez passer le XY.

Open Data : API Tisséo

Page : 12/38

Documentation développeur

Version API : 2
Date : 21/05/2025

4.  OBJETS ET SERVICES

4.1  MODELE DE DONNEES

Voici un modèle de donnée « transport public » simplifié :

Sur ce schéma, vous pouvez voir des Lines, des itinéraires, des StopPoints et des StopArea.

Les Lines sont des lignes commerciales (exemple : ligne T1, ligne 2, …).
Une  Line  appartient  à  un  réseau  de  transport :  network.  Dans  l’API  le  network  vaudra  toujours
« Tisséo ». Cependant, l’objet « network » a été ajouté en prévision d’une ouverture à d’autres réseaux.

Une Line a un transportMode ou RollingStock : bus, métro, tramway, transport à la demande.

Chaque Line est composée d’un ou de plusieurs itinéraires, généralement au moins un aller retour, mais
parfois plus pour les lignes à fourches ou à parcours spécifiques.

Un itinéraire dessert des StopPoints (ou PhysicalStops) qui correspondent à des poteaux d’arrêts.

Dans le cas général, il y a au moins deux StopPoints face à face (un de chaque côté de la rue pour
chaque sens) regroupés dans un Stop Area (ou Arrêt logique).
Un Stop Area porte la dénomination commerciale. C’est à cet objet « nommable » (voir 3.12) qu’un
usager fait allusion lorsqu’il dit « Je pars d’Esquirol ».
Les correspondances entre les StopPoints d’un même Stop Area sont toujours possibles.

Des messages d’information trafic peuvent affecter des Lines ou être globales (Voir 4.10)

Autres objets non « transport public » de l’API
Road : une rue exemple « Rue de Metz (TOULOUSE)»
Address : une rue et un numéro, exemple « 4 impasse Paul Mesplé (TOULOUSE)»
Public Place : un lieu public, exemple « Zénith (TOULOUSE)», « Ecole Lamartine (TOULOUSE)»

Open Data : API Tisséo

Page : 13/38

Documentation développeur

Version API : 2
Date : 21/05/2025

4.2  STOP_AREAS : ZONES D’ARRETS

4.2.1

Principe

Ce service permet d’obtenir des zones d’arrêts d’un réseau, d’une zone géographique, ou d’une ligne.

Une « zone d’arrêt » est le regroupement de plusieurs « poteaux d’arrêts » proches sous un même nom
commercial (voir 4.1).

4.2.2

Mode d’appel et Paramètres

URL : https://api.tisseo.fr/v2/stop_areas.<format>?...paramètres...

Nom
network
srid
bbox

displayLines
displayCoordXY

lineId
terminusId

displayStopPoints

Description du paramètre
Opérateur de transport
système de coordonnées (Voir section 3.4)
Filtre pour les arrêts dont les données GPS sont
comprises dans cette bounding box (voir 3.5)
Retourne en plus les lignes de chaque arrêt
Retourne  en  plus  les  coordonnées  de  chaque
arrêt. C’est le barycentre des arrêts de la zone.
Filtre sur les arrêts de la ligne uniquement.
Filtre  sur  les  zones  d’arrêts  arrivant  et  partant
de ce terminus uniquement
Affiche les arrêts physiques qui appartiennent à
l’arrêt

Requis ?  Valeur défaut
Non
Non
Non

Tisséo
4326

Non
Non

Non
Non

Non

0 : Pas de ligne
0 : Pas de
coordonnées

0

4.2.3

Règles de gestion

Si  lineId  est  passé  en  plus  avec  terminusId,  dans  ce  cas  le  filtre  porte  sur  tous  les  itinéraires  de  cette
ligne ayant ce terminusId.

Remarque : dans le  cas général le  XY d’une  zone  d’arrêt est le barycentre des poteaux d’arrêts qui la
composent.

Open Data : API Tisséo

Page : 14/38

Documentation développeur

Version API : 2
Date : 21/05/2025

4.2.4

Réponse : Stop_area

Stop_area, description

Nom du champ

Type

Description

name
id
cityName
x
y
stops

Nom de l’arrêt
string
Identifiant unique (voir section 3.9)
string
string
Nom de la commune à laquelle appartient l’arrêt
double  « latitude » exprimé dans un srid donné (voir section 3.4)
double  « longitude » exprimé dans un srid donné (voir section 3.4)
liste

Liste des stop_points de l’arrêt

Toujours
affiché ?
oui
oui
oui
oui
oui
non

Stop_area, JSON

{
    "cityName": "BEAUZELLE",
    "id": "stop_area:SA_624",
    "name": "Aéroconstellation",
    "x": "1.362642",
    "y": "43.663088"
}

4.2.5

Exemples d’utilisation

Liste de toutes les zones arrêts au format XML
https://api.tisseo.fr/v2/stop_areas.xml

Liste de toutes les zones d’arrêts au format json
https://api.tisseo.fr/v2/stop_areas.json

Liste de toutes les zones d’arrêts au format xml avec les lignes du réseau Tisséo qui les desservent
https://api.tisseo.fr/v2/stop_areas.xml?displayLines=1

Liste de toutes les zones d’arrêts au format xml avec les lignes du réseau Tisséo ayant ce terminus
https://api.tisseo.fr/v2/stop_areas.xml?displayLines=1&terminusId=stop_area:SA_206

Liste  de  toutes  les  zones  d’arrêts  au  format  xml  avec  lignes  qui  les  desservent  et  les  coordonnées
géographiques de l’arrêt du réseau Tisséo
https://api.tisseo.fr/v2/stop_areas.xml?displayLines=1&displayCoordXY=1

Liste de toutes les zones d’arrêts contenues dans une bbox au format json
https://api.tisseo.fr/v2/stop_areas.json?srid=900913&bbox=158019.352839%2C5403458.895141%2C16
3077.902207%2C5404988.302709

Open Data : API Tisséo

Page : 15/38

Documentation développeur

Version API : 2
Date : 21/05/2025

4.3  STOP_POINTS : ARRETS (POTEAUX D’ARRETS)

4.3.1

Principe

Ce  service  permet  d’obtenir  les  poteaux  d’arrêts  (ou  arrêts  physiques)  d’un  réseau,  d’une  zone
géographique ou d’une zone d’arrêt.

4.3.2

Mode d’appel et Paramètres

URL : https://api.tisseo.fr/v2/stop_points.<format>?...paramètres...

Nom
network
srid
bbox

sortByDistance

number

displayDestinations

displayLines

displayCoordXY

lineId
stopAreaId

Non

le  nb  maxi  de  résultats  à

Description du paramètre
Opérateur de transport
système de coordonnées (Voir section 3.4)
Filtre  pour les arrêts dont les données GPS
sont  comprises  dans  cette  bounding  box
(voir 3.5)
Tri  résultats  selon  la  distance  au  centre  de
la bounding box (0,1)
Filtre  sur
retourner
Retourne  en  plus
chaque poteau (0/1)
Retourne  en  plus  les  lignes  de  chaque
destination (0/1)
Retourne  en  plus
les  coordonnées  de
chaque  arrêt  (poteau  d’arrêt  et    arrêt
logique) (0/1)
Filtre sur les arrêts de la ligne uniquement.  Non
Filtre sur la zone d’arrêt uniquement définie  Non

les  destinations  de

Non

Non

Requis ?  Valeur défaut
Non
Non
Non

Tisséo
4326

0

tous

Retourne
les résultats
0 : Pas de
destinations
0 : Pas de lignes

0 : Pas de
coordonnées

4.3.3

Règles de gestion

Ce service  ne sert pas à récupérer tous les arrêts Tisséo d’un coup !
Si vous avez nesoin de ça, utilisez notre GTFS, et lisez le fichier stops.txt.

Si vous appelez le service stop_points sans bbox, lineId ou stopAreaId valide, alors vous recevrez malgrè
tout une réponse valide. Les performances de la plateforme peuvent cependant s’en trouver affectées.
sortByDistance ne fonctionne que si une bbox est fournie.

Open Data : API Tisséo

Page : 16/38

Documentation développeur

Version API : 2
Date : 21/05/2025

4.3.4

Réponse : Stop_point

Stop_point, description

Nom du champ

Type

Description

string
string

name
id
handicappedCompliance  bool
(0/1)
double  « latitude » exprimée dans un srid donné (voir section 3.4)
double  « longitude » exprimée dans un srid donné (voir section 3.4)
list

Nom de l’arrêt physique
Identifiant unique (voir section 3.9)
Accessibilité de l’arrêt aux PMR (voir section 3.7)

x
y
operatorCodes

stopArea
*ces codes apparaissent en haut des poteaux d’arrêts sur le réseau Tisséo

object

Liste des codes internes au réseau de l’arrêt*
Zone d’arrêt à laquel l’arrêt physique appartient

Toujours
affiché ?
oui
oui
oui

oui
oui
non

non

Stop_point, JSON

{
    "id": "stop_point:SP_2909",
    "name": "Dugay Trouin",
    "handicappedCompliance": "1",
    "x": "1.460312004773155",
    "y": "43.572806000022744",
    "operatorCodes": [
        {
            "operatorCode": {
                "value": "2070",
                "network": "Tisséo"
            }
        }
    ],
    "stopArea": { … }
}

4.3.5

Exemples d’utilisation

Liste de tous les poteaux au format XML
https://api.tisseo.fr/v2/stop_points.xml

Liste de tous les poteaux de ce stopArea au format xml du réseau Tisséo
https://api.tisseo.fr/v2/stop_points.xml?stopAreaId= stop_area:SA_206&network=Tisséo

Liste de tous les poteaux au format json
https://api.tisseo.fr/v2/stop_points.json

Liste de tous les poteaux d’arrêts d’un arrêt commercial où passe une ligne donnée
https://api.tisseo.fr/v2/stop_points.json?stopAreaId=stop_area:SA_206&displayLines=1&lineId= line:7

Liste de tous les poteaux au format json avec les destinations du réseau tisséo
https://api.tisseo.fr/v2/stop_points.json?displayDestinations=1

Liste  de  tous  les  poteaux  au  format  json  avec  les  destinations  dans  une  bounding  box  pour  un  srid
donnée du réseau tisséo.
https://api.tisseo.fr/v2/stop_points.json?displayDestinations=1&srid=900913&bbox=158019.352839%2C5
403458.895141%2C163077.902207%2C5404988.302709

Open Data : API Tisséo

Page : 17/38

Documentation développeur

Version API : 2
Date : 21/05/2025

4.4  PLACES : RECHERCHE DE LIEUX ET GEOCODAGE

4.4.1

Principe

Ce service permet à partir d’un texte (ou d’un point X, Y, ou d’une zone géographique) d’obtenir une liste
de lieux pouvant correspondre. Les lieux retournés peuvent être des rues, des arrêts, des lieux publics ou
des communes connus par notre système.
« Places »  ne  se  contente  pas  de  rechercher  les  lieux  contenant  exactement  la  chaîne  de  caractères
transmise, mais effectue une recherche plus large intégrant des prononciations proches par exemple.

Elle peut être efficacement utilisée :

  dans un objectif d’autocomplétion sur un champ de type lieu
  pour de la géolocalisation

4.4.2

Mode d’appel et Paramètres

URL : https://api.tisseo.fr/v2/places.<format>?...paramètres...

Nom

Description du paramètre

Requis ?  Valeur
défaut

term
network
coordinatesXY

maxDistance

srid

bbox

number

Texte (3 caractères minimum)
Opérateur de transport
Retourne  les  adresses  les  plus  proches  de  ce
point de coordonnées x, y triées par distance
laquelle  s’effectue
Distance  autour  de
recherche
Système de coordonnées (Voir section 3.4)

la

Filtre  les  lieux  dont  les  données  GPS  sont
comprises dans cette bounding box (Voir section
3.5)
Filtre sur le nb maxi de résultats à retourner par
type de lieu

displayBestPlace
displayOnlyStopAreas

displayOnlyRoads

displayOnlyAddresses

Retourne le meilleur résultat en premier (0/1)
Retourne uniquement les lieux dont le className
est « stop » (0/1)
Retourne uniquement les lieux dont le className
est « road » (0/1)
Retourne uniquement les lieux dont le className
est « adress »  (0/1)

Non
Non
Non

Non

Non

Non

Non

Non
Non

Non

Non

displayOnlyPublicPlaces  Retourne uniquement les lieux dont le className

Non

displayOnlyCities

lang
simple
publicPlaceFilter

est « public_places » (0/1)
Retourne uniquement les lieux dont le className
est « city »  (0/1)
Non
Choix de la langue (fr/en/es)
Formatage de la sortie json pour jquery
Non
Liste du type de lieux public qu’on souhaite filtrer  Non

Non

Tisséo

300m

4326

les

Retourne
tous
résultats
0
0 : Pas de
restriction
0 : Pas de
restriction
0 : Pas de
restriction
0 : Pas de
restriction
0 : Pas de
restriction
fr
0

Open Data : API Tisséo

Page : 18/38

Documentation développeur

Version API : 2
Date : 21/05/2025

4.4.3

Règles de gestion

Les  requêtes  d’autocomplétion  (paramètre  Term)  avec  moins  de  3  caractères  sont  interdites,  tenez-en
compte dans votre implémentation

Un  des  2  paramètres  term  ou  coordinatesXY  doit  être  fourni.  Ils  doivent  être  utilisés  de  manière
exclusive, dans le cas contraire c’est l’option coordinatesXY qui est prise en compte uniquement.

Avec l’option displayBestPlace le meilleur résultat est toujours celui qui est affiché en premier.

Les  options  displayOnlyStopAreas,  displayOnlyRoads,  displayOnlyAddresses,  displayOnlyPublicPlaces,
displayOnlyCities ne peuvent pas êtres combinées entre elles, elles sont à utiliser de manière exclusive.

Si coordinatesXY est utilisé alors seulement des Roads ou des Address seront retournées (pour connaitre
les arrêts autour d’un XY, utilisez le service « stop_areas » avec une bbox).

Valeurs possibles :
simple : 1, 0
Mettre  simple=1  permet  de  supprimer  les  entêtes  json,  afin  d’obtenir  un  format  json  formaté  pour
pouvoir  nativement  être  exploité  par  JQuery  autocomplete  (ou  d’autres  librairies  comme  Dojo  par
exemple) avec les catégories : http://jqueryui.com/demos/autocomplete/#categories

Attention : Dans le cas d’une recherche par bbox, seuls les lieux de type « road », « stop » et
« public_places » seront renvoyés

publicPlaceFilter : liste de lieux publics référence par leur typeCompressed séparés par des pipe ‘|’.
La correspondance entre les “typeCompressed” et les type est indiquée à la section 3.10.

Exemples :
publicPlaceFilter=a|p|s  renverra uniquement des administrations, universités et jardins publics
publicPlaceFilter=d renverra uniquement des hôpitaux

4.4.4

Réponses : Stop, Road, Public_place, Address, City

Les  réponses  sont  ordonnées  dans  cet  ordre  :  meilleur  résultat  (qui  peut  être  de  n’importe  quelle  des
catégories), arrêt, adresse, rue, point d’intérêt (lieu publics), communes. Dans chaque catégorie il peut y
avoir plusieurs résultats triés par ordre de pertinence.

Le rank numérote simplement cet ordre.

Stop, description
La description de stop est présentée au 4.2.4

Road, description

Nom du champ

Type

Description

label
category
key
className
x
y
rank

Nom de l’objet à presenter à l’utilisateur
catégorie “road”
Chaine de caractère identifiant l’objet (voir section 3.11)
road

string
string
string
string
double  « latitude » exprimée dans un srid donné (voir section 3.4)
double  « longitude » exprimée dans un srid donné (voir section 3.4)
integer  Ordre dans la réponse

Open Data : API Tisséo

Page : 19/38

Toujours
affiché ?
oui
oui
oui
oui
oui
oui
oui

Documentation développeur

Version API : 2
Date : 21/05/2025

Public_place, description

Nom du champ

Type

Description

label
cityName
postcode
address
key
category
className
x
y
typeCompressed
type
veloStation

Nom du lieu (suivi de la commune)
Nom de la commune du lieu public
Code postal du lieu s’il est connu
Numéro et voirie du lieu, s’ils sont connus
Chaine de caractère identifiant l’objet (voir section 3.11)
catégorie “public_place”
public_place

string
string
string
string
string
string
string
double  « latitude » exprimée dans un srid donné (voir section 3.4)
double  « longitude » exprimée dans un srid donné (voir section 3.4)
Catégorie technique du lieu public (voir section 3.10)
string
Catégorie lisible par un humain
string
int
Identifiant JCDecaux de la station de vélôToulouse*

*permet de faire un appel à l’API open data JCDecaux pour les places disponibles

Public_place, JSON
{
    "label": "LOIS ESQUILE (TOULOUSE)",
    "key": "LOIS ESQUILE TOULOUSE",
    "x": "1.441331",
    "y": "43.606213",
    "typeCompressed": "k",
    "type": "VélôToulouse",
    "cityName": "TOULOUSE",
    "veloStation": "13"
}

Address, description

Nom du champ

Type

Description

label
category
key
className
x
y
rank

Nom de l’objet à presenter à l’utilisateur
catégorie « address »
Chaine de caractère identifiant l’objet (voir section 3.11)
address

string
string
string
string
double  « latitude » exprimée dans un srid donné (voir section 3.4)
double  « longitude » exprimée dans un srid donné (voir section 3.4)
integer  Ordre dans la réponse

City, description

Nom du champ

Type

Description

label
category
key
className
x
y
rank

Nom de l’objet à presenter à l’utilisateur
catégorie “city”
Chaine de caractère identifiant l’objet (voir section 3.11)
city

string
string
string
string
double  « latitude » exprimée dans un srid donné (voir section 3.4)
double  « longitude » exprimée dans un srid donné (voir section 3.4)
integer  Ordre dans la réponse

Toujours
affiché ?
oui
non
non
non
oui
oui
oui
oui
oui
oui
non
non

Toujours
affiché ?
oui
oui
oui
oui
oui
oui
oui

Toujours
affiché ?
oui
oui
oui
oui
oui
oui
oui

Open Data : API Tisséo

Page : 20/38

Documentation développeur

Version API : 2
Date : 21/05/2025

4.4.5

Exemples d’utilisation

Objets correspondant au texte ‘’cav ‘’ au format XML
https://api.tisseo.fr/v2/places.xml?term=cav

Liste  des  adresses
https://api.tisseo.fr/v2/places.json?srid=900913&coordinatesXY=161710.27873%2C5401135.68964&nu
mber=5

triées  par  distance  d’un  point  géographique  donné

les  plus  proches

Rues correspondant au texte ‘’cav ‘’ au format XML
https://api.tisseo.fr/v2/places.xml?term=cav&displayOnlyRoads=1

Objets correspondant au texte ‘’cav ‘’ au format json
https://api.tisseo.fr/v2/places.json?term=cav

Open Data : API Tisséo

Page : 21/38

Documentation développeur

Version API : 2
Date : 21/05/2025

4.5  NETWORKS : RESEAUX DE TRANSPORT DISPONIBLES

4.5.1

Principe

Ce service permet d’obtenir les réseaux de transport disponibles.
Les  id  des  réseaux  obtenus  pourront  être  utiles  dans  les  autres  services  de  l’API,  via  le  paramètre
network List.
Aujourd’hui seul le réseau  Tisséo est disponible, mais d’autres réseaux de transport régionaux pourront
être ajoutés ultérieurement.

4.5.2

Mode d’appel et Paramètres

URL : https://api.tisseo.fr/v2/networks.<format>?...paramètres...

Nom

Description du paramètre

Requis ?  Valeur défaut

Ce service ne prend aucun paramètre

4.5.3

Réponse : Network

Network, description

Nom du champ

Type

Description

name
id

string
string

Nom du réseau
Identifiant unique (voir section 3.9)

Network, XML

Toujours
affiché ?
oui
oui

expirationDate="2013-12-27

<networks
instance" xsi:noNamespaceSchemaLocation="https://api.tisseo.fr/xsd/networks.xsd">
   <network name="Tisséo" id="network:1" />
</networks>

03:45"

xmlns:xsi="https://www.w3.org/2001/XMLSchema-

Network, JSON
 {
{

expirationDate: "2014-12-27 03:45",
networks:
[

{

name: "Tisséo",
id: "network:1"

          }
     ]
}

Open Data : API Tisséo

Page : 22/38

Documentation développeur

Version API : 2
Date : 21/05/2025

4.6  LINES : LES LIGNES COMMERCIALES

4.6.1

Principe

Ce service permet d’obtenir la liste de toutes les lignes disponibles sur le réseau. Il permet également de
connaitre les perturbations qui affectent les lignes ou de filtrer seulement celles qui sont perturbées.

4.6.2

Mode d’appel et Paramètres

https://api.tisseo.fr/v2/lines.<format>?...paramètres...
ou
https://api.tisseo.fr/v2/lines/<id>.<format>?...paramètres...

Nom
Network
lineId *
shortName
displayTerminus

displayMessages

displayOutages

displayOnlyDisrupted

displayGeometry
contentFormat

Description du paramètre
Opérateur de transport
Filtre sur une seule ligne par son ID
Filtre sur une seule ligne par numéro de ligne
Retourne en plus les arrêts logiques terminus de
chaque ligne (0/1)
Retourne  en  plus  les  messages  de  perturbation
de ligne (pour les lignes qui en ont)
Retourne
plus
d’indisponibilité des ascenseurs et escalators
Ne
perturbation en cours
Renvoi la géométrie des lignes en WKT
Format du contenu des messages

lignes  ayant  une

retourne  que

informations

les

les

en

Tisséo

Requis ?  Valeur défaut
Non
Non
Non
Non

0

Non

Non

Non

Non
Non

0

0

0

0
text

*Il est aussi possible d’utiliser la syntaxe RestFULL :
https://api.tisseo.fr/v2/lines/line:61.json
au lieu de
https://api.tisseo.fr/v2/lines.json?lineId=line:61

4.6.3

Règles de gestion

Valeurs possibles

shortName : A, 8, 34, T1, …
contentFormat: text, html

Si displayOnlyDisrupted=1 alors seules les lignes pour lesquelles il y a un message apparaitront.

Si displayMessages=1, vous verrez alors les messages de perturbation de la ligne (voir 4.10).

Open Data : API Tisséo

Page : 23/38

Documentation développeur

Version API : 2
Date : 21/05/2025

Line, description

Nom du champ

Type

Description

4.6.4 Réponse : Line

id
shortName
name
network
Color
bgXmlColor
fgXmlColor

String
String
String
String
String
String
String

Identifiant unique (voir section 3.9)
Numéro de la ligne (21, A, T1, L16, …)
Nom commercial de la ligne
Nom du réseau (Tisséo)
Couleur de la ligne en RVB décimal
Couleur de la ligne en RVB hexadécimal (adapté au web)
Couleur du texte de la ligne en RVB hexadécimal*

transportMode

Object  Mode de transport :

Toujours
affiché ?
Oui
Oui
Oui
Oui
Oui
Oui
Oui

Oui

terminus
messages
outages
geometry
*Certaines lignes qui ont une couleur claire (ex : la ligne B) ont un texte noir au lieu de blanc pour être plus lisibles

bus, métro, tramway, Transport à la demande
Les StopArea de destination de chaque itinéraire de la ligne
Les messages d’information réseau qui affectent la ligne
Les informations d’indisponibilté des ascenseurs et escalators
Tracé géométrique de la ligne en WKT (voir section 3.6)

List
List
List
string

Non
Non
Non
Non

Line, JSON
{
    "color": "(0,198,45)",
    "bgXmlColor": "#00c62d",
    "fgXmlColor": "#FFFFFF",
    "id": "line:72",
    "name": "Basso Cambo / Colomiers Airbus",
    "shortName": "21",
    "network": "Tisséo",
    "transportMode": {
        "id": "commercial_mode:3",
        "article": "le",
        "name": "bus"
    },
    "terminus": [
        {
            "id": "stop_area:SA_206",
            "cityName": "TOULOUSE",
            "name": "Basso Cambo"
        },
        {
            "id": "stop_area:SA_713",
            "cityName": "COLOMIERS",
            "name": "Colomiers Gare SNCF"
        },
        {
            "id": "stop_area:SA_482",
            "cityName": "COLOMIERS",
            "name": "Colomiers Airbus"
        }
    ],
    "messages": […],
    "outages": […],
    "geometry": [
        {

Open Data : API Tisséo

Page : 24/38

Documentation développeur

Version API : 2
Date : 21/05/2025

            "wkt": "GEOMETRYCOLLECTION(LINESTRING(1.39204 43.5693, … "
        }
    ]
}

4.6.5

Exemples d’utilisation

Liste de toutes les lignes au format XML (seulement de Tisséo aujourd’hui)
https://api.tisseo.fr/v2/lines.xml

Liste de toutes les lignes du réseau Tisséo au format json
https://api.tisseo.fr/v2/lines.json?network=Tisséo

Liste de toutes les lignes du réseau Tisséo au format json avec les arrêts logiques terminus.
https://api.tisseo.fr/v2/lines.json?displayTerminus=1

Open Data : API Tisséo

Page : 25/38

Documentation développeur

Version API : 2
Date : 21/05/2025

4.7  STOPS_SCHEDULES : PROCHAINS PASSAGES

4.7.1

Principe

Ce  service  permet  d’obtenir  les  prochains  passages  à  un  ou  plusieurs  poteaux  d’arrêt,  ou  à  l’ensemble
des poteaux d’arrêt d’une zone d’arrêt en temps réel.

Les  horaires  « temps  réel »  sont  des  horaires  ré-estimés  en  fonction  des  conditions  de  trafic  et  de  la
position GPS du véhicule.

Un  champ  « realTime »  dans  la  réponse  précise  pour  chaque  horaire  si  il  a  pu  être  ré-estimé
(realTime="yes") ou si l’horaire reste celui indicatif de la fiche horaire (realTime="no").

Le temps réel ne concerne que les Bus et Tramway, les horaires métros étant construits en fonction de la
fréquence de passage.
Aucune information ne sera retournée pour les TAD.

4.7.2

Mode d’appel et Paramètres

URL : https://api.tisseo.fr/v2/stops_schedules.<format>?...paramètres...

Nom
operatorCode
stopPointId
stopAreaId
stopsList

network
number

lineId

displayRealTime

timetableByArea

datetime

maxDays

firstAndLastOfDay

*voir 0

Description du paramètre
Désigne le code opérateur
Désigne le numéro de l’arrêt physique (poteau)
Désigne le numéro de l’arrêt logique (zone)
Désigne  une  liste  de  numéros  d’arrêts  logiques
ou d’arrêts physiques (ou les deux) séparés par
des virgules
Permet de filtrer en plus pour chaque argument
par ligne commerciale ou direction.
Opérateur de transport
Filtre sur le nb maxi de résultats à retourner
ATTENTION :  CET  ARGUMENT  N’A  PAS  LE
MEME  SENS  SUIVANT  LA  VALEUR  DE
« timetableByArea » *
Filtre les arrêts de la ligne uniquement

CET

Permet  de  spécifier  si  on  souhaite  des  horaires
« théoriques » (0) ou « temps réels » (1)
Regroupe les résultats par arrêt logique puis par
couples  (ligne,  destination)  ordonnés  par  heure
de prochain départ
ATTENTION :
TRANSFORME
FORMAT DE SORTIE*
Date et l’heure à laquelle  on souhaite connaitre
les passages  (YYYY-MM-DD HH:MM)
Limite  le  nombre  de  jour  dans  lequel  sont
recherchés les « number » prochains passages
Ne renvoie que le premier et dernier passage de
la journée de service

ARGUMENT
LE

COMPLETEMENT

Requis ?  Valeur défaut
Non
Non
Non
Non

Non
Non

Tisséo
10

Non

Non

Non

Non

Non

Non

tous

Retourne
les résultats
1 : temps réel

0

date  et  heure
courante
7

0

Open Data : API Tisséo

Page : 26/38

Documentation développeur

Version API : 2
Date : 21/05/2025

4.7.3  Règles de gestion

4.7.3.1 Nombre de résultats retournés

Number : le nombre de prochains passages renvoyés (voir 4.7.4)
maxDays : (valuable seulement pour timeTableByArea=1) define la période entre datetime et datetime
+ maxDays * days dans laquelle sont cherché les prochains passages.
Par exemple si une ligne ne fonctionne que le dimanche et que l’API est interrogée un samedi avec un
maxDays de 1 alors elle ne renverra aucun passage, alors qu’avec un maxDays supérieur ou égal à 2 elle
renverra les passages du dimanche.
firstAndLastOfDay : force l’API à ne renvoyer que le premier et le dernier depart de chaque journée de
service (journée qui commence à 3h30 le jour J pour finir à 3h30 le jour J+1).

4.7.3.2 Filtres sur les objets de transport

Le  code  operateur  correspond  au  N°  de  l’arrêt  (poteau  d’arrêt)  indiqué  par  l’opérateur.  S’il  est  fourni,
l’opérateur de transport (network) doit l’être également.
Un et un seul des 4 paramètres operatorCode (et network), stopPointId, stopAreaId ou stopsList doit
être fourni.

        Format pour stopList :

Le format est une liste “d’éléments” séparés par des virgules.
ELEMENT, ELEMENT, ELEMENT, …

Chaque « élément » ayant ce format
ID_STOP

C’est soit un id de stopPoint (arrêt) soit un id de stopArea (zone d’arrêt)
Dans ce dernier cas, ce sont les passages à tous les arrêts de la zone qui seront renvoyés. (par
exemple tous les départs de basso-cambo)

ou

ID_STOP|ID_COMMERCIAL_LINE

On ajoute un filtre sur une ligne commerciale avec le séparateur pipe : « | »

ou

ID_STOP|ID_COMMERCIAL_LINE|ID_STOP_AREA_DESTINATION,

On ajoute un filtre sur une ligne commerciale et sur un arrêt logique (stopArea) de destination.

Exemples :
   « stop_area:SA_1033,stop_point:SP_2209  »  =  les  départs  de  la  zone  Esquirol  (les  deux  sens
donc), plus les départs du poteau d’arrêt « Ateliers métro » direction « Basso Cambo »

   « stop_area:SA_1033|line:6,stop_point:SP_2209 » = les départs de la zone Esquirol (les deux
sens donc) mais seulement pour la ligne 12, plus les départs du poteau d’arrêt « Ateliers métro »
direction « Basso Cambo »

   « stop_area:SA_1033|line:6|stop_area:SA_206  »  =  les  départs  de  la  zone  Esquirol  (les  deux
sens donc) mais seulement pour la ligne 12 et direction « Basso Cambo »

Notez que dans ce dernier cas, c’est équivalent à passer l’id de l’arrêt physique :
« stop_point:SP_3318|line:6|stop_area:SA_206 »

Open Data : API Tisséo

Page : 27/38

Documentation développeur

Version API : 2
Date : 21/05/2025

4.7.4

Réponse : Stop_schedule

Si timeTableByArea=0 (valeur par défaut), alors vous obtenez les N  (N=number) prochains  passages à
un arrêt physique toutes lignes confondues par ordre de passage chronologique.

Si  timeTableByArea=1,  alors  vous  obtenez  les  N  (N=number)  prochains  passages  de  chaque  couple
« ligne/destination ».

La  grande  différence  sera  donc  que  dans  le  premiers  cas  rien  ne  garantit  que  toutes  les  lignes  et
destinations apparaissent dans le résultat.
En effet, imaginez que vous demandiez 5 résultats à un arrêt ou il y a 10 lignes.

Par contre dans le dernier cas, l’affichage n’est pas chronologique, mais d’abord trié par ligne.

ATTENTION  :  Si  timetableByArea=1  alors  le  champ  “realTime”  prendra  les  valeurs  0  ou  1,  sinon  le
champ  “realTime”  prendra  les  valeurs  “yes”  ou  “no”.  Nous  ne  corrigerons  pas  ce  fonctionnement  pour
des raisons de rétrocompatibilité.

4.7.4.1 Lorsque timeTableByArea = 0

La  section  importante  de  la  réponse  est  « departure »  qui  contient  tous  les  horaires  de  passages  à  un
arrêt ainsi que la ligne et sa destination.

Voici un exemple en JSON :

        "departure": [
            {
                "dateTime": "2014-06-29 12:38:49",
                "realTime": "yes",
                "line": {
                    "name": "Empalot / Gleyze-Vieille",
                    "shortName": "54",
                    "network": "Tisséo",
                    "color": "(255,94,22)"
                },
                "destination": [
                    {
                        "name": "Empalot Métro",
                        "cityName": "TOULOUSE"
                    }
                ]
            },
            {
                "dateTime": "2014-06-29 13:08:49",
                …
            },
            …
        ]

Open Data : API Tisséo

Page : 28/38

Documentation développeur

Version API : 2
Date : 21/05/2025

4.7.4.2 Lorsque timeTableByArea = 1

Regroupé  sous  chaque  stopArea  (vous  pouvez  interroger  plusieurs  StopArea  différents  en  une  seule
requête),  vous  aurez  des  « schedules »  qui  indiquent  pour  chaque  couple  « ligne/destination »  les
« number » prochains passages.

Exemple en JSON :
"stopAreas": [

{"name": "Météo",
"id": "stop_area:SA_444",
"cityName": "TOULOUSE",
"cityId": "admin:fr:31555",
"schedules": [

{"stop": {
"id": "stop_point:SP_176",
"name": "Météo",
"operatorCode": "4601"},
"line":

{"id": "line:143",
"shortName": "18",

                       "color": "(255,104,9)",

"bgXmlColor": "#e46809",
                       "fgXmlColor": "#FFFFFF",
                       "style": "orange",
                       "network": "Tisséo"

"name": "Basso Cambo / Cité Scolaire Rive-Gauche"},

"destination":

{"id": "stop_area:SA_206",
"name": "Basso Cambo",
"cityName": "TOULOUSE",
"cityId": "admin:fr:31555"},

"journeys": [
  {"dateTime": "2014-06-29 16:36:00",

                  "realTime": "1",
                  "waiting_time": "00:03:05"},

  {"dateTime": "2014-06-29 16:46:00",

                  "realTime": "1",
                  "waiting_time": "00:13:20"}]

},…

]

  },…
]

4.7.5

Exemples d’utilisation

Liste des prochains passages pour ce code opérateur (3431) au format xml du réseau Tisséo
https://api.tisseo.fr/v2/stops_schedules.xml?operatorCode=3431

Liste des prochains passages pour cet arrêt physique ou poteau (3377699720883436) au format xml du
réseau Tisséo
https://api.tisseo.fr/v2/stops_schedules.xml?stopPointId=stop_point:SP_3327

Liste des prochains passages pour ce code opérateur (3431) au format json du réseau Tisséo
https://api.tisseo.fr/v2/stops_schedules.json?operatorCode=3431

Liste des prochains passages pour les arrêts logiques Météo France et Ateliers métro groupés par arrêt
logique et donnant les 2 prochains passages pour chaque couple (ligne, destination).
https://api.tisseo.fr/v2/stops_schedules.json?
&stopsList=stop_area:SA_903,stop_area:SA_444&timetableByArea=1&number=2

Open Data : API Tisséo

Page : 29/38

Documentation développeur

Version API : 2
Date : 21/05/2025

4.8  ROLLING_STOCKS : MODES DE TRANSPORTS

4.8.1

Principe

Ce service permet  d’afficher les modes de transports (rolling stocks) disponibles sur le réseau Tisséo.

4.8.2

Mode d’appel et Paramètres

URL : https://api.tisseo.fr/v2/rolling_stocks.<format>?...paramètres...

Nom

Description du paramètre

Requis ?  Valeur défaut

Ce service ne prend aucun paramètre

4.8.3

Réponse : Rolling_stock

https://api.tisseo.fr/v2/rolling_stocks.json

Rolling_stock, description

Nom du champ

Type

Description

name
id

string
string

Nom du mode de transport
Identifiant unique (voir section 3.9)

Toujours
affiché ?
oui
oui

Rolling_stock, JSON

{
   expirationDate: "2014-01-10 03:45",
   rollingStocks: [
      {
         article: "le",
         id: "commercial_mode:3",
         name: "bus"
      },
      {
         article: "le",
         id: "commercial_mode:1",
         name: "métro"
      },
      {
         article: "le",
         id: "commercial_mode:2",
         name: "tramway"
      },…
   ]
}

Open Data : API Tisséo

Page : 30/38

Documentation développeur

Version API : 2
Date : 21/05/2025

4.9  JOURNEYS : CALCUL D’ITINERAIRES

4.9.1

Principe

Ce service permet  de calculer l’itinéraire pour se rendre d’un point A à point B.
Les solutions renvoyées sont les solutions les plus rapides triées par ordre de prochain départ.

4.9.2

Mode d’appel et Paramètres

URL : https://api.tisseo.fr/v2/jouneys.<format>?...paramètres...

Nom

Description du paramètre

departurePlace
departurePlaceXY
arrivalPlace
arrivalPlaceXY
srid
networkList
firstDepartureDatetime  Désigne la première date/heure de départ (YYYY-MM-

Désigne l’adresse ou le lieu de départ
Désigne les coordonnées de départ
Désigne l’adresse ou le lieu d’arrivée
Désigne les coordonnées d’arrivée
Système de coordonnées (Voir section 3.4)
Opérateurs de transport à prendre en compte

DD HH:MM)

lastDepartureDatetime  Désigne la dernière date/heure de départ  (YYYY-MM-

maxTransferNumber

roadMode

DD HH:MM)
Désigne  le  nombre  maximal  de  correspondances  à
utiliser
Désigne  le  mode  avec  lequel  sont  effectuées  les
portions de trajet non « Transport en commun » au
début  (sauf  si  un  « startRoadMode »  différent  est
précisé) ou à la fin du trajet

Valeur défaut

4326
Tisséo

Requis
 ?
non
non
non
non
non
non
non

non

non

5

non

walk (marche à pied)

roadSpeed

Désigne la vitesse (m/s) du roadMode sélectionné

non

roadMaxDistance

startRoadMode

rollingStockList

number
displayResultTable

displayWording

displayMessages

au

(sauf

début

Désigne  la  distance  maximum  qu’on  accepte  de
parcourir
un
startRoadMaxDistance  différent  est  précisé)  et  à  la
fin du trajet
Désigne  le  mode  avec  lequel  sera  effectuée  la
portion de trajet non « Transport en commun » au
début du trajet

si

Modes  de  transport  à  prendre  en  compte  dans  le
calcul (Bus, Métro, Tram, …)
Filtre sur le nb maxi de résultats à retourner
Retourne  en  plus,  un  résumé  du  parcours  sous
forme de tableau.
Retourne  en  plus,  les  commentaires  pour  chaque
tronçon du parcours (0/1)
Retourne  en  plus,
les
perturbation de service

id  de  messages  de

1.111 m/s pour walk
0.556 m/s pour wheelchair
4.167 m/s pour bike
2000 m

non

non

walk

non

non
non

3

non

0 : Pas de commentaires

non

maxApproachDistance   Distance maximale de marche à pied

non

1000m

Open Data : API Tisséo

Page : 31/38

Documentation développeur

Version API : 2
Date : 21/05/2025

4.9.3

Règles de gestion

Valeurs possibles

networkList : Tisséo (il sera possible d’en préciser plusieurs ultérieurement)

number : valeur maximale autorisée est 8

firstDepartureDatetime : 2014-10-21 17:24
Si vous ne précisez pas ce paramètre, c’est l’heure courante qui sera utilisée comme heure de départ.

ATTENTION :  le  paramètre  lastDepartureDatetime  ne  peut  pas  être  utilisé  seul,  mais  peut  être
ajouté optionnellement avec firstDepartureDatetime pour définir une tranche horaire de départ.

departurePlaceXY : 1.43697,43.5849  (valeur en 4326 = WGS84 = système GPS)

walkspeed : 8.355 (3km/h), (n’importe quelle valeur numérique –réaliste-)

rollingStockList est composé des modes de transport séparés par des virgules.
Exemple :
commercial_mode:1,commercial_mode:3,commercial_mode:2 = métro + bus + tram
commercial_mode:1,commercial_mode:2 = metro + tram
(Voir le service rolling_stocks chapitre 4.8 pour la liste des modes disponibles)
Si ce paramètre n’est pas passé, tous les modes de transport seront pris en compte

roadMode et/ou startRoadMode : walk / wheelchair / bike / car
ATTENTION : si roadMode = wheelchair, alors le trajet en transport en commun n’empruntera que des
arrêts, et des lignes accessibles. De même, le calculateur ne fera pas emprunter les ascenceurs en panne
dans les stations de métro.

roadSpeed : 0.8333 ( = 3 km/h)
ATTENTION :  ce  paramètre  ne  fonctionne  pas  pour  la  voiture :  le  calculateur  respecte  les  limites  de
vitesse !

roadMaxDistance et/ou startRoadMaxDistance : 3000
Exemple :
roadMode=walk&startRoadMode=car&roadSpeed=8.333&roadMaxDistance=2000&startRoadMaxDistance
=20000
Correspond à un trajet qui commence par maximum 20km de voiture puis  du transport en commun puis
maximum 2km à pied à 3km/h.

Remarque : Le choix d’un roadMode, ne change pas seulement la vitesse, il change les voies autorisées
(rocades, sens interdit, rue piétonne, piste cyclables, …) et respect du code de la route (interdiction de
tourner à gauche, …)

Open Data : API Tisséo

Page : 32/38

Documentation développeur

Version API : 2
Date : 21/05/2025

4.9.4

Réponse

4.9.4.1 Principe

Tisséo  utilise  le  même  calculateur  d’itinéraire  que  celui  de  l’API  OpenData,  vous  pouvez  donc  vous
familiariser avec les résultat possibles en faisant des essais sur https://www.tisseo.fr/plan-interactif/, ou
https://www.tisseo.fr/ ou sur notre application mobile.

Remarque : le calculateur peut renvoyer des tracés droits pour les lignes TAD zonales. En effet, ces bus
ne suivent pas un itinéraire prédéfini, mais se déplacent en fonction des réservations effectuées.
Nous masquons ces tracés qui induirait l'utilisateur en erreur et les remplaçons par un trait droit :

La section en noir du tracé ci-dessus est faite en TAD zonal

Plus d’information sur la TAD : https://www.tisseo.fr/se-deplacer/bien-voyager/en-tad

4.9.4.2 Format de réponse

Une réponse de calcul d’itinéraire, contient :

  Une  section  « query » :  qui  rappelle  vos  paramètres  d’appel  ainsi  que  les  origines  destinations
trouvées (en effet vous pouvez avoir passé un XY ou une chaine incomplete : voir section 3.11)
  Une  section  « journeys » :  qui  contient  les  prochaines  solutions  par  ordre  chronologique  de

départ

Chaque « journey » a comme attribut :

  Une durée
  Une datetime de départ et d’arrivée
  Une quantité de CO2 en grammes
  Des sections de trajets : les « chunks »
  Un texte d’arrivée

Chaque chunck peut être de type :

  street : le parcours d’une portion de rue ou une correspondance nécéssitant de la marche
  stop : un arrêt de montée / descente
  service : une portion de ligne de transport en commun empruntée

Chacun de ces objets a une géométrie afin d’être représentable sur une carte.

Aide à la feuille de route :
Chaque  élément contient un bloc de texte qui peut vous permettre de générer le texte d’une  feuille de
route.

Open Data : API Tisséo

Page : 33/38

Documentation développeur

Version API : 2
Date : 21/05/2025

Exemple en JSON :

        "journeys": [
            {
                "journey": {
                    "duration": "00:07:00",
                    "departureDateTime": "2014-12-10 18:11:25",

                                    "arrivalDateTime": "2014-12-10 18:52:16",
                                    "co2_emissions": "718.85",

                    "chunks": [
                        {
                            "street": {
                                "length": "104",
                                "wkt":  "MULTILINESTRING  ((1.4478480047797782  43.6050350000280176,  1.4486480047795545
43.6055550000280547, 1.4488080047795100 43.6056650000280897))",
                                "roadMode": "walk",
                                "startAddress": {
                                    "connectionPlace": {
                                        "latitude": "43.605035000028018",
                                        "longitude": "1.4478480047797782"
                                    }
                                },
                                "endAddress": {
                                    "address": {
                                        "latitude": "43.60566500002809",
                                        "longitude": "1.44880800477951",
                                        "streetName": "ALLÉES DU PRÉSIDENT FRANKLIN ROOSEVELT"
                                    }
                                },
                                "text": {
                                    "lang": "fr",
                                    "text": "Marchez 104 mètres sur 'ALLÉES DU PRÉSIDENT FRANKLIN ROOSEVELT'."
                                }
                            }
                        },
                        {
                            "stop": {
                                "firstTime": "15:11",
                                "lastTime": "",
                                "latitude": "43.605279000028013",
                                "longitude": "1.4490520047793991",
                                "name": "Jean Jaurès",
                                "connectionPlace": {
                                    "latitude": "43.605623005177243",
                                    "longitude": "1.4487989848427141",
                                    "id": "stop_area:SA_1707",
                                    "city": "TOULOUSE",
                                    "x": "1.448799",
                                    "y": "43.605623",
                                    "name": "Jean Jaurès"
                                },
                                "text": {
                                    "lang": "fr",
                                    "text": "Rejoignez l'arrêt Jean Jaurès."
                                }
                            }
                        },
                        {
                            "service": {
                                "firstDepartureTime": "15:11",
                                "firstArrivalTime": "15:14",
                                "lastDepartureTime": "",
                                "lastArrivalTime": "",
                                "isContinuousService": "0",
                                "maxWaitingTime": "",
                                "wkt":
43.6052250000279926, 1.4495490047792070)",
                                "destinationStop": {
                                    "id": "11821949021891631",
                                    "name": "Gonin TOULOUSE",
                                    "line": {
                                        "id": "11821949021891631",
                                        "color": "(142,74,5)",
                                        "name": "Marengo - SNCF / Gonin",

43.6053250000280386,

(1.4491400047793750

1.4492390047793338

"LINESTRING

Open Data : API Tisséo

Page : 34/38

Documentation développeur

Version API : 2
Date : 21/05/2025

                                        "shortName": "22",
                                        "style": "beige",
                                        "network": "Tisséo",
                                        "transportMode": {
                                            "id": "commercial_mode :3",
                                            "article": "le",
                                            "name": "bus"
                                        }
                                    }
                                },
                                "text": {
                                    "lang": "fr",
                                    "text": "Prenez le bus, ligne 22, à destination de Gonin TOULOUSE. "
                                }
                            }
                        …

4.9.5

Exemples d’utilisation

Calcul d’itinéraires pour se rendre de la place Basso Cambo à François Verdier au format xml, avec le
nombre de résultats limité à deux, et des commentaires pour chaque trajet.
https://api.tisseo.fr/v2/journeys.xml?departurePlace=basso cambo &arrivalPlace=françois verdier
toulouse&number=2&displayWording=1&lang=fr

Calcul d’itinéraires pour se rendre de la place Basso Cambo à François Verdier au format json, avec le
nombre de résultats limité à deux, et des commentaires pour chaque trajet.
https://api.tisseo.fr/v2/journeys.json?departurePlace=basso cambo&arrivalPlace=françois verdier
toulouse&number=2&displayWording=1&lang=fr

Calcul d’itinéraires pour se rendre de la place Basso Cambo à François Verdier à partir de 15h00 au
format json, avec le nombre de résultats limité à deux, et des commentaires pour chaque trajet.
https://api.tisseo.fr/v2/journeys.json?departurePlace=basso cambo &arrivalPlace=françois verdier
toulouse&firstDepartureDatetime=2014-06-29 15:00&number=2&displayWording=1&lang=fr

Open Data : API Tisséo

Page : 35/38

Documentation développeur

Version API : 2
Date : 21/05/2025

4.10 MESSAGES : MESSAGES D’INFORMATION

4.10.1

Principe

Ce service permet d’obtenir les messages d’information trafic des réseaux de transport (pour le moment
Tisséo uniquement).
Ces informations sont accessibles depuis la page d’accueil de tisseo.fr.

Les  messages  d’information  sont  de  type  « trafic » (déviations  de  lignes,  modifications  d'horaires)  :
https://www.tisseo.fr/infos/reseau

Tous  les  messages  sont rédigés en  langue  française. Tisséo  ne fournira  pas  les  traductions
de ces messages.

4.10.2  Mode d’appel et Paramètres

URL : https://api.tisseo.fr/v2/messages.<format>?...paramètres...

Nom
network
contentFormat
displayImportantOnly

Description du paramètre
Opérateur de transport
Format du contenu des messages
N’affiche que les messages importants
(présents sur la home page de tisseo.fr)

Requis ?  Valeur défaut
Non
Non
Non

Tisséo
text
0

4.10.3

Règles de gestion

Valeurs possibles : contentFormat : text, html

ATTENTION :  certaines  infos  réseaux  de  scope  « line »  n’auront  pas  de  ligne  associée  car  non
disponible dans l’API : c’est le cas des navettes scolaires et navettes Wallon et Stadium.

4.10.4

Réponse : Message

Message, Description

Nom du champ

Type

Description

string

scope

title
content

string
string
string

id
type
importanceLevel

Identifiant
Type de message
Niveau d’importance : normal ou important*
Portée du message : line, event ou global**
Titre du message
Oui
Contenu*** du message en html ou text suivant les paramètres   Oui
url
Oui
Page officielle du message
lines
Lignes impactées par le message
Non
*un message « important » sera affiché en page d’accueil de www.tisseo.fr (ex : panne métro, neige, grève)
**voir des exemples sur tisseo.fr ou dans l’application Tisséo : il y a une logique de couleur que vous pourriez suivre

string
string

string
List

Oui

Toujours
affiché ?
Oui
Oui
Oui

Open Data : API Tisséo

Page : 36/38

Documentation développeur

Version API : 2
Date : 21/05/2025

***Le contenu de la balise content sera toujours encadré par des <![CDATA[ et ]]>  en  XML et sur une seule
ligne avec des \n\t explicites en JSON

Message, JSON

{
    "message": {
        "type": "trafic",
        "id": "522",
        "importanceLevel": "normal",
        "scope": "line",
        "title": "Ligne 21 - Déviation à Colomiers",
        "content": "Déviation à Colomiers

En raison de travaux situés avenue Yves Brunaud à Colomiers, du 16
juin 2014 au 31 décembre 2015, la ligne 21 est déviée.
Arrêts non desservis : Lautaret, Clément Ader.
Vous pouvez vous reporter à l'arrêt provisoire à l'angle de
l'avenue Marcel Dassault et de l'allée de l'Aubrac, à l'arrêt
Pelvoux (Conseil Général), ainsi qu'aux arrêts de la ligne 64 L.P.
Colomiers et Fontaine.",

        "url": "http://www.tisseo.fr/node/522"
    },
    "lines": […]
}

Open Data : API Tisséo

Page : 37/38

Documentation développeur

Version API : 2
Date : 21/05/2025

Open Data : API Tisséo

Page : 38/38

