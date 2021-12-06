# Assignment 7
# Simulate adding and deleting users to a company and the management of their group keys
#
# Author: Michael Bernhardt
# Last Updated: Nov. 19, 2021

# Constants
ADD = 'ADD'
DEL = 'DEL'
QUERY = 'QUERY'
NO_ID = '0'

#
# Node Class
#
class Node:
    
    # Constructor
    # Input: key - integer value of key
    #        user - string of a user name
    #        id - string of a node ID
    def __init__(self, key, user, id):
        self.key = key
        if id != NO_ID:
            self.key_id = id
        else:
            self.key_id = None
        if user != NO_ID:
            self.user = user
        else:
            self.user = None
        self.left = None
        self.right = None
        self.parent = None
    
    
    # Determine if a node is a leaf
    # Output: bool
    def is_leaf(self):
        return self.left is None and self.right is None
        
    
    # Get the sibling of a node
    # Requisite: Every node that is not a leaf has 2 children
    # Output: Node of sibling
    def get_sibling(self):
        if self.parent.left == self:
            return self.parent.right
        else:
            return self.parent.left
            
    
    # Determine if a node is a left child
    # Output: bool
    def is_left_child(self):
        return self.parent.left == self
           
           
    # Determine if a node is a right child
    # Output: bool
    def is_right_child(self):
        return self.parent.right == self
    
    
    # Print a Node as a string
    # Return: string representation of Node
    def __str__(self):
        retstr = ''
        if self.user:
            retstr += self.user + ' '
        else:
            retstr += self.key_id + ' '
            
        retstr += str(self.key)
        return retstr
        
    
    # Represent a Node as a string
    # Return: string representation of Node    
    def __repr__(self):
        retstr = ''
        if self.user:
            retstr += self.user + ' '
        else:
            retstr += self.key_id + ' '
            
        retstr += str(self.key)
        return retstr
        
        
#
# Tree class
#
class Tree:

    # Constructor
    # Input:    prime - Prime integer
    #           generator - Integer of primitive root being used
    #           user1, user2 - Strings of first two user names
    #           key1, key2 - Integer values of first two user keys
    #           key_id - String of first key ID for the blind key root
    def __init__(self, prime, generator, user1, key1, user2, key2, key_id):
        self.p = prime
        self.g = generator
        left_node = Node(key1, user1, key_id)
        right_node = Node(key2, user2, key_id)
        k0_val = mod_expo(generator, key1 * key2, prime)
        
        self.root = Node(k0_val, NO_ID, key_id)
        self.root.left = left_node
        self.root.right = right_node
        self.root.left.parent = self.root
        self.root.right.parent = self.root
        
    
    # Add a user to the tree
    # Input:    sponsor - String of user name that exists in tree already
    #           sponsor_key - Integer of new key sponsor is using
    #           new_user - String of name of new user
    #           new_user_key - Integer value of key the new user is using
    #           key_id - String of key ID that will be the parent of the 2 users
    def add_node(self, sponsor, sponsor_key, new_user, new_user_key, key_id):
        
        # Find the sponsor node and get the parent of the sponsor node   
        sponsor_node = self.__find_user(sponsor)
        parent = sponsor_node.parent
        
        new_key = mod_expo(self.g, sponsor_key * new_user_key, self.p)
        
        # Change sponsor_node key and key_id
        sponsor_node.key = sponsor_key
        sponsor_node.key_id = key_id
        
        # If sponsor a left child
        if sponsor_node.is_left_child():
            parent.left = Node(new_key, NO_ID, key_id)
            parent.left.parent = parent
            parent = parent.left
        
        # Else sponsor is right child
        else:
            parent.right = Node(new_key, NO_ID, key_id)
            parent.right.parent = parent
            parent = parent.right
        
        # Update new blind key's children
        parent.left = sponsor_node
        parent.left.parent = parent
        parent.right = Node(new_user_key, new_user, key_id)
        parent.right.parent = parent
        
        # Update blind key nodes in tree
        self.__update_nodes(parent.right)
        
    
    # Delete a user from the tree
    # Input:    user - user name to be deleted
    #           sibling_key - Integer of new key the deleted user's sibling will use
    #                         if the sibling is a user node
    def del_node(self, user, sibling_key):
        
        # Get the node to delete
        user_node = self.__find_user(user)
        
        # If sibling is leaf node
        sibling = user_node.get_sibling()
        
        parent = user_node.parent
        
        # If the sibling is another user node
        if sibling.is_leaf():
            
            # Change sibling key and update nodes above
            sibling.key = sibling_key
    
            # Move sibling up
            if parent.parent is not None:
                sibling.parent = parent.parent
                if parent.is_left_child():
                    parent.parent.left = sibling
                else:
                    parent.parent.right = sibling
                
                del user_node
            
            self.__update_nodes(sibling)
            
            
        # Sibling is blind key
        else:
        
            # Promote sibling blind key to parent
            if parent.parent is not None:
                sibling.parent = parent.parent
                if parent.is_left_child():
                    parent.parent.left = sibling
                else:
                    parent.parent.right = sibling
                
                parent = sibling
                del user_node
            
            # Update nodes above promoted parent
            self.__update_nodes(parent)
           
    
    # Update the keys of nodes that are ancestors of the given node
    # Input: user - Node of user to start updating
    def __update_nodes(self, user):
        curr = user.parent
        
        # Iterate back up Tree updating keys
        while curr is not None:
            curr.key = mod_expo(self.g, curr.left.key * curr.right.key, self.p)
            curr = curr.parent
    
    
    # Find a return a user in the tree
    # Input: user - String of user name to find
    def __find_user(self, user):
        curr = self.root
        
        # Use list as stack to hold nodes being passed
        stack = []
        
        # Loop until user found or no new node exists
        while True:
            if curr is not None:
                if curr.user == user.upper():
                    return curr
                stack.append(curr)
                curr = curr.left
            
            elif len(stack) > 0:
                curr = stack.pop()
                curr = curr.right
            
            else:
                break
        
    
    # Find the key value of a given blind key
    # Input: key_id - String of the key ID being queried
    # Output: Integer value of key ID's node
    def query(self, key_id):
        curr = self.root
        
        # Use list as stack to hold nodes being passed
        stack = []
        
        # Loop until node found or no new node exists
        while True:
            if curr is not None:
                if curr.key_id == key_id:
                    return curr.key
                stack.append(curr)
                curr = curr.left
            
            elif len(stack) > 0:
                curr = stack.pop()
                curr = curr.right
            
            else:
                break
        
        return NO_ID



