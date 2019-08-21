"""
Created on Fri Jul 19 11:59:35 2019

@author: Jhon Valderrama

This module is the controller layer for orthomosaics postprocessing work flow,
it contains the functions to control the funtions implemented in the base layer.
This module let operate and organize the information for the visualization layer.
 """
import json
import pandas as pd
from pandas import DataFrame
import os
import Base_layer as bf


# ------------------------------------------------------


def find_ortho_crop_stages(DIR, stage_feat=None):
    """This function returns a dictionary with each stage of the
    crop found in the DIR directory.Each element of the dictionary
     contains the file path for each orthomosaic found. If it only prefer
     one stage, it must set the stage_feat parameter.
    Args:
        DIR(str): Directory path for the crop stages
        stage_feat(str): Name of the specific stage that it want to get
    Returns:
        there is a only output:
            Dictionary : a dictionary with each stage of the
            crop found in the DIR directory
    """
    if stage_feat is None:
        # a = os.walk(DIR)
        # data = next(a)
        stages = next(os.walk(DIR))[1]
        stages.remove("SHAPES")
        stage_numbers = len(stages)
        variable = stages

    else:
        variable = [stage_feat]
        stage_numbers = 1
    d = {}
    for j in range(stage_numbers):
        aux = os.walk(DIR + "\\" + variable[j])
        temp = next(aux)
        file_names = temp[2]
        string = []
        file_path2 = {}
        for i in range(len(file_names)):
            string.append(file_names[i][0:file_names[i].find(".")].split("_"))
            if "RM" in string[i]:
                file_path2["RM"] = [temp[0], file_names[i], string[i]
                                    [1:len(string[i])]]
            elif "THM" in string[i]:
                file_path2["THM"] = [temp[0], file_names[i], string[i]
                                     [1:len(string[i])]]
            elif "DEM" in file_names[i]:
                file_path2["DEM"] = [temp[0], file_names[i], string[i]
                                     [1:len(string[i])]]
        d[variable[j]] = file_path2
    return d

# ------------------------------------------------------

def stat_ext_4cylces(Dir, cycle,location,field, stage_feat=None):
    """This function returns a json file path. In this file are the all
     statistics for each crop stage, orthomosaic and plot.
    Args:
        Dir(str): Directory path for the crop stages
        cycle(str): the cycle of the farm
        location(str): the location (Department)
        field(str): the name of the farm field place
        stage_feat(str): Name of the specific stage that it want to get
    Returns:
        there is a only output:
            json : a json file path with all statistics of the cycle

    """
    dir_fix_maps = "\\" + location + "\\DRONES\\MAPS\\CIMARRON\\" + field + \
    "\\ALL\\" # it must be revised
    dir_fix_data = "\\" + location + "\\DRONES\\DATA\\CIMARRON\\" + field + \
    "\\ALL\\"
    dir_completed = Dir + dir_fix_maps + cycle
    d = find_ortho_crop_stages(dir_completed, stage_feat)
    mask = dir_completed + "\\" + "SHAPES" + "\\" + "ALL.shp"
    plots = dir_completed + "\\" + "SHAPES" + "\\" + "PLOTS.shp"
    out = Dir + dir_fix_data + cycle + "\\" + cycle + "_" + "STAT.json"
    dic = {}
    ortho = {}
    for i in d:
        ortho = {}
        if "RM" in d[i]:
            ma = bf.mask_ortho(d[i]["RM"][0], d[i]["RM"][1], mask, 0)
#             print(ma)
#             print(d[i]["RM"][0])
#             print(d[i]["RM"][1])
#             print(mask)
            if ma != [1]:
                e = bf.vegetation_extraction(ma[0], 0)
                # anexar error al archivo log
                if e[0] != 1:
                    path = bf.Vis_cal(e[0])
            del ma
            del e
#             print(path)
#             print(len(path))
#             print(plots)
            dic_RM = {}
            for j in path:
                dic_RM[j] = bf.statistics_extraction(path[j], plots)
            # [stat(path[i],plots) for i in range(len(path))]
            ortho["RM"] = dic_RM
#             delete variable
            del dic_RM
            del path

#        if "THM" in d[i]:
#            ma=mask_ortho(d[i]["THM"][0],d[i]["THM"][1],mask,0)

#            ortho["THM"]=[stat(path[i],plots) for i in range(len(path))]

        if "DEM" in d[i]:
            ma = bf.mask_ortho(d[i]["DEM"][0], d[i]["DEM"][1], mask, 0)
            if ma != [1]:
                ortho["DEM"] = bf.statistics_extraction(ma[0], plots)
            del ma
        # print(ortho)
        dic[i] = ortho

    json_file = json.dumps(dic)
    f = open(out, "w")
    f.write(json_file)
    f.close()
    return out

