"""
HealthRoute Africa - Data Loader Module
Provides mock dataset of Nigerian cities with malaria prevalence statistics
and road network connections for medical supply routing simulation.
"""

import networkx as nx
from typing import Dict, List, Tuple


# State and LGA Structure (Only states with actual LGA data)
STATE_LGA_STRUCTURE = {
    "Adamawa": ["Yola North", "Yola South", "Demsa", "Fufore", "Ganye", "Girei", "Gombi"],
    "Akwa Ibom": ["Uyo", "Eket", "Ikot Ekpene", "Oron", "Abak", "Eastern Obolo", "Esit Eket"],
    "Bauchi": ["Bauchi", "Alkaleri", "Bogoro", "Damban", "Darazo", "Dass", "Gamawa"],
    "Borno": ["Maiduguri", "Bama", "Biu", "Abadam", "Askira/Uba", "Bayo", "Chibok"],
    "Cross River": ["Calabar Municipal", "Calabar South", "Abi", "Akamkpa", "Akpabuyo", "Bakassi", "Bekwarra"],
    "Delta": ["Warri South", "Sapele", "Ughelli North", "Ethiope East", "Oshimili South", "Aniocha North", "Bomadi"],
    "Edo": ["Oredo", "Egor", "Ikpoba-Okha", "Akoko-Edo", "Esan Central", "Esan North-East", "Esan South-East"],
    "Enugu": ["Enugu North", "Enugu South", "Enugu East", "Aninri", "Awgu", "Ezeagu", "Igbo Etiti"],
    "FCT": ["AMAC", "Abuja Municipal", "Bwari", "Gwagwalada", "Kuje", "Kwali", "Abaji"],
    "Imo": ["Owerri Municipal", "Owerri North", "Owerri West", "Aboh Mbaise", "Ahiazu Mbaise", "Ehime Mbano", "Ezinihitte"],
    "Kaduna": ["Kaduna North", "Kaduna South", "Birnin Gwari", "Chikun", "Giwa", "Igabi", "Ikara"],
    "Kano": ["Dala", "Kano Municipal", "Nassarawa", "Ajingi", "Albasu", "Bagwai", "Bebeji"],
    "Kogi": ["Lokoja", "Adavi", "Ajaokuta", "Ankpa", "Bassa", "Dekina", "Ibaji"],
    "Kwara": ["Ilorin South", "Ilorin West", "Ilorin East", "Asa", "Baruten", "Edu", "Ekiti"],
    "Lagos": ["Alimosho", "Ikeja", "Eti-Osa", "Agege", "Ajeromi-Ifelodun", "Amuwo-Odofin", "Apapa"],
    "Niger": ["Chanchaga", "Minna", "Bosso", "Agaie", "Agwara", "Bida", "Borgu"],
    "Ogun": ["Abeokuta South", "Ado-Odo/Ota", "Ifo", "Abeokuta North", "Egbado North", "Egbado South", "Ewekoro"],
    "Ondo": ["Akure South", "Odigbo", "Ondo West", "Akoko North-East", "Akoko North-West", "Akoko South-West", "Akure North"],
    "Osun": ["Osogbo", "Ife Central", "Ife East", "Aiyedaade", "Aiyedire", "Atakumosa East", "Boluwaduro"],
    "Oyo": ["Ibadan North", "Ogbomosho North", "Ibadan North-East", "Afijio", "Akinyele", "Atiba", "Atisbo"],
    "Plateau": ["Jos North", "Jos South", "Jos East", "Barkin Ladi", "Bassa", "Bokkos", "Kanam"],
    "Rivers": ["Port Harcourt", "Obio-Akpor", "Eleme", "Abua/Odual", "Ahoada East", "Ahoada West", "Akuku-Toru"],
    "Sokoto": ["Sokoto North", "Sokoto South", "Binji", "Bodinga", "Dange Shuni", "Gada", "Goronyo"]
}

