import streamlit as st
import os
import pandas as pd
import numpy as np


# <------------------------------------------------------------------------->

# st.set_page_config(layout="wide")

registration_columns = [
    'login',
    'password',
    'email'
    # 'FIO',
    # 'age'
]

def load_users_database(path_to_db='assets/users_database.csv'):
    if os.path.exists(path_to_db):
        users_database = pd.read_csv(path_to_db)
        users_database['login'] = users_database['login'].astype(str)
        users_database['password'] = users_database['password'].astype(str)
        users_database = users_database.set_index('login')
    else:
        users_database = pd.DataFrame(columns=registration_columns).set_index('login')
        users_database.to_csv(path_to_db)
    return users_database

def update_users_database(login, user_values, path_to_db='assets/users_database.csv'):
    users_database.loc[str(login), registration_columns[1:]] = user_values
    users_database['password'] = users_database['password'].astype(str)
    users_database.to_csv(path_to_db)
    return users_database

users_database = load_users_database()
    
# <------------------------------------------------------------------------->   

# Using object notation
with st.sidebar:
    st.title('ХаХаСтарт: Object Detection')
    add_selectbox = st.radio(
        "Раздел",
        ("Информация о задаче", "Рейтинг", "Регистрация", "Загрузка решения")
    )

if add_selectbox == 'Информация о задаче':
    st.header(add_selectbox)


if add_selectbox == 'Рейтинг':
    st.header(add_selectbox)


if add_selectbox == 'Регистрация':
    st.header(add_selectbox)

    st.text('''
    Заполните поля ниже, чтобы зарегистрироваться в соревновании. 
    Логин и пароль нужен для загрузки решений.
    Остальная информация для связи с вами.
    * - обязательно к заполнению.''')

    login = st.text_input('Логин *')
    password = st.text_input('Пароль *')
    email = st.text_input('Email *')

    registration_button = st.button('Зарегистрироваться')

    if registration_button:
        if login and password and email:
            if users_database.loc[login, ].shape[0] > 0 and users_database.loc[login, 'password'] != password:
                st.text('Пользователь с таким логином уже существует.')
                st.text('''
                Если вы забыли пароль, напишите запрос на восстановление
                на почту ХХХ с почты, на которую зарегистрирован аккаунт.''')
            else:
                users_database = update_users_database(login, [password, email])
                st.text('Вы успешно зарегистрировались! Можно загружать решения.')
        else:
            st.text('Регистрация не удалась. Проверьте, что все обязательные поля заполнены верно.')


if add_selectbox == 'Загрузка решения':
    st.header(add_selectbox)

    st.text('Введите логин и пароль, чтобы получить доступ к загрузке решения.')
    
    login = st.text_input('Логин')
    password = st.text_input('Пароль')

    if login and password \
    and users_database.loc[login, ].shape[0] > 0 \
    and users_database.loc[login, 'password'] == password:
        uploaded_file = st.file_uploader('Загрузите файл с решением', accept_multiple_files=False, type=['csv'])
        if uploaded_file:
            st.text(f'Полученная метрика: {0.9999}')
                   