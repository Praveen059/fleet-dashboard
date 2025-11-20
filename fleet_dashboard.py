import streamlit as st
import pandas as pd
import plotly.express as px
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="Fleet Dashboard", layout="wide")

# --------------------------
# -- DATA GENERATION --
# --------------------------
@st.cache_data
def generate_vehicles(n=150):
    models = ['Heavy Truck 45T', 'Heavy Truck 40T', 'Medium Truck 25T', 'Light Truck 12T', 'Multi-Axle 49T']
    regions = ['North', 'South', 'East', 'West', 'Central']
    status = ['Active', 'Idle', 'Maintenance']
    data = []
    for i in range(n):
        odo = random.randint(50000, 500000)
        maint_cost = random.randint(50000, 250000)
        maint_cpkm = round(maint_cost / max(odo, 1), 2)
        data.append({
            "Vehicle ID": f"MH-{str(i+1).zfill(2)}-TRK-{random.randint(1000,9999)}",
            "Model": random.choice(models),
            "Region": random.choice(regions),
            "Status": random.choice(status),
            "Driver": f"Driver {chr(65 + i//10)}{i%10}",
            "FE (km/L)": round(random.uniform(3.2, 5.2), 2),
            "Odometer (km)": odo,
            "Daily Distance (km)": random.randint(200, 650),
            "Operating Cost per KM (₹)": round(random.uniform(25, 45), 2),
            "Maintenance Cost Total (₹)": maint_cost,
            "Maintenance CPKM (₹)": maint_cpkm,
            "Fuel Savings Opportunity (₹)": round(random.uniform(1200, 5200),2),
            "Daily CO2 (kg)": round(random.uniform(20, 35), 1)
        })
    return pd.DataFrame(data)

@st.cache_data
def generate_drivers(n=145):
    data = []
    for i in range(n):
        trips = random.randint(50, 160)
        dist = random.randint(50000, 250000)
        eff = round(random.uniform(3.5, 5.2), 2)
        data.append({
            "Driver ID": f"D-{i+1}",
            "Driver Name": f"Driver {chr(65+i//10)}{i%10}",
            "Score": random.randint(70, 100),
            "Efficiency (km/L)": eff,
            "Total Trips": trips,
            "Total Distance (km)": dist,
            "Avg Distance/Trip (km)": round(dist/trips, 1),
            "Fuel Savings Contributed (₹)": round(random.uniform(900, 2900),2)
        })
    return pd.DataFrame(data)

df_vehicles = generate_vehicles()
df_drivers = generate_drivers()

# --------------------------------
# --- SIDEBAR: MODERN BUSINESS STYLE ---
# --------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style='text-align:center;padding:18px 0 18px 0;'>
            <span style='font-size:1.7rem;'>🌞</span>
            <span style='font-size:1.2rem;background:#f5f6fa;padding:7px 30px;border-radius:16px;margin-left:6px;margin-right:6px;color:#333;'>Dark Mode</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    nav = st.radio("", [
        "🏠 Fleet Overview",
        "🚚 Vehicle Analysis",
        "🧑‍💼 Driver Performance",
        "🌳 CO2 Analytics",
        "📚 Micro Training",
        "💡 FE Opportunities",
        "🔬 Fleet Comparison",
        "🛠️ Maintenance/CPKM",
        "💰 Cost Analysis",
        "✅ Compliance"
    ], label_visibility="collapsed", key="sidebar_menu")

