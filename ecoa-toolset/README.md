# ecoa-toolset

The ECOA Toolset contains common and basic utilities used by all ECOA tools.
It is not intended to be used as a standalone.

Documentation about the architecture, requirements and more are available in the [docs](./docs) directory.

The ECOA Toolset is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the software. The ECOA Toolset and its outputs are not claimed to be fit or safe for any purpose. Any user should satisfy themselves that this software or its outputs are appropriate for its intended purpose.

This software is MIT licensed : see file LICENSE.txt.

Copyright 2023 Dassault Aviation

## Structure

    .
    +-- CHANGELOG.md         # Changelog
    +-- docs                 # Documentation
        +-- source           # Sphinx documentation
    +-- LICENSE.txt          # License
    +-- MANIFEST.in          # Package distribution file
    +-- pyproject.toml       # Package configuration file
    +-- README.md
    +-- setup.py             # Package installation script
    +-- src                  # Source code
        +-- ecoa_toolset     # Actual package
    +-- tests                # Functional tests

## Prerequisites

* Python 3.8 or higher
* Pip 21.3 or higher
* Setuptools 64.0 or higher
* Unix or Windows 10 environment
* GCC
* Makefile
* CMake
* MSVC

## Installation

From the Git repository :

```sh
pip install -e .
```

From a Python packages repository :

```sh
pip install ecoa-toolset
```

with the following options: `--no-build-isolation --no-deps` in the command line or in the `pip.conf` file.
