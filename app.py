import streamlit as st
from explainer import get_root_cause 

st.title("Server Health Dashboard")

# The Box to Paste Errors
user_input = st.text_area("Paste the Error Log here:")

# The Button
if st.button("Analyze Error"):
    answer = get_root_cause(user_input)
    st.write("### Root Cause Analysis:")
    st.success(answer)