import sqlite3
import BeautifulSoup as bs
import urllib as lib
import string


def get_sqlite_connection():
    con = sqlite3.connect('/Users/timeddon/wd/db/landing.db')
    return con

def get_company_key_url_list(sqlite):
    company_key_list = []
    url_list = []
    sqlite.execute("SELECT DISTINCT COMPANY_KEY FROM LND_COMPANY")
    company_keys = sqlite.fetchall()
    for row in company_keys:
        company_key_list.append(row[0])

    for company_key in company_key_list:
        url = "http://www.asx.com.au/asx/share-price-research/company/" + company_key + "/statistics/shares"
        url_list.append(url)

    return url_list


sqlite_con = get_sqlite_connection()
sqlite = sqlite_con.cursor()

url_list = get_company_key_url_list(sqlite)

url = "http://www.asx.com.au/asx/markets/equityPrices.do?by=asxCodes&asxCodes=AMC"
html = lib.urlopen(url)
soup = bs.BeautifulSoup(html)
print(soup)
data = [td.getText() for td in soup.findAll('script', limit = 0)]


        



    
    


