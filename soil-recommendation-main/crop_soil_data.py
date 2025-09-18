# Crop-specific soil requirements and fertilizer recommendations
# Based on agricultural research and optimal growing conditions

CROP_REQUIREMENTS = {
    'rice': {
        'soil_parameters': {
            'N': {'optimal': [80, 120], 'unit': 'kg/ha', 'description': 'High nitrogen for vegetative growth'},
            'P': {'optimal': [40, 60], 'unit': 'kg/ha', 'description': 'Moderate phosphorus for root development'},
            'K': {'optimal': [40, 60], 'unit': 'kg/ha', 'description': 'Potassium for grain filling'},
            'ph': {'optimal': [5.5, 7.0], 'unit': '', 'description': 'Slightly acidic to neutral'},
            'temperature': {'optimal': [20, 35], 'unit': '°C', 'description': 'Warm tropical climate'},
            'humidity': {'optimal': [80, 95], 'unit': '%', 'description': 'High humidity for paddy cultivation'},
            'rainfall': {'optimal': [150, 300], 'unit': 'mm', 'description': 'High water requirement'}
        },
        'recommended_fertilizers': ['Urea', 'DAP', '14:35:14'],
        'fertilizer_schedule': 'Apply 50% nitrogen at transplanting, 25% at tillering, 25% at panicle initiation',
        'soil_type': ['Clayey', 'Loamy'],
        'season': 'Kharif (monsoon season)',
        'growth_duration': '120-150 days',
        'indian_locations': {
            'major_states': ['West Bengal', 'Uttar Pradesh', 'Punjab', 'Odisha', 'Andhra Pradesh', 'Tamil Nadu'],
            'top_districts': ['Bardhaman (WB)', 'Thanjavur (TN)', 'East Godavari (AP)', 'Cuttack (Odisha)', 'Ludhiana (Punjab)'],
            'agro_climatic_zones': ['Lower Gangetic Plains', 'East Coast Plains', 'Upper Gangetic Plains', 'Trans-Gangetic Plains'],
            'production_share': 'West Bengal (15%), Uttar Pradesh (12%), Punjab (11%), Odisha (8%), Andhra Pradesh (7%)',
            'best_regions': {
                'high_yield': ['Punjab', 'Haryana', 'Tamil Nadu'],
                'largest_area': ['West Bengal', 'Uttar Pradesh', 'Odisha'],
                'quality_rice': ['Basmati belt (Punjab, Haryana, UP)', 'Gobindobhog (West Bengal)']
            }
        }
    },
    'maize': {
        'soil_parameters': {
            'N': {'optimal': [120, 180], 'unit': 'kg/ha', 'description': 'Very high nitrogen requirement'},
            'P': {'optimal': [60, 90], 'unit': 'kg/ha', 'description': 'High phosphorus for root and ear development'},
            'K': {'optimal': [40, 80], 'unit': 'kg/ha', 'description': 'Potassium for stalk strength'},
            'ph': {'optimal': [6.0, 7.5], 'unit': '', 'description': 'Neutral to slightly alkaline'},
            'temperature': {'optimal': [21, 27], 'unit': '°C', 'description': 'Moderate temperature'},
            'humidity': {'optimal': [60, 70], 'unit': '%', 'description': 'Moderate humidity'},
            'rainfall': {'optimal': [50, 100], 'unit': 'mm', 'description': 'Moderate water requirement'}
        },
        'recommended_fertilizers': ['Urea', 'DAP', '17:17:17'],
        'fertilizer_schedule': 'Apply 30% nitrogen at sowing, 40% at knee-high stage, 30% at tasseling',
        'soil_type': ['Loamy', 'Black'],
        'season': 'Kharif or Rabi',
        'growth_duration': '90-120 days',
        'indian_locations': {
            'major_states': ['Karnataka', 'Rajasthan', 'Maharashtra', 'Uttar Pradesh', 'Madhya Pradesh', 'Bihar'],
            'top_districts': ['Davanagere (Karnataka)', 'Udaipur (Rajasthan)', 'Ahmednagar (Maharashtra)', 'Muzaffarpur (Bihar)'],
            'agro_climatic_zones': ['Northern Plains', 'Central Plateau', 'Western Plateau', 'Southern Plateau'],
            'production_share': 'Karnataka (16%), Rajasthan (9%), Maharashtra (8%), Uttar Pradesh (7%), Madhya Pradesh (7%)',
            'best_regions': {
                'high_yield': ['Punjab', 'Haryana', 'Karnataka'],
                'largest_area': ['Karnataka', 'Rajasthan', 'Maharashtra'],
                'quality_maize': ['Karnataka (sweet corn)', 'Rajasthan (fodder maize)', 'Maharashtra (popcorn)']
            }
        }
    },
    'chickpea': {
        'soil_parameters': {
            'N': {'optimal': [20, 40], 'unit': 'kg/ha', 'description': 'Low nitrogen due to nitrogen fixation'},
            'P': {'optimal': [40, 60], 'unit': 'kg/ha', 'description': 'High phosphorus requirement'},
            'K': {'optimal': [20, 40], 'unit': 'kg/ha', 'description': 'Moderate potassium'},
            'ph': {'optimal': [6.5, 7.5], 'unit': '', 'description': 'Neutral to slightly alkaline'},
            'temperature': {'optimal': [20, 30], 'unit': '°C', 'description': 'Cool to moderate temperature'},
            'humidity': {'optimal': [60, 70], 'unit': '%', 'description': 'Moderate humidity'},
            'rainfall': {'optimal': [30, 40], 'unit': 'mm', 'description': 'Low water requirement'}
        },
        'recommended_fertilizers': ['DAP', 'MOP', '14:35:14'],
        'fertilizer_schedule': 'Apply full dose at sowing, minimal nitrogen top-dressing',
        'soil_type': ['Black', 'Loamy'],
        'season': 'Rabi (winter season)',
        'growth_duration': '95-120 days',
        'indian_locations': {
            'major_states': ['Madhya Pradesh', 'Rajasthan', 'Maharashtra', 'Uttar Pradesh', 'Karnataka', 'Andhra Pradesh'],
            'top_districts': ['Sehore (MP)', 'Jalore (Rajasthan)', 'Latur (Maharashtra)', 'Jhansi (UP)', 'Gulbarga (Karnataka)'],
            'agro_climatic_zones': ['Central Plateau', 'Western Plateau', 'Northern Plains', 'Southern Plateau'],
            'production_share': 'Madhya Pradesh (40%), Rajasthan (15%), Maharashtra (12%), Uttar Pradesh (8%)',
            'best_regions': {
                'high_yield': ['Punjab', 'Haryana', 'Madhya Pradesh'],
                'largest_area': ['Madhya Pradesh', 'Rajasthan', 'Maharashtra'],
                'quality_chickpea': ['Kabuli: Maharashtra, Karnataka', 'Desi: Madhya Pradesh, Rajasthan']
            }
        }
    },
    'kidneybeans': {
        'soil_parameters': {
            'N': {'optimal': [25, 40], 'unit': 'kg/ha', 'description': 'Moderate nitrogen, nitrogen-fixing crop'},
            'P': {'optimal': [50, 70], 'unit': 'kg/ha', 'description': 'High phosphorus for nodulation'},
            'K': {'optimal': [30, 50], 'unit': 'kg/ha', 'description': 'Moderate potassium'},
            'ph': {'optimal': [6.0, 7.0], 'unit': '', 'description': 'Slightly acidic to neutral'},
            'temperature': {'optimal': [15, 27], 'unit': '°C', 'description': 'Cool to moderate temperature'},
            'humidity': {'optimal': [65, 75], 'unit': '%', 'description': 'Moderate humidity'},
            'rainfall': {'optimal': [60, 120], 'unit': 'mm', 'description': 'Moderate water requirement'}
        },
        'recommended_fertilizers': ['DAP', 'MOP', '20:20'],
        'fertilizer_schedule': 'Apply full dose at planting, light nitrogen topdressing if needed',
        'soil_type': ['Loamy', 'Sandy'],
        'season': 'Kharif or Rabi',
        'growth_duration': '60-90 days'
    },
    'pigeonpeas': {
        'soil_parameters': {
            'N': {'optimal': [20, 30], 'unit': 'kg/ha', 'description': 'Low nitrogen, nitrogen-fixing legume'},
            'P': {'optimal': [50, 80], 'unit': 'kg/ha', 'description': 'High phosphorus for root nodules'},
            'K': {'optimal': [20, 40], 'unit': 'kg/ha', 'description': 'Moderate potassium'},
            'ph': {'optimal': [6.5, 7.5], 'unit': '', 'description': 'Neutral to slightly alkaline'},
            'temperature': {'optimal': [26, 30], 'unit': '°C', 'description': 'Warm temperature'},
            'humidity': {'optimal': [60, 65], 'unit': '%', 'description': 'Moderate humidity'},
            'rainfall': {'optimal': [60, 65], 'unit': 'mm', 'description': 'Moderate rainfall'}
        },
        'recommended_fertilizers': ['DAP', 'MOP'],
        'fertilizer_schedule': 'Apply full dose at sowing, no nitrogen top-dressing needed',
        'soil_type': ['Black', 'Red'],
        'season': 'Kharif',
        'growth_duration': '150-180 days'
    },
    'mothbeans': {
        'soil_parameters': {
            'N': {'optimal': [15, 25], 'unit': 'kg/ha', 'description': 'Very low nitrogen requirement'},
            'P': {'optimal': [40, 50], 'unit': 'kg/ha', 'description': 'Moderate phosphorus'},
            'K': {'optimal': [20, 30], 'unit': 'kg/ha', 'description': 'Low potassium requirement'},
            'ph': {'optimal': [7.0, 8.5], 'unit': '', 'description': 'Alkaline soil tolerant'},
            'temperature': {'optimal': [27, 35], 'unit': '°C', 'description': 'High temperature tolerance'},
            'humidity': {'optimal': [60, 75], 'unit': '%', 'description': 'Moderate humidity'},
            'rainfall': {'optimal': [40, 50], 'unit': 'mm', 'description': 'Low water requirement'}
        },
        'recommended_fertilizers': ['DAP', 'MOP'],
        'fertilizer_schedule': 'Apply at sowing, drought-tolerant crop',
        'soil_type': ['Sandy', 'Loamy'],
        'season': 'Kharif',
        'growth_duration': '60-90 days'
    },
    'mungbean': {
        'soil_parameters': {
            'N': {'optimal': [15, 25], 'unit': 'kg/ha', 'description': 'Low nitrogen, nitrogen-fixing'},
            'P': {'optimal': [40, 60], 'unit': 'kg/ha', 'description': 'Moderate phosphorus'},
            'K': {'optimal': [20, 30], 'unit': 'kg/ha', 'description': 'Low potassium'},
            'ph': {'optimal': [6.2, 7.2], 'unit': '', 'description': 'Neutral pH preferred'},
            'temperature': {'optimal': [28, 35], 'unit': '°C', 'description': 'Warm temperature'},
            'humidity': {'optimal': [65, 75], 'unit': '%', 'description': 'Moderate humidity'},
            'rainfall': {'optimal': [60, 75], 'unit': 'mm', 'description': 'Moderate rainfall'}
        },
        'recommended_fertilizers': ['DAP', 'MOP', '20:20'],
        'fertilizer_schedule': 'Apply full dose at sowing',
        'soil_type': ['Loamy', 'Sandy'],
        'season': 'Kharif or Summer',
        'growth_duration': '60-75 days'
    },
    'blackgram': {
        'soil_parameters': {
            'N': {'optimal': [15, 20], 'unit': 'kg/ha', 'description': 'Very low nitrogen'},
            'P': {'optimal': [40, 50], 'unit': 'kg/ha', 'description': 'Moderate phosphorus'},
            'K': {'optimal': [15, 25], 'unit': 'kg/ha', 'description': 'Low potassium'},
            'ph': {'optimal': [6.5, 7.5], 'unit': '', 'description': 'Neutral pH'},
            'temperature': {'optimal': [25, 35], 'unit': '°C', 'description': 'Warm temperature'},
            'humidity': {'optimal': [65, 75], 'unit': '%', 'description': 'Moderate humidity'},
            'rainfall': {'optimal': [60, 100], 'unit': 'mm', 'description': 'Moderate rainfall'}
        },
        'recommended_fertilizers': ['DAP', 'MOP'],
        'fertilizer_schedule': 'Apply full dose at sowing',
        'soil_type': ['Black', 'Loamy'],
        'season': 'Kharif or Rabi',
        'growth_duration': '70-90 days'
    },
    'lentil': {
        'soil_parameters': {
            'N': {'optimal': [15, 25], 'unit': 'kg/ha', 'description': 'Low nitrogen requirement'},
            'P': {'optimal': [50, 70], 'unit': 'kg/ha', 'description': 'High phosphorus'},
            'K': {'optimal': [20, 30], 'unit': 'kg/ha', 'description': 'Low potassium'},
            'ph': {'optimal': [6.0, 7.5], 'unit': '', 'description': 'Slightly acidic to neutral'},
            'temperature': {'optimal': [18, 30], 'unit': '°C', 'description': 'Cool to moderate temperature'},
            'humidity': {'optimal': [60, 70], 'unit': '%', 'description': 'Moderate humidity'},
            'rainfall': {'optimal': [25, 40], 'unit': 'mm', 'description': 'Low water requirement'}
        },
        'recommended_fertilizers': ['DAP', 'MOP', '14:35:14'],
        'fertilizer_schedule': 'Apply full dose at sowing',
        'soil_type': ['Loamy', 'Black'],
        'season': 'Rabi',
        'growth_duration': '95-110 days'
    },
    'pomegranate': {
        'soil_parameters': {
            'N': {'optimal': [100, 150], 'unit': 'kg/ha', 'description': 'High nitrogen for fruit trees'},
            'P': {'optimal': [50, 80], 'unit': 'kg/ha', 'description': 'Moderate phosphorus'},
            'K': {'optimal': [100, 150], 'unit': 'kg/ha', 'description': 'High potassium for fruit quality'},
            'ph': {'optimal': [6.5, 7.5], 'unit': '', 'description': 'Neutral pH'},
            'temperature': {'optimal': [15, 35], 'unit': '°C', 'description': 'Wide temperature range'},
            'humidity': {'optimal': [35, 60], 'unit': '%', 'description': 'Low to moderate humidity'},
            'rainfall': {'optimal': [50, 70], 'unit': 'mm', 'description': 'Moderate rainfall'}
        },
        'recommended_fertilizers': ['Urea', 'DAP', 'MOP'],
        'fertilizer_schedule': 'Split application: 4 times per year during growing season',
        'soil_type': ['Red', 'Black'],
        'season': 'Perennial',
        'growth_duration': 'Perennial fruit tree'
    },
    'banana': {
        'soil_parameters': {
            'N': {'optimal': [200, 300], 'unit': 'kg/ha', 'description': 'Very high nitrogen requirement'},
            'P': {'optimal': [50, 100], 'unit': 'kg/ha', 'description': 'Moderate phosphorus'},
            'K': {'optimal': [300, 500], 'unit': 'kg/ha', 'description': 'Very high potassium for fruit development'},
            'ph': {'optimal': [6.0, 7.5], 'unit': '', 'description': 'Slightly acidic to neutral'},
            'temperature': {'optimal': [26, 30], 'unit': '°C', 'description': 'Warm tropical climate'},
            'humidity': {'optimal': [75, 85], 'unit': '%', 'description': 'High humidity'},
            'rainfall': {'optimal': [100, 180], 'unit': 'mm', 'description': 'High water requirement'}
        },
        'recommended_fertilizers': ['Urea', 'MOP', '17:17:17'],
        'fertilizer_schedule': 'Monthly applications throughout the year',
        'soil_type': ['Loamy', 'Red'],
        'season': 'Year-round',
        'growth_duration': '12-15 months'
    },
    'mango': {
        'soil_parameters': {
            'N': {'optimal': [100, 200], 'unit': 'kg/ha', 'description': 'High nitrogen for tree growth'},
            'P': {'optimal': [50, 100], 'unit': 'kg/ha', 'description': 'Moderate phosphorus'},
            'K': {'optimal': [100, 200], 'unit': 'kg/ha', 'description': 'High potassium for fruit quality'},
            'ph': {'optimal': [5.5, 7.5], 'unit': '', 'description': 'Slightly acidic to neutral'},
            'temperature': {'optimal': [24, 30], 'unit': '°C', 'description': 'Warm tropical climate'},
            'humidity': {'optimal': [50, 60], 'unit': '%', 'description': 'Moderate humidity'},
            'rainfall': {'optimal': [75, 125], 'unit': 'mm', 'description': 'Moderate to high rainfall'}
        },
        'recommended_fertilizers': ['Urea', 'DAP', 'MOP'],
        'fertilizer_schedule': '3-4 split applications during growing season',
        'soil_type': ['Red', 'Loamy'],
        'season': 'Perennial',
        'growth_duration': 'Perennial fruit tree',
        'indian_locations': {
            'major_states': ['Uttar Pradesh', 'Andhra Pradesh', 'Karnataka', 'Tamil Nadu', 'Gujarat', 'Maharashtra'],
            'top_districts': ['Lucknow (UP)', 'Chittoor (AP)', 'Bangalore Rural (Karnataka)', 'Dharmapuri (TN)', 'Junagadh (Gujarat)'],
            'agro_climatic_zones': ['Northern Plains', 'Southern Plateau', 'East Coast Plains', 'West Coast Plains'],
            'production_share': 'Uttar Pradesh (23%), Andhra Pradesh (20%), Karnataka (11%), Tamil Nadu (9%), Gujarat (7%)',
            'best_regions': {
                'famous_varieties': ['Alphonso (Maharashtra, Gujarat)', 'Dasheri (UP)', 'Kesar (Gujarat)', 'Banganapalli (AP)'],
                'largest_area': ['Uttar Pradesh', 'Andhra Pradesh', 'Karnataka'],
                'export_quality': ['Maharashtra (Alphonso)', 'Gujarat (Kesar)', 'Karnataka (Totapuri)']
            }
        }
    },
    'grapes': {
        'soil_parameters': {
            'N': {'optimal': [80, 120], 'unit': 'kg/ha', 'description': 'Moderate nitrogen'},
            'P': {'optimal': [40, 80], 'unit': 'kg/ha', 'description': 'Moderate phosphorus'},
            'K': {'optimal': [80, 150], 'unit': 'kg/ha', 'description': 'High potassium for fruit quality'},
            'ph': {'optimal': [6.0, 8.0], 'unit': '', 'description': 'Neutral to slightly alkaline'},
            'temperature': {'optimal': [15, 25], 'unit': '°C', 'description': 'Cool to moderate temperature'},
            'humidity': {'optimal': [60, 70], 'unit': '%', 'description': 'Moderate humidity'},
            'rainfall': {'optimal': [50, 75], 'unit': 'mm', 'description': 'Moderate rainfall'}
        },
        'recommended_fertilizers': ['Urea', 'DAP', 'MOP'],
        'fertilizer_schedule': 'Split application: pre-bloom, fruit set, veraison',
        'soil_type': ['Red', 'Black'],
        'season': 'Perennial',
        'growth_duration': 'Perennial vine'
    },
    'watermelon': {
        'soil_parameters': {
            'N': {'optimal': [100, 150], 'unit': 'kg/ha', 'description': 'High nitrogen for vine growth'},
            'P': {'optimal': [50, 80], 'unit': 'kg/ha', 'description': 'Moderate phosphorus'},
            'K': {'optimal': [150, 200], 'unit': 'kg/ha', 'description': 'High potassium for fruit development'},
            'ph': {'optimal': [6.0, 7.0], 'unit': '', 'description': 'Slightly acidic to neutral'},
            'temperature': {'optimal': [24, 35], 'unit': '°C', 'description': 'Warm temperature'},
            'humidity': {'optimal': [65, 75], 'unit': '%', 'description': 'Moderate humidity'},
            'rainfall': {'optimal': [50, 75], 'unit': 'mm', 'description': 'Moderate rainfall'}
        },
        'recommended_fertilizers': ['Urea', 'DAP', 'MOP'],
        'fertilizer_schedule': 'Split application: planting, flowering, fruit development',
        'soil_type': ['Sandy', 'Loamy'],
        'season': 'Summer',
        'growth_duration': '80-100 days'
    },
    'muskmelon': {
        'soil_parameters': {
            'N': {'optimal': [80, 120], 'unit': 'kg/ha', 'description': 'Moderate to high nitrogen'},
            'P': {'optimal': [40, 60], 'unit': 'kg/ha', 'description': 'Moderate phosphorus'},
            'K': {'optimal': [100, 150], 'unit': 'kg/ha', 'description': 'High potassium for sweetness'},
            'ph': {'optimal': [6.0, 7.0], 'unit': '', 'description': 'Neutral pH'},
            'temperature': {'optimal': [24, 30], 'unit': '°C', 'description': 'Warm temperature'},
            'humidity': {'optimal': [60, 70], 'unit': '%', 'description': 'Moderate humidity'},
            'rainfall': {'optimal': [50, 70], 'unit': 'mm', 'description': 'Moderate rainfall'}
        },
        'recommended_fertilizers': ['Urea', 'DAP', 'MOP'],
        'fertilizer_schedule': 'Split application throughout growing season',
        'soil_type': ['Sandy', 'Loamy'],
        'season': 'Summer',
        'growth_duration': '90-110 days'
    },
    'apple': {
        'soil_parameters': {
            'N': {'optimal': [150, 200], 'unit': 'kg/ha', 'description': 'High nitrogen for tree growth'},
            'P': {'optimal': [60, 100], 'unit': 'kg/ha', 'description': 'Moderate to high phosphorus'},
            'K': {'optimal': [150, 250], 'unit': 'kg/ha', 'description': 'High potassium for fruit quality'},
            'ph': {'optimal': [6.0, 7.0], 'unit': '', 'description': 'Slightly acidic to neutral'},
            'temperature': {'optimal': [15, 25], 'unit': '°C', 'description': 'Cool to moderate temperature'},
            'humidity': {'optimal': [60, 70], 'unit': '%', 'description': 'Moderate humidity'},
            'rainfall': {'optimal': [100, 125], 'unit': 'mm', 'description': 'High rainfall'}
        },
        'recommended_fertilizers': ['Urea', 'DAP', 'MOP'],
        'fertilizer_schedule': 'Split application: spring, summer, fall',
        'soil_type': ['Loamy', 'Red'],
        'season': 'Perennial',
        'growth_duration': 'Perennial fruit tree',
        'indian_locations': {
            'major_states': ['Jammu & Kashmir', 'Himachal Pradesh', 'Uttarakhand', 'Arunachal Pradesh'],
            'top_districts': ['Baramulla (J&K)', 'Shimla (HP)', 'Chamoli (Uttarakhand)', 'West Kameng (Arunachal)'],
            'agro_climatic_zones': ['Western Himalayas', 'Eastern Himalayas', 'Hill Regions'],
            'production_share': 'Jammu & Kashmir (77%), Himachal Pradesh (19%), Uttarakhand (2%), Others (2%)',
            'best_regions': {
                'quality_varieties': ['Kashmir (Red Delicious)', 'Himachal (Royal Delicious)', 'Uttarakhand (Gala)'],
                'high_altitude': ['Leh-Ladakh (organic)', 'Kinnaur (HP)', 'Kashmir Valley'],
                'export_quality': ['Kashmir Valley', 'Shimla Hills', 'Kullu Valley']
            }
        }
    },
    'orange': {
        'soil_parameters': {
            'N': {'optimal': [150, 250], 'unit': 'kg/ha', 'description': 'High nitrogen requirement'},
            'P': {'optimal': [50, 80], 'unit': 'kg/ha', 'description': 'Moderate phosphorus'},
            'K': {'optimal': [150, 200], 'unit': 'kg/ha', 'description': 'High potassium for fruit quality'},
            'ph': {'optimal': [6.0, 7.5], 'unit': '', 'description': 'Slightly acidic to neutral'},
            'temperature': {'optimal': [15, 30], 'unit': '°C', 'description': 'Moderate to warm temperature'},
            'humidity': {'optimal': [55, 65], 'unit': '%', 'description': 'Moderate humidity'},
            'rainfall': {'optimal': [100, 120], 'unit': 'mm', 'description': 'High rainfall'}
        },
        'recommended_fertilizers': ['Urea', 'DAP', 'MOP'],
        'fertilizer_schedule': 'Split application: 3-4 times per year',
        'soil_type': ['Red', 'Loamy'],
        'season': 'Perennial',
        'growth_duration': 'Perennial citrus tree'
    },
    'papaya': {
        'soil_parameters': {
            'N': {'optimal': [200, 300], 'unit': 'kg/ha', 'description': 'Very high nitrogen requirement'},
            'P': {'optimal': [50, 100], 'unit': 'kg/ha', 'description': 'Moderate phosphorus'},
            'K': {'optimal': [200, 300], 'unit': 'kg/ha', 'description': 'Very high potassium'},
            'ph': {'optimal': [6.0, 7.0], 'unit': '', 'description': 'Neutral pH'},
            'temperature': {'optimal': [25, 30], 'unit': '°C', 'description': 'Warm tropical climate'},
            'humidity': {'optimal': [70, 80], 'unit': '%', 'description': 'High humidity'},
            'rainfall': {'optimal': [100, 150], 'unit': 'mm', 'description': 'High rainfall'}
        },
        'recommended_fertilizers': ['Urea', 'MOP', '17:17:17'],
        'fertilizer_schedule': 'Monthly applications throughout the year',
        'soil_type': ['Loamy', 'Red'],
        'season': 'Year-round',
        'growth_duration': '10-12 months'
    },
    'coconut': {
        'soil_parameters': {
            'N': {'optimal': [100, 150], 'unit': 'kg/ha', 'description': 'Moderate to high nitrogen'},
            'P': {'optimal': [40, 60], 'unit': 'kg/ha', 'description': 'Moderate phosphorus'},
            'K': {'optimal': [140, 200], 'unit': 'kg/ha', 'description': 'High potassium for nut development'},
            'ph': {'optimal': [5.2, 8.0], 'unit': '', 'description': 'Wide pH tolerance'},
            'temperature': {'optimal': [27, 35], 'unit': '°C', 'description': 'High temperature tolerance'},
            'humidity': {'optimal': [80, 90], 'unit': '%', 'description': 'Very high humidity'},
            'rainfall': {'optimal': [150, 250], 'unit': 'mm', 'description': 'Very high rainfall'}
        },
        'recommended_fertilizers': ['Urea', 'MOP', 'DAP'],
        'fertilizer_schedule': 'Quarterly applications throughout the year',
        'soil_type': ['Sandy', 'Loamy'],
        'season': 'Perennial',
        'growth_duration': 'Perennial palm tree'
    },
    'cotton': {
        'soil_parameters': {
            'N': {'optimal': [120, 180], 'unit': 'kg/ha', 'description': 'High nitrogen for fiber development'},
            'P': {'optimal': [60, 80], 'unit': 'kg/ha', 'description': 'Moderate to high phosphorus'},
            'K': {'optimal': [60, 100], 'unit': 'kg/ha', 'description': 'High potassium for fiber quality'},
            'ph': {'optimal': [5.8, 8.0], 'unit': '', 'description': 'Slightly acidic to alkaline'},
            'temperature': {'optimal': [21, 30], 'unit': '°C', 'description': 'Warm temperature'},
            'humidity': {'optimal': [50, 60], 'unit': '%', 'description': 'Moderate humidity'},
            'rainfall': {'optimal': [50, 100], 'unit': 'mm', 'description': 'Moderate rainfall'}
        },
        'recommended_fertilizers': ['Urea', 'DAP', 'MOP'],
        'fertilizer_schedule': 'Split application: planting, squaring, flowering',
        'soil_type': ['Black', 'Red'],
        'season': 'Kharif',
        'growth_duration': '150-180 days',
        'indian_locations': {
            'major_states': ['Gujarat', 'Maharashtra', 'Telangana', 'Karnataka', 'Andhra Pradesh', 'Rajasthan'],
            'top_districts': ['Surendranagar (Gujarat)', 'Yavatmal (Maharashtra)', 'Adilabad (Telangana)', 'Raichur (Karnataka)'],
            'agro_climatic_zones': ['Western Plateau', 'Central Plateau', 'Southern Plateau', 'Western Plains'],
            'production_share': 'Gujarat (33%), Maharashtra (26%), Telangana (12%), Karnataka (8%), Andhra Pradesh (6%)',
            'best_regions': {
                'bt_cotton': ['Gujarat', 'Maharashtra', 'Telangana'],
                'organic_cotton': ['Madhya Pradesh', 'Odisha', 'Rajasthan'],
                'quality_fiber': ['Gujarat (long staple)', 'Maharashtra (medium staple)', 'Punjab (extra long)']
            }
        }
    },
    'jute': {
        'soil_parameters': {
            'N': {'optimal': [80, 120], 'unit': 'kg/ha', 'description': 'High nitrogen for fiber growth'},
            'P': {'optimal': [40, 60], 'unit': 'kg/ha', 'description': 'Moderate phosphorus'},
            'K': {'optimal': [40, 60], 'unit': 'kg/ha', 'description': 'Moderate potassium'},
            'ph': {'optimal': [6.0, 7.5], 'unit': '', 'description': 'Neutral pH'},
            'temperature': {'optimal': [24, 35], 'unit': '°C', 'description': 'Warm temperature'},
            'humidity': {'optimal': [70, 80], 'unit': '%', 'description': 'High humidity'},
            'rainfall': {'optimal': [150, 250], 'unit': 'mm', 'description': 'High rainfall'}
        },
        'recommended_fertilizers': ['Urea', 'DAP', 'MOP'],
        'fertilizer_schedule': 'Split application during vegetative growth',
        'soil_type': ['Clayey', 'Loamy'],
        'season': 'Kharif',
        'growth_duration': '120-150 days'
    },
    'coffee': {
        'soil_parameters': {
            'N': {'optimal': [200, 300], 'unit': 'kg/ha', 'description': 'Very high nitrogen for perennial crop'},
            'P': {'optimal': [80, 120], 'unit': 'kg/ha', 'description': 'High phosphorus'},
            'K': {'optimal': [200, 300], 'unit': 'kg/ha', 'description': 'Very high potassium for bean development'},
            'ph': {'optimal': [6.0, 6.5], 'unit': '', 'description': 'Slightly acidic'},
            'temperature': {'optimal': [15, 25], 'unit': '°C', 'description': 'Cool to moderate temperature'},
            'humidity': {'optimal': [70, 80], 'unit': '%', 'description': 'High humidity'},
            'rainfall': {'optimal': [150, 200], 'unit': 'mm', 'description': 'High rainfall'}
        },
        'recommended_fertilizers': ['Urea', 'DAP', 'MOP'],
        'fertilizer_schedule': 'Split application: pre-monsoon, post-monsoon, post-harvest',
        'soil_type': ['Red', 'Loamy'],
        'season': 'Perennial',
        'growth_duration': 'Perennial shrub'
    }
}

