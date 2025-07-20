import os 
import pandas as pd
import plotly.express as plt
from datetime import timedelta
from datetime import datetime



Root_path = 'C:\\Users\\mdmes\\OneDrive\\Desktop\\Pandas Data'

product_path = os.path.join(Root_path,'products.csv')
purchases_path =os.path.join(Root_path, 'purchases.csv')
sales_path = os.path.join(Root_path, 'sales.csv')


product_data = pd.read_csv(
    product_path
)
print(product_data.head())



purchases_data = pd.read_csv(
    purchases_path
)

print(purchases_data.head())


sales_data = pd.read_csv(
    sales_path
)

print(sales_data.head())



sales_data['sale_date'] = pd.to_datetime(sales_data['sale_date']).dt.date

date1 =datetime.strptime('2024-09-01','%Y-%m-%d').date()
date2 =datetime.strptime('2024-09-03','%Y-%m-%d').date()

date = sales_data['sale_date'].iloc[0]

print(date1 <= date <= date2)



purchases_data['purchase_date'] = pd.to_datetime(purchases_data['purchase_date']).dt.date

date3 = datetime.strptime('2024-08-18','%Y-%m-%d').date()
date4 = datetime.strptime('2024-08-20','%Y-%m-%d').date()
Date = purchases_data['purchase_date'].iloc[0]

print(date3 <= Date <= date4)


def Current_Stock(product_id,purchases_data,sales_data):
    # per product purchase quantity
    per_product_purchase = purchases_data[
        purchases_data['product_id'] == product_id]['quantity_purchased'].sum()

    # per product sales quantity
    per_product_sale = sales_data[
        sales_data['product_id'] == product_id]['quantity_sold'].sum()


    # Current Stock
    per_product_stock = per_product_purchase - per_product_sale

    return per_product_stock

# print(Current_Stock(1095,purchases_data,sales_data))

# product_data['Current_Stock'] = product_data['product_id'].apply(
#     lambda product_id : Current_Stock(
#         product_id=product_id,
#         purchases_data=purchases_data,
#         sales_data=sales_data        
#         )
#     )

print(product_data.head())



def per_product_profit(product_id,sales_data,product_data):
    per_product_sold_quantity = sales_data[
        sales_data['product_id'] == product_id
    ]['quantity_sold'].sum()

    product = product_data[product_data['product_id'] == product_id]

    per_product_profit = product['selling_price'] - product['cost_price']
    per_product_profit = per_product_profit.iloc[0]

    per_product_total_profit = per_product_profit * per_product_sold_quantity

    return per_product_total_profit

# print(per_product_profit(1095,sales_data,product_data))

# product_data['Per_Product_Profit'] = product_data['product_id'].apply(
#     lambda product_id : per_product_profit(
#         product_id=product_id,
#         sales_data=sales_data,
#         product_data=product_data
#         )
# )

print(product_data.head())



startDate = datetime.strptime('2024-12-31','%Y-%m-%d').date()
lastDate = startDate - timedelta(days=90)
product_id = 1095
product_Sale_by_90days = sales_data[ 
    (sales_data['product_id'] == product_id)&
    (sales_data['sale_date'] >= lastDate)
]['quantity_sold'].sum()

def Slow_Moving_Product(product_id,sales_data):
    per_product_info = sales_data[ 
        (sales_data['product_id'] == product_id) &
        (sales_data['sale_date'] >= lastDate)
    ]['quantity_sold'].sum()

    return per_product_info < 40

# product_data['Slow_Moving_Products'] = product_data['product_id'].apply(
#     lambda product_id: Slow_Moving_Product(
#         product_id=product_id,
#         sales_data=sales_data
#         )
# )

print(product_data.head())



def Stock_status(product_id,product_data):
    product = product_data[
        product_data['product_id'] == product_id
    ].iloc[0]

    current_stock = product['Current_Stock']
    recorder_level = product['reorder_level']

    if current_stock < recorder_level: return 'UnderStock'
    elif current_stock > recorder_level*15: return 'OverStock'
    return 'Perfect Stock'


# print(Stock_status(1095,product_data))

# product_data['Stock_Status'] = product_data['product_id'].apply(
#     lambda product_id: Stock_status(
#         product_id=product_id,
#         product_data=product_data
#     )
# )

print(product_data.head())



def per_product_revenue(product_data, sales_data, product_id):
    selling_price = product_data[ 
        product_data['product_id'] == product_id
    ]['selling_price'].iloc[0]

    quantity_sold = sales_data[ 
        sales_data['product_id'] == product_id
    ]['quantity_sold'].sum()

    revenue = quantity_sold * selling_price

    return revenue

per_product_revenue(
    product_data=product_data,
    sales_data=sales_data,
    product_id=1095
)


def sales_between_dates(sales_data, startDate, lastDate, location):
    return sales_data[ 
        (sales_data['sale_date'] >= startDate)&
        (sales_data['sale_date'] <= lastDate)&
        (sales_data['location'].isin(location))
    ]


def Selected_category(product_data, category):
    return product_data[product_data['category'].isin(category)]


def Product_UnderStock(product_data):
    return product_data[product_data['Stock_Status'] == 'UnderStock']



def summay_of_data(product_data, sales_data):
    total_revenue = product_data['product_id'].apply(
        lambda product_id: per_product_revenue(
            product_data=product_data,
            product_id=product_id,
            sales_data=sales_data
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


def add_business_analytics(sales_data, product_data,purchases_data):
    product_data['Current_Stock'] = product_data['product_id'].apply(
        lambda product_id : Current_Stock(
            product_id,
            purchases_data,
            sales_data
        )
    )

    product_data['Per_Product_Profit'] = product_data['product_id'].apply(
        lambda product_id : per_product_profit(
            product_id,
            sales_data,
            product_data
        )
    )
    product_data['Slow_Moving_Products'] = product_data['product_id'].apply(
        lambda product_id: Slow_Moving_Product(
            product_id,
            sales_data
        )
    )

    product_data['Stock_Status'] = product_data['product_id'].apply(
        lambda product_id: Stock_status(
            product_id,product_data
        )
    )

    return sales_data, product_data, purchases_data
