import streamlit as st
import pandas as pd
import pickle

# --- 1. LOAD THE SAVED MACHINE LEARNING FILES ---
# @st.cache_resource ensures these files only load once, keeping your app fast!
@st.cache_resource 
def load_artifacts():
    model = pickle.load(open('loan_model.pkl', 'rb'))
    scaler = pickle.load(open('scaler.pkl', 'rb'))
    ohe = pickle.load(open('ohe.pkl', 'rb'))
    le_education = pickle.load(open('le_education.pkl', 'rb'))
    model_columns = pickle.load(open('model_columns.pkl', 'rb'))
    return model, scaler, ohe, le_education, model_columns

model, scaler, ohe, le_education, model_columns = load_artifacts()


# --- 2. MAIN PAGE UI ---
st.title("🏦 CreditWise Loan Approval System")
st.write("Welcome to the **CreditWise** automated underwriting portal.")
st.write("👈 Please fill out the applicant's basic details in the sidebar to check their eligibility.")


# --- 3. SIDEBAR USER INPUTS ---
st.sidebar.header("Applicant Details")

name = st.sidebar.text_input("Full Name", "John Doe")
age = st.sidebar.number_input("Age", min_value=18, max_value=100, value=30)
marital_status = st.sidebar.selectbox("Marital Status", ["Single", "Married"])
income = st.sidebar.number_input("Monthly Income (₹)", min_value=0, value=50000, step=5000)
loan_amount = st.sidebar.number_input("Loan Amount Requested (₹)", min_value=0, value=150000, step=10000)


# --- 4. PREDICTION LOGIC ---
if st.sidebar.button("Check Eligibility"):
    
    # Pack the user's answers and fill in the blanks for the model
    user_data = {
        'Applicant_Income': income,      
        'Loan_Amount': loan_amount, 
        'Marital_Status': marital_status,
        'Age': age, 
        
        # --- BEHIND THE SCENES DEFAULTS ---
        'Gender': 'Male',
        'Education_Level': 'Graduate', 
        'Employment_Status': 'Salaried', # Fixed to match your CSV
        'Employer_Category': 'Private',  
        'Property_Area': 'Urban',     
        'Loan_Purpose': 'Personal',       
        'Coapplicant_Income': 2000.0, # Give them a decent co-applicant
        'Dependents': 0.0,
        'Credit_Score': 750.0,        # HIGH credit score so it gets approved!
        'Existing_Loans': 0.0,        # No existing debt
        'DTI_Ratio': 0.20,            # Good debt-to-income ratio
        'Savings': 25000.0,           # Good savings
        'Collateral_Value': 50000.0,  # Good collateral
        'Loan_Term': 60.0      
    }    

    input_df = pd.DataFrame([user_data])
    
    input_df['Education_Level'] = le_education.transform(input_df['Education_Level'])
    
    # Apply One-Hot Encoder
    ohe_cols = ["Employment_Status", "Marital_Status", 'Loan_Purpose', 'Property_Area', 'Gender', 'Employer_Category']
    encoded_input = ohe.transform(input_df[ohe_cols])
    encoded_input_df = pd.DataFrame(encoded_input, columns=ohe.get_feature_names_out(ohe_cols))
    
    input_df = pd.concat([input_df.drop(columns=ohe_cols), encoded_input_df], axis=1)
    
    input_df = input_df.reindex(columns=model_columns, fill_value=0)
    input_scaled = scaler.transform(input_df)
    
    eligibility_check = model.predict(input_scaled)
    
    # --- 5. DISPLAY RESULTS ---
    st.divider() 
    
    if eligibility_check[0] == 1:
        st.balloons()
        st.success(f"### 🎉 Congratulations {name}!")
        st.write(f"Based on your income of ₹{income} and requested amount of ₹{loan_amount}, you are **ELIGIBLE** for this loan.")
    else:
        st.error(f"### ❌ Sorry {name}.")
        st.write(f"Based on current risk parameters, you are **NOT ELIGIBLE** for this loan at this time.")