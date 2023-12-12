# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Functions to manipulate tool arguments.
"""

# Standard library imports
import logging
import os
import subprocess
from typing import List

logger = logging.getLogger(__name__)


def check_ecoa_xml(args: List) -> None:
    """Check if the checker flag is used and check the given ecoa xml is valid.

    Args:
        args: optional arguments

    Returns:
        None
    """
    result = subprocess.run(args.checker.split() + ["-p", args.project])
    if result.returncode != 0:
        raise Exception("The check of the ECOA XML file : " + args.project + " failed.")


def _check_output_directory(path: str, subpaths: List[str]) -> bool:
    for subpath in subpaths:
        if os.path.exists(os.path.join(path, subpath)):
            return True
    return False


def select_output_directory(project_flag: str, output_flag: str, xml_output: List[str]) -> str:
    """Selects the output directory :
        - given by the output flag if used
        - given by the project xml file otherwise

    Args:
        project_flag (str) : The path to the project xml file given by the project flag.
        output_flag (str) : The path to the output directory given by the output flag.
        xml_output (List[str]) : The paths to the output directory given by the project xml file.

    Return:
        str : The path to the output directory.
    """
    if output_flag:
        return output_flag
    elif xml_output:
        xml_output = xml_output[0]
        if os.path.isabs(xml_output):
            return xml_output
        else:
            return os.path.join(os.path.dirname(project_flag), xml_output)
    else:
        raise ValueError("No given output ! Please use -o or --output flag or give the output in the xml project.")


def create_output_directory(force: bool, path: str, subpaths: List[str] = []) -> None:
    """Creates the output directory if it doesn't exist.
    Checks that elements to be generated do not exist otherwise.

    Args:
        force (bool) : The force flag.
        path (str) : The path to the output directory.
        subpaths (List[str]) : The elements to be generated.
    """
    if not os.path.exists(path):
        logger.debug("%s doesn't exists", path)
        os.makedirs(path)
        logger.debug("%s created", path)
    else:
        if force:
            logger.debug("%s exists, overwriting its contents...", path)
        else:
            logger.debug("%s exists, checking its contents...", path)
            if _check_output_directory(path, subpaths):
                raise ValueError(
                    path
                    + " exists and elements to be generated too ! "
                    + "Please use -f or --force flag to overwrite its contents."
                )
            logger.debug("%s exists but elements to be generated doesn't, writing its contents...", path)
