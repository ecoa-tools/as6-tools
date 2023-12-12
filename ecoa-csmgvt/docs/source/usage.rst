.. Copyright 2023 Dassault Aviation
.. MIT License (see LICENSE.txt)

.. _usage:

*****
Usage
*****

This section aims to show how to use the differents options allowed in the tool. The tool must have been installed before, go see the
:ref:`installation<installation>`.

Basic run
#########

To run the CSMGVT tool:

.. code-block:: bash

    ecoa-csmgvt -p <path/to/the/ecoa/project/file> -k <path/to/the/checker>

Given paths can be absolute or relatif (from the current directory where the user run the tool).

Example
*******

Project Pingpong content:
::

  Pingpong
  +-- 0-Types
    +-- ECOA.h
    +-- ECOA.hpp
    +-- pingpong.types.xml
  +-- 1-Services
    +-- svc_PingPong.interface.xml
  +-- 2-ComponentDefinitions
    +-- Ping
      +-- Ping.componentType
      +-- Required-svc_PingPong.interface.qos.xml
    +-- Pong
      +-- Pong.componentType
      +-- Required-svc_PingPong.interface.qos.xml
  +-- 3-InitialAssembly
      +-- demo.composite
  +-- 4-ComponentImplementations
    +-- Ping
      +-- myDemoPing.impl.xml
    +-- Pong
      +-- myDemoPong.impl.xml
  +-- 5-Integration
    +-- demo.impl.composite
    +-- deployment.xml
    +-- logical_system.xml
  +-- pingpong.project.xml

In pingpong.project.xml, a relative path in <outputDirectory> is given : "Output".

.. code-block:: bash

    ecoa-csmgvt -p Pingpong/pingpong.project.xml -k ecoa-exvt

At the end of the command, a directory with the <outputDirectory> name appeared from where the user runs the tool.
::

    Pingpong
    +-- 0-Types
    +-- 1-Services
    +-- 2-ComponentDefinitions
    +-- 3-InitialAssembly
    +-- 4-ComponentImplementations
    +-- 5-Integration
    +-- pingpong.project.xml
    Output
    +-- src
      +-- CSM_pingpong.cpp
      +-- main.cpp
    +-- CMakeList.txt
    +-- results.log

Options
#######

Help
****

To display the ECOA version used and the different available options for the tool:

.. code-block:: bash

    ecoa-csmgvt -h

.. csv-table::
    :name: Help flags
    :header: "Flag", "Description"
    :widths: auto
    :delim: :
    :align: center
    :width: 66%

    "-h, --help":"Displays the optional parameters and the ECOA version of the tool."

Example
=======

Use the commande :

.. code-block:: bash

    ecoa-csmgvt --help

The help option displays the different options and the ECOA version used:

::

  usage: ecoa-csmgvt [-h] -p PROJECT [-o OUTPUT] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-L {C,C++}] [-v] [-f] -k CHECKER

  ecoa-csmgvt generates a framework for functional testing of an ECOA application on a desktop PC.
  ECOA standard version : 6

  optional arguments:
    -h, --help            show this help message and exit
    -p PROJECT, --project PROJECT
                          The path to the ecoa project file.
    -o OUTPUT, --output OUTPUT
                          The path to the CSM generation.
    -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                          Set logging level
                          Available levels:
                                  - DEBUG
                                  - INFO
                                  - WARNING
                                  - ERROR
                                  - CRITICAL
                          Default to INFO.
    -L {C,C++}, --language {C,C++}
                          Set the source code programming language
                          Available languages:
                                  - C
                                  - C++
                          Default to C++.
    -v, --verbose         Displays additionnal information in the logs.
    -f, --force           Overwrite existing files.
    -k CHECKER, --checker CHECKER
                          External tool that checks the validity of ECOA XML files.
                          Return 0 if xml files are valid.

Project
*******

The project option is **mandatory** and allows the tool to run a desire xml project.

.. code-block:: bash

    ecoa-csmgvt -p <path/to/the/ecoa/project/file> -k <path/to/the/checker>

.. csv-table::
    :name: Project flag
    :header: "Flag", "Description"
    :widths: auto
    :delim: :
    :align: center
    :width: 66%

    "-p, --project":"The path to the ecoa project file."

Example
=======

Project ECOA content:
::

  Pingpong
  +-- 0-Types
  +-- 1-Services
  +-- 2-ComponentDefinitions
  +-- 3-InitialAssembly
  +-- 4-ComponentImplementations
  +-- 5-Integration
  +-- pingpong.project.xml

In pingpong.project.xml, a relative path in <outputDirectory> is given : "Output".

.. code-block:: bash

    ecoa-csmgvt -p Pingpong/pingpong.project.xml -k ecoa-exvt

In the end, the Output directory appeared, from where the user runs the tool, with the CSMGVT generation files.

