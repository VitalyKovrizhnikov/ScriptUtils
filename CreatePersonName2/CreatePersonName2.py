import os
import sys
import xlrd
import xlwt3 as xlwt
import pyodbc
import fnmatch

DATA_BOOK = 'TestData.xlsx'
SHEET_NAME = 'TestData'
RESULT_BOOK = 'RESULT_BOOK.xls' 

#Стили для наглядности результирующей таблицы
st_column = xlwt.easyxf("""
                        font: name Times New Roman, height 300, color-index black, bold on;
                        align: wrap on, horiz center
                        """)
st_ok = xlwt.easyxf("""
                    font: name Times New Roman, color-index white, bold on;
                    align: horiz center;
                    pattern: fore_color green, pattern solid
                    """)
st_not = xlwt.easyxf("""
                    font: name Times New Roman, color-index white, bold on;
                    align: horiz center;
                    pattern: fore_color red, pattern solid
                    """)
st_name = xlwt.easyxf('font: name Times New Roman, color-index black')

def newCoursor(server, db, login, password):
    cnxn = pyodbc.connect("""DRIVER={SQL Server};SERVER=%(server)s;DATABASE=%(db)s;UID=%(login)s;PWD=%(password)s"""
        %{'server': server, 'db': db, 'login': login, 'password': password})
    return cnxn.cursor()

def CreatePersonName(cursor, params):
    d_result = {} 
    cursor.execute("""set nocount on
                      declare @RetVal int

-- Очистка входящих таблиц
delete from pAPI_PmOrd_CrtPersonName where spid = @@spid

-- Очистка исходящих таблиц
delete from pAPI_PmOrd_LinkIDNTF     where spid = @@spid
delete from pAPI_PmOrd_PrsName       where spid = @@spid

-- Заполнение входящих таблиц
insert pAPI_PmOrd_CrtPersonName
       (
       spid                  ,
       BranchID              ,
       AccountID             ,
       DirectionFlag         ,
       PersonAddress         ,
       OperationNum          ,
       PersonFullName        ,
       PersonID              ,
       PersonINN             ,
       PersonBirthDay        ,
       PersonBirthPlace      ,
       BudgetDoc             ,
       Business              ,
       Amount                ,
       TransferFlag          ,
       PayeeAccountNumber    ,
       CrossBorderPaymentFlag
       )
select @@spid                , -- spid
       2000                  , -- BranchID
       0                     , -- AccountID
       0                     , -- DirectionFlag
       %(PersonAddress)s     , -- PersonAddress
       %(OperationNum)s      , -- OperationNum
       %(PersonFullName)s    , -- PersonFullName
       0                     , -- PersonID
       %(PersonINN)s         , -- PersonINN
       '19650114'            , -- PersonBirthDay
       ''                    , -- PersonBirthPlace
       %(BudgetDoc)s         , -- BudgetDoc
       ''                    , -- Business
       16000                 , -- Amount
       %(TransferFlag)s      , -- TransferFlag
       ''                    , -- PayeeAccountNumber
       %(CrossBorderPaymentFlag)s    -- CrossBorderPaymentFlag
       

       -- Вызов АПИ процедуры
exec @RetVal = API_PmOrd_CreatePersonName2

select @RetVal as RetVal
select * from tReturnCode where RetCode = @RetVal""" 
                        %{'BudgetDoc': params['BudgetDoc'],
                          'TransferFlag': params['TransferFlag'],
                          'CrossBorderPaymentFlag': params['CrossBorderPaymentFlag'], 
                          'PersonAddress': " '" + params['PersonAddress'] + "' ", 
                          'OperationNum': " '" + params['OperationNum'] + "' ", 
                          'PersonFullName': " '" + params['PersonFullName'] + "' ",
                          'PersonINN': " '" + params['PersonINN'] + "' "})

    rows = cursor.fetchone()
    print(rows)

    cursor.execute("""select p.*
                        from pAPI_PmOrd_LinkIDNTF p
                       where p.spid = @@spid""")
    row = cursor.fetchone()
    #print(row)
    if row:
        d_result['NTFMessage'] = row.NTFMessage
    cursor.execute("""select p.*
                        from pAPI_PmOrd_PrsName p
                       where p.spid = @@spid""")
    row = cursor.fetchone()
    #print(row)
    if row:
        d_result['PersonName'] = row.PersonName
        d_result['PersonINN'] = row.PersonINN
        d_result['PayerKPP'] = row.PayerKPP
    return d_result



