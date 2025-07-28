import os 
import pandas as pd
import plotly.express as plt
from datetime import timedelta
from datetime import datetime


# Root File Path
Root_path = 'C:\\Users\\mdmes\\OneDrive\\Desktop\\Pandas Data'

product_path = os.path.join(Root_path,'products.csv')
purchases_path =os.path.join(Root_path, 'purchases.csv')
sales_path = os.path.join(Root_path, 'sales.csv')

# Load Product Data
product_data = pd.read_csv(
    product_path
)
print(product_data.head())

# Purchases Data
purchases_data = pd.read_csv(
    purchases_path
)
print(purchases_data.head())

# Sales Data
sales_data = pd.read_csv(
    sales_path
)
print(sales_data.head())

# Remote font and back all space
product_data.columns = product_data.columns.str.strip()
purchases_data.columns = purchases_data.columns.str.strip()
sales_data.columns = sales_data.columns.str.strip()


''' Convert String to Datetime '''
sales_data['sale_date'] = pd.to_datetime(sales_data['sale_date']).dt.date
date1 =datetime.strptime('2024-09-01','%Y-%m-%d').date()
date2 =datetime.strptime('2024-09-03','%Y-%m-%d').date()
date = sales_data['sale_date'].iloc[0]

print(date1 <= date <= date2)


''' Convert String to Datetime '''
purchases_data['purchase_date'] = pd.to_datetime(purchases_data['purchase_date']).dt.date
date3 = datetime.strptime('2024-08-18','%Y-%m-%d').date()
date4 = datetime.strptime('2024-08-20','%Y-%m-%d').date()
Date = purchases_data['purchase_date'].iloc[0]
print(date3 <= Date <= date4)


''' Compute Current Stock Function '''
def Current_Stock(product_id,purchases_data,sales_data):
    # per product purchase quantity
    per_product_purchase = purchases_data[purchases_data['product_id'] == product_id]['quantity_purchased'].sum()
    # per product sales quantity
    per_product_sale = sales_data[sales_data['product_id'] == product_id]['quantity_sold'].sum()
    # Current Stock
    per_product_stock = per_product_purchase - per_product_sale

    return per_product_stock

''' Calculate Per Products Profit  '''
def per_product_profit(product_id,sales_data,product_data):
    per_product_sold_quantity = sales_data[
        sales_data['product_id'] == product_id
    ]['quantity_sold'].sum()

    product = product_data[product_data['product_id'] == product_id]

    per_product_profit = product['selling_price'] - product['cost_price']
    per_product_profit = per_product_profit.iloc[0]

    per_product_total_profit = per_product_profit * per_product_sold_quantity

    return per_product_total_profit


startDate = datetime.strptime('2024-12-31','%Y-%m-%d').date()
lastDate = startDate - timedelta(days=90)


''' All Slow Moving Products '''
def Slow_Moving_Product(product_id,sales_data):
    per_product_info = sales_data[ 
        (sales_data['product_id'] == product_id) &
        (sales_data['sale_date'] >= lastDate)
    ]['quantity_sold'].sum()

    return per_product_info < 40


''' Find Products Understock, Overstock, perfectStock '''
def Stock_status(product_id,product_data):
    product = product_data[
        product_data['product_id'] == product_id
    ].iloc[0]

    current_stock = product['Current_Stock']
    recorder_level = product['reorder_level']

    if current_stock < recorder_level: return 'UnderStock'
    elif current_stock > recorder_level*15: return 'OverStock'
    else: return 'Perfect-Stock'


''' Per Products Revenue '''
def per_product_revenue(product_data, sales_data, product_id):
    selling_price = product_data[ 
        product_data['product_id'] == product_id
    ]['selling_price'].iloc[0]

    quantity_sold = sales_data[ 
        sales_data['product_id'] == product_id
    ]['quantity_sold'].sum()

    revenue = quantity_sold * selling_price

    return revenue

print(per_product_revenue(product_data, sales_data,1095))

''' Filter Product by time & location based '''
def sales_between_dates(sales_data, startDate, lastDate, location):
    return sales_data[ 
         (sales_data['sale_date'] >= startDate)&
        (sales_data['sale_date'] <= lastDate)&
        (sales_data['location'].isin(location))
    ]

''' Filter Category '''
def Selected_category(product_data, category):
    return product_data[product_data['category'].isin(category)]

''' Filter UnderStock '''
def Product_UnderStock(product_data):
    return product_data[product_data['Stock_Status'] == 'UnderStock']


''' Product Revenue, profit, sold-quantity, UnderStock '''
def summay_of_data(product_data, sales_data):
    total_revenue = product_data['product_id'].apply(
        lambda product_id: per_product_revenue(
            product_data=product_data,
            sales_data=sales_data,
            product_id=product_id
        )
    ).sum()

    total_profit = product_data['Per_Product_Profit'].sum()
    total_sold_quantity = sales_data['quantity_sold'].sum()
    total_understock = len(Product_UnderStock(
        product_data=product_data
    ))


    return {
        'Total Revenue (K)':int(total_revenue/1e3),
        'Total Profit (K)':int(total_profit/1e3),
        'Total Sold Quantity (K)' : int(total_sold_quantity/1e3),
        'Total Understock Product':total_understock
    }

