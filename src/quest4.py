import re
from collections import namedtuple
from functools import cmp_to_key

from ecd import get_inputs, submit

Entry = namedtuple("Entry", ["id", "quest", "part", "time"]) # entry tuple because it makes life a bit easier

def parse_data(data: dict[str, str]) -> dict[str, dict[int, list[Entry]]]:
    ret = {}
    pattern = re.compile(r"id=(\d+) quest=(\d+) part=(\d+) time=(\d+)", re.IGNORECASE)
    for part, lines in data.items():
        d = {}
        for line in lines.splitlines():
            match = pattern.match(line)
            if match is None:
                raise ValueError(f"Invalid input line: {line!r}")
            entry = Entry(*map(int, match.groups()))
            d[entry.id] = d.get(entry.id, []) + [entry]
        ret[part] = d
    return ret
    

def part1(data: dict[int, list[Entry]]) -> int:
    return sum(i*t for i,t in enumerate(sorted(sum(e.time for e in v) for v in data.values()), 1))

def part2(data: dict[int, list[Entry]]) -> int:
    def cmp(x, y):
        if x[1] > y[1]:
            return -1
        if x[1] < y[1]:
            return 1
        return -1 if x[0] < y[0] else 1
    return sum(i*t for i,t in enumerate((t for t, _ in sorted(((sum(e.time for e in v), sum(1 for _ in v)) for v in data.values()), key=cmp_to_key(cmp))), 1))

# there is probably a more elegant way to calculate all this, but this is my solution
def part3(data: dict[int, list[Entry]]) -> int:
    # mutliple ways to do this
    # we can do it this way: for each id, calculate the time for each quest and part
    # then, based on this, calculate the points

    # calculate time for each quest and part
    d : dict[int, dict[int, dict[int, int]]] = {} # our core dictionary: for each quest, part, and id record the time
    for id, entries in data.items(): # for each recorded participant
        quest = None
        part = None
        for entry in sorted(entries, key=lambda e: (e.quest, e.part)): # sorting here is kinda important so we don't do weird stuff
            quest, part, time = entry.quest, entry.part, entry.time
            if d.get(quest) is None:
                d[quest] = {i: {} for i in range(1, 4)} # add new/unseen quest to result list
            if part != 1:
                time += d[quest][part-1][id] # add times for previous parts (we have the time for part 1 in part 2 as well)
            d[quest][part][id] = time
    
    # calculate the rankings
    scores = {} # final score tally per id
    for quest, parts in d.items():
        for part, ids in parts.items():
            max_points = part * 50 # part 1 = 50, part 2 = 100, part 3 = 150
            ranking = [(id, time) for id, time in sorted(ids.items(), key=lambda item: item[1])] # create the ranking by sorting the finishing times
            for i, (id, time) in enumerate(ranking):
                if i == 0 or time != ranking[i-1][1]: # points adjustments - includes ties
                    score = max(max_points-i, 0) # maximum points minus participants in front
                scores[id] = scores.get(id, 0) + score # add score to total scores
    
    # checksum calculation
    checksum = 0
    scores = sorted(scores.values(), reverse=True) # don't need the ids any more
    for i, score in enumerate(scores):
        if i == 0 or score != scores[i-1]:
            rank = i + 1 # rank includes ties - if same score, rank stays the same
        checksum += rank * score
    return checksum
    

if __name__ == "__main__":
    QUEST = 4
    data = parse_data(get_inputs(quest=QUEST, event=2026))
    submit(quest=QUEST, event=2026, part=1, answer=part1(data['1']))
    submit(quest=QUEST, event=2026, part=2, answer=part2(data['2']))
    submit(quest=QUEST, event=2026, part=3, answer=part3(data['3']))