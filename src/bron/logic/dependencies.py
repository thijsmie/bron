from packaging.markers import Marker
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

_Key = tuple[str, Marker | None]


def _get_key(requirement: Requirement) -> _Key:
    return (canonicalize_name(requirement.name), requirement.marker)


def _add_requirement(dependencies: dict[_Key, Requirement], key: _Key, requirement: Requirement) -> None:
    if key not in dependencies:
        # Add new requirement
        dependencies[key] = requirement
    else:
        # Replace existing requirement
        existing = dependencies[key]

        # If source has no specifier but base has one, keep the base specifier
        specifier = requirement.specifier or existing.specifier

        # Create a new Requirement object with the merged specifier
        dependencies[key] = Requirement(
            f"{requirement.name}{specifier} {f'; {requirement.marker}' if requirement.marker else ''}".strip()
        )


def merge_dependencies(
    base: list[Requirement], update: list[Requirement], nosync: list[Requirement]
) -> list[Requirement]:
    # Dictionary to hold merged requirements
    dependencies: dict[_Key, Requirement] = {_get_key(req): req for req in base}
    nosync_keys = {_get_key(req) for req in nosync}

    for req in update:
        key = _get_key(req)

        if key in nosync_keys:
            continue
        if req.url:
            # Url requirements are not merged but get priority
            dependencies[key] = req
        else:
            _add_requirement(dependencies, key, req)

    return sorted(dependencies.values(), key=lambda req: req.name)
