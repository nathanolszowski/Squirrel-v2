# -*- coding: utf-8 -*-
"""
Handles user-agents management.
This module provides a class 'ListUserAgent' that manages a list of user-agents.
"""

import random
from bs4 import BeautifulSoup
import json
import os
import httpx
import aiofiles
from functools import cached_property
from time import time
from ua_parser import user_agent_parser
import logging
from config.squirrel_settings import (
    USER_AGENT_UPDATE,
    FICHIER_CACHE_USER_AGENT,
)

logger = logging.getLogger(__name__)


class UserAgent:
    """Dataclass for user-agents"""

    def __init__(self, user_agent: str) -> None:
        """
        Setting up a new user-agent

        Args:
            user-agent (str): String representing a user-agent like: "Mozilla/5.0 (Windows NT 10.0; Win64; x64)
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        """
        self.string: str = user_agent
        # User-agent string parser
        self.parsed_string: dict = user_agent_parser.Parse(user_agent)
        self.last_used: float = time()

    # Get browser name
    @cached_property
    def browser(self) -> str:
        return self.parsed_string["user_agent"]["family"]

    # Get browser version
    @cached_property
    def browser_version(self) -> int:
        return int(self.parsed_string["user_agent"]["major"])

    # Get OS
    @cached_property
    def os(self) -> str:
        return self.parsed_string["os"]["family"]

    # Returns full user_agent string after parsing
    def __str__(self) -> str:
        return self.string


