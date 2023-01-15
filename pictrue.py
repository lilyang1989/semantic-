import matplotlib.pyplot as mpt
import numpy as np
import pandas as pd

import main

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

# years = raw.keys()
# data = []

# for year in years:
#     detail = raw.get(year)
#     months = detail.keys()
#     for month in months:
#         left = year
#         right = detail[month]
#         data.append((left, int(right)))
#
# dt = np.dtype([("year", np.int64), ("frequency", np.int64)])
# data = np.array(data, dtype=dt)
# data = np.sort(data, order="year")
# x = []
# y = []
# for i in data:
#     x.append(i[0])
#     y.append(i[1])
#
#
# mpt.title("Date Data")
# mpt.xlabel("x axis caption")
# mpt.ylabel("y axis caption")
# mpt.scatter(x, y)
# mpt.show()
