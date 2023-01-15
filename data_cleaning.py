import numpy as np
import pandas
import pandas as pd


# CP columns means the patent is a citation of these patents
def main():
    data = pd.read_excel("./data2.xlsx")
    # columns contain nan have quantity of 125
    # print(data[data.isnull()].columns.values)
    # print(len(data[data.isnull()].columns.values))
    # delete columns contains nan
    # data = data.dropna(axis=1)
    # print(data.columns.values)
    result = data[["Publication Number", "Publication Date"]]
    # print the quantity of nan of each column
    # print(data_1.isna().sum())
    # result
    # Publication Number      0
    # Backward Citations    144
    # Forward Citations     260
    # Publication Date        0
    # dtype: int64
    # add CP and label to columns
    result = result.reindex(columns=result.columns.tolist() + ["CP", "label"])
    result[['CP', 'label']] = result[['CP', 'label']].astype('object')
    #
    F_citations = data["Forward Citations"]
    B_citations = data["Backward Citations"]
    # manage to clean the data and save it to CP
    # first step:
    for i in range(len(B_citations)):
        tmp: list[str] = str(B_citations[i]).split("|")
        if tmp[0] == "nan":
            continue
        tmp_1 = []
        for j in tmp:
            tmp_2 = j.split(" ")
            if tmp_2[0] == "":
                tmp_1.append(tmp_2[1])
            else:
                tmp_1.append(tmp_2[0])
        # now we get the data of citation patent
        after = cleaner(tmp_1, data["Publication Number"])
        if pd.isnull(result.at[i, 'CP']):
            result.at[i, 'CP'] = pd.array([])
        result.at[i, 'CP'] = pd.array(list(set(list(result.at[i, "CP"]) + after)))
    # the second loop
    for i in range(len(F_citations)):
        tmp = str(F_citations[i]).split("|")
        if tmp[0] == "nan":
            continue
        tmp_1 = []
        for j in tmp:
            tmp_2 = j.split(" ")
            if tmp_2[0] == "":
                tmp_1.append(tmp_2[1])
            else:
                tmp_1.append(tmp_2[0])
                # now we get the data of citation patent
        after = cleaner(tmp_1, data["Publication Number"])
        for j in range(len(after)):
            rows_index = result.loc[result['Publication Number'] == after[j]].index.values[0]
            rows_index = int(rows_index)
            if pd.isnull(result.at[rows_index, 'CP'][0]):
                result.at[rows_index, 'CP'] = pd.array([])
            result.at[rows_index, 'CP'] = list(set(list(result.loc[rows_index, "CP"]) + [after[j]]))
    CP_rows = result["CP"]
    for i in range(len(CP_rows)):
        tmp = pd.isna(CP_rows[i])
        if type(tmp) == np.ndarray:
            if len(tmp) == 0:
                result.drop(i, axis=0, inplace=True)
        elif tmp:
            result.drop(i, axis=0, inplace=True)
    return result


#     #<class 'pandas.core.frame.DataFrame'>
# Int64Index: 57 entries, 4 to 287
# Data columns (total 4 columns):
#  #   Column              Non-Null Count  Dtype
# ---  ------              --------------  -----
#  0   Publication Number  57 non-null     object
#  1   Publication Date    57 non-null     object
#  2   CP                  57 non-null     object
#  3   label               0 non-null      object
# dtypes: object(4)
# memory usage: 2.2+ KB
# None
#


# invoke it a time while processing one patent
# return a list that is qualified for CP
def cleaner(raw: list, data_0: pandas.Series) -> list:
    data = data_0.tolist()
    res = []
    for i in raw:
        if i in data:
            res.append(i)
    res = list(set(res))
    return res


main()
