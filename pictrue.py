import matplotlib.pyplot as mpt
import numpy as np
import pandas as pd

import main


def depict():
    raw = main.readFile()
    data = pd.DataFrame.from_dict(raw)
    # get the 2021 and 2022 data
    data = data.sort_index(axis=1)
    data_2021 = data['2021'].values.tolist()
    data_2022 = data['2022'].values.tolist()
    all = data_2021 + data_2022
    # convert series to numpy array
    # x ranges are from 1 to 24
    x = np.array(range(1, 25))
    y = np.array(all)
    mpt.scatter(x, y)
    mpt.xlabel("months(2021-2022)")
    mpt.ylabel("quantity")
    # define the precision of this function
    precision = 5
    para = np.polyfit(x, y, precision)
    y2 = 0
    # show the formulation of this function
    formulation = ""
    for i in range(precision + 1):
        y2 = y2 + para[i] * x ** (precision - i)
        formulation = formulation + str(para[i]) + "*x^" + str(precision - i)
        if i != precision:
            formulation = formulation + " + "
    print(formulation)
    # picture the image
    mpt.plot(x, y2, "r")
    mpt.xticks(x, rotation=45)
    mpt.savefig("images/quantity.png")
    mpt.show()


def depict2():
    raw = main.readFile()
    data = pd.DataFrame.from_dict(raw)
    # get the sum of everyyear
    data = data.sort_index(axis=1)
    data.loc['sum'] = data.sum(axis=0)
    years = data.loc['sum']
    # drop useless values
    years = years.drop("2023")
    years = years.drop(years.index[0:4])
    print(years)
    # convert series to numpy array
    x = np.array(years.index, dtype="int64")
    y = np.array(years.values)
    mpt.scatter(x, y)
    mpt.xlabel("years")
    mpt.ylabel("quantity")
    # define the precision of this function
    precision = 5
    para = np.polyfit(x, y, precision)
    y2 = 0
    formulation = ""
    for i in range(precision + 1):
        y2 = y2 + para[i] * x ** (precision - i)
        formulation = formulation + str(para[i]) + "*x^" + str(precision - i)
        if i != precision:
            formulation = formulation + " + "
    print(formulation)
    # picture the image
    mpt.plot(x, y2, "r")
    mpt.xticks(x, rotation=45)
    mpt.show()
    mpt.savefig('result_path.png')


depict2()
