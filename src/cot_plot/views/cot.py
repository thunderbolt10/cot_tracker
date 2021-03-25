from pyramid.view import view_config
import logging
import src.common.program as program
import src.common.settings as settings
from src.cot_plot.model import DBmodel
from src.ingester.web_scraper import Scraper

log = logging.getLogger(__name__)

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
@view_config(route_name='home')
def home(request):
    return HTTPFound(location=request.route_url('cot_chart'))

def include_views(config):
    config.add_view('src.cot_plot.views.cot.home',
                    route_name='home',
                    #attr='home',
                    renderer=program.get_template('cot_chart.mako'),
                    request_method='GET')

    config.add_view('src.cot_plot.views.cot.Cot',
                    route_name='cot_chart',
                    attr='show_chart',
                    renderer=program.get_template('cot_chart.mako'),
                    request_method='GET')


    config.add_view('src.cot_plot.views.cot.Cot',
                    route_name='cot_chart_data',
                    attr='get_chart_data',
                    renderer='json',
                    request_method='GET')

    config.add_view('src.cot_plot.views.cot.Cot',
                    route_name='cot_prices',
                    attr='get_price_data',
                    renderer='json',
                    request_method='GET')

class Cot:
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

        url = self.settings.config['cot source']['commodities']['live price url']
        alt_url = self.settings.config['cot source']['commodities']['alt live price url']
        commodities = self.settings.config['cot source']['commodities']['items']

        symbols = []
        for c in commodities:
            symbols.append(c['symbol'])

        ws = Scraper()
        prices = ws.get_commodity_prices(url, alt_url, symbols)

        return prices
