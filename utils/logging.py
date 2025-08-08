# -*- coding: utf-8 -*-
"""
Configuration et utilitaires pour le logging
"""

import logging
import os
from datetime import datetime


def setup_logging(log_dir: str = "logs") -> str:
    """
    Configure le logging pour écrire à la fois dans un fichier et la console

    Args:
        log_dir (str): Chaîne de caractère représentant le répertoire où stocker les logs

    Returns:
        TextIO: Un objet fichier JSON ouvert en mode lecture.
    """
    # Créer le répertoire de logs s'il n'existe pas
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Créer le nom du fichier de log avec horodatage
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    log_file = os.path.join(log_dir, f"scraping_{timestamp}.log")

    # Configuration du format de log
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # Obtenir le logger root
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Supprimer les handlers existants
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Handler pour la console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Handler pour le fichier
    file_handler = logging.FileHandler(log_file, encoding="utf-8", mode="w")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_file}")

    return log_file
