# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 11:59:35 2019

@author: Jhon Valderrama
"""
import json
import pandas as pd 
from pandas import DataFrame

def reorder(out):
    with open(out) as json_file:  
        data = json.load(json_file)
    stages=data.keys()
    type_photo=data[list(stages)[0]].keys()
    indices=data[list(stages)[0]][list(type_photo)[0]].keys()
    statistics=list(data[list(stages)[0]]
    [list(type_photo)[0]][list(data[list(stages)[0]]
    [list(type_photo)[0]].keys())[0]][0].keys())
    dic={}
    dic_stages={}
    list_total=[]
    for i in data:
#        print(i)
        dic={}
        for j in data[i]:
            if j!="DEM":
#                print(j)
                
                for k in data[i][j]: # ALl indices 
#                    print(k)
                    list_total=[]
                    for h in data[i][j][k]: # statistics dictionary
#                        print(h)
                        list_stat=[]
                        for l in h:
                            list_stat.append(h[l])
                        
                        list_total.append(list_stat)
                        
                    dic[k]=list_total
#                    print(k)
#                print(dic)    
                        
        dic_stages[i]=dic
    return [dic_stages,list(stages),list(indices),statistics]

def create_dataframe(list_data,statistics,dir_agronomic_data):
    agronomic_data=pd.read_csv(dir_agronomic_data)
    g=agronomic_data.groupby("STAGE")
    list_stages_csv=list(g.groups.keys())
#    for i in range(len(list_data[2])):
#        list_data[2][i]=list_data[2][i] + "_" + statistics
    dic={}
    list_dataframes=[]
#    print(list_data[1])
#    print(list_stages_csv)
    for i in range(len(list_data[1])):
#        print(list_stages[i])
#        print(i)
        if list_data[1][i] in list_stages_csv:
            
            whole=[]
            for j in list_data[2]:
#                print(j)
                df=DataFrame(list_data[0][list_data[1][i]][j],columns=list_data[3])
                df= df[[statistics]]
                df.columns=[j + "_" + statistics]
                df
                whole.append(df)
                
#            print(list_data[1][i])
            agronomic_dataframe=(g.get_group(list_data[1][i])).reset_index()
            del agronomic_dataframe["TIMESTAMP"]
#            del agronomic_dataframe["STAGE"]
#            del agronomic_dataframe["ID"]
            del agronomic_dataframe["index"]
            
            for m in list(agronomic_dataframe.keys()):
#                print(m)
                if agronomic_dataframe[m].dtypes == object and m!="STAGE" and m!= "ID": 
                    agronomic_dataframe[m] = agronomic_dataframe[m].astype(float)
            agronomic_dataframe["ID"]=agronomic_dataframe["ID"].astype(int)
            whole.append(agronomic_dataframe)
#            print(agronomic_dataframe)
#            dic[list_data[1][i]]=pd.concat(whole,axis=1)
            list_dataframes.append(pd.concat(whole,axis=1))
#    print(list_dataframes)
    mulindex=pd.concat(list_dataframes)
    mulindex=mulindex.set_index(["STAGE","ID"])
                
    return mulindex
#        
        
            
               
                
                
            
            
            
        
    
    
                    
                
                