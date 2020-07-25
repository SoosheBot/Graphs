def earliest_ancestor(ancestors, starting_node):
    #dictionary of ancestors
    parents = {}

    # loop -- if the elder is not in the parent dict set it to the first position, otherwise, just append it to the dict
    for elder in ancestors:
        if elder[1] not in parents:
            parents[elder[1]] = [elder[0]]
        else:
            parents[elder[1]].append(elder[0])

    # if the starting node has no parents then we just leave now
    if starting_node not in parents:
        return -1
    
    current_gen = parents[starting_node]

    while True:
        new_gen = []
        for elder in current_gen:
            if elder in parents:
                new_gen = new_gen + parents[elder]
        
        if len(new_gen) == 0:
            return current_gen[0]
        else:
            current_gen = new_gen