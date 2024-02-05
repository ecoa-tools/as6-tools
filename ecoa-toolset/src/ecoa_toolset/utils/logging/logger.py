# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""The logger implementation."""

# Standard library imports
import logging
import shutil
import sys
from datetime import datetime
from importlib.metadata import version
from typing import Dict

# Third-Party library imports
import colorama

logger = logging.getLogger()

CALL_COUNTER = {
    logging.DEBUG: 0,
    logging.INFO: 0,
    logging.WARNING: 0,
    logging.ERROR: 0,
    logging.CRITICAL: 0,
}

logging_formats = {
    logging.DEBUG: colorama.Style.BRIGHT,
    logging.INFO: colorama.Fore.GREEN,
    logging.WARNING: colorama.Fore.YELLOW,
    logging.ERROR: colorama.Fore.RED + colorama.Style.DIM,
    logging.CRITICAL: colorama.Fore.RED + colorama.Style.BRIGHT,
}


class CustomFormatter(logging.Formatter):
    """Custom formatter for logging."""

    _format: str = None

    # Logging displays format
    _simple_format: str = "%(message)s"
    _verbose_format: str = "%(asctime)s | %(levelname)-8s | %(message)s (%(name)s:%(lineno)d)"
    _FORMATS: Dict[int, str] = {}

    def __init__(self, verbose: int) -> None:
        self._format = self._verbose_format if verbose else self._simple_format
        self._FORMATS = {
            level: logging_formats[level] + self._format + colorama.Style.RESET_ALL for level in logging_formats
        }

    def format(self, record) -> str:
        global CALL_COUNTER
        CALL_COUNTER[record.levelno] += 1
        log_fmt = self._FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Logger:
    """Logging wrapper."""

    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    @classmethod
    def init(cls, log_level: str, verbose: bool) -> None:
        # Transform log level value from string to numeric
        numeric_level = getattr(logging, log_level.upper(), None)
        # Initialize colorama
        colorama.init()
        # Basic config
        logging.basicConfig(level=numeric_level)
        # Remove default handlers
        logging.getLogger().handlers.clear()
        # Creates file and error stream handlers
        fh = logging.FileHandler(filename="results.log", encoding="utf-8", mode="w")
        sh_err = logging.StreamHandler(sys.stderr)
        # Set custom formatter to file and error stream handlers
        fh.setFormatter(CustomFormatter(verbose))
        sh_err.setFormatter(CustomFormatter(verbose))
        # Filter the stderr stream handler so that only ERROR and CRITICAL are handled by it
        logging_limit = logging.ERROR
        sh_err.addFilter(lambda x: x.levelno >= logging_limit)
        # Add file and error stream handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(sh_err)
        # Creates a output stream handler only if needed
        if numeric_level < logging_limit:
            sh_out = logging.StreamHandler(sys.stdout)
            # Set custom formatter to the output stream handler
            sh_out.setFormatter(CustomFormatter(verbose))
            # Filter the output stream handler so that only DEBUG, INFO and WARNING are handled by it
            sh_out.addFilter(lambda x: x.levelno < logging_limit)
            # Add the output stream handler to the logger
            logger.addHandler(sh_out)

    @classmethod
    def display_generation_info(cls, toolname: str) -> None:
        terminal_line_size = shutil.get_terminal_size().columns
        gen_info_title = "GENERATION INFORMATION"
        separator_length = max((terminal_line_size - len(gen_info_title) - 2) // 2, 0)
        logger.info(
            "=" * separator_length
            + (" " if separator_length > 0 else "")
            + gen_info_title
            + (" " if separator_length > 0 else "")
            + "="
            * (
                separator_length
                if separator_length == 0 or 2 * separator_length + len(gen_info_title) + 2 == terminal_line_size
                else separator_length + 1
            )
        )
        logger.info("Tool version : %s", version(toolname))
        logger.info("Date and time : %s", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))

    @classmethod
    def summary(cls) -> None:
        """Print number of critical, error and warning messages that have appeared."""

        """
        Calculating the results
        CALL_COUNTER global variable is incremented as many times as there are
        handlers ; the workaround is to divide by the number of handlers
        """
        number_of_handlers = len(logger.handlers) or 1
        number_of_critical = int(CALL_COUNTER[logging.CRITICAL] / number_of_handlers)
        number_of_error = int(CALL_COUNTER[logging.ERROR] / number_of_handlers)
        number_of_warning = int(CALL_COUNTER[logging.WARNING] / number_of_handlers)

        # Logging results
        logger.info("Ends with : ")
        logger.info(f" - {number_of_critical} critical message(s)")
        logger.info(f" - {number_of_error} error message(s)")
        logger.info(f" - {number_of_warning} warning message(s)")