# LGA Data: Local Government Areas as routing nodes
# Format: "State - LGA": {data}
LGA_DATA = {
    # Lagos State LGAs (7 total)
    "Lagos - Alimosho": {
        "coords": (6.5244, 3.3792),
        "prevalence": 0.25,
        "population": 14000000,
        "state": "Lagos"
    },
    "Lagos - Ikeja": {
        "coords": (6.5964, 3.3406),
        "prevalence": 0.18,
        "population": 600000,
        "state": "Lagos"
    },
    "Lagos - Eti-Osa": {
        "coords": (6.4698, 3.6012),
        "prevalence": 0.20,
        "population": 287785,
        "state": "Lagos"
    },
    "Lagos - Agege": {
        "coords": (6.6158, 3.3211),
        "prevalence": 0.23,
        "population": 459939,
        "state": "Lagos"
    },
    "Lagos - Ajeromi-Ifelodun": {
        "coords": (6.4588, 3.3299),
        "prevalence": 0.26,
        "population": 684105,
        "state": "Lagos"
    },
    "Lagos - Amuwo-Odofin": {
        "coords": (6.4417, 3.2902),
        "prevalence": 0.22,
        "population": 318166,
        "state": "Lagos"
    },
    "Lagos - Apapa": {
        "coords": (6.4489, 3.3594),
        "prevalence": 0.19,
        "population": 217362,
        "state": "Lagos"
    },
    
    # Ogun State LGAs (7 total)
    "Ogun - Abeokuta South": {
        "coords": (7.1475, 3.3619),
        "prevalence": 0.32,
        "population": 593100,
        "state": "Ogun"
    },
    "Ogun - Ado-Odo/Ota": {
        "coords": (6.6988, 3.2004),
        "prevalence": 0.22,
        "population": 350000,
        "state": "Ogun"
    },
    "Ogun - Ifo": {
        "coords": (6.8489, 3.6458),
        "prevalence": 0.28,
        "population": 250000,
        "state": "Ogun"
    },
    "Ogun - Abeokuta North": {
        "coords": (7.1675, 3.3519),
        "prevalence": 0.30,
        "population": 200000,
        "state": "Ogun"
    },
    "Ogun - Egbado North": {
        "coords": (6.9833, 2.9167),
        "prevalence": 0.35,
        "population": 150000,
        "state": "Ogun"
    },
    "Ogun - Egbado South": {
        "coords": (6.8667, 2.9333),
        "prevalence": 0.33,
        "population": 140000,
        "state": "Ogun"
    },
    "Ogun - Ewekoro": {
        "coords": (6.9333, 3.2000),
        "prevalence": 0.29,
        "population": 130000,
        "state": "Ogun"
    },
    
    # Oyo State LGAs (7 total)
    "Oyo - Ibadan North": {
        "coords": (7.3775, 3.9470),
        "prevalence": 0.38,
        "population": 3500000,
        "state": "Oyo"
    },
    "Oyo - Ogbomosho North": {
        "coords": (8.1335, 4.2407),
        "prevalence": 0.78,
        "population": 645000,
        "state": "Oyo"
    },
    "Oyo - Ibadan North-East": {
        "coords": (7.4000, 3.9300),
        "prevalence": 0.40,
        "population": 300000,
        "state": "Oyo"
    },
    "Oyo - Afijio": {
        "coords": (7.8667, 3.9500),
        "prevalence": 0.42,
        "population": 180000,
        "state": "Oyo"
    },
    "Oyo - Akinyele": {
        "coords": (7.5333, 3.9833),
        "prevalence": 0.39,
        "population": 220000,
        "state": "Oyo"
    },
    "Oyo - Atiba": {
        "coords": (8.0000, 4.0000),
        "prevalence": 0.41,
        "population": 170000,
        "state": "Oyo"
    },
    "Oyo - Atisbo": {
        "coords": (8.6667, 3.5000),
        "prevalence": 0.45,
        "population": 160000,
        "state": "Oyo"
    },
    
    # Osun State LGAs (7 total)
    "Osun - Osogbo": {
        "coords": (7.7667, 4.5667),
        "prevalence": 0.41,
        "population": 500000,
        "state": "Osun"
    },
    "Osun - Ife Central": {
        "coords": (7.4833, 4.5600),
        "prevalence": 0.43,
        "population": 350000,
        "state": "Osun"
    },
    "Osun - Ife East": {
        "coords": (7.5000, 4.5833),
        "prevalence": 0.44,
        "population": 200000,
        "state": "Osun"
    },
    "Osun - Aiyedaade": {
        "coords": (7.3667, 4.1333),
        "prevalence": 0.46,
        "population": 150000,
        "state": "Osun"
    },
    "Osun - Aiyedire": {
        "coords": (7.6667, 4.2500),
        "prevalence": 0.42,
        "population": 140000,
        "state": "Osun"
    },
    "Osun - Atakumosa East": {
        "coords": (7.6333, 4.7000),
        "prevalence": 0.45,
        "population": 130000,
        "state": "Osun"
    },
    "Osun - Boluwaduro": {
        "coords": (7.7333, 4.7333),
        "prevalence": 0.40,
        "population": 120000,
        "state": "Osun"
    },
    
    # Kwara State LGAs (7 total)
    "Kwara - Ilorin South": {
        "coords": (8.4966, 4.5424),
        "prevalence": 0.44,
        "population": 908490,
        "state": "Kwara"
    },
    "Kwara - Ilorin West": {
        "coords": (8.4800, 4.5200),
        "prevalence": 0.43,
        "population": 350000,
        "state": "Kwara"
    },
    "Kwara - Ilorin East": {
        "coords": (8.5100, 4.5600),
        "prevalence": 0.45,
        "population": 300000,
        "state": "Kwara"
    },
    "Kwara - Asa": {
        "coords": (8.4000, 4.4000),
        "prevalence": 0.47,
        "population": 180000,
        "state": "Kwara"
    },
    "Kwara - Baruten": {
        "coords": (9.4500, 3.1667),
        "prevalence": 0.50,
        "population": 160000,
        "state": "Kwara"
    },
    "Kwara - Edu": {
        "coords": (8.9000, 4.9500),
        "prevalence": 0.48,
        "population": 170000,
        "state": "Kwara"
    },
    "Kwara - Ekiti": {
        "coords": (8.1333, 4.8333),
        "prevalence": 0.46,
        "population": 150000,
        "state": "Kwara"
    },
    
    # Ondo State LGAs (7 total)
    "Ondo - Akure South": {
        "coords": (7.2571, 5.2058),
        "prevalence": 0.58,
        "population": 484798,
        "state": "Ondo"
    },
    "Ondo - Odigbo": {
        "coords": (6.7500, 4.8833),
        "prevalence": 0.55,
        "population": 150000,
        "state": "Ondo"
    },
    "Ondo - Ondo West": {
        "coords": (7.0936, 4.8350),
        "prevalence": 0.58,
        "population": 275000,
        "state": "Ondo"
    },
    "Ondo - Akoko North-East": {
        "coords": (7.5667, 5.7833),
        "prevalence": 0.60,
        "population": 200000,
        "state": "Ondo"
    },
    "Ondo - Akoko North-West": {
        "coords": (7.5333, 5.7500),
        "prevalence": 0.59,
        "population": 190000,
        "state": "Ondo"
    },
    "Ondo - Akoko South-West": {
        "coords": (7.4833, 5.7167),
        "prevalence": 0.57,
        "population": 180000,
        "state": "Ondo"
    },
    "Ondo - Akure North": {
        "coords": (7.3000, 5.2500),
        "prevalence": 0.56,
        "population": 170000,
        "state": "Ondo"
    },
    
    # Edo State LGAs (7 total)
    "Edo - Oredo": {
        "coords": (6.3350, 5.6037),
        "prevalence": 0.75,
        "population": 1500000,
        "state": "Edo"
    },
    "Edo - Egor": {
        "coords": (6.3400, 5.6300),
        "prevalence": 0.73,
        "population": 350000,
        "state": "Edo"
    },
    "Edo - Ikpoba-Okha": {
        "coords": (6.3600, 5.6500),
        "prevalence": 0.74,
        "population": 300000,
        "state": "Edo"
    },
    "Edo - Akoko-Edo": {
        "coords": (7.2000, 6.5000),
        "prevalence": 0.70,
        "population": 250000,
        "state": "Edo"
    },
    "Edo - Esan Central": {
        "coords": (6.5500, 6.2000),
        "prevalence": 0.72,
        "population": 200000,
        "state": "Edo"
    },
    "Edo - Esan North-East": {
        "coords": (6.6000, 6.3000),
        "prevalence": 0.71,
        "population": 180000,
        "state": "Edo"
    },
    "Edo - Esan South-East": {
        "coords": (6.5000, 6.1500),
        "prevalence": 0.69,
        "population": 170000,
        "state": "Edo"
    },
    
    # Delta State LGAs (7 total)
    "Delta - Warri South": {
        "coords": (5.5167, 5.7500),
        "prevalence": 0.72,
        "population": 536023,
        "state": "Delta"
    },
    "Delta - Sapele": {
        "coords": (5.8939, 5.6769),
        "prevalence": 0.60,
        "population": 180000,
        "state": "Delta"
    },
    "Delta - Ughelli North": {
        "coords": (5.4894, 6.0039),
        "prevalence": 0.62,
        "population": 200000,
        "state": "Delta"
    },
    "Delta - Ethiope East": {
        "coords": (5.7833, 6.0833),
        "prevalence": 0.15,
        "population": 30000,
        "state": "Delta"
    },
    "Delta - Oshimili South": {
        "coords": (6.1987, 6.7337),
        "prevalence": 0.67,
        "population": 282000,
        "state": "Delta"
    },
    "Delta - Aniocha North": {
        "coords": (6.3500, 6.4500),
        "prevalence": 0.65,
        "population": 170000,
        "state": "Delta"
    },
    "Delta - Bomadi": {
        "coords": (5.1500, 5.9000),
        "prevalence": 0.68,
        "population": 150000,
        "state": "Delta"
    },
    
    # Rivers State LGAs (7 total)
    "Rivers - Port Harcourt": {
        "coords": (4.8156, 7.0498),
        "prevalence": 0.68,
        "population": 2000000,
        "state": "Rivers"
    },
    "Rivers - Obio-Akpor": {
        "coords": (4.8500, 7.0000),
        "prevalence": 0.66,
        "population": 400000,
        "state": "Rivers"
    },
    "Rivers - Eleme": {
        "coords": (4.7667, 7.1167),
        "prevalence": 0.67,
        "population": 200000,
        "state": "Rivers"
    },
    "Rivers - Abua/Odual": {
        "coords": (4.8500, 6.6500),
        "prevalence": 0.70,
        "population": 180000,
        "state": "Rivers"
    },
    "Rivers - Ahoada East": {
        "coords": (5.0833, 6.6500),
        "prevalence": 0.69,
        "population": 170000,
        "state": "Rivers"
    },
    "Rivers - Ahoada West": {
        "coords": (5.0500, 6.6000),
        "prevalence": 0.71,
        "population": 160000,
        "state": "Rivers"
    },
    "Rivers - Akuku-Toru": {
        "coords": (4.7500, 6.5000),
        "prevalence": 0.72,
        "population": 150000,
        "state": "Rivers"
    },
    
    # Cross River State LGAs (7 total)
    "Cross River - Calabar Municipal": {
        "coords": (4.9517, 8.3417),
        "prevalence": 0.65,
        "population": 461796,
        "state": "Cross River"
    },
    "Cross River - Calabar South": {
        "coords": (4.9300, 8.3200),
        "prevalence": 0.64,
        "population": 250000,
        "state": "Cross River"
    },
    "Cross River - Abi": {
        "coords": (5.8167, 8.1333),
        "prevalence": 0.66,
        "population": 180000,
        "state": "Cross River"
    },
    "Cross River - Akamkpa": {
        "coords": (5.0167, 8.1500),
        "prevalence": 0.67,
        "population": 170000,
        "state": "Cross River"
    },
    "Cross River - Akpabuyo": {
        "coords": (4.8833, 8.2500),
        "prevalence": 0.63,
        "population": 160000,
        "state": "Cross River"
    },
    "Cross River - Bakassi": {
        "coords": (4.6667, 8.5500),
        "prevalence": 0.68,
        "population": 150000,
        "state": "Cross River"
    },
    "Cross River - Bekwarra": {
        "coords": (6.7833, 8.8333),
        "prevalence": 0.62,
        "population": 140000,
        "state": "Cross River"
    },
    
    # Akwa Ibom State LGAs (7 total)
    "Akwa Ibom - Uyo": {
        "coords": (5.0378, 7.9085),
        "prevalence": 0.70,
        "population": 436606,
        "state": "Akwa Ibom"
    },
    "Akwa Ibom - Eket": {
        "coords": (4.6425, 7.9244),
        "prevalence": 0.72,
        "population": 250000,
        "state": "Akwa Ibom"
    },
    "Akwa Ibom - Ikot Ekpene": {
        "coords": (5.1833, 7.7167),
        "prevalence": 0.71,
        "population": 200000,
        "state": "Akwa Ibom"
    },
    "Akwa Ibom - Oron": {
        "coords": (4.8167, 8.2333),
        "prevalence": 0.73,
        "population": 180000,
        "state": "Akwa Ibom"
    },
    "Akwa Ibom - Abak": {
        "coords": (4.9833, 7.7833),
        "prevalence": 0.69,
        "population": 170000,
        "state": "Akwa Ibom"
    },
    "Akwa Ibom - Eastern Obolo": {
        "coords": (4.5000, 7.7500),
        "prevalence": 0.74,
        "population": 160000,
        "state": "Akwa Ibom"
    },
    "Akwa Ibom - Esit Eket": {
        "coords": (4.6833, 7.8500),
        "prevalence": 0.68,
        "population": 150000,
        "state": "Akwa Ibom"
    },
    
    # Enugu State LGAs (7 total)
    "Enugu - Enugu North": {
        "coords": (6.5244, 7.5105),
        "prevalence": 0.62,
        "population": 800000,
        "state": "Enugu"
    },
    "Enugu - Enugu South": {
        "coords": (6.4500, 7.4900),
        "prevalence": 0.61,
        "population": 300000,
        "state": "Enugu"
    },
    "Enugu - Enugu East": {
        "coords": (6.5500, 7.5300),
        "prevalence": 0.63,
        "population": 250000,
        "state": "Enugu"
    },
    "Enugu - Aninri": {
        "coords": (6.4167, 7.2833),
        "prevalence": 0.60,
        "population": 200000,
        "state": "Enugu"
    },
    "Enugu - Awgu": {
        "coords": (6.0833, 7.4833),
        "prevalence": 0.64,
        "population": 180000,
        "state": "Enugu"
    },
    "Enugu - Ezeagu": {
        "coords": (6.4500, 7.0500),
        "prevalence": 0.59,
        "population": 170000,
        "state": "Enugu"
    },
    "Enugu - Igbo Etiti": {
        "coords": (6.7000, 7.2500),
        "prevalence": 0.58,
        "population": 160000,
        "state": "Enugu"
    },
    
    # Imo State LGAs (7 total)
    "Imo - Owerri Municipal": {
        "coords": (5.4840, 7.0240),
        "prevalence": 0.64,
        "population": 401873,
        "state": "Imo"
    },
    "Imo - Owerri North": {
        "coords": (5.5000, 7.0500),
        "prevalence": 0.65,
        "population": 250000,
        "state": "Imo"
    },
    "Imo - Owerri West": {
        "coords": (5.4500, 7.0000),
        "prevalence": 0.63,
        "population": 220000,
        "state": "Imo"
    },
    "Imo - Aboh Mbaise": {
        "coords": (5.5667, 6.9167),
        "prevalence": 0.66,
        "population": 200000,
        "state": "Imo"
    },
    "Imo - Ahiazu Mbaise": {
        "coords": (5.5333, 6.8833),
        "prevalence": 0.67,
        "population": 180000,
        "state": "Imo"
    },
    "Imo - Ehime Mbano": {
        "coords": (5.7000, 7.1500),
        "prevalence": 0.62,
        "population": 170000,
        "state": "Imo"
    },
    "Imo - Ezinihitte": {
        "coords": (5.6500, 6.9500),
        "prevalence": 0.68,
        "population": 160000,
        "state": "Imo"
    },
    
    # FCT LGAs (7 total)
    "FCT - AMAC": {
        "coords": (9.0765, 7.3986),
        "prevalence": 0.45,
        "population": 3000000,
        "state": "FCT"
    },
    "FCT - Abuja Municipal": {
        "coords": (9.0579, 7.4951),
        "prevalence": 0.44,
        "population": 1500000,
        "state": "FCT"
    },
    "FCT - Bwari": {
        "coords": (9.2833, 7.3833),
        "prevalence": 0.46,
        "population": 400000,
        "state": "FCT"
    },
    "FCT - Gwagwalada": {
        "coords": (8.9500, 7.0833),
        "prevalence": 0.47,
        "population": 350000,
        "state": "FCT"
    },
    "FCT - Kuje": {
        "coords": (8.8833, 7.2167),
        "prevalence": 0.48,
        "population": 300000,
        "state": "FCT"
    },
    "FCT - Kwali": {
        "coords": (8.8833, 7.0167),
        "prevalence": 0.49,
        "population": 250000,
        "state": "FCT"
    },
    "FCT - Abaji": {
        "coords": (8.9667, 6.7167),
        "prevalence": 0.50,
        "population": 200000,
        "state": "FCT"
    },
    
    # Plateau State LGAs (7 total)
    "Plateau - Jos North": {
        "coords": (9.8965, 8.8583),
        "prevalence": 0.35,
        "population": 900000,
        "state": "Plateau"
    },
    "Plateau - Jos South": {
        "coords": (9.8500, 8.8500),
        "prevalence": 0.36,
        "population": 400000,
        "state": "Plateau"
    },
    "Plateau - Jos East": {
        "coords": (9.9500, 8.9000),
        "prevalence": 0.34,
        "population": 300000,
        "state": "Plateau"
    },
    "Plateau - Barkin Ladi": {
        "coords": (9.5333, 8.9000),
        "prevalence": 0.37,
        "population": 250000,
        "state": "Plateau"
    },
    "Plateau - Bassa": {
        "coords": (9.9333, 8.7333),
        "prevalence": 0.38,
        "population": 220000,
        "state": "Plateau"
    },
    "Plateau - Bokkos": {
        "coords": (9.3000, 9.3000),
        "prevalence": 0.33,
        "population": 200000,
        "state": "Plateau"
    },
    "Plateau - Kanam": {
        "coords": (9.9667, 9.5000),
        "prevalence": 0.39,
        "population": 180000,
        "state": "Plateau"
    },
    
    # Niger State LGAs (7 total)
    "Niger - Chanchaga": {
        "coords": (9.6139, 6.5569),
        "prevalence": 0.50,
        "population": 304113,
        "state": "Niger"
    },
    "Niger - Minna": {
        "coords": (9.6167, 6.5500),
        "prevalence": 0.49,
        "population": 250000,
        "state": "Niger"
    },
    "Niger - Bosso": {
        "coords": (9.5667, 6.5167),
        "prevalence": 0.51,
        "population": 200000,
        "state": "Niger"
    },
    "Niger - Agaie": {
        "coords": (9.0167, 6.3333),
        "prevalence": 0.52,
        "population": 180000,
        "state": "Niger"
    },
    "Niger - Agwara": {
        "coords": (11.1000, 4.0833),
        "prevalence": 0.53,
        "population": 170000,
        "state": "Niger"
    },
    "Niger - Bida": {
        "coords": (9.0833, 6.0167),
        "prevalence": 0.48,
        "population": 160000,
        "state": "Niger"
    },
    "Niger - Borgu": {
        "coords": (10.4500, 4.4333),
        "prevalence": 0.54,
        "population": 150000,
        "state": "Niger"
    },
    
    # Kogi State LGAs (7 total)
    "Kogi - Lokoja": {
        "coords": (7.7974, 6.7437),
        "prevalence": 0.55,
        "population": 195261,
        "state": "Kogi"
    },
    "Kogi - Adavi": {
        "coords": (7.6667, 6.5000),
        "prevalence": 0.56,
        "population": 180000,
        "state": "Kogi"
    },
    "Kogi - Ajaokuta": {
        "coords": (7.5500, 6.6500),
        "prevalence": 0.54,
        "population": 170000,
        "state": "Kogi"
    },
    "Kogi - Ankpa": {
        "coords": (7.4000, 7.4000),
        "prevalence": 0.57,
        "population": 160000,
        "state": "Kogi"
    },
    "Kogi - Bassa": {
        "coords": (7.9167, 6.5167),
        "prevalence": 0.53,
        "population": 150000,
        "state": "Kogi"
    },
    "Kogi - Dekina": {
        "coords": (7.6833, 7.7000),
        "prevalence": 0.58,
        "population": 140000,
        "state": "Kogi"
    },
    "Kogi - Ibaji": {
        "coords": (7.0000, 6.7500),
        "prevalence": 0.52,
        "population": 130000,
        "state": "Kogi"
    },
    
    # Kano State LGAs (7 total)
    "Kano - Dala": {
        "coords": (12.0022, 8.5919),
        "prevalence": 0.52,
        "population": 4000000,
        "state": "Kano"
    },
    "Kano - Kano Municipal": {
        "coords": (12.0000, 8.5200),
        "prevalence": 0.51,
        "population": 1500000,
        "state": "Kano"
    },
    "Kano - Nassarawa": {
        "coords": (12.0500, 8.5500),
        "prevalence": 0.53,
        "population": 800000,
        "state": "Kano"
    },
    "Kano - Ajingi": {
        "coords": (11.9333, 8.8500),
        "prevalence": 0.50,
        "population": 400000,
        "state": "Kano"
    },
    "Kano - Albasu": {
        "coords": (11.9833, 9.0833),
        "prevalence": 0.54,
        "population": 350000,
        "state": "Kano"
    },
    "Kano - Bagwai": {
        "coords": (12.2833, 8.2000),
        "prevalence": 0.49,
        "population": 300000,
        "state": "Kano"
    },
    "Kano - Bebeji": {
        "coords": (11.7333, 8.2500),
        "prevalence": 0.55,
        "population": 280000,
        "state": "Kano"
    },
    
    # Kaduna State LGAs (7 total)
    "Kaduna - Kaduna North": {
        "coords": (10.5105, 7.4165),
        "prevalence": 0.48,
        "population": 1600000,
        "state": "Kaduna"
    },
    "Kaduna - Kaduna South": {
        "coords": (10.5000, 7.4000),
        "prevalence": 0.47,
        "population": 800000,
        "state": "Kaduna"
    },
    "Kaduna - Birnin Gwari": {
        "coords": (10.7500, 6.5500),
        "prevalence": 0.50,
        "population": 400000,
        "state": "Kaduna"
    },
    "Kaduna - Chikun": {
        "coords": (10.5500, 7.3500),
        "prevalence": 0.49,
        "population": 350000,
        "state": "Kaduna"
    },
    "Kaduna - Giwa": {
        "coords": (11.2833, 7.7167),
        "prevalence": 0.46,
        "population": 300000,
        "state": "Kaduna"
    },
    "Kaduna - Igabi": {
        "coords": (10.8333, 7.7167),
        "prevalence": 0.51,
        "population": 280000,
        "state": "Kaduna"
    },
    "Kaduna - Ikara": {
        "coords": (11.2167, 8.2167),
        "prevalence": 0.45,
        "population": 260000,
        "state": "Kaduna"
    },
    
    # Sokoto State LGAs (7 total)
    "Sokoto - Sokoto North": {
        "coords": (13.0622, 5.2339),
        "prevalence": 0.56,
        "population": 563861,
        "state": "Sokoto"
    },
    "Sokoto - Sokoto South": {
        "coords": (13.0500, 5.2000),
        "prevalence": 0.55,
        "population": 350000,
        "state": "Sokoto"
    },
    "Sokoto - Binji": {
        "coords": (13.2167, 5.6167),
        "prevalence": 0.57,
        "population": 250000,
        "state": "Sokoto"
    },
    "Sokoto - Bodinga": {
        "coords": (12.8500, 5.1500),
        "prevalence": 0.58,
        "population": 220000,
        "state": "Sokoto"
    },
    "Sokoto - Dange Shuni": {
        "coords": (13.5500, 5.3833),
        "prevalence": 0.54,
        "population": 200000,
        "state": "Sokoto"
    },
    "Sokoto - Gada": {
        "coords": (13.7833, 5.6500),
        "prevalence": 0.59,
        "population": 180000,
        "state": "Sokoto"
    },
    "Sokoto - Goronyo": {
        "coords": (13.4333, 5.6667),
        "prevalence": 0.53,
        "population": 170000,
        "state": "Sokoto"
    },
    
    # Borno State LGAs (7 total)
    "Borno - Maiduguri": {
        "coords": (11.8333, 13.1500),
        "prevalence": 0.60,
        "population": 749000,
        "state": "Borno"
    },
    "Borno - Bama": {
        "coords": (11.5167, 13.6833),
        "prevalence": 0.62,
        "population": 350000,
        "state": "Borno"
    },
    "Borno - Biu": {
        "coords": (10.6167, 12.1833),
        "prevalence": 0.61,
        "population": 300000,
        "state": "Borno"
    },
    "Borno - Abadam": {
        "coords": (13.2667, 13.2000),
        "prevalence": 0.63,
        "population": 250000,
        "state": "Borno"
    },
    "Borno - Askira/Uba": {
        "coords": (10.7667, 12.0833),
        "prevalence": 0.59,
        "population": 220000,
        "state": "Borno"
    },
    "Borno - Bayo": {
        "coords": (10.7500, 11.6667),
        "prevalence": 0.64,
        "population": 200000,
        "state": "Borno"
    },
    "Borno - Chibok": {
        "coords": (10.8667, 12.8333),
        "prevalence": 0.58,
        "population": 180000,
        "state": "Borno"
    },
    
    # Bauchi State LGAs (7 total)
    "Bauchi - Bauchi": {
        "coords": (10.3158, 9.8442),
        "prevalence": 0.54,
        "population": 493810,
        "state": "Bauchi"
    },
    "Bauchi - Alkaleri": {
        "coords": (10.3000, 10.2500),
        "prevalence": 0.55,
        "population": 300000,
        "state": "Bauchi"
    },
    "Bauchi - Bogoro": {
        "coords": (9.6167, 9.6167),
        "prevalence": 0.53,
        "population": 250000,
        "state": "Bauchi"
    },
    "Bauchi - Damban": {
        "coords": (10.7167, 10.7167),
        "prevalence": 0.56,
        "population": 220000,
        "state": "Bauchi"
    },
    "Bauchi - Darazo": {
        "coords": (10.9833, 10.4000),
        "prevalence": 0.52,
        "population": 200000,
        "state": "Bauchi"
    },
    "Bauchi - Dass": {
        "coords": (9.5167, 9.9667),
        "prevalence": 0.57,
        "population": 180000,
        "state": "Bauchi"
    },
    "Bauchi - Gamawa": {
        "coords": (11.8333, 10.5333),
        "prevalence": 0.51,
        "population": 170000,
        "state": "Bauchi"
    },
    
    # Adamawa State LGAs (7 total)
    "Adamawa - Yola North": {
        "coords": (9.2094, 12.4534),
        "prevalence": 0.59,
        "population": 336648,
        "state": "Adamawa"
    },
    "Adamawa - Yola South": {
        "coords": (9.1900, 12.4300),
        "prevalence": 0.60,
        "population": 250000,
        "state": "Adamawa"
    },
    "Adamawa - Demsa": {
        "coords": (9.4500, 12.1500),
        "prevalence": 0.58,
        "population": 200000,
        "state": "Adamawa"
    },
    "Adamawa - Fufore": {
        "coords": (9.2667, 12.6667),
        "prevalence": 0.61,
        "population": 180000,
        "state": "Adamawa"
    },
    "Adamawa - Ganye": {
        "coords": (8.4333, 12.0667),
        "prevalence": 0.62,
        "population": 170000,
        "state": "Adamawa"
    },
    "Adamawa - Girei": {
        "coords": (9.3500, 12.5500),
        "prevalence": 0.57,
        "population": 160000,
        "state": "Adamawa"
    },
    "Adamawa - Gombi": {
        "coords": (10.1667, 12.7333),
        "prevalence": 0.63,
        "population": 150000,
        "state": "Adamawa"
    }
}


