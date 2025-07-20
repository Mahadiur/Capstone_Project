''' Import all Item '''
from Analysis_Data import *
import streamlit as st
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
            product_data = pd.read_csv(file)

        elif file.name == 'purchases.csv':
            purchases_data = pd.read_csv(file)
            purchases_data =pd.to_datetime(purchases_data['purchase_date']).dt.date
        elif file.name == 'sales.csv':
            sales_data = pd.read_csv(file)
            sales_data = pd.to_datetime(sales_data['sale_date']).dt.date
    return product_data, purchases_data, sales_data

product_data, purchases_data, sales_data = upload_file()


''' Sidebar '''
st.sidebar.header('Filters')

date1 = datetime.strptime('2024-01-01','%Y-%m-%d').date()
date2 = datetime.strptime('2024-12-31','%Y-%m-%d').date()

date_range = st.sidebar.date_input(
    label='Select Date Range:',
    value=[date1,date2]
)


locaton_select = st.sidebar.multiselect(
    label='Select Store Location:',
    options=['Dhaka','Chattogram','Rajshahi','Sylhet'],
    default=['Chattogram']
)


category_select = st.sidebar.multiselect(
    label='Select Product Category:',
    options=['Groceries', 'Electronics','Clothing','Perishables'],
    default=['Electronics']
)



''' Dashboard '''
st.header('Business Analytics Dashboard')
if product_data is not None:
    sales_data,product_data,purchases_data= add_business_analytics(
        sales_data,
        product_data,
        purchases_data
    )

    start_date = str(date_range[0])
    last_date = str(date_range[1])

    filtered_sale = sales_between_dates(
        sales_data=sales_data,
        startDate=start_date,
        lastDate=last_date,
        location=locaton_select
    )

    Filterd_products = Selected_category(
        product_data=product_data,
        category=category_select
    )

    understock_product = Product_UnderStock(
        product_data=Filterd_products
    )

    summary_keys = summay_of_data(
        product_data=Filterd_products,
        sales_data=filtered_sale   
    )



    revenue_column, profit_column, quantity_sold, low_stock = st.columns(4)
    with revenue_column:
        st.metric(
            label='Total Revenue (K):',
            value=f'{summary_keys['Total Revenue (K)']}'
        )

    with profit_column:
        st.metric(
            label='Total Profit (K)',
            value=f'{summary_keys['Total Profit (K)']}'
        )

    with quantity_sold:
        st.metric(
            label='Sold Quantity (K)',
            value=f'{summary_keys['Total Sold Quantity (K)']}'
        )

    with low_stock:
        st.metric(
            label='Total UnderStock',
            value=f'{summary_keys['Total Understock Product']}'
        )



