import csv
from heapq import *

def dijkstra(d, root):
    """ Dijkstra using heapq library.
        Ordered by shortest distance, then number of hops
    """
    heap = []
    heappush(heap, (0, 0, root))
    final_dist = {}
    while len(heap) > 0:
        dist, hops, n = heappop(heap)
        if n not in final_dist:
            final_dist[n] = (dist, hops)
            for child, child_dist in d[n].iteritems():
                total_dist = dist + child_dist
                total_hops = hops + 1
                heappush(heap, (total_dist, total_hops, child))

    return final_dist

def dijkstra_hops(d, root):
    """ Dijkstra using heapq library.
        Ordered by shortest number of hops
    """
    heap = []
    heappush(heap, (0, root))
    final_dist = {}
    while len(heap) > 0:
        hops, n = heappop(heap)
        if n not in final_dist:
            final_dist[n] = hops
            for child, child_dist in d[n].iteritems():
                total_hops = hops + 1
                heappush(heap, (total_hops, child))

    return final_dist

# make_link from previous modules
# taken from udacity cs215
def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        (G[node1])[node2] = 0
    (G[node1])[node2] += 1
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        (G[node2])[node1] = 0
    (G[node2])[node1] += 1
    return G

# edited from udacity cs215 code
# returns a graph with the count of how many comics any pair of characters appeared in together
def read_marvel_data(filename):
    bipartite_graph = {}
    characters = set()
    with open(filename) as csvf:
        reader = csv.reader(csvf, delimiter='\t')
        for char, comic in reader:
            if char not in characters:
                characters.add(char)
            make_link(bipartite_graph, char, comic)

    char_list = {}
    for char1 in characters:
        for book in bipartite_graph[char1]:
            for char2 in bipartite_graph[book]:
                if char1 < char2:
                    make_link(char_list, char1, char2)

    return char_list

def add_weight(d):
    # create new object because python passes things as object references!
    # and dictionaries are mutable
    d_new = {}
    for c1, d2 in d.iteritems():
        if c1 not in d_new:
            d_new[c1] = {}
        for c2 in d2:
            d_new[c1][c2] = 1.0 / d[c1][c2]

    return d_new

def count_hop_diffs(g, l):
    count = 0
    for c1 in l:
        char_dist = dijkstra(g, c1)
        hops_dist = dijkstra_hops(g, c1)
        for c2 in char_dist:
            if c1 == c2: continue
            # shortest number of hops from c1 shortest distance to c2
            _, shortest_dist_hops_count = char_dist[c2]
            # shortest number of hops from c1 to c2
            shortest_hops_count = hops_dist[c2]
            if shortest_dist_hops_count != shortest_hops_count:
                count += 1

    return count

# basic test of dijkstra
def test():
    d = {}
    d['a'] = {}
    d['b'] = {}
    d['e'] = {}
    d['c'] = {}
    d['d'] = {}
    d['f'] = {}
    d['a']['b'] = 5
    d['b']['a'] = 5
    d['b']['c'] = 6
    d['c']['b'] = 6
    d['b']['e'] = 7
    d['e']['b'] = 7
    d['e']['f'] = 2
    d['f']['e'] = 2
    d['c']['d'] = 1
    d['d']['c'] = 1
    d['d']['e'] = 3
    d['e']['d'] = 3
    d['b']['d'] = 7
    d['d']['b'] = 7
    print dijkstra(d, 'a')

if __name__ == "__main__":
    marvel_graph_unweighted = read_marvel_data('marvel_graph.tsv')
    marvel_graph_weighted = add_weight(marvel_graph_unweighted)
    print count_hop_diffs(marvel_graph_weighted, [
                                'SPIDER-MAN/PETER PAR',
                                'GREEN GOBLIN/NORMAN ',
                                'WOLVERINE/LOGAN ',
                                'PROFESSOR X/CHARLES ',
                                'CAPTAIN AMERICA'
                                ])
