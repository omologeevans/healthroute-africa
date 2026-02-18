# 🏥 HealthRoute Africa

**Medical Supply Optimization System for CSC 401 (Algorithms & Complexity)**

A priority-weighted routing system that optimizes medical supply delivery to Nigerian clinics based on malaria prevalence and outbreak urgency.

---

## 📋 Project Overview

HealthRoute Africa implements a **Priority-Weighted Dijkstra's Algorithm** to route medical supplies from central hubs to remote clinics. Unlike standard routing that only considers distance, our system prioritizes high malaria-prevalence zones during outbreaks.

### Key Features

- ✅ **Priority-Weighted Routing**: Custom weight formula balancing distance and medical urgency
- ✅ **Three Routing Modes**: Point-to-Point, Optimal Tour, and Priority Tour
- ✅ **Interactive Map**: Real geographic visualization using Folium and OpenStreetMap
- ✅ **33 Nigerian Cities**: Comprehensive network covering major cities and towns
- ✅ **Dynamic Urgency Control**: Adjustable outbreak severity slider (0.1x - 10x)
- ✅ **Multi-City Tours**: Visit all cities with optimal or priority-based routing
- ✅ **Efficient Algorithms**: O((E+V) log V) for point-to-point, O(V²) for tours

---

## 🧮 Algorithm Details

### Routing Modes

#### 1. Point-to-Point Routing
Uses **Priority-Weighted Dijkstra's Algorithm** to find optimal route between two cities.

**Weight Formula:**
```
W = Distance / (Prevalence × Urgency)
```

**Where:**
- **Distance**: Road distance in kilometers
- **Prevalence**: Malaria prevalence rate (0.0 to 1.0)
- **Urgency**: Outbreak severity multiplier (0.1 to 10.0)

**Behavior:**
- Lower weight = Higher priority
- High prevalence → Lower weight (higher priority)
- High urgency → Lower weight (higher priority)
- Long distance → Higher weight (lower priority)

**Complexity**: O((E+V) log V)

#### 2. Optimal Tour Routing
Uses **Nearest Neighbor TSP Approximation** to visit all cities via shortest path.

**Algorithm:**
- Start from selected city
- Repeatedly visit nearest unvisited city (based on priority weight)
- Continue until all cities visited

**Use Case**: Weekly supply distribution routes

**Complexity**: O(V²)

#### 3. Priority Tour Routing
Uses **Greedy Prevalence-Based Selection** to prioritize high-prevalence areas.

**Priority Formula:**
```
Priority = (Prevalence × Urgency) / Distance
```

**Algorithm:**
- Start from selected city
- Always move to highest-priority unvisited city
- Continue until all cities visited

**Use Case**: Emergency outbreak response

**Complexity**: O(V²)

### Complexity Analysis

**Point-to-Point: O((E+V) log V)**
- **E**: Number of edges (roads between cities)
- **V**: Number of vertices (cities)
- **Implementation**: Uses Python's `heapq` module for min-priority queue
- **Operations**:
  - Initialization: O(V)
  - Main loop: O(V) iterations
  - Heap operations: O(log V) per operation
  - Edge relaxation: O(E) total

**Tour Modes: O(V²)**
- Each city selection requires checking all unvisited cities
- V iterations × V checks per iteration
- Efficient for networks with 33 cities (~1,089 operations)

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `streamlit>=1.31.0` - Web application framework
- `networkx>=3.2.1` - Graph data structure
- `matplotlib>=3.8.2` - Plotting library
- `numpy>=1.26.3` - Numerical computations
- `folium>=0.15.0` - Interactive maps
- `streamlit-folium>=0.15.0` - Streamlit-Folium integration

---

## 🎮 Running the Application

### Start the Streamlit Dashboard

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Test the Routing Algorithm

```bash
python routing.py
```

This runs the built-in test cases demonstrating the priority-weighted routing logic.

---

## 📁 Project Structure

