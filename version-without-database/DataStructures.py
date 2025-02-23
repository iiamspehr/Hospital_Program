# This file is for defining and developing data types that are not already defined in Python.

import math
import heapq
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def delete(self, key):
        current = self.head
        if current and current.data == key:
            self.head = current.next
            return
        while current and current.next:
            if current.next.data == key:
                current.next = current.next.next
                return
            current = current.next

    def display(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return "Queue is empty"

    def is_empty(self):
        return len(self.items) == 0

    def display(self):
        print("Queue:", self.items)

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return "Stack is empty"

    def is_empty(self):
        return len(self.items) == 0

    def display(self):
        print("Stack:", self.items)

class HashMap:
    def __init__(self):
        self.size = 100
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[index].append([key, value])

    def get(self, key):
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]
        return None

    def display(self):
        for i, bucket in enumerate(self.table):
            if bucket:
                print(f"Bucket {i}: {bucket}")

# Advanced Graph Class with A* Algorithm
class Graph:
    def __init__(self):
        
        self.adjacency_list = {}  # Store connections
        self.node_types = {}      # Store node types

    def add_node(self, node_name, node_type="Default"):
        """Add a node with a specific type."""
        if node_name in self.adjacency_list:
            print(f"Node '{node_name}' already exists.")
            return
        self.adjacency_list[node_name] = []
        self.node_types[node_name] = node_type

    def remove_node(self, node_name):
        """Remove a node and all associated edges."""
        if node_name not in self.adjacency_list:
            print(f"Node '{node_name}' does not exist.")
            return
        # Remove the node
        del self.adjacency_list[node_name]
        self.node_types.pop(node_name, None)
        # Remove edges connected to this node
        for edges in self.adjacency_list.values():
            edges[:] = [edge for edge in edges if edge[0] != node_name]

    def add_edge(self, from_node, to_node, weight=1):
        """Add a directed edge between two nodes."""
        if from_node not in self.adjacency_list or to_node not in self.adjacency_list:
            print("Both nodes must exist to create an edge.")
            return
        self.adjacency_list[from_node].append((to_node, weight))

    def remove_edge(self, from_node, to_node):
        """Remove an edge between two nodes."""
        if from_node in self.adjacency_list:
            self.adjacency_list[from_node] = [
                edge for edge in self.adjacency_list[from_node] if edge[0] != to_node
            ]    
    def add_hospital(self, hospital_name):
        self.graph.add_node(hospital_name, "Hospital")
        self.display_city_graph()  # Redraw the graph

    def remove_hospital(self, hospital_name):
        self.graph.remove_node(hospital_name)
        self.display_city_graph()  # Redraw the graph



    def dijkstra(self, start, end):
        distances = {node: math.inf for node in self.adjacency_list}
        distances[start] = 0
        priority_queue = [(0, start)]

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.adjacency_list[current_node]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances[end]

    def a_star(self, start, end, heuristic):
        open_set = [(0, start)]
        g_score = {node: math.inf for node in self.adjacency_list}
        g_score[start] = 0

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == end:
                return g_score[end]

            for neighbor, weight in self.adjacency_list[current]:
                tentative_g_score = g_score[current] + weight
                if tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score, neighbor))

        return float('inf')
    

    def add_node(self, node, node_type="Default"):
        """Adds a node with a specified type."""
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []
            self.node_types[node] = node_type  # Store node type properly

    def visualize(self, ambulance_locations):
        """Displays the city graph with enhanced modern styling."""
        G = nx.DiGraph()
        for node, edges in self.adjacency_list.items():
            G.add_node(node)
            for neighbor, weight in edges:
                G.add_edge(node, neighbor, weight=weight)

        # Define modern colors based on node type
        color_map = {
            "Hospital": "#FF6347",   # Tomato Red
            "Home": "#32CD32",       # Lime Green
            "Access Point": "#1E90FF", # Dodger Blue
            "Ambulance": "#FFFF00",   # Yellow
            "Default": "#D3D3D3"     # Light Gray
        }
        node_colors = [color_map[self.node_types.get(node, "Default")] for node in G.nodes]

        # Customizing layout and appearance
        pos = nx.spring_layout(G, seed=42, scale=2)  # Spread out the nodes more
        plt.figure(figsize=(12, 8), facecolor="#1E1E2E")  # Dark Blue Background

        # Drawing nodes and edges
        nx.draw_networkx_nodes(
            G, pos, node_color=node_colors, node_size=1500, edgecolors="white", linewidths=1.5, alpha=0.9
        )
        nx.draw_networkx_edges(G, pos, edge_color="#A9A9A9", arrows=True, arrowstyle="->", alpha=0.6)

        # Adding node names outside the nodes
        labels = {node: node for node in G.nodes}
        nx.draw_networkx_labels(
            G, pos, labels, font_size=10, font_color="white", font_weight="bold", verticalalignment="bottom"
        )

        # Adding edge weights as labels
        edge_labels = {(u, v): d["weight"] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="white")

        # Title and display
        plt.title("City Graph Visualization", fontsize=16, color="white", pad=20)
        plt.axis("off")
        plt.show()


    def display_city_graph(self):
        """Displays the city graph with live ambulance locations."""
        print("Displaying City Graph...")
        
        # Get the latest locations of all ambulances
        ambulance_locations = {amb_id: amb.location for amb_id, amb in self.ambulances.items()}
        
        # Call visualize() with updated ambulance positions
        self.graph.visualize(ambulance_locations)



