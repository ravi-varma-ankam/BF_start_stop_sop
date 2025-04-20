import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
from datetime import datetime, timedelta

# pages = [
#     st.Page("main.py", title = "BF START UP", icon = "🔥"),
#     st.Page("shutdown.py", title = "BF SHUT DOWN", icon = "🔥"),
# ]

# pg = st.navigation(pages, position = "sidebar", expanded = True)
# pg.run()

st.set_page_config(
    page_title="BF START UP",
    page_icon="🔥",
)

##---------- import data -------------
wind_shutdown = pd.read_excel('wind_shutdown.xlsx')
wind_startup = pd.read_excel('wind_startup.xlsx')

# st.write(pd.to_datetime(wind_startup['Hour'], format='%H:%M:%S').dt.time)
# wind_startup['Hour'] = pd.to_datetime(wind_startup['Hour'], format='%H:%M:%S').dt.time
startup_mins = wind_startup['Hour'].astype('str').str.split(':').apply(lambda x: int(x[0]) * 60 + int(x[1])).to_list()
wind_startup['mins'] = startup_mins

# st.write(wind_shutdown)
# st.write(wind_startup)

# ------------------ Title -----------------------
# ------------------------------------------------
st.title("🔥 Blast Furnace START UP")
# --- Form Section ---
st.subheader("🧾 Input Parameters")

# with st.form("start_up_form"):
#     selected_furnace = st.selectbox("1. Select Blast Furnace", ['BF1', 'BF2', 'BF3', 'BF4', 'BF5'])
#     production = st.number_input("2. Enter Production (tons)", min_value=0.0, value=100.0)
#     shutdown_hours = st.number_input("3. Shut Down Hours", min_value=0.0, value=4.0)
#     ramp_up_time = st.time_input("4. Ramp Up Start Time")
#     enrichment_time = st.time_input("5. O₂ Enrichment Start Time (5 min steps)")
#     o2_enrichment_pct = st.slider("6. O₂ Enrichment Percentage", min_value=1.0, max_value=10.0, value=5.0, step = 0.05)
#     tapping_time = st.time_input("7. Tapping Time (after ramp up)")
#     submitted = st.form_submit_button("🚀 Start Process")

with st.form("start_up_form"):
    # Create two columns
    col1, col2 = st.columns(2)

    # Left column
    with col1:
        selected_furnace = st.selectbox("1. Select Blast Furnace", ['BF1', 'BF2', 'BF3', 'BF4', 'BF5'])
        production = st.number_input("2. Enter Production (tons)", min_value=0.0, value=100.0)
        shutdown_hours = st.number_input("3. Shut Down Hours", min_value=0.0, value=4.0)
        ramp_up_time = st.time_input("4. Ramp Up Start Time")

    # Right column
    with col2:
        enrichment_time = st.time_input("5. O₂ Enrichment Start Time (5 min steps)")
        o2_enrichment_pct = st.slider("6. O₂ Enrichment Percentage", min_value=1.0, max_value=10.0, value=5.0, step=0.05)
        tapping_time = st.time_input("7. Tapping Time (after ramp up)")

    # Submit button below columns
    submitted = st.form_submit_button("🚀 Start Process")



