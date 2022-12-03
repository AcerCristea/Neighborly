from __future__ import annotations

from typing import Any, List, Optional, Tuple, cast

from neighborly.builtin import helpers
from neighborly.builtin.components import (
    Active,
    Age,
    CanGetPregnant,
    Deceased,
    Departed,
    Lifespan,
    Retired,
    Vacant,
)
from neighborly.builtin.role_filters import (
    friendship_gt,
    friendship_lt,
    get_romances_gt,
    is_single,
    relationship_has_tags,
    romance_gt,
    romance_lt,
)
from neighborly.core import query as querylib
from neighborly.core.business import Business, Occupation, OpenForBusiness, Unemployed
from neighborly.core.character import GameCharacter, LifeStage, LifeStageValue
from neighborly.core.ecs import GameObject, World
from neighborly.core.engine import NeighborlyEngine
from neighborly.core.event import Event, RoleList
from neighborly.core.life_event import (
    ILifeEvent,
    LifeEvent,
    LifeEventInstance,
    LifeEventRoleType,
    PatternLifeEvent,
)
from neighborly.core.relationship import Relationships
from neighborly.core.residence import Residence, Resident
from neighborly.core.time import SimDateTime


def become_friends_event(
    threshold: float = 0.7, probability: float = 1.0
) -> ILifeEvent:
    """Defines an event where two characters become friends"""

    def effect(world: World, event: Event):
        world.get_gameobject(event["Initiator"]).get_component(Relationships).get(
            event["Other"]
        ).add_tags("Friend")

        world.get_gameobject(event["Other"]).get_component(Relationships).get(
            event["Initiator"]
        ).add_tags("Friend")

    return PatternLifeEvent(
        name="BecomeFriends",
        pattern=querylib.Query(
            find=("Initiator", "Other"),
            clauses=[
                querylib.where(
                    querylib.has_components(GameCharacter, Active), "Initiator"
                ),
                querylib.where(querylib.has_components(GameCharacter, Active), "Other"),
                querylib.ne_(("Initiator", "Other")),
                querylib.where(friendship_gt(threshold), "Initiator", "Other"),
                querylib.where(friendship_gt(threshold), "Other", "Initiator"),
                querylib.where_not(
                    relationship_has_tags("Friend"), "Initiator", "Other"
                ),
            ],
        ),
        effect=effect,
        probability=probability,
    )


def become_enemies_event(
    threshold: float = 0.3, probability: float = 1.0
) -> ILifeEvent:
    """Defines an event where two characters become friends"""

    def effect(world: World, event: Event):
        world.get_gameobject(event["Initiator"]).get_component(Relationships).get(
            event["Other"]
        ).add_tags("Enemy")

        world.get_gameobject(event["Other"]).get_component(Relationships).get(
            event["Initiator"]
        ).add_tags("Enemy")

    return PatternLifeEvent(
        name="BecomeEnemies",
        pattern=querylib.Query(
            find=("Initiator", "Other"),
            clauses=[
                querylib.where(querylib.has_components(GameCharacter), "Initiator"),
                querylib.where(querylib.has_components(Active), "Initiator"),
                querylib.where(querylib.has_components(GameCharacter), "Other"),
                querylib.where(querylib.has_components(Active), "Other"),
                querylib.ne_(("Initiator", "Other")),
                querylib.where(friendship_lt(threshold), "Initiator", "Other"),
                querylib.where(friendship_lt(threshold), "Other", "Initiator"),
                querylib.where_not(
                    relationship_has_tags("Enemy"), "Initiator", "Other"
                ),
            ],
        ),
        effect=effect,
        probability=probability,
    )


