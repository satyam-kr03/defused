from google.oauth2 import service_account
from googleapiclient.discovery import build
import time
from datetime import datetime
from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import json
import streamlit as st
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = "1"

# Copy your credentials from the Google Developers Console
CLIENT_ID = '720743198287-ui7uqdi7nfmml7vnca0kasi6cofptev3.apps.googleusercontent.com'
CLIENT_SECRET = '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'

# Check https://developers.google.com/fit/rest/v1/reference/users/dataSources/datasets/get
# for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/fitness.activity.read'

# DATA SOURCE
DATA_SOURCE = "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
# The ID is formatted like: "startTime-endTime" where startTime and endTime are
# 64 bit integers (epoch time with nanoseconds).

creds = None

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

CLIENT_FILE = 'creds.json'
SCOPES = ['https://www.googleapis.com/auth/fitness.activity.read', 'https://www.googleapis.com/auth/fitness.blood_glucose.read', 'https://www.googleapis.com/auth/fitness.blood_pressure.read', 'https://www.googleapis.com/auth/fitness.body.read', 'https://www.googleapis.com/auth/fitness.body_temperature.read', 'https://www.googleapis.com/auth/fitness.heart_rate.read', 'https://www.googleapis.com/auth/fitness.location.read', 'https://www.googleapis.com/auth/fitness.nutrition.read', 'https://www.googleapis.com/auth/fitness.oxygen_saturation.read', 'https://www.googleapis.com/auth/fitness.reproductive_health.read', 'https://www.googleapis.com/auth/fitness.sleep.read', 'https://www.googleapis.com/auth/userinfo.profile']

REDIRECT_URI = 'http://localhost:8080'  # Use a fixed port
TOKEN_FILE = 'token.json'

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as token:
            creds_data = json.load(token)
            creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
    return creds

creds = get_credentials()
# print(creds)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        st.write('Welcome! Please sign in with your Google Account to continue.')
        if st.button('Sign In with Google'):
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_FILE, SCOPES, redirect_uri=REDIRECT_URI)
            creds = flow.run_local_server(port=8080)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
                st.rerun()
else:
    st.switch_page('pages/Feed.py')




