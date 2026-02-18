# 🏥 HealthRoute Africa - Project Defense Guide

**CSC 401: Algorithms & Complexity Analysis**  
**Medical Supply Routing System Using Priority-Weighted Dijkstra's Algorithm**

---

## 📑 Table of Contents

1. [Project Overview](#project-overview)
2. [Problem Statement](#problem-statement)
3. [System Architecture](#system-architecture)
4. [Algorithm Explanation](#algorithm-explanation)
5. [Malaria Prevalence Data](#malaria-prevalence-data)
6. [Priority Weight Calculation](#priority-weight-calculation)
7. [Interactive Mapping System](#interactive-mapping-system)
8. [Complexity Analysis](#complexity-analysis)
9. [Implementation Details](#implementation-details)
10. [Demonstration Scenarios](#demonstration-scenarios)
11. [Real-World Impact](#real-world-impact)
12. [Conclusion](#conclusion)

---

## 1. Project Overview

### What is HealthRoute Africa?

HealthRoute Africa is an **intelligent medical supply routing system** designed to optimize the delivery of malaria treatment supplies across Nigerian cities. Unlike traditional routing systems that only consider distance, our system **prioritizes high-risk malaria zones** during outbreak scenarios.

### Key Innovation

We modified **Dijkstra's shortest path algorithm** to incorporate:
- **Malaria prevalence rates** (disease burden in each city)
- **Outbreak urgency levels** (severity of the current situation)
- **Road distances** (physical constraints)

This creates a **priority-weighted routing system** that balances speed with medical necessity.

---

## 2. Problem Statement

### The Challenge

In Nigeria, malaria is a major public health concern with varying prevalence rates across different regions. During outbreak situations, medical supplies must be distributed efficiently, but **not all cities have equal need**.

**Traditional routing problems:**
- ❌ Only considers distance (shortest path)
- ❌ Ignores disease burden in different regions
- ❌ Cannot adapt to outbreak severity levels
- ❌ May deliver to low-risk areas while high-risk areas wait

**Our solution:**
- ✅ Considers both distance AND malaria prevalence
- ✅ Prioritizes high-prevalence zones
- ✅ Adjustable urgency multiplier for outbreak scenarios
- ✅ Ensures critical areas receive supplies first

---

## 3. System Architecture

### Three-Layer Architecture

```
┌─────────────────────────────────────────┐
│   PRESENTATION LAYER (app.py)          │
│   - Streamlit web interface            │
│   - Interactive Folium maps            │
│   - User controls & visualization      │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│   ALGORITHM LAYER (routing.py)         │
│   - Priority-Weighted Dijkstra         │
│   - Weight calculation logic           │
│   - Path reconstruction                │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│   DATA LAYER (data_loader.py)          │
│   - Nigerian cities dataset            │
│   - Malaria prevalence statistics      │
│   - Road network graph                 │
└─────────────────────────────────────────┘
```

### Technology Stack

- **Python 3.11+**: Core programming language
- **NetworkX**: Graph data structure and operations
- **Streamlit**: Web application framework
- **Folium**: Interactive geographic mapping
- **heapq**: Min-priority queue for algorithm efficiency

---

## 4. Algorithm Explanation

### Priority-Weighted Dijkstra's Algorithm

Our algorithm is a **modified version of Dijkstra's shortest path algorithm** that uses a custom weight function instead of just distance.

### Standard Dijkstra vs. Our Algorithm

| Aspect | Standard Dijkstra | Priority-Weighted Dijkstra |
|--------|------------------|---------------------------|
| **Weight** | Distance only | Distance / (Prevalence × Urgency) |
| **Goal** | Shortest path | Highest priority path |
| **Use Case** | Navigation | Medical emergency routing |
| **Adaptability** | Fixed | Dynamic (urgency parameter) |

### Algorithm Pseudocode

```
FUNCTION priority_dijkstra(graph, source, destination, urgency):
    
    // 1. INITIALIZATION
    FOR each city in graph:
        distance[city] ← ∞
        priority_weight[city] ← ∞
        predecessor[city] ← NULL
    
    distance[source] ← 0
    priority_weight[source] ← 0
    
    priority_queue ← min_heap()
    priority_queue.insert(0, source)
    visited ← empty_set()
    
    // 2. MAIN LOOP
    WHILE priority_queue is not empty:
        
        current_weight, current_city ← priority_queue.extract_min()
        
        IF current_city in visited:
            CONTINUE
        
        visited.add(current_city)
        
        IF current_city == destination:
            BREAK  // Path found!
        
        // 3. EXPLORE NEIGHBORS
        FOR each neighbor of current_city:
            
            IF neighbor in visited:
                CONTINUE
            
            road_distance ← graph.edge_distance(current_city, neighbor)
            
            current_prev ← graph.prevalence(current_city)
            neighbor_prev ← graph.prevalence(neighbor)
            avg_prevalence ← (current_prev + neighbor_prev) / 2
            
            // 4. CALCULATE PRIORITY WEIGHT
            edge_weight ← road_distance / (avg_prevalence × urgency)
            
            new_weight ← priority_weight[current_city] + edge_weight
            new_distance ← distance[current_city] + road_distance
            
            // 5. RELAXATION STEP
            IF new_weight < priority_weight[neighbor]:
                priority_weight[neighbor] ← new_weight
                distance[neighbor] ← new_distance
                predecessor[neighbor] ← current_city
                priority_queue.insert(new_weight, neighbor)
    
    // 6. RECONSTRUCT PATH
    path ← []
    current ← destination
    WHILE current ≠ NULL:
        path.prepend(current)
        current ← predecessor[current]
    
    RETURN path, distance[destination], priority_weight[destination]
```

### Key Differences from Standard Dijkstra

1. **Custom Weight Function**: Instead of using distance directly, we calculate:
   ```
   Weight = Distance / (Prevalence × Urgency)
   ```

2. **Two Metrics Tracked**:
   - `distance[]`: Actual road distance traveled
   - `priority_weight[]`: Priority score for routing decisions

3. **Average Prevalence**: We use the average prevalence of both endpoints for each road segment

---

## 5. Malaria Prevalence Data

### What is Malaria Prevalence?

**Prevalence** = The proportion of a population that has malaria at a given time

- Expressed as a decimal: 0.0 (0%) to 1.0 (100%)
- Example: 0.75 = 75% of the population has malaria

### Nigerian Cities Dataset (30 Cities)

Our system includes **30 Nigerian cities** with realistic malaria prevalence data:

#### High-Risk Zones (≥67% prevalence)

| City | Prevalence | Population | Region |
|------|-----------|------------|--------|
| **Ogbomosho** | 78% | 645,000 | South-West |
| **Benin City** | 75% | 1,500,000 | South-South |
| **Warri** | 72% | 536,023 | South-South |
| **Uyo** | 70% | 436,606 | South-South |
| **Port Harcourt** | 68% | 2,000,000 | South-South |

#### Medium-Risk Zones (34-66% prevalence)

| City | Prevalence | Population | Region |
|------|-----------|------------|--------|
| **Asaba** | 67% | 282,000 | South-South |
| **Calabar** | 65% | 461,796 | South-South |
| **Owerri** | 64% | 401,873 | South-East |
| **Enugu** | 62% | 800,000 | South-East |
| **Maiduguri** | 60% | 749,000 | North-East |

#### Low-Risk Zones (0-33% prevalence)

| City | Prevalence | Population | Region |
|------|-----------|------------|--------|
| **Lagos** | 25% | 14,000,000 | South-West |
| **Ota** | 22% | 350,000 | South-West |
| **Ikeja** | 18% | 600,000 | South-West |
| **Abraka** | 15% | 30,000 | South-South |

### Road Network

The system includes **over 80 road connections** between cities with realistic distances in kilometers based on actual Nigerian road infrastructure.

---

## 6. Priority Weight Calculation

### The Core Formula

```
Priority Weight = Distance / (Prevalence × Urgency)
```

### Understanding the Formula

**Lower weight = Higher priority** (more important to route through)

#### How Each Factor Affects Priority:

1. **Distance** (numerator):
   - ↑ Longer distance → ↑ Higher weight → ↓ Lower priority
   - ↓ Shorter distance → ↓ Lower weight → ↑ Higher priority

2. **Prevalence** (denominator):
   - ↑ Higher prevalence → ↓ Lower weight → ↑ Higher priority ✅
   - ↓ Lower prevalence → ↑ Higher weight → ↓ Lower priority

3. **Urgency** (denominator):
   - ↑ Higher urgency → ↓ Lower weight → ↑ Higher priority ✅
   - ↓ Lower urgency → ↑ Higher weight → ↓ Lower priority

### Worked Example

**Scenario**: Routing from Lagos to two possible destinations

**Option A: Abraka**
- Distance: 350 km
- Prevalence: 0.15 (15%)
- Urgency: 5.0
- **Weight** = 350 / (0.15 × 5.0) = 350 / 0.75 = **466.67**

**Option B: Benin City**
- Distance: 290 km
- Prevalence: 0.75 (75%)
- Urgency: 5.0
- **Weight** = 290 / (0.75 × 5.0) = 290 / 3.75 = **77.33**

**Result**: Benin City has a **lower weight (77.33 < 466.67)**, so it gets **higher priority** despite being only slightly closer. The high malaria prevalence makes it more critical.

### Urgency Multiplier Ranges

| Urgency Level | Range | Scenario | Effect |
|--------------|-------|----------|--------|
| **Low** | 0.1 - 2.0 | Standard delivery | Distance matters most |
| **Medium** | 2.1 - 5.0 | Elevated priority | Balance distance & prevalence |
| **High** | 5.1 - 10.0 | Emergency outbreak | Prevalence critical |

---

## 7. Interactive Mapping System

### Folium Geographic Visualization

Our system uses **Folium** to create interactive maps with real geographic coordinates.

### Map Features

#### 1. City Markers (Color-Coded by Prevalence)

- 🟢 **Green** (0-33%): Low malaria prevalence
- 🟠 **Orange** (34-66%): Medium malaria prevalence  
- 🔴 **Red** (67-100%): High malaria prevalence

#### 2. Special Markers

- 🔵 **Blue marker**: Source hub (supply center)
- 🟣 **Purple marker**: Destination clinic (target location)

#### 3. Road Network

- **Gray lines**: All available roads between cities
- **Red animated line**: Optimal route (with AntPath animation)

#### 4. Interactive Popups

Click any city to see:
- City name
- Malaria prevalence percentage
- Population
- GPS coordinates

### Map Legend

The map includes a dynamic legend showing:
- Prevalence color coding
- Source/destination markers
- Optimal route indicator (when calculated)

---

## 8. Complexity Analysis

### Time Complexity: O((E + V) log V)

**Where:**
- **V** = Number of vertices (cities) = 30
- **E** = Number of edges (roads) = 80+

### Breakdown of Operations

| Operation | Complexity | Count | Total |
|-----------|-----------|-------|-------|
| **Initialization** | O(1) per city | V | O(V) |
| **Main loop** | - | V iterations | - |
| **Extract min from heap** | O(log V) | V times | O(V log V) |
| **Edge relaxation** | O(1) per edge | E total | O(E) |
| **Insert into heap** | O(log V) | ≤ E times | O(E log V) |
| **Path reconstruction** | O(1) per city | ≤ V | O(V) |

**Total**: O(V) + O(V log V) + O(E) + O(E log V) + O(V) = **O((E + V) log V)**

### Space Complexity: O(V + E)

- **Graph storage**: O(V + E)
- **Distance arrays**: O(V)
- **Priority queue**: O(V)
- **Visited set**: O(V)
- **Predecessor array**: O(V)

**Total**: O(V + E)

### Why This is Efficient

For **sparse graphs** (typical road networks where E ≈ V):
- Our complexity: O((V + V) log V) = **O(V log V)**
- Much better than O(V²) for dense graphs

For our dataset:
- V = 30 cities
- E ≈ 80 roads
- Operations: ≈ (30 + 80) × log(30) ≈ **540 operations**

This is **extremely fast** even for larger networks!

---

## 9. Implementation Details

### Module Structure

#### 1. `data_loader.py` - Data Management

**Purpose**: Manages city data and road network

**Key Components**:
```python
CITIES = {
    "Lagos": {
        "coords": (6.5244, 3.3792),
        "prevalence": 0.25,
        "population": 14000000
    },
    # ... 29 more cities
}

ROAD_NETWORK = [
    ("Lagos", "Ibadan", 120),  # city1, city2, distance_km
    # ... 80+ road connections
]
```

**Functions**:
- `create_graph()`: Builds NetworkX graph from data
- `get_city_data(city)`: Returns city information
- `get_all_cities()`: Returns list of all city names

#### 2. `routing.py` - Algorithm Implementation

**Purpose**: Implements Priority-Weighted Dijkstra's Algorithm

**Key Functions**:

```python
def calculate_priority_weight(distance, prevalence, urgency):
    """
    Calculate priority weight for a road segment.
    Returns: distance / (prevalence × urgency)
    """
    if prevalence == 0 or urgency == 0:
        return float('inf')
    return distance / (prevalence * urgency)

def priority_dijkstra(graph, source, destination, urgency):
    """
    Main routing algorithm.
    Returns: (path, total_distance, priority_score)
    """
    # Implementation with heapq priority queue
    # ... (see algorithm pseudocode above)
```

#### 3. `app.py` - Web Interface

**Purpose**: Streamlit dashboard for user interaction

**Features**:
- City selection dropdowns
- Urgency slider (0.1 - 10.0)
- Interactive Folium map
- Route results display
- Step-by-step route breakdown

### Data Structures Used

1. **NetworkX Graph**: Stores cities (nodes) and roads (edges)
2. **Min-Heap (heapq)**: Priority queue for efficient extraction
3. **Dictionaries**: Fast O(1) lookups for distances and weights
4. **Sets**: O(1) visited city tracking

---

## 10. Demonstration Scenarios

### Scenario 1: Low Urgency (Standard Delivery)

**Setup**:
- Source: Lagos
- Destination: Kano
- Urgency: 1.0 (standard)

**Expected Behavior**:
- Algorithm balances distance and prevalence equally
- Route may favor shorter paths
- Priority score moderate

**How to Demonstrate**:
1. Open app: `streamlit run app.py`
2. Select Lagos → Kano
3. Set urgency to 1.0
4. Click "Calculate Optimal Route"
5. Note the route and priority score

---

### Scenario 2: High Urgency (Emergency Outbreak)

**Setup**:
- Source: Lagos
- Destination: Benin City
- Urgency: 8.0 (emergency)

**Expected Behavior**:
- High-prevalence routes strongly favored
- Priority score very low (high priority)
- May take slightly longer route through high-prevalence areas

**How to Demonstrate**:
1. Select Lagos → Benin City
2. Set urgency to 8.0
3. Calculate route
4. Compare priority score to low urgency scenario

---

### Scenario 3: Comparing Priority Scores

**Setup**: Test same route with different urgency levels

**Route**: Ibadan → Ilorin (goes through Ogbomosho, 78% prevalence)

| Urgency | Priority Score | Interpretation |
|---------|---------------|----------------|
| 0.5x | ~353.59 | Low priority - can wait |
| 1.0x | ~176.79 | Normal priority |
| 3.0x | ~58.93 | Elevated priority |
| 6.0x | ~29.47 | High priority - urgent |
| 10.0x | ~17.68 | Emergency - immediate action |

**Observation**: Priority score drops dramatically with urgency, showing how the system adapts to outbreak severity.

---

### Scenario 4: Route Comparison

**Setup**: Compare routes to high vs. low prevalence cities

**From Lagos, High Urgency (5.0x)**:

**To Abraka** (Low prevalence 15%):
- Distance: ~350 km
- Priority Score: ~466.67 (lower priority)

**To Benin City** (High prevalence 75%):
- Distance: 290 km
- Priority Score: ~77.33 (HIGHER priority)

**Result**: System correctly prioritizes Benin City despite similar distances.

---

## 11. Real-World Impact

### Healthcare Logistics Application

#### Problem in Nigeria

- Malaria causes **60% of outpatient visits** in Nigeria
- **97% of the population** is at risk
- Uneven distribution of medical supplies
- Limited resources require smart allocation

#### How Our System Helps

1. **Prioritizes High-Risk Areas**
   - Ensures critical zones get supplies first
   - Reduces mortality in outbreak situations

2. **Adapts to Outbreak Severity**
   - Urgency multiplier adjusts to current situation
   - Can switch from routine to emergency mode

3. **Transparent Decision-Making**
   - Visual map shows why routes are chosen
   - Priority scores justify resource allocation

4. **Scalable Solution**
   - O((E+V) log V) complexity handles larger networks
   - Can expand to all 36 Nigerian states

### Potential Extensions

1. **Multi-Disease Support**: Add prevalence data for other diseases (cholera, yellow fever)
2. **Multi-Hub Routing**: Optimize from multiple supply centers simultaneously
3. **Real-Time Traffic**: Integrate traffic data to update road distances
4. **Supply Constraints**: Add vehicle capacity and supply quantity limits
5. **Historical Analysis**: Track outbreak patterns over time

---

## 12. Conclusion

### Project Summary

HealthRoute Africa demonstrates how **classical algorithms can be adapted** to solve modern real-world problems. By modifying Dijkstra's algorithm with a custom weight function, we created a system that:

✅ **Balances multiple objectives** (distance vs. medical need)  
✅ **Adapts to changing situations** (urgency multiplier)  
✅ **Maintains efficiency** (O((E+V) log V) complexity)  
✅ **Provides transparency** (visual maps and clear metrics)

### Key Achievements

1. **Algorithm Design**: Successfully modified Dijkstra's algorithm for multi-criteria optimization
2. **Real-World Data**: Integrated realistic Nigerian city and malaria prevalence data
3. **User Interface**: Created intuitive web dashboard with interactive maps
4. **Complexity Analysis**: Proven efficient time and space complexity
5. **Practical Application**: Addressed genuine healthcare logistics challenge

### Technical Skills Demonstrated

- **Algorithm Analysis**: Understanding and modifying classical algorithms
- **Data Structures**: Graphs, heaps, dictionaries, sets
- **Complexity Theory**: Big-O analysis and optimization
- **Software Engineering**: Modular design, clean code, documentation
- **Web Development**: Streamlit, Folium, interactive visualization
- **Problem Solving**: Translating real-world needs into algorithmic solutions

### Defense Talking Points

1. **Why modify Dijkstra?**
   - Standard Dijkstra only finds shortest path
   - Healthcare needs priority-based routing
   - Custom weight function allows multi-criteria optimization

2. **Why this weight formula?**
   - Inverse relationship: high prevalence = low weight = high priority
   - Urgency multiplier provides adaptability
   - Simple, interpretable, mathematically sound

3. **How does it scale?**
   - O((E+V) log V) is efficient for sparse graphs
   - Can handle hundreds of cities
   - Priority queue ensures fast min-extraction

4. **Real-world applicability?**
   - Malaria is a critical issue in Nigeria
   - System can adapt to other diseases
   - Transparent decision-making for stakeholders

---

## Appendix: Quick Reference

### Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Start web dashboard
streamlit run app.py

# Test algorithm directly
python routing.py
```

### Key Files

- `app.py`: Web interface (406 lines)
- `routing.py`: Algorithm implementation (246 lines)
- `data_loader.py`: Dataset and graph creation (402 lines)
- `requirements.txt`: Python dependencies

### Core Formula

```
Priority Weight = Distance / (Prevalence × Urgency)

Lower weight = Higher priority
```

### Complexity

- **Time**: O((E + V) log V)
- **Space**: O(V + E)

### Dataset

- **30 cities** across Nigeria
- **80+ road connections**
- **Prevalence range**: 15% (Abraka) to 78% (Ogbomosho)

---

**End of Defense Guide**

*Good luck with your project defense! 🎓*