```
401/
├── app.py                 # Streamlit web dashboard
├── routing.py             # Priority-Weighted Dijkstra's Algorithm
├── data_loader.py         # Nigerian cities dataset and graph creation
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

---

## 🗺️ Dataset

### Nigerian Cities (10 nodes)

| City | Malaria Prevalence | Population | Coordinates |
|------|-------------------|------------|-------------|
| Lagos | 25% | 14,000,000 | (6.5244, 3.3792) |
| Abuja | 45% | 3,000,000 | (9.0765, 7.3986) |
| Benin City | **75%** | 1,500,000 | (6.3350, 5.6037) |
| Abraka | 15% | 30,000 | (5.7833, 6.0833) |
| Port Harcourt | 68% | 2,000,000 | (4.8156, 7.0498) |
| Kano | 52% | 4,000,000 | (12.0022, 8.5919) |
| Ibadan | 38% | 3,500,000 | (7.3775, 3.9470) |
| Enugu | 62% | 800,000 | (6.5244, 7.5105) |
| Kaduna | 48% | 1,600,000 | (10.5105, 7.4165) |
| Jos | 35% | 900,000 | (9.8965, 8.8583) |

### Road Network (16 edges)

The road network includes major highways connecting these cities with realistic distances in kilometers.

---

## 🧪 Verification Test Case

**Scenario**: Emergency malaria outbreak response

**Setup:**
- Source: Lagos
- Urgency: 5.0x (High outbreak severity)
- Compare two destinations:
  - **Abraka**: Closer (350km), Low prevalence (15%)
  - **Benin City**: Medium distance (290km), High prevalence (75%)

**Expected Result**: 
The algorithm should prioritize **Benin City** despite Abraka being closer, because the high malaria prevalence and urgency multiplier result in a lower priority weight.

**Run Test:**
```bash
python routing.py
```

---

## 🎨 Dashboard Features

### Routing Mode Selector
- **Point-to-Point**: Find optimal route between two cities
- **Optimal Tour**: Visit all cities using shortest total path
- **Priority Tour**: Visit cities by prevalence/priority order

### Priority Trip Score Rating
Visual indicator showing route urgency level:
- 🔴 **HIGH** (Red): Critical priority - High prevalence route (score/km < 1.5)
- 🟡 **MEDIUM** (Yellow): Moderate priority - Balanced route (score/km < 3.0)
- 🟢 **LOW** (Green): Low priority - Distance-optimized route (score/km ≥ 3.0)

Lower priority score indicates higher urgency (better route for high-prevalence areas)

### Interactive Map
- Real geographic visualization on OpenStreetMap
- Color-coded cities by malaria prevalence:
  - 🟢 Green: Low (0-33%)
  - 🟠 Orange: Medium (34-66%)
  - 🔴 Red: High (67-100%)
- Animated route path with AntPath effect
- **Numbered waypoints** for tour routes (1, 2, 3...)
- Clickable city markers with detailed popups

### Control Panel
- Routing mode selector (radio buttons)
- Start city / Source hub selector
- Destination clinic selector (Point-to-Point only)
- Urgency slider (0.1x - 10x)
- Calculate route/tour button

### Results Display
- **Priority rating badge** with color coding
- Total distance (km)
- Priority score
- Cities visited (tours) / Route segments (point-to-point)
- Step-by-step route breakdown
- Segment-level details (distance, prevalence)

---

## 📊 Project Defense Points

### Algorithm Complexity
- **Proven O((E+V) log V)** using heapq min-priority queue
- Efficient for sparse graphs (typical road networks)
- Scalable to larger datasets

### Real-World Impact
- Addresses critical healthcare logistics in Nigeria
- Prioritizes high-risk malaria zones during outbreaks
- Balances speed and medical urgency

### Technical Implementation
- Clean separation of concerns (data, algorithm, UI)
- Reusable routing logic for other diseases
- Interactive visualization for stakeholder communication

---

## 👨‍💻 Author

**CSC 401 Project - Algorithms & Complexity**

**System**: Priority-Weighted Dijkstra's Algorithm  
**Application**: Medical Supply Routing  
**Region**: Nigeria  
**Disease Focus**: Malaria

---

## 📝 License

This project is created for educational purposes as part of CSC 401 coursework.

---

## 🔮 Future Enhancements

- Real-time traffic data integration
- Multi-hub routing optimization
- Historical outbreak data analysis
- Mobile app for field workers
- Integration with WHO malaria statistics
