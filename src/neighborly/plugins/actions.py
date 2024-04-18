"""Action definitions.

"""

import random

from neighborly.action import Action
from neighborly.components.business import (
    Business,
    BusinessStatus,
    Occupation,
    Unemployed,
)
from neighborly.components.character import Pregnant
from neighborly.components.relationship import Relationship
from neighborly.components.residence import Resident, ResidentialUnit, Vacant
from neighborly.datetime import SimDate
from neighborly.defs.base_types import JobRoleDef
from neighborly.ecs import GameObject
from neighborly.helpers.action import get_action_success_probability, get_action_utility
from neighborly.helpers.business import close_business, fire_employee, leave_job
from neighborly.helpers.character import (
    depart_settlement,
    move_into_residence,
    move_out_of_residence,
)
from neighborly.helpers.location import add_frequented_location
from neighborly.helpers.relationship import get_relationship
from neighborly.helpers.stats import get_stat
from neighborly.helpers.traits import (
    add_trait,
    get_relationships_with_traits,
    has_trait,
    remove_trait,
)
from neighborly.life_event import add_to_personal_history, dispatch_life_event
from neighborly.plugins.default_events import (
    DatingBreakUpEvent,
    PregnancyEvent,
    RetirementEvent,
    StartBusinessEvent,
)


class BecomeBusinessOwner(Action):
    """Character attempts to become the owner of a business."""

    __action_id__ = "become-business-owner"

    __slots__ = ("character", "business")

    character: GameObject
    business: GameObject

    def __init__(self, character: GameObject, business: GameObject) -> None:
        super().__init__(character.world)
        self.character = character
        self.business = business

    def on_success(self) -> None:
        owner_role = self.business.get_component(Business).owner_role
        business_component = self.business.get_component(Business)

        self.character.add_component(
            Occupation(
                self.character,
                business=self.business,
                start_date=self.world.resources.get_resource(SimDate).copy(),
                job_role=owner_role,
            )
        )

        add_frequented_location(self.character, self.business)

        business_component.set_owner(self.character)

        business_component.status = BusinessStatus.OPEN

        if self.character.has_component(Unemployed):
            self.character.remove_component(Unemployed)

        start_business_event = StartBusinessEvent(
            character=self.character,
            business=self.business,
        )

        add_to_personal_history(self.character, start_business_event)
        add_to_personal_history(self.business, start_business_event)
        dispatch_life_event(self.world, start_business_event)

    def on_failure(self) -> None:
        return


class FormCrush(Action):
    """A character forms a crush on another."""

    __action_id__ = "form-crush"

    __slots__ = ("character", "crush")

    character: GameObject
    crush: GameObject

    def __init__(self, character: GameObject, crush: GameObject) -> None:
        super().__init__(character.world)
        self.character = character
        self.crush = crush

    def on_success(self) -> None:
        for rel in get_relationships_with_traits(self.character, "crush"):
            remove_trait(rel, "crush")

        add_trait(get_relationship(self.character, self.crush), "crush")

    def on_failure(self) -> None:
        return


class Retire(Action):
    """A character retires from their position at a business."""

    __action_id__ = "retire"

    __slots__ = ("character",)

    character: GameObject

    def __init__(self, character: GameObject) -> None:
        super().__init__(character.world)
        self.character = character

    def on_success(self) -> None:
        rng = self.world.resource_manager.get_resource(random.Random)

        occupation = self.character.get_component(Occupation)
        business = occupation.business
        business_data = business.get_component(Business)

        add_trait(self.character, "retired")
        dispatch_life_event(
            self.world,
            RetirementEvent(self.character, business, occupation.job_role),
        )
        leave_job(business, self.character)

        # If the character retiring is the owner of the business, try to find a
        # successor among the people they like. If none is found, lay everyone off and
        # close the business.
        if business.get_component(Business).owner == self.character:

            potential_successors: list[tuple[GameObject, float]] = sorted(
                [
                    (
                        employee,
                        get_stat(
                            get_relationship(self.character, employee), "reputation"
                        ).value,
                    )
                    for employee, _ in business_data.employees.items()
                ],
                key=lambda entry: entry[1],
            )

            if not potential_successors:
                return

            successor = potential_successors[-1][0]

            action = BecomeBusinessOwner(successor, business)

            utility_score = get_action_utility(action)

            if rng.random() < utility_score:

                probability_success = get_action_success_probability(action)

                if rng.random() < probability_success:
                    action.on_success()
                else:
                    action.on_failure()
                    close_business(business)

    def on_failure(self) -> None:
        return


class GetPregnant(Action):
    """A character gets pregnant by another."""

    __action_id__ = "get-pregnant"

    __slots__ = ("character", "partner")

    character: GameObject
    partner: GameObject

    def __init__(self, character: GameObject, partner: GameObject) -> None:
        super().__init__(character.world)
        self.character = character
        self.partner = partner

    def on_success(self) -> None:
        due_date = self.world.resources.get_resource(SimDate).copy()
        due_date.increment(months=9)

        self.character.add_component(Pregnant(self.character, self.partner, due_date))

        dispatch_life_event(self.world, PregnancyEvent(self.character, self.partner))

    def on_failure(self) -> None:
        return


class BreakUp(Action):
    """A character stops dating another."""

    __action_id__ = "break-up"

    __slots__ = ("character", "partner")

    character: GameObject
    partner: GameObject

    def __init__(self, character: GameObject, partner: GameObject) -> None:
        super().__init__(character.world)
        self.character = character
        self.partner = partner

    def on_success(self) -> None:
        remove_trait(get_relationship(self.character, self.partner), "dating")
        remove_trait(get_relationship(self.partner, self.character), "dating")

        add_trait(get_relationship(self.character, self.partner), "ex_partner")
        add_trait(get_relationship(self.partner, self.character), "ex_partner")

        get_stat(
            get_relationship(self.partner, self.character), "romance"
        ).base_value -= 15

        dispatch_life_event(
            self.world, DatingBreakUpEvent(self.character, self.partner)
        )

    def on_failure(self) -> None:
        return


