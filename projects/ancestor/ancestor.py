def earliest_ancestor(ancestors, starting_node):
    #dictionary of ancestors
    parents = {}

    # loop -- if the elder is not in the parent dict set it to the first position, otherwise, just append it to the dict
    for elder in ancestors:
        if elder[1] not in parents:
            parents[elder[1]] = [elder[0]]
        else:
            parents[elder[1]].append(elder[0])

    # current_node = starting_node

    # if the starting node has no parents then we just leave now
    if starting_node not in parents:
        return -1
    
    current_elders = parents[starting_node]
    # visited = set()

    while True:
        new_elders = []
        for elder in current_elders:
            if elder in parents:
                new_elders = new_elders + parents[elder]
        
        if len(new_elders) == 0:
            return current_elders[0]
        else:
            current_elders = new_elders