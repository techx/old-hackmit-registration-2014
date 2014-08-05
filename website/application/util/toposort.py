def toposort(collection, neighbor_func):
    collection = toposorted(collection, neighbor_func)

def toposorted(collection, neighbor_func):
    visited = set()
    order = []

    def visit(collection, item, neighbor_func):
        visited.add(item)
        for implied in neighbor_func(collection, item):
            if implied not in visited:
                visit(collection, implied, neighbor_func)
        order.append(item)

    for item in collection:
        if item not in visited:
            visit(collection, item, neighbor_func)
    return order

