import pandas as pd
import psycopg2
import pandas as pds
from sqlalchemy import create_engine
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
ae=create_engine('postgresql+psycopg2://postgres:postgres@127.0.0.1',pool_recycle=3600)
dbconn= ae.connect()
df= pds.read_sql("select * from \"test\"",dbconn)
pds.set_option('display.expand_frame_repr',False)
len_col=len(df.columns)

# print(df.columns)


df["AddressLine2"]=df["AddressLine2"].replace(['NULL'],'')
df["AddressLine2"]=df["AddressLine2"].replace([pd.NA],'')
df["MiddleName"]=df["MiddleName"].replace(['NULL'],'')
df["MiddleName"]=df["MiddleName"].replace([pd.NA],'')
df["AddressLine1"]=df["AddressLine1"]+ df["AddressLine2"]
# print(df["MiddleName"])
def par_ratio(x,y):
    r=fuzz.partial_ratio(x,y)
    return r
def sort_ratio(x,y):
    r=fuzz.token_sort_ratio(x,y)
    return r
def w_ratio(x,y):
    r=fuzz.WRatio(x,y)
    return r
def avg(x,y,z):
    ans= (x+y+z)/3
    return ans
same_rows=[]
scores=[]
labels=[]
test_col=(1,2,3,5,7,9,10,11,12,13)
for row_no in range(len(df)-1):
    for comp_row in range(row_no+1,len(df)):
        temp=[0 for i in range(14)]
        itr=0
        for col_no in test_col:

            ele=df.iat[row_no,col_no]
            comp_ele=df.iat[comp_row,col_no]
            if ele !='' or comp_ele!='' or ele is not pd.NA or comp_ele is not pd.NA:
                r1=par_ratio(str(ele),str(comp_ele))
                r2=w_ratio(str(ele),str(comp_ele))
                r3=sort_ratio(str(ele), str(comp_ele))
                average=avg(r1,r2,r3)
                temp[col_no]=average
        scores.append(temp)
        # Making Label dataset
        # if df.iat[row_no,4]==df.iat[comp_row,4]:
        #     labels.append("Duplicate")
        # else:
        #     labels.append("Not-Duplicate")
        count=0
        for ele in temp:
            if ele>=90:
                count+=1
            if count>=4:
                same_rows.append((row_no,comp_row))
# df_lab=pd.DataFrame(labels)
# df_lab.to_csv(r'C:\Users\averm200\Desktop\labels.csv')
df_sco=pd.DataFrame(scores)
df_sco.to_csv(r'C:\Users\averm200\Desktop\scores.csv')
print(same_rows)
print(labels)
