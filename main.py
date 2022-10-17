import streamlit as st
import pandas as pd
import os
from twilio.rest import Client
import plotly.graph_objects as go

st.set_page_config(page_title="Astia a Smishing Platform", page_icon=":fishing_pole_and_fish:", layout="wide")

global message
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("styles/mystyle.css")


def send_message(str):
    account_sid = st.secrets['account_sid']
    auth_token = st.secrets['auth_token']
    client = Client(account_sid, auth_token)
    for i in range(len(number_column)):
        st.write(number_column[i])
        message = client.messages.create(
            body=str,
            from_= st.secrets['twilio_number'],
            to=number_column[i]
        )
        st.success(f"Sent to {i + 1} device")
        st.write(message.body)


with st.container():
    tab1, tab2, tab3 = st.tabs(["Attack", "Targets", "Campaign"])

    with tab1:
        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader("Attack Templates")
            options = st.radio(
                "Select a template for the smishing: ",
                ('Flu Season (Recommended)', 'Sick Family', 'Sign In', 'You Won', 'Double Tap'))
            if options == 'Flu Season (Recommended)':
                st.write('You selected flu Season template. Hit Confirm and go to Target tab!')

                message = """
                It is flu season, get your flu shot. If you are eligible for an updated COVID 19 
                booster,you can get your flu shot at the same time. Visit covid19.nj.gov/finder to find a convenient 
                location near you or Call us: NJDOH COVID 19 Hotline, 855-568-0545. Para recibir este mensaje en 
                espanol responda 1. Reply STOP to opt out
                """
                with right_column:
                    st.subheader("Preview")
                    st.image("images/flu.png", width=300)
                with left_column:
                    if st.button("See The SMS", key=None, help=None, on_click=None):
                        st.success(message)

            if options == 'Sick Family':
                st.write('You selected Sick Family template. Hit Confirm and go to Target tab!')
                message = """Sick Family"""
                with right_column:
                    st.subheader("Preview")
                    st.image("images/image1.png", width=300)
                    with left_column:
                        if st.button("See The SMS", key=None, help=None, on_click=None):
                            st.success(message)

            if options == 'Sign In':
                st.write('You selected Sign In template. Hit Confirm and go to Target tab!')
                message = """Sign In"""
                with right_column:
                    st.subheader("Preview")
                    st.image("images/signin.jpg", width=300)
                    with left_column:
                        if st.button("See The SMS", key=None, help=None, on_click=None):
                            st.success(message)

            if options == 'You Won':
                st.write('You selected You Won template. Hit Confirm and go to Target tab!')
                message = """You won"""
                with right_column:
                    st.subheader("Preview")
                    st.image("images/lottery.png", width=300)
                    with left_column:
                        if st.button("See The SMS", key=None, help=None, on_click=None):
                            st.success(message)

            if options == 'Double Tap':
                st.write('You selected Double Tap template. Hit Confirm and go to Target tab!')
                message = """Double Tap"""
                with right_column:
                    st.subheader("Preview")
                    st.image("images/image2.png", width=300)
                    with left_column:
                        if st.button("See The SMS", key=None, help=None, on_click=None):
                            st.success(message)

    with tab2:
        left_column, right_column = st.columns(2)
        with right_column:
            st.subheader("Preview of Targeted Data")
        with left_column:
            st.subheader("Set Your Target")
            try:
                uploaded_file = st.file_uploader("Select a CSV file contains employees name and phone number")
                if uploaded_file is not None:
                    data = pd.read_csv(uploaded_file)
                        #data.to_html("Table.htm")
                    html_file = data.to_html()
                    try:
                        number_column = data['PhoneNumber'].tolist()
                        with right_column:
                            st.write(html_file, unsafe_allow_html=True)
                            with left_column:
                                st.success(
                                        "Data Uploaded Successfully.\nHit the Launch Attack button. Go to campaign tab to see the "
                                        "result.")
                                if st.button("Launch Attack", key=None, help=None, on_click=None):
                                    try:
                                        send_message(message)
                                    except:
                                        st.error("This Number is not verified. Twilio Trial Account Limitation!")
                    except:
                        st.error("Number Column's header should be \'PhoneNumber\'")
                else:
                    st.warning("Type Sensetive: Must upload a CSV")
                st.write("##")
                st.write("##")
            except:
                st.error("Type Sensetive: Must upload a CSV")
    with tab3:
        st.header("Dashboard")
        uploaded_file = st.file_uploader("Upload the file sent via email to see the analytics!")
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
            sent_link_count = data['SentLink'].tolist()
            clicked_link_count = data['ClickedLink'].tolist()
            entered_cred_count = data['EnteredCred'].tolist()
            executive_emp = data['Executive'].tolist()
            management_emp = data['Management'].tolist()
            general_emp = data['General'].tolist()

        kpi1, kpi2, kpi3 = st.columns(3)
        try:
            kpi1.metric(label="Sent Link", value=sent_link_count[0])
            kpi2.metric(label="Clicked Link", value=clicked_link_count[0])
            kpi3.metric(label="Entered Credential", value=entered_cred_count[0])
            left_column, right_column = st.columns(2)
            labels = ['Link Sent', 'Clicked Link', 'Entered Credential']
            tags = ['Executive Level', 'Management Level', 'General Employee']
            values = [executive_emp[0], management_emp[0], general_emp[0]]
            fig1 = go.Figure([go.Bar(x=labels, y=[sent_link_count[0], clicked_link_count[0], entered_cred_count[0]])])
            fig2 = go.Figure(data=[go.Pie(labels=tags, values=values, pull=[0, 0, 0.2, 0])])
            with left_column:
                st.write(fig1)
            with right_column:
                st.write(fig2)
        except:
            st.error("First Upload Data")