# Road network: (lga1, lga2, distance_in_km)
# Comprehensive network connecting all 161 LGAs
ROAD_NETWORK = [
    # ===== INTRA-STATE CONNECTIONS (LGAs within same state) =====
    
    # Lagos State - Internal connections
    ("Lagos - Alimosho", "Lagos - Ikeja", 15),
    ("Lagos - Alimosho", "Lagos - Agege", 10),
    ("Lagos - Ikeja", "Lagos - Agege", 8),
    ("Lagos - Ikeja", "Lagos - Eti-Osa", 25),
    ("Lagos - Eti-Osa", "Lagos - Apapa", 12),
    ("Lagos - Apapa", "Lagos - Ajeromi-Ifelodun", 8),
    ("Lagos - Ajeromi-Ifelodun", "Lagos - Amuwo-Odofin", 10),
    
    # Ogun State - Internal connections
    ("Ogun - Abeokuta South", "Ogun - Abeokuta North", 5),
    ("Ogun - Abeokuta South", "Ogun - Ewekoro", 20),
    ("Ogun - Ado-Odo/Ota", "Ogun - Ifo", 15),
    ("Ogun - Ifo", "Ogun - Ewekoro", 25),
    ("Ogun - Egbado North", "Ogun - Egbado South", 12),
    
    # Oyo State - Internal connections
    ("Oyo - Ibadan North", "Oyo - Ibadan North-East", 8),
    ("Oyo - Ibadan North", "Oyo - Akinyele", 15),
    ("Oyo - Ogbomosho North", "Oyo - Atiba", 20),
    ("Oyo - Afijio", "Oyo - Atisbo", 25),
    
    # Osun State - Internal connections
    ("Osun - Osogbo", "Osun - Ife Central", 40),
    ("Osun - Ife Central", "Osun - Ife East", 10),
    ("Osun - Aiyedaade", "Osun - Aiyedire", 15),
    ("Osun - Atakumosa East", "Osun - Boluwaduro", 18),
    
    # Kwara State - Internal connections
    ("Kwara - Ilorin South", "Kwara - Ilorin West", 8),
    ("Kwara - Ilorin West", "Kwara - Ilorin East", 10),
    ("Kwara - Asa", "Kwara - Ilorin South", 25),
    ("Kwara - Baruten", "Kwara - Edu", 40),
    ("Kwara - Edu", "Kwara - Ekiti", 30),
    
    # Ondo State - Internal connections
    ("Ondo - Akure South", "Ondo - Akure North", 12),
    ("Ondo - Odigbo", "Ondo - Ondo West", 60),
    ("Ondo - Ondo West", "Ondo - Akure South", 70),
    ("Ondo - Akoko North-East", "Ondo - Akoko North-West", 15),
    ("Ondo - Akoko North-West", "Ondo - Akoko South-West", 20),
    
    # Edo State - Internal connections
    ("Edo - Oredo", "Edo - Egor", 10),
    ("Edo - Egor", "Edo - Ikpoba-Okha", 12),
    ("Edo - Akoko-Edo", "Edo - Esan Central", 40),
    ("Edo - Esan Central", "Edo - Esan North-East", 15),
    ("Edo - Esan North-East", "Edo - Esan South-East", 18),
    
    # Delta State - Internal connections
    ("Delta - Warri South", "Delta - Sapele", 50),
    ("Delta - Sapele", "Delta - Ughelli North", 40),
    ("Delta - Ughelli North", "Delta - Ethiope East", 50),
    ("Delta - Ethiope East", "Delta - Oshimili South", 50),
    ("Delta - Oshimili South", "Delta - Aniocha North", 30),
    ("Delta - Warri South", "Delta - Bomadi", 45),
    
    # Rivers State - Internal connections
    ("Rivers - Port Harcourt", "Rivers - Obio-Akpor", 10),
    ("Rivers - Port Harcourt", "Rivers - Eleme", 20),
    ("Rivers - Abua/Odual", "Rivers - Ahoada East", 25),
    ("Rivers - Ahoada East", "Rivers - Ahoada West", 15),
    ("Rivers - Akuku-Toru", "Rivers - Port Harcourt", 60),
    
    # Cross River State - Internal connections
    ("Cross River - Calabar Municipal", "Cross River - Calabar South", 8),
    ("Cross River - Abi", "Cross River - Akamkpa", 30),
    ("Cross River - Akamkpa", "Cross River - Akpabuyo", 25),
    ("Cross River - Bakassi", "Cross River - Calabar Municipal", 40),
    ("Cross River - Bekwarra", "Cross River - Abi", 50),
    
    # Akwa Ibom State - Internal connections
    ("Akwa Ibom - Uyo", "Akwa Ibom - Eket", 45),
    ("Akwa Ibom - Uyo", "Akwa Ibom - Ikot Ekpene", 30),
    ("Akwa Ibom - Oron", "Akwa Ibom - Eket", 35),
    ("Akwa Ibom - Abak", "Akwa Ibom - Ikot Ekpene", 20),
    ("Akwa Ibom - Eastern Obolo", "Akwa Ibom - Esit Eket", 25),
    
    # Enugu State - Internal connections
    ("Enugu - Enugu North", "Enugu - Enugu South", 8),
    ("Enugu - Enugu South", "Enugu - Enugu East", 10),
    ("Enugu - Aninri", "Enugu - Awgu", 25),
    ("Enugu - Awgu", "Enugu - Ezeagu", 20),
    ("Enugu - Igbo Etiti", "Enugu - Enugu North", 30),
    
    # Imo State - Internal connections
    ("Imo - Owerri Municipal", "Imo - Owerri North", 8),
    ("Imo - Owerri North", "Imo - Owerri West", 10),
    ("Imo - Aboh Mbaise", "Imo - Ahiazu Mbaise", 15),
    ("Imo - Ehime Mbano", "Imo - Owerri Municipal", 25),
    ("Imo - Ezinihitte", "Imo - Aboh Mbaise", 18),
    
    # FCT - Internal connections
    ("FCT - AMAC", "FCT - Abuja Municipal", 5),
    ("FCT - AMAC", "FCT - Bwari", 20),
    ("FCT - Gwagwalada", "FCT - Kuje", 15),
    ("FCT - Kuje", "FCT - Kwali", 18),
    ("FCT - Kwali", "FCT - Abaji", 20),
    
    # Plateau State - Internal connections
    ("Plateau - Jos North", "Plateau - Jos South", 8),
    ("Plateau - Jos South", "Plateau - Jos East", 12),
    ("Plateau - Barkin Ladi", "Plateau - Jos North", 25),
    ("Plateau - Bassa", "Plateau - Jos East", 20),
    ("Plateau - Bokkos", "Plateau - Kanam", 30),
    
    # Niger State - Internal connections
    ("Niger - Chanchaga", "Niger - Minna", 5),
    ("Niger - Minna", "Niger - Bosso", 10),
    ("Niger - Agaie", "Niger - Bida", 25),
    ("Niger - Agwara", "Niger - Borgu", 40),
    
    # Kogi State - Internal connections
    ("Kogi - Lokoja", "Kogi - Adavi", 20),
    ("Kogi - Adavi", "Kogi - Ajaokuta", 15),
    ("Kogi - Ankpa", "Kogi - Dekina", 25),
    ("Kogi - Bassa", "Kogi - Lokoja", 30),
    ("Kogi - Ibaji", "Kogi - Dekina", 35),
    
    # Kano State - Internal connections
    ("Kano - Dala", "Kano - Kano Municipal", 5),
    ("Kano - Kano Municipal", "Kano - Nassarawa", 8),
    ("Kano - Ajingi", "Kano - Albasu", 20),
    ("Kano - Bagwai", "Kano - Bebeji", 25),
    
    # Kaduna State - Internal connections
    ("Kaduna - Kaduna North", "Kaduna - Kaduna South", 8),
    ("Kaduna - Birnin Gwari", "Kaduna - Chikun", 30),
    ("Kaduna - Giwa", "Kaduna - Igabi", 20),
    ("Kaduna - Ikara", "Kaduna - Giwa", 25),
    
    # Sokoto State - Internal connections
    ("Sokoto - Sokoto North", "Sokoto - Sokoto South", 8),
    ("Sokoto - Binji", "Sokoto - Bodinga", 20),
    ("Sokoto - Dange Shuni", "Sokoto - Gada", 25),
    ("Sokoto - Goronyo", "Sokoto - Gada", 18),
    
    # Borno State - Internal connections
    ("Borno - Maiduguri", "Borno - Bama", 60),
    ("Borno - Biu", "Borno - Askira/Uba", 20),
    ("Borno - Abadam", "Borno - Maiduguri", 80),
    ("Borno - Bayo", "Borno - Chibok", 25),
    
    # Bauchi State - Internal connections
    ("Bauchi - Bauchi", "Bauchi - Alkaleri", 30),
    ("Bauchi - Bogoro", "Bauchi - Dass", 25),
    ("Bauchi - Damban", "Bauchi - Darazo", 35),
    ("Bauchi - Gamawa", "Bauchi - Darazo", 40),
    
    # Adamawa State - Internal connections
    ("Adamawa - Yola North", "Adamawa - Yola South", 8),
    ("Adamawa - Demsa", "Adamawa - Yola North", 35),
    ("Adamawa - Fufore", "Adamawa - Yola North", 25),
    ("Adamawa - Ganye", "Adamawa - Girei", 40),
    ("Adamawa - Gombi", "Adamawa - Yola North", 50),
    
    # ===== INTER-STATE CONNECTIONS (Major highways between states) =====
    
    # Lagos ↔ Ogun
    ("Lagos - Alimosho", "Ogun - Abeokuta South", 100),
    ("Lagos - Ikeja", "Ogun - Ado-Odo/Ota", 20),
    ("Lagos - Alimosho", "Ogun - Ifo", 60),
    
    # Lagos ↔ Oyo
    ("Lagos - Alimosho", "Oyo - Ibadan North", 120),
    
    # Lagos ↔ Ondo
    ("Lagos - Alimosho", "Ondo - Odigbo", 180),
    
    # Lagos ↔ Edo
    ("Lagos - Alimosho", "Edo - Oredo", 290),
    ("Lagos - Ikeja", "Edo - Oredo", 240),
    
    # Lagos ↔ Delta
    ("Lagos - Ikeja", "Delta - Warri South", 180),
    
    # Lagos ↔ Rivers
    ("Lagos - Ikeja", "Rivers - Port Harcourt", 350),
    
    # Ogun ↔ Oyo
    ("Ogun - Abeokuta South", "Oyo - Ibadan North", 80),
    ("Ogun - Ado-Odo/Ota", "Oyo - Ibadan North", 75),
    ("Ogun - Ifo", "Oyo - Ibadan North", 50),
    
    # Ogun ↔ Osun
    ("Ogun - Abeokuta South", "Osun - Osogbo", 140),
    
    # Ogun ↔ Delta
    ("Ogun - Ado-Odo/Ota", "Delta - Warri South", 160),
    
    # Ogun ↔ Edo
    ("Ogun - Ado-Odo/Ota", "Edo - Oredo", 200),
    
    # Oyo ↔ Osun
    ("Oyo - Ibadan North", "Osun - Osogbo", 90),
    ("Oyo - Ogbomosho North", "Osun - Osogbo", 45),
    
    # Oyo ↔ Kwara
    ("Oyo - Ibadan North", "Kwara - Ilorin South", 155),
    ("Oyo - Ogbomosho North", "Kwara - Ilorin South", 50),
    
    # Oyo ↔ Ondo
    ("Oyo - Ibadan North", "Ondo - Akure South", 170),
    ("Oyo - Ibadan North", "Ondo - Ondo West", 140),
    
    # Oyo ↔ Kogi
    ("Oyo - Ibadan North", "Kogi - Lokoja", 320),
    
    # Osun ↔ Kwara
    ("Osun - Osogbo", "Kwara - Ilorin South", 75),
    
    # Osun ↔ Ondo
    ("Osun - Osogbo", "Ondo - Akure South", 130),
    
    # Osun ↔ Kogi
    ("Osun - Osogbo", "Kogi - Lokoja", 220),
    
    # Osun ↔ FCT
    ("Osun - Osogbo", "FCT - AMAC", 380),
    
    # Kwara ↔ Niger
    ("Kwara - Ilorin South", "Niger - Chanchaga", 280),
    
    # Kwara ↔ Kogi
    ("Kwara - Ilorin South", "Kogi - Lokoja", 150),
    
    # Kwara ↔ Kaduna
    ("Kwara - Ilorin South", "Kaduna - Kaduna North", 380),
    
    # Kwara ↔ FCT
    ("Kwara - Ilorin South", "FCT - AMAC", 430),
    
    # Ondo ↔ Edo
    ("Ondo - Akure South", "Edo - Oredo", 210),
    ("Ondo - Odigbo", "Edo - Oredo", 110),
    ("Ondo - Ondo West", "Ondo - Akure South", 70),
    ("Ondo - Odigbo", "Ondo - Ondo West", 60),
    ("Ondo - Odigbo", "Delta - Sapele", 85),
    ("Ondo - Odigbo", "Ondo - Akure South", 130),
    
    # Ondo ↔ Delta
    ("Ondo - Akure South", "Delta - Warri South", 180),
    ("Ondo - Akure South", "Delta - Oshimili South", 200),
    
    # Edo ↔ Delta
    ("Edo - Oredo", "Delta - Ethiope East", 85),
    ("Edo - Oredo", "Delta - Warri South", 110),
    ("Edo - Oredo", "Delta - Oshimili South", 95),
    ("Edo - Oredo", "Delta - Sapele", 70),
    
    # Edo ↔ Enugu
    ("Edo - Oredo", "Enugu - Enugu North", 180),
    
    # Edo ↔ Rivers
    ("Edo - Oredo", "Rivers - Port Harcourt", 180),
    
    # Edo ↔ Kogi
    ("Edo - Oredo", "Kogi - Lokoja", 280),
    
    # Delta ↔ Rivers
    ("Delta - Warri South", "Rivers - Port Harcourt", 140),
    ("Delta - Ethiope East", "Rivers - Port Harcourt", 150),
    ("Delta - Ughelli North", "Rivers - Port Harcourt", 150),
    
    # Delta ↔ Imo
    ("Delta - Warri South", "Imo - Owerri Municipal", 160),
    ("Delta - Oshimili South", "Imo - Owerri Municipal", 100),
    
    # Delta ↔ Enugu
    ("Delta - Oshimili South", "Enugu - Enugu North", 120),
    
    # Delta ↔ Kogi
    ("Delta - Oshimili South", "Kogi - Lokoja", 140),
    
    # Rivers ↔ Imo
    ("Rivers - Port Harcourt", "Imo - Owerri Municipal", 65),
    
    # Rivers ↔ Akwa Ibom
    ("Rivers - Port Harcourt", "Akwa Ibom - Uyo", 90),
    
    # Rivers ↔ Cross River
    ("Rivers - Port Harcourt", "Cross River - Calabar Municipal", 165),
    
    # Rivers ↔ Enugu
    ("Rivers - Port Harcourt", "Enugu - Enugu North", 200),
    
    # Cross River ↔ Akwa Ibom
    ("Cross River - Calabar Municipal", "Akwa Ibom - Uyo", 80),
    
    # Akwa Ibom ↔ Imo
    ("Akwa Ibom - Uyo", "Imo - Owerri Municipal", 180),
    
    # Enugu ↔ Imo
    ("Enugu - Enugu North", "Imo - Owerri Municipal", 110),
    
    # Enugu ↔ Kogi
    ("Enugu - Enugu North", "Kogi - Lokoja", 240),
    
    # Enugu ↔ FCT
    ("Enugu - Enugu North", "FCT - AMAC", 280),
    
    # Kogi ↔ FCT
    ("Kogi - Lokoja", "FCT - AMAC", 200),
    
    # Kogi ↔ Niger
    ("Kogi - Lokoja", "Niger - Chanchaga", 180),
    
    # FCT ↔ Kaduna
    ("FCT - AMAC", "Kaduna - Kaduna North", 170),
    
    # FCT ↔ Plateau
    ("FCT - AMAC", "Plateau - Jos North", 220),
    
    # FCT ↔ Niger
    ("FCT - AMAC", "Niger - Chanchaga", 120),
    
    # FCT ↔ Kano
    ("FCT - AMAC", "Kano - Dala", 480),
    
    # Plateau ↔ Bauchi
    ("Plateau - Jos North", "Bauchi - Bauchi", 110),
    
    # Plateau ↔ Kaduna
    ("Plateau - Jos North", "Kaduna - Kaduna North", 180),
    
    # Plateau ↔ Kano
    ("Plateau - Jos North", "Kano - Dala", 290),
    
    # Niger ↔ Kaduna
    ("Niger - Chanchaga", "Kaduna - Kaduna North", 140),
    
    # Niger ↔ Sokoto
    ("Niger - Chanchaga", "Sokoto - Sokoto North", 380),
    
    # Kaduna ↔ Kano
    ("Kaduna - Kaduna North", "Kano - Dala", 210),
    
    # Kaduna ↔ Sokoto
    ("Kaduna - Kaduna North", "Sokoto - Sokoto North", 350),
    
    # Kaduna ↔ Bauchi
    ("Kaduna - Kaduna North", "Bauchi - Bauchi", 320),
    
    # Kano ↔ Sokoto
    ("Kano - Dala", "Sokoto - Sokoto North", 320),
    
    # Kano ↔ Borno
    ("Kano - Dala", "Borno - Maiduguri", 620),
    
    # Kano ↔ Bauchi
    ("Kano - Dala", "Bauchi - Bauchi", 280),
    
    # Bauchi ↔ Borno
    ("Bauchi - Bauchi", "Borno - Maiduguri", 300),
    
    # Bauchi ↔ Adamawa
    ("Bauchi - Bauchi", "Adamawa - Yola North", 260),
    
    # Adamawa ↔ Borno
    ("Adamawa - Yola North", "Borno - Maiduguri", 270),
    
    # ===== ADDITIONAL CONNECTIONS TO BRIDGE ISOLATED COMPONENTS =====
    
    # Connect remaining Lagos LGAs
    ("Lagos - Eti-Osa", "Lagos - Amuwo-Odofin", 15),
    
    # Connect remaining Ogun LGAs
    ("Ogun - Abeokuta North", "Ogun - Egbado North", 35),
    ("Ogun - Egbado South", "Ogun - Ewekoro", 22),
    
    # Connect remaining Oyo LGAs
    ("Oyo - Ibadan North-East", "Oyo - Afijio", 30),
    ("Oyo - Akinyele", "Oyo - Atiba", 25),
    ("Oyo - Atisbo", "Oyo - Ogbomosho North", 40),
    
    # Connect remaining Osun LGAs
    ("Osun - Ife East", "Osun - Aiyedaade", 35),
    ("Osun - Aiyedire", "Osun - Atakumosa East", 28),
    ("Osun - Boluwaduro", "Osun - Osogbo", 25),
    
    # Connect remaining Kwara LGAs
    ("Kwara - Ilorin East", "Kwara - Asa", 20),
    ("Kwara - Baruten", "Kwara - Ilorin West", 120),
    ("Kwara - Ekiti", "Kwara - Asa", 35),
    
    # Connect remaining Ondo LGAs
    ("Ondo - Akoko North-East", "Ondo - Akure North", 45),
    ("Ondo - Akoko South-West", "Ondo - Akoko North-West", 18),
    
    # Connect remaining Edo LGAs
    ("Edo - Ikpoba-Okha", "Edo - Akoko-Edo", 50),
    ("Edo - Esan Central", "Edo - Oredo", 45),
    ("Edo - Esan South-East", "Edo - Egor", 40),
    
    # Connect remaining Delta LGAs
    ("Delta - Aniocha North", "Delta - Bomadi", 55),
    
    # Connect remaining Rivers LGAs
    ("Rivers - Obio-Akpor", "Rivers - Eleme", 15),
    ("Rivers - Abua/Odual", "Rivers - Akuku-Toru", 35),
    ("Rivers - Ahoada West", "Rivers - Port Harcourt", 80),
    
    # Connect remaining Cross River LGAs
    ("Cross River - Calabar South", "Cross River - Abi", 60),
    ("Cross River - Akpabuyo", "Cross River - Bakassi", 30),
    ("Cross River - Bekwarra", "Cross River - Akamkpa", 70),
    
    # Connect remaining Akwa Ibom LGAs
    ("Akwa Ibom - Eket", "Akwa Ibom - Ikot Ekpene", 40),
    ("Akwa Ibom - Oron", "Akwa Ibom - Abak", 45),
    ("Akwa Ibom - Eastern Obolo", "Akwa Ibom - Uyo", 50),
    ("Akwa Ibom - Esit Eket", "Akwa Ibom - Eket", 20),
    
    # Connect remaining Enugu LGAs
    ("Enugu - Enugu East", "Enugu - Aninri", 35),
    ("Enugu - Awgu", "Enugu - Enugu South", 30),
    ("Enugu - Ezeagu", "Enugu - Igbo Etiti", 40),
    
    # Connect remaining Imo LGAs
    ("Imo - Owerri West", "Imo - Aboh Mbaise", 20),
    ("Imo - Ahiazu Mbaise", "Imo - Ehime Mbano", 30),
    ("Imo - Ezinihitte", "Imo - Owerri North", 25),
    
    # Connect remaining FCT LGAs
    ("FCT - Abuja Municipal", "FCT - Bwari", 18),
    ("FCT - Gwagwalada", "FCT - AMAC", 25),
    ("FCT - Abaji", "FCT - Gwagwalada", 30),
    
    # Connect remaining Plateau LGAs
    ("Plateau - Jos East", "Plateau - Barkin Ladi", 28),
    ("Plateau - Bassa", "Plateau - Bokkos", 35),
    ("Plateau - Kanam", "Plateau - Jos South", 40),
    
    # Connect remaining Niger LGAs
    ("Niger - Bosso", "Niger - Agaie", 30),
    ("Niger - Bida", "Niger - Chanchaga", 50),
    ("Niger - Agwara", "Niger - Minna", 180),
    ("Niger - Borgu", "Niger - Bosso", 120),
    
    # Connect remaining Kogi LGAs
    ("Kogi - Adavi", "Kogi - Bassa", 25),
    ("Kogi - Ajaokuta", "Kogi - Ankpa", 60),
    ("Kogi - Dekina", "Kogi - Lokoja", 70),
    ("Kogi - Ibaji", "Kogi - Bassa", 40),
    
    # Connect remaining Kano LGAs
    ("Kano - Nassarawa", "Kano - Ajingi", 35),
    ("Kano - Albasu", "Kano - Kano Municipal", 45),
    ("Kano - Bagwai", "Kano - Dala", 55),
    ("Kano - Bebeji", "Kano - Nassarawa", 40),
    
    # Connect remaining Kaduna LGAs
    ("Kaduna - Kaduna South", "Kaduna - Birnin Gwari", 80),
    ("Kaduna - Chikun", "Kaduna - Kaduna North", 25),
    ("Kaduna - Giwa", "Kaduna - Kaduna South", 60),
    ("Kaduna - Igabi", "Kaduna - Chikun", 35),
    ("Kaduna - Ikara", "Kaduna - Igabi", 30),
    
    # Connect remaining Sokoto LGAs
    ("Sokoto - Sokoto South", "Sokoto - Binji", 40),
    ("Sokoto - Bodinga", "Sokoto - Sokoto North", 35),
    ("Sokoto - Dange Shuni", "Sokoto - Binji", 50),
    ("Sokoto - Gada", "Sokoto - Goronyo", 18),
    
    # Connect remaining Borno LGAs
    ("Borno - Bama", "Borno - Biu", 100),
    ("Borno - Abadam", "Borno - Bama", 90),
    ("Borno - Askira/Uba", "Borno - Maiduguri", 85),
    ("Borno - Bayo", "Borno - Biu", 30),
    ("Borno - Chibok", "Borno - Askira/Uba", 35),
    
    # Connect remaining Bauchi LGAs
    ("Bauchi - Alkaleri", "Bauchi - Bogoro", 35),
    ("Bauchi - Dass", "Bauchi - Bauchi", 40),
    ("Bauchi - Damban", "Bauchi - Alkaleri", 45),
    ("Bauchi - Darazo", "Bauchi - Damban", 35),
    ("Bauchi - Gamawa", "Bauchi - Bauchi", 80),
    
    # Connect remaining Adamawa LGAs
    ("Adamawa - Yola South", "Adamawa - Demsa", 30),
    ("Adamawa - Fufore", "Adamawa - Girei", 20),
    ("Adamawa - Ganye", "Adamawa - Yola South", 85),
    ("Adamawa - Girei", "Adamawa - Yola North", 15),
    ("Adamawa - Gombi", "Adamawa - Demsa", 60),
]


