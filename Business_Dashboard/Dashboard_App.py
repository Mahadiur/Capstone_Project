''' Import all Item '''
import streamlit as st
from Analysis_Data import *
import plotly.express as plt
import base64
import numpy as np


st.set_page_config(
    page_title='Business Analytics Dashboard',
    layout='centered'
)


def upload_file():
    uploaded_file = st.sidebar.file_uploader(
        label='Upload CSV File',
        type='csv',
        accept_multiple_files=True
    )


    product_data, purchases_data, sales_data = None, None, None
    for file in uploaded_file:
        if file.name == 'products.csv':
            product_data = pd.read_csv('file')

        elif file.name == 'purchases.csv':
            purchases_data = pd.read_csv('file')
            purchases_data =pd.to_datetime(purchases_data['purchase_date']).dt.date
        elif file.name == 'sales.csv':
            sales_data = pd.read_csv('file')
            sales_data = pd.to_datetime(sales_data['sale_date']).dt.date
    return product_data, purchases_data, sales_data

product_data, purchases_data, sales_data = upload_file()



