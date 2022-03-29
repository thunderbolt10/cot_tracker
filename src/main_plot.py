# The following imports are required for pinstaller to detect required modules >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
import pyramid_mako
# end of required modules <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
import logging
import logging.config
import logging.handlers
import os
import sys
from socket import gethostname
#from wsgiref.simple_server import make_server
import cherrypy

from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

import src.common.program as program
import src.common.settings as settings
from src.cot_plot.security import groupfinder, forbidden, load_user_accounts
from src.updater import Updater

import src.cot_plot.views.commodity
import src.cot_plot.views.financial

def commodity_routes(config):
    config.add_route('comm_chart', '/chart')
    config.add_route('comm_chart_data', '/chart/{code}' )
    config.add_route('comm_prices', '/prices')

def financial_routes(config):
    config.add_route('fin_chart', '/chart')
    config.add_route('fin_chart_data', '/chart/{code}' )
    config.add_route('fin_prices', '/prices')


def include_routes(config):
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('forbidden', '/forbidden')

    config.add_route('home', 'cot/chart')
    
    config.include(commodity_routes, route_prefix='commodities')
    config.include(financial_routes, route_prefix='financials')



class Web_TimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, filename):
        logging.handlers.TimedRotatingFileHandler.__init__(self,
                                                           filename,
                                                           when='S', interval=86400, backupCount=20, encoding='utf8')

    def __del__(self):
        if hasattr(logging.handlers.TimedRotatingFileHandler, "__del__"):
            logging.handlers.TimedRotatingFileHandler.__del__(self)

LOG_CONF = {
    'version': 1,

    'formatters': {
        'void': {
            'format': ''
        },
        'standard': {
            'format': '%(asctime)s %(levelname)-5.5s [%(name)s:%(lineno)s][%(threadName)s] %(message)s [%(funcName)s()]',
            'datefmt': '%Y/%m/%d %H:%M:%S:',
            'filemode': 'a'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'src.main_plot.Web_TimedRotatingFileHandler',
            'filename': 'cot_plot.log',
        },

    },
    'loggers': {
        '': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG'
        },
        'root': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG'
        },
        'cherrypy': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': False
        },

    }
}


class WebServer(object):
    def __init__(self):
        self.server = None
        log_folder = program.get_base_dir('logs')

        if not os.path.exists(log_folder):
            os.mkdir(log_folder)

        log_file = os.path.join(log_folder, 'cot_plot.log')
        LOG_CONF['handlers']['logfile']['filename'] = log_file

        logging.config.dictConfig(LOG_CONF)
        self.logger = logging.getLogger(__name__)
        self.logger.debug("==============================================================")
        self.logger.debug("CoT Plot web werver started")

        self.pyramid_settings = {'reload_all': False,
                    'debug_all': True,
                    'pyramid.debug_all': True,
                    'pyramid.debug_routematch': True,
                    'pyramid.reload_all': False,
                    'cotplot.secret': '$nif2-EERG1$£03mf£AF$&^-'
                    }
        self.config = Configurator(settings=self.pyramid_settings,
                              root_factory='src.cot_plot.resources.Root')

        self.settings = settings.Settings()
        self.updater = Updater()

    def startup(self):
        status = False

        try:
            self.logger.info("initialise pyramid...")

            self.config.include('pyramid_mako')
            #config.include('pyramid_debugtoolbar')

            # Security policies
            authn_policy = AuthTktAuthenticationPolicy(
                self.pyramid_settings['cotplot.secret'],
                callback=groupfinder,
                cookie_name="cotplot-authtkt",
                secure=False,
                http_only=True,
                include_ip=True,
                path='cot_plot',
                hashalg='sha512')
            authz_policy = ACLAuthorizationPolicy()
            self.config.set_authentication_policy(authn_policy)
            self.config.set_authorization_policy(authz_policy)
            self.config.add_forbidden_view(forbidden)


            self.logger.info("load settings from file...")
            self.settings.load(program.get_base_dir('settings.json'))
            port = self.settings.get_web_port()

            static_path = program.get_bin_dir('cot_plot/static')

            self.logger.info("static path: %s", static_path)
            self.config.add_static_view(name='/cot_plot/static',
                                   path=static_path,
                                   cache_max_age=3600)

            template_path = program.get_bin_dir('cot_plot//templates')
            program.set_template_path(template_path)
            # The default home 
            self.config.add_route('home', '/')
            
            self.config.include(include_routes, route_prefix='/')

            # When this app is frozen config.scan() does not work, so we manually include the views here
            self.logger.info("include views...")
            #self.config.scan('web.views')
            src.cot_plot.views.commodity.include_views(self.config)
            src.cot_plot.views.financial.include_views(self.config)

            self.logger.info("setup wsgi...")
            app = self.config.make_wsgi_app()


            print("Web serving: http://localhost:%s/cot_plot" % port)
            self.logger.info("Web serving: http://localhost:%s/cot_plot", port)

            # Mount the application (or *app*)
            cherrypy.tree.graft(app, "/cot_plot")

            # Unsubscribe the default server
            cherrypy.server.unsubscribe()

            cherrypy.config.update({'environment': 'production',
                                    'log.error_file': 'cp_error.log',
                                    })

            # Instantiate a new server object
            self.server = cherrypy._cpserver.Server()

            # Configure the server object
            self.server.socket_host = "127.0.0.1"
            self.server.socket_port = int(port)
            self.server.thread_pool = 3
            #self.server.ssl_certificate = src.common.program.get_base_dir('cert.pem')
            #self.server.ssl_private_key = src.common.program.get_base_dir('key.pem')
            #self.server.ssl_module = 'builtin'

            # Subscribe this server
            self.server.subscribe()

            # Start the server engine (Option 1 *and* 2)
            cherrypy.engine.start()
            status = True
        except Exception as e:
            self.logger.error("Exception starting web service!")
            self.logger.exception(e)

        return status

    def run(self):
        self.logger.info('Start updater')
        self.updater.initialise()
        self.logger.info("Server Running")
        try:
            cherrypy.engine.block()
        except Exception as e:
            self.logger.exception(e)

        self.logger.info("Server exit")

    def shutdown(self):
        try:
            self.logger.info("Exit cherrypy engine")
            cherrypy.engine.exit()

            self.logger.info("Exit updater")
            self.updater.shutdown()
        
            self.logger.info("Shutdown complete")
        except Exception as e:
            self.logger.exception(e)


if __name__ == '__main__':
    svr = WebServer()
    svr.startup()
    svr.run()