# Get line of input from the console
# Output: List of strings read
def get_input_line():
    in_line = input()
    in_line = in_line.split(' ')
    return in_line
   

# Initialize the tree being used to store the users and their keys
# Input:    p - Integer prime
#           g - Integer generator
# Output: Tree with first two users in it
def init_tree(p, g):
    initial_users = input().split()
    user1, key1, user2, key2, key_id = initial_users
    key1, key2 = int(key1), int(key2)
    
    # Calculate shared key
    root_val = mod_expo(g, key1 * key2, p)
  
    ret_tree = Tree(p, g, user1, key1, user2, key2, key_id)
    
    return ret_tree
    
    
# Calculate modular exponentiation
# Input: integers base, exponent, mod
# Output: The calculated mod exponent
def mod_expo(base, exp, mod):

    # base case
    if exp == 0:
        return 1

    # even
    elif exp % 2 == 0:
        return (mod_expo(base, exp // 2, mod) * mod_expo(base, exp // 2, mod)) % mod

    # odd
    else:
        return (base * mod_expo(base, exp - 1, mod)) % mod


#
# Main Program
#
if __name__ == "__main__":

    print('             ======== Group Diffie Hellman ========')
    
    # Get prime and generator
    line_1 = input().split()
    prime, generator = int(line_1[0]), int(line_1[1])

    # Get number of commands to modify tree structure
    num_cmds = int(input())
    
    # Initialize the Tree with the first 2 users
    tree = init_tree(prime, generator)

    # Read each of the rest of the lines in
    for i in range(num_cmds - 1):
        line = get_input_line()
        cmd = line[0].upper()
        
        # Add user to Tree
        if cmd == ADD:
            add, sponsor, sponsor_key, user, user_key, key_id = line
            sponsor_key, user_key = int(sponsor_key), int(user_key)
            tree.add_node(sponsor, sponsor_key, user, user_key, key_id)
        
        # Delete user from Tree
        elif cmd == DEL:
            delete, user, sibling_key = line
            sibling_key = int(sibling_key)
            tree.del_node(user, sibling_key)
        
        # Query the key from a blind node in the tree
        elif cmd == QUERY:
            key_id = line[1]
            print(tree.query(key_id))
        
        # Error - Invalid first string in input
        else:
            print('error')