# ECOA IHM

This repository contains the code source of the ECOA IHM.
The ECOA IHM allows to launch the ECOA Tools via an interface instead of a command line.

The ECOA IHM is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the software. The ECOA IHM and its outputs are not claimed to be fit or safe for any purpose. Any user should satisfy themselves that this software or its outputs are appropriate for its intended purpose.

This software is MIT licensed : see file LICENSE.txt.

Copyright 2023 Dassault Aviation

## Table of Contents

* Structure
* Prerequisites
* Installation
* Usage

## Structure

    .
    +-- ecoa_ihm.py      # ECOA IHM Entry Point
    +-- ecoa_app.py      # ECOA IHM Application
    +-- images           # Images used by the IHM
    +-- LICENSE.txt      # License
    +-- README.md
    +-- requirements.txt # Dependencies

## Prerequisites

* Python 3.8 or higher
* ecoa-exvt
* ecoa-asctg
* ecoa-mscigt
* ecoa-csmgvt
* ecoa-ldp

## Installation

```sh
pip install -r requirements.txt
```

## Usage

```sh
python ecoa_ihm.py
```
