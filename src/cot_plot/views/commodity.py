from pyramid.view import view_config
import logging
import src.common.program as program
import src.common.settings as settings
from src.cot_plot.model import DBmodel
from src.ingester.web_scraper import Scraper
import src.yfinance as yf

log = logging.getLogger(__name__)

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
@view_config(route_name='home')
def home(request):
    return HTTPFound(location=request.route_url('comm_chart'))

def include_views(config):
    config.add_view('src.cot_plot.views.commodity.home',
                    route_name='home',
                    #attr='home',
                    renderer=program.get_template('commodity_chart.mako'),
                    request_method='GET')

    config.add_view('src.cot_plot.views.commodity.Commodity',
                    route_name='comm_chart',
                    attr='show_chart',
                    renderer=program.get_template('commodity_chart.mako'),
                    request_method='GET')


    config.add_view('src.cot_plot.views.commodity.Commodity',
                    route_name='comm_chart_data',
                    attr='get_chart_data',
                    renderer='json',
                    request_method='GET')

    config.add_view('src.cot_plot.views.commodity.Commodity',
                    route_name='comm_prices',
                    attr='get_price_data',
                    renderer='json',
                    request_method='GET')

class Commodity:
    def __init__(self, request):
        self.logger = logging.getLogger(__name__)
        self.request = request
        self.settings = settings.Settings()
        self.settings.load(program.get_base_dir('settings.json'))
        
    def show_chart(self):
        self.logger.info("show_chart called")
        
        commodities = self.settings.config['cot source']['commodities']['items']
        return {'commodities': commodities}

    def get_chart_data(self):
        com_code = self.request.matchdict['code']

        self.logger.info('Commodity Code: %s', com_code)
    
        model = DBmodel(self.settings.config['cot source']['commodities']['output file name'] + '.db')
        data = model.get_commodity_data(com_code)
        return data

    def get_price_data(self):

        commodities = self.settings.config['cot source']['commodities']['items']

        symbols = []
        indexes = ''
        for c in commodities:
            symbols.append(c['symbol'])
            indexes += c['symbol'] + '=F '

        prices = []
        try:
            t = yf.Tickers(indexes)
            for s in symbols:
                index = s + '=F'
                
                prices.append({
                    'symbol': s,
                    'price': t.tickers[index].info['regularMarketPrice'],
                    'change': round(t.tickers[index].info['regularMarketChange'],3),
                    'p change': round(t.tickers[index].info['regularMarketChangePercent'],3)
                })
        except Exception as e:
            self.logger.exception(e)

        return prices

