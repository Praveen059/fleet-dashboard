import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
from datetime import datetime, timedelta

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Fleet Managers Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🚛"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Main container */
    .main {padding: 1rem 2rem !important;}
    
    /* KPI cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        border: 1px solid #e2e8f0;
    }
    
    /* Headers */
    h1 {color: #667eea; font-size: 2.2rem !important; font-weight: 700 !important;}
    h2 {color: #1e293b; font-size: 1.8rem !important; margin-top: 1.5rem !important;}
    h3 {color: #475569; font-size: 1.3rem !important;}
    
    /* Tables */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        border: none;
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
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATA GENERATION ====================
@st.cache_data
def generate_vehicles(n=150):
    """Generate 150 vehicles with realistic data"""
    models = ['Heavy Truck 45T', 'Heavy Truck 40T', 'Heavy Truck 35T', 'Medium Truck 25T', 
              'Medium Truck 20T', 'Medium Truck 16T', 'Light Truck 12T', 'Light Truck 10T', 
              'Multi-Axle 49T', 'Multi-Axle 55T', 'Tipper 31T']
    states = ['MH', 'DL', 'GJ', 'KA', 'TN', 'UP', 'RJ', 'HR', 'PB', 'WB']
    statuses = ['Active', 'Idle', 'Maintenance']
    drivers_list = [f"Driver {chr(65 + i//10)}{i%10}" for i in range(1, 151)]
    
    vehicles = []
    for i in range(1, n + 1):
        state = random.choice(states)
        dist = str(random.randint(1, 50)).zfill(2)
        series = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))
        num = str(random.randint(1000, 9999))
        
        odo = random.randint(50000, 500000)
        maint_cost = random.randint(40000, 250000)
        
        vehicles.append({
            'Vehicle ID': f"{state}-{dist}-TRK-{num}",
            'Model': random.choice(models),
            'Status': random.choice(statuses),
            'Driver': drivers_list[i-1] if i <= len(drivers_list) else random.choice(drivers_list),
            'FE (km/L)': round(random.uniform(3.2, 5.2), 2),
            'Odometer (km)': odo,
            'Daily Distance (km)': random.randint(200, 600),
            'Cost per KM (₹)': round(random.uniform(25, 45), 2),
            'Maintenance Cost (₹)': maint_cost,
            'Maintenance CPKM (₹)': round(maint_cost / odo, 2),
            'Daily CO2 (kg)': round(random.uniform(15, 30), 1),
            'Idle Time (min)': random.randint(20, 180),
            'Last Service (days)': random.randint(5, 90),
            'Next Service (days)': random.randint(-10, 60),
            'KM Since Service': random.randint(1000, 15000)
        })
    
    return pd.DataFrame(vehicles)

@st.cache_data
def generate_drivers(n=145):
    """Generate 145 drivers with realistic data"""
    drivers = []
    for i in range(1, n + 1):
        letter = chr(65 + (i-1) // 10)
        num = (i % 10) if (i % 10) != 0 else 10
        trips = random.randint(50, 150)
        
        drivers.append({
            'Name': f"Driver {letter}{num}",
            'Score': random.randint(70, 100),
            'Efficiency (km/L)': round(random.uniform(3.5, 5.0), 2),
            'Total Trips': trips,
            'Violations': random.randint(0, 5),
            'Experience (years)': random.randint(2, 15),
            'Training Complete': random.random() > 0.13
        })
    
    return pd.DataFrame(drivers)

# Load data
df_vehicles = generate_vehicles()
df_drivers = generate_drivers()

# ==================== SIDEBAR NAVIGATION ====================
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:20px 10px;border-bottom:2px solid rgba(255,255,255,0.1);margin-bottom:20px;'>
        <h1 style='color:#667eea;font-size:1.5rem;margin:0;'>🚛 Fleet Dashboard</h1>
        <p style='color:#94a3b8;font-size:0.9rem;margin-top:5px;'>Indian Heavy Commercial Vehicles</p>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation",
        [
            "🏠 Fleet Overview",
            "🚛 Vehicle Analysis",
            "👤 Driver Performance",
            "🌱 CO2 Analytics",
            "📚 Micro Training",
            "💡 FE Opportunities",
            "🔬 Advanced Analytics",
            "🔧 Maintenance",
            "💰 Cost Analysis",
            "✅ Compliance"
        ],
        label_visibility="collapsed"
    )

# ==================== FLEET OVERVIEW ====================
if page == "🏠 Fleet Overview":
    st.title("Fleet Overview")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Fleet Average", "4.1 km/L", "↑ 7.2%")
    with col2:
        st.metric("Weekly Fuel Cost", "₹1.68L", "↓ ₹17.4K")
    with col3:
        active = len(df_vehicles[df_vehicles['Status'] == 'Active'])
        st.metric("Active Vehicles", f"{active}/150")
    with col4:
        total_co2 = df_vehicles['Daily CO2 (kg)'].sum()
        st.metric("Daily CO2", f"{total_co2:.0f} kg", "↓ 15.3%")
    
    # Performance Trends
    st.subheader("📈 Fleet Performance Trends")
    view = st.radio("Time Period", ["Daily", "Weekly", "Monthly"], horizontal=True)
    
    if view == "Daily":
        fig = px.line(x=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                     y=[4.1, 4.3, 4.2, 4.4, 4.5, 4.3, 4.4],
                     labels={'x': 'Day', 'y': 'Efficiency (km/L)'})
    elif view == "Weekly":
        fig = px.line(x=['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                     y=[4.2, 4.3, 4.1, 4.4])
    else:
        fig = px.line(x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                     y=[4.0, 4.1, 4.2, 4.1, 4.3, 4.4])
    
    fig.update_traces(line_color='#667eea', fill='tozeroy', fillcolor='rgba(102, 126, 234, 0.1)')
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)
    
    # Priority Alerts
    st.subheader("🚨 Priority Alerts")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.error("**⚠️ Critical Alert**\nMH-12-TRK-052 - Extended idle: 285 min\nFuel waste: 18.4L")
    with col2:
        st.warning("**🔧 Maintenance Due**\nGJ-01-TRK-031 - Brake service overdue\nOverdue by: 1,200km")
    with col3:
        st.success("**📈 Top Performer**\nDriver A1 - Excellent efficiency\nImprovement: 22% this month")

# ==================== VEHICLE ANALYSIS ====================
elif page == "🚛 Vehicle Analysis":
    st.title("Vehicle Analysis")
    
    # Sub-tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 All Vehicles (150)",
        "⭐ Top Performers",
        "⚠️ Needs Attention",
        "🔧 Maintenance Due",
        "📊 Efficiency Analysis"
    ])
    
    with tab1:
        st.subheader("All Vehicles")
        search = st.text_input("🔍 Search vehicles...", key="vehicle_search")
        
        filtered = df_vehicles.copy()
        if search:
            filtered = filtered[filtered['Vehicle ID'].str.contains(search, case=False)]
        
        st.dataframe(filtered[['Vehicle ID', 'Model', 'Status', 'Driver', 'FE (km/L)', 
                               'Odometer (km)', 'Daily Distance (km)']],
                    use_container_width=True, height=400)
        
        # Vehicle drill-down
        st.markdown("### 🔍 Select Vehicle for Details")
        selected_vehicle = st.selectbox("Vehicle ID", filtered['Vehicle ID'].tolist(), key="veh_detail")
        
        if selected_vehicle:
            v = df_vehicles[df_vehicles['Vehicle ID'] == selected_vehicle].iloc[0]
            
            with st.expander(f"**{selected_vehicle}** - Detailed Analysis", expanded=True):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("FE", f"{v['FE (km/L)']} km/L")
                with col2:
                    st.metric("Odometer", f"{v['Odometer (km)']:,} km")
                with col3:
                    st.metric("Daily Avg", f"{v['Daily Distance (km)']} km")
                with col4:
                    st.metric("CO2/Day", f"{v['Daily CO2 (kg)']} kg")
                
                # 7-day performance
                days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                perf = [round(random.uniform(3.8, 4.8), 2) for _ in range(7)]
                fig = px.line(x=days, y=perf, markers=True, title="7-Day Performance")
                fig.update_traces(line_color='#667eea')
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Top 20 Performing Vehicles")
        top20 = df_vehicles.nlargest(20, 'FE (km/L)')
        fig = px.bar(top20, x='FE (km/L)', y='Vehicle ID', orientation='h',
                    color='FE (km/L)', color_continuous_scale='Greens')
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Vehicles Requiring Attention")
        attention = df_vehicles[
            (df_vehicles['Status'] == 'Maintenance') | 
            (df_vehicles['FE (km/L)'] < 3.5) |
            (df_vehicles['Idle Time (min)'] > 150)
        ]
        st.dataframe(attention, use_container_width=True)
        st.warning(f"⚠️ {len(attention)} vehicles need attention")
    
    with tab4:
        st.subheader("Maintenance Schedule (Next 30 Days)")
        maint = df_vehicles[(df_vehicles['Next Service (days)'] >= 0) & 
                           (df_vehicles['Next Service (days)'] <= 30)]
        maint = maint.sort_values('Next Service (days)')
        st.dataframe(maint[['Vehicle ID', 'Model', 'Next Service (days)', 'KM Since Service']],
                    use_container_width=True)
    
    with tab5:
        st.subheader("Efficiency Distribution")
        fig = px.histogram(df_vehicles, x='FE (km/L)', nbins=25,
                          color_discrete_sequence=['#667eea'])
        st.plotly_chart(fig, use_container_width=True)

