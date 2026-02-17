"""
HealthRoute Africa - Priority-Weighted Dijkstra's Algorithm
Implements medical supply routing with priority based on malaria prevalence and urgency.

Algorithm Complexity: O((E+V) log V)
- E: Number of edges (roads)
- V: Number of vertices (cities)
- Uses heapq for min-priority queue operations
"""

import heapq
import networkx as nx
from typing import Dict, List, Tuple, Optional


def calculate_priority_weight(distance: float, prevalence: float, urgency: float) -> float:
    """
    Calculate priority weight for routing.
    
    Formula: W = Distance / (Prevalence × Urgency)
    
    Lower weight = Higher priority
    - Higher prevalence increases priority (lower weight)
    - Higher urgency increases priority (lower weight)
    - Longer distance decreases priority (higher weight)
    
    Args:
        distance: Road distance in kilometers
        prevalence: Malaria prevalence rate (0.0 to 1.0)
        urgency: Urgency multiplier (0.1 to 10.0)
        
    Returns:
        Priority weight (lower is better)
    """
    # Prevent division by zero
    if prevalence == 0 or urgency == 0:
        return float('inf')
    
    return distance / (prevalence * urgency)


def priority_dijkstra(graph: nx.Graph, 
                     source: str, 
                     destination: str,
                     urgency: float = 1.0) -> Tuple[Optional[List[str]], float, float]:
    """
    Priority-Weighted Dijkstra's Algorithm for medical supply routing.
    
    Finds the optimal path considering both distance and malaria prevalence.
    
    Complexity Analysis:
    - Initialization: O(V)
    - Main loop: O(V) iterations
    - Each iteration: O(log V) for heap operations
    - Edge relaxation: O(E) total across all iterations
    - Total: O((E+V) log V)
    
    Args:
        graph: NetworkX graph with city nodes and road edges
        source: Starting city name
        destination: Target city name
        urgency: Urgency multiplier (default 1.0, range 0.1-10.0)
        
    Returns:
        Tuple of (path, total_distance, priority_score)
        - path: List of cities in optimal route (None if no path exists)
        - total_distance: Total distance in kilometers
        - priority_score: Final priority weight
    """
    # Validate inputs
    if source not in graph.nodes or destination not in graph.nodes:
        return None, float('inf'), float('inf')
    
    if source == destination:
        return [source], 0.0, 0.0
    
    # Initialize data structures
    # Priority queue: (priority_weight, current_distance, current_node)
    pq = [(0.0, 0.0, source)]
    
    # Best known priority weights to each node
    best_weights = {node: float('inf') for node in graph.nodes}
    best_weights[source] = 0.0
    
    # Best known distances to each node
    distances = {node: float('inf') for node in graph.nodes}
    distances[source] = 0.0
    
    # Track predecessors for path reconstruction
    predecessors = {node: None for node in graph.nodes}
    
    # Track visited nodes
    visited = set()
    
    # Main Dijkstra loop - O(V) iterations
    while pq:
        # Extract minimum - O(log V)
        current_weight, current_distance, current_node = heapq.heappop(pq)
        
        # Skip if already visited (optimization)
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        # Early termination if destination reached
        if current_node == destination:
            break
        
        # Skip if we've found a better path already
        if current_weight > best_weights[current_node]:
            continue
        
        # Get current node's malaria prevalence
        current_prevalence = graph.nodes[current_node].get('prevalence', 0.5)
        
        # Explore neighbors - O(E) total across all iterations
        for neighbor in graph.neighbors(current_node):
            if neighbor in visited:
                continue
            
            # Get edge weight (road distance)
            edge_data = graph.get_edge_data(current_node, neighbor)
            road_distance = edge_data.get('distance', 0)
            
            # Get neighbor's malaria prevalence
            neighbor_prevalence = graph.nodes[neighbor].get('prevalence', 0.5)
            
            # Use average prevalence for this edge
            avg_prevalence = (current_prevalence + neighbor_prevalence) / 2
            
            # Calculate priority weight for this edge
            edge_priority = calculate_priority_weight(road_distance, avg_prevalence, urgency)
            
            # Calculate new cumulative values
            new_distance = current_distance + road_distance
            new_weight = current_weight + edge_priority
            
            # Relaxation step
            if new_weight < best_weights[neighbor]:
                best_weights[neighbor] = new_weight
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_node
                
                # Add to priority queue - O(log V)
                heapq.heappush(pq, (new_weight, new_distance, neighbor))
    
    # Reconstruct path
    if predecessors[destination] is None and destination != source:
        # No path exists
        return None, float('inf'), float('inf')
    
    path = []
    current = destination
    while current is not None:
        path.append(current)
        current = predecessors[current]
    
    path.reverse()
    
    return path, distances[destination], best_weights[destination]


