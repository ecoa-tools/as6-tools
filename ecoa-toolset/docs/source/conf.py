#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "ecoa-toolset"
copyright = "2023, Dassault Aviation"
author = "Dassault Aviation"
release = "1.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]

templates_path = ["_templates"]
exclude_patterns = []

# Setting up the package directory

sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "src")))

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
