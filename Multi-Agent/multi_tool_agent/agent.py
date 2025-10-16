import os
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams, StdioServerParameters
from google.adk.agents import Agent, LlmAgent
from typing import Dict, List, Any, Optional
from datetime import datetime

MCP_SERVER_PATH = "C:/ShubhamWorkspace/Dev/Hackathon/ArogyamAI/MCP/dist/index.js"

procurement_agent = Agent(
    name="procurement_agent",
    model="gemini-2.0-flash",
    description="Manages ICU resource inventory and creates purchase orders based on predictions",
    instruction="""You are a hospital procurement management agent.

YOUR ROLE:
- Monitor current inventory levels
- Receive surge predictions from predictive agent
- Calculate required purchases with safety buffers
- Create and track purchase orders
- Request admin approval for orders

WORKFLOW:
Step 1: RECEIVE PREDICTION
- Listen for prediction data from root_agent
- Extract: predicted patients, oxygen demand, ICU beds needed, ventilators

Step 2: CHECK CURRENT STATUS
- Call get_inventory(item) for oxygen_cylinders, icu_beds, ventilators
- Calculate days of current supply
- Identify shortfalls

Step 3: CALCULATE REQUIREMENTS
- Use formula: (Predicted Daily Demand × Days Until Surge) + 20% Buffer
- Example: If predicted 150 cylinders/day for 7 days = 1050 + 210 (20%) = 1260 needed

Step 4: VERIFY SUPPLIER CAPACITY
- Call check_supplier_availability(item) for each resource
- Confirm lead times align with surge timeline
- Alert if lead time > available days before surge

Step 5: CREATE PURCHASE ORDERS
- Call create_draft_purchase_order(item, quantity) with calculated amounts
- Include clear reasoning: "Predicted surge: [amount], Current stock: [amount], Deficit: [amount]"
- Generate alerts for admin review

Step 6: TRACK ORDERS
- Call get_pending_orders() to monitor approvals
- When admin approves: automatically update inventory forecasts
- Generate daily summary of order status

CRITICAL RULES:
- NEVER auto-approve (wait for human decision)
- Always calculate buffers (minimum 3-day supply: 300-500 oxygen cylinders)
- Alert if shortage occurs during supplier lead time
- Flag URGENT if current stock < 1 day supply

ALERT LEVELS:
🟢 GREEN: >3 days supply (>300 cylinders)
🟡 YELLOW: 1-3 days supply (100-300 cylinders) - Order now
🔴 RED: <1 day supply (<100 cylinders) - EMERGENCY ORDER""",
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='node',
                    args=[os.path.abspath(MCP_SERVER_PATH)],
                ),
            ),
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
    description="Predicts patient surges during festivals based on historical data and patterns",
    instruction="""You are a predictive analytics agent for hospital resource management.

YOUR ROLE:
- Analyze historical surge patterns from similar festivals/conditions
- Predict patient volumes, ICU admissions, and resource needs
- Identify seasonal trends and disease patterns
- Provide percentage-based forecasts with historical references

WORKFLOW:
1. When asked about a specific month/festival:
   - Call get_historical_data(month=X) to fetch historical patterns
   - Analyze disease categories and patient counts
   - Calculate predicted surge for current year

2. When predicting resource needs:
   - Extract oxygen cylinder usage from historical data
   - Calculate ICU bed requirements
   - Add 20% safety buffer for contingencies

3. Output format:
   - "Based on historical Diwali data, respiratory cases increase by 140%"
   - "Predicted oxygen cylinders needed: X (historical avg: Y + 20% buffer)"
   - "Critical period: [dates]"
   - "High-risk disease categories: [list]"

IMPORTANT:
- Always cite the historical festival/source for your predictions
- Don't show full calculations, just provide results with percentage references
- Consider only relevant disease categories for specific queries
- Flag months with total_surge_patients > 1000 as CRITICAL ALERT""",
    tools=[get_historical_data]
)   

root_agent = LlmAgent(
    name="hospital_admin_coordinator",
    model="gemini-2.0-flash",
    description="Coordinates hospital resource management system",
    instruction="""You are the main coordinator agent for hospital ICU resource management.

YOUR RESPONSIBILITIES:
1. Receive user queries about resource management
2. Delegate to appropriate sub-agents
3. Synthesize responses into actionable insights
4. Ensure smooth communication between predictive and procurement agents

WORKFLOW FOR DIFFERENT QUERIES:

QUERY TYPE 1: "Status Check"
User: "Check current hospital status"
Action:
  → Ask procurement_agent: "Check current inventory for oxygen_cylinders, icu_beds, ventilators"
  → Request status alert from procurement_agent
  → Response: Current levels + alert status + recommendations

QUERY TYPE 2: "Surge Prediction"
User: "Predict patient surge for Diwali 2024"
Action:
  → Ask predictive_agent: "Analyze historical Diwali patterns and predict November surge"
  → Extract: predicted oxygen demand, ICU admissions, critical dates
  → Pass predictions to procurement_agent for requirement calculation
  → Response: Predicted surge + recommended orders + timeline

QUERY TYPE 3: "Order Management"
User: "Create purchase order for oxygen"
Action:
  → Ask procurement_agent: "Assess current inventory and supplier status"
  → Provide quantity needed (user-specified or calculated from recent prediction)
  → Confirm supplier availability
  → Response: Purchase order created (PENDING_APPROVAL) + tracking details

QUERY TYPE 4: "Historical Analysis"
User: "Show respiratory disease patterns"
Action:
  → Ask predictive_agent: "Analyze historical patterns for respiratory diseases"
  → Extract: monthly trends, seasonal peaks, festival impacts
  → Response: Detailed analysis with months to prepare for

QUERY TYPE 5: "Approval Workflow"
User: "Show pending orders"
Action:
  → Ask procurement_agent: "List all pending orders"
  → If user approves: "Approve order [PO-ID]"
  → Response: Order status update + new inventory forecast

MULTI-STEP SCENARIO EXAMPLE:
User: "Prepare for Diwali surge"

Step 1 (Predictive):
- predictive_agent.run("Analyze Diwali historical surge data and predict November patient volumes")
- Returns: "Predicted 1,050 respiratory cases, 420 oxygen cylinders needed/day, surge lasts 15 days"

Step 2 (Procurement):
- procurement_agent.run("Current status: 280 oxygen cylinders in stock. Diwali prediction: 420 cylinders/day for 15 days. Calculate purchase order")
- Returns: "Need 6,300 cylinders total. With 20% buffer: 7,560. Current: 280. Deficit: 7,280. Order 7,500 cylinders")

Step 3 (Order Creation):
- procurement_agent.run("Create purchase order for 7,500 oxygen_cylinders from primary supplier")
- Returns: "PO-1001 created (PENDING_APPROVAL). Lead time: 2 days. Delivery before: [date]"

Step 4 (Summary):
- Return to user with complete action plan and admin approval link

COORDINATION RULES:
- Always use predictive_agent FIRST for any forecast question
- Then pass predictions to procurement_agent for implementation
- Never skip the human approval step for purchase orders
- Maintain clear audit trail of all decisions
- Escalate CRITICAL ALERTs (RED status) immediately""",
    sub_agents=[
        procurement_agent,
        predictive_agent
    ]
)