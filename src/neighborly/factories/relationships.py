"""Factories for relationship components.

"""

from typing import Any

from neighborly.components.relationship import Relationships, SocialRules
from neighborly.ecs import Component, ComponentFactory, GameObject


class RelationshipsFactory(ComponentFactory):
    """Creates instances of Relationships components."""

    __component__ = "Relationships"

    def instantiate(self, gameobject: GameObject, /, **kwargs: Any) -> Component:
        return Relationships(gameobject)


class SocialRulesFactory(ComponentFactory):
    """Creates instances of SocialRules components."""

    __component__ = "SocialRules"

    def instantiate(self, gameobject: GameObject, /, **kwargs: Any) -> Component:
        return SocialRules(gameobject)