# ==================== DRIVER PERFORMANCE ====================
elif page == "👤 Driver Performance":
    st.title("Driver Performance")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview",
        "🏆 Top Performers",
        "📈 Trends",
        "📚 Training Status"
    ])
    
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Drivers", "145")
        with col2:
            avg_eff = df_drivers['Efficiency (km/L)'].mean()
            st.metric("Avg Efficiency", f"{avg_eff:.2f} km/L")
        with col3:
            trained = len(df_drivers[df_drivers['Training Complete'] == True])
            st.metric("Training Complete", f"{trained}/145")
        with col4:
            avg_score = df_drivers['Score'].mean()
            st.metric("Avg Score", f"{avg_score:.0f}/100")
        
        st.subheader("All Drivers")
        st.dataframe(df_drivers.sort_values('Score', ascending=False),
                    use_container_width=True, height=400)
        
        # Driver drill-down
        st.markdown("### 🔍 Select Driver for Details")
        selected_driver = st.selectbox("Driver Name", df_drivers['Name'].tolist())
        
        if selected_driver:
            d = df_drivers[df_drivers['Name'] == selected_driver].iloc[0]
            
            with st.expander(f"**{selected_driver}** - Detailed Analysis", expanded=True):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Score", d["Score"])
                with col2:
                    st.metric("Efficiency", f"{d['Efficiency (km/L)']} km/L")
                with col3:
                    st.metric("Total Trips", d["Total Trips"])
                with col4:
                    st.metric("Violations", d["Violations"])
                
                # Performance history
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
                scores = [round(d['Score'] + random.uniform(-5, 5), 1) for _ in range(6)]
                fig = px.line(x=months, y=scores, markers=True, title="Performance History")
                fig.update_traces(line_color='#667eea')
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Top 20 Drivers by Efficiency")
        top20 = df_drivers.nlargest(20, 'Efficiency (km/L)')
        fig = px.bar(top20, x='Efficiency (km/L)', y='Name', orientation='h',
                    color='Score', color_continuous_scale='Viridis')
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Performance Trends")
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        avg_scores = [82, 84, 83, 86, 88, 89]
        fig = px.line(x=months, y=avg_scores, markers=True)
        fig.update_traces(line_color='#10b981')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Training Status")
        trained_count = len(df_drivers[df_drivers['Training Complete'] == True])
        in_progress = 19
        not_started = 145 - trained_count - in_progress
        
        fig = go.Figure(data=[go.Pie(
            labels=['Completed', 'In Progress', 'Not Started'],
            values=[trained_count, in_progress, not_started],
            marker=dict(colors=['#10b981', '#f59e0b', '#ef4444'])
        )])
        st.plotly_chart(fig, use_container_width=True)

