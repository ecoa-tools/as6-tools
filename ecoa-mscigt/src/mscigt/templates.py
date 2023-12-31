# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Templates class.
"""

# Standard library imports
import datetime
import os
from typing import Dict, List

# Third-Party library imports
import pkg_resources


class Templates:
    """"""

    _path: str = None
    _user: Dict[str, List] = None
    _default: List = None

    def __init__(self, path: str) -> None:
        self._path = path
        self._open_user_templates()
        self._create_default_template()

    def _open_user_templates(self) -> None:
        self._user = {}
        if self._path:
            for file_name in os.listdir(self._path):
                file_path = os.path.join(self._path, file_name)
                if os.path.isfile(file_path):
                    self._open_user_template(file_path, file_name)

    def _open_user_template(self, file_path: str, file_name: str) -> None:
        root, ext = os.path.splitext(file_name)
        if (root == "header_template" and ext in [".h", ".hpp"]) or (root == "code_template" and ext in [".c", ".cpp"]):
            with open(file_path) as f:
                self._user[ext] = f.readlines()

    def _create_default_template(self) -> None:
        self._default = []
        self._default.append("")
        self._default.append("@file FILE")
        self._default.append("@date DATE")
        self._default.append("@time TIME")
        self._default.append("")
        self._default.append("Generated by : MSCIGT MSCIGT_VERSION")
        self._default.append("               Copyright (c) 2023 Dassault Aviation")
        self._default.append("")

    def _replace_tags(self, template: List, file_name: str) -> None:
        new_template = []
        for line in template:
            new_line = line
            new_line = new_line.replace("FILE", file_name)
            new_line = new_line.replace("DATE", datetime.datetime.now().strftime("%Y-%m-%d"))
            new_line = new_line.replace("TIME", datetime.datetime.now().strftime("%H:%M:%S.%f"))
            new_line = new_line.replace("MSCIGT_VERSION", pkg_resources.require("ecoa-mscigt")[0].version)
            new_template.append(new_line)
        return new_template

    def generate(self, key: str, file_name: str, file_description: str, file_unmodifiable=False) -> str:
        generation = ""
        if self._user.get(key):
            user = self._replace_tags(self._user.get(key), file_name)
            for line in user:
                generation += line
        else:
            default = self._replace_tags(self._default, file_name)
            default.append(file_description)
            if file_unmodifiable:
                default.append("Warning : This file shall not be modified")
            default.append("")
            block_width = len(max(default, key=len))
            generation += "/" + ("*" * (block_width + 4)) + "/\n"
            for line in default:
                generation += "/* " + line + (" " * (block_width - len(line))) + " */\n"
            generation += "/" + ("*" * (block_width + 4)) + "/\n\n"
        return generation