if submitted:
    inputs = {
    "Furnace": selected_furnace,
    "Production": production,
    "Shutdown Hours": shutdown_hours,
    "Ramp Up Time": ramp_up_time,
    "O₂ Enrichment Time": enrichment_time,
    "O₂ Enrichment %": o2_enrichment_pct,
    "Tapping Time": tapping_time
    }

    st.subheader("📋 Submitted")


    # ... your logic and graph after this
    st.header(inputs['Furnace'])

    ## OPERATION
    on_blast_taken = inputs["Ramp Up Time"]
    
    ###------------- Extra Coke table ------------------
    extra_coke = wind_startup
    extra_coke['Ramp Up time'] = on_blast_taken
    
    ramp_up = []
    for i in range(len(startup_mins)):
        ramp_up.append(
            datetime.combine(datetime.today(), wind_startup.loc[i, 'Ramp Up time'])  + timedelta(minutes = startup_mins[i])
        )
        
    extra_coke['ramp up'] = ramp_up
    extra_coke['BF1'] = extra_coke['BF1']*60
    extra_coke['BF2'] = extra_coke['BF2']*60
    extra_coke['BF3'] = extra_coke['BF3']*60
    extra_coke['BF4'] = extra_coke['BF4']*60
    extra_coke['BF5'] = extra_coke['BF5']*60
    
    ###-------------------------------------------- Extra Coke table End ----------------------------------------------------------------------
    ###-------------------------------------------- Extra Coke table End ----------------------------------------------------------------------
    ###-------------------------------------------- Extra Coke table End ----------------------------------------------------------------------


    
    ## ---------------------------------------------- HM melting table ------------------------------------------------------------
    ## ---------------------------------------------- HM melting table ------------------------------------------------------------
    ## ---------------------------------------------- HM melting table ------------------------------------------------------------
    
    # HM table Calculation
    
    hm_time = extra_coke['ramp up'].dt.time.to_list()
    o2_time = inputs['O₂ Enrichment Time']
    wind_vol = extra_coke[inputs['Furnace']].to_list()
    
    hm = []
    n = len(wind_vol)
    
    for i in range(n):
        hm.append((((wind_vol[i]*0.21) + (wind_vol[i] * inputs['O₂ Enrichment %']/100))/320)/12 if (hm_time[i] >= o2_time) else (wind_vol[i]*0.21/320)/12)
    
    
    hm_cum = []
    for i in range(n):
        if i == 0:
            hm_cum.append(hm[i])
        else:
            hm_cum.append(hm[i]+hm_cum[i-1])
    
    
    hm_table = pd.DataFrame({
        "Time" : hm_time,
        "HM Accumulated" : hm_cum
    })
    
    # st.write(hm_table)
    
    
    ## ------------------------------------------------------- HM table End -------------------------------------------------------------------
    ## ------------------------------------------------------- HM table End -------------------------------------------------------------------
    ## ------------------------------------------------------- HM table End -------------------------------------------------------------------
    
    
    ## ------------ Plots ---------------------
    # ---------------------------- Graph 1--------------------------------------------
    st.title("Time vs Volume Line Plot")
        
        # Plotly line chart1
    fig = px.line(extra_coke, x='ramp up', y=inputs['Furnace'], markers=True,
                    title="Volume Over Time",
                    labels={'ramp up': 'Time', inputs['Furnace']: 'Volume'})

    # Customize layout for grid
    fig.update_layout(
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        hovermode="x unified"
    )

    # Display the plot
    st.plotly_chart(fig, use_container_width=True) 
        
    
    # --------------------- Graph 2 --------------------------------------
    st.title("Time vs Hot Metal Accumulated Plot")
        # Plotly line chart2
    fig1 = px.line(hm_table, x='Time', y='HM Accumulated', markers=True,
                title="Hot Metal Over Time",
                    labels={'Time': 'Time', 'HM Accumulated': 'Hot Metal Accumulated'})

        # Customize layout for grid
    fig1.update_layout(
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
            hovermode="x unified"
    )

        # Display the plot
    st.plotly_chart(fig1, use_container_width=True)        
    
    # ------------------------------------ End Graphs -----------------------------------------
    # ------------------------------------ End Graphs -----------------------------------------
    # ------------------------------------ End Graphs -----------------------------------------
    
    blast_27_percent = datetime.combine(datetime.today(), on_blast_taken) + timedelta(minutes=30)
    blast_55_percent = datetime.combine(datetime.today(), on_blast_taken) + timedelta(minutes=80)

    # # (Optional) Extract back just the time if needed
    # blast_27_percent_time = blast_27_percent.time()
    # blast_55_percent_time = blast_55_percent.time()  
    

    targeted_volume_reached = datetime.combine(datetime.today(), on_blast_taken) + timedelta(hours=3, minutes=30)
    normalized = datetime.combine(datetime.today(), on_blast_taken) + timedelta(hours=1, minutes=30)
    gcp_connection = blast_27_percent
    o2_enrichment_time = inputs["O₂ Enrichment Time"]
    o2_enrich_percent = inputs["O₂ Enrichment %"]
    tapping_time1 = datetime.today()
    actual_tapping_time = inputs["Tapping Time"]
    hot_metal_accum = 0
    hm_index = 0
    slag_rate = 390
    

    
    for index, row in hm_table.iterrows():
        if row['HM Accumulated'] > 150:
            tapping_time1 = row['Time']
            hm_index = index
            break
            
    hot_metal_accum = hm_table.loc[hm_index, 'HM Accumulated']
    
    # st.write(extra_coke)
    # st.header('BF Operation')
    
    # Create the data
    steps = [
        {
            "Operation": "On Blast taken",
            "Blast Volume (Nm³/min)": 0,
            "Time (HH:MM)":  f"{on_blast_taken.hour}:{on_blast_taken.minute:02d}"
        },
        {
            "Operation": "Increase the volume at 100 Nm³/min",
            "Blast Volume (Nm³/min)": 100,
            "Time (HH:MM)": ""
        },
        {
            "Operation": "Blast Reaches 27% Connect GCP, Close bleeder, Start Charging",
            "Blast Volume (Nm³/min)": extra_coke[inputs['Furnace']].to_list()[6]/60 ,
            "Time (HH:MM)": f"{blast_27_percent.hour}:{blast_27_percent.minute:02d}"
        },
        {
            "Operation": "55% Target Volume: wait for burden descent, begin tapping, initiate PCI and O2 Enrich",
            "Blast Volume (Nm³/min)": extra_coke[inputs['Furnace']].to_list()[16]/60,
            "Time (HH:MM)": f"{blast_55_percent.hour}:{blast_55_percent.minute:02d}"
        },
        {
            "Operation": "Blast volume by 50 Nm³/min until 90% of the targeted volume",
            "Blast Volume (Nm³/min)": "",
            "Time (HH:MM)": ""
        },
        {
            "Operation": "Reached the targeted Volume",
            "Blast Volume (Nm³/min)": extra_coke[inputs['Furnace']].to_list()[-1]/60,
            "Time (HH:MM)": f"{targeted_volume_reached.hour}:{targeted_volume_reached.minute:02d}"
        }
    ]

    # Convert to DataFrame
    df = pd.DataFrame(steps)

    # Streamlit App
    st.title("📋 Blast Furnace Blowing Steps")

    st.table(df)
    
    st.metric("Furnace Normalised", normalized.strftime("%H:%M"))
    

    
    


    
    
    




