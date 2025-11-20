import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

st.set_page_config(page_title="Fleet Managers Dashboard", layout="wide", page_icon="🚛")

# Generate Data
@st.cache_data
def generate_vehicles(count=150):
    models = ['Heavy Truck 45T', 'Heavy Truck 40T', 'Medium Truck 25T', 'Light Truck 12T', 'Multi-Axle 49T']
    states = ['MH', 'DL', 'GJ', 'KA', 'TN', 'UP', 'RJ', 'HR', 'PB', 'WB']
    statuses = ['Active', 'Idle', 'Maintenance']
    
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
            'Driver': f"Driver {chr(65 + i//10)}{i%10}",
            'FE (km/L)': round(random.uniform(3.2, 5.2), 2),
            'Odometer': random.randint(50000, 550000),
            'Daily Distance': random.randint(200, 600),
            'Cost/KM': round(random.uniform(25, 45), 2),
            'Daily CO2 (kg)': round(random.uniform(15, 30), 1)
        })
    
    return pd.DataFrame(vehicles)

df_vehicles = generate_vehicles(150)

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
        "💰 Cost Analysis",
        "🔧 Maintenance",
        "✅ Compliance"
    ])

# FLEET OVERVIEW
if page == "🏠 Fleet Overview":
    st.title("Fleet Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Fleet Average", "4.1 km/L", "↑ 7.2%")
    with col2:
        st.metric("Weekly Fuel Cost", "₹1.68L", "↓ ₹17.4K")
    with col3:
        st.metric("Active Vehicles", "127/150")
    with col4:
        st.metric("Daily CO2", "2,940 kg", "↓ 15.3%")
    
    st.markdown("### Fleet Performance Trend")
    fig = px.line(x=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                 y=[4.1, 4.3, 4.2, 4.4, 4.5, 4.3, 4.4],
                 labels={'x': 'Day', 'y': 'Efficiency (km/L)'},
                 template='plotly_dark')
    fig.update_traces(line_color='#667eea', fill='tozeroy')
    st.plotly_chart(fig, use_container_width=True)

# VEHICLE ANALYSIS
elif page == "🚛 Vehicle Analysis":
    st.title("Vehicle Analysis")
    
    search = st.text_input("🔍 Search vehicles...")
    if search:
        filtered = df_vehicles[df_vehicles['Vehicle ID'].str.contains(search, case=False)]
    else:
        filtered = df_vehicles
    
    st.dataframe(filtered, use_container_width=True, height=400)
    
    st.markdown("### Efficiency Distribution")
    fig = px.histogram(df_vehicles, x='FE (km/L)', nbins=20,
                      template='plotly_dark', color_discrete_sequence=['#667eea'])
    st.plotly_chart(fig, use_container_width=True)

# DRIVER PERFORMANCE
elif page == "👤 Driver Performance":
    st.title("Driver Performance")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Drivers", "145")
    with col2:
        st.metric("Avg Efficiency", "4.2 km/L")
    with col3:
        st.metric("Training Complete", "87%")
    
    fig = go.Figure(data=[go.Pie(
        labels=['Completed', 'In Progress', 'Not Started'],
        values=[126, 19, 5],
        marker=dict(colors=['#10b981', '#f59e0b', '#ef4444'])
    )])
    fig.update_layout(template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

# CO2 ANALYTICS
elif page == "🌱 CO2 Analytics":
    st.title("CO2 Analytics")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Daily Emissions", "2,940 kg", "↓ 15.3%")
    with col2:
        st.metric("Monthly Emissions", "88.2 t")
    with col3:
        st.metric("Target Progress", "76.5%")
    
    fig = px.line(x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                 y=[3200, 3100, 3050, 2980, 2950, 2940],
                 labels={'x': 'Month', 'y': 'CO2 (kg)'},
                 template='plotly_dark')
    fig.update_traces(line_color='#10b981', fill='tozeroy')
    st.plotly_chart(fig, use_container_width=True)

# COST ANALYSIS
elif page == "💰 Cost Analysis":
    st.title("Cost Analysis")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Cost", "₹45.2L")
    with col2:
        st.metric("Cost per KM", "₹32.4")
    with col3:
        st.metric("Fuel Cost", "₹28.5L")
    
    fig = go.Figure(data=[go.Pie(
        labels=['Fuel', 'Maintenance', 'Salary', 'Insurance', 'Others'],
        values=[63, 15, 12, 6, 4]
    )])
    fig.update_layout(template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

# MAINTENANCE
elif page == "🔧 Maintenance":
    st.title("Maintenance")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Due in 7 Days", "8")
    with col2:
        st.metric("Due in 15 Days", "15")
    with col3:
        st.metric("Total Cost", "₹12.4L")
    
    fig = px.line(x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                 y=[1.8, 2.1, 1.9, 2.3, 2.0, 2.3],
                 labels={'x': 'Month', 'y': 'Cost (₹L)'},
                 template='plotly_dark')
    fig.update_traces(line_color='#f59e0b', fill='tozeroy')
    st.plotly_chart(fig, use_container_width=True)

# COMPLIANCE
elif page == "✅ Compliance":
    st.title("Compliance")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Compliance Score", "96%")
    with col2:
        st.metric("BS-VI Compliant", "142/150")
    with col3:
        st.metric("Expiring Soon", "6")
    
    fig = px.bar(x=['Registration', 'Insurance', 'Permits', 'Fitness', 'Pollution', 'License'],
                y=[98, 96, 94, 95, 97, 99],
                template='plotly_dark', color_discrete_sequence=['#10b981'])
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**Fleet Managers Dashboard** • Indian HCV • Built with Streamlit")

