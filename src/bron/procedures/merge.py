from packaging.requirements import Requirement
from pytoml11 import Array, Item, String, Table

from bron.procedures.dependencies import merge_dependencies


class MergeError(Exception):
    pass


def item_is_nosync(item: Item) -> bool:
    return any("nosync" in comment for comment in item.comments)


def _merge_regular_tables(base: Table, update: Table, path: tuple[str, ...], merge_arrays: bool) -> None:
    for k, v in update.value.items():
        if k in base and item_is_nosync(base[k]):
            continue

        if k in base and isinstance(base[k], Table) and isinstance(v, Table):
            _merge(base[k], v, (*path, k), merge_arrays)
        else:
            base[k] = v.copy()


def _merge_regular_arrays(base: Array, update: Array, merge_arrays: bool) -> None:
    if merge_arrays:
        for item in update.value:
            if item not in base:
                base.append(item.copy())
    else:
        for item in base.value:
            if item_is_nosync(item):
                update.insert(0, item.copy())

        base.clear()

        for item in update.value:
            base.append(item.copy())


def _merge_regular(base: Table | Array, update: Table | Array, path: tuple[str, ...], merge_arrays: bool) -> None:
    if isinstance(base, Table):
        if not isinstance(update, Table):
            raise MergeError(f"Cannot update {'.'.join(path)} with a non-Table item.")

        _merge_regular_tables(base, update, path, merge_arrays)
    elif isinstance(base, Array):
        if not isinstance(update, Array):
            raise MergeError(f"Cannot update {'.'.join(path)} with a non-Array item.")

        _merge_regular_arrays(base, update, merge_arrays)


def _merge_dependency_arrays(existing: Array, update: Array, path: tuple[str, ...]) -> None:
    nosync: list[Item] = []

    # pre-condition validity check
    for item in existing.value:
        if not isinstance(item, String):
            subpath = (*path, existing.value.index(item))
            raise MergeError(f"Expected a String, got {type(item)} at {'.'.join(subpath)}")
        if item_is_nosync(item):
            nosync.append(item)

    for item in update.value:
        if not isinstance(item, String):
            subpath = (*path, existing.value.index(item))
            raise MergeError(f"Expected a String, got {type(item)} at {'.'.join(subpath)}")

    existing_reqs = [Requirement(dep.value) for dep in existing.value]
    update_reqs = [Requirement(dep.value) for dep in update.value]
    nosync_reqs = [Requirement(dep.value) for dep in nosync]

    merged_reqs = merge_dependencies(existing_reqs, update_reqs, nosync_reqs)

    existing.clear()

    for req in merged_reqs:
        if req in nosync_reqs:
            existing.append(String(str(req), comments=[" nosync"]))
        else:
            existing.append(String(str(req)))


def _merge_special_cases(base: Item, update: Item, path: tuple[str, ...]) -> bool:
    if path in {
        ("project", "dependencies"),
        ("tool", "uv", "constraint-dependencies"),
        ("tool", "uv", "override-dependencies"),
    }:
        _merge_dependency_arrays(base, update, path)
        return True
    elif path in {("project", "optional-dependencies"), ("dependency-groups",)}:
        for k, v in update.value.items():
            if k in base:
                _merge_dependency_arrays(base[k], v, (*path, k))
            else:
                base[k] = v.copy()
        return True
    elif path in {("tool", "bron")}:
        # Ignore bron tool table
        return True

    return False


def _merge(base: Item, update: Item, path: tuple[str, ...], merge_arrays: bool) -> None:
    if _merge_special_cases(base, update, path):
        return
    _merge_regular(base, update, path, merge_arrays)


def merge_pyproject(base: Table, update: Table, merge_arrays: bool = False) -> None:
    _merge(base, update, (), merge_arrays)
