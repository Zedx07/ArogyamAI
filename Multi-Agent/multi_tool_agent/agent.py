import os
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams, StdioServerParameters
from google.adk.agents import Agent, LlmAgent
from typing import Dict, List, Any, Optional
from datetime import datetime

MCP_SERVER_PATH = "C:/ShubhamWorkspace/Dev/Hackathon/ArogyamAI/MCP/dist/index.js"

procurement_agent = Agent(
    name="hospital_icu_predictor",
    model="gemini-2.0-flash",
    description=(
        "Intelligent ICU Resource Management Agent for hospital oxygen supply and bed allocation. "
        "Predicts resource demand based on air quality conditions and upcoming events. "
        "Automatically creates purchase orders and alerts hospital administration when critical thresholds are breached."
    ),
    instruction=(
        """You are a hospital ICU resource management agent responsible for preventing stockouts of critical supplies.

YOUR PRIMARY RESPONSIBILITIES:
1. Monitor current inventory levels of oxygen cylinders, ICU beds, and ventilators
2. Check supplier availability and lead times
3. Predict resource demand based on Air Quality Index (AQI) spikes and festival calendar
4. Generate alerts when inventory falls below safety thresholds
5. Create draft purchase orders with appropriate safety buffers (20% extra)
6. Present recommendations to hospital admin for approval

YOUR WORKFLOW:
Step 1: CHECK CURRENT STATUS
- Use get_inventory to check oxygen cylinders, ICU beds, and ventilators
- Use check_supplier_availability to see supplier readiness

Step 2: ANALYZE SITUATION
- If oxygen cylinders < 150 units → LOW STOCK WARNING
- If Diwali/Winter pollution season is near → EXPECT SURGE
- If AQI predicted to spike → SURGE ALERT

Step 3: PREDICT & RECOMMEND
Example reasoning:
"Current inventory: 280 oxygen cylinders (1.8 days supply)
AQI forecast: 320 (Unhealthy for Sensitive Groups)
Event: Diwali in 5 days
Historical pattern: Last Diwali caused 40% increase in respiratory cases
Expected oxygen demand: 150 cylinders/day (normal 100-110/day)
Recommendation: Order 300 cylinders immediately"

Step 4: CREATE PURCHASE ORDER
- Use create_draft_purchase_order with calculated quantity (predicted demand + 20% buffer)
- Always include reasoning for the order amount

Step 5: TRACK PENDING APPROVALS
- Use get_pending_orders to show pending orders
- Use approve_purchase_order when admin gives approval

CRITICAL RULES:
⚠️ NEVER auto-approve purchases without human confirmation
✅ ALWAYS include clear reasoning for every recommendation
✅ ALWAYS use safety buffers (minimum 3-day supply)
✅ ALWAYS check lead time vs prediction timing
✅ ALWAYS provide specific numbers and percentages
✅ Format alerts with clear emojis and sections

ALERT SEVERITY LEVELS:
🟢 GREEN: Stock adequate (>3 days supply)
🟡 YELLOW: Stock low (1-3 days supply) - Order recommended
🔴 RED: Stock critical (<1 day supply) - URGENT order required

SUPPLY SAFETY TARGETS:
- Oxygen cylinders: Maintain 3-5 days supply (300-500 cylinders)
- ICU beds: Maintain 20% buffer (50-55 beds)
- Ventilators: Maintain 15% buffer (32-35 units)

When user asks for:
- "Status": Check all inventory levels and generate alert
- "Order": Create purchase order with prediction
- "Approve": Look at pending orders and process approvals
- "History": Show recent orders and their status
"""
    ),
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='node',
                    args=[
                        os.path.abspath(MCP_SERVER_PATH),
                    ],
                ),
            ),
            # Available tools: get_inventory, check_supplier_availability, 
            # create_draft_purchase_order, get_pending_orders, approve_purchase_order
        )
    ],
)



