# -*- coding: utf-8 -*-
"""
Fonctions pour gérer les user_agents
"""

import random
import httpx
from bs4 import BeautifulSoup
import json
import os
from functools import cached_property
from typing import List, Optional, Union, Dict
from time import time
from ua_parser import user_agent_parser
import logging
from config.squirrel_settings import (
    USER_AGENT_UPDATE,
    FICHIER_CACHE_USER_AGENT,
    REQUEST_TIMEOUT,
)

logger = logging.getLogger(__name__)


class UserAgent:
    """Dataclass for user-agents"""

    def __init__(self, user_agent: str) -> None:
        """
        Setting up a new user-agent

        Args:
            user-agent (str): Character string representing a user-agent like : "Mozilla/5.0 (Windows NT 10.0; Win64; x64)
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        """
        self.string: str = user_agent
        # User-agent string parser
        self.parsed_string: dict = user_agent_parser.Parse(user_agent)
        self.last_used: float = time()

    # Getting browser name
    @cached_property
    def browser(self) -> str:
        return self.parsed_string["user_agent"]["family"]

    # Getting browser version
    @cached_property
    def browser_version(self) -> int:
        return int(self.parsed_string["user_agent"]["major"])

    # Getting OS
    @cached_property
    def os(self) -> str:
        return self.parsed_string["os"]["family"]

    # Return full user_agent string after parsing
    def __str__(self) -> str:
        return self.string


