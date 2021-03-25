from bs4 import BeautifulSoup
import urllib.request
import re
import logging



class Scraper():
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def find_td_value(self, row, class_name):
        r = row.find("td", class_=re.compile(class_name))
        if r:
            return r.string

        return ''

    def find_symbol_data(self, soup, symbol):
        item = {
            'symbol': symbol,
            'price': 0.0,
            'time': '',
            'change': 0.0,
            '% change': 0.0
        }

        try:

            class_name = 'row%s=F' % symbol
            r = soup.find_all("tr", class_=re.compile(class_name))

            if r and len(r):
                row = r[0]
                if row:
                    item['price'] = round(float(self.find_td_value(row, 'data-col2').replace(',','')), 2)
                    item['time'] = self.find_td_value(row, 'data-col3' )
                    item['change'] = round(float(self.find_td_value(row, 'data-col4' ).replace(',','')), 2)
                    item['% change'] = round(float(self.find_td_value(row, 'data-col5' ).replace(',','')[:-1]), 2)
        except Exception as e:
            self.log.exception(e)

        return item

    def find_direct_commodity_price(self, symbol, url_prefix):
        url = url_prefix + symbol + '=F/'

        item = {
                    'symbol': symbol,
                    'price': 0.0,
                    'time': '',
                    'change': 0.0,
                    '% change': 0.0
                }

        try:
            with urllib.request.urlopen(url) as response:
                soup = BeautifulSoup(response, 'html.parser')
                item['price'] = float(soup.find('td', attrs={'data-test': 'ASK-value'}).string.replace(',',''))
                open_price = float(soup.find('td', attrs={'data-test': 'OPEN-value'}).string.replace(',',''))
                item['change'] = round(item['price'] - open_price, 2)
                item['% change'] = round(((item['change'] * 100.0 ) / open_price), 2)
                item['price'] = round(item['price'], 2)
                 
        except Exception as e:
            self.log.exception(e)

        return item
    def get_commodity_prices(self, url, alt_url, symbols):
        try:
            with urllib.request.urlopen(url) as response:
                soup = BeautifulSoup(response, 'html.parser')

                data = []
                for s in symbols:
                    item = self.find_symbol_data(soup, s)

                    if item['price'] != 0.0:
                        data.append(item)
                    else:
                        item = self.find_direct_commodity_price(s, alt_url)
                        data.append(item)
        except Exception as e:
            self.log.exception(e)

        return data
