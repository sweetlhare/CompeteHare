import streamlit as st
import os
from io import StringIO
import pandas as pd
import numpy as np


from deta import Deta

deta_key = st.secrets['deta_key']
deta = Deta(deta_key)
deta_drive = deta.Drive("name of drive")


from metric import calculate_metric


# <------------------------------------------------------------------------->


registration_columns = [
    'Login',
    'Password',
    'Email',
    'Telegram',
    'FIO',
]

def load_users(path_to_file='assets/users_database.csv'):
    users_database = pd.read_csv(StringIO(str(deta_drive.get(path_to_file).read(), 'utf-8')))
    users_database = users_database.set_index('Login')
    return users_database

def update_users(login, user_values, path_to_file='assets/users_database.csv'):
    users_database.loc[str(login), registration_columns[1:]] = user_values
    users_database['Password'] = users_database['Password'].astype(str)
    users_database.to_csv(path_to_file)
    deta_drive.put(path_to_file, path=f"./{path_to_file}")
    return users_database

def load_gt(path_to_file='assets/gt.csv'):
    gt_file = pd.read_csv(StringIO(str(deta_drive.get(path_to_file).read(), 'utf-8')))
    return gt_file

def load_rating(path_to_file='assets/rating.csv'):
    rating_file = pd.read_csv(StringIO(str(deta_drive.get(path_to_file).read(), 'utf-8')))
    return rating_file

def update_rating(login, metric, path_to_file='assets/rating.csv'):
    rating.loc[rating.shape[0], ['Login', 'Metric']] = [login, metric]
    rating.to_csv(path_to_file, index=False)
    deta_drive.put(path_to_file, path=f"./{path_to_file}")
    return rating

users_database = load_users()
gt = load_gt()
rating = load_rating()

    
# <------------------------------------------------------------------------->   

# Sidebar Menu
with st.sidebar:
    st.title('Name of competition')
    add_selectbox = st.radio(
        "Menu",
        ("Task description", "Leaderbord", "Registration", "Send solution")
    )

# Task Description
if add_selectbox == 'Task description':
    st.header(add_selectbox)
    st.text('''
    Write description of your task here.
    You can also add some charts and tables.
    '''
    )

# Leaderboard
if add_selectbox == 'Leaderbord':
    st.header(add_selectbox)
    st.dataframe(rating)

# New User Registration
if add_selectbox == 'Registration':
    st.header(add_selectbox)

    st.text('''
    Fill in the fields below to register in the competition. 
    Login and password are needed to send solutions.
    The rest of the information to contact you.
    * - required to be filled in.''')

    login = st.text_input('Login *')
    password = st.text_input('Password *')
    fio = st.text_input('Full name *')
    email = st.text_input('Email *')
    telegram = st.text_input('Telegram')

    registration_button = st.button('Register')

    if registration_button:
        if login and password and email:
            if login in users_database.index.values and users_database.loc[login, 'Password'] != password:
                st.text('A user with this username already exists.')
                st.text('''
                If you forgot your password, write a recovery request
                to the XXX@gmail.com from the email to which the account is registered.''')
            else:
                users_database = update_users(login, [password, email, telegram, fio])
                st.text('You have successfully registered! You can upload solutions.')
        else:
            st.text('Registration failed. Check that all required fields are filled in correctly.')

# Solution uploading
if add_selectbox == 'Send solution':
    st.header(add_selectbox)

    st.text('Enter your username and password to access the download of the solution.')
    
    login = st.text_input('Login')
    password = st.text_input('Password')

    if login and password \
    and login in users_database.index.values \
    and users_database.loc[login, 'Password'] == password:
        uploaded_file = st.file_uploader('Upload the solution file', accept_multiple_files=False, type=['csv'])
        if uploaded_file:
            metric = calculate_metric(uploaded_file, gt)
            rating = update_rating(login, metric)
            st.text(f'Resulting metric: {metric}')
                   
