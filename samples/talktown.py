#!/usr/bin/python3

"""
Talk of the Town Sample
=======================

This samples shows Neighborly simulating a Talk of the Town-style town. It uses the
talktown plugin included with Neighborly and simulates 140 years of town history.

"""

import time

from neighborly import NeighborlyConfig, SimDateTime
from neighborly.exporter import export_to_json
from neighborly.settlement import Settlement
from neighborly.simulation import Neighborly

EXPORT_WORLD = True

sim = Neighborly(
    NeighborlyConfig.parse_obj(
        {
            "seed": "Apples",
            "plugins": [
                "neighborly.plugins.defaults.all",
                "neighborly.plugins.talktown",
            ],
            "logging": {
                "logging_enabled": True,
                "log_level": "DEBUG",
            },
        }
    )
)

if __name__ == "__main__":
    st = time.time()
    sim.run_for(140)
    elapsed_time = time.time() - st

    print(f"World Year: {sim.world.resource_manager.get_resource(SimDateTime).year}")
    print(f"Settlement: {sim.world.resource_manager.get_resource(Settlement).name}")
    print("Execution time: ", elapsed_time, "seconds")

    if EXPORT_WORLD:
        with open(f"neighborly_{sim.config.seed}.json", "w") as f:
            f.write(export_to_json(sim))
