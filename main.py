import streamlit as st
import os
import pandas as pd
import numpy as np


from deta import Deta

deta_key = st.secrets['deta_key']
deta = Deta(deta_key)
deta_drive = deta.Drive("hahastart_object_detection")


from metric import calculate_metric


# <------------------------------------------------------------------------->

# st.set_page_config(layout="wide")

registration_columns = [
    'Login',
    'Password',
    'Email',
    'Telegram',
    'FIO',
]
from io import StringIO

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
    st.title('ХаХаСтарт: Object Detection')
    add_selectbox = st.radio(
        "Раздел",
        ("Информация о задаче", "Рейтинг", "Регистрация", "Загрузка решения")
    )

# Task Description
if add_selectbox == 'Информация о задаче':
    st.header(add_selectbox)

# Leaderboard
if add_selectbox == 'Рейтинг':
    st.header(add_selectbox)
    st.dataframe(rating)

# New User Registration
if add_selectbox == 'Регистрация':
    st.header(add_selectbox)

    st.text('''
    Заполните поля ниже, чтобы зарегистрироваться в соревновании. 
    Логин и пароль нужен для загрузки решений.
    Остальная информация для связи с вами.
    * - обязательно к заполнению.''')

    login = st.text_input('Логин *')
    password = st.text_input('Пароль *')
    fio = st.text_input('ФИО *')
    email = st.text_input('Email *')
    telegram = st.text_input('Telegram')

    registration_button = st.button('Зарегистрироваться')

    if registration_button:
        if login and password and email:
            if login in users_database.index.values and users_database.loc[login, 'Password'] != password:
                st.text('Пользователь с таким логином уже существует.')
                st.text('''
                Если вы забыли пароль, напишите запрос на восстановление
                на почту ХХХ с почты, на которую зарегистрирован аккаунт.''')
            else:
                users_database = update_users(login, [password, email, telegram, fio])
                st.text('Вы успешно зарегистрировались! Можно загружать решения.')
        else:
            st.text('Регистрация не удалась. Проверьте, что все обязательные поля заполнены верно.')

# Solution uploading
if add_selectbox == 'Загрузка решения':
    st.header(add_selectbox)

    st.text('Введите логин и пароль, чтобы получить доступ к загрузке решения.')
    
    login = st.text_input('Логин')
    password = st.text_input('Пароль')

    if login and password \
    and login in users_database.index.values \
    and users_database.loc[login, 'Password'] == password:
        uploaded_file = st.file_uploader('Загрузите файл с решением', accept_multiple_files=False, type=['csv'])
        if uploaded_file:
            metric = calculate_metric(uploaded_file, gt)
            rating = update_rating(login, metric)
            st.text(f'Полученная метрика: {0.9999}')
                   
