# -*- coding: utf-8 -*-
"""
Script global variables settings
"""

"""
=========PATHS=========
"""
# Cache path for user-agents
FICHIER_CACHE_USER_AGENT:str = "user_agent.json"

"""
=========GENERAL OPTIONS=========
"""
# Updating user_agents list (True) or not (False)
USER_AGENT_UPDATE:bool = False
# Used to limit url parsing to speed up testing, set to None in order to parse all urls
URL_PARSER_LIMITATION:int|None = 5

"""
=========PROXY=========
HTTP link to your proxy, single or rotating
"""
PROXY:str = ""

"""
=========TIMEOUTS=========
Various timeouts for scrapling fetchers by utility
"""
SIMPLE_TIMEOUT:int = 1000  # in milliseconds, basic usage
ADVANCED_TIMEOUT:int = 2000  # in milliseconds, stealthy fetcher option because of playwright lib latence

"""
=========URL Filters=========
List of postcodes used to filter url when fetching urls :
- IDF = ["75", "77", "78", "91", "92", "93", "94", "95"]
- Paris = [75000, "75001", "75002", "75003", "75004", "75005", "75006", "75007", "75008", "75009", "75010", "75011", "75012", "75013", "75014", "75016", "75116", "75017", "75018", "75019", "75020"]
- Lyon = ["6900", "69001", "69002", "69003", "69004", "69005", "69005", "69006", "69007", "69008", "69009"]
- Toulouse = ["31000", "31100", "31200", "31300", "31400", "31500", "31004", "31090", "31043"]
"""
DEPARTMENTS:list[str] = ["75", "77", "78", "91", "92", "93", "94", "95"]
