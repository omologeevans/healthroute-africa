#!/usr/bin/env python3
"""Check which LGAs are missing from the road network"""

import sys
sys.path.insert(0, r'c:\Users\Ismail\Documents\Hamplus\401 - Copy')

from data_loader import LGA_DATA, ROAD_NETWORK

# Get all LGAs from data
all_lgas = set(LGA_DATA.keys())
print(f"Total LGAs in LGA_DATA: {len(all_lgas)}")

# Get LGAs that appear in road network
lgas_in_network = set()
for road in ROAD_NETWORK:
    lgas_in_network.add(road[0])
    lgas_in_network.add(road[1])

print(f"LGAs in ROAD_NETWORK: {len(lgas_in_network)}")
print(f"Total road connections: {len(ROAD_NETWORK)}")

# Find missing LGAs
missing_lgas = all_lgas - lgas_in_network

if missing_lgas:
    print(f"\n❌ Missing {len(missing_lgas)} LGAs from road network:")
    
    # Group by state
    by_state = {}
    for lga in missing_lgas:
        state = lga.split(" - ")[0]
        if state not in by_state:
            by_state[state] = []
        by_state[state].append(lga)
    
    for state in sorted(by_state.keys()):
        print(f"\n{state}:")
        for lga in sorted(by_state[state]):
            print(f"  - {lga}")
else:
    print("\n✅ All LGAs are in the road network!")
