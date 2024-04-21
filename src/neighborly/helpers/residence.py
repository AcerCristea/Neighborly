"""Helper functions for managing residences and residents.

"""

from __future__ import annotations

from neighborly.components.location import Location
from neighborly.components.residence import ResidentialBuilding, ResidentialUnit, Vacant
from neighborly.components.traits import Traits
from neighborly.defs.base_types import ResidenceDef
from neighborly.ecs import GameObject, World
from neighborly.libraries import ResidenceLibrary


def create_residence(
    world: World,
    definition_id: str,
) -> GameObject:
    """Create a new residence instance."""
    library = world.resource_manager.get_resource(ResidenceLibrary)

    residence_def = library.get_definition(definition_id)

    residence = world.gameobject_manager.spawn_gameobject(
        components=residence_def.components
    )
    residence.metadata["definition_id"] = definition_id

    world = residence.world
    building = residence.get_component(ResidentialBuilding)

    for _ in range(residence_def.residential_units):
        residential_unit = world.gameobject_manager.spawn_gameobject(
            name="ResidentialUnit"
        )
        residential_unit.add_component(Traits(residential_unit))
        residence.add_child(residential_unit)
        residential_unit.add_component(
            ResidentialUnit(residential_unit, building=residence)
        )
        residential_unit.add_component(Location(residential_unit, is_private=True))
        building.add_residential_unit(residential_unit)
        residential_unit.add_component(Vacant(residential_unit))

    return residence


def register_residence_def(world: World, definition: ResidenceDef) -> None:
    """Add a new residence definition for the ResidenceLibrary.

    Parameters
    ----------
    world
        The world instance containing the residence library.
    definition
        The definition to add.
    """
    world.resource_manager.get_resource(ResidenceLibrary).add_definition(definition)
    world.resource_manager.get_resource(ResidenceLibrary).add_definition(definition)
