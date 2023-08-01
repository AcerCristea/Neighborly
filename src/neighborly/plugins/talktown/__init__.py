from neighborly.plugins.talktown import businesses, occupations
from neighborly.plugins.talktown.school import (
    CollegeGraduate,
    EnrollInSchoolSystem,
    GraduateAdultStudentsSystem,
    SchoolSystemGroup,
    Student,
)
from neighborly.simulation import Neighborly, PluginInfo
from neighborly.systems import EarlyUpdateSystemGroup

plugin_info = PluginInfo(
    name="Talk of the Town Plugin",
    plugin_id="default.talktown",
    version="0.1.0",
)


def setup(sim: Neighborly):
    sim.world.system_manager.add_system(
        SchoolSystemGroup(), system_group=EarlyUpdateSystemGroup
    )
    sim.world.system_manager.add_system(
        EnrollInSchoolSystem(), system_group=SchoolSystemGroup
    )
    sim.world.system_manager.add_system(
        GraduateAdultStudentsSystem(), system_group=SchoolSystemGroup
    )

    # Register student component for school system
    sim.world.gameobject_manager.register_component(Student)
    sim.world.gameobject_manager.register_component(CollegeGraduate)

    # Register Business components
    sim.world.gameobject_manager.register_component(businesses.Bakery)
    sim.world.gameobject_manager.register_component(businesses.Bank)
    sim.world.gameobject_manager.register_component(businesses.Bar)
    sim.world.gameobject_manager.register_component(businesses.BarberShop)
    sim.world.gameobject_manager.register_component(businesses.BlacksmithShop)
    sim.world.gameobject_manager.register_component(businesses.Brewery)
    sim.world.gameobject_manager.register_component(businesses.BusDepot)
    sim.world.gameobject_manager.register_component(businesses.ButcherShop)
    sim.world.gameobject_manager.register_component(businesses.CandyStore)
    sim.world.gameobject_manager.register_component(
        businesses.CarpentryCompany
    )
    sim.world.gameobject_manager.register_component(businesses.Cemetery)
    sim.world.gameobject_manager.register_component(businesses.CityHall)
    sim.world.gameobject_manager.register_component(businesses.ClothingStore)
    sim.world.gameobject_manager.register_component(businesses.CoalMine)
    sim.world.gameobject_manager.register_component(
        businesses.ConstructionFirm
    )
    sim.world.gameobject_manager.register_component(businesses.Dairy)
    sim.world.gameobject_manager.register_component(businesses.DaycareCenter)
    sim.world.gameobject_manager.register_component(businesses.Deli)
    sim.world.gameobject_manager.register_component(businesses.DentistOffice)
    sim.world.gameobject_manager.register_component(businesses.DepartmentStore)
    sim.world.gameobject_manager.register_component(businesses.Diner)
    sim.world.gameobject_manager.register_component(businesses.Distillery)
    sim.world.gameobject_manager.register_component(businesses.DrugStore)
    sim.world.gameobject_manager.register_component(businesses.Farm)
    sim.world.gameobject_manager.register_component(businesses.FireStation)
    sim.world.gameobject_manager.register_component(businesses.Foundry)
    sim.world.gameobject_manager.register_component(businesses.FurnitureStore)
    sim.world.gameobject_manager.register_component(businesses.GeneralStore)
    sim.world.gameobject_manager.register_component(businesses.GroceryStore)
    sim.world.gameobject_manager.register_component(businesses.HardwareStore)
    sim.world.gameobject_manager.register_component(businesses.Hospital)
    sim.world.gameobject_manager.register_component(businesses.Hotel)
    sim.world.gameobject_manager.register_component(businesses.Inn)
    sim.world.gameobject_manager.register_component(
        businesses.InsuranceCompany
    )
    sim.world.gameobject_manager.register_component(businesses.JewelryShop)
    sim.world.gameobject_manager.register_component(businesses.LawFirm)
    sim.world.gameobject_manager.register_component(businesses.OptometryClinic)
    sim.world.gameobject_manager.register_component(businesses.PaintingCompany)
    sim.world.gameobject_manager.register_component(businesses.Park)
    sim.world.gameobject_manager.register_component(businesses.Pharmacy)
    sim.world.gameobject_manager.register_component(
        businesses.PlasticSurgeryClinic
    )
    sim.world.gameobject_manager.register_component(businesses.PlumbingCompany)
    sim.world.gameobject_manager.register_component(businesses.PoliceStation)
    sim.world.gameobject_manager.register_component(businesses.Quarry)
    sim.world.gameobject_manager.register_component(businesses.RealtyFirm)
    sim.world.gameobject_manager.register_component(businesses.Restaurant)
    sim.world.gameobject_manager.register_component(businesses.School)
    sim.world.gameobject_manager.register_component(businesses.ShoemakerShop)
    sim.world.gameobject_manager.register_component(businesses.Supermarket)
    sim.world.gameobject_manager.register_component(businesses.TailorShop)
    sim.world.gameobject_manager.register_component(businesses.TattooParlor)
    sim.world.gameobject_manager.register_component(businesses.Tavern)
    sim.world.gameobject_manager.register_component(businesses.TaxiDepot)
    sim.world.gameobject_manager.register_component(businesses.University)

    # Occupation types
    sim.world.gameobject_manager.register_component(occupations.Apprentice)
    sim.world.gameobject_manager.register_component(occupations.Architect)
    sim.world.gameobject_manager.register_component(occupations.Bottler)
    sim.world.gameobject_manager.register_component(occupations.Bricklayer)
    sim.world.gameobject_manager.register_component(occupations.Builder)
    sim.world.gameobject_manager.register_component(occupations.Cashier)
    sim.world.gameobject_manager.register_component(occupations.Cook)
    sim.world.gameobject_manager.register_component(occupations.Dishwasher)
    sim.world.gameobject_manager.register_component(occupations.Groundskeeper)
    sim.world.gameobject_manager.register_component(occupations.HotelMaid)
    sim.world.gameobject_manager.register_component(occupations.Janitor)
    sim.world.gameobject_manager.register_component(occupations.Laborer)
    sim.world.gameobject_manager.register_component(occupations.Secretary)
    sim.world.gameobject_manager.register_component(occupations.Waiter)
    sim.world.gameobject_manager.register_component(occupations.WhiteWasher)
    sim.world.gameobject_manager.register_component(occupations.Busboy)
    sim.world.gameobject_manager.register_component(occupations.Stocker)
    sim.world.gameobject_manager.register_component(occupations.Seamstress)
    sim.world.gameobject_manager.register_component(occupations.Farmer)
    sim.world.gameobject_manager.register_component(occupations.Farmhand)
    sim.world.gameobject_manager.register_component(occupations.Miner)
    sim.world.gameobject_manager.register_component(occupations.Painter)
    sim.world.gameobject_manager.register_component(occupations.Banker)
    sim.world.gameobject_manager.register_component(occupations.BankTeller)
    sim.world.gameobject_manager.register_component(occupations.Grocer)
    sim.world.gameobject_manager.register_component(occupations.Bartender)
    sim.world.gameobject_manager.register_component(occupations.Concierge)
    sim.world.gameobject_manager.register_component(occupations.DaycareProvider)
    sim.world.gameobject_manager.register_component(occupations.Landlord)
    sim.world.gameobject_manager.register_component(occupations.Baker)
    sim.world.gameobject_manager.register_component(occupations.Cooper)
    sim.world.gameobject_manager.register_component(occupations.Barkeeper)
    sim.world.gameobject_manager.register_component(occupations.Milkman)
    sim.world.gameobject_manager.register_component(occupations.Plasterer)
    sim.world.gameobject_manager.register_component(occupations.Barber)
    sim.world.gameobject_manager.register_component(occupations.Butcher)
    sim.world.gameobject_manager.register_component(occupations.FireFighter)
    sim.world.gameobject_manager.register_component(occupations.Carpenter)
    sim.world.gameobject_manager.register_component(occupations.TaxiDriver)
    sim.world.gameobject_manager.register_component(occupations.BusDriver)
    sim.world.gameobject_manager.register_component(occupations.Blacksmith)
    sim.world.gameobject_manager.register_component(occupations.Woodworker)
    sim.world.gameobject_manager.register_component(occupations.StoneCutter)
    sim.world.gameobject_manager.register_component(occupations.Dressmaker)
    sim.world.gameobject_manager.register_component(occupations.Distiller)
    sim.world.gameobject_manager.register_component(occupations.Plumber)
    sim.world.gameobject_manager.register_component(occupations.Joiner)
    sim.world.gameobject_manager.register_component(occupations.Innkeeper)
    sim.world.gameobject_manager.register_component(occupations.Nurse)
    sim.world.gameobject_manager.register_component(occupations.Shoemaker)
    sim.world.gameobject_manager.register_component(occupations.Brewer)
    sim.world.gameobject_manager.register_component(occupations.TattooArtist)
    sim.world.gameobject_manager.register_component(occupations.Puddler)
    sim.world.gameobject_manager.register_component(occupations.Clothier)
    sim.world.gameobject_manager.register_component(occupations.Teacher)
    sim.world.gameobject_manager.register_component(occupations.Principal)
    sim.world.gameobject_manager.register_component(occupations.Tailor)
    sim.world.gameobject_manager.register_component(occupations.Molder)
    sim.world.gameobject_manager.register_component(occupations.Turner)
    sim.world.gameobject_manager.register_component(occupations.QuarryMan)
    sim.world.gameobject_manager.register_component(occupations.Proprietor)
    sim.world.gameobject_manager.register_component(occupations.Dentist)
    sim.world.gameobject_manager.register_component(occupations.Doctor)
    sim.world.gameobject_manager.register_component(occupations.Druggist)
    sim.world.gameobject_manager.register_component(occupations.Engineer)
    sim.world.gameobject_manager.register_component(occupations.FireChief)
    sim.world.gameobject_manager.register_component(occupations.InsuranceAgent)
    sim.world.gameobject_manager.register_component(occupations.Jeweler)
    sim.world.gameobject_manager.register_component(occupations.Lawyer)
    sim.world.gameobject_manager.register_component(occupations.Manager)
    sim.world.gameobject_manager.register_component(occupations.Mayor)
    sim.world.gameobject_manager.register_component(occupations.Mortician)
    sim.world.gameobject_manager.register_component(occupations.Owner)
    sim.world.gameobject_manager.register_component(occupations.Professor)
    sim.world.gameobject_manager.register_component(occupations.Optometrist)
    sim.world.gameobject_manager.register_component(occupations.Pharmacist)
    sim.world.gameobject_manager.register_component(occupations.PlasticSurgeon)
    sim.world.gameobject_manager.register_component(occupations.PoliceChief)
    sim.world.gameobject_manager.register_component(occupations.PoliceOfficer)
    sim.world.gameobject_manager.register_component(occupations.Realtor)