def start_dating_event(threshold: float = 0.7, probability: float = 1.0) -> ILifeEvent:
    """Defines an event where two characters become friends"""

    def effect(world: World, event: Event):
        world.get_gameobject(event["Initiator"]).get_component(Relationships).get(
            event["Other"]
        ).add_tags("Dating", "Significant Other")

        world.get_gameobject(event["Other"]).get_component(Relationships).get(
            event["Initiator"]
        ).add_tags("Dating", "Significant Other")

    return PatternLifeEvent(
        name="StartDating",
        pattern=querylib.Query(
            find=("Initiator", "Other"),
            clauses=[
                querylib.get_with_components((GameCharacter, Active), "Initiator"),
                get_romances_gt(threshold, ("Initiator", "Other")),
                get_romances_gt(threshold, ("Other", "Initiator")),
                querylib.ne_(("Initiator", "Other")),
                querylib.where_not(
                    relationship_has_tags("Significant Other"), "Other", "Other_Curr_SO"
                ),
                querylib.where_not(
                    relationship_has_tags("Significant Other"),
                    "Initiator",
                    "Initiator_Curr_SO",
                ),
                querylib.where_not(
                    relationship_has_tags("Significant Other"), "Other", "Initiator"
                ),
                querylib.where_not(
                    relationship_has_tags("Family"), "Other", "Initiator"
                ),
                querylib.filter_(is_single, "Initiator"),
                querylib.filter_(is_single, "Other"),
            ],
        ),
        effect=effect,
        probability=probability,
    )


def stop_dating_event(threshold: float = 0.4, probability: float = 1.0) -> ILifeEvent:
    """Defines an event where two characters become friends"""

    def effect(world: World, event: Event):
        world.get_gameobject(event["Initiator"]).get_component(Relationships).get(
            event["Other"]
        ).remove_tags("Dating", "Significant Other")

        world.get_gameobject(event["Other"]).get_component(Relationships).get(
            event["Initiator"]
        ).remove_tags("Dating", "Significant Other")

    return PatternLifeEvent(
        name="DatingBreakUp",
        pattern=querylib.Query(
            find=("Initiator", "Other"),
            clauses=[
                querylib.where(
                    querylib.has_components(GameCharacter, Active), "Initiator"
                ),
                querylib.where(querylib.has_components(GameCharacter, Active), "Other"),
                querylib.ne_(("Initiator", "Other")),
                querylib.where(romance_lt(threshold), "Initiator", "Other"),
                querylib.where(romance_lt(threshold), "Other", "Initiator "),
                querylib.where(relationship_has_tags("Dating"), "Initiator", "Other"),
            ],
        ),
        effect=effect,
        probability=probability,
    )


def divorce_event(threshold: float = 0.4, probability: float = 1.0) -> ILifeEvent:
    """Defines an event where two characters become friends"""

    def effect(world: World, event: Event):
        world.get_gameobject(event["Initiator"]).get_component(Relationships).get(
            event["Other"]
        ).remove_tags("Spouse", "Significant Other")

        world.get_gameobject(event["Other"]).get_component(Relationships).get(
            event["Initiator"]
        ).remove_tags("Spouse", "Significant Other")

    return PatternLifeEvent(
        name="Divorce",
        pattern=querylib.Query(
            find=("Initiator", "Other"),
            clauses=[
                querylib.where(
                    querylib.has_components(GameCharacter, Active), "Initiator"
                ),
                querylib.where(querylib.has_components(GameCharacter, Active), "Other"),
                querylib.ne_(("Initiator", "Other")),
                querylib.where(romance_lt(threshold), "Initiator", "Other"),
                querylib.where(romance_lt(threshold), "Other", "Initiator "),
                querylib.where(relationship_has_tags("Spouse"), "Initiator", "Other"),
            ],
        ),
        effect=effect,
        probability=probability,
    )


def marriage_event(threshold: float = 0.7, probability: float = 1.0) -> ILifeEvent:
    """Defines an event where two characters become friends"""

    def effect(world: World, event: Event):
        world.get_gameobject(event["Initiator"]).get_component(Relationships).get(
            event["Other"]
        ).add_tags("Spouse", "Significant Other")

        world.get_gameobject(event["Initiator"]).get_component(Relationships).get(
            event["Other"]
        ).remove_tags("Dating")

        world.get_gameobject(event["Other"]).get_component(Relationships).get(
            event["Initiator"]
        ).add_tags("Spouse", "Significant Other")

        world.get_gameobject(event["Other"]).get_component(Relationships).get(
            event["Initiator"]
        ).remove_tags("Dating")

    return PatternLifeEvent(
        name="GetMarried",
        pattern=querylib.Query(
            find=("Initiator", "Other"),
            clauses=[
                querylib.where(
                    querylib.has_components(GameCharacter, Active), "Initiator"
                ),
                querylib.where(querylib.has_components(GameCharacter, Active), "Other"),
                querylib.ne_(("Initiator", "Other")),
                querylib.where(romance_gt(threshold), "Initiator", "Other"),
                querylib.where(romance_gt(threshold), "Other", "Initiator "),
                querylib.where(relationship_has_tags("Dating"), "Initiator", "Other"),
            ],
        ),
        effect=effect,
        probability=probability,
    )


