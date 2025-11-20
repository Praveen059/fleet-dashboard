import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(page_title="Fleet Managers Dashboard", layout="wide", initial_sidebar_state="expanded")

# Data generators
@st.cache_data
def generate_vehicles(n=150):
    models = ['Heavy Truck 45T', 'Heavy Truck 40T', 'Medium Truck 25T', 'Light Truck 12T', 'Multi-Axle 49T']
    regions = ['North', 'South', 'East', 'West', 'Central']
    statuses = ['Active', 'Idle', 'Maintenance']
    data = []
    for i in range(n):
        odo = random.randint(60000, 520000)
        maint_cost = random.randint(40000, 240000)
        maint_cpkm = round(maint_cost/(odo+1),2)
        data.append({
            "Vehicle ID": f"MH-{str(i+1).zfill(2)}-TRK-{random.randint(1000,9999)}",
            "Model": random.choice(models),
            "Region": random.choice(regions),
            "Status": random.choice(statuses),
            "Driver": f"Driver {chr(65 + i//10)}{i%10}",
            "FE (km/L)": round(random.uniform(3.2, 5.4), 2),
            "Odometer (km)": odo,
            "Daily Distance (km)": random.randint(200, 670),
            "Operating Cost per KM (₹)": round(random.uniform(25, 48), 2),
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
        dist = random.randint(50000, 270000)
        eff = round(random.uniform(3.7, 5.3),2)
        data.append({
            "Driver ID": f"D-{i+1}",
            "Driver Name": f"Driver {chr(65+i//10)}{i%10}",
            "Score": random.randint(70, 100),
            "Efficiency (km/L)": eff,
            "Total Trips": trips,
            "Total Distance (km)": dist,
            "Avg Distance/Trip (km)": round(dist/trips, 1),
            "Fuel Savings Contributed (₹)": round(random.uniform(900, 3500),2)
        })
    return pd.DataFrame(data)

df_vehicles = generate_vehicles()
df_drivers = generate_drivers()

# Sidebar – icons, clean, modern business look
nav_options = [
    "🏠 Fleet Overview",
    "🚚 Vehicles",
    "🧑‍💼 Drivers",
    "💡 Fuel Opportunities",
    "🔬 Fleet Ranking",
    "🛠️ Maintenance",
    "📉 CPKM Analytics",
    "🌳 CO2 Impact",
    "✅ Compliance",
    "💰 Cost Summary"
]

with st.sidebar:
    st.markdown(
        """
        <div style='text-align:center;margin-bottom:18px;'>
            <span style='font-size:22px;'>🟦</span>
            <span style='font-size:1.28rem;font-weight:620;padding:8px 28px 9px 28px;border-radius:18px;color:#246eff;background:#f5f6fa;margin:0 8px;'>Fleet Managers Dashboard</span>
        </div>
        """, unsafe_allow_html=True
    )
    nav = st.radio("", nav_options, index=0, label_visibility="collapsed")

# KPIs always at top
st.markdown("""
<style>
.metric-white div[data-testid="stMetric"] {
  background: #fff;
  color: #222;
  border-radius: 13px;
  box-shadow: 0 2px 10px rgba(100,150,200,0.08);
  font-weight: 550;
}
</style>
<div style='margin-bottom:9px;'></div>
""",unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("Total Vehicles", len(df_vehicles))
with k2:
    st.metric("Fleet Avg. Efficiency", f"{df_vehicles['FE (km/L)'].mean():.2f} km/L")
with k3:
    st.metric("Total Fuel Savings (₹)", f"{df_vehicles['Fuel Savings Opportunity (₹)'].sum():,.0f}")
with k4:
    st.metric("Avg. Maint CPKM (₹)", f"{df_vehicles['Maintenance CPKM (₹)'].mean():.2f}")

# Main content
if nav == "🏠 Fleet Overview":
    st.header("Fleet Efficiency & Composition")
    col1, col2 = st.columns([1.8,1.2])
    with col1:
        fig = px.line(
            x=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
            y=[4.2,4.1,4.4,4.7,4.6,4.3,4.5],
            labels={"x":"Day","y":"Efficiency (km/L)"},
            title="Efficiency Trend"
        )
        fig.update_layout(margin=dict(l=10,r=10,b=18), height=260)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        reg_counts = df_vehicles["Region"].value_counts()
        fig = px.pie(values=reg_counts.values, names=reg_counts.index, title="Fleet by Region",
                     color_discrete_sequence=["#246eff","#10b981","#ef4444","#f59e0b","#596377"])
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Fleet Breakdown by Model")
    fig = px.bar(df_vehicles, x="Model", color="Model", title="Vehicle Count by Model")
    st.plotly_chart(fig, use_container_width=True)
    st.info("Priority Alerts: 1 Brake service due | 1 Extended idle | 1 Efficiency increase")

elif nav == "🚚 Vehicles":
    st.header("Vehicles")
    s1, s2 = st.columns([1.2,1])
    with s1:
        search = st.text_input("🔎 Vehicle Search")
    with s2:
        status = st.selectbox("Status",["All"]+sorted(df_vehicles["Status"].unique()))
    dfv = df_vehicles.copy()
    if search:
        dfv = dfv[dfv["Vehicle ID"].str.contains(search,case=False)]
    if status!="All":
        dfv = dfv[dfv["Status"]==status]
    st.dataframe(dfv, use_container_width=True, height=340)
    st.write("Select a vehicle below for full details:")
    selected = st.selectbox("Vehicle ID", dfv["Vehicle ID"],index=0)
    v = dfv[dfv["Vehicle ID"]==selected].iloc[0]
    with st.expander(f"Details for {selected}", expanded=True):
        c1,c2,c3 = st.columns(3)
        with c1:
            st.metric("Model",v["Model"])
            st.metric("Driver",v["Driver"])
            st.metric("Region",v["Region"])
        with c2:
            st.metric("Efficiency",f"{v['FE (km/L)']} km/L")
            st.metric("Maint CPKM",f"₹{v['Maintenance CPKM (₹)']}")
        with c3:
            st.metric("Odometer",f"{v['Odometer (km)']:,} km")
            st.metric("Fuel Savings",f"₹{v['Fuel Savings Opportunity (₹)']}")
        fig = px.bar(
            x=["Fuel","Maintenance","Other"],
            y=[v["Operating Cost per KM (₹)"],v["Maintenance CPKM (₹)"],random.uniform(5,10)],
            labels={"x":"Category","y":"₹/KM"},
            title="CPKM Breakdown"
        )
        st.plotly_chart(fig, use_container_width=True)
        fig = px.line(x=["Jan","Feb","Mar"],y=[random.uniform(3.5,4.7),random.uniform(3.5,4.7),random.uniform(3.8,5.3)],title="Efficiency History")
        st.plotly_chart(fig,use_container_width=True)

elif nav == "🧑‍💼 Drivers":
    st.header("Drivers")
    search = st.text_input("Search Driver Name",key="drvsearch")
    dfd = df_drivers.copy()
    if search:
        dfd = dfd[dfd["Driver Name"].str.contains(search,case=False)]
    st.dataframe(dfd, use_container_width=True, height=340)
    sel_d = st.selectbox("Driver Name",dfd["Driver Name"],index=0)
    d = dfd[dfd["Driver Name"]==sel_d].iloc[0]
    with st.expander(f"Details for {sel_d}",expanded=True):
        a1,a2,a3,a4 = st.columns(4)
        with a1:
            st.metric("Efficiency",f"{d['Efficiency (km/L)']}")
            st.metric("Score",d["Score"])
        with a2:
            st.metric("Total Trips",d["Total Trips"])
            st.metric("Total Distance",f"{d['Total Distance (km)']:,} km")
        with a3:
            st.metric("Avg Distance/Trip",f"{d['Avg Distance/Trip (km)']} km")
        with a4:
            st.metric("Fuel Savings",f"₹{d['Fuel Savings Contributed (₹)']}")
        fig = px.line(x=["Jan","Feb","Mar","Apr"],y=[random.randint(70,100) for _ in range(4)],title="Performance History")
        st.plotly_chart(fig, use_container_width=True)

elif nav == "💡 Fuel Opportunities":
    st.header("Fuel Savings Opportunities")
    st.metric("Total Opportunity",f"₹{df_vehicles['Fuel Savings Opportunity (₹)'].sum():,}".replace(",",""))
    mdf = df_vehicles.groupby("Model")["Fuel Savings Opportunity (₹)"].sum().reset_index()
    fig = px.bar(mdf, x="Model", y="Fuel Savings Opportunity (₹)", color="Model",title="Fuel Savings by Model")
    st.plotly_chart(fig,use_container_width=True)
    topv = df_vehicles.nlargest(7,"Fuel Savings Opportunity (₹)")
    st.subheader("Top Vehicles")
    st.dataframe(topv[["Vehicle ID","Model","Fuel Savings Opportunity (₹)"]],use_container_width=True)

elif nav == "🔬 Fleet Ranking":
    st.header("Fleet Ranking & Comparison")
    most_eff = df_vehicles.nlargest(7,"FE (km/L)")
    least_eff = df_vehicles.nsmallest(7,"FE (km/L)")
    st.subheader("Most Efficient Vehicles")
    st.dataframe(most_eff[["Vehicle ID","Model","FE (km/L)"]], use_container_width=True)
    st.subheader("Least Efficient Vehicles")
    st.dataframe(least_eff[["Vehicle ID","Model","FE (km/L)"]], use_container_width=True)
    fig = px.scatter(df_vehicles,x="FE (km/L)",y="Maintenance CPKM (₹)",color="Model",title="Efficiency vs Maintenance")
    st.plotly_chart(fig,use_container_width=True)

elif nav == "🛠️ Maintenance":
    st.header("Maintenance Analysis")
    st.metric("Fleet Maint CPKM",f"₹{df_vehicles['Maintenance CPKM (₹)'].mean():.2f}")
    fig = px.histogram(df_vehicles,x="Maintenance CPKM (₹)",nbins=25,title="CPKM by Vehicle")
    st.plotly_chart(fig,use_container_width=True)
    st.subheader("Upcoming Services")
    df_up = df_vehicles.sample(7)
    st.dataframe(df_up[["Vehicle ID","Model","Odometer (km)","Maintenance CPKM (₹)"]],use_container_width=True)

elif nav == "📉 CPKM Analytics":
    st.header("Deep Dive CPKM Analytics")
    fig = px.box(df_vehicles,x="Model",y="Maintenance CPKM (₹)",color="Model",title="CPKM by Model")
    st.plotly_chart(fig,use_container_width=True)
    fig = px.pie(df_vehicles,names="Model",values="Maintenance CPKM (₹)",title="Model-wise Maint CPKM Share")
    st.plotly_chart(fig,use_container_width=True)

elif nav == "🌳 CO2 Impact":
    st.header("Environmental Impact")
    st.metric("Total Daily CO2",f"{df_vehicles['Daily CO2 (kg)'].sum():,.0f} kg")
    fig = px.histogram(df_vehicles,x="Daily CO2 (kg)",color="Model",nbins=24,title="CO2 Emissions Distribution")
    st.plotly_chart(fig,use_container_width=True)

elif nav == "✅ Compliance":
    st.header("Compliance Overview")
    st.success(f"BS-VI Compliant: {random.randint(120,150)}/150 vehicles")
    st.info("Renewal Pending: Registration, PUC - 9 vehicles within 30 days")
    fig = px.bar(
        x=["Registration","Insurance","Permits","Fitness","Pollution","License"],
        y=[98,96,95,92,97,99],title="Compliance Percentage"
    )
    st.plotly_chart(fig,use_container_width=True)

elif nav == "💰 Cost Summary":
    st.header("Fleet Cost Summary")
    st.metric("Avg Cost/KM",f"₹{df_vehicles['Operating Cost per KM (₹)'].mean():.2f}")
    fig = px.box(df_vehicles,x="Model",y="Operating Cost per KM (₹)",color="Model",title="Operating Cost/KM by Model")
    st.plotly_chart(fig,use_container_width=True)
    fig = px.pie(df_vehicles,names="Model",values="Operating Cost per KM (₹)",title="Cost share by Model")
    st.plotly_chart(fig,use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#555;font-size:1rem;padding:7px;'>Fleet Managers Dashboard · Indian HCV · Powered by Streamlit</div>",
    unsafe_allow_html=True)