class ListUserAgent:
    """Set and manage user-agents list"""

    def __init__(
        self,
        user_agent_cache=FICHIER_CACHE_USER_AGENT,
        enabling_update=USER_AGENT_UPDATE,
    ):
        self.user_agent_cache: str = user_agent_cache
        self.enabling_update: bool = enabling_update

    async def set_user_agents_list(self) -> None:
        """Returns the complete ListUserAgents"""
        self.liste_user_agents: list[UserAgent] = [
            UserAgent(ua) for ua in await self.get_update_user_agents_list()
        ]

    async def get_updated_url_user_agents(self) -> str:
        """
        Fetches from the useragents.io sitemap the updated url with a list of user-agents available for scraping

        Returns:
            last_update_url (str): String representing the url of the latest up-to-date user-agents list
        """
        logger.info("Retrieving the url to the latest updated list of user-agents")
        url_usergantsio: str = "https://useragents.io/sitemaps/useragents.xml"
        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.get(url_usergantsio)
                soup = BeautifulSoup(response.text, "xml")
                actual_url_user_agents = soup.find_all("sitemap")[-1]
                actual_url_user_agents = actual_url_user_agents.find("loc").text
                logger.info(
                    "Url to the latest updated list of user-agents has been retrieved"
                )
            return actual_url_user_agents
        except httpx.HTTPError as e:
            logger.error(
                f"[{url_usergantsio}] Error when attempting to reach useragents.io site : {e}"
            )
            # If the site url is not available, use the cached url instead
            return await self.get_cache_url_user_agents()
        except IndexError as e:
            logger.error(
                f"[{url_usergantsio}] Unable to find the last updated url from useragents.io because the path 'sitemap' doesn't exist : {e}"
            )
            # If the site url is not available, use the cached url instead
            return await self.get_cache_url_user_agents()
        except AttributeError as e:
            logger.error(
                f"[{url_usergantsio}] Unable to find the last updated url from useragents.io because the 'loc' tag doesn't exist : {e}"
            )
            # If the site url is not available, use the cached url instead
            return await self.get_cache_url_user_agents()

    async def get_updated_user_agents_list(self) -> list[str]:
        """
        Retrieves user_agents strings from the latest up-to-date list

        Returns:
            user_agents (list[str]): String representing the url of the latest up-to-date user-agents sitemap
        """
        logger.info("Retrieves updated user_agents list")
        default_user_agents_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
        ]
        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.get(self.actual_url_user_agents)
                actual_url = BeautifulSoup(response.text, "xml")
                user_agents_liens = [
                    url.find("loc").text for url in actual_url.find_all("url")
                ]
        except httpx.HTTPError as e:
            logger.error(
                f"[{self.actual_url_user_agents}] Error retrieving last updated list of user-agents : {e}"
            )
            return default_user_agents_list
        except IndexError as e:
            logger.error(
                f"[{self.actual_url_user_agents}] Error retrieving value from last updated user-agents list because 'loc' tag doesn't exist : {e}"
            )
            return default_user_agents_list
        except AttributeError as e:
            logger.error(
                f"[{self.actual_url_user_agents}] Error retrieving value from last updated user-agents list because 'url' tag doesn't exist : {e}"
            )
            return default_user_agents_list
        else:
            user_agents_string = []
            for url in user_agents_liens:
                response = await client.get(url)
                soup = BeautifulSoup(response.content, "html.parser")
                ua_chaine = soup.select_one("body > div:nth-child(1) > main > h1")
                if ua_chaine:
                    ua_chaine = ua_chaine.get_text()
                    if any(
                        ua_chaine.startswith(browser)
                        for browser in ["Mozilla", "Opera"]
                    ):
                        user_agents_string.append(ua_chaine)
                else:
                    logger.warning(
                        f"CSS selector doesn't find any user-agents, it may be broke : {url}"
                    )
            logger.info(
                f"Found {len(user_agents_string)} updated user-agents available for scraping"
            )
            return user_agents_string

    async def read_cache_user_agents(self) -> dict[str, list[str]]:
        """Checks for the presence of the user-agents cache file"""
        logger.info("Checks for the presence of the user-agents cache file")
        safe_callback: dict[str, list[str]] = {
            "absolute_url_not_found": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            ]
        }
        try:
            if os.path.exists("user_agent.json"):
                logger.info("Cache file with user-agents exists")
                async with aiofiles.open(
                    self.user_agent_cache, "r", encoding="utf-8"
                ) as f:
                    cache_user_agents = await f.read()
                data = json.loads(cache_user_agents)
                if isinstance(data, dict) and all(
                    isinstance(v, list) and all(isinstance(i, str) for i in v)
                    for v in data.values()
                ):
                    return data
                else:
                    logger.error(
                        f"[{self.user_agent_cache}] It seems that the cache file is not in the excepted format."
                    )
                    return safe_callback
            else:
                logger.error(
                    f"[{self.user_agent_cache}] Error when openning JSON cache file"
                )
                return safe_callback
        except json.JSONDecodeError as e:
            logger.error(
                f"[{self.user_agent_cache}] Error when reading JSON cache file : {e}"
            )
            return safe_callback

    async def get_cache_url_user_agents(self) -> str:
        """
        Retrieves the url of the latest user-agents list from our cache

        Returns:
            Optional[str]: Represents the url of the latest user-agents list from the cache
        """
        cache = await self.read_cache_user_agents()
        if cache:
            return next(iter(cache.keys()), "absolute_url_not_found")
        else:
            return "absolute_url_not_found"

    async def compare_url_actualise_url_cache(self) -> bool:
        """
        Compares the updated url from useragents.io with the url present in our JSON cache
        """
        self.actual_url_user_agents = await self.get_updated_url_user_agents()
        cache_url = await self.get_cache_url_user_agents()
        return self.actual_url_user_agents == cache_url

    async def save_cache_user_agents(self, user_agents: list[str]) -> None:
        """Saves the list of user-agents in the JSON cache"""
        logger.info("Starting to save the user-agents list in the JSON cache")
        try:
            liste_user_agents = user_agents
            contenu_actualise = {self.actual_url_user_agents: liste_user_agents}
            async with aiofiles.open(self.user_agent_cache, "w", encoding="utf-8") as f:
                await f.write(
                    json.dumps(contenu_actualise, ensure_ascii=False, indent=4)
                )
        except IOError as e:
            logger.error(
                f"[{self.user_agent_cache}] Error with JSON cache file openning : {e}"
            )
        except json.JSONDecodeError as e:
            logger.error(
                f"[{self.user_agent_cache}] Error when reading JSON cache file : {e}"
            )

    async def get_update_user_agents_list(self) -> list[str]:
        """Returns the list of user-agents to update or not"""
        logger.info(
            "Start retrieving the updated list of user-agents, from the cache if possible."
        )
        if await self.compare_url_actualise_url_cache() or not self.enabling_update:
            logger.info("URL unchanged or update not activated. Loading from cache.")
            cache = await self.read_cache_user_agents()
            return list(cache.values())[0] if cache else []
        else:
            logger.info("URL has changed. Update required.")
            user_agents = await self.get_updated_user_agents_list()
            await self.save_cache_user_agents(user_agents)
            return user_agents

    def scored_user_agent(self, user_agent: UserAgent) -> int:
        """
        Rates a user-agent according to its characteristics

        Args:
            user_agent (UserAgent): Object representing a user-agent
        Returns:
            (int): Rating of the user-agent being analyzed
        """
        notation: int = 1000

        # Increases the score for the least-used user-agents
        if user_agent.last_used:
            _seconds_since_last_use = int(time() - user_agent.last_used)
            notation += _seconds_since_last_use

        # Increases the score by the browser used
        if user_agent.browser == "Chrome":
            notation += 100
        if user_agent.browser == "Firefox" or "Edge":
            notation += 50
        if user_agent.browser == "Chrome Mobile" or "Firefox Mobile":
            notation += 0

        # Increases the score by most recent browser version
        if user_agent.browser_version:
            notation += user_agent.browser_version * 10

        # Increases the score for browsers that use version 50 or higher of Chrome
        if user_agent.browser == "Chrome" and user_agent.browser_version > 50:
            notation += 200

        # Increases the score based on the OS type
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
        Public method to return a user-agent chosen according to its rating and its last usage date

        Returns:
            (str): Returns a user-agent chosen according to its rating and its last usage date
        """
        # Calculates the rating of each user-agent
        logger.info("Calculating the rating of each user-agent")
        user_agent_notes = []
        for user_agent in self.liste_user_agents:
            user_agent_notes.append(self.scored_user_agent(user_agent))
        # Select a user-agent
        user_agent = random.choices(
            self.liste_user_agents,
            weights=user_agent_notes,
            k=1,
        )[0]
        # Update the last used time
        user_agent.last_used = time()
        return str(user_agent)
