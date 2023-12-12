# CSMGVT VDD

Reference: DGT 2034174  
Version: B  
Copyright 2023 Dassault Aviation
MIT License (see LICENSE.txt)

## 1. Version Description

The Connected System Model Generator and Verification Tool (`CSMGVT`) allows to
generate a framework for functional testing of an ECOA application on a desktop PC
without an ECOA middleware and without real time considerations.

The 1.0.0 version of CSMGVT introduces those features:
* Installation and usage documentation.
* Initial version of CSM Generator and Verification Tool.

## 2. Version identification
### CSMGVT

|Product|Version|Description|
|-------|:-----:|----------:|
|CSMGVT|v1.0.0|Initial version of CSM Generator and Verification Tool.|

### Packages

|Product|Version|Description|
|-------|:-----:|----------:|
|ecoa-csmgvt|v1.0.0|Initial version of CSM Generator and Verification Tool.|
|ecoa-toolset|v1.0.0|Tools aiming to reduce development and through-life costs of complex software.|

### Documentation

|Product|Version|Description|
|-------|:-----:|----------:|
|CSMGVT|v1.0.0|User documentation (installation, usage and compilation)|
|DGT 2021740|A|TOR-TORTC: Tool Operational Requirements and Test Cases for CSMGVT|

## Environment / Compatibility

Linux: CentOS 7.X or higher  
Windows: 10 build 1909 or higher

ECOA Architecture Specifications Version 6

## Evolution

|Version|Version date|Summary of changes|
|:-----:|:----------:|-----------------:|
|A|May 16, 2023|Initial version.|
|B|August 25, 2023|Correction of the requirements coverage for Windows. Added TOR_CSMGVT_REQ_200 requirement in "Limitations" section.|

## Correction

Initial version.

## Requirements Coverage

Number of requirements: 54

Linux (MANDATORY):

|Fully covered|Partially covered|Not covered|Other|Total|
|:-----------:|:---------------:|:---------:|:---:|:---:|
|90.7%|7.4%|0%|1.9%|100%|

Windows (DESIRABLE):

|Fully covered|Partially covered|Not covered|Other|Total|
|:-----------:|:---------------:|:---------:|:---:|:---:|
|74.1%|9.3%|0%|16.7%|100%|

## Limitations / Possible problems / Known errors

### Limitations

|Requirement|Status|Linux|Windows|Comment|
|:----------|:----:|:---:|:-----:|------:|
|TOR_CSMGVT_REQ_030|Not applicable||x|Linux requirement.|
|TOR_CSMGVT_REQ_031|Not applicable|x||Windows requirement.|
|TOR_CSMGVT_REQ_100|Partially covered|x|x|Recursive assembly/cross-views not supported. Multi-plateform can not be managed. Modules can't have the same name. Timout is not activated at the execution through the generated code when request-responses are running.|
|TOR_CSMGVT_REQ_200|Unknown||x|Not checked on Windows yet.|
|TOR_CSMGVT_REQ_210|Unknown||x|Not checked on Windows yet.|
|TOR_CSMGVT_REQ_220|Unknown||x|Not checked on Windows yet.|
|TOR_CSMGVT_REQ_230|Unknown||x|Not checked on Windows yet.|
|TOR_CSMGVT_REQ_240|Unknown||x|Not checked on Windows yet.|
|TOR_CSMGVT_REQ_250|Unknown||x|Not checked on Windows yet.|
|TOR_CSMGVT_REQ_260|Unknown||x|Not checked on Windows yet.|
|TOR_CSMGVT_REQ_270|Unknown||x|Not checked on Windows yet.|
|TOR_CSMGVT_REQ_350|Partially covered|x|x|Compilation only tested on x86 architecture.|
|TOR_CSMGVT_REQ_370|Partially covered||x|Profiling mode can be run depending of the Visual Studio version. Coverage mode is not available.|
|TOR_CSMGVT_PER_010|Partially covered|x|x|Output generation is done in less than 1 second on our examples.|
|TOR_CSMGVT_PER_020|Partially covered|x|x|Output generation with less than 2 Gbytes of RAM is not proved.|

### Possible problems

NA

### Known errors

NA

## Delivery

Via GitHub (see ECOA Website for more informations).

## Glossary

* CSM: Connected System Model
* CSMGVT: Connected System Model Generation and Verification Tool
* ECOA: European Component Oriented Architecture, the standard used to design components inside a system
* NA: Not Applicable
* RAM: Random Access Memory
* TOR: Tool Operational Requirements
* TORTC: Test Cases of TOR
* VDD: Version Description Document
