"""Components for representing residential buildings.

"""

from __future__ import annotations

from typing import Any, Iterable

from ordered_set import OrderedSet
from sqlalchemy import ForeignKey, delete
from sqlalchemy.orm import Mapped, mapped_column

from neighborly.ecs import Component, GameData, GameObject, TagComponent


class ResidentialUnitData(GameData):
    """Queryable information about a residential unit."""

    __tablename__ = "residential_units"

    uid: Mapped[int] = mapped_column(
        ForeignKey("gameobjects.uid"), primary_key=True, unique=True
    )
    district_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))
    building_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))


class ResidentialUnit(Component):
    """A Residence is a place where characters live."""

    __slots__ = "_owners", "_residents", "_district", "_building"

    _building: GameObject
    """The building this unit is in."""
    _district: GameObject
    """The district the residence is in."""
    _owners: OrderedSet[GameObject]
    """Characters that currently own the residence."""
    _residents: OrderedSet[GameObject]
    """All the characters who live at the residence (including non-owners)."""

    def __init__(
        self, gameobject: GameObject, building: GameObject, district: GameObject
    ) -> None:
        super().__init__(gameobject)
        self._building = building
        self._district = district
        self._owners = OrderedSet([])
        self._residents = OrderedSet([])

    @property
    def building(self) -> GameObject:
        """Get the building the residential unit is in."""
        return self._building

    @property
    def district(self) -> GameObject:
        """Get the district the residence is in."""
        return self._district

    @property
    def owners(self) -> Iterable[GameObject]:
        """Get the owners of the residence."""
        return self._owners

    @property
    def residents(self) -> Iterable[GameObject]:
        """Get all the residents of the residence."""
        return self._residents

    def to_dict(self) -> dict[str, Any]:
        return {
            "district": self.district.uid,
            "owners": [entry.uid for entry in self.owners],
            "residents": [entry.uid for entry in self.residents],
        }

    def add_owner(self, owner: GameObject) -> None:
        """Add owner to the residence.

        Parameters
        ----------
        owner
            A GameObject reference to a residence owner.
        """
        self._owners.add(owner)
        self.gameobject.world.rp_db.insert(
            f"{self.gameobject.uid}.residence.owners.{owner.uid}"
        )

    def remove_owner(self, owner: GameObject) -> None:
        """Remove owner from residence.

        Parameters
        ----------
        owner
            A GameObject reference to a residence owner.
        """
        self._owners.remove(owner)
        self.gameobject.world.rp_db.delete(
            f"{self.gameobject.uid}.residence.owners.{owner.uid}"
        )

    def is_owner(self, character: GameObject) -> bool:
        """Check if a GameObject owns a residence.

        Parameters
        ----------
        character
            A GameObject reference to a residence owner.
        """
        return character in self._owners

    def add_resident(self, resident: GameObject) -> None:
        """Add a tenant to this residence.

        Parameters
        ----------
        resident
            A GameObject reference to a resident.
        """
        self._residents.add(resident)
        self.gameobject.world.rp_db.insert(
            f"{self.gameobject.uid}.residence.residents.{resident.uid}"
        )

    def remove_resident(self, resident: GameObject) -> None:
        """Remove a tenant rom this residence.

        Parameters
        ----------
        resident
            A GameObject reference to a resident.
        """
        self._residents.remove(resident)
        self.gameobject.world.rp_db.delete(
            f"{self.gameobject.uid}.residence.residents.{resident.uid}"
        )

    def is_resident(self, character: GameObject) -> bool:
        """Check if a GameObject is a resident.

        Parameters
        ----------
        character
            A GameObject reference to a character
        """
        return character in self._residents

    def on_add(self) -> None:
        with self.gameobject.world.session.begin() as session:
            session.add(
                ResidentialUnitData(
                    uid=self.gameobject.uid,
                    district_id=self.district.uid,
                    building_id=self.building.uid,
                )
            )

        self.gameobject.world.rp_db.insert(
            f"{self.gameobject.uid}.residence.district!{self.district.uid}"
        )

    def on_remove(self) -> None:
        with self.gameobject.world.session.begin() as session:
            session.execute(
                delete(ResidentialUnitData).where(
                    ResidentialUnitData.uid == self.gameobject.uid
                )
            )

        self.gameobject.world.rp_db.delete(f"{self.gameobject.uid}.residence")

    def __repr__(self) -> str:
        return f"Residence({self.to_dict()})"

    def __str__(self) -> str:
        return f"Residence({self.to_dict()})"

    def __len__(self) -> int:
        return len(self._residents)


