import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="Fleet Managers Dashboard",
    layout="wide",
    page_icon="🚛",
    initial_sidebar_state="expanded"
)

# Professional CSS Styling
st.markdown("""
<style>
    /* Main Container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0 !important;
    }
    
    .block-container {
        padding: 2rem 3rem !important;
        max-width: none !important;
    }
    
    /* Headers */
    h1 {
        color: #1e293b;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    h2 {
        color: #334155;
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
    }
    
    h3 {
        color: #475569;
        font-size: 1.3rem !important;
        font-weight: 500 !important;
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        border: 1px solid #e2e8f0;
    }
    
    [data-testid="stMetric"] label {
        font-size: 0.9rem !important;
        color: #64748b !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #1e293b !important;
    }
    
    /* DataFrames */
    [data-testid="stDataFrame"] {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        color: white;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: white;
        padding: 0.5rem;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: white;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        font-weight: 600;
        color: #1e293b;
    }
    
    /* Success/Warning/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stError {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border-radius: 8px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Data Generation Functions
@st.cache_data
def generate_vehicles(count=150):
    models = ['Heavy Truck 45T', 'Heavy Truck 40T', 'Medium Truck 25T', 'Light Truck 12T', 'Multi-Axle 49T']
    states = ['MH', 'DL', 'GJ', 'KA', 'TN', 'UP', 'RJ', 'HR', 'PB', 'WB']
    statuses = ['Active', 'Idle', 'Maintenance']
    regions = ['North', 'South', 'East', 'West', 'Central']
    
    vehicles = []
    for i in range(1, count + 1):
        state = random.choice(states)
        dist = str(random.randint(1, 50)).zfill(2)
        series = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))
        num = str(random.randint(1000, 9999))
        
        odo = random.randint(50000, 550000)
        maint_cost_total = random.randint(50000, 250000)
        maint_cpkm = round(maint_cost_total / odo, 2)
        
        vehicles.append({
            'Vehicle ID': f"{state}-{dist}-TRK-{num}",
            'Model': random.choice(models),
            'Status': random.choice(statuses),
            'Region': random.choice(regions),
            'Driver': f"Driver {chr(65 + i//10)}{i%10}",
            'FE (km/L)': round(random.uniform(3.2, 5.2), 2),
            'Odometer (km)': odo,
            'Daily Distance (km)': random.randint(200, 600),
            'Operating Cost/KM (₹)': round(random.uniform(25, 45), 2),
            'Maintenance Cost Total (₹)': maint_cost_total,
            'Maintenance CPKM (₹)': maint_cpkm,
            'Daily CO2 (kg)': round(random.uniform(15, 30), 1),
            'Idle Time (min)': random.randint(20, 180),
            'Speed Avg (km/h)': random.randint(45, 75),
            'Last Service (days ago)': random.randint(5, 90),
            'Next Service (days)': random.randint(-10, 60),
            'Harsh Braking': random.randint(0, 15),
            'Harsh Acceleration': random.randint(0, 12),
            'Overspeed Events': random.randint(0, 10)
        })
    
    return pd.DataFrame(vehicles)

@st.cache_data
def generate_drivers(count=145):
    drivers = []
    for i in range(1, count + 1):
        trips = random.randint(50, 150)
        total_dist = random.randint(50000, 200000)
        
        drivers.append({
            'Name': f"Driver {chr(65 + i//10)}{i%10}",
            'Score': random.randint(70, 100),
            'Efficiency (km/L)': round(random.uniform(3.5, 5.0), 2),
            'Total Trips': trips,
            'Total Distance (km)': total_dist,
            'Avg Distance/Trip (km)': round(total_dist / trips, 1),
            'Violations': random.randint(0, 5),
            'Experience (years)': random.randint(2, 15),
            'Training Complete': random.random() > 0.13,
            'Harsh Braking': random.randint(0, 20),
            'Harsh Acceleration': random.randint(0, 18),
            'Speeding Events': random.randint(0, 15),
            'Fatigue Alerts': random.randint(0, 8),
            'Monthly Salary (₹)': random.randint(35000, 65000)
        })
    
    return pd.DataFrame(drivers)

# Load Data
df_vehicles = generate_vehicles(150)
df_drivers = generate_drivers(145)

# Sidebar Navigation
with st.sidebar:
    st.markdown("## 🚛 Fleet Dashboard")
    st.markdown("**Indian HCV Management**")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        [
            "🏠 Fleet Overview",
            "🚛 Vehicle Analysis",
            "👤 Driver Performance",
            "🌱 CO2 Analytics",
            "🔧 Maintenance & CPKM",
            "💰 Cost Analysis",
            "✅ Compliance"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### Quick Stats")
    st.metric("Total Vehicles", "150")
    st.metric("Total Drivers", "145")
    st.metric("Fleet Efficiency", "4.1 km/L")

# FLEET OVERVIEW
if page == "🏠 Fleet Overview":
    st.title("📊 Fleet Overview Dashboard")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Fleet Efficiency", "4.1 km/L", "↑ 7.2%", delta_color="normal")
    with col2:
        st.metric("Weekly Fuel Cost", "₹1.68L", "↓ ₹17.4K", delta_color="inverse")
    with col3:
        active = len(df_vehicles[df_vehicles['Status'] == 'Active'])
        st.metric("Active Vehicles", f"{active}/150", f"{150-active} inactive")
    with col4:
        total_co2 = df_vehicles['Daily CO2 (kg)'].sum()
        st.metric("Daily CO2", f"{total_co2:.0f} kg", "↓ 15.3%", delta_color="inverse")
    
    st.markdown("---")
    
    # Performance Trends
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📈 Fleet Performance Trends")
        view = st.radio("Time Period", ["Daily", "Weekly", "Monthly"], horizontal=True)
        
        if view == "Daily":
            fig = px.line(
                x=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                y=[4.1, 4.3, 4.2, 4.4, 4.5, 4.3, 4.4],
                labels={'x': 'Day', 'y': 'Efficiency (km/L)'},
                template='plotly_white'
            )
        elif view == "Weekly":
            fig = px.line(
                x=['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                y=[4.2, 4.3, 4.1, 4.4],
                template='plotly_white'
            )
        else:
            fig = px.line(
                x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                y=[4.0, 4.1, 4.2, 4.1, 4.3, 4.4],
                template='plotly_white'
            )
        
        fig.update_traces(line_color='#667eea', fill='tozeroy', fillcolor='rgba(102, 126, 234, 0.2)')
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🗺️ Regional Distribution")
        region_counts = df_vehicles['Region'].value_counts()
        fig = px.pie(
            values=region_counts.values,
            names=region_counts.index,
            color_discrete_sequence=px.colors.sequential.Purples_r
        )
        fig.update_layout(height=350, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Priority Alerts
    st.markdown("### 🚨 Priority Alerts")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.error("**⚠️ Critical Alert**  \nMH-12-TRK-052 - Extended idle: 285 min  \nFuel waste: 18.4L")
    
    with col2:
        st.warning("**🔧 Maintenance Due**  \nGJ-01-TRK-031 - Brake service overdue  \nOverdue by: 1,200km")
    
    with col3:
        st.success("**📈 Top Performer**  \nDriver A1 - Excellent efficiency  \nImprovement: 22% this month")

# VEHICLE ANALYSIS
elif page == "🚛 Vehicle Analysis":
    st.title("🚛 Vehicle Analysis & Drill-Down")
    
    st.markdown("### Vehicle Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Vehicles", len(df_vehicles))
    with col2:
        st.metric("Avg Efficiency", f"{df_vehicles['FE (km/L)'].mean():.2f} km/L")
    with col3:
        st.metric("Avg Odometer", f"{df_vehicles['Odometer (km)'].mean()/1000:.0f}K km")
    with col4:
        st.metric("Maintenance Needed", len(df_vehicles[df_vehicles['Status'] == 'Maintenance']))
    
    st.markdown("---")
    
    # Search and Filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍 Search by Vehicle ID", placeholder="e.g., MH-12-TRK-1234")
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All"] + list(df_vehicles['Status'].unique()))
    
    # Apply filters
    filtered_df = df_vehicles.copy()
    if search:
        filtered_df = filtered_df[filtered_df['Vehicle ID'].str.contains(search, case=False, na=False)]
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df['Status'] == status_filter]
    
    # Display table
    st.markdown(f"### All Vehicles ({len(filtered_df)} shown)")
    st.dataframe(
        filtered_df[[
            'Vehicle ID', 'Model', 'Status', 'Driver', 
            'FE (km/L)', 'Odometer (km)', 'Daily Distance (km)'
        ]],
        use_container_width=True,
        height=400
    )
    
    st.markdown("---")
    
    # Vehicle Drill-Down
    st.markdown("### 🔍 Vehicle Deep Dive")
    selected_vehicle = st.selectbox(
        "Select a vehicle for detailed analysis:",
        filtered_df['Vehicle ID'].tolist(),
        index=0
    )
    
    if selected_vehicle:
        vehicle_data = df_vehicles[df_vehicles['Vehicle ID'] == selected_vehicle].iloc[0]
        
        st.markdown(f"## **{selected_vehicle}** - Detailed Analysis")
        
        # Vehicle KPIs
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Model", vehicle_data['Model'])
        with col2:
            st.metric("Status", vehicle_data['Status'])
        with col3:
            st.metric("Driver", vehicle_data['Driver'])
        with col4:
            st.metric("Region", vehicle_data['Region'])
        with col5:
            st.metric("FE", f"{vehicle_data['FE (km/L)']} km/L")
        
        st.markdown("---")
        
        # Tabbed Deep Dive
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Performance", "⛽ Fuel & Efficiency", "🔧 Maintenance", 
            "💰 Cost Analysis", "🌱 Environmental"
        ])
        
        with tab1:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Odometer", f"{vehicle_data['Odometer (km)']:,} km")
            with col2:
                st.metric("Daily Average", f"{vehicle_data['Daily Distance (km)']} km")
            with col3:
                st.metric("Avg Speed", f"{vehicle_data['Speed Avg (km/h)']} km/h")
            
            st.markdown("#### 7-Day Performance Trend")
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            perf_data = [round(random.uniform(3.8, 4.8), 2) for _ in range(7)]
            fig = px.line(x=days, y=perf_data, markers=True, template='plotly_white')
            fig.update_traces(line_color='#667eea')
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Fuel Efficiency", f"{vehicle_data['FE (km/L)']} km/L")
                st.metric("Idle Time/Day", f"{vehicle_data['Idle Time (min)']} min")
            with col2:
                st.metric("Operating Cost/KM", f"₹{vehicle_data['Operating Cost/KM (₹)']}")
                st.metric("Daily CO2", f"{vehicle_data['Daily CO2 (kg)']} kg")
            
            st.markdown("#### Fuel Consumption Breakdown")
            fig = go.Figure(data=[go.Pie(
                labels=['Highway', 'City', 'Idle', 'Others'],
                values=[45, 30, vehicle_data['Idle Time (min)']/10, 10]
            )])
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Last Service", f"{vehicle_data['Last Service (days ago)']} days ago")
            with col2:
                next_service = vehicle_data['Next Service (days)']
                delta_color = "normal" if next_service > 15 else "inverse"
                st.metric("Next Service", f"In {next_service} days", delta_color=delta_color)
            with col3:
                st.metric("Maintenance CPKM", f"₹{vehicle_data['Maintenance CPKM (₹)']}")
            
            st.markdown("#### Maintenance Cost History")
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            costs = [round(random.uniform(15000, 35000), 0) for _ in range(6)]
            fig = px.bar(x=months, y=costs, template='plotly_white')
            fig.update_traces(marker_color='#f59e0b')
            st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            st.metric("Total Maintenance Cost", f"₹{vehicle_data['Maintenance Cost Total (₹)']:,}")
            st.metric("Maintenance CPKM", f"₹{vehicle_data['Maintenance CPKM (₹)']}")
            st.metric("Operating CPKM", f"₹{vehicle_data['Operating Cost/KM (₹)']}")
            
            st.markdown("#### Cost Breakdown")
            fig = go.Figure(data=[go.Pie(
                labels=['Fuel', 'Maintenance', 'Driver', 'Others'],
                values=[63, 20, 12, 5]
            )])
            st.plotly_chart(fig, use_container_width=True)
        
        with tab5:
            st.metric("Daily CO2 Emissions", f"{vehicle_data['Daily CO2 (kg)']} kg")
            st.metric("Monthly CO2", f"{vehicle_data['Daily CO2 (kg)'] * 30:.0f} kg")
            
            st.markdown("#### CO2 Trend (Last 6 Months)")
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            co2_data = [round(vehicle_data['Daily CO2 (kg)'] * 30 + random.uniform(-50, 50), 1) for _ in range(6)]
            fig = px.line(x=months, y=co2_data, markers=True, template='plotly_white')
            fig.update_traces(line_color='#10b981', fill='tozeroy')
            st.plotly_chart(fig, use_container_width=True)

# DRIVER PERFORMANCE
elif page == "👤 Driver Performance":
    st.title("👤 Driver Performance & Analysis")
    
    # Driver Summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Drivers", len(df_drivers))
    with col2:
        st.metric("Avg Efficiency", f"{df_drivers['Efficiency (km/L)'].mean():.2f} km/L")
    with col3:
        trained = df_drivers['Training Complete'].sum()
        st.metric("Training Complete", f"{trained}/{len(df_drivers)}")
    with col4:
        st.metric("Avg Score", f"{df_drivers['Score'].mean():.0f}/100")
    
    st.markdown("---")
    
    # Driver Table
    st.markdown("### All Drivers")
    st.dataframe(
        df_drivers[[
            'Name', 'Score', 'Efficiency (km/L)', 'Total Trips', 
            'Violations', 'Experience (years)'
        ]].sort_values('Score', ascending=False),
        use_container_width=True,
        height=400
    )
    
    st.markdown("---")
    
    # Driver Drill-Down
    st.markdown("### 🔍 Driver Deep Dive")
    selected_driver = st.selectbox(
        "Select a driver for detailed analysis:",
        df_drivers['Name'].tolist(),
        index=0
    )
    
    if selected_driver:
        driver_data = df_drivers[df_drivers['Name'] == selected_driver].iloc[0]
        
        st.markdown(f"## **{selected_driver}** - Detailed Analysis")
        
        # Driver KPIs
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Performance Score", f"{driver_data['Score']}/100")
        with col2:
            st.metric("Efficiency", f"{driver_data['Efficiency (km/L)']} km/L")
        with col3:
            st.metric("Total Trips", driver_data['Total Trips'])
        with col4:
            st.metric("Experience", f"{driver_data['Experience (years)']} years")
        with col5:
            training_status = "✅ Complete" if driver_data['Training Complete'] else "⏳ Pending"
            st.metric("Training", training_status)
        
        st.markdown("---")
        
        # Tabbed Deep Dive
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Performance", "🚗 Behavior Analysis", "📚 Training", "💰 Financial"
        ])
        
        with tab1:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Distance", f"{driver_data['Total Distance (km)']:,} km")
            with col2:
                st.metric("Avg Distance/Trip", f"{driver_data['Avg Distance/Trip (km)']} km")
            with col3:
                st.metric("Violations", driver_data['Violations'])
            
            st.markdown("#### Monthly Performance Trend")
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            scores = [round(driver_data['Score'] + random.uniform(-5, 5), 1) for _ in range(6)]
            fig = px.line(x=months, y=scores, markers=True, template='plotly_white')
            fig.update_traces(line_color='#667eea')
            fig.update_layout(yaxis_range=[0, 100])
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Harsh Braking", driver_data['Harsh Braking'])
                st.metric("Harsh Acceleration", driver_data['Harsh Acceleration'])
            with col2:
                st.metric("Speeding Events", driver_data['Speeding Events'])
                st.metric("Fatigue Alerts", driver_data['Fatigue Alerts'])
            
            st.markdown("#### Behavior Score Breakdown")
            categories = ['Speed Control', 'Smooth Driving', 'Route Adherence', 'Safety', 'Fuel Economy']
            scores = [round(random.uniform(70, 95), 1) for _ in range(5)]
            fig = go.Figure(data=go.Scatterpolar(
                r=scores,
                theta=categories,
                fill='toself'
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            training_status = "Completed" if driver_data['Training Complete'] else "In Progress"
            st.metric("Training Status", training_status)
            
            modules = ['Eco Driving', 'Safety Protocol', 'Route Planning', 'Vehicle Care', 'Regulations']
            completion = [100 if driver_data['Training Complete'] else random.randint(40, 90) for _ in range(5)]
            
            fig = px.bar(x=completion, y=modules, orientation='h', template='plotly_white')
            fig.update_traces(marker_color='#10b981')
            fig.update_layout(xaxis_range=[0, 100])
            st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            st.metric("Monthly Salary", f"₹{driver_data['Monthly Salary (₹)']:,}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Cost per Trip", f"₹{driver_data['Monthly Salary (₹)'] / driver_data['Total Trips']:.0f}")
            with col2:
                st.metric("Cost per KM", f"₹{driver_data['Monthly Salary (₹)'] / driver_data['Total Distance (km)']:.2f}")

# CO2 ANALYTICS
elif page == "🌱 CO2 Analytics":
    st.title("🌱 CO2 & Environmental Analytics")
    
    total_co2 = df_vehicles['Daily CO2 (kg)'].sum()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Daily Emissions", f"{total_co2:.0f} kg", "↓ 15.3%", delta_color="inverse")
    with col2:
        st.metric("Monthly Emissions", f"{total_co2*30/1000:.1f} tonnes")
    with col3:
        st.metric("Target Progress", "76.5%", "↑ 8.2%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Emission Trends (6 Months)")
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        emissions = [3200, 3100, 3050, 2980, 2950, 2940]
        fig = px.area(x=months, y=emissions, template='plotly_white')
        fig.update_traces(line_color='#10b981', fillcolor='rgba(16, 185, 129, 0.3)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### CO2 Source Breakdown")
        fig = go.Figure(data=[go.Pie(
            labels=['Fuel Burn', 'Idle Time', 'Route Inefficiency', 'Load Factor'],
            values=[65, 18, 12, 5],
            marker=dict(colors=['#667eea', '#f59e0b', '#ef4444', '#10b981'])
        )])
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Top 15 CO2 Emitters")
    top_emitters = df_vehicles.nlargest(15, 'Daily CO2 (kg)')
    fig = px.bar(top_emitters, x='Daily CO2 (kg)', y='Vehicle ID', orientation='h', template='plotly_white')
    fig.update_traces(marker_color='#ef4444')
    st.plotly_chart(fig, use_container_width=True)

# MAINTENANCE & CPKM
elif page == "🔧 Maintenance & CPKM":
    st.title("🔧 Maintenance Management & Cost Per Kilometer")
    
    # Overall Maintenance CPKM
    total_maint_cost = df_vehicles['Maintenance Cost Total (₹)'].sum()
    total_odo = df_vehicles['Odometer (km)'].sum()
    overall_cpkm = total_maint_cost / total_odo
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Maintenance CPKM", f"₹{overall_cpkm:.2f}")
    with col2:
        total_cost_lakhs = total_maint_cost / 100000
st.metric("Total Maintenance Cost", f"₹{total_cost_lakhs:.2f}L")
    with col3:
        due_7days = len(df_vehicles[(df_vehicles['Next Service (days)'] >= 0) & (df_vehicles['Next Service (days)'] <= 7)])
        st.metric("Due in 7 Days", due_7days)
    with col4:
        due_15days = len(df_vehicles[(df_vehicles['Next Service (days)'] > 7) & (df_vehicles['Next Service (days)'] <= 15)])
        st.metric("Due in 15 Days", due_15days)
    
    st.markdown("---")
    
    # CPKM Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Maintenance CPKM Distribution")
        fig = px.histogram(df_vehicles, x='Maintenance CPKM (₹)', nbins=25, template='plotly_white')
        fig.update_traces(marker_color='#f59e0b')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Top 10 Highest CPKM Vehicles")
        top_cpkm = df_vehicles.nlargest(10, 'Maintenance CPKM (₹)')
        fig = px.bar(top_cpkm, x='Maintenance CPKM (₹)', y='Vehicle ID', orientation='h', template='plotly_white')
        fig.update_traces(marker_color='#ef4444')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed Maintenance Table
    st.markdown("### Vehicle-wise Maintenance Details")
    maintenance_df = df_vehicles[[
        'Vehicle ID', 'Model', 'Odometer (km)', 'Maintenance Cost Total (₹)', 
        'Maintenance CPKM (₹)', 'Last Service (days ago)', 'Next Service (days)'
    ]].sort_values('Maintenance CPKM (₹)', ascending=False)
    
    st.dataframe(maintenance_df, use_container_width=True, height=400)
    
    st.markdown("---")
    
    # Monthly Cost Trends
    st.markdown("### Monthly Maintenance Cost Trends")
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    costs = [1.8, 2.1, 1.9, 2.3, 2.0, 2.3]
    fig = px.line(x=months, y=costs, markers=True, template='plotly_white')
    fig.update_traces(line_color='#f59e0b', fill='tozeroy', fillcolor='rgba(245, 158, 11, 0.2)')
    st.plotly_chart(fig, use_container_width=True)

# COST ANALYSIS
elif page == "💰 Cost Analysis":
    st.title("💰 Cost Analysis & Financial Insights")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Operating Cost", "₹45.2L")
    with col2:
        st.metric("Avg Cost per KM", "₹32.4")
    with col3:
        st.metric("Fuel Cost (63%)", "₹28.5L")
    with col4:
        st.metric("Maintenance Cost", f"₹{total_maint_cost/100000:.2f}L")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Cost Breakdown")
        fig = go.Figure(data=[go.Pie(
            labels=['Fuel', 'Maintenance', 'Driver Salary', 'Insurance', 'Others'],
            values=[63, 15, 12, 6, 4],
            marker=dict(colors=['#667eea', '#f59e0b', '#10b981', '#3b82f6', '#ef4444'])
        )])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Monthly Cost Trends")
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        costs = [42.5, 44.2, 43.8, 46.1, 44.8, 45.2]
        fig = px.line(x=months, y=costs, markers=True, template='plotly_white')
        fig.update_traces(line_color='#667eea', fill='tozeroy')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Vehicle-wise Cost Analysis")
    cost_df = df_vehicles[[
        'Vehicle ID', 'Operating Cost/KM (₹)', 'Maintenance CPKM (₹)', 
        'Odometer (km)', 'Maintenance Cost Total (₹)'
    ]].copy()
    cost_df['Total Cost (₹)'] = cost_df['Operating Cost/KM (₹)'] * cost_df['Odometer (km)']
    st.dataframe(cost_df.sort_values('Total Cost (₹)', ascending=False), use_container_width=True, height=400)

# COMPLIANCE
elif page == "✅ Compliance":
    st.title("✅ Compliance & Regulatory Status")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Compliance Score", "96%", "↑ 2%")
    with col2:
        bs6_compliant = random.randint(140, 148)
        st.metric("BS-VI Compliant", f"{bs6_compliant}/150")
    with col3:
        st.metric("Expiring Soon (30d)", "6 documents")
    
    st.markdown("---")
    
    st.markdown("### Compliance Status by Category")
    compliance_df = pd.DataFrame({
        'Category': ['Registration', 'Insurance', 'Permits', 'Fitness', 'Pollution', 'License'],
        'Compliance (%)': [98, 96, 94, 95, 97, 99]
    })
    fig = px.bar(compliance_df, x='Category', y='Compliance (%)', template='plotly_white')
    fig.update_traces(marker_color='#10b981')
    fig.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b; padding: 2rem;'>"
    "<strong>Fleet Managers Dashboard</strong> • Indian Heavy Commercial Vehicles • Built with Streamlit 🚛"
    "</div>",
    unsafe_allow_html=True
)