# ==================== CO2 ANALYTICS ====================
elif page == "🌱 CO2 Analytics":
    st.title("CO2 & Environmental Analytics")
    
    total_co2 = df_vehicles['Daily CO2 (kg)'].sum()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Daily Emissions", f"{total_co2:.0f} kg", "↓ 15.3%")
    with col2:
        st.metric("Monthly Emissions", f"{total_co2*30/1000:.1f} tonnes")
    with col3:
        st.metric("Target Progress", "76.5%", "↑ 8.2%")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Emission Trends (6 Months)")
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        emissions = [3200, 3100, 3050, 2980, 2950, 2940]
        fig = px.area(x=months, y=emissions)
        fig.update_traces(line_color='#10b981', fillcolor='rgba(16, 185, 129, 0.3)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("CO2 Source Breakdown")
        fig = go.Figure(data=[go.Pie(
            labels=['Fuel Burn', 'Idle Time', 'Route Inefficiency', 'Load Factor'],
            values=[65, 18, 12, 5],
            marker=dict(colors=['#667eea', '#f59e0b', '#ef4444', '#10b981'])
        )])
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Top 15 CO2 Emitters")
    top_emitters = df_vehicles.nlargest(15, 'Daily CO2 (kg)')
    fig = px.bar(top_emitters, x='Daily CO2 (kg)', y='Vehicle ID', orientation='h')
    fig.update_traces(marker_color='#ef4444')
    st.plotly_chart(fig, use_container_width=True)

# ==================== MICRO TRAINING ====================
elif page == "📚 Micro Training":
    st.title("Micro Training & Development")
    
    col1, col2, col3 = st.columns(3)
    trained_count = len(df_drivers[df_drivers['Training Complete'] == True])
    with col1:
        st.metric("Available Modules", "24")
    with col2:
        st.metric("Completion Rate", f"{trained_count/145*100:.0f}%")
    with col3:
        st.metric("Avg Module Rating", "4.6/5")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Training Status")
        fig = go.Figure(data=[go.Pie(
            labels=['Completed', 'In Progress', 'Not Started'],
            values=[trained_count, 19, 145-trained_count-19],
            marker=dict(colors=['#10b981', '#f59e0b', '#ef4444'])
        )])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Module Effectiveness")
        modules = ['Eco Driving', 'Safety', 'Route Planning', 'Vehicle Care', 'Regulations']
        ratings = [4.8, 4.6, 4.5, 4.7, 4.4]
        fig = px.bar(x=modules, y=ratings, color=ratings, color_continuous_scale='Greens')
        fig.update_layout(yaxis_range=[0, 5])
        st.plotly_chart(fig, use_container_width=True)

# ==================== FE OPPORTUNITIES ====================
elif page == "💡 FE Opportunities":
    st.title("Fuel Efficiency Opportunities")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Monthly Opportunity", "₹2.4L")
    with col2:
        st.metric("Captured (75%)", "₹1.8L", "↑ 12%")
    with col3:
        st.metric("Lost Opportunity", "₹0.6L")
    
    st.subheader("Opportunity Breakdown")
    categories = ['Idle Reduction', 'Speed Optimization', 'Route Efficiency', 'Load Planning']
    captured = [45000, 38000, 42000, 35000]
    lost = [15000, 12000, 10000, 8000]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Captured', x=categories, y=captured, marker_color='#10b981'))
    fig.add_trace(go.Bar(name='Lost', x=categories, y=lost, marker_color='#ef4444'))
    fig.update_layout(barmode='stack', height=400)
    st.plotly_chart(fig, use_container_width=True)

# ==================== ADVANCED ANALYTICS ====================
elif page == "🔬 Advanced Analytics":
    st.title("Advanced Analytics & AI Insights")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Predicted Failures", "12", "next 30 days")
    with col2:
        st.metric("Prevention Success", "94%")
    with col3:
        st.metric("Cost Saved", "₹8.4L", "YTD")
    
    st.subheader("Fuel Efficiency Forecast (Next 4 Weeks)")
    weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
    predicted = [4.3, 4.4, 4.5, 4.6]
    actual = [4.3, 4.4, None, None]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=weeks, y=predicted, name='Predicted',
                            line=dict(dash='dash', color='#667eea')))
    fig.add_trace(go.Scatter(x=weeks[:2], y=actual[:2], name='Actual',
                            line=dict(color='#10b981')))
    st.plotly_chart(fig, use_container_width=True)

