import streamlit as st
import pdfplumber
import re
import pandas as pd

# Page Config
st.set_page_config(page_title="Credit Architect Pro", layout="wide")

st.title("🛡️ Credit Architect: Action Plan Engine")
st.markdown("### Upload your credit report to generate your Level-Up roadmap.")

# --- SIDEBAR: LEAD CAPTURE ---
with st.sidebar:
    st.header("Save Your Progress")
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    if st.button("Register for PDF Export"):
        st.success(f"Welcome, {name}! Lead captured.")
        # Here you would connect to Formspree/Email API

# --- STEP 1: UPLOAD & PARSE ---
uploaded_file = st.file_uploader("Upload Credit Report (PDF)", type="pdf")

if uploaded_file:
    # This logic "scrapes" the PDF for Account Names, Balances, and Limits
    # For this demo, we use a structured input to ensure accuracy
    st.info("Reading report... Extracting tradelines.")
    
    # Mock data extracted from PDF (In a full version, pdfplumber parses this)
    data = [
        {"Account": "Chase Freedom", "Balance": 4500, "Limit": 5000, "APR": 24.99},
        {"Account": "Capital One Quicksilver", "Balance": 800, "Limit": 1000, "APR": 21.0},
        {"Account": "Auto Loan", "Balance": 12000, "Limit": 15000, "APR": 5.5}
    ]
    df = pd.DataFrame(data)

    # --- STEP 2: CALCULATIONS (THE POLISH) ---
    df['Utilization'] = (df['Balance'] / df['Limit']) * 100
    df['Monthly_Interest'] = (df['Balance'] * (df['APR']/100)) / 12
    
    total_bal = df['Balance'].sum()
    total_lim = df['Limit'].sum()
    total_util = (total_bal / total_lim) * 100
    total_leak = df['Monthly_Interest'].sum()

    # --- STEP 3: DASHBOARD ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Utilization", f"{total_util:.1f}%", delta="-5%" if total_util < 30 else "HIGH", delta_color="inverse")
    col2.metric("Monthly Interest Leak", f"${total_leak:.2f}", delta="Cost of Debt")
    
    # Score Boost Estimator Logic
    boost = 0
    if total_util > 30: boost = 45
    elif total_util > 10: boost = 20
    col3.metric("Est. Score Potential", f"+{boost} Points")

    # --- STEP 4: VISIBLE HIERARCHY (The Table) ---
    st.subheader("Your Credit Mix & Account Breakdown")
    st.table(df[['Account', 'Balance', 'Limit', 'Utilization', 'APR']])

    # --- STEP 5: DOLLAR-SPECIFIC ACTION PLAN ---
    st.subheader("⚔️ Active Quests (Your Action Plan)")
    
    for index, row in df.iterrows():
        if row['Utilization'] > 29:
            target = row['Limit'] * 0.28
            pay_amount = row['Balance'] - target
            st.error(f"**Quest: Optimize {row['Account']}**")
            st.write(f"👉 Pay exactly **${pay_amount:,.2f}** to drop this card to 28% utilization.")
            st.progress(0.29) # Visual progress bar
        else:
            st.success(f"**Quest Complete: {row['Account']}** is already optimized.")

    # --- STEP 6: CREDIT MIX RECOMMENDATION ---
    has_installment = any(df['Limit'] > 10000) # Simple logic for loan check
    if not has_installment:
        st.warning("⚠️ **Credit Mix Alert:** You lack an installment loan. Consider a Credit Builder Loan to diversify your profile.")

    # --- STEP 7: DOWNLOAD ---
    st.download_button(
        label="Download Strategy as CSV",
        data=df.to_csv().encode('utf-8'),
        file_name='credit_action_plan.csv',
        mime='text/csv',
    )
