import win32com.client
import oracledb
import os
# instCpStockCode = win32com.client.Dispatch("CpUtil.CpStockCode")

# # Make stock table
# for i in range(100):
#     print(instCpStockCode.GetData(2, i))


instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
codeList = instCpCodeMgr.GetStockListByMarket(1)

stockList = []
for code in codeList:
    name = instCpCodeMgr.CodeToName(code)
    stockList.append((code, name, 'KOSPI'))

un = os.environ.get('PYTHON_USERNAME')
pw = os.environ.get('PYTHON_PASSWORD')
cs = os.environ.get('PYTHON_CONNECTSTRING')

with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
    with connection.cursor() as cursor:
        sql = ('INSERT INTO STOCK_INFO (STOCK_CODE, STOCK_NAME, MARKET_KIND) VALUES(:STOCK_CODE, :STOCK_NAME, :MARKET_KIND)')
        cursor.executemany(sql, stockList)
        connection.commit()