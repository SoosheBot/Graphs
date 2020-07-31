import random
from util import Queue  # These may come in handy

class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    # initializing with the last known id at 0 and open dicts for users and friendships with these users
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    # If your user id equals the id of the friend you're trying to make, you'll get an error, and if the friend's id already exists in the self.friendships dict OR your id is in the friendship dict of your friend, then you get a message that you're already connected
    #If ALL of that checks out, then you add the friend's id to your dict, and your id gets added to your friend's dict
    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship. Therefore creates an undirected graph. Makes TWO friendships
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    #To actually add users to your dict
    #--make sure you're increasing the ids incrementally to glom on to the latest user
    #--have that last id in your users dict equal to the user's name
    #--set your friendships dict with the last id
    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    # Witchcraft
    def fisher_yates_shuffle(self,l):
        for i in range(0, len(l)):
            random_index = random.randint(i, len(l) -1)
            l[random_index], l[i] = l[i], l[random_index]


    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships as arguments.
        Creates that number of users and a randomly distributed friendships between those users.
        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        for i in range(num_users):
            self.add_user(f'user {i}')
        
        # Add users
        for user in range(num_users):
            self.add_user(user)
        # starts at 1, up to and including num_users

        # * Hint 1: To create N random friendships,
        # # you could create a list with all possible friendship combinations of user ids,
        friendship_combinations = []
        # O(n^2)
        for user in range(1, self.last_id + 1):
            for friend in range(user + 1, self.last_id + 1):
                friendship_combinations.append((user, friend))
        
        # shuffle the list
        self.fisher_yates_shuffle(friendship_combinations)

        # then grab the first N elements from the list.
        total_friendships = num_users * avg_friendships

        friends_to_make = friendship_combinations[:(total_friendships // 2)]

        # Create friendships
        for friendship in friends_to_make:
            self.add_friendship(friendship[0], friendship[1])


    def get_all_social_paths(self, user_id): 
        q = Queue()
        visited = {}
        q.enqueue([user_id])

        while q.size() > 0:
            
            current_path = q.dequeue()
            current_node = current_path[-1]

            if current_node not in visited:
                visited[current_node] = current_path

                friends = self.friendships[current_node]

                for friend in friends:
                    friend_path = current_path.copy()
                    friend_path.append(friend)

                    q.enqueue(friend_path)
        return visited

if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)


