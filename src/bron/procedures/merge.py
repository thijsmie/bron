from typing import overload

from packaging.requirements import Requirement
from pytoml11 import Array, Item, String, Table

from bron.procedures.dependencies import merge_dependencies


def item_is_nosync(item: Item) -> bool:
    return any("nosync" in comment for comment in item.comments)


@overload
def _merge_regular(base: Table, update: Table, path: tuple[str, ...]) -> None: ...
@overload
def _merge_regular(base: Array, update: Array, path: tuple[str, ...]) -> None: ... # type: ignore


def _merge_regular(base: Table | Array, update: Table | Array, path: tuple[str, ...]) -> None:
    if isinstance(base, Table):
        assert isinstance(update, Table)

        for k, v in update.value.items():
            if k in base and item_is_nosync(base[k]):
                continue

            if (k in base and isinstance(base[k], Table) and isinstance(v, Table)) or (
                k in base and isinstance(base[k], Array) and isinstance(v, Array)
            ):
                _merge(base[k], v, (*path, k))
            else:
                base[k] = v.copy()

        return

    assert isinstance(base, Array)
    assert isinstance(update, Array)

    dedup_set: set[str | int | bool | float | None] = set()  # Not all entities can be compared
    for item in base.value:
        if isinstance(item.value, str | int | bool | float):
            dedup_set.add(item.value)

    for item in update.value:
        if isinstance(item.value, str | int | bool | float) and item.value not in dedup_set:
            base.append(item.copy())
        else:
            base.append(item.copy())


def _merge_dependency_arrays(existing: Array, update: Array) -> None:
    nosync: list[Item] = []

    # pre-condition validity check
    for item in existing.value:
        if not isinstance(item, String):
            raise ValueError(f"Expected a String, got {type(item)}")
        if item_is_nosync(item):
            nosync.append(item)

    for item in update.value:
        if not isinstance(item, String):
            raise ValueError(f"Expected a String, got {type(item)}")

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


def _merge_depencency_cases(base: Item, update: Item, path: tuple[str, ...]) -> bool:
    if path in {
        ("project", "dependencies"),
        ("tool", "uv", "constraint-dependencies"),
        ("tool", "uv", "override-dependencies"),
    }:
        _merge_dependency_arrays(base, update)
        return True
    elif path in {("project", "optional-dependencies"), ("dependency-groups",)}:
        for k, v in update.value.items():
            if k in base:
                _merge_dependency_arrays(base[k], v)
            else:
                base[k] = v.copy()
        return True

    return False


def _merge(base: Item, update: Item, path: tuple[str, ...]) -> None:
    if _merge_depencency_cases(base, update, path):
        return
    _merge_regular(base, update, path)


def merge_pyproject(base: Table, update: Table) -> None:
    _merge(base, update, ())
