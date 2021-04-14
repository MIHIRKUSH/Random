import pandas as pd
import sqlite3
from IPython.display import display, HTML
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


countries=pd.read_csv('counties.csv')
countries.loc[0]=list(countries.columns)
countries.columns=['Country','Population']

products=pd.read_csv('products.csv')
products.loc[0]=list(products.columns)
products.columns=['Item_no','Category_name','Item_description' ,'Vendor','Vendor_name','Bottle_size','Pack','Inner_pack','Age','Proof','List_date','Upc','Scc','Bottle_price','Shelf_price' ,'Case_cost']

sales=pd.read_csv('sales.csv')
sales.loc[0]=list(sales.columns)
sales.columns=['Date','Convenience_store','Store','County_number','County','Category','Category_name','Vendor_no','Vendor','Item','Description','Pack','Liter_size','State_btl_cost','Btl_price','Bottle_qty','Total']

stores=pd.read_csv('stores.csv')
stores.loc[0]=list(stores.columns)
stores.columns=['Stores','Name','Store_Status','Store_address','Address_info']


#MAKING OF DB
conn = sqlite3.connect('Shaddi.db')
c = conn.cursor()
 
countries.to_sql('COUNTRY', conn, if_exists='replace', index = False)
products.to_sql('PRODUCTS', conn, if_exists='replace', index = False)
sales.to_sql('SALES', conn, if_exists='replace', index = False)
stores.to_sql('STORES', conn, if_exists='replace', index = False)



tables = pd.read_sql_query("SELECT NAME AS 'Table_Name' FROM sqlite_master WHERE type='table'",conn)
tables = tables["Table_Name"].values.tolist()
for table in tables:
    query = "PRAGMA TABLE_INFO({})".format(table)
    schema = pd.read_sql_query(query,conn)
    print("Schema of",table)
    display(schema)
    print("-"*100)
    print("\n")

#PRODUCTS=ITEM DESCRIPTION and Category_name is different 
##1st
pd.read_sql_query('SELECT Item_description FROM PRODUCTS where PRODUCTS.Case_cost >100',conn)

##2nd
pd.read_sql_query(""" SELECT Item_description FROM PRODUCTS where PRODUCTS.Case_cost >100 and PRODUCTS.Category_name like 'TEQUILA' """ ,conn)


##3rd
pd.read_sql_query(""" SELECT Item_description FROM PRODUCTS where PRODUCTS.Case_cost >100 and PRODUCTS.Category_name='TEQUILA' OR PRODUCTS.Category_name='SCOTCH WHISKIES' """ ,conn)

#4th
pd.read_sql_query(""" SELECT Item_description FROM PRODUCTS where PRODUCTS.Case_cost BETWEEN 100  AND 120 and PRODUCTS.Category_name='TEQUILA' OR PRODUCTS.Category_name='SCOTCH WHISKIES' """ ,conn)


#5th
pd.read_sql_query('SELECT Item_description FROM PRODUCTS where PRODUCTS.Case_cost >100 and PRODUCTS.Category_name  like "%WHISKIES%"',conn)

#6th
pd.read_sql_query('SELECT Item_description FROM PRODUCTS where PRODUCTS.Case_cost BETWEEN 100 and 150  and PRODUCTS.Category_name  like "%WHISKIES%"',conn)


#7th
pd.read_sql_query('SELECT Item_description FROM PRODUCTS where PRODUCTS.Case_cost BETWEEN 100 and 150  and PRODUCTS.Category_name not like "%TEQUILA%"',conn)


#8th
pd.read_sql_query('SELECT Item_description FROM PRODUCTS where  PRODUCTS.Vendor_name not like "%Jim Beam Brands%"',conn)


#9th
pd.read_sql_query('SELECT Item_description FROM PRODUCTS where  PRODUCTS.proof > 90',conn)


#10th
pd.read_sql_query('SELECT Item_description FROM PRODUCTS where  PRODUCTS.Case_cost <60',conn)



#11th
pd.read_sql_query('SELECT Item_description FROM PRODUCTS where  PRODUCTS.Category_name like "SINGLE MALT SCOTCH" OR PRODUCTS.Category_name like "CANADIAN WHISKIES" ' ,conn)