def depart_due_to_unemployment() -> ILifeEvent:
    def bind_unemployed_character(
        world: World, roles: Event, candidate: Optional[GameObject]
    ):
        if candidate:
            if (
                candidate.has_component(Unemployed)
                and candidate.get_component(Unemployed).duration_days > 30
            ):
                return candidate
            return None

        eligible_characters: List[GameObject] = []
        for _, (unemployed, _) in world.get_components(Unemployed, Active):
            unemployed = cast(Unemployed, unemployed)
            if unemployed.duration_days > 30:
                eligible_characters.append(unemployed.gameobject)
        if eligible_characters:
            return world.get_resource(NeighborlyEngine).rng.choice(eligible_characters)
        return None

    def effect(world: World, event: Event):
        departed = world.get_gameobject(event["Person"])
        departed.remove_component(Active)
        departed.add_component(Departed())
        helpers.set_location(world, departed, None)

    return LifeEvent(
        name="DepartDueToUnemployment",
        roles=[LifeEventRoleType(name="Person", binder_fn=bind_unemployed_character)],
        effect=effect,
        probability=1,
    )


def pregnancy_event() -> ILifeEvent:
    """Defines an event where two characters stop dating"""

    def execute(world: World, event: Event):
        due_date = SimDateTime.from_iso_str(
            world.get_resource(SimDateTime).to_iso_str()
        )
        due_date.increment(months=9)

        world.get_gameobject(event["PregnantOne"]).add_component(
            Pregnant(
                partner_id=event["Other"],
                due_date=due_date,
            )
        )

    def prob_fn(world: World, event: Event):
        gameobject = world.get_gameobject(event["PregnantOne"])
        children = gameobject.get_component(Relationships).get_all_with_tags("Child")
        if len(children) >= 5:
            return 0.0
        else:
            return 4.0 - len(children) / 8.0

    return PatternLifeEvent(
        name="GotPregnant",
        pattern=querylib.Query(
            find=("PregnantOne", "Other"),
            clauses=[
                querylib.where(
                    querylib.has_components(GameCharacter, Active, CanGetPregnant),
                    "PregnantOne",
                ),
                querylib.where_not(querylib.has_components(Pregnant), "PregnantOne"),
                querylib.where(querylib.has_components(GameCharacter, Active), "Other"),
                querylib.ne_(("PregnantOne", "Other")),
                querylib.where_any(
                    querylib.where(
                        relationship_has_tags("Dating"), "PregnantOne", "Other"
                    ),
                    querylib.where(
                        relationship_has_tags("Married"), "PregnantOne", "Other"
                    ),
                ),
            ],
        ),
        effect=execute,
        probability=prob_fn,
    )


def retire_event(probability: float = 0.4) -> ILifeEvent:
    """
    Event for characters retiring from working after reaching elder status

    Parameters
    ----------
    probability: float
        Probability that an entity will retire from their job
        when they are an elder

    Returns
    -------
    LifeEvent
        LifeEventType instance with all configuration defined
    """

    def bind_retiree(
        world: World, roles: RoleList, candidate: Optional[GameObject] = None
    ):

        if candidate:
            if not candidate.has_component(Retired) and candidate.has_component(
                LifeStage, Occupation, Active
            ):
                if candidate.get_component(LifeStage).stage >= LifeStageValue.Senior:
                    return candidate
            return None

        eligible_characters: List[GameObject] = []
        for gid, (life_stage, _, _) in world.get_components(
            LifeStage, Occupation, Active
        ):
            life_stage = cast(LifeStage, life_stage)

            if life_stage.stage < LifeStageValue.Senior:
                continue

            gameobject = world.get_gameobject(gid)
            if not gameobject.has_component(Retired):
                eligible_characters.append(gameobject)
        if eligible_characters:
            return world.get_resource(NeighborlyEngine).rng.choice(eligible_characters)
        return None

    def execute(world: World, event: Event):
        retiree = world.get_gameobject(event["Retiree"])
        retiree.add_component(Retired())
        helpers.end_job(world, retiree, event.name)

    return LifeEvent(
        name="Retire",
        roles=[
            LifeEventRoleType(name="Retiree", binder_fn=bind_retiree),
        ],
        effect=execute,
        probability=probability,
    )


