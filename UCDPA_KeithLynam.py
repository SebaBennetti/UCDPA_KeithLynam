#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# I built my own dictionary consisting all US states divided into four distinct areas
US_State_regions = {"Northeast":[ "Connecticut","Maine","Massachusetts","New Hampshire",
                                 "New Jersey","New York","New York City","Pennsylvania","Rhode Island","Vermont"],
                    "Midwest":["Illinois","Indiana","Iowa","Kansas","Michigan","Minnesota","Missouri","Nebraska",
                               "North Dakota","Ohio","South Dakota","Wisconsin"],
                    "South":["Alabama","Arkansas","Delaware","District of Columbia","Florida",
                             "Georgia","Kentucky","Louisiana","Maryland","Mississippi","North Carolina",
                             "Oklahoma","South Carolina","Tennessee","Texas","Virginia","West Virginia","Puerto Rico"],                    
                    "West":["Alaska","Arizona","California","Colorado","Hawaii","Idaho","Montana","Nevada",
                            "New Mexico","Oregon","Utah","Washington","Wyoming"]}

# imported csv file locally path file name "data"
# Deaths by the weeks, by state of occurrence, and by select causes for 2014-2018 kaggle
US_Death_data = pd.read_csv(r"C:\Users\lynam\OneDrive\Desktop\data.csv", sep = ',')

# print check the dataframe structure and contained info
print (US_Death_data.head())
print (US_Death_data.shape)
print (US_Death_data.info())
# print (US_State_regions)


# In[2]:


# performed a count function to show number of missing values in each column
missing_value = US_Death_data.isnull().sum()
print (missing_value)


# In[3]:


# missing values  are replaced with zeros as a test exercise
blank_replace_zero = US_Death_data.fillna(0)
print (blank_replace_zero.isna().sum())


# In[4]:


# the least relevant data columns are dropped
# flag_ columns not really relevant to our enquiry
US_Death_data_drop = US_Death_data.drop(axis=1, columns=["flag_allcause","flag_natcause",
                                                         "flag_sept","flag_neopl","flag_diab", 
                                                         "flag_alz","flag_inflpn","flag_clrd","flag_otherresp",
                                                         "flag_nephr","flag_otherunk","flag_hd","flag_stroke" ])
# US_Death_data_drop = US_Death_data.drop([13892,14095], axis=0, inplace =True



print (US_Death_data_drop.columns)
print (US_Death_data_drop.head())


# In[5]:


# For loop, here we added a new column to US_Death_data_drop, region set blank
# Used the for loop to check Jurisdiction_of_Occurrence against US State US_State_regions entries in the dictionary, then designated the applicable key "region" to the region column



US_Death_data_drop["region"] = ''
        
for key in US_State_regions.items():
    
    for i in range(len(US_Death_data_drop)):
        
        Jurisdiction_of_Occurrence = US_Death_data_drop['Jurisdiction_of_Occurrence'].values[i]
                
        if (Jurisdiction_of_Occurrence in key[1]):
            US_Death_data_drop.at[i, 'region'] = key[0]
           
print(US_Death_data_drop.head())
print(US_Death_data_drop.info())


# In[6]:


# Here I dropped the rows with missing values in US_Death_data_drop to remove all rows with nan

US_Death_data_dropV2 =US_Death_data_drop.dropna()
print (US_Death_data_dropV2.head())
print (US_Death_data_dropV2.info())
#No missing values left within the DataFrame


# In[8]:


# sort under year / week ending with region in ascending order
US_Death_data_sorted = US_Death_data_dropV2.sort_values(["MMWR_Year","region"])
print (US_Death_data_sorted.head())


# In[9]:


# reset the index to show order ascending
US_Death_data_sorted_index=US_Death_data_sorted.reset_index(drop=True)
print (US_Death_data_sorted_index.head())


# In[10]:


# Here I added a column "Death Totals" showing the  sum of each cause of death
# A subset is created, slicing all rows with year, Death Totals and region 
US_Death_data_sorted_index["Death_Totals"]=US_Death_data_sorted_index["All  Cause"]+ US_Death_data_sorted_index["Natural Cause"]+US_Death_data_sorted_index["Septicemia "]+US_Death_data_sorted_index["Malignant_neoplasms"]+US_Death_data_sorted_index["Diabetes_mellitus "]+US_Death_data_sorted_index["Alzheimer disease "]+US_Death_data_sorted_index["Influenza and pneumonia "]+US_Death_data_sorted_index["Chronic lower respiratory diseases "]
+ US_Death_data_sorted_index["Other diseases of respiratory system "]+US_Death_data_sorted_index["Nephritis, nephrotic syndrome and nephrosis "]+US_Death_data_sorted_index["Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified"]+US_Death_data_sorted_index["Diseases of heart "]+US_Death_data_sorted_index["Cerebrovascular diseases"]
print (US_Death_data_sorted_index.head())
US_Death_total_data_region = US_Death_data_sorted_index.loc[:,["MMWR_Year","region","Death_Totals"]]
print (US_Death_total_data_region.head())


# In[11]:


# groupby year, region and sum of each region's Death Totals
region_Death = US_Death_total_data_region.groupby(["MMWR_Year","region"])["Death_Totals"].sum().reset_index()
print (region_Death)


# In[12]:


# Here a line plot shows each region total deaths from 2014 to 2018
# First insight
lineplot1=sns.lineplot(x="MMWR_Year", y="Death_Totals",data=region_Death,hue="region")
lineplot1.set_title("Total Deaths in each region 2014 - 2018")
lineplot1.set(xlabel="year", ylabel="Total Death Figures (x100000)")
plt.show()


# In[13]:


# The Def function is employed to lineplot any US State the user inputs, to show that state's
# Death Totals between 2014 & 2018
def my_function(Jurisdiction_of_Occurrence):
    state_file=US_Death_data_sorted_index.loc[US_Death_data_sorted_index["Jurisdiction_of_Occurrence"]==Jurisdiction_of_Occurrence]
        
    func_lineplot=sns.lineplot(x="MMWR_Year",y="Death_Totals",data=state_file,hue="Jurisdiction_of_Occurrence")
    func_lineplot.set_title("Total Death in " + Jurisdiction_of_Occurrence + " USA 2014 - 2018")
    func_lineplot.set(xlabel="year",ylabel="Total Death Figures (x10")
    plt.show()
    
my_function("Alabama")


# In[14]:


# Here I used the iterrows function to loop through the dataframe to 
# display the Natural cause of Death info
for ind,row in US_Death_data_sorted_index.iterrows():
    print (" In ", str(row["MMWR_Year"]), " ",row["Jurisdiction_of_Occurrence"]," had ", str(row["Natural Cause"])," Natural Cause Deaths.")


# In[18]:


# Dataframe merger, subset 2 dataframes and merged them

print (US_Death_data_sorted_index.info())
US_Blood_related_Deaths = US_Death_data_sorted_index[["MMWR_Year","Jurisdiction_of_Occurrence","Septicemia ","Diabetes_mellitus "]]
print (US_Blood_related_Deaths.head())
US_Respitory_Deaths = US_Death_data_sorted_index[["MMWR_Year","Jurisdiction_of_Occurrence","Influenza and pneumonia ","Chronic lower respiratory diseases "]]
print (US_Respitory_Deaths.head())
US_Combined_Deaths = US_Blood_related_Deaths.merge(US_Respitory_Deaths,left_index=True,right_index=True)
print (US_Combined_Deaths.info())


# In[15]:


# numpy function
# Here I used the numpy function to calc the  max, min, mean & median Death Totals in each region
# (each year has similar totals which result in flat ish lineplots)
print (US_Death_data_sorted_index.info())
Death_info = US_Death_data_sorted_index.groupby(["MMWR_Year","region"])["Death_Totals"].agg([np.max,np.min,np.mean,np.median])
print (Death_info)
bar=sns.lineplot(x="MMWR_Year",y="median",hue="region",data=Death_info)
bar.set_title("Median Death Figures in the US 2014 - 2018")
bar.set(xlabel="MMWR_Year", ylabel="Median Death Figures")
plt.show()


# In[16]:


# Second Insight 
# Correlation between all causes and not elswhere classified causes of death
print (US_Death_data_sorted_index.info())
sns.lmplot(x="All  Cause",y="Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified",ci=50,data=US_Death_data_sorted_index,palette="Set2",scatter_kws={"s": 3},line_kws={'color': 'red'})
plt.xlabel("All Causes (x 10")
plt.ylabel("Unclassified (x 100")
plt.title("Correlation Between All Causes And Unclassified", y =1.1)
plt.show()


# In[28]:


# Third Insight 
# From the Median Death Figures in the US between  2014 - 2018
# we see death figures peaked slightly around 2017 in South, Midwest and Northeast
# Firstly we want to reveal the top 5 states in each of these US regions with the  highest death figures during 2017
west_south_midwest = US_Death_data_sorted_index[(US_Death_data_sorted_index["MMWR_Year"] == 2017)
                                      &(US_Death_data_sorted_index["region"].isin(["West","South","Midwest"]))].sort_values(["region","Death_Totals"],ascending = [True,False])
print (west_south_midwest.head())


# In[18]:


smnbar=sns.catplot(x="Death_Totals",y="Jurisdiction_of_Occurrence",
                   data=west_south_midwest.groupby("region").apply(lambda x: x.nlargest(5,["Death_Totals"])),
                   kind="bar", hue = "region")
smnbar.fig.suptitle("     Top 5 highest death figures in West, South & Midwest", y=1.1)
smnbar.set(xlabel = "Total death (x100)", ylabel = "Top 5 states in West, South, Midwest")
plt.show()        


# In[19]:


# We have the Top 5 highest death figures in West, South & Midwest US.
# we want to show the comparison of Blood related Deaths and Respitory Deaths in 2017
# we will use total of Septicemia and Diabetes_mellitus as blood related deaths
# we will use total of Influenza and pneumonia and Chronic lower respiratory diseases as Respitory related Deaths
west_south_midwest["Total_US_Blood_related_Deaths"]=west_south_midwest["Septicemia "]+west_south_midwest["Diabetes_mellitus "]
west_south_midwest["Total_US_Respitory_Deaths"]=west_south_midwest["Influenza and pneumonia "]+west_south_midwest["Chronic lower respiratory diseases "]
print (west_south_midwest.head())
print (west_south_midwest.info())


# In[20]:


Respitory=sns.lmplot(data=west_south_midwest,x="All  Cause",y="Total_US_Respitory_Deaths",hue="region",ci=95)
Respitory.fig.suptitle("Correlation between All Causes of death and Respiritory deaths within three regions during 2017",y=1.02)
Respitory.set(xlabel="All causes (x100)",ylabel="Total_US_Respitory_Deaths")
plt.show()


# In[21]:


Blood=sns.lmplot(data=west_south_midwest,x="All  Cause",y="Total_US_Blood_related_Deaths",hue="region",ci=95)
Blood.fig.suptitle("Correlation between All Causes of Death and Total Blood Related Deaths within three regions during 2017",y=1.02)
Blood.set(xlabel="All Causes (x100)",ylabel="Total Blood Related Deaths")
plt.show()


# In[22]:


# differentiate total death figures for all regions in 2016, 2017 and 2018
year=(2016,2017,2018)
differentiate=US_Death_data_sorted_index[US_Death_data_sorted_index["MMWR_Year"].isin(year)
                                      ].sort_values(["MMWR_Year","region","Death_Totals"],ascending = [True,True,False])
