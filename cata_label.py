import pandas as pd

NAME = "VR"


def label():
    data = pd.read_excel(f"result/metaverse/{NAME}_mid_result.xlsx")
    # drop the former index from last processing
    data.drop(["Unnamed: 0", 'label'], axis=1, inplace=True)
    data['label'] = NAME
    data.drop("Publication Date", axis=1, inplace=True)
    data.to_excel(f"label_result/{NAME}.xlsx")


print(label())