::

  PingPong
  +-- 0-Types
  +-- 1-Services
  +-- 2-ComponentDefinitions
  +-- 3-InitialAssembly
  +-- 4-ComponentImplementations
  +-- 5-Integration
  +-- pingpong.project.xml
  Output
  +-- src
    +-- CSM_pingpong.cpp
    +-- main.cpp
  +-- CMakeList.txt
  +-- results.log

Checker
*******

The checker option is **mandatory** and is an external tools that verifies if the xml project given in the input project flag is valid.
It returns 0 if the xml files are valid.

.. code-block:: bash

    ecoa-csmgvt -p <path/to/the/ecoa/project/file> -k <path/to/the/checker>

.. csv-table::
    :name: Checker flag
    :header: "Flag", "Description"
    :widths: auto
    :delim: :
    :align: center
    :width: 66%

    "-k, --checker":"Check the validity of ECOA XML files."

In pingpong.project.xml, a relative path in <outputDirectory> is given : "Output".

.. code-block:: bash

    ecoa-csmgvt -p Pingpong/pingpong.project.xml -k ecoa-exvt

In the end, the Output folder appeared from where the user runs the tool, with the CSMGVT generation files.

::

  PingPong
  +-- 0-Types
  +-- 1-Services
  +-- 2-ComponentDefinitions
  +-- 3-InitialAssembly
  +-- 4-ComponentImplementations
  +-- 5-Integration
  +-- pingpong.project.xml
  Output
  +-- src
    +-- CSM_pingpong.cpp
    +-- main.cpp
  +-- CMakeList.txt
  +-- results.log

Output
******

The output option allows to choose where to generate the CSM generated files even if the path does not exist.

.. warning:
    An output is mandatory when running the tool. It must be given either in the xml projet with the balistic <OutputDirectory>
    or with the -o (--output) flag. Be carefull, the -o flag surpasses the xml <OutputDirectory> if the two are given.
    The given path, either it is with the -o output flag or in the xml <OutputDirectory>, can be absolute or relative
    (files are generated from where the tool is run).

.. code-block:: bash

    ecoa-csmgvt -p <path/to/the/ecoa/project/file> -k <path/to/the/checker> -o <path/where/to/put/generated/files>

.. csv-table::
    :name: Output flags
    :header: "Flag", "Description"
    :widths: auto
    :delim: :
    :align: center
    :width: 66%

    "-o, --output":"Path where the files will be generated."

Example
=======

Project ECOA content:
::

  Pingpong
  +-- 0-Types
  +-- 1-Services
  +-- 2-ComponentDefinitions
  +-- 3-InitialAssembly
  +-- 4-ComponentImplementations
  +-- 5-Integration
  +-- pingpong.project.xml

In pingpong.project.xml, a relative path in <outputDirectory> is given : "Output".

.. code-block:: bash

    ecoa-csmgvt -p Pingpong/pingpong.project.xml -k ecoa-exvt -o Result/Output

<outputDirectory> in the xml and the output -o flag are given, the tool will take the output given in the -o flag
and create the result directory (if the path is relative, from where the user runs the tool).
::

  Pingpong
  +-- 0-Types
  +-- 1-Services
  +-- 2-ComponentDefinitions
  +-- 3-InitialAssembly
  +-- 4-ComponentImplementations
  +-- 5-Integration
  +-- pingpong.project.xml
  Result
  +-- Output
      +-- src
        +-- CSM_pingpong.cpp
        +-- main.cpp
      +-- CMakeList.txt
      +-- results.log

Log Level
*********

The log option displays specific informations during tool exacution.

.. code-block:: bash

    ecoa-csmgvt -p <path/to/the/ecoa/project/file> -k <path/to/the/checker> -lKEYWORD*

.. csv-table::
    :name: Log flags
    :header: "Flag", "Description"
    :widths: auto
    :delim: :
    :align: center
    :width: 66%

    "-l, --log":"Displays additionnal information during the run."

Specific arameters can be combined with -l flag :

.. csv-table::
    :name: Log Parameters
    :header: "Parameters", "Description"
    :widths: auto
    :delim: :
    :align: center
    :width: 66%

    "DEBUG":"Displays all the informations."
    "INFO":" (default) Displays the information messages only."
    "WARNING":"Displays the warning messages only."
    "ERROR":"Displays the error messages only."
    "CRITICAL":"Displays the critical messages only."

Example
=======

When running the tool with the log option, more specific informations will be displayed.

.. code-block:: bash

    ecoa-csmgvt -p Pingpong/pingpong.project.xml -k ecoa-exvt -lDEBUG

Example of output during the run:

