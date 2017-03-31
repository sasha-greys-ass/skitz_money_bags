import sqlite3
import BeautifulSoup as bs
import urllib as lib
import string


def get_sqlite_connection():
    con = sqlite3.connect('/Users/timeddon/wd/db/landing.db')
    return con


def get_element_list():
    alphabet_list = list(string.ascii_uppercase)
    element_list = []
    url = "http://www.asx.com.au/asx/research/listedCompanies.do?coName="
    for letter in alphabet_list:
        url_insert = url + letter
        html = lib.urlopen(url_insert)
        soup = bs.BeautifulSoup(html)
        data = [td.getText() for td in soup.findAll('td', limit = 0)]
        element_list.append(data)

    return element_list
        

def get_company_dict(data):
    data1 = []
    data2 = []
    data3 = []

    for data in element_list:
        for index, row in enumerate(data):
            if (index % 3 == 0):
                data1.append(row.replace("'","''"))
            if (index % 3 == 1):
                data2.append(row.replace("'","''"))
            if (index % 3 == 2):
                data3.append(row.replace("'","''"))

    company_dictionary = dict()

    for row1,row2,row3 in zip(data1,data2,data3):
        if("'" + str(row2) + "'" not in company_dictionary):
            company_dictionary["'" + str(row2) + "'"] = [row2,row1,row3]

    return company_dictionary

def company_insert(company_dictionary, sqlite):
    for key in company_dictionary:
        try:
            sqlite.execute("INSERT INTO LND_COMPANY VALUES ('" + "','".join(company_dictionary[key]) + "')")
        except:
            print("INSERT INTO LND_COMPANY VALUES ('" + "','".join(company_dictionary[key]) + "')")


sqlite_connection = get_sqlite_connection()
sqlite = sqlite_connection.cursor()

element_list = get_element_list()
company_dict = get_company_dict(element_list)
company_insert(company_dict, sqlite)

sqlite.close()
sqlite_connection.commit()
sqlite_connection.close()


    
    