def find_own_place_event(probability: float = 0.1) -> ILifeEvent:
    def bind_potential_mover(world: World) -> List[Tuple[Any, ...]]:
        eligible: List[Tuple[Any, ...]] = []

        for gid, (_, _, life_stage, resident, _) in world.get_components(
            GameCharacter, Occupation, LifeStage, Resident, Active
        ):
            resident = cast(Resident, resident)
            life_stage = cast(LifeStage, life_stage)

            if life_stage.stage < LifeStageValue.YoungAdult:
                continue

            residence = world.get_gameobject(resident.residence).get_component(
                Residence
            )
            if gid not in residence.owners:
                eligible.append((gid,))

        return eligible

    def find_vacant_residences(world: World) -> List[Residence]:
        """Try to find a vacant residence to move into"""
        return list(
            map(
                lambda pair: cast(Residence, pair[1][0]),
                world.get_components(Residence, Vacant),
            )
        )

    def choose_random_vacant_residence(world: World) -> Optional[Residence]:
        """Randomly chooses a vacant residence to move into"""
        vacancies = find_vacant_residences(world)
        if vacancies:
            return world.get_resource(NeighborlyEngine).rng.choice(vacancies)
        return None

    def execute(world: World, event: Event):
        # Try to find somewhere to live
        character = world.get_gameobject(event["Character"])
        vacant_residence = choose_random_vacant_residence(world)
        if vacant_residence:
            # Move into house with any dependent children
            helpers.set_residence(world, character, vacant_residence.gameobject)

        # Depart if no housing could be found
        else:
            helpers.depart_town(world, character, event.name)

    return PatternLifeEvent(
        name="FindOwnPlace",
        probability=probability,
        pattern=querylib.Query(
            ("Character",), [querylib.where(bind_potential_mover, "Character")]
        ),
        effect=execute,
    )


def die_of_old_age(probability: float = 0.8) -> ILifeEvent:
    def execute(world: World, event: Event) -> None:
        deceased = world.get_gameobject(event["Deceased"])
        deceased.add_component(Deceased())
        deceased.remove_component(Active)

    return PatternLifeEvent(
        name="DieOfOldAge",
        probability=probability,
        pattern=querylib.Query(
            ("Deceased",),
            [
                querylib.where(
                    querylib.has_components(GameCharacter, Active, Age, Lifespan),
                    "Deceased",
                ),
                querylib.filter_(
                    lambda world, *gameobjects: gameobjects[0].get_component(Age).value
                    >= gameobjects[0].get_component(Lifespan).value,
                    "Deceased",
                ),
            ],
        ),
        effect=execute,
    )


def go_out_of_business_event() -> ILifeEvent:
    def effect(world: World, event: Event):
        business = world.get_gameobject(event["Business"])
        helpers.shutdown_business(world, business)

    def probability_fn(world: World, event: LifeEventInstance) -> float:
        business = world.get_gameobject(event.roles["Business"])
        lifespan = business.get_component(Lifespan).value
        age = business.get_component(Age).value
        if age < 5:
            return 0
        elif age < lifespan:
            return age / lifespan
        else:
            return 0.8

    return PatternLifeEvent(
        name="GoOutOfBusiness",
        pattern=querylib.Query(
            find=("Business",),
            clauses=[
                querylib.where(
                    querylib.has_components(Business, OpenForBusiness, Active),
                    "Business",
                )
            ],
        ),
        effect=effect,
        probability=probability_fn,
    )