if __name__ == "__main__":
    print(sys.argv[1])
    print(sys.argv[2])
    print(sys.argv[3])
    print(sys.argv[4])
    coursor = newCoursor(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

    f = xlrd.open_workbook(DATA_BOOK)
    d_result = {}
    sheet = f.sheet_by_name(SHEET_NAME)
    for rownum in range(sheet.nrows):
        d_result[rownum] = {}
        params_dict = {}
        row = sheet.row_values(rownum)
        #print(row)
        params_dict['PersonAddress'] = row[0]
        params_dict['OperationNum'] = str(int(row[1]))
        params_dict['PersonFullName'] = row[2]
        if row[3] == 0:
            params_dict['PersonINN'] = str(int(row[3]))
        else:
            params_dict['PersonINN'] = str(row[3])
        params_dict['BudgetDoc'] = int(row[4])
        params_dict['TransferFlag'] = int(row[5])
        params_dict['CrossBorderPaymentFlag'] = int(row[6])
        print(params_dict)
        d_result[rownum]['Input'] =params_dict
        d_result[rownum]['Result'] = CreatePersonName(coursor, params_dict)
        #print(d_result)

    #Записать результат в RESULT_BOOK
    result_book = xlwt.Workbook()
    rb_sheet = result_book.add_sheet('TestResults')
    rb_sheet.write(0, 0, 'PersonAddress', st_column)
    rb_sheet.write(0, 1, 'OperationNum', st_column)
    rb_sheet.write(0, 2, 'PersonFullName', st_column)
    rb_sheet.write(0, 3, 'PersonINN', st_column)
    rb_sheet.write(0, 4, 'BudgetDoc', st_column)
    rb_sheet.write(0, 5, 'TransferFlag', st_column)
    rb_sheet.write(0, 6, 'CrossBorderPaymentFlag', st_column)
    rb_sheet.write(0, 8, 'Наименование плательщика', st_column)
    rb_sheet.write(0, 9, 'ИНН плательщика', st_column)
    rb_sheet.write(0, 10, 'КПП плательщика', st_column)
    rb_sheet.write(0, 11, 'NTFMessage', st_column)
    row_count = 1
    for row in d_result:
        rb_sheet.write(row_count, 0, d_result[row]['Input']['PersonAddress'], st_name)
        rb_sheet.write(row_count, 1, d_result[row]['Input']['OperationNum'], st_name)
        rb_sheet.write(row_count, 2, d_result[row]['Input']['PersonFullName'], st_name)
        rb_sheet.write(row_count, 3, d_result[row]['Input']['PersonINN'], st_name)
        rb_sheet.write(row_count, 4, d_result[row]['Input']['BudgetDoc'], st_name)
        rb_sheet.write(row_count, 5, d_result[row]['Input']['TransferFlag'], st_name)
        rb_sheet.write(row_count, 6, d_result[row]['Input']['CrossBorderPaymentFlag'], st_name)
        if 'PersonName' in d_result[row]['Result']:
            rb_sheet.write(row_count, 8, d_result[row]['Result']['PersonName'], st_name)
        if 'PersonINN' in d_result[row]['Result']:
            rb_sheet.write(row_count, 9, d_result[row]['Result']['PersonINN'], st_name)
        if 'PayerKPP' in d_result[row]['Result']:
            rb_sheet.write(row_count, 10, d_result[row]['Result']['PayerKPP'], st_name)
        if 'NTFMessage' in d_result[row]['Result']:
            rb_sheet.write(row_count, 11, d_result[row]['Result']['NTFMessage'], st_name)
        row_count += 1

    result_book.save(RESULT_BOOK)
        

        
    







