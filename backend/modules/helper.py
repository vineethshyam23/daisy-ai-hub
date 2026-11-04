import os
import pathlib
from types import SimpleNamespace
import logging

import yaml

# Use centralized logging configuration
try:
    from config import get_logger
    logger = get_logger(__name__)
except ImportError:
    # Fallback to basic logging if config module is not available
    logger = logging.getLogger(__name__)


def loadConfig(filename: str, namespace: bool = False):
    base = pathlib.Path(__file__).parents[1].resolve()  # Updated to navigate up two levels instead of one
    cfg_path = os.path.join(base, 'config', f'{filename}')
    try:
        if os.path.exists(cfg_path):
            logger.info(f'Loading config file: {cfg_path}')
            with open(cfg_path, 'r') as yaml_file:
                logger.info(f'Loading info from yaml file: {cfg_path}')
                config = yaml.load(yaml_file, Loader=yaml.FullLoader)
                if namespace:
                    return SimpleNamespace(**config)
                else:
                    return config
    except Exception as e:
        logger.error(e)
        raise