.. code-block:: bash

    Parsing simple types from libmarx
    Parsing record types from libmarx
    Parsing constant types from libmarx
    Parsing variant_record types from libmarx
    Parsing array types from libmarx
    Parsing fixed_array types from libmarx
    Parsing enum types from libmarx
    Parsing component implementation: myElder
    Parsing modules
    myElder_Main_impl libraries: ['libmarx']
    Parsing dataRead from module type: myElder_Main_t and module implementation: myElder_Main_impl
    Linking EventSend (16) and EventReceived (17)
    Linking myElder:myElder_Main_t:myElder_Main_inst:command to myCadet:myCadet_Main_t:myCadet_Main_inst:older_command
    Linking myElder:myElder_Main_t:myElder_Main_inst:command to myCadet:myCadet_Main_t:myCadet_Main_inst:older_command
    Linking myElder:myElder_Main_t:myElder_Main_inst:command to myCadet:myCadet_Main_t:myCadet_Main_inst:older_command
    Linking myElder:myElder_Main_t:myElder_Main_inst:command to myCadet:myCadet_Main_t:myCadet_Main_inst:older_command
    Linking myElder:myElder_Main_t:myElder_Main_inst:command to myJunior:myJunior_Main_t:myJunior_Main_inst:command

Language
********

This option is obsolete.

Verbose
*******

The verbose option displays more detailled information when the tool is running.

.. code-block:: bash

    ecoa-csmgvt -p <path/to/the/ecoa/project/file> -k <path/to/the/checker> -v

.. csv-table::
    :name: Verbose flags
    :header: "Flag", "Description"
    :widths: auto
    :delim: :
    :align: center
    :width: 66%

    "-v, --verbose":"Displays additionnal information in the logs."

Example
=======

Project ECOA content:
::

  Pingpong
  +-- 0-Types
  +-- 1-Services
  +-- 2-ComponentDefinitions
  +-- 3-InitialAssembly
  +-- 4-ComponentImplementations
  +-- 5-Integration
  +-- pingpong.project.xml

When running the tool with the verbose options, the results.log file will appaered and be filled.

.. code-block:: bash

    ecoa-csmgvt -p Pingpong/pingpong.project.xml -k ecoa-exvt -v

::

  PingPong
  +-- 0-Types
  +-- 1-Services
  +-- 2-ComponentDefinitions
  +-- 3-InitialAssembly
  +-- 4-ComponentImplementations
  +-- 5-Integration
  +-- pingpong.project.xml
  Output
  +-- src
    +-- CSM_pingpong.cpp
    +-- main.cpp
  +-- CMakeList.txt
  +-- results.log

Exemple of the beginning of the results.log file:

.. code-block:: bash

    [1mParsing project file marx_brothers.project.xml[0m
    [32mParsing xml_only_marx/marx_brothers.project.xml[0m
    [32m	0-Types/libmarx.types.xml[0m
    [32m	1-Services/brother.interface.xml[0m
    [32m	4-ComponentImplementations/myElder/myElder.impl.xml[0m
    [32m	4-ComponentImplementations/myCadet/myCadet.impl.xml[0m
    [32m	4-ComponentImplementations/myJunior/myJunior.impl.xml[0m
    [32m	5-Integration/marx_brothers.impl.composite[0m
    [32m	5-Integration/marx_brothers.deployment.xml[0m
    [1m== PRINT TYPES ==[0m

Force
*****

The force option allows to overwrite already generated files.

.. code-block:: bash

    ecoa-csmgvt -p <path/to/the/ecoa/project/file> -k <path/to/the/checker>
    ecoa-csmgvt -p <path/to/the/ecoa/project/file> -k <path/to/the/checker> -f

.. csv-table::
    :name: Force flags
    :header: "Flag", "Description"
    :widths: auto
    :delim: :
    :align: center
    :width: 66%

    "-f, --force":"Overwrite existing generated files."

Example
=======

Project ECOA content:
::

  Pingpong
  +-- 0-Types
  +-- 1-Services
  +-- 2-ComponentDefinitions
  +-- 3-InitialAssembly
  +-- 4-ComponentImplementations
  +-- 5-Integration
  +-- pingpong.project.xml

In pingpong.project.xml, the <outputDirectory> is "Output".

.. code-block:: bash

    ecoa-csmgvt -p Pingpong/pingpong.project.xml -k ecoa-exvt

At the end of the command, a directory with the name given in the pingpong.project.xml, <outputDirectory>, appaeared from where the user runs the tool, with the CSMGVT generation files.
::

  Pingpong
  +-- 0-Types
  +-- 1-Services
  +-- 2-ComponentDefinitions
  +-- 3-InitialAssembly
  +-- 4-ComponentImplementations
  +-- 5-Integration
  +-- pingpong.project.xml
  Output
  +-- src
    +-- CSM_pingpong.cpp
    +-- main.cpp
  +-- CMakeList.txt
  +-- results.log

.. code-block:: bash

    ecoa-csmgvt -p Pingpong/pingpong.project.xml -k ecoa-exvt -f

At the end of the command, the directory will be overwritten.
::

  Pingpong
  +-- 0-Types
  +-- 1-Services
  +-- 2-ComponentDefinitions
  +-- 3-InitialAssembly
  +-- 4-ComponentImplementations
  +-- 5-Integration
  +-- pingpong.project.xml
  Output
  +-- src
    +-- CSM_pingpong.cpp
    +-- main.cpp
  +-- CMakeList.txt
  +-- results.log