#12th
pd.read_sql_query('SELECT Item_description FROM PRODUCTS where  PRODUCTS.Category_name like "%WHISKIES%" ',conn)


#13th
pd.read_sql_query('SELECT Item_description FROM PRODUCTS where  PRODUCTS.Shelf_price BETWEEN 10 and 4',conn)

#14th 
pd.read_sql_query('SELECT Item_description FROM PRODUCTS where  PRODUCTS.Bottle_price BETWEEN 10 AND 4',conn)



#15th 
pd.read_sql_query('SELECT  DISTINCT  Item_description FROM PRODUCTS where  PRODUCTS.Pack > 12 ',conn)

#16th
pd.read_sql_query('SELECT  DISTINCT  Item_description FROM PRODUCTS where  PRODUCTS.Pack <12 ',conn)


#17th  
pd.read_sql_query('SELECT  DISTINCT  Item_description FROM PRODUCTS where  PRODUCTS.Case_cost < 70 ',conn)


#18th 
pd.read_sql_query('SELECT  DISTINCT  Item_description FROM PRODUCTS where  PRODUCTS.Pack > 12 and  Products.Case_Cost < 70 ',conn)

#19th
pd.read_sql_query('SELECT COUNT (DISTINCT Item_description) FROM Products',conn)


#20th
pd.read_sql_query('SELECT PRODUCTS.Item_description,SUM(Bottle_qty) FROM PRODUCTS LEFT JOIN SALES on PRODUCTS.Item_no=SALES.Item Group by PRODUCTS.Item_no',conn)


#21st
pd.read_sql_query('SELECT PRODUCTS.Item_description,SUM(Bottle_qty) FROM PRODUCTS LEFT JOIN SALES on PRODUCTS.Item_no=SALES.Item and SALES.Item != "NaN" where PRODUCTS.Proof >80 Group by PRODUCTS.Item_no',conn)


#22nd
pd.read_sql_query('SELECT COUNT (DISTINCT County) FROM SALES',conn)

#23rd
pd.read_sql_query('SELECT *FROM SALES LEFT JOIN STORES on SALES.Store=STORES.Stores where STORES.Store_Status="A" and SALES.County="Polk" ',conn)


#24t
pd.read_sql_query('SELECT SUM(SALES.TOTAL),SUM(SALES.Bottle_qty),Stores.STATUS FROM SALES LEFT JOIN STORES on SALES.Store=STORES.Stores where SALES.County="Polk" ',conn)

#25th 1st 
pd.read_sql_query('SELECT SALES.Store,SALES.Category_name,AVG(SALES.Btl_price),AVG(SALES.Total) FROM SALES LEFT JOIN PRODUCTS on SALES.Item=PRODUCTS.Item_no',conn)


#25th 2nd
pd.read_sql_query('SELECT * FROM SALES LEFT JOIN PRODUCTS on PRODUCTS.Item_no=SALES.Item LEFT JOIN STORES on STORES.Stores=SALES.Store where SALES.Category_name like "%Tequila%" and STORES.Store_address like "%Mason City%" and STORES.Store_Status="A" ',conn)

#25th 3rd
pd.read_sql_query('SELECT * FROM SALES Group by SALES.Store ORDER BY  SALES.Store ASC ',conn)


###EDA
the_whole_df=pd.concat([countries,products,stores],axis=1)
the_whole_df=the_whole_df.drop(['Age','Address_info'],axis=1)#Deleting nan values 

#Grouping and taking out unique value_counts
unique_category_names=the_whole_df['Category_name'].value_counts()

unique_Vendor_name=the_whole_df['Vendor_name'].value_counts()




#Correlation Matrix
the_whole_df['Store_Status']=the_whole_df['Store_Status'].str.replace('A','1')
the_whole_df['Store_Status']=the_whole_df['Store_Status'].str.replace('I','0')

when_active = the_whole_df[(the_whole_df['Store_Status'] == '1')] 
when_active=when_active[['Case_cost','Bottle_price','Shelf_price','Population','Bottle_size']] 
when_active['Bottle_price'] = when_active['Bottle_price'].str.replace('$', '')
when_active['Bottle_price'] = when_active['Bottle_price'].str.replace(',', '')
when_active=when_active.astype(float)
when_active =when_active.corr()    # female corr


