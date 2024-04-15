"""Other event implementations.

"""

from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from neighborly.defs.base_types import JobRoleDef
from neighborly.ecs import GameObject
from neighborly.life_event import LifeEvent


class StartNewJobEvent(LifeEvent):
    """A character will attempt to find a job."""

    __event_id__ = "new_job"
    __tablename__ = "new_job_event"
    __mapper_args__ = {
        "polymorphic_identity": "new_job",
    }

    event_id: Mapped[int] = mapped_column(
        ForeignKey("life_events.event_id"), primary_key=True, autoincrement=True
    )
    character_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))
    character: GameObject
    business: GameObject
    business_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))
    job_role: JobRoleDef
    job_role_id: Mapped[str]

    def __init__(
        self, character: GameObject, business: GameObject, job_role: JobRoleDef
    ) -> None:
        super().__init__(character.world)
        self.character = character
        self.character_id = character.uid
        self.business = business
        self.business_id = business.uid
        self.job_role = job_role
        self.job_role_id = job_role.definition_id

    def __str__(self) -> str:
        return (
            f"{self.character.name} started a new job as a "
            f"{self.job_role.name} at {self.business.name}."
        )


class StartBusinessEvent(LifeEvent):
    """Character starts a specific business."""

    __event_id__ = "start_business"
    __tablename__ = "start_business_event"
    __mapper_args__ = {
        "polymorphic_identity": "start_business",
    }

    event_id: Mapped[int] = mapped_column(
        ForeignKey("life_events.event_id"), primary_key=True, autoincrement=True
    )
    character_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))
    character: GameObject
    business: GameObject
    business_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))

    def __init__(
        self,
        character: GameObject,
        business: GameObject,
    ) -> None:
        super().__init__(character.world)
        self.character = character
        self.character_id = character.uid
        self.business = business
        self.business_id = business.uid

    def __str__(self) -> str:
        return f"{self.character.name} opened a new business, {self.business.name}."


class StartDatingEvent(LifeEvent):
    """Event dispatched when two characters start dating."""

    __event_id__ = "start_dating"
    __tablename__ = "start_dating_event"
    __mapper_args__ = {
        "polymorphic_identity": "start_dating",
    }

    event_id: Mapped[int] = mapped_column(
        ForeignKey("life_events.event_id"), primary_key=True, autoincrement=True
    )
    initiator_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))
    initiator: GameObject
    partner: GameObject
    partner_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))

    def __init__(self, initiator: GameObject, partner: GameObject) -> None:
        super().__init__(initiator.world)
        self.initiator = initiator
        self.initiator_id = initiator.uid
        self.partner = partner
        self.partner_id = partner.uid

    def __str__(self) -> str:
        return f"{self.initiator.name} and {self.partner.name} started dating."


class MarriageEvent(LifeEvent):
    """Event dispatched when two characters get married."""

    __event_id__ = "marriage"
    __tablename__ = "marriage_event"
    __mapper_args__ = {
        "polymorphic_identity": "marriage_event",
    }

    event_id: Mapped[int] = mapped_column(
        ForeignKey("life_events.event_id"), primary_key=True, autoincrement=True
    )
    initiator_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))
    initiator: GameObject
    partner: GameObject
    partner_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))

    def __init__(self, initiator: GameObject, partner: GameObject) -> None:
        super().__init__(initiator.world)
        self.initiator = initiator
        self.initiator_id = initiator.uid
        self.partner = partner
        self.partner_id = partner.uid

    def __str__(self) -> str:
        return f"{self.initiator.name} and {self.partner.name} got married."


class DivorceEvent(LifeEvent):
    """Dispatched to officially divorce two married characters."""

    __event_id__ = "divorce"
    __tablename__ = "divorce_event"
    __mapper_args__ = {
        "polymorphic_identity": "divorce",
    }

    event_id: Mapped[int] = mapped_column(
        ForeignKey("life_events.event_id"), primary_key=True, autoincrement=True
    )
    initiator_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))
    initiator: GameObject
    partner: GameObject
    partner_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))

    def __init__(self, initiator: GameObject, partner: GameObject) -> None:
        super().__init__(initiator.world)
        self.initiator = initiator
        self.initiator_id = initiator.uid
        self.partner = partner
        self.partner_id = partner.uid

    def __str__(self) -> str:
        return f"{self.initiator.name} divorced from {self.partner.name}."


