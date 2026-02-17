"""
HealthRoute Africa - Interactive Medical Supply Routing Dashboard
Streamlit web application for visualizing priority-weighted routing.
"""

import streamlit as st
import networkx as nx
import folium
from folium import plugins
# import matplotlib.pyplot as plt # Removed
# import matplotlib.patches as mpatches # Removed
from matplotlib.colors import LinearSegmentedColormap # This import is no longer needed as create_color_map is removed
import numpy as np
from streamlit_folium import st_folium

from data_loader import (create_graph, get_all_lgas, get_lga_data, 
                         get_all_states, get_lgas_for_state, get_lgas_by_state)
from routing import priority_dijkstra, get_route_details, optimal_tour_routing, priority_tour_routing


# Page configuration
st.set_page_config(
    page_title="HealthRoute Africa",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stAlert {
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)


def get_prevalence_color(prevalence):
    """
    Get color based on malaria prevalence.
    
    Args:
        prevalence: Malaria prevalence (0.0 to 1.0)
        
    Returns:
        Hex color code
    """
    if prevalence < 0.33:
        return '#2ecc71'  # Green - Low
    elif prevalence < 0.67:
        return '#f39c12'  # Orange - Medium
    else:
        return '#e74c3c'  # Red - High


def get_priority_rating(priority_score, total_distance):
    """
    Get priority trip rating based on priority score and distance.
    
    Lower priority score = Higher urgency (better route considering prevalence)
    
    Args:
        priority_score: Calculated priority score from routing algorithm
        total_distance: Total distance of the route in km
        
    Returns:
        Tuple of (rating_text, color_hex, description)
    """
    # Calculate score per km to normalize for route length
    if total_distance > 0:
        score_per_km = priority_score / total_distance
    else:
        score_per_km = priority_score
    
    # Thresholds for classification
    # Lower score per km = higher priority (better route for high-prevalence areas)
    if score_per_km < 1.5:
        return ("HIGH", "#e74c3c", "Critical priority - High prevalence route")
    elif score_per_km < 3.0:
        return ("MEDIUM", "#f39c12", "Moderate priority - Balanced route")
    else:
        return ("LOW", "#2ecc71", "Low priority - Distance-optimized route")


def create_folium_map(graph, path=None, source=None, destination=None, is_tour=False):
    """
    Create interactive Folium map of the road network.
    
    Args:
        graph: NetworkX graph
        path: Optional route to highlight
        source: Source LGA
        destination: Destination LGA
        is_tour: Whether this is a multi-city tour (shows numbered waypoints)
        
    Returns:
        Folium map object
    """
    # Center map on Nigeria
    nigeria_center = [9.0820, 8.6753]
    m = folium.Map(
        location=nigeria_center,
        zoom_start=6,
        tiles='OpenStreetMap',
        control_scale=True
    )
    
    # Add all road connections (edges) first
    for edge in graph.edges():
        lga1, lga2 = edge
        coords1 = graph.nodes[lga1]['pos']
        coords2 = graph.nodes[lga2]['pos']
        distance = graph.edges[edge]['distance']
        
        # Draw road as a light gray line
        folium.PolyLine(
            locations=[coords1, coords2],
            color='#cccccc',
            weight=3,
            opacity=0.6,
            popup=f"{lga1} ↔ {lga2}<br>{distance} km"
        ).add_to(m)
    
    # Highlight the optimal path if provided
    if path and len(path) > 1:
        path_coords = []
        for lga in path:
            coords = graph.nodes[lga]['pos']
            path_coords.append(coords)
        
        # Draw the route in red
        route_label = "Tour Route" if is_tour else f"Optimal Route: {' → '.join(path)}"
        folium.PolyLine(
            locations=path_coords,
            color='#e74c3c',
            weight=5,
            opacity=0.9,
            popup=route_label
        ).add_to(m)
        
        # Add animated marker along the route
        plugins.AntPath(
            locations=path_coords,
            color='#e74c3c',
            weight=3,
            opacity=0.8,
            delay=1000
        ).add_to(m)
        
        # Add numbered waypoints for tours
        if is_tour:
            for idx, lga in enumerate(path, 1):
                coords = graph.nodes[lga]['pos']
                folium.Marker(
                    location=coords,
                    icon=folium.DivIcon(
                        html=f"""
                        <div style="
                            font-size: 12px;
                            font-weight: bold;
                            color: white;
                            background-color: #e74c3c;
                            padding: 4px 8px;
                            border-radius: 50%;
                            border: 2px solid white;
                            text-align: center;
                            min-width: 24px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                        ">{idx}</div>
                        """
                    )
                ).add_to(m)
    
    # Add LGA markers
    for node in graph.nodes():
        coords = graph.nodes[node]['pos']
        prevalence = graph.nodes[node]['prevalence']
        population = graph.nodes[node]['population']
        
        # Determine marker color and icon
        if node == source:
            icon_color = 'blue'
            icon = 'home'
            marker_color = 'blue'
            prefix = '🏥 SOURCE HUB' if not is_tour else '🏥 START'
        elif node == destination and not is_tour:
            icon_color = 'purple'
            icon = 'plus-sign'
            marker_color = 'purple'
            prefix = '🏥 DESTINATION CLINIC'
        else:
            icon_color = 'white'
            icon = 'info-sign'
            marker_color = get_prevalence_color(prevalence)
            prefix = '📍'
        
        # Create popup content
        popup_html = f"""
        <div style="font-family: Arial; min-width: 200px;">
            <h4 style="margin: 0 0 10px 0; color: {marker_color};">{prefix}<br>{node}</h4>
            <p style="margin: 5px 0;"><strong>Malaria Prevalence:</strong> {prevalence*100:.0f}%</p>
            <p style="margin: 5px 0;"><strong>Population:</strong> {population:,}</p>
            <p style="margin: 5px 0;"><strong>Coordinates:</strong> {coords[0]:.4f}, {coords[1]:.4f}</p>
        </div>
        """
        
        # Add marker
        folium.CircleMarker(
            location=coords,
            radius=10 if node in [source, destination] else 8,
            popup=folium.Popup(popup_html, max_width=300),
            color='white',
            fill=True,
            fillColor=marker_color,
            fillOpacity=0.9,
            weight=2
        ).add_to(m)
        
        # Add LGA label
        folium.Marker(
            location=coords,
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    font-size: 10px;
                    font-weight: bold;
                    color: #333;
                    background-color: rgba(255, 255, 255, 0.8);
                    padding: 2px 5px;
                    border-radius: 3px;
                    border: 1px solid #ccc;
                    white-space: nowrap;
                    transform: translate(-50%, 15px);
                ">{node}</div>
                """
            )
        ).add_to(m)
    
    # Add legend
    legend_html = f"""
    <div style="
        position: fixed;
        top: 10px;
        right: 10px;
        width: 240px;
        background-color: white;
        border: 2px solid #333;
        border-radius: 8px;
        padding: 12px;
        font-size: 13px;
        z-index: 9999;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    ">
        <h4 style="margin: 0 0 12px 0; color: #222; font-weight: bold; font-size: 14px;">Legend</h4>
        <p style="margin: 6px 0; color: #333; font-weight: 500;"><span style="color: #2ecc71; font-size: 16px;">●</span> Low Prevalence (0-33%)</p>
        <p style="margin: 6px 0; color: #333; font-weight: 500;"><span style="color: #f39c12; font-size: 16px;">●</span> Medium Prevalence (34-66%)</p>
        <p style="margin: 6px 0; color: #333; font-weight: 500;"><span style="color: #e74c3c; font-size: 16px;">●</span> High Prevalence (67-100%)</p>
        <hr style="margin: 10px 0; border: 0; border-top: 1px solid #ddd;">
        <p style="margin: 6px 0; color: #333; font-weight: 500;"><span style="color: blue; font-size: 16px;">●</span> {'Start LGA' if is_tour else 'Source Hub'}</p>
        {f'<p style="margin: 6px 0; color: #333; font-weight: 500;"><span style="color: purple; font-size: 16px;">●</span> Destination Clinic</p>' if not is_tour else ''}
        {f'<p style="margin: 6px 0; color: #333; font-weight: 500;"><span style="color: #e74c3c; font-size: 16px; font-weight: bold;">━━</span> {"Tour Route" if is_tour else "Optimal Route"}</p>' if path else ''}
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return m


def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<div class="main-header">🏥 HealthRoute Africa</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Medical Supply Optimization System | Priority-Weighted Routing</div>',
        unsafe_allow_html=True
    )
    
    # Load graph
    G = create_graph()
    lgas = get_all_lgas()
    states = get_all_states()
    
    # Sidebar controls
    st.sidebar.header("⚙️ Routing Configuration")
    
    # Routing mode selector
    st.sidebar.markdown("### 🚦 Routing Mode")
    routing_mode = st.sidebar.radio(
        "Select routing mode:",
        options=["Point-to-Point", "Optimal Tour", "Priority Tour"],
        help="""
        - **Point-to-Point**: Find optimal route between two LGAs
        - **Optimal Tour**: Visit all LGAs using shortest total path (TSP)
        - **Priority Tour**: Visit LGAs by prevalence/priority order
        """
    )
    
    is_tour_mode = routing_mode in ["Optimal Tour", "Priority Tour"]
    
    st.sidebar.markdown("### 📍 Select Locations")
    
    # Source/Start LGA selection with State → LGA
    source_label = "Start Location" if is_tour_mode else "Source Hub (Supply Center)"
    st.sidebar.markdown(f"**{source_label}**")
    
    # Source State selection
    source_state = st.sidebar.selectbox(
        "Select State",
        states,
        index=states.index("Lagos") if "Lagos" in states else 0,
        key="source_state"
    )
    
    # Source LGA selection
    source_lgas = get_lgas_by_state(source_state)
    if source_lgas:
        source = st.sidebar.selectbox(
            "Select Local Government",
            source_lgas,
            key="source_lga"
        )
    else:
        # Fallback to first LGA
        source = lgas[0] if lgas else "Lagos - Alimosho"
    
    # Destination (only for point-to-point)
    destination = None
    if not is_tour_mode:
        st.sidebar.markdown("**Destination Clinic**")
        
        # Destination State selection
        dest_state = st.sidebar.selectbox(
            "Select State",
            states,
            index=states.index("Kano") if "Kano" in states else 1,
            key="dest_state"
        )
        
        # Destination LGA selection
        dest_lgas = get_lgas_by_state(dest_state)
        if dest_lgas:
            destination = st.sidebar.selectbox(
                "Select Local Government",
                dest_lgas,
                key="dest_lga"
            )
        else:
            # Fallback to second LGA
            destination = lgas[1] if len(lgas) > 1 else "Kano - Dala"
    
    st.sidebar.markdown("### 🚨 Outbreak Severity")
    urgency = st.sidebar.slider(
        "Urgency Multiplier",
        min_value=0.1,
        max_value=10.0,
        value=1.0,
        step=0.1,
        help="Higher values prioritize high-prevalence areas more strongly"
    )
    
    st.sidebar.markdown(f"""
    **Current Setting:** `{urgency:.1f}x`
    
    - **Low (0.1-2.0)**: Standard delivery
    - **Medium (2.1-5.0)**: Elevated priority
    - **High (5.1-10.0)**: Emergency outbreak response
    """)
    
    # Algorithm info
    with st.sidebar.expander("ℹ️ Algorithm Details"):
        st.markdown("""
        **Priority-Weighted Dijkstra's Algorithm**
        
        **Weight Formula:**
        ```
        W = Distance / (Prevalence × Urgency)
        ```
        
        **Complexity:** O((E+V) log V)
        - E: Number of roads
        - V: Number of cities
        - Uses min-heap priority queue
        
        **Behavior:**
        - Lower weight = Higher priority
        - High prevalence → Lower weight
        - High urgency → Lower weight
        - Long distance → Higher weight
        """)
    
    # Calculate route button
    button_label = "🚀 Calculate Tour" if is_tour_mode else "🚀 Calculate Optimal Route"
    calculate = st.sidebar.button(button_label, type="primary", use_container_width=True)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🗺️ Interactive Network Map")
        
        # Calculate route if button clicked
        if calculate:
            # Validate inputs
            if not is_tour_mode and source == destination:
                st.error("❌ Source and destination must be different!")
            else:
                # Run appropriate routing algorithm
                with st.spinner("Calculating route..."):
                    if routing_mode == "Point-to-Point":
                        path, total_distance, priority_score = priority_dijkstra(
                            G, source, destination, urgency
                        )
                    elif routing_mode == "Optimal Tour":
                        path, total_distance, priority_score = optimal_tour_routing(
                            G, source, urgency
                        )
                    else:  # Priority Tour
                        path, total_distance, priority_score = priority_tour_routing(
                            G, source, urgency
                        )
                
                if path:
                    # Store results in session state
                    st.session_state['path'] = path
                    st.session_state['distance'] = total_distance
                    st.session_state['score'] = priority_score
                    st.session_state['source'] = source
                    st.session_state['destination'] = destination
                    st.session_state['routing_mode'] = routing_mode
                    st.session_state['is_tour'] = is_tour_mode
                else:
                    st.error("❌ No route found!")
                    # Clear session state if no route found
                    if 'path' in st.session_state:
                        del st.session_state['path']
        
        # Display map with route if available in session state
        if 'path' in st.session_state and st.session_state.get('source') == source:
            # Check if mode matches
            if st.session_state.get('routing_mode') == routing_mode:
                # For point-to-point, also check destination matches
                if not is_tour_mode and st.session_state.get('destination') != destination:
                    # Show default map
                    folium_map = create_folium_map(G, None, source, destination, is_tour=False)
                    st_folium(folium_map, width=900, height=600, key="map_default")
                else:
                    # Show map with the stored route
                    is_tour = st.session_state.get('is_tour', False)
                    folium_map = create_folium_map(
                        G, st.session_state['path'], source, destination, is_tour=is_tour
                    )
                    st_folium(folium_map, width=900, height=600, key="map_with_route")
            else:
                # Mode changed, show default map
                folium_map = create_folium_map(G, None, source, destination, is_tour=is_tour_mode)
                st_folium(folium_map, width=900, height=600, key="map_default")
        else:
            # Show default map without route
            folium_map = create_folium_map(G, None, source, destination, is_tour=is_tour_mode)
            st_folium(folium_map, width=900, height=600, key="map_default")
    
    with col2:
        # Dynamic header based on mode
        header = "📊 Tour Statistics" if is_tour_mode else "📊 Route Analysis"
        st.subheader(header)
        
        # Show LGA information
        st.markdown(f"#### {'Start Location' if is_tour_mode else 'Source Hub'}")
        source_data = get_lga_data(source)
        st.metric(
            label=source,
            value=f"{source_data['prevalence']*100:.0f}% Prevalence",
            delta=f"Pop: {source_data['population']:,}"
        )
        
        # Show destination only for point-to-point
        if not is_tour_mode and destination:
            st.markdown("#### Destination Clinic")
            dest_data = get_lga_data(destination)
            st.metric(
                label=destination,
                value=f"{dest_data['prevalence']*100:.0f}% Prevalence",
                delta=f"Pop: {dest_data['population']:,}"
            )
        
        # Show results if available
        should_show_results = False
        if 'path' in st.session_state and st.session_state.get('source') == source:
            if st.session_state.get('routing_mode') == routing_mode:
                if is_tour_mode or st.session_state.get('destination') == destination:
                    should_show_results = True
        
        if should_show_results:
            st.markdown("---")
            result_header = "#### 🎯 Tour Results" if is_tour_mode else "#### 🎯 Optimal Route Results"
            st.markdown(result_header)
            
            path = st.session_state['path']
            distance = st.session_state['distance']
            score = st.session_state['score']
            
            # Get priority rating
            rating_text, rating_color, rating_desc = get_priority_rating(score, distance)
            
            # Display priority rating with color-coded badge
            st.markdown(f"""
            <div style="
                background-color: {rating_color}15;
                border-left: 4px solid {rating_color};
                padding: 12px;
                border-radius: 4px;
                margin: 10px 0;
            ">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="
                        background-color: {rating_color};
                        color: white;
                        padding: 4px 12px;
                        border-radius: 12px;
                        font-weight: bold;
                        font-size: 0.9rem;
                    ">{rating_text}</span>
                    <span style="color: #555; font-size: 0.9rem;">{rating_desc}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Metrics
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Total Distance", f"{distance:.1f} km")
            with col_b:
                st.metric("Priority Score", f"{score:.2f}")
            
            # Tour-specific metrics
            if is_tour_mode:
                st.metric("LGAs Visited", f"{len(path)}/{len(G.nodes())}")
            else:
                st.metric("Route Segments", f"{len(path)-1} hops")
            
            # Route details
            st.markdown("#### 📍 Step-by-Step Route")
            route_details = get_route_details(G, path)
            
            for i, segment in enumerate(route_details, 1):
                with st.expander(f"Segment {i}: {segment['from']} → {segment['to']}"):
                    st.write(f"**Distance:** {segment['distance']} km")
                    st.write(f"**From Prevalence:** {segment['from_prevalence']*100:.0f}%")
                    st.write(f"**To Prevalence:** {segment['to_prevalence']*100:.0f}%")
            
            # Success message
            st.success(f"✅ Route calculated successfully! {len(path)} LGAs in path.")
    
    # Footer with project info
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888; font-size: 0.9rem;'>
        <strong>HealthRoute Africa</strong> | CSC 401 Project | 
        Priority-Weighted Dijkstra's Algorithm | O((E+V) log V) Complexity
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