# --------------------------------
# --- KPIs Always Visible ---
# --------------------------------
st.markdown("""
<div style='background:#fff;border-radius:9px;padding:10px 8px 1px 18px;margin-bottom:0;box-shadow:0 1px 8px #e3e9fa;'>
    <span style='font-size:1.9rem;color:#246eff;font-weight:700;'>Fleet Management Dashboard</span>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Vehicles", len(df_vehicles))
with col2:
    st.metric("Fleet Efficiency", f"{df_vehicles['FE (km/L)'].mean():.2f} km/L")
with col3:
    st.metric("Monthly Fuel Savings", f"₹{df_vehicles['Fuel Savings Opportunity (₹)'].sum():,.0f}")
with col4:
    st.metric("Monthly Maint CPKM", f"₹{df_vehicles['Maintenance CPKM (₹)'].mean():.2f}")

# --- Main Content ---
if nav == "🏠 Fleet Overview":
    st.subheader("Fleet Efficiency & Composition")
    col1, col2 = st.columns([2,1])
    with col1:
        fig = px.line(x=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
            y=[4.1, 4.3, 4.2, 4.4, 4.3, 4.5, 4.2], labels={"x":"Day","y":"Efficiency (km/L)"})
        fig.update_layout(margin=dict(l=0,r=0,b=20), height=270)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        reg_counts = df_vehicles["Region"].value_counts()
        fig = px.pie(values=reg_counts.values, names=reg_counts.index, title="Fleet by Region", color_discrete_sequence=["#246eff","#10b981","#ef4444","#f59e0b","#596377"])
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)
    st.subheader("Fleet Breakdown by Model")
    fig = px.bar(df_vehicles, x="Model", color="Model", title="Vehicle Count by Model")
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Priority Alerts")
    st.warning("⚠️ MH-12-TRK-032 - Brake service overdue by 1100 km")
    st.error("🚨 DL-08-TRK-115 - Extended idle: 220 min; Fuel waste: 14L")
    st.success("✅ Driver A3 - Efficiency improved by 15% this week")

elif nav == "🚚 Vehicle Analysis":
    st.subheader("Vehicles Table")
    search = st.text_input("Search Vehicle ID", key="veh_search")
    vehicles_df = df_vehicles.copy()
    if search:
        vehicles_df = vehicles_df[vehicles_df["Vehicle ID"].str.contains(search, case=False)]
    status_filter = st.selectbox("Status Filter", ["All"] + sorted(df_vehicles["Status"].unique()), key="veh_status")
    if status_filter != "All":
        vehicles_df = vehicles_df[vehicles_df["Status"] == status_filter]

    st.dataframe(vehicles_df, use_container_width=True, height=350)
    st.markdown("### Select a Vehicle for Details")
    selected = st.selectbox("Select Vehicle ID", vehicles_df["Vehicle ID"], key="veh_selected")
    if selected:
        v = vehicles_df[vehicles_df["Vehicle ID"] == selected].iloc[0]
        st.markdown(f"#### {selected} - Detail Panel", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Model", v["Model"])
            st.metric("Driver", v["Driver"])
            st.metric("Region", v["Region"])
        with col2:
            st.metric("Efficiency", f"{v['FE (km/L)']} km/L")
            st.metric("Operating CPKM", f"₹{v['Operating Cost per KM (₹)']}")
            st.metric("Maint CPKM", f"₹{v['Maintenance CPKM (₹)']}")
        with col3:
            st.metric("Odometer", f"{v['Odometer (km)']:,} km")
            st.metric("Daily Distance", f"{v['Daily Distance (km)']} km")
            st.metric("Fuel Savings Opp.", f"₹{v['Fuel Savings Opportunity (₹)']}")

        st.markdown("**Performance & Cost Charts**")
        fig = px.bar(
            x=["Fuel","Maintenance","Other"],
            y=[v["Operating Cost per KM (₹)"],v["Maintenance CPKM (₹)"],random.uniform(5,12)],
            labels={"x":"Category","y":"Cost per KM (₹)"}
        )
        st.plotly_chart(fig, use_container_width=True)
        fig = px.line(x=["Jan","Feb","Mar","Apr"],y=[random.uniform(3.5,5.2) for _ in range(4)],title="Efficiency History")
        st.plotly_chart(fig, use_container_width=True)

elif nav == "🧑‍💼 Driver Performance":
    st.subheader("Drivers Table")
    search = st.text_input("Search Driver Name", key="drv_search")
    drivers_df = df_drivers.copy()
    if search:
        drivers_df = drivers_df[drivers_df["Driver Name"].str.contains(search, case=False)]
    st.dataframe(drivers_df, use_container_width=True, height=350)
    st.markdown("### Select a Driver for Details")
    selected = st.selectbox("Select Driver Name", drivers_df["Driver Name"], key="drv_selected")
    if selected:
        d = drivers_df[drivers_df["Driver Name"] == selected].iloc[0]
        st.markdown(f"#### {selected} - Detail Panel", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Efficiency", f"{d['Efficiency (km/L)']}")
            st.metric("Score", d["Score"])
        with col2:
            st.metric("Total Trips", d["Total Trips"])
            st.metric("Total Distance", f"{d['Total Distance (km)']:,} km")
        with col3:
            st.metric("Avg Dist/Trip", f"{d['Avg Distance/Trip (km)']} km")
        with col4:
            st.metric("Fuel Savings", f"₹{d['Fuel Savings Contributed (₹)']}")

        st.markdown("**Performance Charts**")
        fig = px.line(x=["Jan","Feb","Mar","Apr"],y=[random.randint(70,100) for _ in range(4)],title="Performance History")
        st.plotly_chart(fig, use_container_width=True)

elif nav == "🌳 CO2 Analytics":
    st.subheader("Fleet CO2 & Environmental Impact")
    st.metric("Total Daily CO2", f"{df_vehicles['Daily CO2 (kg)'].sum():.0f} kg")
    fig = px.histogram(df_vehicles,x="Daily CO2 (kg)",color="Model",nbins=24,title="Daily CO2 Distribution")
    st.plotly_chart(fig, use_container_width=True)

elif nav == "📚 Micro Training":
    st.subheader("Driver Micro Training Overview")
    st.success("85% drivers have completed micro training modules")
    fig = px.bar(df_drivers,x="Driver Name",y="Score",color="Score",title="Driver Training Scores")
    st.plotly_chart(fig,use_container_width=True)

elif nav == "💡 FE Opportunities":
    st.subheader("Fleet Fuel Savings Opportunities")
    st.metric("Monthly Fleet Fuel Savings", f"₹{df_vehicles['Fuel Savings Opportunity (₹)'].sum():,.0f}")
    models = df_vehicles.groupby("Model")["Fuel Savings Opportunity (₹)"].sum().reset_index()
    fig = px.bar(models, x="Model", y="Fuel Savings Opportunity (₹)", color="Model",title="Fuel Savings by Model")
    st.plotly_chart(fig, use_container_width=True)
    top = df_vehicles.nlargest(5, "Fuel Savings Opportunity (₹)")
    st.markdown("#### Top 5 Vehicles by Fuel Savings Opportunity")
    st.dataframe(top[["Vehicle ID","Model","Fuel Savings Opportunity (₹)"]], use_container_width=True)

elif nav == "🔬 Fleet Comparison":
    st.subheader("Fleet Comparison & Ranking")
    most_efficient = df_vehicles.nlargest(10,"FE (km/L)")
    least_efficient = df_vehicles.nsmallest(10,"FE (km/L)")
    st.markdown("#### Top 10 Most Efficient Vehicles")
    st.dataframe(most_efficient[["Vehicle ID","Model","FE (km/L)"]], use_container_width=True)
    st.markdown("#### Bottom 10 Least Efficient Vehicles")
    st.dataframe(least_efficient[["Vehicle ID","Model","FE (km/L)"]], use_container_width=True)
    fig = px.scatter(df_vehicles,x="FE (km/L)",y="Maintenance CPKM (₹)",color="Model",title="Efficiency vs Maintenance")
    st.plotly_chart(fig, use_container_width=True)

elif nav == "🛠️ Maintenance/CPKM":
    st.subheader("Fleet Maintenance & CPKM Analysis")
    st.metric("Overall Maintenance CPKM", f"₹{df_vehicles['Maintenance CPKM (₹)'].mean():.2f}")
    fig = px.histogram(df_vehicles,x="Maintenance CPKM (₹)",nbins=25,title="CPKM Distribution")
    st.plotly_chart(fig, use_container_width=True)
    top_maint = df_vehicles.nlargest(10,"Maintenance CPKM (₹)")
    st.markdown("#### Top 10 Maintenance CPKM Vehicles")
    st.dataframe(top_maint[["Vehicle ID","Model","Maintenance CPKM (₹)"]], use_container_width=True)

elif nav == "💰 Cost Analysis":
    st.subheader("Fleet Cost Analysis")
    st.metric("Avg Fleet Cost per KM", f"₹{df_vehicles['Operating Cost per KM (₹)'].mean():.2f}")
    fig = px.box(df_vehicles,x="Model",y="Operating Cost per KM (₹)",color="Model",title="Operating Cost/KM by Model")
    st.plotly_chart(fig, use_container_width=True)
    fig = px.pie(df_vehicles,names="Model",values="Operating Cost per KM (₹)",title="Model-wise Cost Share")
    st.plotly_chart(fig, use_container_width=True)

elif nav == "✅ Compliance":
    st.subheader("Fleet Compliance Status")
    st.success(f"BS-VI Compliant Vehicles: {random.randint(120,150)}/150")
    st.warning("Renewal Due Soon: Registration/PUC - 8 vehicles within 30 days")
    fig = px.bar(
        x=["Registration","Insurance","Permits","Fitness","Pollution","License"],
        y=[98,96,95,92,97,99], labels={"x":"Category","y":"Compliance %"},title="Compliance by Category"
    )
    st.plotly_chart(fig,use_container_width=True)

st.markdown("""
---
<div style='text-align:center;color:#888;font-size:1rem;padding:6px;'>
Fleet Managers Dashboard &middot; Indian HCV &middot; Powered by Streamlit
</div>
""", unsafe_allow_html=True)
