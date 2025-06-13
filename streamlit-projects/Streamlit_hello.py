import streamlit as st
import pandas as pd
import numpy as np

st.title ("this is the heading !!!")
st.write(
    """
    # My first app. 
    # This is very nice to code

    Hello **world!** 

    ## Welcome Upendra to the Streamlit..

    """
)

st.header("Charting", divider=True)
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b','c']
)
st.line_chart(chart_data)

st.header("checkbox", divider=True)
agree = st.checkbox("I agree")
if agree:
    st.write("Great!")

donotagree = st.checkbox("I dont agree")
if donotagree:
    st.write("ok fine !")



col1, col2, col3= st.columns(3)
# Add checkboxes to separate columns
with col1:
    check1 = st.checkbox("Option 1")

with col2:
    check2 = st.checkbox("Option 2")

with col3:
    check3 = st.checkbox("Option 3")


# Show selected options
if check1:
    st.write("You selected Option 1!")

if check2:
    st.write("You selected Option 2!")

if check3:
    st.write("You selected Option 3!")

st.header("radio", divider=True)
genre = st.radio(
    "What's your favorite movie genre",
    [":rainbow[Comedy]", "***Drama***", "Documentary :movie_camera:"],
    captions=[
        "Laugh out loud.",
        "Get the popcorn.",
        "Never stop learning.",
    ],
)

if genre == "***Drama***":
    st.success("You selected Drama.")
else:
    st.write("You didn't select Drama.")


def sqr(num):
    return num*num


num = st.number_input("Enter a number", value=0)
st.write(f"square of number is {sqr(num)}")