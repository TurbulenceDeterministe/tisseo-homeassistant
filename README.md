# Tisséo Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Intégration Home Assistant pour l'API Open Data **Tisséo** (Toulouse).

## Fonctionnalités

- **Prochains passages** : Capteurs pour chaque arrêt configuré avec les horaires temps réel/théoriques
- **Perturbations** : Capteurs binaires par ligne pour suivre les disruptions
- **Messages réseau** : Capteur global avec les alertes et infos trafic
- **Itinéraire** : Capteur de durée de trajet entre deux points + service `tisseo.calculate_journey`

## Installation

### Via HACS

1. Ajoutez ce dépôt comme dépôt personnalisé dans HACS
2. Installez l'intégration **Tisséo**
3. Redémarrez Home Assistant

### Manuelle

1. Copiez le dossier `custom_components/tisseo/` dans votre dossier `custom_components/`
2. Redémarrez Home Assistant

## Configuration

1. Allez dans **Paramètres > Appareils et services > Ajouter une intégration**
2. Recherchez **Tisséo**
3. Entrez votre **clé API** (obtenue sur `opendata@tisseo.fr`)
4. Recherchez et sélectionnez les **arrêts** à surveiller
5. Sélectionnez les **lignes** à surveiller pour les perturbations
6. (Optionnel) Configurez un **itinéraire** de référence

## Dépannage : aucun arrêt trouvé

La recherche utilise l'API **v2** `places.json` avec au moins trois caractères et
`displayOnlyStopAreas=1`. Tester uniquement `/v1/stop_areas.json` ne vérifie pas
cette recherche. Essayez un nom comme `Esquirol` ou `Basso Cambo`.

Pour consulter les journaux, ouvrez **Paramètres > Système > Journaux**, choisissez
**Home Assistant Core**, puis affichez ou téléchargez les journaux bruts après avoir
reproduit le problème. Si l'intégration n'est pas encore configurée, ajoutez ceci
dans `configuration.yaml` (en complétant la section `logger` si elle existe), puis
redémarrez Home Assistant :

```yaml
logger:
  logs:
    custom_components.tisseo: debug
```

Les logs indiquent le statut HTTP et le nombre de résultats reçus et utilisables.
Pour signaler un problème, joignez le texte recherché, l'heure du test, la version
de l'intégration et les logs correspondants. Masquez votre clé API dans tout
extrait ou URL partagé. Désactivez ensuite le débogage.

## Tests de développement

```sh
python -m pip install aiohttp voluptuous
python -m unittest discover -s tests -v
```

Les tests utilisent des réponses API simulées et des doubles du framework Home
Assistant pour les transitions de configuration. Ils ne remplacent pas un essai
avec une clé Tisséo valide dans une installation Home Assistant.

## Services

### `tisseo.calculate_journey`

Calcule un itinéraire à la demande.

| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `departure` | string | Oui | Lieu de départ |
| `arrival` | string | Oui | Lieu d'arrivée |
| `datetime` | string | Non | Date/heure de départ (YYYY-MM-DD HH:MM) |

Le résultat est émis via l'événement `tisseo_journey_result`.

## Licence

MIT

## Crédits

Données fournies par [Tisséo](https://www.tisseo.fr/) sous licence ODbL.
