''' Import all Item '''
from Analysis_Data import *
import streamlit as st
import plotly.express as plt
import base64
import numpy as np
import pandas as pd
from datetime import datetime


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
            product_data = pd.read_csv(file)
        elif file.name == 'purchases.csv':
            purchases_data = pd.read_csv(file)
            purchases_data['purchase_date'] =pd.to_datetime(purchases_data['purchase_date']).dt.date
        elif file.name == 'sales.csv':
            sales_data = pd.read_csv(file)
            sales_data['sale_date'] = pd.to_datetime(sales_data['sale_date']).dt.date
    return product_data, purchases_data, sales_data

product_data, purchases_data, sales_data = upload_file()



st.sidebar.header('Filters')

date1 = datetime.strptime('2024-01-01','%Y-%m-%d').date()
date2 = datetime.strptime('2024-12-31','%Y-%m-%d').date()

date_range = st.sidebar.date_input(
    label='Select Date Range:',
    value=[date1,date2]
)


locaton_select = st.sidebar.multiselect(
    label='Select Store Location:',
    options=['Dhaka','Chittagong','Rajshahi','Sylhet'],
    default=['Chittagong']
)


category_select = st.sidebar.multiselect(
    label='Select Product Category:',
    options=['Groceries','Electronics','Clothing','Perishables'],
    default=['Electronics']
)
print(category_select)



st.header('Business Analytics Dashboard')
if product_data is not None and purchases_data is not None and sales_data is not None:
    sales_data,product_data,purchases_data= add_business_analytics(
        sales_data,
        product_data,
        purchases_data
    )

    start_date = str(date_range[0])
    last_date =str(date_range[1])
    print(start_date, last_date)

    filtered_sale = sales_between_dates(
        sales_data=sales_data,
        startDate=datetime.strptime(start_date,'%Y-%m-%d').date(),
        lastDate=datetime.strptime(last_date,'%Y-%m-%d').date(),
        location=locaton_select
    )
    print(filtered_sale)

    Filterd_products = Selected_category(
        product_data=product_data,
        category=category_select
    )
    print(Filterd_products)

    understock_product = Product_UnderStock(
        product_data=Filterd_products
    )

    summary_keys = summay_of_data(
        product_data=Filterd_products,
        sales_data=filtered_sale   
    )

    revenue_col, profit_col, Total_sold_col, Understock_product_col = st.columns(4)
    with revenue_col:
        st.metric(
            label='Total Revenue (K)',
            value=f"{summary_keys['Total Revenue (K)']}"
        )

    with profit_col:
        st.metric(
            label='Total Profit (K)',
            value=f"{summary_keys['Total Profit (K)']}"
        )

    with Total_sold_col:
        st.metric(
            label='Total Sold Quantity (K)',
            value=f"{summary_keys['Total Sold Quantity (K)']}"
        )

    with Understock_product_col:
        st.metric(
            label='Total Understock Product',
            value=f"{summary_keys['Total Understock Product']}"
        )