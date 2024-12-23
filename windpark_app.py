#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
from plotly.subplots import make_subplots
from shapely.wkt import loads
import pandas as pd
import geopandas as gpd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import altair as alt


df=pd.read_csv('https://raw.githubusercontent.com/ValeriaMalin/Fun_Project_German_WindParks_Folium/main/Datasets/onshores_windparks.csv', delimiter=';'
offshores=pd.read_csv('https://raw.githubusercontent.com/ValeriaMalin/Fun_Project_German_WindParks_Folium/main/Datasets/Offshores_windparks.csv', delimiter=';'
data_l=pd.read_csv('https://raw.githubusercontent.com/ValeriaMalin/Fun_Project_German_WindParks_Folium/main/Datasets/geo_landkreis_windparks.csv', delimiter=';'
data_b=pd.read_csv('https://raw.githubusercontent.com/ValeriaMalin/Fun_Project_German_WindParks_Folium/main/Datasets/geo_bundesland_windparks.csv', delimiter=';'

# Set page configuration
st.set_page_config(
    page_title="Wind Energy Dashboard",
    page_icon="💨",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Inject custom CSS for additional styling
st.markdown(
    """
    <style>
    /* General page background */
    .block-container {
        background-color: #121212 !important;  /* Dark background */
        color: white !important;  /* White text */
    }

    /* Sidebar background and text */
    .css-1d391kg, .css-1lcbmhc {
        background-color: #121212 !important;  /* Dark sidebar */
        color: white !important;  /* White text */
    }
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #2f2f2f; /* Slightly lighter dark background */
        color: #fafafa; /* White text */
    }

    /* Headers, subheaders, and other text elements */
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: white !important;
    }

    /* Metrics styling */
    .stMetric-value, .stMetric-label {
        color: white !important;
    }

    /* Expander header and content */
    .streamlit-expanderHeader {
        color: white !important;
    }

    .streamlit-expanderContent {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Wind energy  in Germany in 2024 - Onshore and offshore turbines dashboard")
st.sidebar.title("About")
st.sidebar.info("""
This dashboard provides insights into wind energy projects across Germany, focusing on offshore and onshore wind parks.
You can explore:
- Distribution of wind parks by region and sea location.
- Trends in turbine capacity and commissioning over the years.
- Key manufacturers and their contributions to wind energy development.

The data aims to support policymakers, researchers, and enthusiasts in understanding the state of wind energy in Germany.
""")

pages=["Onshore Windcrafts", "Offshores Windcrafts"]
page=st.sidebar.radio("Windparks in Germany", pages)

# Calculate the metrics
unique_parks = df.drop_duplicates(subset='Name_x')  # Replace 'park_name' with the correct column
in_betrieb = offshores.loc[offshores['Status']=='in Betrieb']
total_turbines = df['count'].sum() + in_betrieb['AnzahlWKAs'].sum()
total_capacity = unique_parks['Gesamtleistung (MW)'].sum() + in_betrieb['Leistung(MW)'].sum()

# Assuming you have static data for total renewable capacity (or fetch dynamically)
total_renewable_energy = 285000000  #  MW
wind_production = 141000000 #  MW data
wind_contribution = (wind_production / total_renewable_energy) * 100
total_energy = (4.8+22.5+285.2+79.0+77+26.4)*1000000   #Data are from https://www.cleanenergywire.org/factsheets/germanys-energy-consumption-and-power-mix-charts

# Display metrics on the sidebar
st.sidebar.metric("Total Turbines", f"{total_turbines:,}")
st.sidebar.metric("Installed Capacity", f"{total_capacity:,.1f} MW")
st.sidebar.subheader("""Germany produced 285.0  TW of renewable energy in 2024""")
st.sidebar.metric("Wind Contribution in renewal energy", f"{wind_contribution:.2f}%")
st.sidebar.subheader("""Total energy production in Germany in 2024 is 585.0 TW""")
st.sidebar.metric("Wind Contribution in total energy:", f"{(wind_production/total_energy)*100:.2f}%")
st.sidebar.subheader("Data Sources:")
st.sidebar.write("""
- [Source 1: Bundesnetzagentur](https://www.bundesnetzagentur.de)
- [Source 2: Renewable Energy Database](https://example-renewables.org)
- [Source 3: Clean Energy Wire - Germany's Energy Consumption and Power Mix Charts](https://www.cleanenergywire.org/factsheets/germanys-energy-consumption-and-power-mix-charts)
- [Source 4: Wikipedia - List of Wind Turbines in Germany](https://de.wikipedia.org/wiki/Liste_von_Windkraftanlagen_in_Deutschland)
""")

if page == pages[0]:
 col1, col2, col3 = st.columns(3)
 with col1:
    #st.title("Onshore Turbines Dashboard")
  
    # 1 Plot - cumulative numbers and capacity
    # Group data by year and calculate cumulative sums
    growth_data = unique_parks.groupby('Anfangjahr').agg({
       'Anzahl': 'sum',   # Total number of turbines per year
       'Gesamtleistung (MW)': 'sum' #Total sum of capacity (Gesamtleistung (MW))
       }).sort_index()

    # Calculate cumulative sums
    growth_data['cumulative_turbines'] = growth_data['Anzahl'].cumsum()
    growth_data['cumulative_capacity_MW'] = growth_data['Gesamtleistung (MW)'].cumsum()
    st.subheader("Cumulative growth of onshore wind energy in Germany")

    # Plot cumulative growth
    fig1 = px.line(
       growth_data,
       x=growth_data.index,
       y=['cumulative_turbines', 'cumulative_capacity_MW'],
       labels={'value': 'Cumulative Total', 'variable': 'Metric', 'Anfangjahr': 'Year'},
       markers=True
       )
    fig1.update_layout(
       plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
       paper_bgcolor='rgba(0,0,0,0)', 
       width=900, height=400,
       xaxis=dict(
              title=dict(text='Year', font=dict(size=16, color='white')),
              tickfont=dict(color='white')),
       yaxis=dict(
               title=dict(text='Cumulative Total', font=dict(size=16, color='white')),
               tickfont=dict(color='white')),
       legend_title=dict(font=dict(color='white')),         
       legend=dict(font=dict(color='white'))
                       )

    # Display the plot
    st.plotly_chart(fig1, use_container_width=True)

    # 2 Plot - geo - bundesland
    # Apply fix for invalid geometries
 
    data_b['geometry'] = data_b['geometry'].apply(loads)
    geo_b=gpd.GeoDataFrame(data_b, geometry='geometry')
    st.subheader("Distribution of onshore wind turbines across the regions")

    # Plot the map
    fig2= px.choropleth(data_b,
                        geojson=geo_b,
                        locations="NUTS_ID",
                        color="Anzahl",
                        color_continuous_scale="PuBuGn",
                        range_color=(data_b["Anzahl"].min(), data_b["Anzahl"].max()),
                        labels={"Anzahl": "The number is", "NUTS_NAME": "Region"},  # Adjust labels
                        featureidkey="properties.NUTS_ID",
                        width=600,  # Adjusted width
                        height=600,  # Adjusted height
                        hover_name="NUTS_NAME",  # This ensures NUTS_NAME is displayed on hover
                        hover_data={"NUTS_NAME": True, "Anzahl": True}  # Show both NUTS_NAME and Anzahl
                    )
 

    # Update geos for zooming in on Germany
    fig2.update_geos(
       center={"lat": 51.3657, "lon": 10.4515},  # Coordinates for Germany's center
       projection_type="mercator",  # Mercator projection for zoom control
       visible=False,  # Hide gridlines
       projection_scale=29)  # Adjust zoom level
 
    # Set a new background color
    fig2.update_layout(
       template='plotly_dark',
       paper_bgcolor="rgba(0, 0, 0, 0)",  # Transparent figure background
       plot_bgcolor="rgba(0, 0, 0, 0)",   # Transparent plot background
       margin={"r": 0, "t": 0, "l": 0, "b": 0}  # Remove extra margins
    )
    fig2.show()

   # Display the map
    st.plotly_chart(fig2, use_container_width=True)

    #3 Plot - Cumulative capacity dynamic across the regions

    def plot_cumulative_power(unique_parks):
    # Group by year and Bundesland, then sum the turbine power
        df_cumulative = (
           unique_parks.groupby(['Anfangjahr', 'NUTS 1.1'])['Gesamtleistung (MW)']
           .sum()
           .groupby(level=1)
           .cumsum()
           .reset_index())
    
    # Rename columns for better understanding
        df_cumulative.rename(
           columns={'Gesamtleistung (MW)': 'Cumulative Power (MW)', 'NUTS 1.1': 'Bundesland'},inplace=True)
    
    # Create a line plot with animation over time
        fig3 = px.line(
           df_cumulative,
           x='Anfangjahr',  # Year on x-axis
           y='Cumulative Power (MW)',  # Cumulative power on y-axis
           color='Bundesland',  # Different lines for each Bundesland
           title='Cumulative Turbine Power Over Time by Bundesland',
           labels={'Anfangjahr': 'Year', 'Cumulative Power (MW)': 'Cumulative Turbine Power (MW)'},
           height=600
        )
    
    # Customize the layout to match Streamlit's dark mode styling
        fig3.update_layout(
           plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
           paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
           font=dict(color='white'),  # White font for text
           title_font=dict(size=20, color='white'),  # Title font styling
           xaxis=dict(
              title=dict(text='Year', font=dict(size=16, color='white')),
              tickfont=dict(color='white')),
            yaxis=dict(
               title=dict(text='Cumulative Turbine Power (MW)', font=dict(size=16, color='white')),
               tickfont=dict(color='white')),
            legend_title=dict(font=dict(color='white')),  
            legend=dict(font=dict(color='white'))  # White font for legend
        )
    
       # Display the plot using Streamlit
        st.plotly_chart(fig3, use_container_width=True)
    plot_cumulative_power(unique_parks)

    # Plot 4 - Top Manufacturers by Bundesland
    def plot_top_10_manufacturers_by_count():
       # Count turbines by Bundesland and Manufacturer
       df_manufacturer_count = (
          df.groupby(['NUTS 1.1', 'Manufacturer'])
         .size()
         .reset_index(name='Turbine Count')
         .sort_values('Manufacturer', ascending=True)
        )

       # Sort within each Bundesland to get the top 10 manufacturers
       df_manufacturer_count = (
          df_manufacturer_count.sort_values(['NUTS 1.1', 'Turbine Count'], ascending=[True, False])
          .groupby('NUTS 1.1')
          .head(10)
          )

       # Now, let's sort the Bundesländer by total turbine count (sum of turbines per region)
       df_bundesland_totals = (
          df_manufacturer_count.groupby('NUTS 1.1')['Turbine Count']
          .sum()
          .reset_index()
          .sort_values('Turbine Count', ascending=False)  # Sort by total turbine count
          )

       # Merge this sorted order back to the top 10 dataframe
       df_top_10_sorted = df_manufacturer_count.merge(
          df_bundesland_totals[['NUTS 1.1', 'Turbine Count']],
          on='NUTS 1.1',
          suffixes=('', '_total')
        )
    
       # Sort df_top_10 by the total turbines in each Bundesland
       df_top_10_sorted = df_top_10_sorted.sort_values(['Turbine Count_total','Manufacturer'], ascending=[False, True])

        # Create a bar plot
       fig4 = px.bar(
          df_top_10_sorted,
          x='NUTS 1.1',
          y='Turbine Count',
          color='Manufacturer',
          title='Top 10 Manufacturers by Turbine Count in Each Region',
          labels={'NUTS 1.1': 'Bundesland', 'Turbine Count': 'Number of Turbines'},
          height=600
        )
        # Update layout for Streamlit styling
       fig4.update_layout(
          xaxis_tickangle=-45,  # Rotate x-axis labels
          xaxis=dict(
             title=dict(text='Bundesland', font=dict(size=16, color='white')),
             tickfont=dict(color='white')
            ),
          yaxis=dict(
             title=dict(text='Number of Turbines', font=dict(size=16, color='white')),
             tickfont=dict(color='white')
            ),
          legend_title=dict(font=dict(color='white')),  
          legend=dict(font=dict(color='white')),
          plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
          paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for Streamlit
          font=dict(color='white'),
          title_font=dict(size=20, color='white')
        )
       # Show the plot
       return fig4 

    fig4= plot_top_10_manufacturers_by_count()
    st.plotly_chart(fig4, use_container_width=True)


 with col2:
     st.subheader("""The most modern trubines""")

     with st.expander("Modern wind turbine: overview and types:"):
       st.write("""
                Modern wind turbines are advanced machines designed to convert wind energy into electricity efficiently. They feature cutting-edge technology to maximize energy output and adapt to various wind conditions. Below are some of the most advanced models and their characteristics:

Latest Wind Turbine Models

- Nordex N163/6800: High-rated capacity (6.8 MW), ideal for large-scale energy production.
- Vestas V162-7.2MW: Among the most powerful, with exceptional efficiency.
- Enercon E-175 EP5: Large rotor diameter and high efficiency.
- Siemens Gamesa SG 6.6-170: Compact design for space-limited wind parks.
- GE 5.5-158: Advanced technology delivering high energy yield.
- Enercon E-160 EP5 E3: Optimized for low to medium wind speeds.
- eno160-6.0MW: Offshore turbine with high capacity.
- Vestas V172-7.2MW: Latest generation with maximum energy yield.
                
Other Advanced Models by Manufacturer:

Siemens Gamesa:
- SG 5.0-145: 5 MW, optimized for low-medium wind speeds.
- SG 4.7-155: 4.7 MW, efficient in medium wind conditions.
Vestas:
- V150-4.2 MW: Suitable for weaker wind regions.
- V162-6.2 MW EnVentus: Modular platform, high efficiency.
Nordex:
- N149/4.X: Flexible for varying wind speeds.
- N163/5.X: Great for low-medium wind speeds.
GE Renewable Energy:
- Cypress 5.3-158: Modular design, ideal for weaker wind locations.
- Cypress 4.8-158: Compact and efficient.

These turbines represent the pinnacle of wind energy technology, offering flexibility and efficiency across various environments.
        """)
    # Calculate the proportion of modern turbines
    # Filter modern turbines
     modern_types = df.loc[df['is_modern'] == True]

    # Total turbines: sum of 'count' column in the entire dataframe
     total_turbines = df['count'].sum()  # Corrected with parentheses

    # Modern turbines: sum of 'count' column in the modern turbines subset
     modern_turbines_count = modern_types['count'].sum()  # Corrected with parentheses

    # Calculate the proportion of modern turbines
     proportion_modern = (modern_turbines_count / total_turbines) * 100  # Calculate proportion

    # Display the metric
     st.metric(
       label="Proportion of Modern Turbines",
       value=f"{proportion_modern:.2f}%",
       delta=f"{modern_turbines_count} / {total_turbines} Turbines"
       )

    #5 Plot - The most modern turbines by Bundeslander
    # Filter the DataFrame to include only modern turbine types
     modern_turbines = df.loc[df['is_modern']==True]

    # Group by Bundesland and turbine type, and count occurrences
     bundesland_turbine_counts = (
       modern_turbines.groupby(['NUTS 1.1', 'type'])
       .size()
       .reset_index(name='Count')
     )
     modern_turbines.groupby(['NUTS 1.1', 'type']).size().reset_index(name='Count')

    # Find the top 15 turbines for each Bundesland
     top_15_by_bundesland = (
       bundesland_turbine_counts.groupby('NUTS 1.1', group_keys=False)
       .apply(lambda group: group.nlargest(15, 'Count'))  # Get the top 15 for each Bundesland
       .reset_index(drop=True).sort_values('Count', ascending=False)
     )

    # Visualization
     fig5 = px.bar(
       top_15_by_bundesland,
       x='NUTS 1.1',
       y='Count',
       color='type',
       title='Top 15 modern turbines across the regions',
       labels={'NUTS 1.1': 'Bundesland', 'type': 'Modern Turbine Type', 'Count': 'Number of Turbines'},
       height=700
       )

     # Customize the layout to match the app style
     fig5.update_layout(
       barmode='stack', 
       xaxis_tickangle=-45,  # Rotate x-axis labels
       xaxis=dict(
          title=dict(text='Bundesland', font=dict(size=16, color='white')),  # Add x-axis label
          tickfont=dict(color='white')  # Styling for tick label
          ),
       yaxis=dict(
          title=dict(text='Number of turbines', font=dict(size=16, color='white')),  # Add y-axis label
          tickfont=dict(color='white')  # Styling for tick labels
          ),
       plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
       paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper
       font=dict(color='white'),  # White font to match dark mode
       title_font=dict(size=20, color='white'),
       legend=dict(font=dict(color='white')),   # Title font styling
       legend_title=dict(font=dict(size=14, color='white')))  # Legend title styling
 
    # Display the plot in Streamlit
     st.plotly_chart(fig5, use_container_width=True)

    
    # 6 Plot - Manufacturers: 
     def plot_top_manufacturers_overall():
        # Count turbines by Manufacturer
        df_top_manufacturers_overall = (
           df['Manufacturer']
           .value_counts()
           .head(10)
           .reset_index()
           )

        # Create a bar plot
        fig_a = px.bar(
           df_top_manufacturers_overall,
           x='Manufacturer',
           y='count',
           title='Top 10 manufacturers overall',
           labels={'Turbine Count': 'Number of Turbines'},
           height=600
           )
    # Show the plot
        return fig_a
  
    # Function to plot top manufacturers for modern turbines
     def plot_top_manufacturers_overall_modern():
       # Count turbines by Manufacturer
       modern_types=df.loc[df['is_modern']==True]
       df_top_manufacturers_overall_modern = (
          modern_types['Manufacturer']
          .value_counts()
          .reset_index()
        )

       # Create a bar plot
       fig_b = px.bar(
          df_top_manufacturers_overall_modern,
          x='Manufacturer',
          y='count',
          title='Top 10 modern manufacturers overall',
          labels={'Manufacturer': 'Manufacturer'},
          height=600
          )
       
       return fig_b
     
    # Get the figures
     fig_a = plot_top_manufacturers_overall()
     fig_b = plot_top_manufacturers_overall_modern()

    # Combine the plots into subplots using `make_subplots`
     combined_fig = make_subplots(
       rows=1, cols=2,  # One row, two columns
       subplot_titles=('Top 10 manufacturers overall', 'Top 10 modern manufacturers')
       )
    # Add the first figure
     for trace in fig_a.data:
       combined_fig.add_trace(trace, row=1, col=1)

    # Add the second figure
     for trace in fig_b.data:
       combined_fig.add_trace(trace, row=1, col=2)

    # Update layout to match Streamlit's style
     combined_fig.update_layout(
       showlegend=False,
       title_text="Comparison of manufacturers",
       plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
       paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
       font=dict(color='white'),  # White font for text
       title_font=dict(size=20, color='white'),  # Title font styling
       height=600, width=1200,  # Adjusting size for better view)
       xaxis_tickangle=-45,
       xaxis2_tickangle=-45,

       xaxis=dict(
             title=dict(font=dict(size=16, color='white')),  # Add x-axis label
             tickfont=dict(color='white')  # Styling for tick label
            ),
       yaxis=dict(
             title=dict( font=dict(size=16, color='white')),  # Add y-axis label
             tickfont=dict(color='white')  # Styling for tick labels
            ),

        xaxis2=dict(
           title=dict(font=dict(size=16, color='white')),  # Add x-axis label for second subplot
           tickfont=dict(color='white')  # Styling for tick label
            ),
        yaxis2=dict(
           title=dict(font=dict(size=16, color='white')),  # Add y-axis label for second subplot
           tickfont=dict(color='white')  # Styling for tick labels
           ),
           )
       

    # Display the combined plot
     st.plotly_chart(combined_fig, use_container_width=True)

 with col3:
      st.subheader('Top 15 wind energy contributors by "Landkreises"')

     #7 Plot Top 15 contributors among landkreises
      top_regions = data_l.nlargest(15, 'Anzahl')  # Replace 'Anzahl' with energy capacity if available

     # Bar chart
      fig7 = px.bar(
        top_regions,
        x='NUTS_NAME',
        y='Anzahl',  # or energy capacity
        labels={'NUTS_NAME': 'Landkreis', 'Anzahl': 'Number of turbines'},
        color='Anzahl',
        color_continuous_scale='Blues',
        )
      
      fig7.update_layout(
          xaxis_tickangle=-45,  # Rotate x-axis labels
          xaxis=dict(
             title=dict(text='Landkreis', font=dict(size=16, color='white')),
             tickfont=dict(color='white')
            ),
          yaxis=dict(
             title=dict(text='Number of turbines', font=dict(size=16, color='white')),
             tickfont=dict(color='white')
            ),
          plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
          paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for Streamlit
          font=dict(color='white'),
          legend_title=dict(font=dict(color='white')),  
          legend=dict(font=dict(color='white'))
          
        )

      # Display the plot
      st.plotly_chart(fig7, use_container_width=True)
    
      #8 Plot - geo - landkreises

      data_l['geometry'] = data_l['geometry'].apply(loads)
      geo_l=gpd.GeoDataFrame(data_l, geometry='geometry')

      st.subheader("Distribution of wind turbine across the 'Landkreises'")
     # Plot the map
      fig8 = px.choropleth(data_l,
                         geojson=geo_l,
                         locations="NUTS_ID",
                         color="Anzahl",
                         color_continuous_scale="PuBuGn",
                         range_color=(data_l["Anzahl"].min(), data_l["Anzahl"].max()),
                         labels={"Anzahl": "The number of Turbines:", "NUTS_NAME": "Region"},  # Adjust labels
                         featureidkey="properties.NUTS_ID",
                         width=600,  # Adjusted width
                         height=600,  # Adjusted height
                         hover_name="NUTS_NAME",  # This ensures NUTS_NAME is displayed on hover
                         hover_data={"NUTS_NAME": True, "Anzahl": True}  # Show both NUTS_NAME and Anzahl
                        )
 

     # Update geos for zooming in on Germany
      fig8.update_geos(
       center={"lat": 51.3657, "lon": 10.4515},  # Coordinates for Germany's center
       projection_type="mercator",  # Mercator projection for zoom control
       visible=False,  # Hide gridlines
       projection_scale=29)  # Adjust zoom level
 
    # Set a new background color
      fig8.update_layout(
       template='plotly_dark', 
       paper_bgcolor="rgba(0, 0, 0, 0)",  # Transparent figure background
       plot_bgcolor="rgba(0, 0, 0, 0)",   # Transparent plot background
       margin={"r": 0, "t": 0, "l": 0, "b": 0}  # Remove extra margins
       )
      fig8.show()
    # Display the map
      st.plotly_chart(fig8, use_container_width=True)

    #9 Top 15 Windparks  Turbine Count

    # Calculate the top 15 wind parks by turbine count in Landkreises
      top_15_parks = (
         unique_parks.groupby(['Name_x', 'Landkreis'])['count']
        .sum().reset_index()
        .sort_values(by='count', ascending=False)
        .head(15)
        )
      # Create the bar plot using Plotly Express
      fig9 = px.bar(
         top_15_parks,
         x='count',
         y='Name_x',
         color='Landkreis',
      #   orientation='h',  # Horizontal bar chart
         title='Top 15 wind parks by turbine count',
         labels={'count': 'Number of turbines', 'Name_x': 'Wind park', 'Landkreis': 'Landkreis'},
         height=600
        )

      # Customize the layout to match the Streamlit theme
      fig9.update_layout(
         title_font=dict(size=20, color='white'),
         yaxis=dict(title='Wind park', tickfont=dict(size=12, color='white')),
         xaxis=dict(title='Number of turbines', tickfont=dict(size=12, color='white')),
         legend_title=dict(text='Landkreis'),
         plot_bgcolor='rgba(0,0,0,0)',
         paper_bgcolor='rgba(0,0,0,0)',
         font=dict(color='white')  # Adjust to Streamlit's dark mode
         )

       # Display the plot in Streamlit
      st.plotly_chart(fig9, use_container_width=True)

#Offshores Page
if page == pages[1] :
    col1, col2, col3 = st.columns(3)
    with col1:
       # Calculate metrics
       num_offshore_turbines = in_betrieb['AnzahlWKAs'].sum()
       num_onshore_turbines = df['count'].sum()
       capacity_offshore = in_betrieb['Leistung(MW)'].sum()
       capacity_onshore = unique_parks['Gesamtleistung (MW)'].sum()

       turbine_ratio = (num_offshore_turbines / num_onshore_turbines)*100
       capacity_ratio = (capacity_offshore / capacity_onshore)*100

       # Streamlit app structure
       st.subheader("Offshore Turbines")

       # Display metrics
       cola, colb = st.columns(2)
       with cola:
          st.metric("Turbines offshore/onshore ratio", f"{turbine_ratio:.2f}""%")
       with colb:
          st.metric("Capacity offshore/onshore ratio", f"{capacity_ratio:.2f}""%")

       # Create the figure with scattermapbox
       fig = go.Figure(go.Scattermapbox(
          lat=in_betrieb["Latitude_cor"], 
          lon=in_betrieb["Longitude_cor"],
          mode='markers+text',
          marker={'size': 9},
          text=in_betrieb["Name"],
          hoverinfo="text",
        ))

       # Update map layout
       fig.update_layout(
          title= ('Map of offshores parks'),
          title_font=dict(size=20, color='white'),
          mapbox_style="open-street-map",  # Map style
          mapbox_center={"lat": 54.5, "lon": 10.0},  # Center of the map
          mapbox_zoom=5,  # Zoom level
          plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
          paper_bgcolor='rgba(0,0,0,0)',  
          template='plotly_dark'
        #  title="Offshore Parks"
        )  

        # Display the map
       st.plotly_chart(fig, use_container_width=True)

       #4 Plot Distribution of Offshore WInd Parks by Sea Region

        # Count the number of wind parks in each sea region
       location_counts = in_betrieb['Location'].value_counts().reset_index()
       location_counts.columns = ['Sea Region', 'Number of wind parks']

       # Create the bar chart
       fig1 = px.bar(
          location_counts,
          x='Sea Region',
          y='Number of wind parks',
          title="Distribution of offshore wind parks by sea region",
          labels={'Sea Region': 'Sea region', 'Number of Wind Parks': 'Number of wind parks'},
          color='Sea Region',
          color_continuous_scale='bluered',
          height=500,
        )
       fig1.update_layout(
          title_font=dict(size=20, color='white'),
          plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
          paper_bgcolor='rgba(0,0,0,0)',
          xaxis=dict(
             title=dict(text='Sea', font=dict(size=16, color='white')),
             tickfont=dict(color='white')
            ),
          yaxis=dict(
             title=dict(text='Number of Wind Parks', font=dict(size=16, color='white')),
             tickfont=dict(color='white')
            ),
          legend_title=dict(text='Sea Region', font=dict(color='white')), 
          legend=dict(font=dict(color='white')),
       )

       # Add the chart to Streamlit
       st.plotly_chart(fig1, use_container_width=True)

    with col2:
        
        # 2 Plot Average capacity by Status
        # Group by status and calculate the mean capacity
       avg_capacity_by_status = offshores.groupby('Status')['Leistung(MW)'].mean().reset_index()

       # Create a bar chart using Plotly
       fig1 = px.bar(
          avg_capacity_by_status,
          x='Status',
          y='Leistung(MW)',
    #      title='Average Capacity of Offshore Wind Parks by Status',
          labels={'Status': 'Status', 'Leistung(MW)': 'Average Capacity (MW)'},
          color='Status',  # Color by status for distinction
        height=600
       )

       # Customize layout
       fig1.update_layout(
      #    title_font=dict(size=20, color='white'),
          plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
          paper_bgcolor='rgba(0,0,0,0)',
          xaxis=dict(
             title=dict(text='Status', font=dict(size=16, color='white')),
             tickfont=dict(color='white')
            ),
          yaxis=dict(
             title=dict(text='Average Capacity (MW)', font=dict(size=16, color='white')),
             tickfont=dict(color='white')
            ),
          legend_title=dict(text='Average Capacity (MW)', font=dict(color='white')), 
          legend=dict(font=dict(color='white')),
           )
          

        # Streamlit display
       st.subheader("Average capacity of offshore wind turbines by status")
       st.plotly_chart(fig1, use_container_width=True)

       #3 Plot status of Offshore Wind Parks
       # # Count statuses
       status_counts = offshores['Status'].value_counts()

       # Create a pie chart using Plotly
       fig2 = go.Figure(data=[go.Pie(
          labels=status_counts.index,
          values=status_counts.values,
          hole=0.4,  # For a donut-style chart
          textinfo='percent+label',
          marker=dict(colors=['#1f77b4', '#d62728', '#7f7f7f', '#e377c2'])  # Use a qualitative color palette
        )])

       # Customize layout
       fig2.update_layout(
          
          title_text='Status of offshore wind parks',
          title_font=dict(size=20, color='white'), 
          legend_title=dict(text='Average Capacity (MW)', font=dict(color='white')), 
          legend=dict(font=dict(color='white')),
          showlegend=True,
          paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper
          font=dict(color='white')  # White font for Streamlit dark mode
        )

       st.plotly_chart(fig2, use_container_width=True)

    with col3: 
       
       #5 Plot the Number of offshores parks by Manufacturer:

       # Streamlit subheader
       st.subheader("Number of offshore wind turbines by manufacturer ")

       # Count the number of wind parks by manufacturer
       manufacturer_counts = in_betrieb['Manufacturer'].value_counts().reset_index()
       manufacturer_counts.columns = ['Manufacturer', 'Number of Wind Parks']

       # Calculate the sum of turbines (Anzahl(WKA)) per manufacturer
       total_turbines_by_manufacturer = in_betrieb.groupby('Manufacturer')['AnzahlWKAs'].sum().sort_values(ascending=False)

       # Create the bar chart
       fig2 = px.bar(
          total_turbines_by_manufacturer,
          x=total_turbines_by_manufacturer.index,
          y=total_turbines_by_manufacturer.values,
          labels={'Manufacturer': 'Manufacturer', 'AnzahlWKAs': 'Number of Wind Parks'},
          color='AnzahlWKAs',
          color_continuous_scale='bluered',
          height=500
        )

        # Customize the layout for better readability
       fig2.update_layout(
          legend_title=dict(text='Number of wind parks', font=dict(color='white')), 
          legend=dict(font=dict(color='white')),
          showlegend=True,
          plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
          paper_bgcolor='rgba(0,0,0,0)',
          xaxis=dict(
             title=dict(text='Manufacturer', font=dict(size=16, color='white')),
             tickfont=dict(color='white')
            ),
          yaxis=dict(
             title=dict(text='Number of wind turbines', font=dict(size=16, color='white')),
             tickfont=dict(color='white')
            ),
          xaxis_tickangle=-45)

       # Add the chart to Streamlit
       st.plotly_chart(fig2, use_container_width=True)

       #6 Plot NUmber of the WInd Parks Commissioned by Year:
       # Count the number of wind parks per year
       year_counts = offshores['Anfangjahr'].value_counts().sort_index().reset_index()
       year_counts.columns = ['Year', 'Number of Wind Parks']

       # Create the bar chart
       fig3 = px.bar(
          year_counts,
          x='Year',
          y='Number of Wind Parks',
          title="Number of Wind Parks Commissioned by Year",
          labels={'Year': 'Year', 'Number of Wind Parks': 'Number of Wind Parks'},
          height=550,
          color_continuous_scale='#1f77b4'
       )

        # Customize the layout
       fig3.update_layout(
          title_font=dict(size=20, color='white'),
          plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
          paper_bgcolor='rgba(0,0,0,0)',
          xaxis=dict(
             title=dict(text='Year', font=dict(size=16, color='white')),
             tickfont=dict(color='white')
            ),
          yaxis=dict(
             title=dict(text='Number of wind parks', font=dict(size=16, color='white')),
             tickfont=dict(color='white')
            ),
          xaxis_tickangle=-45)
      

       # Add the chart to Streamlit
       st.plotly_chart(fig3, use_container_width=True)

    
 
    
    
