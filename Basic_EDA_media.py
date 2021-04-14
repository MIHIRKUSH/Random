import pandas as pd
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ba=pd.read_excel('F:/Test 2.xlsx',sheet_name=0)
pa=pd.read_excel('F:/Test 2.xlsx',sheet_name=1)
ia=pd.read_excel('F:/Test 2.xlsx',sheet_name=2)
da=pd.read_excel('F:/Test 2.xlsx',sheet_name=3)

def columns(dataframe):
    col_data =dataframe.iloc[1]
    col_list=[]
    for i in range(len(col_data)):
        col_list.append(col_data[i])
    dataframe.columns=col_list
    dataframe=dataframe.iloc[2:]
    return dataframe

ba=columns(ba)
pa=columns(pa)
ia=columns(ia)
da=columns(da)
ba.columns=['Month', 'Product', 'Campaign ID', 'AD set ID', 'Behaviors',
       'Behaviour Category', 'Reach', 'Impression', 'Click', 'Cost(USD)',
       'Click conversion', 'View conversion',
       'Total conversion']
#For BA
Behaviour=pd.DataFrame(ba['Behaviour Category']).drop_duplicates()
be_col_value=pd.DataFrame(ba['Behaviour Category']).value_counts()





#2D Scatter Plot For Behaviour category Between No devce and under 1 Year 
#We can do the many combinations between those 4 vraibales ,No-device,1 y,1 to 1.5 years and so on
no=pd.DataFrame()
for index,row in ba.iterrows():
    if (row['Behaviour Category']=='No device' or   row['Behaviour Category']=='Under 1y'):
        no=pd.concat([no,row],axis=1)

no=no.transpose()
#For Reach and Click
sns.set_style("whitegrid")
sns.FacetGrid(no,hue="Behaviour Category",height=5).map(plt.scatter,"Reach", "Click").add_legend()  
plt.show()

#For Reach and Impression 
sns.set_style("whitegrid")
sns.FacetGrid(no,hue="Behaviour Category",height=5).map(plt.scatter,"Reach", "Impression").add_legend()  
plt.show()


#For Reach and Impression 
sns.set_style("whitegrid")
sns.FacetGrid(no,hue="Behaviour Category",height=5).map(plt.scatter,"Click", "Impression").add_legend()  
plt.show()


##CDF OF REACH and  WITH NO DEVICE
##On the Y axis it show Probablity 
#As most of the points are 0 ,the graph tends to fall sharply 
#CDF denotes the numbers of points which are <= for point on the x-axis with its probablity on the Y-axis
no=ba.loc[ba['Behaviour Category']=='No device']
count,edges=np.histogram(no['Reach'],bins=10,density=True) 
pdf_age=count/sum(count)
cdf=np.cumsum(pdf_age)
plt.title('People who survived more than 5 years')
plt.xlabel('AGE')
plt.plot(edges[1:],cdf,label='CDF')
plt.plot(edges[1:],pdf_age,label='PDF')
plt.legend()


##CDF OF Impression and  WITH NO DEVICE
count,edges=np.histogram(no['Impression'],bins=10,density=True) 
pdf_age=count/sum(count)
cdf=np.cumsum(pdf_age)
plt.title('People who survived more than 5 years')
plt.xlabel('AGE')
plt.plot(edges[1:],cdf,label='CDF')
plt.plot(edges[1:],pdf_age,label='PDF')
plt.legend()


##CDF OF Impression and  WITH NO DEVICE
count_imp_C,edges_imp_C=np.histogram(no['Click'],bins=10,density=True) 
pdf_age_imp_C=count_imp_C/sum(count_imp_C)
cdf_imp_C=np.cumsum(pdf_age_imp_C)
plt.xlabel('Click')
plt.plot(edges[1:],cdf_imp_C,label='CDF')
plt.plot(edges[1:],pdf_age_imp_C,label='PDF')
plt.legend()







#PDF #you can use displot also for histograms
#Height represets the number of points of a paticular the category in the behaviour category column ,it represent the density of the points 
#THe smooth lines are PDFs of the histogram 
#PDF represents how many points on the X-axis and its probablity on the Y -axis
#becuase most of the rows are empty the density is hightest at 0 

#For View Conversion
sns.FacetGrid(ba,hue=ba.columns[5] ,height=8).map(sns.distplot,ba.columns[9]).add_legend()
plt.title('Cost')
plt.show()

#Reach
sns.FacetGrid(ba,hue=ba.columns[5] ,height=8).map(sns.distplot,ba.columns[6]).add_legend()
plt.title('Reach')
plt.show()



#Impression
sns.FacetGrid(ba,hue=ba.columns[5] ,height=8).map(sns.distplot,ba.columns[7]).add_legend()
plt.title('Reach')
plt.show()




###Univariete Analysis
sns.set_style("whitegrid")
sns.FacetGrid(ba,hue=ba.columns[5],height=5).map(plt.scatter,ba.columns[9]).add_legend()
plt.title('STATUS AND NODES')
plt.show()