def create_graph() -> nx.Graph:
    """
    Create a NetworkX graph representing the Nigerian road network.
    
    Returns:
        nx.Graph: Graph with LGAs as nodes and roads as edges
    """
    G = nx.Graph()
    
    # Add nodes with LGA attributes
    for lga, data in LGA_DATA.items():
        G.add_node(
            lga,
            pos=data["coords"],
            prevalence=data["prevalence"],
            population=data["population"]
        )
    
    # Add edges with distance weights
    for lga1, lga2, distance in ROAD_NETWORK:
        G.add_edge(lga1, lga2, distance=distance)
    
    return G


def get_all_states() -> List[str]:
    """
    Get list of all states in alphabetical order.
    
    Returns:
        List of state names
    """
    return sorted(STATE_LGA_STRUCTURE.keys())


def get_lgas_for_state(state: str) -> List[str]:
    """
    Get list of LGAs for a specific state.
    
    Args:
        state: Name of the state
        
    Returns:
        List of LGA names for the state
    """
    return STATE_LGA_STRUCTURE.get(state, [])


def get_lgas_by_state(state: str) -> List[str]:
    """
    Get all LGAs in a specific state.
    
    Args:
        state: Name of the state
        
    Returns:
        List of LGA names (format: "State - LGA")
    """
    return [lga for lga, data in LGA_DATA.items() if data.get('state') == state]


