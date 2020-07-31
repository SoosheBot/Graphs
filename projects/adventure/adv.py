from room import Room
from player import Player
from world import World
from util import Stack, Queue


import random
from ast import literal_eval



# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "projects/adventure/maps/test_line.txt"
# map_file = "projects/adventure/maps/test_cross.txt"
# map_file = "projects/adventure/maps/test_loop.txt"
# map_file = "projects/adventure/maps/test_loop_fork.txt"
# map_file = "projects/adventure/maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited = {}
backtrack_path = []
directions = {"n": "s", "e": "w", "s": "n", "w": "e"}

#begin in first room -- look for exits
visited[player.current_room.id] = player.current_room.get_exits()

#traverse the room -- when we start off, the number of rooms we have visited will be less than the total number of rooms
while len(visited) < len(room_graph) - 1:
    if player.current_room.id not in visited:
        #add the room to the visited dict and then look for its exits
        visited[player.current_room.id]  = player.current_room.get_exits()

        #remove exits one at a time so we don't backtrack before we are all the way done
        visited[player.current_room.id].remove(backtrack_path[1])

    #When we finally run out of rooms we can backtrack
    while len(visited[player.current_room.id]) == 0:
        #go back from the way we came in
        backtrack = backtrack_path.pop()

        #like Theseus and his ball of yarn, we wind our way back the way we came
        traversal_path.append(backtrack)
        #move the player in the opposite direction from whence they came
        player.travel(backtrack)
    
    #find the first available exit -- which is the one that was most recently added to the list of room entry/exits -- and then update the path
    journey = visited[player.current_room.id].pop()
    traversal_path.append(journey)

    #now we have to update the backtracking path too, since we're taking all of the things out of its basket
    backtrack_path.append(directions[journey])

    #move the player in that direction and backtrack along
    player.travel(journey)
        

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"There are {len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True: 
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
