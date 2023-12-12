# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

""" MSCIGT - Module Skeletons and Container Interfaces Generator Tool.
"""

# Standard library imports
import logging
import os
import sys

# Local imports
from mscigt.component.generator import ComponentGenerator
from mscigt.templates import Templates

# Internal library imports
from ecoa_toolset.arguments import check_ecoa_xml, create_output_directory, select_output_directory
from ecoa_toolset.configuration import ecoa_std_version
from ecoa_toolset.generators.types.generator import TypesGenerator
from ecoa_toolset.models.ecoa_model import ECOAModel
from ecoa_toolset.utils.arguments.argument_factory import ArgumentFactory
from ecoa_toolset.utils.arguments.custom_action import Once, OnceAndStoreTrue
from ecoa_toolset.utils.arguments.custom_type import check_checker_value, check_project_value, check_template_value
from ecoa_toolset.utils.arguments.optional import OptionalArgument
from ecoa_toolset.utils.logging.logger import Logger

logger = logging.getLogger(__name__)


def _generate_module_implementations(ecoa_model, project: str, output: str, force: bool, templates: Templates) -> None:
    for path, component_implementation in ecoa_model.components.items():
        component_directory_path = os.path.join(os.path.dirname(project), os.path.split(path)[0])
        component_impl_name = os.path.basename(component_directory_path)
        for module in component_implementation.module_implementation:
            module_directory_path = os.path.join(component_directory_path, module.name)
            logger.debug("Attempt to create directory %s", module_directory_path)
            if os.path.exists(module_directory_path):
                logger.debug("%s module directory already exists !", module_directory_path)
            else:
                os.mkdir(module_directory_path)
                logger.debug("Created module directory %s", module_directory_path)
            ComponentGenerator(
                ecoa_model, module_directory_path, component_impl_name, module.name, force, templates, output
            ).generate()


def _create_argument_parser():
    return ArgumentFactory.create(
        "ecoa-mscigt generate container interfaces and module skeletons\n"
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
                "The path (absolute or relative) where the 0-Types folder will be generated.",
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
                "-t",
                "--template",
                "The path to the directory containing code and header templates.",
                action=Once,
                type=check_template_value,
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

        # Checking the ECOA XML files
        check_ecoa_xml(args)

        # Init logger config for the entire app
        Logger.init(args.log, args.verbose)

        templates = Templates(args.template)

        # Parsing ECOA project XML file
        project_file_name = os.path.basename(args.project)
        logger.debug("Parsing project file %s", project_file_name)
        ecoa_model = ECOAModel(project_file_name.split(".")[0], args.project)
        ecoa_model.parse()

        logger.debug("Found %d component(s)", ecoa_model.get_component_count())
        logger.debug("Found %d module(s)", ecoa_model.get_module_count())

        # Generating the output directory
        args.output = select_output_directory(args.project, args.output, ecoa_model.ecoa_xml_model._output)
        create_output_directory(args.force, args.output)

        # Generating the module implementation files
        _generate_module_implementations(ecoa_model, args.project, args.output, args.force, templates)

        # Generating the types files
        TypesGenerator(ecoa_model, args.output, args.force, templates=templates).generate()

    except KeyboardInterrupt:
        failure = True
        logger.critical("...Stopped\nCaught keyboard interrupt from user")

    except Exception as e:
        failure = True
        logger.critical(f"There was a critical error during execution of MSCIGT: {e}\nTerminating...")

    finally:
        # Display generation information
        Logger.display_generation_info("ecoa-mscigt")

        # Showing execution results
        Logger.summary()
        sys.exit(1 if failure else 0)
