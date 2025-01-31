from pytoml11 import Array, Table

from bron.logic.merge import item_is_nosync


def _erase_tables(base: Table, remove: Table) -> None:
    if item_is_nosync(base):
        return

    for k, v in remove.value.items():
        if k not in base:
            continue

        if item_is_nosync(base[k]):
            continue

        if base[k] == v:
            del base[k]
            continue

        if isinstance(base[k], Table) and isinstance(v, Table):
            _erase_tables(base[k], v)
        elif isinstance(base[k], Array) and isinstance(v, Array):
            _erase_arrays(base[k], v)


def _erase_arrays(base: Array, remove: Array) -> None:
    if item_is_nosync(base):
        return

    for i, value in reversed(list(enumerate(base.value))):
        if item_is_nosync(value):
            continue
        if value in remove:
            del base[i]


def erase(base: Table | Array, remove: Table | Array) -> None:
    if isinstance(base, Table):
        if not isinstance(remove, Table):
            return

        _erase_tables(base, remove)
    elif isinstance(base, Array):
        if not isinstance(remove, Array):
            return

        _erase_arrays(base, remove)
