# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

""" CSMGVT - Connected System Model Generator and Verification Tool.
"""

# Standard library imports
import logging
import os
import sys

# Local imports
from csmgvt.generators import ComponentsGenerator, CSMGenerator

# Internal library imports
from ecoa_toolset.arguments import check_ecoa_xml, create_output_directory, select_output_directory
from ecoa_toolset.configuration import ecoa_std_version
from ecoa_toolset.generators.types.generator import TypesGenerator
from ecoa_toolset.models.ecoa_model import ECOAModel
from ecoa_toolset.utils.arguments.argument_factory import ArgumentFactory
from ecoa_toolset.utils.arguments.custom_action import Once, OnceAndStoreTrue
from ecoa_toolset.utils.arguments.custom_type import check_checker_value, check_project_value
from ecoa_toolset.utils.arguments.optional import OptionalArgument
from ecoa_toolset.utils.logging.logger import Logger

logger = logging.getLogger(__name__)
languages = ["C", "C++"]


def _get_subpaths(ecoa_model) -> bool:
    subpaths = ["src", "CMakeLists.txt"]
    for component_path in ecoa_model.components.keys():
        component_impl_name = os.path.normpath(component_path).split(os.path.sep)[-2]
        subpaths.append(component_impl_name)
    return subpaths


def _create_argument_parser():
    return ArgumentFactory.create(
        "ecoa-csmgvt generates a framework for functional testing of an ECOA application on a desktop PC.\n"
        "ECOA standard version : {}".format(ecoa_std_version),
        [],
        [
            OptionalArgument(
                "-p",
                "--project",
                "The path (absolute or relative) to the ecoa project file.",
                action=Once,
                type=check_project_value,
                required=True,
            ),
            OptionalArgument(
                "-o",
                "--output",
                "The path (absolute or relative) where the CSM will be generated.",
                action=Once,
            ),
            OptionalArgument(
                "-l",
                "--log",
                (
                    "Set logging level\nAvailable levels:\n\t- "
                    + "\n\t- ".join([level for level in Logger.levels])
                    + "\nDefault to "
                    + Logger.levels[1]
                    + "."
                ),
                action=Once,
                default=Logger.levels[1],
                choices=Logger.levels,
            ),
            OptionalArgument(
                "-L",
                "--language",
                (
                    "[OSBOLETE] Set the source code programming language\nAvailable languages:\n\t- "
                    + "\n\t- ".join([lang for lang in languages])
                    + "\nDefault to "
                    + languages[1]
                    + "."
                ),
                action=Once,
                default=languages[1],
                choices=languages,
            ),
            OptionalArgument(
                "-v",
                "--verbose",
                "Displays additionnal information in the logs.",
                action=OnceAndStoreTrue,
            ),
            OptionalArgument(
                "-f",
                "--force",
                "Overwrite existing files.",
                action=OnceAndStoreTrue,
            ),
            OptionalArgument(
                "-k",
                "--checker",
                (
                    "External tool (absolute or relative) that checks the validity of ECOA XML files.\n"
                    + "Return 0 if xml files are valid."
                ),
                action=Once,
                type=check_checker_value,
                required=True,
            ),
        ],
    )


def main() -> None:
    """The entry point."""

    failure = False

    try:
        # Defining CLI arguments
        arg_parser = _create_argument_parser()

        # Parsing CLI arguments
        args = arg_parser.parse_args()
        check_ecoa_xml(args)

        # Init logger config for the entire app
        Logger.init(args.log, args.verbose)

        # Parsing ECOA project XML file
        project_file_name = os.path.basename(args.project)
        logger.debug("Parsing project file %s", project_file_name)
        ecoa_model = ECOAModel(project_file_name.split(".")[0], args.project)
        ecoa_model.parse()

        logger.debug("Found %d component(s)", ecoa_model.get_component_count())
        logger.debug("Found %d module(s)", ecoa_model.get_module_count())

        # Generating the output directory
        args.output = select_output_directory(args.project, args.output, ecoa_model.ecoa_xml_model._output)
        create_output_directory(args.force, args.output, subpaths=_get_subpaths(ecoa_model))

        # Generating the CSM files
        CSMGenerator(ecoa_model, args.output, args.force).generate()

        # Generating the components files
        ComponentsGenerator(ecoa_model, args.output, args.force).generate()

        # Generating the types files
        TypesGenerator(ecoa_model, args.output, args.force).generate()

    except KeyboardInterrupt:
        failure = True
        logger.critical("...Stopped\nCaught keyboard interrupt from user")

    except Exception as e:
        failure = True
        logger.critical(f"There was a critical error during execution of CSMGVT: {e}\nTerminating...")

    finally:
        # Display generation information
        Logger.display_generation_info("ecoa-csmgvt")

        # Showing execution results
        Logger.summary()
        sys.exit(1 if failure else 0)
