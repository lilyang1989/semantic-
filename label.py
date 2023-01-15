import time

import pandas as pd


def label():
    data = pd.read_excel("./mid_result.xlsx")
    time_columns = data["Publication Date"]
    border = time.strptime("2019-01-01", "%Y-%m-%d")
    # drop the former index from last processing
    data.drop(["Unnamed: 0"], axis=1, inplace=True)
    for i in range(len(time_columns)):
        _time = time.strptime(str(time_columns[i]), "%Y-%m-%d")
        if _time > border:
            data.loc[i, "label"] = "2"
        else:
            data.loc[i, "label"] = "1"
    data.drop("Publication Date", axis=1, inplace=True)
    data.to_excel("./final_result.xlsx")
    return data


label()