class ResidentialBuildingData(GameData):
    """Queryable residential component data."""

    __tablename__ = "residential_buildings"

    uid: Mapped[int] = mapped_column(
        ForeignKey("gameobjects.uid"), primary_key=True, unique=True
    )
    district_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))


class ResidentialBuilding(Component):
    """Tags a building as managing multiple residential units."""

    __slots__ = "_residential_units", "_district"

    _district: GameObject
    """The district the residence is in."""
    _residential_units: list[GameObject]
    """The residential units that belong to this building."""

    def __init__(self, gameobject: GameObject, district: GameObject) -> None:
        super().__init__(gameobject)
        self._district = district
        self._residential_units = []

    @property
    def district(self) -> GameObject:
        """Get the district the residential building belongs to."""
        return self._district

    @property
    def units(self) -> Iterable[GameObject]:
        """Get the residential units within the building."""
        return self._residential_units

    def add_residential_unit(self, residence: GameObject) -> None:
        """Add a residential unit to the building."""
        self._residential_units.append(residence)
        self.gameobject.world.rp_db.insert(
            f"{self.gameobject.uid}.residential_building.units.{residence.uid}"
        )

    def remove_residential_unit(self, residence: GameObject) -> None:
        """Add a residential unit to the building."""
        self._residential_units.remove(residence)
        self.gameobject.world.rp_db.delete(
            f"{self.gameobject.uid}.residential_building.units.{residence.uid}"
        )

    def on_add(self) -> None:
        with self.gameobject.world.session.begin() as session:
            session.add(
                ResidentialBuildingData(
                    uid=self.gameobject.uid, district_id=self.district.uid
                )
            )

        self.gameobject.world.rp_db.insert(
            f"{self.gameobject.uid}.residential_building.district!{self.district.uid}"
        )

    def on_remove(self) -> None:
        with self.gameobject.world.session.begin() as session:
            session.execute(
                delete(ResidentialBuildingData).where(
                    ResidentialBuildingData.uid == self.gameobject.uid
                )
            )

        self.gameobject.world.rp_db.delete(
            f"{self.gameobject.uid}.residential_building"
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "district": self.district.uid,
            "units": [u.uid for u in self._residential_units],
        }


class ResidentData(GameData):
    """Queryable Vacant component data."""

    __tablename__ = "residents"

    uid: Mapped[int] = mapped_column(
        ForeignKey("gameobjects.uid"), primary_key=True, unique=True
    )
    residence_id: Mapped[int] = mapped_column(ForeignKey("gameobjects.uid"))


class Resident(Component):
    """A Component attached to characters that tracks where they live."""

    __slots__ = ("residence",)

    residence: GameObject
    """The GameObject ID of their residence."""

    def __init__(self, gameobject: GameObject, residence: GameObject) -> None:
        """
        Parameters
        ----------
        residence
            A GameObject reference to their residence.
        """
        super().__init__(gameobject)
        self.residence = residence

    def on_add(self) -> None:
        with self.gameobject.world.session.begin() as session:
            session.add(
                ResidentData(uid=self.gameobject.uid, residence_id=self.residence.uid)
            )

        self.gameobject.world.rp_db.insert(
            f"{self.gameobject.uid}.resident.residence!{self.residence.uid}"
        )

    def on_remove(self) -> None:
        with self.gameobject.world.session.begin() as session:
            session.execute(
                delete(ResidentData).where(ResidentData.uid == self.gameobject.uid)
            )

        self.gameobject.world.rp_db.delete(f"{self.gameobject.uid}.resident")

    def to_dict(self) -> dict[str, Any]:
        return {"residence": self.residence.uid}

    def __repr__(self) -> str:
        return f"Resident({self.to_dict()})"

    def __str__(self) -> str:
        return f"Resident({self.to_dict()})"


class VacantData(GameData):
    """Queryable Vacant component data."""

    __tablename__ = "vacant"

    uid: Mapped[int] = mapped_column(
        ForeignKey("gameobjects.uid"), primary_key=True, unique=True
    )


class Vacant(TagComponent):
    """Tags a residence that does not currently have anyone living there."""

    def on_add(self) -> None:
        with self.gameobject.world.session.begin() as session:
            session.add(VacantData(uid=self.gameobject.uid))

        self.gameobject.world.rp_db.insert(f"{self.gameobject.uid}.vacant")

    def on_remove(self) -> None:
        with self.gameobject.world.session.begin() as session:
            session.execute(
                delete(VacantData).where(VacantData.uid == self.gameobject.uid)
            )

        self.gameobject.world.rp_db.delete(f"{self.gameobject.uid}.vacant")
