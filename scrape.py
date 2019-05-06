import requests
from bs4 import BeautifulSoup
import csv
import time

url="http://www.elections.ny.gov:8080/plsql_browser/registrantsbycounty_new"
counties={"01":"Albany County", "02":"Allegany County", "03":"Bronx County", "04":"Broome County", "05":"Cattaraugus County", "06":"Cayuga County", "07":"Chautauqua County", "08":"Chemung County", "09":"Chenango County", "10":"Clinton County", "11":"Columbia County", "12":"Cortland County", "13":"Delaware County", "14":"Dutchess County", "15":"Erie County", "16":"Essex County", "17":"Franklin County", "18":"Fulton County", "19":"Genesee County", "20":"Greene County", "21":"Hamilton County", "22":"Herkimer County", "23":"Jefferson County", "24":"Kings County (Brooklyn)", "25":"Lewis County", "26":"Livingston County", "27":"Madison County", "28":"Monroe County", "29":"Montgomery County", "30":"Nassau County", "31":"New York County (Manhattan)", "32":"Niagara County", "33":"Oneida County", "34":"Onondaga County", "35":"Ontario County", "36":"Orange County", "37":"Orleans County", "38":"Oswego County", "39":"Otsego County", "40":"Putnam County", "41":"Queens County", "42":"Rensselaer County", "43":"Richmond County (Staten Island)", "44":"Rockland County", "50":"Saint Lawrence County", "45":"Saratoga County", "46":"Schenectady County", "47":"Schoharie County", "48":"Schuyler County", "49":"Seneca County", "51":"Steuben County", "52":"Suffolk County", "53":"Sullivan County", "54":"Tioga County", "55":"Tompkins County", "56":"Ulster County", "57":"Warren County", "58":"Washington County", "59":"Wayne County", "60":"Westchester County", "61":"Wyoming County", "62":"Yates County"}


payload={"OFFICE_IN":"ALL","DISTRICT_IN":"","county_IN":"","municipality_in":""}


def scrape(county_id):
    payload["county_IN"]=county_id
    while True:
        try:
            r=requests.post(url,data=payload,timeout=20000)
            break
        except:
            print("Connection error - trying again")
            pass
    #print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    tables=soup.find_all("table")
    #print(len(tables))
    ret=[]
    if len(tables)==1:
        table=tables[0]
        for row in table.find_all("tr"):
            cells=row.find_all("td")
            if len(cells)==0:
                continue #header
            elif len(cells)==6:
                dat=[c.text for c in cells[:-1]]
                #print(cells[-1])
                dat=[cells[-1].find("input")["value"]]+dat
                ret+=[dat]
                #print(dat)
            else:
                raise Exception("Unexpected row length: %d"%len(cells))
                #print(len(cells))
    return ret

with open("candidates_counties.csv","w") as csvfile:    
    writer = csv.writer(csvfile)
    writer.writerow(["Filer ID","Name","Office","Subdivision","Municipality","District","County"])
    for c_id in counties:
        print(counties[c_id])
        rows=[r+[counties[c_id]] for r in scrape(c_id)]
        writer.writerows(rows)
        time.sleep(5)



