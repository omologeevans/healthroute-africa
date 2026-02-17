# Priority-Weighted Routing Algorithm

## Algorithm: Medical Supply Routing with Malaria Prevalence

**Input**: Graph G, Source city, Destination city, Urgency level  
**Output**: Optimal path, Total distance, Priority score

---

### Algorithm Steps:

```
1.  Initialize all cities in graph:
        distance[city] ← ∞
        weight[city] ← ∞
        predecessor[city] ← NULL

2.  Set source city:
        distance[source] ← 0
        weight[source] ← 0

3.  Create priority_queue (min-heap)
    Add (0, source) to priority_queue
    Create empty visited set

4.  WHILE priority_queue is not empty:
        
        current ← Extract city with minimum weight from queue
        
        IF current in visited:
            CONTINUE
        
        Add current to visited
        
        IF current = destination:
            BREAK (path found)
        
        FOR EACH neighbor of current:
            IF neighbor in visited:
                CONTINUE
            
            road_distance ← distance between current and neighbor
            avg_prevalence ← (prevalence[current] + prevalence[neighbor]) / 2
            
            edge_weight ← road_distance / (avg_prevalence × urgency)
            
            new_weight ← weight[current] + edge_weight
            new_distance ← distance[current] + road_distance
            
            IF new_weight < weight[neighbor]:
                weight[neighbor] ← new_weight
                distance[neighbor] ← new_distance
                predecessor[neighbor] ← current
                Add (new_weight, neighbor) to priority_queue

5.  Reconstruct path:
        path ← []
        current ← destination
        WHILE current ≠ NULL:
            Add current to path
            current ← predecessor[current]
        Reverse path

6.  RETURN path, distance[destination], weight[destination]
```

---

### Key Formula:
```
Edge Weight = Distance / (Average Prevalence × Urgency)
```

**Effect**:
- High prevalence → Low weight → High priority
- High urgency → Low weight → High priority
- Long distance → High weight → Low priority

**Complexity**: O((E+V) log V) where E = roads, V = cities
