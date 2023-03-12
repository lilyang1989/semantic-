import numpy as np
import pandas
import pandas as pd

""""
这个代码很💩山，别乱动哥们
"""


# CP columns means the patent is a citation of these patents
def main():
    data = pd.read_excel("data/data.xlsx")
    result = data[["Publication Number", "Publication Date"]]
    result = result.reindex(columns=result.columns.tolist() + ["CP", "label"])
    result[['CP', 'label']] = result[['CP', 'label']].astype('object')
    # use as a referring
    refer = result.copy()
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
    # drop the nan CP
    for i in range(len(CP_rows)):
        tmp = pd.isna(CP_rows[i])
        if type(tmp) == np.ndarray:
            if len(tmp) == 0:
                result.drop(i, axis=0, inplace=True)
        elif tmp:
            result.drop(i, axis=0, inplace=True)
    # reindex
    result.index = range(len(result))
    result = result_fix(result, refer)
    result.to_excel("result/mid_result.xlsx")
    return result


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


def result_fix(raw: pandas.DataFrame, refer: pandas.DataFrame) -> pandas.DataFrame:
    CP_list = raw["CP"]
    PN = raw["Publication Number"].tolist()
    origin_PN = refer["Publication Number"]
    for i in range(len(CP_list)):
        tmp_0 = CP_list[i]
        for j in range(len(tmp_0)):
            if tmp_0[j] in PN:
                continue
            else:
                if tmp_0[j] in origin_PN.tolist():
                    # prevent duplication
                    PN.append(tmp_0[j])
                    rows_index = refer.loc[refer['Publication Number'] == tmp_0[j]]
                    raw = raw.append(rows_index, ignore_index=True)
    raw.index = range(len(raw))
    PN = raw["Publication Number"]
    CP_list = raw["CP"]
    # remove self-citation
    for i in range(len(PN)):
        if type(CP_list[i]) == list and PN[i] in CP_list[i]:
            CP_list[i].remove(PN[i])
    raw.index = range(len(raw))
    return raw


main()
