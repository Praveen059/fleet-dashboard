import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="Fleet Managers Dashboard", layout="wide", page_icon="🚛")

# Custom CSS for better styling
st.markdown("""
<style>
    .main {padding: 0rem 1rem;}
    h1 {color: #667eea; font-size: 2.5rem;}
    h2 {color: #667eea; font-size: 2rem;}
    h3 {color: #667eea; font-size: 1.5rem;}
    .stMetric {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
               padding: 1rem; border-radius: 0.5rem; color: white;}
    .stMetric label {color: white !important;}
    .stMetric div {color: white !important;}
</style>
""", unsafe_allow_html=True)

# Generate Data Functions
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
        
        vehicles.append({
            'Vehicle ID': f"{state}-{dist}-TRK-{num}",
            'Model': random.choice(models),
            'Status': random.choice(statuses),
            'Region': random.choice(regions),
            'Driver': f"Driver {chr(65 + i//10)}{i%10}",
            'FE (km/L)': round(random.uniform(3.2, 5.2), 2),
            'Odometer': random.randint(50000, 550000),
            'Daily Distance': random.randint(200, 600),
            'Cost/KM': round(random.uniform(25, 45), 2),
            'Daily CO2 (kg)': round(random.uniform(15, 30), 1),
            'Idle Time (min)': random.randint(20, 180),
            'Speed Avg (km/h)': random.randint(45, 75)
        })
    
    return pd.DataFrame(vehicles)

@st.cache_data
def generate_drivers(count=145):
    drivers = []
    for i in range(1, count + 1):
        drivers.append({
            'Name': f"Driver {chr(65 + i//10)}{i%10}",
            'Score': random.randint(70, 100),
            'Efficiency': round(random.uniform(3.5, 5.0), 2),
            'Trips': random.randint(50, 150),
            'Violations': random.randint(0, 5),
            'Experience': random.randint(2, 15),
            'Training': random.random() > 0.13
        })
    
    return pd.DataFrame(drivers)

# Load data
df_vehicles = generate_vehicles(150)
df_drivers = generate_drivers(145)

# Sidebar
with st.sidebar:
    st.title("🚛 Fleet Dashboard")
    st.markdown("**Indian Heavy Commercial Vehicles**")
    st.markdown("---")
    
    page = st.radio("Navigation", [
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
    ])

# FLEET OVERVIEW
if page == "🏠 Fleet Overview":
    st.title("Fleet Overview Dashboard")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Fleet Efficiency", "4.1 km/L", "↑ 7.2%")
    with col2:
        st.metric("Weekly Fuel Cost", "₹1.68L", "↓ ₹17.4K")
    with col3:
        active = len(df_vehicles[df_vehicles['Status'] == 'Active'])
        st.metric("Active Vehicles", f"{active}/150", f"{150-active} inactive")
    with col4:
        total_co2 = df_vehicles['Daily CO2 (kg)'].sum()
        st.metric("Daily CO2", f"{total_co2:.0f} kg", "↓ 15.3%")
    
    # Multi-view Performance Chart
    st.markdown("### 📈 Fleet Performance Trends")
    view = st.radio("View", ["Daily", "Weekly", "Monthly"], horizontal=True)
    
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
    
    fig.update_traces(line_color='#667eea', fill='tozeroy')
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)
    
    # Region-wise Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🗺️ Region-wise Fleet Distribution")
        region_counts = df_vehicles['Region'].value_counts()
        fig_region = px.pie(values=region_counts.values, names=region_counts.index,
                           color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_region, use_container_width=True)
    
    with col2:
        st.markdown("### 🚛 Model-wise Performance")
        model_perf = df_vehicles.groupby('Model')['FE (km/L)'].mean().sort_values(ascending=False)
        fig_model = px.bar(x=model_perf.values, y=model_perf.index, orientation='h',
                          color=model_perf.values, color_continuous_scale='Viridis')
        fig_model.update_layout(showlegend=False)
        st.plotly_chart(fig_model, use_container_width=True)
    
    # Fuel Consumption Breakdown
    st.markdown("### ⛽ Fuel Consumption Breakdown")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        consumption_data = pd.DataFrame({
            'Category': ['Highway', 'City', 'Idle', 'Others'],
            'Consumption (%)': [45, 30, 18, 7]
        })
        fig_fuel = px.bar(consumption_data, x='Category', y='Consumption (%)',
                         color='Consumption (%)', color_continuous_scale='Reds')
        st.plotly_chart(fig_fuel, use_container_width=True)
    
    with col2:
        st.metric("Avg Idle Time", "87 min/day", "↓ 12 min")
        st.metric("Fuel Wasted (Idle)", "145 L/day", "↓ 18 L")
        st.metric("Cost Impact", "₹18,200/day", "↓ ₹2,400")
    
    # Efficiency vs Distance Scatter
    st.markdown("### 📊 Efficiency vs Daily Distance Analysis")
    fig_scatter = px.scatter(df_vehicles, x='Daily Distance', y='FE (km/L)',
                            size='Odometer', color='Status',
                            hover_data=['Vehicle ID', 'Model'],
                            color_discrete_map={'Active': '#10b981', 'Idle': '#f59e0b', 'Maintenance': '#ef4444'})
    fig_scatter.update_layout(height=400)
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Priority Alerts
    st.markdown("### 🚨 Priority Alerts Timeline")
    alerts = pd.DataFrame({
        'Time': ['08:15', '10:42', '14:23', '16:55'],
        'Vehicle': ['MH-12-TRK-052', 'GJ-01-TRK-031', 'DL-08-TRK-124', 'KA-05-TRK-089'],
        'Alert': ['Extended Idle: 285 min', 'Brake Service Overdue', 'Harsh Braking Event', 'Speeding Alert'],
        'Severity': ['Critical', 'High', 'Medium', 'Medium']
    })
    
    for _, alert in alerts.iterrows():
        severity_color = {'Critical': '🔴', 'High': '🟠', 'Medium': '🟡', 'Low': '🟢'}
        st.markdown(f"{severity_color[alert['Severity']]} **{alert['Time']}** - {alert['Vehicle']}: {alert['Alert']}")

