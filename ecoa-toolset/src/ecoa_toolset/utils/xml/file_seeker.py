# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""
The file seeker implementation.
"""

from glob import glob


class FileSeeker:
    """
    The File Seeker.
    """

    @staticmethod
    def search_in_directory(search_path: str, file_pattern: str) -> dict:
        """
        Searches files recursively inside a folder.

        Args:
            search_path (str): The path to search the file.
            file_pattern (str): The file pattern.

        Returns:
            dict: The dictionary of files.
        """

        files_dict = {}
        for file_name in glob(search_path + "/**/" + file_pattern, recursive=True):
            files_dict[file_name.split("/")[-1].split(".")[0]] = file_name
        return files_dict

    @staticmethod
    def search(file_pattern: str) -> dict:
        """
        Searches files recursively inside the current folder.

        Args:
            file_pattern (str): The file pattern.

        Returns:
            dict: The dictionary of files.
        """

        files_dict = {}
        for file_name in glob("./**/" + file_pattern, recursive=True):
            files_dict[file_name.split("/")[-1].split(".")[0]] = file_name
        return files_dict
