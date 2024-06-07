# Documentation

- DocsGen is a Python library that generates documentation for Python libraries.

- Library Features:
    - Generates documentation in markdown format.
    - Simple to use.
    - Automatic documentation generation.
    - Supports creating examples for usage.

## Example to load the library

```python
from docsgen import *
```


## `DocsGen` (class)
---

### `DocsGen.__init__` (method)
**Description**: Constructor for DocsGen.

**Arguments**:
```txt
lib_name: str 
directory_path: str 
```

**Example for use**:
```python
docsgen = DocsGen(lib_name, directory_path)
```

---

### `DocsGen.write_documentation` (method)
**Description**: Method to write the documentation.

**Arguments**:
```txt
This function has no arguments.
```

**Returns**:
```txt
NoneType
```
**Returns Description**: Returns nothing.

**Example for use**:
```python
docsgen = DocsGen(lib_name, directory_path)
docsgen.write_documentation()
```

---

### Command Line Interface (CLI)
To use the library's CLI, execute the following command:

```
docsgen lib_name, dir
```

This command generates documentation for the specified library (`lib_name`) located in the specified directory (`dir`).