''' More import Function for Dashboard '''
def add_business_analytics(sales_data, product_data,purchases_data):
    product_data['Current_Stock'] = product_data['product_id'].apply(
        lambda product_id : Current_Stock(
            product_id=product_id,
            purchases_data=purchases_data,
            sales_data=sales_data
        )
    )

    product_data['Per_Product_Profit'] = product_data['product_id'].apply(
        lambda product_id : per_product_profit(
            product_id=product_id,
            sales_data=sales_data,
            product_data=product_data
        )
    )
    product_data['Slow_Moving_Products'] = product_data['product_id'].apply(
        lambda product_id : Slow_Moving_Product(
            product_id=product_id,
            sales_data=sales_data
        )
    )

    product_data['Stock_Status'] = product_data['product_id'].apply(
        lambda product_id: Stock_status(
            product_id=product_id,
            product_data=product_data
        )
    )

    return sales_data, product_data, purchases_data
sales_data, product_data, purchases_data = add_business_analytics(sales_data, product_data,purchases_data)
print(product_data.head())
print(purchases_data.head())
print(sales_data.head())
filtered_sale = sales_between_dates(
    sales_data=sales_data,
    startDate=datetime.strptime('2024-01-01','%Y-%m-%d').date(),
    lastDate= datetime.strptime('2024-12-31','%Y-%m-%d').date(),
    location=['Dhaka']
)
filtered_product = Selected_category(
    product_data=product_data,
    category=['Electronics']
)
summay_check = summay_of_data(filtered_product, filtered_sale)
print(f'{summay_check['Total Revenue (K)']}')
print(f'{summay_check['Total Profit (K)']}')
print(f'{summay_check['Total Sold Quantity (K)']}')
print(f'{summay_check['Total Understock Product']}')
print(filtered_sale)

''' Import all Item '''
# from Analysis_Data import *
import streamlit as st
import plotly.express as pt
import base64
import numpy as np
import pandas as pd
from datetime import datetime

# Dashboard Page Setup
st.set_page_config(
    page_title='Business Analytics Dashboard',
    layout='centered'
)

# Dashboard File Uploading function
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


# Dashboard Sidebar
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


# Dashboard
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

    # Dashboard column

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

    # Visualaization by plotly
    st.subheader('Top 10 Products by Profit:')
    top_product = Filterd_products.nlargest(10,'Per_Product_Profit')[['product_name', 'Per_Product_Profit']]
    plot1 = pt.bar(top_product, x='product_name', y='Per_Product_Profit',title='Top 10 Products by Profit')
    st.plotly_chart(plot1, use_container_width=True)


    st.subheader('Product Distribution:')
    product =Filterd_products.groupby('category')['Per_Product_Profit'].sum().reset_index()
    plot2 = pt.pie(product, values='Per_Product_Profit',names='category', title='Product Distribution')
    st.plotly_chart(plot2, use_container_width=True)


    # Dashboard Table
    st.subheader('Product Stock and Profit information:')
    stock_info = filtered_product[[
        'product_name','category','Current_Stock','reorder_level','Per_Product_Profit','Stock_Status'
    ]]
    stock_info['Stock_Status']= stock_info['Stock_Status'].map({
        'UnderStock':"<span style='color:red'>UnderStock</span>",
        'Perfect-Stock':"<span style='color:skyblue'>Perfect Stock</span>",
        'OverStock':"<span style='color:blue'>OverStock</span>"
    })
    st.markdown(stock_info.to_html(escape=False),unsafe_allow_html=True)


    st.subheader('OverStock and UnderStock Products:')
    over_under_stock = filtered_product[filtered_product['Stock_Status'].isin(['UnderStock', 'OverStock'])]
    over_under_stock = over_under_stock[['product_name', 'category', 'reorder_level', 'Current_Stock', 'Stock_Status']]
    over_under_stock['Suggested_reorder'] = np.where(over_under_stock['Stock_Status']=='UnderStock', over_under_stock['reorder_level'] - over_under_stock['Current_Stock'],0)
    over_under_stock['Stock_Status'] = over_under_stock['Stock_Status'].map({
        'UnderStock':"<span style='color:red'>UnderStock</span>",
        'OverStock':"<span style='color:green'>OverStock</span>"
    })
    st.markdown(over_under_stock.to_html(escape=False), unsafe_allow_html=True)


    # Download system
    def Download_function(data, filename):
        csv = data.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        return f"<a href='data/file;base64,{b64}' download='{filename}.csv'>Download {filename} </a>"

    st.markdown(Download_function(stock_info, 'stock_info'),unsafe_allow_html=True) 
    st.markdown(Download_function(over_under_stock, 'over_under_stock') ,unsafe_allow_html=True)


    # Recommendations
    st.subheader('Business Recommendations:')
    recommends=[]

    UnderStock= Filterd_products[Filterd_products['Stock_Status'] == 'UnderStock']
    if not UnderStock.empty:
        recommends.append(
            f'**Argently Restock: {len(UnderStock)} products are UnderStock.UnderStock Products Name => {UnderStock['product_name'].tolist()}'
        )
    Slow_moving = Filterd_products[Filterd_products['Slow_Moving_Products'] == True]
    if not Slow_moving.empty:
        recommends.append(
            f'**Slow Moving Products: {len(Slow_moving)} products are Move Slowly. Slow moving produts name => {Slow_moving['product_name'].tolist()}'
        )

    OverStock = Filterd_products[Filterd_products['Stock_Status'] == 'OverStock']
    if not OverStock.empty:
        recommends.append(
            f'**Argently Sale: {len(OverStock)} products are OverStock. OverStock Products name Rainbow:{OverStock['product_name'].tolist()}'
        )

    for i in recommends:
        st.markdown(f' :rainbow[{i}]')

    # Just for enjoy 
    if st.button('Send Ballons'):
        st.balloons()