def get_lga_data(lga_name: str) -> Dict:
    """
    Get detailed data for a specific LGA.
    
    Args:
        lga_name: Name of the LGA (format: "State - LGA")
        
    Returns:
        Dictionary containing LGA data
    """
    return LGA_DATA.get(lga_name, {})


def get_all_lgas() -> List[str]:
    """
    Get list of all LGA names.
    
    Returns:
        List of LGA names (format: "State - LGA")
    """
    return list(LGA_DATA.keys())


def calculate_haversine_distance(coord1: Tuple[float, float], 
                                 coord2: Tuple[float, float]) -> float:
    """
    Calculate approximate distance between two coordinates (for reference).
    Note: Road distances are used in the actual routing.
    
    Args:
        coord1: (latitude, longitude) of first point
        coord2: (latitude, longitude) of second point
        
    Returns:
        Distance in kilometers
    """
    from math import radians, sin, cos, sqrt, atan2
    
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    # Earth's radius in kilometers
    R = 6371
    
    return R * c


if __name__ == "__main__":
    # Test the data loader
    G = create_graph()
    print(f"Graph created with {G.number_of_nodes()} cities and {G.number_of_edges()} roads")
    print(f"\nCities: {get_all_cities()}")
    print(f"\nLagos data: {get_city_data('Lagos')}")