print (differentiate)


# In[23]:


differentiate_year=sns.catplot(x="region",y="Death_Totals",kind="bar",data=differentiate,hue="MMWR_Year",ci=None)
differentiate_year.fig.suptitle("Comparison of total death figures in each region USA in 2016,2017 & 2018",y=1.02)
differentiate_year.set(xlabel="region", ylabel="Death total figures")
plt.show()


# In[24]:


# fourth insight
# top 5 states in each region in 2018 are they still the same?
top5_2018 = US_Death_data_sorted_index[(US_Death_data_sorted_index["MMWR_Year"] == 2018)
                                      &(US_Death_data_sorted_index["region"].isin(["West","South","Midwest"]))].sort_values(["region","Death_Totals"],ascending = [True,False])
          
print (top5_2018.head())

top5bar_2018=sns.catplot(x="Death_Totals",y="Jurisdiction_of_Occurrence",
                   data= top5_2018.groupby("region").apply(lambda x: x.nlargest(5,["Death_Totals"])),
                   kind="bar", hue = "region")
top5bar_2018.fig.suptitle("     Top 5 highest death figures in West, South & Midwest 2018", y=1.02)
top5bar_2018.set(xlabel = "Total Crime (x1000000)", ylabel = "     Top 5 highest death figures in West, South & Midwest")
plt.show()   


# In[35]:


top5bar_2018=sns.catplot(x="Death_Totals",y="Jurisdiction_of_Occurrence",
                   data= top5_2018.groupby("region").apply(lambda x: x.nlargest(5,["Death_Totals"])),
                   kind="bar", hue = "region")
top5bar_2018.fig.suptitle("     Top 5 highest death figures in West, South & Midwest 2018", y=1.02)
top5bar_2018.set(xlabel = "Death Totals (x10)", ylabel = "     Top 5 highest death figures in West, South & Midwest")
plt.show()   


# In[25]:


# fifth insight 
# shows the death figues for each cause of death from each region 2014 - 2018
Death_cause = US_Death_data_sorted_index.groupby(["MMWR_Year","region"])[["All  Cause",
                                             "Natural Cause","Septicemia ",
                                                              "Malignant_neoplasms",
                                                              "Diabetes_mellitus ",
                                                              "Alzheimer disease ","Influenza and pneumonia ",
                                                              "Chronic lower respiratory diseases ","Other diseases of respiratory system ",
                                                               "Nephritis, nephrotic syndrome and nephrosis ", "Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified",
                                                                      "Diseases of heart ","Cerebrovascular diseases" ]].agg(np.mean,).reset_index()
print (Death_cause)
print(Death_cause.info())


# In[26]:


Death_cause_all_causes=sns.lineplot(x="MMWR_Year",y="All  Cause",data=Death_cause,hue="region")
Death_cause_all_causes.set_title("Mean All Causes of Death figures in each US Region 2014 - 2018")
Death_cause_all_causes.set(xlabel="Year",ylabel="All Cause figures")
plt.show()

Death_cause_natural=sns.lineplot(x="MMWR_Year",y="Natural Cause",data=Death_cause,hue="region")
Death_cause_natural.set_title("Mean Natural Causes of Death figures in each US Region 2014 - 2018")
Death_cause_natural.set(xlabel="Year",ylabel="Natural Causes figures")
plt.show()

Death_cause_septicemia=sns.lineplot(x="MMWR_Year",y="Septicemia ",data=Death_cause,hue="region")
Death_cause_septicemia.set_title("Mean Septicemia Death figures in each US Region 2014 - 2018")
Death_cause_septicemia.set(xlabel="Year",ylabel="Septicemia figures")
plt.show()


Death_cause_neoplasms=sns.lineplot(x="MMWR_Year",y="Malignant_neoplasms",data=Death_cause,hue="region")
Death_cause_neoplasms.set_title("Mean Malignant neoplasms Death figures in each US Region 2014 - 2018")
Death_cause_neoplasms.set(xlabel="Year",ylabel="Malignant neoplasms figures")
plt.show()