# Fertilizer details for recommendations
FERTILIZER_DETAILS = {
    'Urea': {
        'composition': '46% Nitrogen',
        'benefits': 'Rapid nitrogen supply, promotes vegetative growth',
        'application_rate': '100-200 kg/ha',
        'best_for': 'Leafy crops, cereals, fruit trees'
    },
    'DAP': {
        'composition': '18% Nitrogen, 46% Phosphorus',
        'benefits': 'Root development, flowering, energy transfer',
        'application_rate': '100-150 kg/ha',
        'best_for': 'All crops during planting'
    },
    'MOP': {
        'composition': '60% Potassium',
        'benefits': 'Disease resistance, water regulation, fruit quality',
        'application_rate': '50-100 kg/ha',
        'best_for': 'Fruit crops, root crops'
    },
    '14:35:14': {
        'composition': '14% N, 35% P, 14% K',
        'benefits': 'Balanced nutrition with high phosphorus',
        'application_rate': '150-200 kg/ha',
        'best_for': 'Legumes, root crops'
    },
    '17:17:17': {
        'composition': '17% N, 17% P, 17% K',
        'benefits': 'Complete balanced nutrition',
        'application_rate': '200-250 kg/ha',
        'best_for': 'General purpose fertilizer'
    },
    '20:20': {
        'composition': '20% N, 20% P',
        'benefits': 'High nitrogen and phosphorus',
        'application_rate': '150-200 kg/ha',
        'best_for': 'Early growth stages'
    },
    '28:28': {
        'composition': '28% N, 28% P',
        'benefits': 'High concentration N-P fertilizer',
        'application_rate': '100-150 kg/ha',
        'best_for': 'Intensive farming'
    }
}