# VEHICLE ANALYSIS
elif page == "🚛 Vehicle Analysis":
    st.title("Vehicle Analysis")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 All Vehicles", "⭐ Top Performers", "⚠️ Attention Required",
        "🔧 Maintenance Due", "📊 Efficiency Analysis"
    ])
    
    with tab1:
        st.markdown("### All Vehicles (150)")
        search = st.text_input("🔍 Search vehicles...", key="vehicle_search")
        
        if search:
            filtered = df_vehicles[df_vehicles['Vehicle ID'].str.contains(search, case=False)]
        else:
            filtered = df_vehicles
        
        st.dataframe(filtered, use_container_width=True, height=450)
        
        # Click to drill down
        selected_vehicle = st.selectbox("Select vehicle for detailed analysis:", filtered['Vehicle ID'].tolist())
        if selected_vehicle:
            vehicle_data = df_vehicles[df_vehicles['Vehicle ID'] == selected_vehicle].iloc[0]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Current FE", f"{vehicle_data['FE (km/L)']} km/L")
            with col2:
                st.metric("Odometer", f"{vehicle_data['Odometer']:,} km")
            with col3:
                st.metric("Daily Avg", f"{vehicle_data['Daily Distance']} km")
            with col4:
                st.metric("CO2/Day", f"{vehicle_data['Daily CO2 (kg)']} kg")
            
            # 7-day performance chart for selected vehicle
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            performance = [round(random.uniform(3.8, 4.6), 2) for _ in range(7)]
            fig_perf = px.line(x=days, y=performance, markers=True,
                              labels={'x': 'Day', 'y': 'Efficiency (km/L)'})
            fig_perf.update_traces(line_color='#667eea')
            st.plotly_chart(fig_perf, use_container_width=True)
    
    with tab2:
        st.markdown("### Top 20 Performing Vehicles")
        top20 = df_vehicles.nlargest(20, 'FE (km/L)')
        fig = px.bar(top20, x='FE (km/L)', y='Vehicle ID', orientation='h',
                    color='FE (km/L)', color_continuous_scale='Greens')
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Vehicles Requiring Attention")
        attention = df_vehicles[
            (df_vehicles['Status'] == 'Maintenance') | 
            (df_vehicles['FE (km/L)'] < 3.5) |
            (df_vehicles['Idle Time (min)'] > 150)
        ]
        st.dataframe(attention, use_container_width=True)
        st.warning(f"⚠️ {len(attention)} vehicles need attention")
    
    with tab4:
        st.markdown("### Maintenance Schedule (Next 30 Days)")
        maint_data = df_vehicles.sample(25).copy()
        maint_data['Days Until Service'] = [random.randint(1, 30) for _ in range(25)]
        maint_data = maint_data.sort_values('Days Until Service')
        
        fig = px.bar(maint_data, x='Days Until Service', y='Vehicle ID',
                    orientation='h', color='Days Until Service',
                    color_continuous_scale='RdYlGn_r')
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.markdown("### Efficiency Distribution")
        fig = px.histogram(df_vehicles, x='FE (km/L)', nbins=25,
                          color_discrete_sequence=['#667eea'])
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Efficiency by Model
        st.markdown("### Efficiency by Model (Box Plot)")
        fig_box = px.box(df_vehicles, x='Model', y='FE (km/L)',
                        color='Model', points="all")
        st.plotly_chart(fig_box, use_container_width=True)

