import xlrd
import xlwt
from tqdm import trange

time = []


def readFile():
    xls_Data = xlrd.open_workbook('./data2.xlsx')
    table = xls_Data.sheets()[0]  # we set the first sheet as a default sheet
    index = table.row_values(0, start_colx=0, end_colx=None)
    date_index = 0  # find out the index of url
    for i in index:
        if "Publication Date" == i:
            break
        date_index = date_index + 1
    date_data = table.col_values(date_index, start_rowx=1, end_rowx=None)
    date = []
    length = len(date_data)
    for m in trange(length):
        i = str(date_data[m]).strip()
        res = [i[0:4], i[5:7], i[8:10]]
        date.append(res)
    resp = process(date)
    return resp


# def eSpace(url: str) -> str:
#     req = "&date=(\d*)"
#     try:
#         time1 = re.findall(req, url)[0]
#         res = [time1[0:4], time1[4:6], time1[6:8]]
#         return res
#
#     except Exception as e:
#         print(e)
#         return "Not Found"


# def apx(url0: str) -> list:
#     req = "=DN/(\d*)"
#     try:
#         num = re.findall(req, url0)[0]
#     except Exception as e:
#         print(e)
#         print(url0)
#     url = "https://ppubs.uspto.gov/dirsearch-public/searches/generic"
#
#     payload = json.dumps({
#         "cursorMarker": "*",
#         "databaseFilters": [
#             {
#                 "databaseName": "*"
#             }
#         ],
#         "fields": [
#             "datePublished"
#         ],
#         "q": "(" + str(num) + ").pn.",
#         "sort": "date_publ desc"
#     })
#     headers = {
#         'authority': 'ppubs.uspto.gov',
#         'accept': 'application/json',
#         'content-type': 'application/json',
#         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
#                       'Chrome/108.0.0.0 Safari/537.36 '
#     }
#
#     response = requests.request("POST", url, headers=headers, data=payload)
#     text = response.text
#     op = json.loads(text)
#     time00 = str(op["docs"][0]["datePublished"])
#     return time00.split("-")


def process(raw: list) -> dict:
    data = {}
    for i in raw:
        keys = data.keys()
        if i[0] in keys:
            count = data[i[0]][i[1]] + 1
            data[i[0]][i[1]] = count
        else:
            data[i[0]] = {"01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0,
                          "11": 0, "12": 0}
            count = data[i[0]][i[1]] + 1
            data[i[0]][i[1]] = count
    return data


def write(data: dict):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet("result")
    for i in range(1, 13):
        worksheet.write(0, i, str(i) + "月")
    keys = data.keys()
    count_years = 1
    for year in keys:
        worksheet.write(count_years, 0, str(year))
        for i in range(1, 13):
            month = ""
            if i < 10:
                month = "0" + str(i)
            else:
                month = str(i)
            worksheet.write(count_years, i, str(data[str(year)][month]))
        count_years = count_years + 1
    workbook.save("./result.xls")


readFile()
