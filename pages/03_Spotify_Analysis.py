import streamlit as st
import pandas as pd

# The actual page content is executed here by Streamlit
st.title("🎧 Student C: Music Popularity Analysis")
st.markdown("---")

# Retrieve shared data from the Home page's session state
if 'student_data' not in st.session_state or st.session_state['student_data']['st3_df'].empty:
    st.warning("Data not loaded. Please ensure the main Home Page ran successfully and the data files exist.")
else:
    df = st.session_state['student_data']['st3_df']

    # --- Student Introductory Section ---
    st.header("1. Introduction and Project Goal")
    st.markdown("""
        **Data Description:** This dataset contains simulated **Spotify track metadata**, including popularity scores, duration, genre, and objective audio features like Danceability, Energy, and Valence (musical positivity).
        
        **Question:** Which **audio features** have the strongest correlation with a track's **Popularity**?
        
        **Interaction:** Use the selection box below to choose a feature for the X-axis (Danceability, Energy, or Valence). The scatter plot and correlation metric will update to show the relationship with Popularity.
    """)
    st.markdown("---")

    # --- Analysis Controls (Moved from Sidebar to Main Page) ---
    x_axis = st.selectbox(
        'Select X-Axis Feature to Compare with Popularity:',
        ['Danceability', 'Energy', 'Valence'],
        index=0 # Default to Danceability
    )
    
    # --- Analysis Content ---
    st.subheader(f"2. Popularity vs. {x_axis} by Genre")
    
    # Create an interactive scatter chart
    st.scatter_chart(
        df,
        x=x_axis,
        y='Popularity',
        color='Genre', # Use genre to color points
        size='Duration_ms', # Use duration to size points
    )
    
    st.caption(f"Scatter plot showing Popularity against {x_axis}, colored by Genre, with point size representing song duration.")

    # Show correlation
    correlation = df[[x_axis, 'Popularity']].corr().iloc[0, 1]
    st.metric(label=f"Correlation Coefficient ({x_axis} vs. Popularity)", value=f"{correlation:.3f}")