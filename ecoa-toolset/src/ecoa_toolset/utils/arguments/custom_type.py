# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""The custom types functions."""

# Standard library imports
import argparse
import os
import shutil


def check_checker_value(checker_executable_path):
    """Check if the checker executable exists and is valid.

    Args:
        checker_executable_path (str): The checker executable path.

    Returns:
        checker_executable_path (str): The checker executable path.

    Raise:
        argparse.ArgumentTypeError
    """
    if not shutil.which(checker_executable_path.split()[0]):
        raise argparse.ArgumentTypeError("invalid value, executable path doesn't exists.")
    return checker_executable_path


def check_project_value(project_file_path):
    """Check if the project file exists and is valid.

    Args:
        project_file_path (str): The project file path.

    Returns:
        project_file_path (str): The project file path.

    Raise:
        argparse.ArgumentTypeError
    """
    if not os.path.exists(project_file_path):
        raise argparse.ArgumentTypeError("invalid value, path doesn't exists")
    if not os.path.isfile(project_file_path):
        raise argparse.ArgumentTypeError("invalid value, path is not leading to a file")
    root, ext = os.path.splitext(project_file_path)
    if not (os.path.splitext(root)[1] == ".project" and ext == ".xml"):
        raise argparse.ArgumentTypeError("invalid value, path is not leading to an ecoa project file")
    return project_file_path


def check_template_value(template_directory_path):
    """Check if the template directory exists and is valid.

    Args:
        template_directory_path (str): The template directory path.

    Returns:
        template_directory_path (str): The template directory path.

    Raise:
        argparse.ArgumentTypeError
    """
    if not os.path.exists(template_directory_path):
        raise argparse.ArgumentTypeError("invalid value, path doesn't exists")
    if not os.path.isdir(template_directory_path):
        raise argparse.ArgumentTypeError("invalid value, path is not leading to a directory")
    return template_directory_path