class DatingBreakUpEvent(LifeEvent):
    """Dispatched to officially break up a dating relationship between characters."""

    __event_id__ = "dating_break_up"
    __tablename__ = "break_up_event"
    __mapper_args__ = {
        "polymorphic_identity": "dating_break_up",
    }

    event_id: Mapped[int] = mapped_column(
        ForeignKey("life_events.event_id"), primary_key=True, autoincrement=True
    )
    initiator_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))
    initiator: GameObject
    partner: GameObject
    partner_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))

    def __init__(self, initiator: GameObject, partner: GameObject) -> None:
        super().__init__(initiator.world)
        self.initiator = initiator
        self.initiator_id = initiator.uid
        self.partner = partner
        self.partner_id = partner.uid

    def __str__(self) -> str:
        return f"{self.initiator.name} broke up with " f"{self.partner.name}."


class PregnancyEvent(LifeEvent):
    """Characters have a chance of getting pregnant while in romantic relationships."""

    __event_id__ = "pregnancy"
    __tablename__ = "pregnancy_event"
    __mapper_args__ = {
        "polymorphic_identity": "pregnancy",
    }

    event_id: Mapped[int] = mapped_column(
        ForeignKey("life_events.event_id"), primary_key=True, autoincrement=True
    )
    character_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))
    character: GameObject
    partner: GameObject
    partner_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))

    def __init__(
        self,
        character: GameObject,
        partner: GameObject,
    ) -> None:
        super().__init__(character.world)
        self.character = character
        self.character_id = character.uid
        self.partner = partner
        self.partner_id = partner.uid

    def __str__(self) -> str:
        return f"{self.character.name} got pregnant."


class RetirementEvent(LifeEvent):
    """Simulates a character retiring from their position at a business.

    When a business owner retires they may appoint a current employee or family member
    to become the owner of the business. If they can't find a suitable successor,
    then they shut the business down and everyone is laid-off.

    If the retiree is an employee, they are just removed from their role and business
    continues as usual.
    """

    __event_id__ = "retirement"
    __tablename__ = "retirement_event"
    __mapper_args__ = {
        "polymorphic_identity": "retirement",
    }

    event_id: Mapped[int] = mapped_column(
        ForeignKey("life_events.event_id"), primary_key=True, autoincrement=True
    )
    character_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))
    character: GameObject
    business: GameObject
    business_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))
    job_role: JobRoleDef
    job_role_id: Mapped[str]

    def __init__(
        self,
        character: GameObject,
        business: GameObject,
        job_role: JobRoleDef,
    ) -> None:
        super().__init__(character.world)
        self.character = character
        self.character_id = character.uid
        self.business = business
        self.business_id = business.uid
        self.job_role = job_role
        self.job_role_id = job_role.definition_id

    def __str__(self) -> str:
        return (
            f"{self.character.name} retired from their "
            f"position as {self.job_role.name} at {self.business.name}."
        )


class JobPromotionEvent(LifeEvent):
    """The character is promoted at their job from a lower role to a higher role."""

    __event_id__ = "job_promotion"
    __tablename__ = "job_promotion_event"
    __mapper_args__ = {
        "polymorphic_identity": "job_promotion",
    }

    event_id: Mapped[int] = mapped_column(
        ForeignKey("life_events.event_id"), primary_key=True, autoincrement=True
    )
    character_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))
    character: GameObject
    business: GameObject
    business_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))
    job_role: JobRoleDef
    job_role_id: Mapped[str]

    def __init__(
        self,
        character: GameObject,
        business: GameObject,
        job_role: JobRoleDef,
    ) -> None:
        super().__init__(character.world)
        self.character = character
        self.character_id = character.uid
        self.business = business
        self.business_id = business.uid
        self.job_role = job_role
        self.job_role_id = job_role.definition_id

    def __str__(self) -> str:
        return (
            f"{self.character.name} was promoted from to "
            f"{self.job_role.name} at {self.business.name}."
        )


class FiredFromJobEvent(LifeEvent):
    """The character is fired from their job."""

    __event_id__ = "fired"
    __tablename__ = "fired_event"
    __mapper_args__ = {
        "polymorphic_identity": "fired",
    }

    event_id: Mapped[int] = mapped_column(
        ForeignKey("life_events.event_id"), primary_key=True, autoincrement=True
    )
    character_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))
    character: GameObject
    business: GameObject
    business_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))
    job_role: JobRoleDef
    job_role_id: Mapped[str]

    def __init__(
        self, character: GameObject, business: GameObject, job_role: JobRoleDef
    ) -> None:
        super().__init__(character.world)
        self.character = character
        self.character_id = character.uid
        self.business = business
        self.business_id = business.uid
        self.job_role = job_role
        self.job_role_id = job_role.definition_id

    def __str__(self) -> str:
        return (
            f"{self.character.name} was fired from their role as a "
            f"{self.job_role.name} at {self.business.name}."
        )