# Drug Management
class TreeNode:
    def __init__(self, drug_id, name=None, category=None, price=None, doses=None):
        self.drug_id = drug_id
        self.name = name
        self.category = category
        self.price = price
        self.doses = doses  # Number of doses available for the drug
        self.left = None
        self.right = None


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        
class DrugTree:
    def __init__(self):
        self.root = None

    def add_drug(self, drug_id, name, category, price, doses):
        if not self.root:
            self.root = TreeNode(drug_id, name, category, price, doses)
            print(f"Drug '{name}' added as the root.")
        else:
            self._add(self.root, drug_id, name, category, price, doses)

    def _add(self, node, drug_id, name, category, price, doses):
        if not node:
            return TreeNode(drug_id, name, category, price, doses)

        if drug_id < node.drug_id:
            if node.left is None:
                node.left = TreeNode(drug_id, name, category, price, doses)
            else:
                self._add(node.left, drug_id, name, category, price, doses)
        elif drug_id > node.drug_id:
            if node.right is None:
                node.right = TreeNode(drug_id, name, category, price, doses)
            else:
                self._add(node.right, drug_id, name, category, price, doses)
        else:
            print(f"Drug ID '{drug_id}' already exists. Skipping insertion.")

    def display_in_order(self):
        """Displays all drugs in ascending order based on their ID."""
        if not self.root:
            print("No drugs available.")
            return
        self._in_order_traversal(self.root)

    def _in_order_traversal(self, node):
        """Helper function for in-order traversal."""
        if node:
            self._in_order_traversal(node.left)
            print(f"ID: {node.drug_id}, Name: {node.name}, Category: {node.category}, Price: {node.price}, Doses: {node.doses}")
            self._in_order_traversal(node.right)
    def delete_drug(self, drug_id, drug_trie):
        """Deletes a drug from both DrugTree and Trie."""
        self.root, deleted_name = self._delete(self.root, drug_id)

        if deleted_name:
            drug_trie.delete(deleted_name)  # Remove from Trie
            print(f"Drug '{deleted_name}' removed from system.")

    def _delete(self, node, drug_id):
        """Recursive delete helper function."""
        if not node:
            return None, None

        if drug_id < node.drug_id:
            node.left, deleted_name = self._delete(node.left, drug_id)
        elif drug_id > node.drug_id:
            node.right, deleted_name = self._delete(node.right, drug_id)
        else:
            deleted_name = node.name  # Store name for Trie deletion

            if not node.left:
                return node.right, deleted_name
            if not node.right:
                return node.left, deleted_name

            successor = self._min_value_node(node.right)
            node.drug_id, node.name, node.category, node.price, node.doses = (
                successor.drug_id, successor.name, successor.category, successor.price, successor.doses
            )
            node.right, _ = self._delete(node.right, successor.drug_id)

        return node, deleted_name

    def _min_value_node(self, node):
        """Finds the node with the smallest value (leftmost node)."""
        current = node
        while current.left:
            current = current.left
        return current

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """Inserts a word into the Trie."""
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_end_of_word = True

    def delete(self, word):
        """Deletes a word from the Trie."""
        def _delete(node, word, depth):
            if not node:
                return None

            if depth == len(word):
                if node.is_end_of_word:
                    node.is_end_of_word = False
                if not node.children:
                    return None
                return node

            char = word[depth]
            node.children[char] = _delete(node.children.get(char), word, depth + 1)

            if not node.children and not node.is_end_of_word:
                return None
            return node

        _delete(self.root, word, 0)

    def search(self, prefix):
        """Returns a list of words that start with the given prefix."""
        current = self.root
        for char in prefix:
            if char not in current.children:
                return []  # Prefix not found
            current = current.children[char]
        return self._autocomplete(current, prefix)

    def _autocomplete(self, node, prefix):
        """Recursively collects all words starting from the given node."""
        results = []
        if node is None:  # Safety check to prevent accessing None
            return results

        if node.is_end_of_word:
            results.append(prefix)

        for char, child in node.children.items():
            results.extend(self._autocomplete(child, prefix + char))
        return results