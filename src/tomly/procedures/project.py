from pytoml11 import Item, Table, Array, String


_PROJECT_SORT_ORDER = [
    "name",
    "version",
    "description",
    "authors",
    "maintainers",
    "documentation",
    "homepage",
    "repository",
    "repository",
    "license",
    "keywords",
    "categories",
    "readme",
    "readme-file",
    "readme-url",
    "license-file",
    "license-url",
    "license-text",
    "license-file",
    "license-url",
    "license-text",
    "requires-python",
    "scripts",
]

def _project_sort_key(key: str, value: Item) -> int:
    if key in _PROJECT_SORT_ORDER:
        v = _PROJECT_SORT_ORDER.index(key)
    else:
        v = len(_PROJECT_SORT_ORDER) + 1
    print(key, value, v)
    return v


def format_project(project: Table) -> Table:
    as_dict = {
        k: v.copy() for k, v in sorted(
            project.value.items(),
            key=lambda kv: _project_sort_key(kv[0], kv[1])
        )
    }

    # Sort dependencies
    if "dependencies" in as_dict:
        as_dict["dependencies"] = Array(
            sorted(
                (d.copy() for d in as_dict["dependencies"]),
                key=lambda d: d.value
            )
        )

    if "optional-dependencies" in as_dict and isinstance(as_dict["optional-dependencies"], Table):
        optional_dependencies = {}
        for k,v in sorted(as_dict["optional-dependencies"].value.items()):
            optional_dependencies[k] = Array(
                sorted(
                    (d.copy() for d in v),
                    key=lambda d: d.value
                )
            )
        as_dict["optional-dependencies"] = Table(optional_dependencies)

    return Table(as_dict)