class ListUserAgent:
    """Set and manage user-agents list"""

    def __init__(
        self,
        http_client,
        user_agent_cache=FICHIER_CACHE_USER_AGENT,
        enabling_update=USER_AGENT_UPDATE,
    ):
        self.user_agent_cache: str = user_agent_cache
        self.enabling_update: bool = enabling_update
        self.http_client: str = http_client
        self.actual_url_user_agents: str = self.get_update_url_user_agents()
        self.liste_user_agents: list[UserAgent] = [
            UserAgent(ua) for ua in self.get_update_user_agents_list()
        ]

    def get_user_agents_list(self) -> list[UserAgent]:
        """Return the complete ListUserAgents"""
        return self.liste_user_agents if self.liste_user_agents else []

    def get_update_url_user_agents(self) -> str:
        """
        Fetches from the useragents.io sitemap the updated url with a list of user-agents available for scraping

        Returns:
            last_update_url (str): Chaîne de caractère représentant l'url de la dernière liste d'user-agents à jour
        """
        logger.info("Retrieving the url to the latest updated list of user-agents")
        url_usergantsio: str = "https://useragents.io/sitemaps/useragents.xml"
        response = self.http_client.get(url_usergantsio)
        soup = BeautifulSoup(response.text, "xml")
        actual_url_user_agents = soup.find_all("sitemap")[-1]
        actual_url_user_agents = actual_url_user_agents.find("loc").text
        logger.info("Url to the latest updated list of user-agents has been retrieved")
        return actual_url_user_agents

    def obtenir_liste_user_agents_actualise(self) -> list[str]:
        """
        Récupère les user_agents string depuis la dernière liste à jour

        Returns:
            user_agents (list[str]): Chaîne de caractère représentant l'url de la dernière sitemap d'user-agents à jour
        """
        logger.info("Récupération de la liste d'user-agents")
        try:
            with httpx.Client(
                proxy=self.proxy,
                headers={
                    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                },
                timeout=REQUEST_TIMEOUT,
                follow_redirects=True,
            ) as client:
                liste_agents = client.get(self.url_actuelle_user_agents)
            sitemap_actuelle = BeautifulSoup(liste_agents.text, "xml")
            user_agents_liens = [
                url.find("loc").text for url in sitemap_actuelle.find_all("url")
            ]
        except httpx.HTTPError as e:
            logger.error(
                f"[{self.url_actuelle_user_agents}] Erreur lors de la récupération la dernière liste à jour d'user-agents : {e}"
            )
        except AttributeError as e:
            logger.error(
                f"[{self.url_actuelle_user_agents}] Erreur lors de la récupération de la valeur de la dernière liste à jour d'user-agents : {e}"
            )
        user_agents_string = []
        for url in user_agents_liens:
            try:
                with httpx.Client(
                    proxy=self.proxy,
                    headers={
                        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                    },
                    timeout=REQUEST_TIMEOUT,
                    follow_redirects=True,
                ) as client:
                    response = client.get(url)
                soup = BeautifulSoup(response.content, "html.parser")
                ua_chaine = soup.select_one(
                    "body > div:nth-child(1) > main > h1"
                ).get_text()
                if any(
                    ua_chaine.startswith(browser) for browser in ["Mozilla", "Opera"]
                ):
                    user_agents_string.append(ua_chaine)
            except httpx.HTTPError as e:
                logger.error(
                    f"[{self.url_actuelle_user_agents}] Erreur lors de la récupération la dernière liste à jour d'user-agents : {e}"
                )
            except AttributeError as e:
                logger.error(
                    f"Erreur lors de la récupération de la valeur de la dernière liste à jour d'user-agents : {e}"
                )

        logger.info(
            f"Trouvé {len(user_agents_string)} user-agents à jour disponibles pour le scraping"
        )
        return user_agents_string

    def lire_cache_user_agents(self) -> Union[Dict[str, list[str]], None]:
        """Vérifie la présence du fichier de cache d'user-agents"""
        logger.info("Vérifie la présence du fichier de cache d'user-agents")
        try:
            if os.path.exists("user_agent.json"):
                logger.info("Le fichier de cache avec la liste d'user-agents existe")
                with open(self.fichier_cache, "r", encoding="utf-8") as f:
                    cache_user_agents = json.load(f)
                return cache_user_agents
            else:
                return None
        except IOError as e:
            logger.error(
                f"[{self.fichier_cache}] Erreur lors de l'ouverture du ficher cache JSON : {e}"
            )
        except json.JSONDecodeError as e:
            logger.error(
                f"[{self.fichier_cache}] Erreur lors de la lecture du ficher cache JSON : {e}"
            )

    def obtenir_url_cache_user_agents(self) -> Optional[str]:
        """
        Récupére l'url de la dernière liste d'user-agents depuis notre cache

        Returns:
            Optional[str]: Représente l'url de la dernière liste d'user-agents depuis le cache
        """
        cache = self.lire_cache_user_agents()
        if cache:
            return next(iter(cache.keys()), None)
        return None

    def compare_url_actualise_url_cache(self) -> bool:
        """
        Compare l'url actualisée depuis le site useragents.io avec l'url présent dans notre cache JSON
        """
        cache_url = self.obtenir_url_cache_user_agents()
        return self.url_actuelle_user_agents == cache_url

    def sauvegarder_cache_user_agents(self, user_agents: list[str]) -> None:
        """Sauvegarde la liste d'user-agents dans le cache JSON"""
        logger.info(
            "Début de la sauvegarde de la liste d'user-agents dans le cache JSON"
        )
        try:
            liste_user_agents = user_agents
            contenu_actualise = {self.url_actuelle_user_agents: liste_user_agents}
            with open(self.fichier_cache, "w", encoding="utf-8") as f:
                json.dump(contenu_actualise, f, ensure_ascii=False, indent=4)
        except IOError as e:
            logger.error(
                f"[{self.fichier_cache}] Erreur lors de l'ouverture du ficher cache JSON : {e}"
            )
        except json.JSONDecodeError as e:
            logger.error(
                f"[{self.fichier_cache}] Erreur lors de la lecture du ficher cache JSON : {e}"
            )

    def get_update_user_agents_list(self) -> list[str]:
        """Renvoi la liste d'user-agents à mettre à jour ou non"""
        logger.info(
            "Début de la récupération de la liste d'user-agents à jour, depuis le cache si possible."
        )
        if self.compare_url_actualise_url_cache() or not self.activer_maj:
            logger.info(
                "URL inchangée ou la mise à jour n'a pas été activée. Chargement depuis le cache."
            )
            cache = self.lire_cache_user_agents()
            return list(cache.values())[0] if cache else []
        else:
            logger.info("URL a changée. Mise à jour nécessaire.")
            user_agents = self.obtenir_liste_user_agents_actualise()
            self.sauvegarder_cache_user_agents(user_agents)
            return user_agents

    def notation_user_agent(self, user_agent: UserAgent) -> int:
        """
        Notation d'un user-agent selon ses caractéristiques

        Args:
            user_agent (UserAgent): Objet représentant un user-agent
        Returns:
            (int): Notation de l'user-agent en cours d'analyse
        """
        notation: int = 1000

        # Augmente la note pour les user-agents les moins utilisés
        if user_agent.last_used:
            _seconds_since_last_use = int(time() - user_agent.last_used)
            notation += _seconds_since_last_use

        # Augmente la note par rapport au navigateur utilisé
        if user_agent.browser == "Chrome":
            notation += 100
        if user_agent.browser == "Firefox" or "Edge":
            notation += 50
        if user_agent.browser == "Chrome Mobile" or "Firefox Mobile":
            notation += 0

        # Augmente la note pour les navigateurs avec une version récente
        if user_agent.browser_version:
            notation += user_agent.browser_version * 10

        # Augmente la note pour les navigateurs qui utilisent une version 50 ou supérieure de Chrome
        if user_agent.browser == "Chrome" and user_agent.browser_version > 50:
            notation += 200

        # Augmente la note pour based on the OS type
        if user_agent.os == "Windows":
            notation += 150
        if user_agent.os == "Mac OS X":
            notation += 100
        if user_agent.os in ["Linux", "Ubuntu"]:
            notation -= 50
        if user_agent.os == "Android":
            notation -= 100
        return notation

    def get_user_agent(self) -> str:
        """
        Retourne un user-agent qui aura été choisi selon sa notation et sa dernière date d'utilisation

        Returns:
            (str): Retourne un user-agent qui aura été choisi selon sa notation et sa dernière date d'utilisation
        """
        # Note tous les user-agents
        user_agent_notes = []
        for user_agent in self.user_agents:
            user_agent_notes.append(self.notation_user_agent(user_agent))
        # Sélectionne un user-agent
        user_agent = random.choices(
            self.user_agents,
            weights=user_agent_notes,
            k=1,
        )[0]
        # Met à jour l'attribut de dernière utilisation
        user_agent.last_used = time()
        return str(user_agent)