# ------------------------------------------------------

def reorder(Dir, cycle,location,field):
    """This function returns a list with the next elements:
       1) dictionary: dictionary of crop stages, in each element of this
          dictionary are the information about Vis, dem and thm for each plot
          of each crop stages.
       2) list: stages names
       3) list: VIs names
       4) list: name of statistics variables
    Args:
        Dir(str): Directory path for the crop stages
        cycle(str): the cycle of the farm
        location(str): the location (Department)
        field(str): the name of the farm field place
    Returns:
        there is a only output:
            list

    """
    dir_fix_jsons = Dir + "\\" + location + "\\DRONES\\DATA\\CIMARRON\\" + field + \
    "\\ALL\\" + cycle + "\\" + cycle + "_" + "STAT.json"
    with open(dir_fix_jsons) as json_file:
        data = json.load(json_file)
    stages=data.keys()
    type_photo=data[list(stages)[0]].keys()
    ortho_data_plots=data[list(stages)[0]][list(type_photo)[0]].keys()
    ortho_data_plots=list(ortho_data_plots)
    ortho_data_plots.append("THM")
    ortho_data_plots.append("DEM")
    plots_number=len(data[list(stages)[0]][list(type_photo)[0]][ortho_data_plots[0]])
    statistics=list(data[list(stages)[0]]
    [list(type_photo)[0]][list(data[list(stages)[0]]
    [list(type_photo)[0]].keys())[0]][0].keys())
    statistics_len=len(statistics)

    dic={}
    dic_stages={}
    list_total=[]
    for i in data: # i is stages
#        print(i)
        dic={}
        for j in data[i]: #j is the type of orthomosaic
            if not("DEM" in data[i]):
                dic["DEM"]= [[None] * statistics_len]*plots_number
            if not("THM" in data[i]):
                dic["THM"]= [[None] * statistics_len]*plots_number
            if not("RM" in data[i]):
                dic["RM"]= [[None] * statistics_len]*plots_number
            if j=="RM":
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
            if j=="DEM":
                list_total=[]
                for h in data[i][j]:
                    # print(h)
                    list_stat=[]
                    for l in h:
                        list_stat.append(h[l])
                        # print(h[l])
                    list_total.append(list_stat)
                dic["DEM"]=list_total

                # print(i)
                # print(j)
                # print(data[i][j]) # DEM
            # if j=="THM":
        dic_stages[i]=dic
    return [dic_stages,list(stages),ortho_data_plots,statistics]

# ------------------------------------------------------

def create_consolidated_dataframe(data_list,statistics,Dir, cycle,location,field):
    """This function returns a consolidated dataframe  with statistics data
        from orthomosaics and agronomic data:
    Args:
        data_list: list[dictionary,list,list,list] --> see reorder function
        Dir(str): Directory path for the crop stages
        cycle(str): the cycle of the farm
        location(str): the location (Department)
        field(str): the name of the farm field place
    Returns:
        there is a only output:
            Consolidated Dataframe

    """
    dir_fix_csv = Dir + "\\" + location + "\\DRONES\\DATA\\CIMARRON\\" + field + \
    "\\ALL\\" + cycle + "\\" +  "agronomic_data.csv"
    agronomic_data=pd.read_csv(dir_fix_csv) # read agronomic_data
    g=agronomic_data.groupby("STAGE")
    list_stages_csv=list(g.groups.keys())
    dic={}
    list_dataframes=[]
    for i in range(len(data_list[1])): # from i to number of stages
        if data_list[1][i] in list_stages_csv: # to filter the stages in csv file
            whole=[]
            for j in data_list[2]: #from j to ortho_data_plots
                data_stages_plots_dic=data_list[0]
                stages=data_list[1][i]
                #create a dataframe with each ortho_data_plots element
                df=DataFrame(data_stages_plots_dic[stages][j],columns=data_list[3])
                df= df[[statistics]]
                df.columns=[j + "_" + statistics]
                df
                whole.append(df)
            agronomic_dataframe=(g.get_group(data_list[1][i])).reset_index()
            del agronomic_dataframe["TIMESTAMP"]
            del agronomic_dataframe["index"]
            for m in list(agronomic_dataframe.keys()):
                if agronomic_dataframe[m].dtypes == object and m!="STAGE" and m!= "ID":
                    agronomic_dataframe[m] = agronomic_dataframe[m].astype(float)
            agronomic_dataframe["ID"]=agronomic_dataframe["ID"].astype(int)
            whole.append(agronomic_dataframe)
            list_dataframes.append(pd.concat(whole,axis=1))
    mulindex=pd.concat(list_dataframes)
    mulindex=mulindex.set_index(["STAGE","ID"])
    return mulindex

# ------------------------------------------------------
