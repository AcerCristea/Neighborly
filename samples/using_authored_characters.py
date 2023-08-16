#!/usr/bin/env python3

"""
Using Authored Characters Sample
================================

This samples shows how users may inject user-specified characters into the simulation.
Normally characters are spawned into the settlement based on the spawn table.

"""

import time
from typing import Any

from neighborly import Neighborly, NeighborlyConfig, SimDateTime, System
from neighborly.components.character import (
    BaseCharacter,
    CharacterConfig,
    Female,
    GameCharacter,
)
from neighborly.components.residence import set_residence
from neighborly.data_collection import DataCollector
from neighborly.decorators import component, system
from neighborly.ecs import GameObject, TagComponent, World
from neighborly.exporter import export_to_json
from neighborly.plugins.defaults.residences import House
from neighborly.relationship import Friendship, InteractionScore, Relationships, Romance
from neighborly.statuses import Statuses

sim = Neighborly(
    NeighborlyConfig.parse_obj(
        {
            "settlement_name": "Westworld",
            "plugins": [
                "neighborly.plugins.defaults.all",
                "neighborly.plugins.talktown",
            ],
        }
    )
)


@component(sim.world)
class Robot(TagComponent):
    """Tags a character as a Robot"""

    pass


@system(sim.world)
class RelationshipReporter(System):
    def on_add(self, world: World) -> None:
        world.resource_manager.get_resource(DataCollector).create_new_table(
            "relationships",
            (
                "timestamp",
                "owner",
                "target",
                "friendship",
                "romance",
                "interaction_score",
                "statuses",
            ),
        )

    def on_update(self, world: World) -> None:
        timestamp = world.resource_manager.get_resource(SimDateTime).to_iso_str()
        data_collector = world.resource_manager.get_resource(DataCollector)
        for guid, (game_character, relationship_manager) in world.get_components(
            (GameCharacter, Relationships)
        ):
            if (
                game_character.first_name == "Delores"
                and game_character.last_name == "Abernathy"
            ):
                for target, relationship in relationship_manager.outgoing.items():
                    data_collector.add_table_row(
                        "relationships",
                        {
                            "timestamp": timestamp,
                            "owner": guid,
                            "target": target.uid,
                            "friendship": relationship.get_component(Friendship).value,
                            "romance": relationship.get_component(Romance).value,
                            "interaction_score": relationship.get_component(
                                InteractionScore
                            ).value,
                            "statuses": str(relationship.get_component(Statuses)),
                        },
                    )


EXPORT_SIM = False
YEARS_TO_SIMULATE = 500


@component(sim.world)
class Android(BaseCharacter):
    config = CharacterConfig(base_health_decay=0)

    @classmethod
    def _instantiate(
        cls,
        world: World,
        **kwargs: Any,
    ) -> GameObject:
        character = super()._instantiate(world, **kwargs)

        character.add_component(Robot)

        return character


def main():
    """Main entry point for this module"""

    dolores = Android.instantiate(
        sim.world,
        first_name="Dolores",
        last_name="Abernathy",
        age=32,
        gender=Female,
    )

    house = House.instantiate(sim.world, lot=(1, 1))

    set_residence(dolores, house)

    st = time.time()
    sim.run_for(YEARS_TO_SIMULATE)
    elapsed_time = time.time() - st

    print(f"World Date: {str(sim.world.resource_manager.get_resource(SimDateTime))}")
    print("Execution time: ", elapsed_time, "seconds")

    if EXPORT_SIM:
        with open(f"neighborly_{sim.config.seed}.json", "w") as f:
            f.write(export_to_json(sim))


if __name__ == "__main__":
    main()
