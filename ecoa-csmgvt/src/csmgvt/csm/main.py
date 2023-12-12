# -*- coding: utf-8 -*-
# Copyright (c) 2023 Dassault Aviation
# SPDX-License-Identifier: MIT

"""Main generation class.
"""

# Standard library imports
import logging
import os
from typing import TextIO

# Internal library imports
from ecoa_toolset.generators.common import Common
from ecoa_toolset.generators.helpers.platform_hook import PlatformHook, PlatformHookHelper

logger = logging.getLogger(__name__)


class MainGenerator:
    """The main generator."""

    _ecoa_model = None
    _path: str = None
    _module_helper = None
    _platform_hook_helper = None
    _modules = []
    _hooks = []

    @classmethod
    def _generate_includes(cls, f: TextIO) -> None:
        # Standard includes
        f.write("/* Standards libraries */" + Common.LINE_BREAK[:1])
        libraries = ["stdio", "stdlib", "string"]
        for library in libraries:
            f.write("#include <" + library + ".h" + ">" + Common.LINE_BREAK[:1])
        f.write(Common.LINE_BREAK[:1])
        # Module includes
        f.write("/* Modules libraries */" + Common.LINE_BREAK[:1])
        for module in cls._ecoa_model.module_impls.values():
            f.write('#include "' + module.name + ".")
            if "C" == module.language:
                f.write("h")
            elif "C++" == module.language:
                f.write("hpp")
            f.write('"' + Common.LINE_BREAK[:1])
        f.write(Common.LINE_BREAK[:1])

    @classmethod
    def _generate_c_lang_modules_instanciation(
        cls,
        f: TextIO,
        module_impl_name: str,
        module_inst_name: str,
        component_name: str,
    ) -> None:
        f.write(
            "extern"
            + Common.SPACE_INDENTATION[:1]
            + module_impl_name
            + "__context"
            + Common.SPACE_INDENTATION[:1]
            + module_inst_name
            + "_"
            + component_name
            + "_Context;"
            + Common.LINE_BREAK[:1]
        )

    @classmethod
    def _generate_cpp_lang_modules_instanciation(
        cls,
        f: TextIO,
        module_impl_name: str,
        module_inst_name: str,
        component_name: str,
    ) -> None:
        f.write(
            "extern"
            + Common.SPACE_INDENTATION[:1]
            + module_impl_name
            + "::Module"
            + Common.SPACE_INDENTATION[:1]
            + module_inst_name
            + "_"
            + component_name
            + "_Module;"
            + Common.LINE_BREAK[:1]
        )

    @classmethod
    def _generate_modules_instanciation(cls, f: TextIO) -> None:
        for hook in cls._hooks:
            for component_name in hook.component_names:
                if "c" == hook.language.lower():
                    cls._generate_c_lang_modules_instanciation(
                        f,
                        hook.module_impl_name,
                        hook.module_inst_name,
                        component_name,
                    )
                elif "c++" == hook.language.lower():
                    cls._generate_cpp_lang_modules_instanciation(
                        f,
                        hook.module_impl_name,
                        hook.module_inst_name,
                        component_name,
                    )
        f.write(Common.LINE_BREAK[:1])

    @classmethod
    def _generate_trigger_event_received_call(
        cls, module_impl, module_inst_name, component_name, operation_name
    ) -> str:
        generation = ""
        if "c++" == module_impl.language.lower():
            generation += (
                Common.SPACE_INDENTATION[:4]
                + module_inst_name
                + "_"
                + component_name
                + "_Module."
                + operation_name
                + "__received();"
                + Common.LINE_BREAK[:1]
            )
        elif "c" == module_impl.language.lower():
            generation += (
                Common.SPACE_INDENTATION[:4]
                + module_impl.name
                + "__"
                + operation_name
                + "__received(&"
                + module_inst_name
                + "_"
                + component_name
                + "_Context);"
                + Common.LINE_BREAK[:1]
            )
        return generation

    @classmethod
    def _generate_trigger_event_received_calls(cls, trigger) -> str:
        generation = ""
        for key_receiver, receiver in trigger.receivers.items():
            module_inst_name, component_name = tuple(key_receiver.split(":"))
            module_inst = cls._ecoa_model.module_insts.get(receiver.component_impl_name + ":" + module_inst_name)
            module_impl = cls._ecoa_model.module_impls.get(
                receiver.component_impl_name + ":" + module_inst.implementation_name
            )
            generation += cls._generate_trigger_event_received_call(
                module_impl, module_inst_name, component_name, receiver.name
            )
        return generation

    @classmethod
    def _generate_main_loop(cls, f: TextIO):
        f.write(
            Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "/* Call the entry points linked to the activation of the concerned modules */"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "while (1)"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "{"
            + Common.LINE_BREAK[:2]
            + Common.SPACE_INDENTATION[:4]
        )
        triggers = [trigger for v in cls._ecoa_model.triggers.values() for trigger in v]
        if triggers:
            f.write("/* Activating the trigger entry points. */" + Common.LINE_BREAK[:1])
            for trigger in triggers:
                f.write(cls._generate_trigger_event_received_calls(trigger))
        f.write(
            Common.LINE_BREAK[:2]
            + Common.SPACE_INDENTATION[:4]
            + "/* Insert run logic here. */"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:4]
            + "/* Insert report logic here. */"
            + Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "}"
            + Common.LINE_BREAK[:2]
        )

    @classmethod
    def _generate_initialize_modules(cls, f: TextIO, hook: PlatformHook, component_name: str) -> None:
        if "c++" == hook.language.lower():
            f.write(
                Common.SPACE_INDENTATION[:2]
                + hook.module_inst_name
                + "_"
                + component_name
                + "_Module.INITIALIZE__received();"
                + Common.LINE_BREAK[:1]
            )
        elif "c" == hook.language.lower():
            f.write(
                Common.SPACE_INDENTATION[:2]
                + hook.module_impl_name
                + "__INITIALIZE__received(&"
                + hook.module_inst_name
                + "_"
                + component_name
                + "_Context);"
                + Common.LINE_BREAK[:1]
            )

    @classmethod
    def _generate_start_modules(cls, f: TextIO, hook: PlatformHook, component_name: str) -> None:
        if "c++" == hook.language.lower():
            f.write(
                Common.SPACE_INDENTATION[:2]
                + hook.module_inst_name
                + "_"
                + component_name
                + "_Module.START__received();"
                + Common.LINE_BREAK[:1]
            )
        elif "c" == hook.language.lower():
            f.write(
                Common.SPACE_INDENTATION[:2]
                + hook.module_impl_name
                + "__START__received(&"
                + hook.module_inst_name
                + "_"
                + component_name
                + "_Context);"
                + Common.LINE_BREAK[:1]
            )

    @classmethod
    def _generate_initialize_start_modules(cls, f: TextIO) -> None:
        # Initialize lifecycle function
        f.write(Common.SPACE_INDENTATION[:2] + "/* Initializing the ECOA modules. */" + Common.LINE_BREAK[:1])
        for hook in cls._hooks:
            for component_name in hook.component_names:
                cls._generate_initialize_modules(f, hook, component_name)
        # Insert arguments logic
        f.write(
            Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "// Insert arguments logic here."
            + Common.LINE_BREAK[:2]
        )
        # Start lifecycle function
        f.write(Common.SPACE_INDENTATION[:2] + "// Starting the ECOA modules." + Common.LINE_BREAK[:1])
        for hook in cls._hooks:
            for component_name in hook.component_names:
                cls._generate_start_modules(f, hook, component_name)

    @classmethod
    def _generate_stop_modules(cls, f: TextIO, hook: PlatformHook, component_name: str) -> None:
        if "c++" == hook.language.lower():
            f.write(
                Common.SPACE_INDENTATION[:2]
                + hook.module_inst_name
                + "_"
                + component_name
                + "_Module.STOP__received();"
                + Common.LINE_BREAK[:1]
            )
        elif "c" == hook.language.lower():
            f.write(
                Common.SPACE_INDENTATION[:2]
                + hook.module_impl_name
                + "__STOP__received(&"
                + hook.module_inst_name
                + "_"
                + component_name
                + "_Context);"
                + Common.LINE_BREAK[:1]
            )

    @classmethod
    def _generate_shudown_modules(cls, f: TextIO, hook: PlatformHook, component_name: str) -> None:
        if "c++" == hook.language.lower():
            f.write(
                Common.SPACE_INDENTATION[:2]
                + hook.module_inst_name
                + "_"
                + component_name
                + "_Module.SHUTDOWN__received();"
                + Common.LINE_BREAK[:1]
            )
        elif "c" == hook.language.lower():
            f.write(
                Common.SPACE_INDENTATION[:2]
                + hook.module_impl_name
                + "__SHUTDOWN__received(&"
                + hook.module_inst_name
                + "_"
                + component_name
                + "_Context);"
                + Common.LINE_BREAK[:1]
            )

    @classmethod
    def _generate_stop_shutdown_modules(cls, f: TextIO) -> None:
        # Stop lifecycle function
        f.write(Common.SPACE_INDENTATION[:2] + "// Stopping the ECOA modules." + Common.LINE_BREAK[:1])
        for hook in cls._hooks:
            for component_name in hook.component_names:
                cls._generate_stop_modules(f, hook, component_name)
        # Shutdown lifecycle function
        f.write(
            Common.LINE_BREAK[:1]
            + Common.SPACE_INDENTATION[:2]
            + "// Shutting down the ECOA modules."
            + Common.LINE_BREAK[:1]
        )
        for hook in cls._hooks:
            for component_name in hook.component_names:
                cls._generate_shudown_modules(f, hook, component_name)

    @classmethod
    def generate(cls, ecoa_model, path: str, force: bool) -> None:
        """Generates the following file:
            - <output>/src/main.cpp.

        Args:
            ecoa_model : The ECOA model.
            path (str) : The generation directory path.
            force (bool) : True if the file can be overwritten, False otherwise.
        """
        cls._ecoa_model = ecoa_model
        cls._path = path
        cls._platform_hook_helper = PlatformHookHelper(cls._ecoa_model)
        cls._hooks = cls._platform_hook_helper.find_all().values()
        file_name = "main.cpp"
        file_path = os.path.join(cls._path, "src", file_name)
        if os.path.exists(file_path) and force:
            logger.debug("%s already exists, forcing, overwriting it...", file_path)
        with open(file_path, "w") as f:
            # Header comment and standards includes
            f.write("/* " + file_name + " */" + Common.LINE_BREAK[:2])
            cls._generate_includes(f)
            # Global variables declaration
            cls._generate_modules_instanciation(f)
            visited = False
            if cls._ecoa_model.module_impls:
                f.write("extern void cm_initialize(void);" + Common.LINE_BREAK[:1])
                visited = True
            if cls._ecoa_model.pinfos:
                f.write("extern void cm_shutdown(void);" + Common.LINE_BREAK[:1])
                visited = True
            f.write(Common.LINE_BREAK[:visited])
            # Start of main function
            f.write("int main(void)" + Common.LINE_BREAK[:1] + "{" + Common.LINE_BREAK[:1])
            if cls._ecoa_model.module_impls:
                f.write(Common.SPACE_INDENTATION[:2] + "cm_initialize();" + Common.LINE_BREAK[:2])
            # Initialize and start modules
            cls._generate_initialize_start_modules(f)
            # Main logic
            cls._generate_main_loop(f)
            # stop and shutdown modules
            cls._generate_stop_shutdown_modules(f)
            if cls._ecoa_model.pinfos:
                f.write(Common.LINE_BREAK[:1] + Common.SPACE_INDENTATION[:2] + "cm_shutdown();" + Common.LINE_BREAK[:2])
            # End of main function
            f.write(Common.SPACE_INDENTATION[:2] + "return 0;" + Common.LINE_BREAK[:1] + "}" + Common.LINE_BREAK[:1])
        logger.debug("%s generated", file_path)
