# logs.py
from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler

_LOGGER_NAME = "loja"
_LOG_DIR = "logs"
_LOG_FILE = os.path.join(_LOG_DIR, "app.log")


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def get_logger(name: str | None = None) -> logging.Logger:
    """Logger com arquivo + console; evita handlers duplicados entre imports."""
    _ensure_dir(_LOG_DIR)

    logger = logging.getLogger(name or _LOGGER_NAME)
    logger.setLevel(logging.INFO)
    logger.propagate = False  # não repassar para o root (evita logs duplicados)

    # Evita duplicar handlers se já configurado
    have_file = any(isinstance(h, RotatingFileHandler) for h in logger.handlers)
    have_console = any(isinstance(h, logging.StreamHandler) and not isinstance(h, RotatingFileHandler)
                       for h in logger.handlers)

    if not have_file:
        fh = RotatingFileHandler(_LOG_FILE, maxBytes=512_000, backupCount=3, encoding="utf-8")
        fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        logger.addHandler(fh)

    if not have_console:
        ch = logging.StreamHandler()  # stdout -> aparece em `docker logs`
        ch.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        logger.addHandler(ch)

    # Garante que o arquivo exista mesmo sem logs ainda
    try:
        with open(_LOG_FILE, "a", encoding="utf-8"):
            pass
    except Exception:
        pass

    return logger