class Divorce(Action):
    """A character stops being married another."""

    __action_id__ = "divorce"

    __slots__ = ("character", "partner")

    character: GameObject
    partner: GameObject

    def __init__(self, character: GameObject, partner: GameObject) -> None:
        super().__init__(character.world)
        self.character = character
        self.partner = partner

    def on_success(self) -> None:
        remove_trait(get_relationship(self.character, self.partner), "spouse")
        remove_trait(get_relationship(self.partner, self.character), "spouse")

        add_trait(get_relationship(self.character, self.partner), "ex_spouse")
        add_trait(get_relationship(self.partner, self.character), "ex_spouse")

        get_stat(
            get_relationship(self.partner, self.character), "romance"
        ).base_value -= 25

        # initiator finds new place to live or departs
        vacant_housing = self.world.get_components((ResidentialUnit, Vacant))

        move_out_of_residence(self.character)

        if vacant_housing:
            _, (residence, _) = vacant_housing[0]

            move_into_residence(
                self.character, new_residence=residence.gameobject, is_owner=True
            )

        else:
            depart_settlement(self.character)

    def on_failure(self) -> None:
        return


class GetMarried(Action):
    """A two characters get married."""

    __action_id__ = "get-married"

    __slots__ = ("character", "partner")

    character: GameObject
    partner: GameObject

    def __init__(self, character: GameObject, partner: GameObject) -> None:
        super().__init__(character.world)
        self.character = character
        self.partner = partner

    def on_success(self) -> None:
        remove_trait(get_relationship(self.character, self.partner), "dating")
        remove_trait(get_relationship(self.partner, self.character), "dating")

        add_trait(get_relationship(self.character, self.partner), "spouse")
        add_trait(get_relationship(self.partner, self.character), "spouse")

        # Update residences
        shared_residence = self.character.get_component(Resident).residence

        move_into_residence(self.partner, shared_residence, is_owner=True)

        for rel in get_relationships_with_traits(
            self.partner, "child", "live_together"
        ):
            target = rel.get_component(Relationship).target
            move_into_residence(target, shared_residence)

        # Update step sibling relationships
        for rel_0 in get_relationships_with_traits(self.character, "child"):
            if not rel_0.is_active:
                continue

            child_0 = rel_0.get_component(Relationship).target

            for rel_1 in get_relationships_with_traits(self.partner, "child"):
                if not rel_1.is_active:
                    continue

                child_1 = rel_1.get_component(Relationship).target

                add_trait(get_relationship(child_0, child_1), "step_sibling")
                add_trait(get_relationship(child_0, child_1), "sibling")
                add_trait(get_relationship(child_1, child_0), "step_sibling")
                add_trait(get_relationship(child_1, child_0), "sibling")

        # Update relationships parent/child relationships
        for rel in get_relationships_with_traits(self.character, "child"):
            if rel.is_active:
                child = rel.get_component(Relationship).target
                if not has_trait(get_relationship(self.partner, child), "child"):
                    add_trait(get_relationship(self.partner, child), "child")
                    add_trait(get_relationship(self.partner, child), "step_child")
                    add_trait(get_relationship(child, self.partner), "parent")
                    add_trait(get_relationship(child, self.partner), "step_parent")

        for rel in get_relationships_with_traits(self.partner, "child"):
            if rel.is_active:
                child = rel.get_component(Relationship).target
                if not has_trait(get_relationship(self.character, child), "child"):
                    add_trait(get_relationship(self.character, child), "child")
                    add_trait(get_relationship(self.character, child), "step_child")
                    add_trait(get_relationship(child, self.character), "parent")
                    add_trait(get_relationship(child, self.character), "step_parent")

    def on_failure(self) -> None:
        return


class StartDating(Action):
    """A character start dating another."""

    __action_id__ = "start-dating"

    __slots__ = ("character", "partner")

    character: GameObject
    partner: GameObject

    def __init__(self, character: GameObject, partner: GameObject) -> None:
        super().__init__(character.world)
        self.character = character
        self.partner = partner

    def on_success(self) -> None:
        add_trait(get_relationship(self.character, self.partner), "dating")
        add_trait(get_relationship(self.partner, self.character), "dating")

    def on_failure(self) -> None:
        return


class FireEmployee(Action):
    """A business owner fires an employee."""

    __action_id__ = "fire-employee"

    __slots__ = ("character", "employee")

    character: GameObject
    employee: GameObject

    def __init__(self, character: GameObject, employee: GameObject) -> None:
        super().__init__(character.world)
        self.character = character
        self.employee = employee

    def on_success(self) -> None:
        business = self.character.get_component(Occupation).business
        fire_employee(business, self.employee)

    def on_failure(self) -> None:
        return


class PromoteEmployee(Action):
    """A business owner promotes an employee."""

    __action_id__ = "promote-employee"

    __slots__ = ("character", "employee", "role")

    character: GameObject
    employee: GameObject
    role: JobRoleDef

    def __init__(
        self, character: GameObject, employee: GameObject, role: JobRoleDef
    ) -> None:
        super().__init__(character.world)
        self.character = character
        self.employee = employee
        self.role = role

    def on_success(self) -> None:
        business = self.character.get_component(Occupation).business
        fire_employee(business, self.employee)

    def on_failure(self) -> None:
        return
