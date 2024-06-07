import os
import inspect
from typing import Any, Dict, List, Optional, Tuple, Set, get_type_hints
from runpy import run_path
import docstring_parser

class DocsGen:
    def __init__(self, lib_name: str, directory_path: str) -> None:
        self.directory_path = directory_path
        self.lib_name = lib_name
        self.output_file = f'{lib_name}_documentation.md'
        self.modules = self.__load_modules()
        self.ignored_classes = {'Any'}

    def __load_modules(self) -> Dict[str, Any]:
        modules = {}
        for root, _, files in os.walk(self.directory_path):
            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    relative_path = os.path.relpath(root, self.directory_path)
                    module_name_parts = relative_path.split(os.sep)
                    module_name_parts.append(os.path.splitext(file)[0])
                    module_name = '.'.join(filter(None, module_name_parts))
                    file_path = os.path.join(root, file)
                    try:
                        modules[module_name] = run_path(file_path)
                    except Exception as e:
                        print(f"Could not load module {module_name}: {e}")
        return modules

    @staticmethod
    def __clean_docstring(doc: str) -> str:
        return doc.split("\n")[0].strip() if doc else ""

    @staticmethod
    def __extract_arguments(method) -> str:
        docstring = inspect.getdoc(method)
        parsed_docstring = docstring_parser.parse(docstring)
        params = {param.arg_name: param.description for param in parsed_docstring.params}

        signature = inspect.signature(method)
        args = []
        for name, param in signature.parameters.items():
            if name == 'self':
                continue
            param_type = param.annotation if param.annotation != inspect.Parameter.empty else type(param.default).__name__
            param_desc = params.get(f"{name}", "")
            param_str = f"{name}: {param_type.__name__}" if isinstance(param_type, type) else f"{name}: {param_type}"
            args.append(f"{param_str} {param_desc}")
        return "\n".join(args) if args else "This function has no arguments."

    @staticmethod
    def __analyze_return_type(return_type) -> str:
        if hasattr(return_type, '__origin__'):
            if return_type.__origin__ in {list, List, dict, Dict, tuple, Tuple, set, Set, Optional}:
                inner_type = ", ".join(DocsGen.__analyze_return_type(arg) for arg in return_type.__args__)
                return f"{return_type.__origin__.__name__}[{inner_type}]"
        return return_type.__name__ if isinstance(return_type, type) else str(return_type)

    @staticmethod
    def __format_return_value(value, indent=0) -> str:
        indent_str = ' ' * indent
        if isinstance(value, (dict, list, tuple, set)):
            items = ",\n".join(f"{indent_str}    {DocsGen.__format_return_value(v, indent + 4)}" for v in value)
            return f"{type(value).__name__}[\n{items}\n{indent_str}]"
        return type(value).__name__

    def __get_return_type_hints(self, method) -> str:
        try:
            hints = get_type_hints(method)
            return_type = hints.get('return', 'No return type specified')
            if return_type != 'No return type specified':
                return self.__analyze_return_type(return_type)
            else:
                return 'No return type specified'
        except Exception as e:
            return f"Could not analyze return type: {e}"

    def __extract_example(self, class_name: str, method_name: str, init_args: List[str], method_args: List[str]) -> str:
        try:
            init_args_str = ", ".join(init_args)
            method_args_str = ", ".join(method_args)
            if method_name == '__init__':
                return f"{class_name.lower()} = {class_name}({init_args_str})"
            else:
                return f"{class_name.lower()} = {class_name}({init_args_str})\n{class_name.lower()}.{method_name}({method_args_str})"
        except Exception as e:
            return f"Could not generate example usage: {e}"

    def write_documentation(self) -> None:
        with open(self.output_file, "w") as f:
            f.write("# Documentation\n\n")
            f.write(f"## Example to load the library\n\n```python\nfrom {self.lib_name} import *\n```\n\n")

        for module_name, module in self.modules.items():
            for obj_name, obj in module.items():
                if inspect.isclass(obj) and obj_name not in self.ignored_classes:
                    self.__append_to_file(f"\n## `{obj_name}` (class)\n---\n")
                    init_args = []
                    if hasattr(obj, '__init__'):
                        init_method = obj.__init__
                        init_args = [param for param in inspect.signature(init_method).parameters if param != 'self']
                        args = self.__extract_arguments(init_method)
                        example = self.__extract_example(obj_name, '__init__', init_args, [])
                        self.__append_to_file(f"\n### `{obj_name}.__init__` (method)\n"
                                            f"**Description**: Constructor for {obj_name}\n\n"
                                            f"**Arguments**:\n```txt\n{args}\n```\n\n"
                                            f"**Example for use**:\n```python\n{example}\n```\n\n---\n")
                    for name, method in inspect.getmembers(obj, inspect.isfunction):
                        if name.startswith("_"):
                            continue
                        docstring = inspect.getdoc(method)
                        parsed_docstring = docstring_parser.parse(docstring)
                        description = parsed_docstring.short_description if parsed_docstring.short_description else "No method description provided."
                        args = self.__extract_arguments(method)
                        return_type = self.__get_return_type_hints(method)
                        return_desc = parsed_docstring.returns.description if parsed_docstring.returns else ""
                        sample_value = self.__get_sample_return_value(method)
                        return_value_str = self.__format_return_value(sample_value) if sample_value is not None else return_type
                        method_args = [param for param in inspect.signature(method).parameters if param != 'self']
                        example = self.__extract_example(obj_name, name, init_args, method_args)
                        self.__append_to_file(f"\n### `{obj_name}.{name}` (method)\n"
                                            f"**Description**: {description}\n\n"
                                            f"**Arguments**:\n```txt\n{args}\n```\n\n"
                                            f"**Returns**:\n```txt\n{return_value_str}\n```\n**Returns Description**:\n{return_desc}\n\n"
                                            f"**Example for use**:\n```python\n{example}\n```\n\n---\n")

    def __append_to_file(self, content: str) -> None:
        with open(self.output_file, "a") as f:
            f.write(content)

    @staticmethod
    def __get_sample_return_value(method) -> Any:
        try:
            instance = method.__self__ if hasattr(method, '__self__') else None
            if instance:
                args = [instance] + [1] * (len(inspect.signature(method).parameters) - 1)
            else:
                args = [1] * len(inspect.signature(method).parameters)
            sample_value = method(*args)
            return sample_value
        except Exception as e:
            print(f"Could not get sample return value: {e}")
            return None
