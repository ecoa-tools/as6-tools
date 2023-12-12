# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change.

Please note we have a [Code of Conduct](./CODE_OF_CONDUCT.md), please follow it in all your interactions with the project.

## Important resources

* [docs](./docs)

## Setting up the development environment

### Prerequisites

* Python 3.8 or higher
* Pip 21.3 or higher
* Setuptools 64.0 or higher
* Unix or Windows 10 environment
* GCC
* Makefile
* CMake
* MSVC
* Visual Studio (min 22 2017, for Windows)

### Installation

1. Clone the repo
   ```sh
   git clone ssh://git@bitbucket.dassault-aviation.pro:7999/soda/ecoa-tools.git
   ```

2. Create a virtual environment

   Linux
   ```sh
   python3 -m venv .venv
   ```

   Windows
   ```cmd
   py -3 -m venv venv
   ```

3. Activate the virtual environment

   Linux
   ```sh
   source .venv/bin/activate
   ```

   Windows
   ```cmd
   venv/Scripts/activate.bat
   ```

4. Install the development dependences

   ```sh
   pip install -r requirements-dev.txt
   ```

   If you're using a hosted repository, you can either:
   * Use the option: `-i, --index-url <url>`
   * Create a `pip.conf` at the root of the virtual environment directory or `~/.config/pip` with the `index-url` entry
      ```
         [global]
         index-url = <url>
      ```


5. Install the package(s) you're going to work on locally

   Move to a package directory and run:

   ```sh
   pip install -e .
   ```

   with the following options: `--no-build-isolation --no-deps` in the command line or in the `pip.conf` file.

6. (optional) Install the pre-commit hook

   ```sh
   pre-commit install
   ```

## Documentation

We are using Sphinx for the documentation.

You can check it out by either reading the raw files or by building an HTML representation:

```sh
cd path/to/tool/directory/docs
sphinx-build -b html source/ build/html
```

* [ecoa-toolset/docs](./ecoa-toolset/docs) - Architecture guide, TOR-REF, ECOA norm documentation, ECOA tree
* [ecoa-csmgvt/docs](./ecoa-csmgvt/docs) - CSMGVT user guide, VDD, TORTC, TORTR
* [ecoa-mscigt/docs](./ecoa-mscigt/docs) - MSCIGT user guide, VDD, TORTC, TORTR

## Running tests

There is a `tests` directory at the root of each package where you can run requirements tests :

```sh
cd path/to/tool/directory
pytest -v
```

* [ecoa-toolset/tests](./ecoa-toolset/tests)
* [ecoa-csmgvt/tests](./ecoa-csmgvt/tests) - CSMGVT requirements tests
* [ecoa-mscigt/tests](./ecoa-mscigt/tests) - MSCIGT requirements tests

Output:

```sh
================================================================================== test session starts ==================================================================================
platform linux -- Python 3.8.3, pytest-7.2.0, pluggy-1.0.0 -- /ldisk/tmp_users/emalherb/ecoa-tools/.venv/bin/python3.8
cachedir: .pytest_cache
rootdir: /ldisk/tmp_users/emalherb/ecoa-tools/ecoa-mscigt
collected 38 items

tests/test_arguments_handling.py::test_should_exit_with_1_when_given_no_arguments - TOR_MSCIGT_TC_300 PASSED                                                                      [  2%]
tests/test_arguments_handling.py::test_should_exit_with_1_when_given_too_many_arguments - TOR_MSCIGT_TC_310 PASSED                                                                [  5%]
tests/test_arguments_handling.py::test_should_exit_with_1_when_given_invalid_arguments - TOR_MSCIGT_TC_320 PASSED                                                                 [  7%]
[...]

tests/test_template_flag.py::test_should_generate_user_templates_with_template_flag[-t] - TOR_MSCIGT_TC_040 PASSED                                                                [ 94%]
tests/test_template_flag.py::test_should_generate_user_templates_with_template_flag[--template] - TOR_MSCIGT_TC_040 PASSED                                                        [ 97%]
tests/test_template_flag.py::test_should_generate_predefined_templates_without_template_flag - TOR_MSCIGT_TC_350 PASSED                                                           [100%]

============================================================================= 38 passed in 76.66s (0:01:16) =============================================================================
```

### Writing tests

For each test, it is mandatory to add the following line and write the name of the test with "test_should_":

```python
@pytest.mark.TC("TC_ID")
def test_should_exit():
    pass
```

otherwise the test will be skipped.

## Pull Request Process

1. Run the tests

2. Run `pre-commit run --all-files`

3. Update the Sphinx documentation with details of changes to the interface.

4. Increase the version numbers in any examples files and the README.md to the new version that this
   Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).

5. You may merge the Pull Request in once you have the sign-off of two other developers, or if you
   do not have permission to do that, you may request the second reviewer to merge it for you.