# ==================== MAINTENANCE ====================
elif page == "🔧 Maintenance":
    st.title("Maintenance Management & CPKM")
    
    total_maint_cost = df_vehicles['Maintenance Cost (₹)'].sum()
    total_odo = df_vehicles['Odometer (km)'].sum()
    overall_cpkm = total_maint_cost / total_odo
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Maint CPKM", f"₹{overall_cpkm:.2f}")
    with col2:
        st.metric("Total Maint Cost", f"₹{total_maint_cost/100000:.2f}L")
    with col3:
        due_7 = len(df_vehicles[(df_vehicles['Next Service (days)'] >= 0) & 
                                (df_vehicles['Next Service (days)'] <= 7)])
        st.metric("Due in 7 Days", due_7)
    with col4:
        due_15 = len(df_vehicles[(df_vehicles['Next Service (days)'] > 7) & 
                                 (df_vehicles['Next Service (days)'] <= 15)])
        st.metric("Due in 15 Days", due_15)
    
    st.subheader("Maintenance CPKM Distribution")
    fig = px.histogram(df_vehicles, x='Maintenance CPKM (₹)', nbins=25)
    fig.update_traces(marker_color='#f59e0b')
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Vehicle-wise Maintenance Details")
    maint_df = df_vehicles[['Vehicle ID', 'Model', 'Odometer (km)', 'Maintenance Cost (₹)', 
                            'Maintenance CPKM (₹)']].sort_values('Maintenance CPKM (₹)', ascending=False)
    st.dataframe(maint_df, use_container_width=True, height=400)

