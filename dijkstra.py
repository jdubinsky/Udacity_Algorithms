from Heap import Heap

def dijkstra(d, root):
    """ Returns a dict of the dist from the root to all other nodes in d.
        Implemented using a heap.
    """
    heap = Heap()
    heap.insert(root, 0)
    final_dist = {}
    while len(final_dist) != len(d):
        n = heap.remove_min()
        if n.name not in final_dist:
            # minimum value in heap is the shortest path to that node
            # lock it down
            final_dist[n.name] = n.value
            for child, dist in d[n.name].iteritems():
                total_dist = dist + n.value
                heap.insert(child, total_dist)

    return final_dist
