import re
from collections import defaultdict
from dataclasses import dataclass

from ecd import get_inputs, submit


@dataclass
class Cloud:
    energy: int
    connections: set[str]

@dataclass
class Pulse:
    energy: int
    clouds: dict[str, int] # cloud and how often it is hit

def parse_data(data: dict[str, str]) -> dict[str, dict[str, Cloud]]:
    return {k: get_energy_grid(v) for k, v in data.items()}

def get_energy_grid(lines: str) -> dict[str, Cloud]:
    pattern = re.compile(r"id=([0-9]+), energy=([0-9]+), connections=(.*)", re.IGNORECASE)
    d = {}
    for line in lines.splitlines():
        match = pattern.match(line)
        if match is None:
            raise ValueError(f"Invalid input line: {line!r}")
        id, energy, connections = match.groups()
        connections = set(connections.split(','))
        d[id] = Cloud(int(energy), connections) # convert energy to int because we actually count that
    return d

# this is an approach you don't get to intuitively
# part 3 requires tracking multiple pulses, so i basically had to rewrite everything
# i had started with tracking how often the pulse hit a specific node, 
# which was fast since i only processed at most the number of nodes in the graph
# for part 1, i only used the data as a parameter
# for part 2, i added the energy parameter (free win)
# for part 3, i had to rewrite it all since it wasn't sufficient to track how often a node was hit, 
# but also by which pulse it was hit by ("Those new impulses propagated exactly as before, decreasing to 9, 8, 7 and so on.")
# i don't know how efficient this is, but it needs ~ 1s to process the complicated example
# hint for a very clean solution i saw online: instead of pulses, track the charge (1..10) and count for each cloud
# that way you only have one data structure you have to work with beside energies (which are the live clouds)
def impulse(data:dict[str, Cloud], energy: int, start: str, explosion_limit: float | None = None) -> int:
    """Function to track pulses along the grid

    Args:
        data (dict[str, Cloud]): Input data with cloud id as the key and energy and connections as values
        energy (int): energy of the first pulse
        start (str): the id of the cloud to start from
        explosion_limit (float, optional): energy limit at which a cloud explodes. Defaults to None.

    Returns:
        int: The total energy remaining in the system after all pulses have finished propagating
    """
    energies = {k: v for k,v in data.items()} # make a full copy for housekeeping
    first_pulse = Pulse(energy, defaultdict(lambda: 0))
    first_pulse.clouds[start] = 1 # first cloud is hit with one pulse of energy
    pulses = [first_pulse] # list of pulses we send through the grid
    while pulses: # while pulses are active
        next_pulses: list[Pulse] = [] # list of next pulses
        for pulse in pulses:
            next_pulse = Pulse(pulse.energy - 1, defaultdict(lambda: 0))
            # propagate the pulse through the grid
            for q, p in sorted(pulse.clouds.items()):
                for v in energies[q].connections:
                    next_pulse.clouds[v] += p
            # add the energy this pulse added to each cloud
            energies = {k: Cloud(c.energy + pulse.energy * pulse.clouds[k], c.connections) for k, c in energies.items()}
            # if the pulse has more juice, continue
            if next_pulse.energy > 0:
                next_pulses.append(next_pulse)
        pulses = next_pulses

        # part 3: explosion logic
        # for part 1 and 2, you don't need to update the connections in the grid and add new pulses
        # since the default value of explosion_limit is infinite, this only copies the energy dict around
        # in short, if you remove this section, the results for part 1 and part 2 are still correct
        if explosion_limit is not None: 
            new_energies: dict[str, Cloud] = {}
            exploded : set[str] = set()
            # explode clouds
            for k, c in energies.items():
                if c.energy < explosion_limit:
                    new_energies[k] = c
                else:
                    clouds = defaultdict(lambda: 0)
                    for v in c.connections:
                        clouds[v] = 1
                    pulses.append(Pulse(10, clouds)) # add a new pulse with energy of 10
                    exploded.add(k)
            # remove exploded clouds from pulses
            for k in exploded:
                for pulse in pulses:
                    if k in pulse.clouds:
                        del pulse.clouds[k]
            # remove exploded clouds from connections so we don't needlessly send them any more energy
            for c in new_energies.values():
                c.connections = c.connections.difference(exploded)
            energies = new_energies
    return sum(c.energy for c in energies.values())

def part1(data: dict[str, Cloud]) -> int:
    id, _ = max(data.items(), key=lambda d: len(d[1].connections))
    return impulse(data, 5, id)

def part2(data: dict[str, Cloud]) -> int:
    id, _ = max(data.items(), key=lambda d: len(d[1].connections))
    return impulse(data, 10, id)

def part3(data: dict[str, Cloud], explosion_limit: float = 1000000) -> int:
    starts = {v: impulse(data, 10, v, explosion_limit) for v in data}
    return max(starts.values())

if __name__ == "__main__":
    QUEST = 7
    data = parse_data(get_inputs(quest=QUEST, event=2026))
    submit(quest=QUEST, event=2026, part=1, answer=part1(data['1']))
    submit(quest=QUEST, event=2026, part=2, answer=part2(data['2']))
    submit(quest=QUEST, event=2026, part=3, answer=part3(data['3']))