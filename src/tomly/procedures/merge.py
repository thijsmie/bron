from pytoml11 import Item, Table, Array, String
from packaging.requirements import Requirement
from tomly.procedures.merge_dependencies import merge_dependencies
from tomly.procedures.project import format_project


def item_is_nosync(item: Item) -> bool:
    for comment in item.comments:
        if "nosync" in comment:
            return True
    return False


def merge(left: Item, right: Item) -> Item:
    if isinstance(left, Table) and isinstance(right, Table):
        leftish = {k: v.copy() for k,v in left.value.items()}
        rightish = {k: v.copy() for k,v in right.value.items()}

        for k, v in leftish.items():
            if item_is_nosync(v):
                continue

            if k in rightish:
                leftish[k] = merge(v, rightish.pop(k))

        leftish.update(rightish)
        return Table({k: v for k, v in sorted(leftish.items())})

    if isinstance(left, Array) and isinstance(right, Array):
        new_array = left.copy()
        dedup_set: set[str | int | bool | float | None] = set()  # Not all entities can be compared
        for item in left.value:
            if isinstance(item.value, (str, int, bool, float)):
                dedup_set.add(item.value)

        for item in right.value:
            if isinstance(item.value, (str, int, bool, float)):
                if item.value not in dedup_set:
                    new_array.value.append(item)
                    dedup_set.add(item.value)
            else:
                new_array.value.append(item)

        return new_array

    return right.copy()


def _merge_dependency_arrays(existing: Array, update: Array) -> Array:
    # pre-condition validity check
    for item in existing.value:
        if not isinstance(item, String):
            raise ValueError(f"Expected a String, got {type(item)}")
    for item in update.value:
        if not isinstance(item, String):
            raise ValueError(f"Expected a String, got {type(item)}")
        
    existing_reqs = [Requirement(dep.value) for dep in existing.value]
    update_reqs = [Requirement(dep.value) for dep in update.value]

    merged_reqs = merge_dependencies(existing_reqs, update_reqs)

    return Array([String(str(req)) for req in merged_reqs])


def _merge_pyproject_project(existing: Table, update: Table) -> Table:
    merged = {k: v.copy() for k, v in existing.value.items()}

    for k, v in update.value.items():
        if k in merged and item_is_nosync(merged[k]):
            continue

        if k in merged:
            if k == "dependencies":
                merged[k] = _merge_dependency_arrays(merged[k], v)
            elif k == "optional-dependencies":
                for k2, v2 in v.value.items():
                    if k2 in merged[k]:
                        if item_is_nosync(merged[k][k2]):
                            continue

                        merged[k][k2] = _merge_dependency_arrays(merged[k][k2], v2)
                    else:
                        merged[k][k2] = v2.copy()
            else:
                merged[k] = merge(merged[k], v)
        else:
            merged[k] = v.copy()

    return Table(merged)


def merge_pyproject(existing: Table, update: Table) -> Table:
    if "project" in existing.value and "project" in update.value:
        project = _merge_pyproject_project(existing.value["project"], update.value["project"])
        del existing.value["project"]
        del update.value["project"]
    elif "project" in update.value:
        project = update.value["project"]
        del update.value["project"]
    elif "project" in existing.value:
        project = existing.value["project"]
        del existing.value["project"]
    else:
        project = Table({})

    merged = {
        "project": format_project(project),
    }

    doc = merge(existing, update)
    if isinstance(doc, Table):
        for key, value in sorted(doc.value.items()):
            merged[key] = value.copy()
            
    return Table(merged)
