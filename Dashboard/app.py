import streamlit as st
import os
import json
import subprocess
import re

BASE_PATH = "outputs/accounts"

st.set_page_config(page_title="Clara Agent Pipeline", layout="wide", initial_sidebar_state="collapsed")

# Inject Custom CSS for Premium Look
st.markdown("""
<style>
    /* Base typography & container tweaks */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        border-bottom: 1px solid rgba(128, 128, 128, 0.2);
    }
    .stTabs [data-baseweb="tab"] {
        padding-top: 1rem;
        padding-bottom: 1rem;
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    /* Soft shadows for generic containers */
    div[data-testid="stExpander"] {
        border-radius: 0.5rem;
        border: 1px solid rgba(128, 128, 128, 0.2);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    /* Header typography */
    h1 {
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    h2, h3 {
        font-weight: 600 !important;
        letter-spacing: -0.01em;
    }
</style>
""", unsafe_allow_html=True)

st.title("Clara Agent Configuration System")
st.markdown("Monitor and manage your automation pipeline configurations across multiple accounts.")
st.divider()

tab1, tab2, tab3 = st.tabs(["Dashboard Overview", "Configuration Diff Viewer", "Pipeline Control"])

# -----------------------------
# TAB 1: DASHBOARD
# -----------------------------

with tab1:
    st.header("Accounts Overview")
    
    if not os.path.exists(BASE_PATH):
        st.warning("No accounts found. Run the pipeline first to generate data.")
    else:
        accounts = os.listdir(BASE_PATH)
        
        # Summary Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Accounts", len(accounts))
        # Count processed versions simply by checking if v2 exists
        processed_count = sum(1 for acc in accounts if os.path.exists(os.path.join(BASE_PATH, acc, "v2")))
        col2.metric("Processed (v2 Available)", processed_count)
        col3.metric("System Status", "Active")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        for account in accounts:
            account_path = os.path.join(BASE_PATH, account)
            v1_path = os.path.join(account_path, "v1", "memo.json")
            v2_path = os.path.join(account_path, "v2", "memo.json")

            with st.expander(f"Account Details: {account}", expanded=False):
                col_v1, col_v2 = st.columns(2)

                if os.path.exists(v1_path):
                    with open(v1_path) as f:
                        memo_v1 = json.load(f)

                    with col_v1:
                        st.markdown("### Version 1 Record")
                        st.markdown(f"**Company Identity:** {memo_v1.get('company_name', 'N/A')}")
                        st.markdown(f"**Services Supported:** {memo_v1.get('services_supported', 'N/A')}")
                        st.markdown(f"**Business Hours:** {memo_v1.get('business_hours', 'N/A')}")

                if os.path.exists(v2_path):
                    with open(v2_path) as f:
                        memo_v2 = json.load(f)

                    with col_v2:
                        st.markdown("### Version 2 Record")
                        st.markdown(f"**Updated Business Hours:** {memo_v2.get('business_hours', 'N/A')}")
                        # Could add more dynamically if v2 contains them
                        for k, v in memo_v2.items():
                            if k not in ['business_hours']:
                                st.markdown(f"**{str(k).replace('_', ' ').title()}:** {v}")

# -----------------------------
# TAB 2: DIFF VIEWER
# -----------------------------

with tab2:
    st.header("Configuration Changes Analysis")

    if not os.path.exists(BASE_PATH):
        st.info("System idle. No data available for analysis.")
    else:
        accounts = [acc for acc in os.listdir(BASE_PATH) if os.path.isdir(os.path.join(BASE_PATH, acc))]

        if not accounts:
            st.info("No account directories available.")
        else:
            selected_account = st.selectbox("Select Account for Diff Analysis", accounts)
            change_file = os.path.join(BASE_PATH, selected_account, "changes.json")

            if os.path.exists(change_file):
                with open(change_file) as f:
                    changes_data = json.load(f)
                
                st.subheader("Detected Alterations structure: v1 to v2")
                
                # Format data for a nice dataframe presentation
                table_data = []
                for change in changes_data.get("changes", []):
                    table_data.append({
                        "Field Changed": str(change.get("field", "")).replace("_", " ").title(),
                        "Previous Value": str(change.get("old_value", "")),
                        "Current Value": str(change.get("new_value", ""))
                    })
                
                if table_data:
                    st.dataframe(table_data, use_container_width=True, hide_index=True)
                else:
                    st.success("No critical field alterations detected in this cycle.")
            else:
                st.info("Diff log not found for the selected account.")

# -----------------------------
# TAB 3: PIPELINE CONTROL
# -----------------------------

with tab3:
    st.header("Pipeline Execution Center")
    st.write("Initialize and run the primary automation sequence directly from the dashboard engine.")
    
    col_btn, col_status = st.columns([1, 4])
    
    with col_btn:
        run_trigger = st.button("Initialize Pipeline", type="primary", use_container_width=True)

    if run_trigger:
        with st.status("Executing system processes...", expanded=True) as status:
            st.write("Initializing standard runtime...")
            
            try:
                result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
                
                if result.returncode == 0:
                    status.update(label="Pipeline execution completed successfully.", state="complete", expanded=False)
                    st.success("The pipeline has successfully processed all files. Review the summary below.")
                    
                    # Parse the output for the summary
                    out_text = result.stdout
                    summary_start = out_text.find("PIPELINE SUMMARY")
                    
                    if summary_start != -1:
                        # Extract metrics using regex
                        demo_calls = re.search(r"Demo Calls Processed:\s+(\d+)", out_text)
                        onboarding_calls = re.search(r"Onboarding Calls Processed:\s+(\d+)", out_text)
                        accounts_created = re.search(r"Accounts Created:\s+(\d+)", out_text)
                        agents_generated = re.search(r"Agent Specs Generated:\s+(\d+)", out_text)
                        
                        st.markdown("### Execution Summary")
                        sc1, sc2, sc3, sc4 = st.columns(4)
                        if demo_calls:
                            sc1.metric("Demo Calls", demo_calls.group(1))
                        if onboarding_calls:
                            sc2.metric("Onboarding Calls", onboarding_calls.group(1))
                        if accounts_created:
                            sc3.metric("Accounts Created", accounts_created.group(1))
                        if agents_generated:
                            sc4.metric("Agent Specs", agents_generated.group(1))
                    else:
                        st.info("Execution completed but summary metrics could not be parsed.")
                            
                    with st.expander("View Detailed Execution Logs"):
                        st.code(result.stdout, language="text")
                        
                else:
                    status.update(label="Pipeline execution finished with internal errors.", state="error", expanded=True)
                    st.error("Runtime emitted warnings or errors:")
                    st.code(result.stderr, language="text")
                    with st.expander("View Partial Output Logs"):
                        st.code(result.stdout, language="text")
            except Exception as e:
                status.update(label="System initialization failed.", state="error", expanded=True)
                st.error(f"Failed to launch subprocess: {str(e)}")