# DRIVER PERFORMANCE
elif page == "👤 Driver Performance":
    st.title("Driver Performance Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Drivers", "145")
    with col2:
        avg_eff = df_drivers['Efficiency'].mean()
        st.metric("Avg Efficiency", f"{avg_eff:.2f} km/L")
    with col3:
        trained = len(df_drivers[df_drivers['Training'] == True])
        st.metric("Training Complete", f"{trained}/145 ({trained/145*100:.0f}%)")
    with col4:
        avg_score = df_drivers['Score'].mean()
        st.metric("Avg Score", f"{avg_score:.0f}/100")
    
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "🏆 Top Performers", "📈 Trends"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Performance Distribution")
            bins = pd.cut(df_drivers['Score'], bins=[0, 70, 80, 90, 100],
                         labels=['Below Avg', 'Average', 'Good', 'Excellent'])
            dist = bins.value_counts()
            fig = px.pie(values=dist.values, names=dist.index,
                        color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Efficiency vs Experience")
            fig = px.scatter(df_drivers, x='Experience', y='Efficiency',
                           size='Trips', color='Score',
                           hover_data=['Name'])
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### All Drivers")
        st.dataframe(df_drivers.sort_values('Score', ascending=False).head(30),
                    use_container_width=True)
    
    with tab2:
        st.markdown("### Top 20 Drivers by Efficiency")
        top20 = df_drivers.nlargest(20, 'Efficiency')
        fig = px.bar(top20, x='Efficiency', y='Name', orientation='h',
                    color='Score', color_continuous_scale='Viridis')
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Performance Trends (Simulated)")
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        avg_scores = [82, 84, 83, 86, 88, 89]
        fig = px.line(x=months, y=avg_scores, markers=True,
                     labels={'x': 'Month', 'y': 'Avg Score'})
        fig.update_traces(line_color='#10b981')
        st.plotly_chart(fig, use_container_width=True)

# CO2 ANALYTICS
elif page == "🌱 CO2 Analytics":
    st.title("CO2 & Environmental Analytics")
    
    col1, col2, col3 = st.columns(3)
    total_co2 = df_vehicles['Daily CO2 (kg)'].sum()
    with col1:
        st.metric("Daily Emissions", f"{total_co2:.0f} kg", "↓ 15.3%")
    with col2:
        st.metric("Monthly Emissions", f"{total_co2*30/1000:.1f} tonnes")
    with col3:
        st.metric("Target Progress", "76.5%", "↑ 8.2%")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Emission Trends (6 Months)")
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        emissions = [3200, 3100, 3050, 2980, 2950, 2940]
        fig = px.area(x=months, y=emissions,
                     labels={'x': 'Month', 'y': 'CO2 (kg/day)'})
        fig.update_traces(line_color='#10b981', fillcolor='rgba(16, 185, 129, 0.3)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### CO2 Source Breakdown")
        sources = pd.DataFrame({
            'Source': ['Fuel Burn', 'Idle Time', 'Route Inefficiency', 'Load Factor'],
            'Contribution (%)': [65, 18, 12, 5]
        })
        fig = px.pie(sources, values='Contribution (%)', names='Source',
                    color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Top 15 CO2 Emitters")
    top_emitters = df_vehicles.nlargest(15, 'Daily CO2 (kg)')
    fig = px.bar(top_emitters, x='Daily CO2 (kg)', y='Vehicle ID',
                orientation='h', color='Daily CO2 (kg)',
                color_continuous_scale='Reds')
    st.plotly_chart(fig, use_container_width=True)

# MICRO TRAINING
elif page == "📚 Micro Training":
    st.title("Micro Training & Development")
    
    col1, col2, col3 = st.columns(3)
    trained_count = len(df_drivers[df_drivers['Training'] == True])
    with col1:
        st.metric("Available Modules", "24")
    with col2:
        st.metric("Completion Rate", f"{trained_count/145*100:.0f}%")
    with col3:
        st.metric("Avg Module Rating", "4.6/5")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Training Status")
        status_data = pd.DataFrame({
            'Status': ['Completed', 'In Progress', 'Not Started'],
            'Count': [trained_count, 19, 145-trained_count-19]
        })
        fig = px.pie(status_data, values='Count', names='Status',
                    color='Status',
                    color_discrete_map={'Completed': '#10b981',
                                       'In Progress': '#f59e0b',
                                       'Not Started': '#ef4444'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Module Effectiveness")
        modules = pd.DataFrame({
            'Module': ['Eco Driving', 'Safety', 'Route Planning', 'Vehicle Care', 'Regulations'],
            'Rating': [4.8, 4.6, 4.5, 4.7, 4.4]
        })
        fig = px.bar(modules, x='Module', y='Rating',
                    color='Rating', color_continuous_scale='Greens')
        fig.update_layout(yaxis_range=[0, 5])
        st.plotly_chart(fig, use_container_width=True)

# FE OPPORTUNITIES
elif page == "💡 FE Opportunities":
    st.title("Fuel Efficiency Opportunities")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Monthly Opportunity", "₹2.4L")
    with col2:
        st.metric("Captured (75%)", "₹1.8L", "↑ 12%")
    with col3:
        st.metric("Lost Opportunity", "₹0.6L", "↓ ₹8K")
    
    st.markdown("### Opportunity Breakdown")
    opp_data = pd.DataFrame({
        'Category': ['Idle Reduction', 'Speed Optimization', 'Route Efficiency', 'Load Planning'],
        'Captured': [45000, 38000, 42000, 35000],
        'Lost': [15000, 12000, 10000, 8000]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Captured', x=opp_data['Category'], y=opp_data['Captured'],
                        marker_color='#10b981'))
    fig.add_trace(go.Bar(name='Lost', x=opp_data['Category'], y=opp_data['Lost'],
                        marker_color='#ef4444'))
    fig.update_layout(barmode='stack', height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Monthly Trend")
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    captured = [1.2, 1.4, 1.6, 1.7, 1.8, 1.8]
    lost = [0.9, 0.8, 0.7, 0.65, 0.62, 0.6]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=captured, name='Captured',
                            line=dict(color='#10b981'), fill='tozeroy'))
    fig.add_trace(go.Scatter(x=months, y=lost, name='Lost',
                            line=dict(color='#ef4444'), fill='tozeroy'))
    st.plotly_chart(fig, use_container_width=True)

# ADVANCED ANALYTICS
elif page == "🔬 Advanced Analytics":
    st.title("Advanced Analytics & AI Insights")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Predicted Failures", "12", "next 30 days")
    with col2:
        st.metric("Prevention Success", "94%")
    with col3:
        st.metric("Cost Saved", "₹8.4L", "YTD")
    
    st.markdown("### Fuel Efficiency Forecast (Next 4 Weeks)")
    weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
    predicted = [4.3, 4.4, 4.5, 4.6]
    actual = [4.3, 4.4, None, None]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=weeks, y=predicted, name='Predicted',
                            line=dict(dash='dash', color='#667eea')))
    fig.add_trace(go.Scatter(x=weeks[:2], y=actual[:2], name='Actual',
                            line=dict(color='#10b981')))
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Route Intelligence")
        routes = pd.DataFrame({
            'Route': ['Route A', 'Route B', 'Route C', 'Route D', 'Route E'],
            'Efficiency': [4.5, 4.2, 4.7, 3.9, 4.4]
        })
        fig = px.bar(routes, x='Route', y='Efficiency',
                    color='Efficiency', color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Cost Optimization Scenarios")
        scenarios = pd.DataFrame({
            'Scenario': ['Current', 'Optimized Routes', 'Idle Reduction', 'Combined'],
            'Monthly Cost (₹L)': [15.2, 14.1, 13.8, 12.5]
        })
        fig = px.bar(scenarios, x='Scenario', y='Monthly Cost (₹L)',
                    color='Monthly Cost (₹L)', color_continuous_scale='Greens_r')
        st.plotly_chart(fig, use_container_width=True)

# MAINTENANCE
elif page == "🔧 Maintenance":
    st.title("Maintenance Management")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Due in 7 Days", "8 vehicles")
    with col2:
        st.metric("Due in 15 Days", "15 vehicles")
    with col3:
        st.metric("Total Cost (YTD)", "₹12.4L")
    with col4:
        avg_cost = 12.4 / 150
        st.metric("Avg Cost/Vehicle", f"₹{avg_cost:.2f}L")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Maintenance Schedule")
        bins = ['0-7 Days', '8-15 Days', '16-30 Days', '> 30 Days']
        counts = [8, 15, 32, 95]
        fig = px.bar(x=bins, y=counts,
                    labels={'x': 'Days Until Service', 'y': 'Vehicles'},
                    color=counts, color_continuous_scale='RdYlGn_r')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Monthly Cost Trends")
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        costs = [1.8, 2.1, 1.9, 2.3, 2.0, 2.3]
        fig = px.line(x=months, y=costs,
                     labels={'x': 'Month', 'y': 'Cost (₹L)'},
                     markers=True)
        fig.update_traces(line_color='#f59e0b', fill='tozeroy')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Upcoming Maintenance (Next 15 Days)")
    maint_upcoming = df_vehicles.sample(15).copy()
    maint_upcoming['Days Until Service'] = [random.randint(1, 15) for _ in range(15)]
    st.dataframe(maint_upcoming[['Vehicle ID', 'Model', 'Odometer', 'Days Until Service']],
                use_container_width=True)

# COST ANALYSIS
elif page == "💰 Cost Analysis":
    st.title("Cost Analysis & Financial Insights")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Operating Cost", "₹45.2L")
    with col2:
        st.metric("Cost per KM", "₹32.4")
    with col3:
        st.metric("Fuel Cost (63%)", "₹28.5L")
    with col4:
        st.metric("Maintenance (15%)", "₹6.8L")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Cost Breakdown")
        cost_data = pd.DataFrame({
            'Category': ['Fuel', 'Maintenance', 'Driver Salary', 'Insurance', 'Others'],
            'Percentage': [63, 15, 12, 6, 4]
        })
        fig = px.pie(cost_data, values='Percentage', names='Category',
                    color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Monthly Cost Trends")
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        total_costs = [42.5, 44.2, 43.8, 46.1, 44.8, 45.2]
        fig = px.line(x=months, y=total_costs,
                     labels={'x': 'Month', 'y': 'Total Cost (₹L)'},
                     markers=True)
        fig.update_traces(line_color='#667eea', fill='tozeroy')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Vehicle-wise Cost Analysis (Top 20)")
    cost_details = df_vehicles.sample(20).copy()
    cost_details['Total Cost'] = cost_details['Cost/KM'] * cost_details['Odometer'] / 1000
    st.dataframe(cost_details[['Vehicle ID', 'Model', 'Cost/KM', 'Odometer', 'Total Cost']].sort_values('Total Cost', ascending=False),
                use_container_width=True)

# COMPLIANCE
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
    
    st.markdown("### Compliance Status by Category")
    compliance = pd.DataFrame({
        'Category': ['Registration', 'Insurance', 'Permits', 'Fitness', 'Pollution', 'License'],
        'Compliance (%)': [98, 96, 94, 95, 97, 99]
    })
    fig = px.bar(compliance, x='Category', y='Compliance (%)',
                color='Compliance (%)', color_continuous_scale='Greens')
    fig.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Upcoming Renewals (Next 60 Days)")
    docs = ['Registration', 'Insurance', 'Permit', 'Fitness', 'PUC']
    renewals = []
    for i in range(15):
        vehicle = df_vehicles.sample(1).iloc[0]
        days = random.randint(5, 60)
        renewals.append({
            'Vehicle ID': vehicle['Vehicle ID'],
            'Document': random.choice(docs),
            'Expiry Date': (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d'),
            'Days Left': days,
            'Status': 'Urgent' if days < 15 else 'Soon' if days < 30 else 'OK'
        })
    
    renewals_df = pd.DataFrame(renewals).sort_values('Days Left')
    st.dataframe(renewals_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**Fleet Managers Dashboard** • Indian Heavy Commercial Vehicles • Built with Streamlit 🚛")
