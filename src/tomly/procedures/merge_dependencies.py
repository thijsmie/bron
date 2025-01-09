from packaging.requirements import Requirement
from packaging.markers import Marker
from packaging.utils import canonicalize_name


def _get_key(requirement: Requirement) -> tuple[str, Marker | None]:
    return (
        canonicalize_name(requirement.name),
        requirement.marker
    )


def _add_requirement(dependencies: dict[tuple[str, Marker | None], Requirement], requirement: Requirement) -> None:
    key = _get_key(requirement)
    if key not in dependencies:
        # Add new requirement
        dependencies[key] = requirement
    else:
        # Merge with existing requirement
        existing = dependencies[key]
        if existing.specifier and requirement.specifier:
            combined_specifier = existing.specifier & requirement.specifier
        else:
            combined_specifier = existing.specifier or requirement.specifier
        
        # Create a new Requirement object with the merged specifier
        dependencies[key] = Requirement(
            f"{requirement.name}{combined_specifier} {f'; {requirement.marker}' if requirement.marker else ''}".strip()
        )


def merge_dependencies(base: list[Requirement], update: list[Requirement]) -> list[Requirement]:
    # Dictionary to hold merged requirements
    dependencies: dict[tuple[str, Marker | None], Requirement] = {}

    for req_list in [base, update]:
        for req in req_list:
            if req.url:
                # Url requirements are not merged but get priority
                dependencies[_get_key(req)] = req
            else:
                _add_requirement(dependencies, req)

    return sorted(dependencies.values(), key=lambda req: req.name)
