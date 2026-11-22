from collections import defaultdict

from ecd import get_inputs, submit


def parse_data(data: dict[str, str]):
    return {k: build_graph(v.splitlines()) for k, v in data.items()}

def build_graph(lines: list[str]) -> dict[str,list[str]]:
    edges = {}
    for line in lines:
        v, e = line.split(':')
        edges[v] = e.split(',')
    return edges

def invert_graph(edges: dict[str, list[str]]) -> dict[str,list[str]]:
    inverted = defaultdict(list)
    for v, vs in edges.items():
        for w in vs:
            inverted[w].append(v)
    return inverted

def bfs(graph: dict[str, list[str]], start: str) -> set[str]:
    visited = {start}
    queue = {start}
    while queue:
        curr = queue.pop()
        visited.add(curr)
        queue = queue.union({v for v in graph.get(curr, []) if v not in visited})
    # remove the start from the set of visited nodes because it's not part of the solution
    visited.remove(start)
    return visited

def part1(data: dict[str,list[str]]) -> int:
    # some version of bfs
    return len(bfs(data, 'NULL'))

def part2(data: dict[str,list[str]]) -> int:
    # same as part 1, but with inverted graphs
    edges = invert_graph(data)
    return len(bfs(edges, 'NULL'))

def part3(data: dict[str,list[str]]) -> int:
    # same as part2, but this time we do three searches
    edges = invert_graph(data)
    null_contain: dict[str, set[str]] = {}
    # find the vertices leading from each of the nulls
    for nullv in ['NULLv1', 'NULLv2', 'NULLv3']:
        null_contain[nullv] = bfs(edges, nullv)
    # for the result, find all vertices that use at least two of the nulls
    # we have to do a pairwise comparison
    res: set[str] = set()
    res = (
        null_contain['NULLv1'].intersection(null_contain['NULLv2'])
        .union(
            null_contain['NULLv1'].intersection(null_contain['NULLv3'])
        )
        .union(
            null_contain['NULLv2'].intersection(null_contain['NULLv3'])
        )
    )
    # return the result
    return len(res)

if __name__ == "__main__":
    QUEST = 6
    data = parse_data(get_inputs(quest=QUEST, event=2026))
    submit(quest=QUEST, event=2026, part=1, answer=part1(data['1']))
    submit(quest=QUEST, event=2026, part=2, answer=part2(data['2']))
    submit(quest=QUEST, event=2026, part=3, answer=part3(data['3']))