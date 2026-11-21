from ecd import get_inputs, submit


def parse_data(data: dict[str, str]):
    return {k: [[(x[0], x[1], x[2]) for x in line.split()] for line in v.split('\n')] for k, v in data.items()}


"""
I have to admit I got here iteratively, and this is not how you would approach the problem starting from part 1.
Parts 2 and 3 are generalizations of part 1, so the solution works for all three parts.
After writing this, I realized that the question is asking for a simple topological graph sort, which is what you see here.
"""
def checksum(line):
    # dictionary representing the graph, where the key is the item and the value is a set of items that are "harder" than the key
    d: dict[str, set[str]] = {}
    # build the graph, add edges from the hard item to the soft item (which is the direction of the solution)
    for left, cmp, right in line:
        ls = d.get(left, set())
        rs = d.get(right, set())
        if cmp == '<':
            ls.add(right)
        else:
            rs.add(left)
        d[left] = ls
        d[right] = rs
    # topological sort (the task implies that there is only one solution)
    # the queue contains the items that have no incoming edges (no items are harder than them)
    queue = [k for k, v in d.items() if len(v) == 0]
    s = "" # solution: the number that is built from the items in the order they are removed from the graph
    while queue:
        # get the next item in the queue (no incoming edges)
        item = queue.pop(0)
        s += item # solution: add item to the solution
        # remove the item from the dictionary
        del d[item]
        # remove the item from the sets of the other items (incoming edges)
        for k, v in d.items():
            if item in v:
                v.remove(item)
                # if the set is empty, add the item to the queue
                if len(v) == 0:
                    queue.append(k)
    return int(s)

def part1(data) -> int:
    return sum(checksum(line) for line in data)

def part2(data):
    return sum(checksum(line) for line in data)

def part3(data):
    return sum(checksum(line) for line in data)

if __name__ == "__main__":
    data = parse_data(get_inputs(quest=2, event=2026))
    submit(quest=2, event=2026, part=1, answer=part1(data['1']))
    submit(quest=2, event=2026, part=2, answer=part2(data['2']))
    submit(quest=2, event=2026, part=3, answer=part3(data['3']))