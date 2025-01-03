import networkx as nx
import matplotlib.pyplot as plt
import math


def parse_circuit(filename: str):
    graph = nx.DiGraph()  # Directed graph for circuit
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("#") or not line:  # Skip comments and empty lines
                continue
            
            tokens = line.split()
            node_type, node_id = tokens[0], tokens[1]
            inputs = tokens[2:]
            
            graph.add_node(node_id, type=node_type, delay=get_delay(node_type))
            for input_node in inputs:
                graph.add_edge(input_node, node_id)
    
    return graph


def get_delay(node_type: str) -> float:
    delays = {
        "INPUT": 0.0,
        "OUTPUT": 0.0,
        "ADD": 1.0,
        "MUL": 1.0,
        "REG": 0.2,
    }
    return delays.get(node_type, 1.0)  # Default delay for unknown types


def find_critical_path(graph: nx.DiGraph):
    longest_path = []
    max_delay = 0.0
    path_delays = {}

    # Topological sort to process nodes
    for node in nx.topological_sort(graph):
        # Get delay of incoming edges
        incoming_delays = [
            path_delays[predecessor] + graph.nodes[predecessor]['delay']
            for predecessor in graph.predecessors(node)
        ]
        path_delays[node] = max(incoming_delays, default=0) + graph.nodes[node]['delay']

        # Update longest path if needed
        if path_delays[node] > max_delay:
            max_delay = path_delays[node]
            longest_path = nx.dag_longest_path(graph, weight='delay')

    return longest_path, max_delay


def visualize_circuits(circuit_graphs: list, critical_paths: list, circuit_names: list):
    num_circuits = len(circuit_graphs)
    grid_cols = math.ceil(math.sqrt(num_circuits))  # Number of columns
    grid_rows = math.ceil(num_circuits / grid_cols)  # Number of rows

    plt.figure(figsize=(15, 5 * grid_rows))  # Dynamic figure size based on rows and columns

    for i, (graph, critical_path, name) in enumerate(zip(circuit_graphs, critical_paths, circuit_names), 1):
        plt.subplot(grid_rows, grid_cols, i)  # Create a subplot for each circuit
        pos = nx.spring_layout(graph)

        # Draw all nodes and edges
        nx.draw(graph, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=700, font_size=10)

        # Highlight critical path
        critical_edges = [(critical_path[j], critical_path[j+1]) for j in range(len(critical_path) - 1)]
        nx.draw_networkx_edges(graph, pos, edgelist=critical_edges, edge_color="red", width=2)
        
        # Annotate nodes in the critical path
        for node in critical_path:
            x, y = pos[node]
            plt.text(x, y + 0.05, f"{node}\n({graph.nodes[node]['delay']} tu)", fontsize=8, color="black", ha="center")

        plt.title(f"Circuit: {name} (Critical Path in Red)", fontsize=12)

    plt.tight_layout()
    plt.show()


def main():
    # Circuit files
    circuit_files = ["cir1.txt", "cir2.txt", "cir3.txt", "cir_4.txt", "cir_5.txt"]
    circuit_graphs = []
    critical_paths = []
    circuit_names = []

    for filename in circuit_files:
        print(f"\nAnalyzing Circuit: {filename}")
        
        # Parse and analyze circuit
        graph = parse_circuit(filename)
        critical_path, total_delay = find_critical_path(graph)

        # Print results
        print(f"Critical Path: {' -> '.join(critical_path)}")
        print(f"Total Delay: {total_delay/2:.2f} time units")
        print("Components in Critical Path with Delays:")
        for node in critical_path:
            delay = graph.nodes[node]['delay']
            print(f"  - {node}: {delay} time units")

        
        # Store results for visualization
        circuit_graphs.append(graph)
        critical_paths.append(critical_path)
        circuit_names.append(filename)

    # Visualize all circuits in one figure
    visualize_circuits(circuit_graphs, critical_paths, circuit_names)


if __name__ == "__main__":
    main()