def get_route_details(graph: nx.Graph, path: List[str]) -> List[Dict]:
    """
    Get detailed information about each segment of the route.
    
    Args:
        graph: NetworkX graph
        path: List of cities in the route
        
    Returns:
        List of dictionaries with segment details
    """
    if not path or len(path) < 2:
        return []
    
    details = []
    
    for i in range(len(path) - 1):
        current = path[i]
        next_city = path[i + 1]
        
        # Get edge data (may be None if cities aren't directly connected)
        edge_data = graph.get_edge_data(current, next_city)
        
        # If no direct edge, calculate distance using Dijkstra
        if edge_data is None:
            # Cities not directly connected, find shortest path
            try:
                temp_path, temp_dist, _ = priority_dijkstra(graph, current, next_city, urgency=1.0)
                distance = temp_dist if temp_path else 0
            except:
                distance = 0
        else:
            distance = edge_data.get('distance', 0)
        
        # Get city data
        current_data = graph.nodes[current]
        next_data = graph.nodes[next_city]
        
        details.append({
            'from': current,
            'to': next_city,
            'distance': distance,
            'from_prevalence': current_data.get('prevalence', 0),
            'to_prevalence': next_data.get('prevalence', 0),
        })
    
    return details


def calculate_tour_metrics(graph: nx.Graph, path: List[str], urgency: float) -> Tuple[float, float]:
    """
    Calculate total distance and priority score for a complete tour.
    
    Args:
        graph: NetworkX graph
        path: List of cities in the tour
        urgency: Urgency multiplier
        
    Returns:
        Tuple of (total_distance, total_priority_score)
    """
    if not path or len(path) < 2:
        return 0.0, 0.0
    
    total_distance = 0.0
    total_priority = 0.0
    
    for i in range(len(path) - 1):
        current = path[i]
        next_city = path[i + 1]
        
        # Get edge data
        edge_data = graph.get_edge_data(current, next_city)
        if not edge_data:
            continue
            
        distance = edge_data.get('distance', 0)
        total_distance += distance
        
        # Calculate priority weight for this segment
        current_prevalence = graph.nodes[current].get('prevalence', 0.5)
        next_prevalence = graph.nodes[next_city].get('prevalence', 0.5)
        avg_prevalence = (current_prevalence + next_prevalence) / 2
        
        priority_weight = calculate_priority_weight(distance, avg_prevalence, urgency)
        total_priority += priority_weight
    
    return total_distance, total_priority


def optimal_tour_routing(graph: nx.Graph, 
                        start_city: str,
                        urgency: float = 1.0) -> Tuple[Optional[List[str]], float, float]:
    """
    Optimal Tour Routing using Nearest Neighbor TSP approximation.
    
    Starting from start_city, repeatedly visit the nearest unvisited city
    based on priority-weighted distance until all cities are visited.
    
    Complexity: O(V²) where V is the number of cities
    
    Args:
        graph: NetworkX graph with city nodes and road edges
        start_city: Starting city name
        urgency: Urgency multiplier (default 1.0, range 0.1-10.0)
        
    Returns:
        Tuple of (path, total_distance, priority_score)
        - path: List of cities in tour order (None if start_city invalid)
        - total_distance: Total distance in kilometers
        - priority_score: Total priority weight
    """
    # Validate input
    if start_city not in graph.nodes:
        return None, float('inf'), float('inf')
    
    # Initialize
    all_cities = set(graph.nodes())
    visited = {start_city}
    path = [start_city]
    current_city = start_city
    
    # Visit all remaining cities - O(V) iterations
    while len(visited) < len(all_cities):
        best_next = None
        best_weight = float('inf')
        
        # Find nearest unvisited city - O(V) per iteration
        for neighbor in graph.nodes():
            if neighbor in visited:
                continue
            
            # Try to find shortest path to this unvisited city
            try:
                # Use priority_dijkstra to find best path from current to neighbor
                temp_path, temp_dist, temp_weight = priority_dijkstra(
                    graph, current_city, neighbor, urgency
                )
                
                if temp_path and temp_weight < best_weight:
                    best_weight = temp_weight
                    best_next = neighbor
            except:
                continue
        
        # If no reachable city found, break
        if best_next is None:
            break
        
        # Move to the nearest city
        visited.add(best_next)
        path.append(best_next)
        current_city = best_next
    
    # Calculate tour metrics
    total_distance, total_priority = calculate_tour_metrics(graph, path, urgency)
    
    return path, total_distance, total_priority