Death_cause_diabetes=sns.lineplot(x="MMWR_Year",y="Diabetes_mellitus ",data=Death_cause,hue="region")
Death_cause_diabetes.set_title("Mean Diabetes mellitus Death figures in Each Region USA 1979 - 2019")
Death_cause_diabetes.set(xlabel="Year",ylabel="Diabetes mellitus figures")
plt.show()

Death_cause_alzheimer=sns.lineplot(x="MMWR_Year",y="Alzheimer disease ",data=Death_cause,hue="region")
Death_cause_alzheimer.set_title("Mean Alzheimer disease Death figures in each US Region 2014 - 2018")
Death_cause_alzheimer.set(xlabel="Year",ylabel="Alzheimer disease figures")
plt.show()

Death_cause_pneumonia=sns.lineplot(x="MMWR_Year",y="Influenza and pneumonia ",data=Death_cause,hue="region")
Death_cause_pneumonia.set_title("Mean Influenza & pneumonia Death figures in each US Region 2014 - 2018")
Death_cause_pneumonia.set(xlabel="Year",ylabel="Influenza & pneumonia figures")
plt.show()

Death_cause_chronres=sns.lineplot(x="MMWR_Year",y="Chronic lower respiratory diseases ",data=Death_cause,hue="region")
Death_cause_chronres.set_title("Mean Chronic lower respiratory diseases Death figures in each US Region 2014 - 2018")
Death_cause_chronres.set(xlabel="Year",ylabel="Chronic lower respiratory diseases figures")
plt.show()

Death_cause_othres=sns.lineplot(x="MMWR_Year",y="Other diseases of respiratory system ",data=Death_cause,hue="region")
Death_cause_othres.set_title("Mean Other diseases of respiratory system Death figures in each US Region 2014 - 2018")
Death_cause_othres.set(xlabel="Year",ylabel="Other diseases of respiratory system figures")
plt.show()

Death_cause_nephrotic=sns.lineplot(x="MMWR_Year",y="Nephritis, nephrotic syndrome and nephrosis ",data=Death_cause,hue="region")
Death_cause_nephrotic.set_title("Mean Nephritis, nephrotic syndrome & nephrosis Death figures in each US Region 2014 - 2018")
Death_cause_nephrotic.set(xlabel="Year",ylabel="Nephritis & nephrosis figures")
plt.show()

Death_cause_abnormal=sns.lineplot(x="MMWR_Year",y="Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified",data=Death_cause,hue="region")
Death_cause_abnormal.set_title("Mean Abnormal clinical and laboratory findings, not elsewhere classified Death figures in each US Region 2014 - 2018")
Death_cause_abnormal.set(xlabel="Year",ylabel="Mean Abnormal findings figures")
plt.show()

Death_cause_heart=sns.lineplot(x="MMWR_Year",y="Diseases of heart ",data=Death_cause,hue="region")
Death_cause_heart.set_title("Mean Diseases of Heart Death figures in each US Region 2014 - 2018")
Death_cause_heart.set(xlabel="Year",ylabel="Diseases of Heart Death figures")
plt.show()

Death_cause_cerebro=sns.lineplot(x="MMWR_Year",y="Cerebrovascular diseases",data=Death_cause,hue="region")
Death_cause_cerebro.set_title("Mean Cerebrovascular Diseases Death figures in each US Region 2014 - 2018")
Death_cause_cerebro.set(xlabel="Year",ylabel="Cerebrovascular Diseases Death figures")
plt.show()


# In[30]:


# Retrieve data using online APIs
import requests
authors = requests.get('https://openlibrary.org/search/authors.json?q=j%20k%20rowling')
#authors = authors.json()
pd.DataFrame(authors.json())

print(authors.status_code)
print(authors.text)


# In[ ]:




