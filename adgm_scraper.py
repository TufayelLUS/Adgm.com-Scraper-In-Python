import requests
from bs4 import BeautifulSoup as bs
import csv
import os


def saveData(dataset):
    with open('data.csv', mode='a+', encoding='utf-8-sig', newline='') as csvFile:
        fieldnames = [
            "Company", "Financial Services Permission Number", "Company Status", "Address", "Link"]
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames,
                                delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if os.stat('data.csv').st_size == 0:
            writer.writeheader()
        writer.writerow({
            "Company": dataset[0],
            "Financial Services Permission Number": dataset[1],
            "Company Status": dataset[2],
            "Address": dataset[3],
            "Link": dataset[4]
        })


def scrapeResults():
    link = "https://www.adgm.com/api/fsf/GetFirms"
    page_no = 1
    while True:
        print("Page: {}".format(page_no))
        params = {
            'sc_itemid': 'fcea6284-884f-40f5-a6ba-f2179587e043',
            'sc_mode': 'normal',
            'pageNumber': str(page_no),
            'pageSize': '100',
            'companyStatus': '',
            'regulatedActivity': '',
            'query': '',
            'orderByField': 'name_srt',
            'orderDesc': 'false',
        }
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
            'cache-control': 'max-age=0',
            'dnt': '1',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }
        try:
            resp = requests.get(link, headers=headers, params=params).json()
        except:
            print("Failed to open {}".format(link))
            return
        html_data = resp.get('tableResult')
        soup = bs(html_data, 'html.parser')
        records = soup.find_all('div', {'class': 'opn-accord'})
        if len(records) == 0:
            break
        for record in records:
            try:
                parent = record.parent
                hyperlink = "https://www.adgm.com" + parent.find('div', {'class': 'click'}).a.get('href')
            except:
                hyperlink = ""
            data = record.find_all('div')
            data = [x.text.strip() for x in data]
            data.append(hyperlink)
            print("Company: {}".format(data[0]))
            saveData(data)
        page_no += 1


if __name__ == "__main__":
    scrapeResults()