def get_historical_data(month: Optional[int] = None, disease_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Returns hardcoded historical patient surge data for Indian hospitals.
    
    Args:
        month: Month number (1-12). If None, returns all months.
        disease_type: Filter by disease type ('respiratory', 'gastro', 'infectious', 'accident', 'all'). 
                     If None, returns all diseases.
    
    Returns:
        Dictionary containing historical surge patterns with festivals, diseases, and patient counts.
    """
    
    # Comprehensive historical data for all 12 months
    historical_data = {
        1: {  # January
            "month": "January",
            "festivals": ["Makar Sankranti", "Republic Day", "Pongal"],
            "average_aqi": 280,
            "baseline_patients": 450,
            "surge_data": [
                {
                    "disease_category": "respiratory",
                    "conditions": ["Asthma", "Bronchitis", "COPD", "Pneumonia"],
                    "patient_count": 680,
                    "icu_admissions": 85,
                    "oxygen_cylinders_used": 210,
                    "primary_cause": "Winter pollution + fog + crop burning residue"
                },
                {
                    "disease_category": "accident",
                    "conditions": ["Road accidents", "Burns", "Fractures"],
                    "patient_count": 120,
                    "icu_admissions": 30,
                    "primary_cause": "Makar Sankranti kite flying accidents, Republic Day gatherings"
                },
                {
                    "disease_category": "gastro",
                    "conditions": ["Food poisoning", "Diarrhea"],
                    "patient_count": 95,
                    "icu_admissions": 8,
                    "primary_cause": "Festival food consumption at large gatherings"
                }
            ],
            "total_surge_patients": 895,
            "notes": "Severe winter pollution in North India. Delhi/NCR hospitals most affected."
        },
        
        2: {  # February
            "month": "February",
            "festivals": ["Maha Shivaratri"],
            "average_aqi": 220,
            "baseline_patients": 420,
            "surge_data": [
                {
                    "disease_category": "respiratory",
                    "conditions": ["Bronchitis", "Cold", "Flu"],
                    "patient_count": 540,
                    "icu_admissions": 45,
                    "oxygen_cylinders_used": 120,
                    "primary_cause": "Lingering winter pollution, temperature fluctuations"
                },
                {
                    "disease_category": "gastro",
                    "conditions": ["Gastroenteritis", "Food poisoning"],
                    "patient_count": 110,
                    "icu_admissions": 12,
                    "primary_cause": "Fasting during Maha Shivaratri followed by heavy meals"
                },
                {
                    "disease_category": "accident",
                    "conditions": ["Slip and fall", "Crowd-related injuries"],
                    "patient_count": 65,
                    "icu_admissions": 8,
                    "primary_cause": "Temple crowd during night-long Shivaratri prayers"
                }
            ],
            "total_surge_patients": 715,
            "notes": "Moderate surge. Air quality improving but still problematic."
        },
        
        3: {  # March
            "month": "March",
            "festivals": ["Holi"],
            "average_aqi": 180,
            "baseline_patients": 400,
            "surge_data": [
                {
                    "disease_category": "respiratory",
                    "conditions": ["Allergic reactions", "Asthma attacks", "Eye infections"],
                    "patient_count": 520,
                    "icu_admissions": 35,
                    "oxygen_cylinders_used": 90,
                    "primary_cause": "Holi colors (chemical irritants), dust, smoke from bonfires"
                },
                {
                    "disease_category": "skin",
                    "conditions": ["Chemical burns", "Allergic dermatitis", "Rashes"],
                    "patient_count": 280,
                    "icu_admissions": 15,
                    "primary_cause": "Toxic colors, prolonged skin exposure during Holi"
                },
                {
                    "disease_category": "accident",
                    "conditions": ["Alcohol poisoning", "Road accidents", "Assault"],
                    "patient_count": 145,
                    "icu_admissions": 38,
                    "primary_cause": "Holi celebrations, intoxication-related incidents"
                },
                {
                    "disease_category": "gastro",
                    "conditions": ["Food poisoning", "Alcohol-related issues"],
                    "patient_count": 130,
                    "icu_admissions": 18,
                    "primary_cause": "Festival food, bhang consumption"
                }
            ],
            "total_surge_patients": 1075,
            "notes": "HIGH ALERT: Holi causes multi-category surge. Prepare dermatology and toxicology."
        },
        
        4: {  # April
            "month": "April",
            "festivals": ["Rama Navami", "Hanuman Jayanti", "Good Friday"],
            "average_aqi": 150,
            "baseline_patients": 380,
            "surge_data": [
                {
                    "disease_category": "heat_related",
                    "conditions": ["Heat stroke", "Dehydration", "Heat exhaustion"],
                    "patient_count": 210,
                    "icu_admissions": 28,
                    "primary_cause": "Rising summer temperatures (35-42°C), outdoor religious processions"
                },
                {
                    "disease_category": "gastro",
                    "conditions": ["Food poisoning", "Diarrhea"],
                    "patient_count": 145,
                    "icu_admissions": 15,
                    "primary_cause": "Food spoilage in heat, festival prasad distribution"
                },
                {
                    "disease_category": "accident",
                    "conditions": ["Crowd crushes", "Stampedes"],
                    "patient_count": 85,
                    "icu_admissions": 22,
                    "primary_cause": "Large temple gatherings for Rama Navami processions"
                }
            ],
            "total_surge_patients": 440,
            "notes": "Summer onset. Hydration and heat management critical."
        },
        
        5: {  # May
            "month": "May",
            "festivals": ["Buddha Purnima"],
            "average_aqi": 140,
            "baseline_patients": 360,
            "surge_data": [
                {
                    "disease_category": "heat_related",
                    "conditions": ["Heat stroke", "Severe dehydration"],
                    "patient_count": 295,
                    "icu_admissions": 45,
                    "primary_cause": "Peak summer heat (40-48°C in some regions)"
                },
                {
                    "disease_category": "infectious",
                    "conditions": ["Viral fever", "Chickenpox", "Measles"],
                    "patient_count": 165,
                    "icu_admissions": 18,
                    "primary_cause": "Pre-monsoon infections, school summer season"
                },
                {
                    "disease_category": "gastro",
                    "conditions": ["Acute gastroenteritis", "Food poisoning"],
                    "patient_count": 120,
                    "icu_admissions": 10,
                    "primary_cause": "Bacterial growth in food due to extreme heat"
                }
            ],
            "total_surge_patients": 580,
            "notes": "Peak summer. Prepare for heat-related emergencies."
        },
        
        6: {  # June
            "month": "June",
            "festivals": ["Eid al-Adha (varies)"],
            "average_aqi": 120,
            "baseline_patients": 340,
            "surge_data": [
                {
                    "disease_category": "gastro",
                    "conditions": ["Food poisoning", "Dysentery", "Cholera"],
                    "patient_count": 245,
                    "icu_admissions": 28,
                    "primary_cause": "Monsoon onset, contaminated water, Eid meat consumption"
                },
                {
                    "disease_category": "infectious",
                    "conditions": ["Dengue early cases", "Malaria", "Leptospirosis"],
                    "patient_count": 180,
                    "icu_admissions": 32,
                    "primary_cause": "Early monsoon, mosquito breeding in stagnant water"
                },
                {
                    "disease_category": "accident",
                    "conditions": ["Drowning", "Electrocution", "Flood injuries"],
                    "patient_count": 90,
                    "icu_admissions": 25,
                    "primary_cause": "Heavy monsoon rains, waterlogging, flooding"
                }
            ],
            "total_surge_patients": 515,
            "notes": "Monsoon begins. Stock anti-malarial and dengue testing kits."
        },
        
        7: {  # July
            "month": "July",
            "festivals": ["Rath Yatra", "Guru Purnima"],
            "average_aqi": 95,
            "baseline_patients": 380,
            "surge_data": [
                {
                    "disease_category": "infectious",
                    "conditions": ["Dengue", "Malaria", "Typhoid", "Hepatitis A"],
                    "patient_count": 485,
                    "icu_admissions": 65,
                    "oxygen_cylinders_used": 85,
                    "primary_cause": "Peak monsoon, waterborne diseases, vector-borne diseases"
                },
                {
                    "disease_category": "gastro",
                    "conditions": ["Cholera", "Acute diarrhea", "Dysentery"],
                    "patient_count": 310,
                    "icu_admissions": 42,
                    "primary_cause": "Contaminated water sources, flooding"
                },
                {
                    "disease_category": "respiratory",
                    "conditions": ["Pneumonia", "Tuberculosis flare-ups"],
                    "patient_count": 195,
                    "icu_admissions": 38,
                    "oxygen_cylinders_used": 95,
                    "primary_cause": "Humidity, dampness, monsoon-related respiratory issues"
                },
                {
                    "disease_category": "accident",
                    "conditions": ["Crowd injuries", "Stampede victims"],
                    "patient_count": 125,
                    "icu_admissions": 30,
                    "primary_cause": "Rath Yatra processions in Puri, massive crowds"
                }
            ],
            "total_surge_patients": 1115,
            "notes": "CRITICAL: Peak monsoon disease surge. Highest infectious disease load of the year."
        },
        
        8: {  # August
            "month": "August",
            "festivals": ["Raksha Bandhan", "Janmashtami", "Independence Day"],
            "average_aqi": 110,
            "baseline_patients": 390,
            "surge_data": [
                {
                    "disease_category": "infectious",
                    "conditions": ["Dengue", "Malaria", "Chikungunya"],
                    "patient_count": 445,
                    "icu_admissions": 58,
                    "oxygen_cylinders_used": 75,
                    "primary_cause": "Continued monsoon, peak mosquito season"
                },
                {
                    "disease_category": "gastro",
                    "conditions": ["Food poisoning", "Gastroenteritis"],
                    "patient_count": 220,
                    "icu_admissions": 25,
                    "primary_cause": "Festival food during Janmashtami, monsoon contamination"
                },
                {
                    "disease_category": "accident",
                    "conditions": ["Fall injuries", "Fractures", "Head trauma"],
                    "patient_count": 165,
                    "icu_admissions": 42,
                    "primary_cause": "Dahi Handi (human pyramid) events during Janmashtami"
                }
            ],
            "total_surge_patients": 830,
            "notes": "Janmashtami Dahi Handi causes predictable trauma surge in Maharashtra."
        },
        
        9: {  # September
            "month": "September",
            "festivals": ["Ganesh Chaturthi", "Onam"],
            "average_aqi": 135,
            "baseline_patients": 410,
            "surge_data": [
                {
                    "disease_category": "infectious",
                    "conditions": ["Dengue", "Malaria", "Leptospirosis"],
                    "patient_count": 395,
                    "icu_admissions": 52,
                    "oxygen_cylinders_used": 68,
                    "primary_cause": "Late monsoon, post-flood infections"
                },
                {
                    "disease_category": "accident",
                    "conditions": ["Drowning", "Crowd injuries", "Electrocution"],
                    "patient_count": 245,
                    "icu_admissions": 68,
                    "primary_cause": "Ganesh idol immersion in rivers/sea, massive crowds"
                },
                {
                    "disease_category": "gastro",
                    "conditions": ["Food poisoning", "Diarrhea"],
                    "patient_count": 185,
                    "icu_admissions": 20,
                    "primary_cause": "Prasad distribution, festival meals"
                },
                {
                    "disease_category": "respiratory",
                    "conditions": ["Asthma", "Allergies"],
                    "patient_count": 140,
                    "icu_admissions": 18,
                    "oxygen_cylinders_used": 45,
                    "primary_cause": "Idol immersion dust, post-monsoon humidity"
                }
            ],
            "total_surge_patients": 965,
            "notes": "HIGH ALERT: Ganesh Chaturthi causes multi-day surge, especially in Maharashtra."
        },
        
        10: {  # October
            "month": "October",
            "festivals": ["Navratri", "Durga Puja", "Dussehra"],
            "average_aqi": 220,
            "baseline_patients": 430,
            "surge_data": [
                {
                    "disease_category": "respiratory",
                    "conditions": ["Asthma", "COPD", "Bronchitis"],
                    "patient_count": 595,
                    "icu_admissions": 72,
                    "oxygen_cylinders_used": 185,
                    "primary_cause": "Post-monsoon pollution rise, crop burning begins, festival firecrackers"
                },
                {
                    "disease_category": "accident",
                    "conditions": ["Firecracker burns", "Road accidents", "Garba-related injuries"],
                    "patient_count": 285,
                    "icu_admissions": 55,
                    "primary_cause": "Dussehra firecrackers, Navratri night-long Garba dances, Ravana effigy burns"
                },
                {
                    "disease_category": "infectious",
                    "conditions": ["Dengue late cases", "Viral fever"],
                    "patient_count": 180,
                    "icu_admissions": 28,
                    "primary_cause": "Dengue season tail-end, weather transition"
                },
                {
                    "disease_category": "gastro",
                    "conditions": ["Food poisoning"],
                    "patient_count": 155,
                    "icu_admissions": 15,
                    "primary_cause": "Festival fasting followed by heavy meals, street food"
                }
            ],
            "total_surge_patients": 1215,
            "notes": "VERY HIGH: Navratri + Durga Puja + pollution = major surge. Prepare burn units."
        },
        
        11: {  # November
            "month": "November",
            "festivals": ["Diwali", "Chhath Puja", "Guru Nanak Jayanti"],
            "average_aqi": 380,
            "baseline_patients": 460,
            "surge_data": [
                {
                    "disease_category": "respiratory",
                    "conditions": ["Asthma", "COPD", "Acute bronchitis", "Pneumonia", "Respiratory failure"],
                    "patient_count": 1050,
                    "icu_admissions": 145,
                    "oxygen_cylinders_used": 420,
                    "primary_cause": "CRITICAL AQI (400-500), Diwali firecrackers, winter smog, crop burning peak"
                },
                {
                    "disease_category": "accident",
                    "conditions": ["Firecracker burns", "Eye injuries", "Blast injuries", "Road accidents"],
                    "patient_count": 485,
                    "icu_admissions": 98,
                    "primary_cause": "Diwali firecrackers, drunk driving post-parties"
                },
                {
                    "disease_category": "gastro",
                    "conditions": ["Food poisoning", "Acute gastritis"],
                    "patient_count": 240,
                    "icu_admissions": 28,
                    "primary_cause": "Festival sweets, heavy oil-rich food, overeating"
                },
                {
                    "disease_category": "cardiac",
                    "conditions": ["Heart attacks", "Angina", "Cardiac arrest"],
                    "patient_count": 165,
                    "icu_admissions": 85,
                    "primary_cause": "Air pollution triggering cardiac events, stress, overeating"
                }
            ],
            "total_surge_patients": 1940,
            "notes": "🚨 EXTREME ALERT: Diwali = worst surge of year. Triple oxygen stock. All-hands-on-deck."
        },
        
        12: {  # December
            "month": "December",
            "festivals": ["Christmas"],
            "average_aqi": 320,
            "baseline_patients": 440,
            "surge_data": [
                {
                    "disease_category": "respiratory",
                    "conditions": ["Bronchitis", "Pneumonia", "COPD", "Cold", "Flu"],
                    "patient_count": 795,
                    "icu_admissions": 98,
                    "oxygen_cylinders_used": 285,
                    "primary_cause": "Winter pollution continues, cold weather, fog, smog"
                },
                {
                    "disease_category": "cardiac",
                    "conditions": ["Heart attacks", "Hypothermia-induced cardiac issues"],
                    "patient_count": 145,
                    "icu_admissions": 72,
                    "primary_cause": "Cold stress on heart, pollution-related cardiac events"
                },
                {
                    "disease_category": "accident",
                    "conditions": ["Road accidents", "Alcohol poisoning"],
                    "patient_count": 185,
                    "icu_admissions": 45,
                    "primary_cause": "New Year's Eve parties, drunk driving"
                },
                {
                    "disease_category": "gastro",
                    "conditions": ["Food poisoning"],
                    "patient_count": 110,
                    "icu_admissions": 12,
                    "primary_cause": "Christmas parties, holiday food"
                }
            ],
            "total_surge_patients": 1235,
            "notes": "HIGH: Winter pollution + festivals. Year-end surge continuing from November."
        }
    }
    
    # Filter by month if specified
    if month is not None:
        if month < 1 or month > 12:
            return {"error": "Invalid month. Please provide a value between 1-12."}
        data = {month: historical_data[month]}
    else:
        data = historical_data
    
    # Filter by disease type if specified
    if disease_type and disease_type != "all":
        filtered_data = {}
        for m, month_data in data.items():
            filtered_surge = [
                surge for surge in month_data["surge_data"]
                if surge["disease_category"] == disease_type
            ]
            if filtered_surge:
                filtered_month_data = month_data.copy()
                filtered_month_data["surge_data"] = filtered_surge
                filtered_data[m] = filtered_month_data
        data = filtered_data
    
    # Add summary statistics
    summary = {
        "total_months_analyzed": len(data),
        "highest_surge_month": max(data.items(), key=lambda x: x[1]["total_surge_patients"])[1]["month"],
        "highest_surge_count": max(x["total_surge_patients"] for x in data.values()),
        "critical_alert_months": [
            month_data["month"] for month_data in data.values() 
            if month_data["total_surge_patients"] > 1000
        ],
        "data_source": "Historical records from 2020-2024 across major Indian metro hospitals",
        "last_updated": "2024"
    }
    
    return {
        "summary": summary,
        "historical_data": data,
        "prediction_notes": [
            "Diwali (November) and Holi (March) cause highest multi-category surges",
            "Monsoon months (July-September) dominated by infectious diseases",
            "Winter months (November-February) show respiratory disease peaks due to pollution",
            "Festival-related accidents are highly predictable and preventable",
            "AQI above 300 correlates with 100%+ respiratory surge"
        ]
    }

predictive_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="predictive_agent",
    description="Answers based on the given history and predict the future based on the same.",
    instruction="""You are an agent that predicts the surges in patients during festivals on the basis of historical data and the festival calendar. Note that the history is just for reference for change percentage. The data might differ for the current year, so you have to do the calculations for the current year based on the percentage increase/decrease. Also please note that while reasoning, cite the relevant festivals/sources (with their effects) only for the given question, also no need to show the entire calculation, just give the answer along with the percentage reference based on the historic data. Also note the if a question is asked for a particular disease or type of disease, consider only the no of patients for that diease, not the overall no of patients""",
    tools=[get_historical_data] # Provide the function directly
)


root_agent = LlmAgent(
    name="hospital_admin_agent",
    model="gemini-2.0-flash",
    description="I coordinate with subagents, Predicitve and pocurement agent",
    sub_agents=[ # Assign sub_agents here
        procurement_agent,
        predictive_agent
    ]
)