fig = plt.figure(figsize=(12,6))
plt.subplot(121)   #  subplot 1 - female
plt.title('Active_Store_Status')
sns.heatmap(when_active, annot=True, fmt='.2f', square=True, cmap = 'Reds_r')



not_when_active = the_whole_df[(the_whole_df['Store_Status'] == '0')] 
not_when_active=not_when_active[['Case_cost','Bottle_price','Shelf_price','Population','Bottle_size']] 
not_when_active['Bottle_price'] = not_when_active['Bottle_price'].str.replace('$', '')
not_when_active['Bottle_price'] = not_when_active['Bottle_price'].str.replace(',', '')
not_when_active=not_when_active.astype(float)
not_when_active =not_when_active.corr()    # female corr
fig = plt.figure(figsize=(12,6))
plt.subplot(121)   #  subplot 1 - female
plt.title('InActive_Store_Status')
sns.heatmap(not_when_active, annot=True, fmt='.2f', square=True, cmap = 'Reds_r')








#BOX-PLOT

#BOX PLOT OF SHELF PRICE
foo = the_whole_df.explode('Shelf_price')
foo['Shelf_price'] = foo['Shelf_price'].astype('float')
sns.boxplot(x='Store_Status',y="Shelf_price",data=foo)
plt.title('SHELF_PRICE AND STATUS')
plt.show()


#VOILIN-PLOTS OF BOTTLE PRICE
foo = the_whole_df.explode('Bottle_price')
foo['Bottle_price'] = foo['Bottle_price'].str.replace('$', '')
foo['Bottle_price'] = foo['Bottle_price'].str.replace(',', '')
foo['Bottle_price'] = foo['Bottle_price'].astype('float')
sns.violinplot(x='Store_Status',y="Bottle_price",data=foo)
plt.title('BOTTLE_PRICE AND STORE_STATUS')
plt.show()


##PAIR PLOTS_Bottle_price
foo = the_whole_df.explode('Bottle_price')
foo['Bottle_price'] = foo['Bottle_price'].str.replace('$', '')
foo['Bottle_price'] = foo['Bottle_price'].str.replace(',', '')
foo['Bottle_price'] = foo['Bottle_price'].astype('float')
foo['List_date'] = pd.to_datetime(foo['List_date'])##pair plot needs one variable as date or year
sns.pairplot(data =foo,hue='Store_Status',height=4 ,vars=['Bottle_price','List_date'])
plt.show()

##PAIR PLOTS_OF SHELF_PRICE
foo = the_whole_df.explode('Shelf_price')
foo['Shelf_price'] = foo['Shelf_price'].astype('float')
foo['List_date'] = pd.to_datetime(foo['List_date'])##pair plot needs one variable as date or year
sns.pairplot(data =foo,hue='Store_Status',height=4 ,vars=['Shelf_price','List_date'])
plt.show()

##PAIR PLOTS_OF CASE_COSt
foo = the_whole_df.explode('Case_cost')
foo['Case_cost'] = foo['Case_cost'].astype('float')
foo['List_date'] = pd.to_datetime(foo['List_date'])##pair plot needs one variable as date or year
sns.pairplot(data =foo,hue='Store_Status',height=4 ,vars=['Case_cost','List_date'])
plt.show()


 
#Countour-plots_Bottle_price
foo = the_whole_df.explode('Bottle_price')
foo['Bottle_price'] = foo['Bottle_price'].str.replace('$', '')
foo['Bottle_price'] = foo['Bottle_price'].str.replace(',', '')
foo['Bottle_price'] = foo['Bottle_price'].astype('float')
foo['List_date'] = pd.to_datetime(foo['List_date'])##pair plot needs one variable as date or year
sns.jointplot(x='Bottle_price',y='List_date',data=foo,kind='kde')
plt.title('Bottle Price',x=4)
plt.show()


#Contour Plots case_clots
foo=the_whole_df.explode('Case_cost')
foo['Case_cost'] = foo['Case_cost'].astype('float')
foo['List_date'] = pd.to_datetime(foo['List_date'])##pair plot needs one variable as date or year

sns.jointplot(x='Case_cost',y='List_date',data=foo,kind='kde')
plt.show()