def priority_tour_routing(graph: nx.Graph,
                         start_city: str,
                         urgency: float = 1.0) -> Tuple[Optional[List[str]], float, float]:
    """
    Priority-Based Tour Routing using greedy prevalence-based selection.
    
    From current city, always move to the highest-priority unvisited city.
    Priority = (prevalence × urgency) / distance_from_current
    
    Complexity: O(V²) where V is the number of cities
    
    Args:
        graph: NetworkX graph with city nodes and road edges
        start_city: Starting city name
        urgency: Urgency multiplier (default 1.0, range 0.1-10.0)
        
    Returns:
        Tuple of (path, total_distance, priority_score)
        - path: List of cities in tour order (None if start_city invalid)
        - total_distance: Total distance in kilometers
        - priority_score: Total priority weight
    """
    # Validate input
    if start_city not in graph.nodes:
        return None, float('inf'), float('inf')
    
    # Initialize
    all_cities = set(graph.nodes())
    visited = {start_city}
    path = [start_city]
    current_city = start_city
    
    # Visit all remaining cities - O(V) iterations
    while len(visited) < len(all_cities):
        best_next = None
        best_priority = -float('inf')  # Higher is better for priority
        
        # Find highest-priority unvisited city - O(V) per iteration
        for candidate in graph.nodes():
            if candidate in visited:
                continue
            
            # Calculate priority score for this candidate
            candidate_prevalence = graph.nodes[candidate].get('prevalence', 0.5)
            
            # Find shortest path distance from current to candidate
            try:
                temp_path, temp_dist, _ = priority_dijkstra(
                    graph, current_city, candidate, urgency=1.0
                )
                
                if temp_path and temp_dist > 0:
                    # Priority = (prevalence × urgency) / distance
                    # Higher prevalence and urgency = higher priority
                    # Shorter distance = higher priority
                    priority_score = (candidate_prevalence * urgency) / temp_dist
                    
                    if priority_score > best_priority:
                        best_priority = priority_score
                        best_next = candidate
            except:
                continue
        
        # If no reachable city found, break
        if best_next is None:
            break
        
        # Move to the highest-priority city
        visited.add(best_next)
        path.append(best_next)
        current_city = best_next
    
    # Calculate tour metrics
    total_distance, total_priority = calculate_tour_metrics(graph, path, urgency)
    
    return path, total_distance, total_priority


if __name__ == "__main__":
    # Test the routing algorithm
    from data_loader import create_graph
    
    G = create_graph()
    
    print("=" * 60)
    print("HealthRoute Africa - Routing Algorithm Test")
    print("=" * 60)
    
    # Test case 1: Standard routing
    print("\nTest 1: Lagos to Kano (Standard Urgency)")
    path, distance, weight = priority_dijkstra(G, "Lagos", "Kano", urgency=1.0)
    if path:
        print(f"Path: {' -> '.join(path)}")
        print(f"Total Distance: {distance:.2f} km")
        print(f"Priority Score: {weight:.4f}")
    
    # Test case 2: High urgency scenario
    print("\n" + "=" * 60)
    print("Test 2: Lagos to Benin City vs Abraka (High Urgency)")
    print("=" * 60)
    
    # Abraka: closer (350km), low prevalence (15%)
    path1, dist1, weight1 = priority_dijkstra(G, "Lagos", "Abraka", urgency=5.0)
    print(f"\nRoute to Abraka (Low Prevalence 15%):")
    print(f"Path: {' -> '.join(path1)}")
    print(f"Distance: {dist1:.2f} km")
    print(f"Priority Score: {weight1:.4f}")
    
    # Benin City: medium distance (290km), high prevalence (75%)
    path2, dist2, weight2 = priority_dijkstra(G, "Lagos", "Benin City", urgency=5.0)
    print(f"\nRoute to Benin City (High Prevalence 75%):")
    print(f"Path: {' -> '.join(path2)}")
    print(f"Distance: {dist2:.2f} km")
    print(f"Priority Score: {weight2:.4f}")
    
    print(f"\n{'='*60}")
    if weight2 < weight1:
        print("✓ CORRECT: High-prevalence city prioritized despite distance!")
    else:
        print("✗ ERROR: Algorithm not prioritizing correctly")
    print(f"{'='*60}")
    
    # Test case 3: Optimal Tour Routing
    print("\n" + "=" * 60)
    print("Test 3: Optimal Tour from Lagos (Standard Urgency)")
    print("=" * 60)
    
    tour_path, tour_dist, tour_weight = optimal_tour_routing(G, "Lagos", urgency=1.0)
    if tour_path:
        print(f"\nTour Path: {' -> '.join(tour_path)}")
        print(f"Cities Visited: {len(tour_path)}/{len(G.nodes())}")
        print(f"Total Distance: {tour_dist:.2f} km")
        print(f"Priority Score: {tour_weight:.4f}")
    
    # Test case 4: Priority Tour Routing (High Urgency)
    print("\n" + "=" * 60)
    print("Test 4: Priority Tour from Lagos (High Urgency)")
    print("=" * 60)
    
    priority_path, priority_dist, priority_weight = priority_tour_routing(G, "Lagos", urgency=5.0)
    if priority_path:
        print(f"\nPriority Tour Path: {' -> '.join(priority_path)}")
        print(f"Cities Visited: {len(priority_path)}/{len(G.nodes())}")
        print(f"Total Distance: {priority_dist:.2f} km")
        print(f"Priority Score: {priority_weight:.4f}")
        
        # Show prevalence of first few cities visited
        print("\nFirst 5 cities visited (with prevalence):")
        for i, city in enumerate(priority_path[:5], 1):
            prev = G.nodes[city].get('prevalence', 0) * 100
            print(f"  {i}. {city} - {prev:.0f}% prevalence")
    
    print(f"\n{'='*60}")
