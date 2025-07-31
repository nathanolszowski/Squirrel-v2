# Squirrel Scraper V.2

This project is a collection of scrapers to extract real estate ad data from different Agency sites.
It allows you to have a complete market view for offices in Île-de-France, business premises and warehouses in France.
List of available agency sites:
- CBRE
- BNP
- JLL /!/ Disabled /!/
- AlexBolton
- Cushman & Wakefield
- Knight Frank
- ArthurLoyd
- Savills

## Project status

1. Priority 1 :
- Improve the recovery of longitude/latitude and addresses for all agencies
- Homogenize collected datas
- Manage duplicate :
   - compare lat/long, adresse, accroche, titre et surface totale

2. Priority 2 :
- Cache system to avoid re-scraping the same pages too often?
- Identification of too large number of None values

3. Priority 3 :
- Work on code factorization and scraping speed
- Addition of market sectors
- Compare the new export with the old one
- Progress bar
- Setting up retry mechanisms for failed requests
- Asynchronous scraping
- Tests


## Project structure

```
Squirrel/
├── config/
│   ├── scrapers_config.py      # Configuration for scrapers
│   └── scrapers_selectors.py     # CSS selectors by scraper
│   └── squirrel_settings.py     # Global configuration
├── core/
│   ├── api_scraper.py           # Class for api scraper
│   ├── base_scraper.py          # Base class for all scrapers
│   ├── http_scraper.py          # Class for http scraper
│   ├── scraper_factory.py        # Factory for create a new scraper
│   └── url_discovery_strategy.py  # Stratégie de découverte d'url
├── scrapers/
│   ├── bnp.py
│   ├── jll.py
│   └── ...
├── data/
├── exports/
├── logs/
├── network/
│   └── http_client_handler     # Http client handler for web scraping requests
│   └── user_agent.py         # User-agents generator
├── tests/
│   └── network/
│       └── test_user_agents
├── utils/
│   └── logging_config        # Initialisation du logger (create a log file in logs/ folder)
└── main.py             # Entry point
```

## Installation

1. Create a virtual environnement :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies :
```bash
pip install -r requirements.txt
```

3. Add your proxy adress :
`main.py`
```
    PROXY = "YOUR PROXY ADRESS"
```

## Usage

Starting program with :
```bash
python main.py
```

JSON Format :
```
{
   "confrere": "BNP",
   "url": "https://bnppre.fr/a-vendre/local-activite/seine-et-marne-77/croissy-beaubourg-77183/vente-local-activite-1110-m2-non-divisible-OVACT2423977.html",
   "reference": "Référence : OVACT2423977",
   "contrat": "Vente",
   "actif": "Locaux d'activité",
   "disponibilite": "Immédiate",
   "surface": "1 111 m²",
   "division": "N/A",
   "adresse": "N/A 77183 Croissy-Beaubourg",
   "contact": "Baptiste Quilgars",
   "accroche": "BNP PARIBAS REAL ESTATE vous propose, à la Vente, une cellule d'activité avec bureaux d'accompagnement, en bon état, disponible à Croissy-Beaubourg.",
   "amenagements": "L'essentiel à retenirDisponibilité :ImmédiateCharge au sol Rdc :2,00 tonne(s)/m²Porte d'accès plain-pied :3HauteursHauteur sous poutre :5,00 mètre(s)Accès véhiculesAccessibilité type véhicules :Tous porteursEquipementsCharge au sol Rdc :2,00 tonne(s)/m²Climatisation :Réversible dans la partie BureauxEclairage Bureaux :Luminaires encastrésEclairage naturel :SkydomesFaux plafond :OuiFenêtres :OuiPorte d'accès plain-pied :3Sol bureaux :ParquetSols du bâtiment :BétonSource chauffage :Electrique 2 AérothermesType / Etat du bâtimentEtat de l'immeuble :Etat d'usagePrestations de serviceParking :35 PlacesSécurité :Contrôle d'accès - PortailAménagementsAménagement des bureaux :CloisonnésLocaux sociaux :SanitairesSanitaires :Oui",
   "url_image": "https://www.bnppre.fr/sites/default/files/styles/max_2600x2600/public/offers/34/34fcc0a002c3245f1c2cd2c393d1e2b89a1e5582.jpg.webp?itok=tGm22I-P",
   "latitude": 44.8019097,
   "longitude": -0.6488505,
   "prix_global": "1 700 000 €"
}
```

## Fonctionnalities

- Extraction of listings for offices in the Paris region and logistics in France
- Support for several listings sites (BNP, JLL, etc.)
- Data export in JSON
- Asynchronous scraping
- Detailed logging
- User-agent management
- Use of proxy

## Add a new scraper

1. Créer un nouveau fichier dans le dossier `scrapers/`
2. Hériter de `BaseScraper`
3. Implémenter la méthode `post_traitement_hook()` si besoin spécifique du scraper
4. Ajouter les sélecteurs dans `config/scrapers_selectors.py`
5. Ajouter le sitemap dans `config/scrapers_config.py`
6. Instancier le scraper dans `main.py`

## Maintain

- CSS selectors are centralised in `config/scrapers_selectors.py`
- Global configuration in `config/squirrel_settings.py`
- Tests are centralised in `tests/`
- Logs allow you to monitor execution and diagnose errors

## Error handling

- [Errno 11001] getaddrinfo failed
└──> Traduit l'argument host/port en une séquence de 5 tuples contenant tous les arguments nécessaires à la création d'une socket connectée à ce service. host est un nom de domaine, une représentation sous forme de chaîne d'une adresse IPv4/v6 ou None.
- [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1000)
└──> TLS support version ?
- peer closed connection without sending complete message body (incomplete chunked read)
└──> Limite imposé par le serveur interrogé.
   └──> Rien n'a faire du côté client. Possiblement espacer les requêtes.
- Server disconnected without sending a response
└──> erreur dû aux timeouts ou à la "keep-alive connection" (soit côté client, soit côté serveur)
   └──> Voir paramétrage httpx.Limits.

