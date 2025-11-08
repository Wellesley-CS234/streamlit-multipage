import streamlit as st
import pandas as pd

# The actual page content is executed here by Streamlit
st.title("📚 Student B: Exam Results Analysis")
st.markdown("---")

# Retrieve shared data from the Home page's session state
if 'student_data' not in st.session_state or st.session_state['student_data']['st2_df'].empty:
    st.warning("Data not loaded. Please ensure the main Home Page ran successfully and the data files exist.")
else:
    df = st.session_state['student_data']['st2_df']

    # --- Student Introductory Section ---
    st.header("1. Introduction and Project Goal")
    st.markdown("""
        **Data Description:** This dataset contains **student exam results** across five different subjects, including numerical scores, letter grades (A-F), and a boolean pass/fail status.
        
        **Question:** What is the **distribution of scores and grades** across various subjects, and which subject shows the highest pass rate?
        
        **Interaction:** Use the multiselect box below to choose the subjects you want to include in the analysis. The pass rate and score chart will update instantly.
    """)
    st.markdown("---")

    # --- Analysis Controls (Moved from Sidebar to Main Page) ---
    subject_filter = st.multiselect(
        "Select Subjects to Analyze:", 
        df['Subject'].unique(),
        default=df['Subject'].unique()
    )
    
    filtered_df = df[df['Subject'].isin(subject_filter)]
    
    # --- Analysis Content ---
    if filtered_df.empty:
        st.info("No data found. Please ensure at least one subject is selected in the multiselect filter.")
    else:
        st.subheader("2. Score Distribution")
        # FIX: Using st.bar_chart on the score column to show distribution (like a simple histogram)
        st.bar_chart(filtered_df['Score'])
        
        col1, col2 = st.columns(2)
        
        # Pass Status Metric
        total_students = len(filtered_df)
        passed_students = filtered_df['Pass_Status'].sum()
        pass_rate = (passed_students / total_students) * 100 if total_students > 0 else 0
        
        with col1:
            st.metric(
                label="Overall Pass Rate (Selected Subjects)", 
                value=f"{pass_rate:.1f}%",
                delta=f"Passed: {passed_students} / Total: {total_students}"
            )

        with col2:
            with st.expander("View Grade Frequencies"):
                # Ensure grades are ordered correctly (A, B, C, D, F)
                grade_order = ['A', 'B', 'C', 'D', 'F']
                # Calculate counts, reindex to enforce order, fill missing with 0
                grade_counts = filtered_df['Grade'].value_counts().reindex(grade_order, fill_value=0)
                st.dataframe(grade_counts.to_frame(name="Count"), use_container_width=True)