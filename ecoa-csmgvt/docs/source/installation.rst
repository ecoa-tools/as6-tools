.. Copyright 2023 Dassault Aviation
.. MIT License (see LICENSE.txt)

.. _installation:

************
Installation
************

This category aims to explain each step needed to install the CSMGVT tool.

.. warning::
    In order to succeed the installation of the tool, please verify that those :underline:`prerequisites` are respected:|br|

      * Python 3.8 or higher |br|
      * Pip 21.3 or higher |br|
      * Setuptools 64.0 or higher |br|
      * Unix or Windows 10 environment |br|
      * GCC or MSVC |br|
      * Makefile or MSVC |br|
      * CMake |br|
      * Checker to run the tool |br|
      * Visual Studio (min 22 2017, for Windows) |br|

(Optional) Create and activate the virtual environnement
********************************************************

If needed, at the root of the ECOA tool directory, create and activate the virtual python environnement following those lines:

**Linux**

.. code-block:: bash

    python3 -m venv .venv
    source .venv/bin/activate

**Windows**

.. code-block:: bash

    py -3 -m venv venv
    venv/Scripts/activate.bat

Installation of the tools
*************************

At the root of the ecoa directory, install the following tools:

.. code-block:: bash

    cd path/to/tool/ecoa-csmgvt
    pip install -e . --no-build-isolation --no-deps

.. note::
    ecoa-exvt, a tool in the genplatform directory, is a tool used to check if the xml project entry follows the structure of ECOA standard.
    Checker is mandatory but if you're using your own, :underline:`installing ecoa-exvt is not mandatory`.
    It returns 0 when the checker valids the xml files.

CSMGVT tool is now installed, to see if the installation worked, call the help flag of the tool:

    .. code-block:: bash

        ecoa-csmgvt -h
        (or) ecoa-csmgvt --help

A block of optional arguments displays. To know more about the usage of the different parameters of the tool, you can read the :ref:`usage<usage>` documentation.

Error output
============

If you obtain this error when installing the tool :
    .. code-block:: bash

        ERROR: File "setup.py" not found. Directory cannot be installed in editable mode: /ldisk/tmp_users/emalherb/taches/ecoa-tools/ecoa-csmgvt
        (A "pyproject.toml" file was found, but editable mode currently requires a setup.py based build.)

        Solution:
        pip install pip --upgrade
        (On a Dassault host) pip install pip --upgrade -i http://svinfulanxu.dassault-avion.fr:8081/repository/SODA-pypi/simple --trusted-host svinfulanxu.dassault-avion.fr

        pip install setuptools --upgrade
        (On a Dassault host) pip install setuptools --upgrade -i http://svinfulanxu.dassault-avion.fr:8081/repository/SODA-pypi/simple --trusted-host svinfulanxu.dassault-avion.fr

If you obtain this error when installing the tool :
    .. code-block:: bash

        Traceback (most recent call last):
          File "/ldisk/tmp_users/emalherb/ecoa-tools/.venv/bin/ecoa-csmgvt", line 5, in <module>
            from csmgvt.__main__ import main
          File "/ldisk/tmp_users/emalherb/ecoa-tools/ecoa-csmgvt/src/csmgvt/__main__.py", line 11, in <module>
            from csmgvt.c.strategy import CLanguageStrategy
          File "/ldisk/tmp_users/emalherb/ecoa-tools/ecoa-csmgvt/src/csmgvt/c/strategy.py", line 8, in <module>
            from csmgvt.c.cmakelists import CMakeListsGenerator
          File "/ldisk/tmp_users/emalherb/ecoa-tools/ecoa-csmgvt/src/csmgvt/c/cmakelists.py", line 11, in <module>
            from csmgvt.cmakelists import CMakeListsGenerator as GlobalCMakeListsGenerator
          File "/ldisk/tmp_users/emalherb/ecoa-tools/ecoa-csmgvt/src/csmgvt/cmakelists.py", line 8, in <module>
            from ecoa_toolset.generators.common import Common
        ModuleNotFoundError: No module named 'ecoa_toolset'

        Solution:
        (at root directory) cd path/to/tool/ecoa-toolset
        pip install -e . --no-build-isolation --no-deps

Compilation
===========

To know more about the compilation of the tool, you can read the :ref:`compilation<compilation>` documentation.
