import streamlit as st
import requests # To make HTTP requests to the Flask API
import json     # To work with JSON data

st.title("Loan Approval Prediction Client")

st.subheader("Enter Loan Application Details:")

# Input fields for the loan application
gender = st.selectbox("Gender", ["Male", "Female"])
married = st.selectbox("Married", ["Unmarried", "Yes"]) # Assuming "Yes" maps to Married=1
credit_history = st.selectbox("Credit History", ["Unclear Debts", "Clear Debts"]) # Assuming "Clear Debts" maps to Credit_History=1
applicant_income = st.number_input("Applicant Income", min_value=0, value=5000)
loan_amount = st.number_input("Loan Amount", min_value=0, value=150)

# Button to trigger prediction
if st.button("Predict Loan Approval"):
    # Prepare the payload for the Flask API
    payload = {
        "Gender": gender,
        "Married": married,
        "Credit_History": credit_history,
        "ApplicantIncome": applicant_income,
        "LoanAmount": loan_amount
    }

    # Define the Flask API endpoint URL
    # Make sure your Flask app (app.py) is running on port 5000
    flask_api_url = "http://127.0.0.1:5000/prediction"

    st.write("Sending data to Flask API:", payload)

    try:
        # Send a POST request to the Flask API
        response = requests.post(flask_api_url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        # Get the prediction from the response
        prediction_result = response.json()
        loan_status = prediction_result.get("loan_approval_status")

        if loan_status:
            st.success(f"Loan Approval Status: {loan_status}")
            if loan_status == "Approved":
                st.balloons()
            else:
                st.snow() # Or some other visual for rejection
        else:
            st.error("Could not retrieve prediction status from the API response.")
            st.json(prediction_result) # Show the raw response for debugging

    except requests.exceptions.ConnectionError:
        st.error(f"Connection Error: Could not connect to the Flask API at {flask_api_url}. Please ensure the Flask server is running.")
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error: {e.response.status_code} - {e.response.reason}")
        st.text(f"Response content: {e.response.text}")
    except json.JSONDecodeError:
        st.error("Error decoding JSON response from the API. The API might not have returned valid JSON.")
        st.text(f"Raw response: {response.text}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

