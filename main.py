import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
from datetime import datetime, timedelta

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

with st.form("start_up_form"):
    selected_furnace = st.selectbox("1. Select Blast Furnace", ['BF1', 'BF2', 'BF3', 'BF4', 'BF5'])
    production = st.number_input("2. Enter Production (tons)", min_value=0.0, value=100.0)
    shutdown_hours = st.number_input("3. Shut Down Hours", min_value=0.0, value=4.0)
    ramp_up_time = st.time_input("4. Ramp Up Start Time")
    enrichment_time = st.time_input("5. O₂ Enrichment Start Time (5 min steps)")
    o2_enrichment_pct = st.slider("6. O₂ Enrichment Percentage", min_value=1.0, max_value=10.0, value=5.0, step = 0.05)
    tapping_time = st.time_input("7. Tapping Time (after ramp up)")
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

    st.subheader("📋 Submitted Input Summary")
    # st.json(inputs)    


        # ... your logic and graph after this
    st.header(inputs['Furnace'])

    ## OPERATION
    on_blast_taken = inputs["Ramp Up Time"]

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
    # tapping_time = 
    actual_tapping_time = inputs["Tapping Time"]
    # hot_metal_accum = 
    slag_rate = 390
    
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
    
    # st.write(extra_coke)
    ## ------------- Extra Coke Table end ------------------
    
    ## ------------ Plots ---------------------
    st.title("Time vs Volume Line Plot")
    
    # Plotly line chart
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
    
    
    




