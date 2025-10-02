# Squirrel Scraper V.2

This project is a collection of scrapers to extract real estate ad data from different french Agency sites.
It allows you to have a complete market view for offices in Île-de-France, business premises and warehouses in France.
List of available agency sites:

- CBRE
- BNP
- JLL /!/ In progress /!/
- AlexBolton
- Cushman & Wakefield
- Knight Frank
- ArthurLoyd
- Savills

## Project status

1. Priority 1 :

- [ ] Improve the quality of data recovery in particular longitude/latitude and addresses for all agencies (asset_type for arthur loyd, resume for alexbolton)
- [ ] Homogenize data collection
- [ ] Working on filters rationalisation (in particular JLL)
- [x] Working on asynchronous programing

2. Priority 2 :
- [ ] Deduplicate the request logic
- [ ] Improve scraper heritage
- [ ] Improve descovery strategy
- [ ] Adding a scraping limitation for APIScraper
- [ ] Cache system to avoid re-scraping the same pages too often?
- [ ] Identification of too large number of None values (css selector validation)
- [ ] Manage duplicates :
   - compare lat/long, adresse, accroche, titre et surface totale

3. Priority 3 :
- [ ] Addition of market sectors
- [ ] Progress bar
- [ ] Compare the new export with the old one
- [ ] Natural language processing for resume and amenities (with IA if possible)
- [ ] Visualisation and exploration



## Project structure

```
Squirrel-v2/
├── config/
│   ├── scrapers_config.py      # Configuration for scrapers
│   ├── scrapers_selectors.py     # CSS selectors by scraper
│   └── squirrel_settings.py     # Global configuration
├── core/
│   ├── api_scraper.py           # Class for api scrapers
│   ├── base_scraper.py          # Base class for all scrapers
│   ├── http_scraper.py          # Class for http scrapers
├── scrapers/                 # Scraper for each sites
│   ├── bnp.py
│   ├── jll.py
│   └── ...
├── datas/
│   ├── listing_exporter.py      # Class for listing exporter
│   ├── listing_manager.py       # Class for listings manager
│   ├── property_listing.py      # Class for properties manager
│   └── property.py              # Dataclass for http scrapers
├── exports/
├── logs/
├── network/
│   └── user_agent.py         # User-agents generator
├── tests/
│   ├── datas/
│   |    └── test_properties.py
│   └── network/
│       └── test_user_agents.py
├── utils/
│   └── logging.py        # Initialisation du logger (create a log file in logs/ folder)
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

/!/ By default all scrapers are enabled. In order to disabled one or several scrapers, go to the config/scrapers_config and set the "enabled" to False /!/

Starting program with :
```bash
python main.py
```

## Default return format

JSON Format :
```
{
   "confrere": "BNP",
   "url": "https://bnppre.fr/a-vendre/local-activite/seine-et-marne-77/croissy-beaubourg-77183/vente-local-activite-1110-m2-non-divisible-OVACT2423977.html",
   "reference": "Référence : OVACT2423977",
   "contract": "Vente",
   "asset_type": "Locaux d'activité",
   "disponibility": "Immédiate",
   "area": "1 111 m²",
   "division": "Non divisible",
   "adress": "N/A 77183 Croissy-Beaubourg",
   "postal_code": None
   "contact": "Baptiste Quilgars",
   "resume": "BNP PARIBAS REAL ESTATE vous propose, à la Vente, une cellule d'activité avec bureaux d'accompagnement, en bon état, disponible à Croissy-Beaubourg.",
   "amenities": "L'essentiel à retenirDisponibilité :ImmédiateCharge au sol Rdc :2,00 tonne(s)/m²Porte d'accès plain-pied :3HauteursHauteur sous poutre :5,00 mètre(s)Accès véhiculesAccessibilité type véhicules :Tous porteursEquipementsCharge au sol Rdc :2,00 tonne(s)/m²Climatisation :Réversible dans la partie BureauxEclairage Bureaux :Luminaires encastrésEclairage naturel :SkydomesFaux plafond :OuiFenêtres :OuiPorte d'accès plain-pied :3Sol bureaux :ParquetSols du bâtiment :BétonSource chauffage :Electrique 2 AérothermesType / Etat du bâtimentEtat de l'immeuble :Etat d'usagePrestations de serviceParking :35 PlacesSécurité :Contrôle d'accès - PortailAménagementsAménagement des bureaux :CloisonnésLocaux sociaux :SanitairesSanitaires :Oui",
   "url_image": "https://www.bnppre.fr/sites/default/files/styles/max_2600x2600/public/offers/34/34fcc0a002c3245f1c2cd2c393d1e2b89a1e5582.jpg.webp?itok=tGm22I-P",
   "latitude": 44.8019097,
   "longitude": -0.6488505,
   "global_price": "1 700 000 €"
}
```

## Fonctionnalities

- Extraction of listings for offices in the Paris region and logistics in France
- Support for several listings sites (BNP, JLL, etc.)
- Data export in JSON
- Asynchronous scraping
- Detailed logging
- User-agent management
- Proxy handling

## Add a new HTTP scraper

1. Create a new python file in `scrapers/`
2. Inherits from `BaseScraper`
3. Implement `post_traitement_hook()` and `instance_filter_url()` method if needed
4. Add all selectors in `config/scrapers_selectors.py`
5. Feel the config for the scraper at `config/scrapers_config.py`
6. Instance the scraper in `main.py`

## Maintain

- CSS selectors are centralised in `config/scrapers_selectors.py`
- Global configuration in `config/squirrel_settings.py`
- Scraper configuration in `config/scrapers_config.py`
- Tests are centralised and classified in `tests/`
- Logs allow you to monitor execution and diagnose errors

## Error handling

- [Errno 11001] getaddrinfo failed
└──> Translates the host/port argument into a sequence of 5 tuples containing all the arguments necessary to create a socket connected to this service. host is a domain name, a string representation of an IPv4/v6 address, or None.
- [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1000)
└──> TLS support version ?
- peer closed connection without sending complete message body (incomplete chunked read)
└──> Limited by the server
   └──> Nothing to do client side. Maybe delayed requests
- Server disconnected without sending a response
└──> timeouts errors or "keep-alive connection" (client or sever side)
   └──> See httpx.Limits parameters

