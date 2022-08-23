import pandas as pd
import streamlit as st

from deta import Deta

deta_key = 'your deta key'
deta = Deta(deta_key)
deta_drive = deta.Drive("name of drive")


registration_columns = [
    'Login',
    'Password',
    'Email',
    'Telegram',
    'FIO',
]

users_database = pd.DataFrame(columns=registration_columns)
users_database.to_csv('assets/users_database.csv', index=False)
deta_drive.put('assets/users_database.csv', path=f"./assets/users_database.csv")

rating = pd.DataFrame(columns=['Login', 'Metric'])
rating.to_csv('assets/rating.csv', index=False)
deta_drive.put('assets/rating.csv', path=f"./assets/rating.csv")

deta_drive.put('assets/gt.csv', path=f"./assets/gt.csv")