# ==================== COST ANALYSIS ====================
elif page == "💰 Cost Analysis":
    st.title("Cost Analysis & Financial Insights")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Operating Cost", "₹45.2L")
    with col2:
        st.metric("Avg Cost per KM", "₹32.4")
    with col3:
        st.metric("Fuel Cost (63%)", "₹28.5L")
    with col4:
        st.metric("Maintenance Cost", f"₹{total_maint_cost/100000:.2f}L")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cost Breakdown")
        fig = go.Figure(data=[go.Pie(
            labels=['Fuel', 'Maintenance', 'Driver Salary', 'Insurance', 'Others'],
            values=[63, 15, 12, 6, 4],
            marker=dict(colors=['#667eea', '#f59e0b', '#10b981', '#3b82f6', '#ef4444'])
        )])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Monthly Cost Trends")
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        costs = [42.5, 44.2, 43.8, 46.1, 44.8, 45.2]
        fig = px.line(x=months, y=costs, markers=True)
        fig.update_traces(line_color='#667eea', fill='tozeroy')
        st.plotly_chart(fig, use_container_width=True)

# ==================== COMPLIANCE ====================
elif page == "✅ Compliance":
    st.title("Compliance & Regulatory Status")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Compliance Score", "96%", "↑ 2%")
    with col2:
        bs6_compliant = random.randint(140, 148)
        st.metric("BS-VI Compliant", f"{bs6_compliant}/150")
    with col3:
        st.metric("Expiring Soon (30d)", "6 documents")
    
    st.subheader("Compliance Status by Category")
    categories = ['Registration', 'Insurance', 'Permits', 'Fitness', 'Pollution', 'License']
    compliance = [98, 96, 94, 95, 97, 99]
    fig = px.bar(x=categories, y=compliance, color=compliance, color_continuous_scale='Greens')
    fig.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#888;font-size:0.9rem;padding:1rem;'>"
    "Fleet Managers Dashboard · Indian Heavy Commercial Vehicles · Powered by Streamlit 🚛"
    "</div>",
    unsafe_allow_html=True
)
