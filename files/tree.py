import os
class Node:
    def __init__(self, value=None):
        self.value = value
        self.child = None

class LinearTree:
    def __init__(self):
        self.root = None
    
    def add_node(self, value):
        new_node = Node(value)

        if not self.root:
            self.root = new_node

        else:
            current = self.root
            while current.child:
                current = current.child
            current.child = new_node
    
    def cut_node(self, value):
        if self.root.value == value:
            self.root = self.root.child

        elif self.root:
            current = self.root
            while current.child:
                if current.child.value == value:
                    current.child = current.child.child
                    break
                current = current.child
    
    def delete_node(self, value):
        if self.root.value == value:
            self.root = None

        elif self.root:
            current = self.root
            while current.child:
                if current.child.value == value:
                    current.child = None
                    break
                current = current.child
        
    def traverse(self):
        current = self.root
        while current:
            print(current.value, end=' -> ') if current.child else print(current.value, '\n')
            current = current.child

tree = LinearTree()
while True:
    os.system("cls" if os.name == "nt" else "clear")
    tree.traverse()
    user_input = input("[n]ew node, [c]ut node, [d]elete node, [q]uit: ")
    if user_input == "n":
        new_node = input("new node: ")
        tree.add_node(new_node)
    elif user_input == "c":
        to_cut_node = input("cut node: ")
        tree.cut_node(to_cut_node)
    elif user_input == "d":
        delete_node = input("delete node: ")
        tree.delete_node(delete_node)
    elif user_input == "q":
        break
    else:
        print("Invalid input. Please try again.")