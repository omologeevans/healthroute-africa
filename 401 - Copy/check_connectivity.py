#!/usr/bin/env python3
"""Check if the road network graph is fully connected"""

import sys
sys.path.insert(0, r'c:\Users\Ismail\Documents\Hamplus\401 - Copy')

from data_loader import create_graph
import networkx as nx

G = create_graph()

print(f"Graph stats:")
print(f"  Nodes: {G.number_of_nodes()}")
print(f"  Edges: {G.number_of_edges()}")
print()

# Check if graph is connected
if nx.is_connected(G):
    print("✅ Graph is FULLY CONNECTED - all LGAs are reachable from any other LGA!")
else:
    print("❌ Graph is NOT CONNECTED - some LGAs are isolated in separate components")
    
    components = list(nx.connected_components(G))
    print(f"\nNumber of separate components: {len(components)}")
    
    # Sort components by size
    components_sorted = sorted(components, key=len, reverse=True)
    
    for i, component in enumerate(components_sorted, 1):
        print(f"\nComponent {i}: {len(component)} LGAs")
        if len(component) <= 20:  # Show all if small
            for lga in sorted(component):
                print(f"  - {lga}")
        else:  # Show first 10 if large
            for lga in sorted(list(component))[:10]:
                print(f"  - {lga}")
            print(f"  ... and {len(component) - 10} more")
