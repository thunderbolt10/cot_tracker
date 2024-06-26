import logging
import sqlite3
import os
import pathlib
import datetime
import itertools

class Importer():
    def __init__(self, db_folder, source):
        self.log = logging.getLogger()
        self.db_folder = db_folder
        self.config = source
        db_filename = source['output file name'] + '.db'
        self.db_filepath = os.path.join(self.db_folder, db_filename)

    def create_db(self, db_filepath):
        try:
            con = sqlite3.connect(db_filepath, detect_types=sqlite3.PARSE_DECLTYPES |
                                                        sqlite3.PARSE_COLNAMES)
            cur = con.cursor()
            if self.config['data type'] == 'commodity':
                self.log.info('Create db %s with format: %s', db_filepath, self.config['data type'])

                tables = []
                cur.execute('''SELECT * FROM sqlite_master where type='table' ''')
                res = cur.fetchall()
                for r in res:
                    tables.append(r[2])

                if 'market_names' not in tables:
                    cur.execute('''CREATE TABLE market_names 
                        (
                            id_name INTEGER NOT NULL PRIMARY KEY, 
                            display_name TEXT,
                            filter_name TEXT NOT NULL UNIQUE,
                            symbol TEXT NOT NULL UNIQUE
                        );''')

                if 'futures' not in tables:
                    cur.execute('''CREATE TABLE futures 
                        (
                            id_future INTEGER NOT NULL PRIMARY KEY,
                            id_name INTEGER NOT NULL,
                            report_date DATE NOT NULL,
                            cftc_code INTEGER,
                            open_interest INTEGER,
                            pm_long INTEGER,
                            pm_short INTEGER,
                            mm_long INTEGER,
                            mm_short INTEGER,
                            swap_long INTEGER,
                            swap_short INTEGER,
                            other_long INTEGER,
                            other_short INTEGER,
                            FOREIGN KEY (id_name) REFERENCES market_name (id_name) 
                                ON DELETE CASCADE ON UPDATE NO ACTION,
                            UNIQUE(id_name, report_date)
                        );''')

                    cur.execute('''CREATE VIEW future_calc AS
                        SELECT t2.*, 
                            100.0 * (t2.pm_net_as_percent_oi - t2.pm_5_yr_min )/ NULLIF(t2.pm_5_yr_max - t2.pm_5_yr_min, 0) as dealer_net_5_yr,
                            100.0 * (t2.mm_net_as_percent_oi - t2.mm_5_yr_min )/ nullif(t2.mm_5_yr_max - t2.mm_5_yr_min, 0) as spec_net_5_yr
                        FROM (
                            SELECT t1.*,                        
                                MIN(t1.pm_net_as_percent_oi) OVER (PARTITION BY id_name ORDER BY julianday(report_date) ASC RANGE BETWEEN 1826 PRECEDING AND CURRENT ROW) as pm_5_yr_min,
                                MAX(t1.pm_net_as_percent_oi) OVER (PARTITION BY id_name ORDER BY julianday(report_date) ASC RANGE BETWEEN 1826 PRECEDING AND CURRENT ROW) as pm_5_yr_max,
                                MIN(t1.mm_net_as_percent_oi) OVER (PARTITION BY id_name ORDER BY julianday(report_date) ASC RANGE BETWEEN 1826 PRECEDING AND CURRENT ROW) as mm_5_yr_min,
                                MAX(t1.mm_net_as_percent_oi) OVER (PARTITION BY id_name ORDER BY julianday(report_date) ASC RANGE BETWEEN 1826 PRECEDING AND CURRENT ROW) as mm_5_yr_max
                            FROM (
                                SELECT market_names.display_name, market_names.filter_name, 
                                    futures.*, 
                                    (futures.pm_long-futures.pm_short) as pm_net,
                                    100.0 * CAST ((futures.pm_long + futures.swap_long)-(futures.pm_short+futures.swap_short) as FLOAT)/futures.open_interest as pm_net_as_percent_oi,
                                    
                                    (futures.mm_long-futures.mm_short) as mm_net,
                                    100.0 * CAST ((futures.mm_long+futures.other_long)-(futures.mm_short+futures.other_short) as FLOAT)/futures.open_interest as mm_net_as_percent_oi

                                FROM futures
                                JOIN market_names on futures.id_name = market_names.id_name
                                ORDER BY futures.id_name, report_date 
                            ) as t1
                        ) as t2;''')

                if 'future_prices' not in tables:
                    cur.execute('''CREATE TABLE future_prices 
                        (
                            id_price INTEGER NOT NULL PRIMARY KEY,
                            id_name INTEGER NOT NULL,
                            report_date DATE NOT NULL,
                            close REAL,
                            volume INTEGER,
                            FOREIGN KEY (id_name) REFERENCES market_name (id_name) 
                                ON DELETE CASCADE ON UPDATE NO ACTION,
                            UNIQUE(id_name, report_date)
                        );''')

            elif self.config['data type'] == 'financial':
                self.log.info('Create db %s with Financial format', db_filepath)

                tables = []
                cur.execute('''SELECT * FROM sqlite_master where type='table' ''')
                res = cur.fetchall()
                for r in res:
                    tables.append(r[2])

                if 'market_names' not in tables:
                    cur.execute('''CREATE TABLE market_names 
                        (
                            id_name INTEGER NOT NULL PRIMARY KEY, 
                            display_name TEXT,
                            filter_name TEXT NOT NULL UNIQUE,
                            symbol TEXT NOT NULL UNIQUE
                        );''')

                if 'futures' not in tables:
                    cur.execute('''CREATE TABLE futures 
                        (
                            id_future INTEGER NOT NULL PRIMARY KEY,
                            id_name INTEGER NOT NULL,
                            report_date DATE NOT NULL,
                            cftc_code INTEGER,
                            open_interest INTEGER,
                            dp_long INTEGER,
                            dp_short INTEGER,
                            am_long INTEGER,
                            am_short INTEGER,
                            lm_long INTEGER,
                            lm_short INTEGER,
                            or_long INTEGER,
                            or_short INTEGER,
                            FOREIGN KEY (id_name) REFERENCES market_name (id_name) 
                                ON DELETE CASCADE ON UPDATE NO ACTION,
                            UNIQUE(id_name, report_date)
                        );''')

                    cur.execute('''CREATE VIEW future_calc AS
                        SELECT t2.*, 
                            100.0 * (t2.dealer_net_as_percent_oi - t2.dealer_5_yr_min )/ NULLIF(t2.dealer_5_yr_max - t2.dealer_5_yr_min, 0) as dealer_net_5_yr,
                            100.0 * (t2.spec_net_as_percent_oi - t2.spec_5_yr_min )/ nullif(t2.spec_5_yr_max - t2.spec_5_yr_min, 0) as spec_net_5_yr
                        FROM (
                            SELECT t1.*,                        
                                MIN(t1.dealer_net_as_percent_oi) OVER (PARTITION BY id_name ORDER BY julianday(report_date) ASC RANGE BETWEEN 1826 PRECEDING AND CURRENT ROW) as dealer_5_yr_min,
                                MAX(t1.dealer_net_as_percent_oi) OVER (PARTITION BY id_name ORDER BY julianday(report_date) ASC RANGE BETWEEN 1826 PRECEDING AND CURRENT ROW) as dealer_5_yr_max,
                                MIN(t1.spec_net_as_percent_oi) OVER (PARTITION BY id_name ORDER BY julianday(report_date) ASC RANGE BETWEEN 1826 PRECEDING AND CURRENT ROW) as spec_5_yr_min,
                                MAX(t1.spec_net_as_percent_oi) OVER (PARTITION BY id_name ORDER BY julianday(report_date) ASC RANGE BETWEEN 1826 PRECEDING AND CURRENT ROW) as spec_5_yr_max
                            FROM (
                                SELECT market_names.display_name, market_names.filter_name, 
                                    futures.*, 
                                    (futures.dp_long-futures.dp_short) as dealer_net,
                                    100.0 * CAST ((futures.dp_long-futures.dp_short) as FLOAT) / futures.open_interest as dealer_net_as_percent_oi,
                                    ((futures.am_long + futures.lm_long + futures.or_long)-(futures.am_short + futures.lm_short + futures.or_short)) as spec_net,
                                    100.0 * CAST ((futures.am_long + futures.lm_long + futures.or_long)-(futures.am_short + futures.lm_short + futures.or_short) as FLOAT)/futures.open_interest as spec_net_as_percent_oi
                                FROM futures
                                JOIN market_names on futures.id_name = market_names.id_name
                                ORDER BY futures.id_name, report_date 
                            ) as t1
                        ) as t2;''')

                if 'future_prices' not in tables:
                    cur.execute('''CREATE TABLE future_prices 
                        (
                            id_price INTEGER NOT NULL PRIMARY KEY,
                            id_name INTEGER NOT NULL,
                            report_date DATE NOT NULL,
                            close REAL,
                            volume INTEGER,
                            FOREIGN KEY (id_name) REFERENCES market_name (id_name) 
                                ON DELETE CASCADE ON UPDATE NO ACTION,
                            UNIQUE(id_name, report_date)
                        );''')


            con.commit()
        except Exception as e:
            con.rollback()
            self.log.exception(e)  
        finally:
            con.close()      


    def import_cot_data(self, data):
        fpath = pathlib.Path(self.db_filepath)

        #if not fpath.exists():
        self.create_db(self.db_filepath)


        try:
            fdata = self.filter_names(data)
            con = sqlite3.connect(self.db_filepath, detect_types=sqlite3.PARSE_DECLTYPES |
                                                        sqlite3.PARSE_COLNAMES)
            cur = con.cursor()

            if self.config['data type'] == 'commodity':
                cur.executemany('''INSERT OR IGNORE INTO futures 
                    (id_name, report_date, cftc_code, open_interest,
                    pm_long, pm_short, mm_long, mm_short,
                    swap_long, swap_short, other_long, other_short)
                    VALUES (:market_id, :report_date, :CFTC_Contract_Market_Code, 
                        :Open_Interest_All, 
                        :Prod_Merc_Positions_Long_All, :Prod_Merc_Positions_Short_All,
                        :M_Money_Positions_Long_All, :M_Money_Positions_Short_All,
                        :Swap_Positions_Long_All, :Swap__Positions_Short_All,
                        :Other_Rept_Positions_Long_All, :Other_Rept_Positions_Short_All
                        );''', fdata)
            elif self.config['data type'] == 'financial':
                cur.executemany('''INSERT OR IGNORE INTO futures 
                    (id_name, report_date, cftc_code, open_interest,
                    dp_long, dp_short, am_long, am_short,
                    lm_long, lm_short, or_long, or_short)
                    VALUES (:market_id, :report_date, :CFTC_Contract_Market_Code, 
                        :Open_Interest_All, 
                        :Dealer_Positions_Long_All, :Dealer_Positions_Short_All,
                        :Asset_Mgr_Positions_Long_All, :Asset_Mgr_Positions_Short_All,
                        :Lev_Money_Positions_Long_All, :Lev_Money_Positions_Short_All,
                        :Other_Rept_Positions_Long_All, :Other_Rept_Positions_Short_All
                        );''', fdata)

            con.commit()
        
        except Exception as e:
            con.rollback()
            self.log.exception(e)
        finally:
            con.close()

    

    def intialise_filters(self, fmap):
        try:
            market_names = []

            symbols = []

            for filter in fmap:
                if fmap[filter]['symbol'] not in symbols:
                    market_names.append({'display': None, 'filter': filter, 'symbol': fmap[filter]['symbol']})
                    symbols.append(fmap[filter]['symbol'])

            con = sqlite3.connect(self.db_filepath, detect_types=sqlite3.PARSE_DECLTYPES |
                                                        sqlite3.PARSE_COLNAMES)
            cur = con.cursor()

            # Add any new market names
            cur.executemany('''INSERT OR IGNORE INTO market_names (display_name, filter_name, symbol) 
                            VALUES (:display, :filter, :symbol);''', market_names)

            cur.execute('''SELECT * FROM market_names''')

            result = cur.fetchall()        

            if result:
                for row in result:
                    for filter in fmap:
                        if row[3] == fmap[filter]['symbol']:
                            fmap[filter]['id'] = row[0]
                            fmap[row[2]]['display_name'] = row[1]
                            
            con.commit()
        except Exception as e:
            con.rollback()
            self.log.exception(e)
        finally:
            con.close()

    def update_market_names(self, fmap):
        try:
            market_names = []
            for filter in fmap:
                market_names.append({'display': fmap[filter]['display_name'], 'id': fmap[filter]['id']})

            con = sqlite3.connect(self.db_filepath, detect_types=sqlite3.PARSE_DECLTYPES |
                                                        sqlite3.PARSE_COLNAMES)
            cur = con.cursor()

            # update the display name of existing market names to the latest representation
            cur.executemany('''UPDATE market_names SET display_name = :display
                            WHERE id_name = :id''', market_names)

            con.commit()
        except Exception as e:
            con.rollback()
            self.log.exception(e)
        finally:
            con.close()

    def generate_filter_names(self):
        names = {}

        for item in self.config['items']:
            for filter in item['filters']:
                names[filter] = item


        return names

    def filter_names(self, data):
        fdata = [] # filtered data to the commodities we are interested in
        fmap = {}

        filter_names = self.generate_filter_names()

        for filter in filter_names:
            fmap[filter.upper()] = {'id': None, 'display_name': None, 'symbol': filter_names[filter]['symbol']}

        self.intialise_filters(fmap)

        try:
            last_filter = None
            last_row = None

            for row in data:
                if 'Report_Date_as_YYYY-MM-DD' in row:
                    row['report_date'] = datetime.datetime.strptime(row['Report_Date_as_YYYY-MM-DD'], '%Y-%m-%d').date()
                elif 'Report_Date_as_MM_DD_YYYY' in row:
                    row['report_date'] = datetime.datetime.strptime(row['Report_Date_as_MM_DD_YYYY'], '%Y-%m-%d').date()
                else:
                    self.log.warning('Row missing a field for Report Date: %s', row)
                    continue
                    
                # Optimisation - check if last filter used matches
                if last_row == row['Market_and_Exchange_Names'] \
                    and last_filter \
                        and last_filter in row['Market_and_Exchange_Names'].upper():
                    row['market_id'] = fmap[last_filter]['id']
                    fdata.append(row)
                else:
                    # must be a new filter so scan list of filters
                    for filter in fmap:
                        if filter in row['Market_and_Exchange_Names'].upper():
                            row['market_id'] = fmap[filter]['id']
                            fdata.append(row)
                            last_filter = filter
                            last_row = row['Market_and_Exchange_Names']

                            if not fmap[filter]['display_name']:
                                fmap[filter]['display_name'] = row['Market_and_Exchange_Names'].upper()

                            print("%s:  '%s' matched to filter: '%s' " % ( fmap[filter]['symbol'], row['Market_and_Exchange_Names'].upper(), filter))
                            break

            self.update_market_names(fmap)
            
        except Exception as e:
            self.log.exception(e)

        return fdata

    def import_commodity_price(self, item, data):
        self.log.info('Import price for: %s', item)

        try:
            con = sqlite3.connect(self.db_filepath, detect_types=sqlite3.PARSE_DECLTYPES |
                                                        sqlite3.PARSE_COLNAMES)
            cur = con.cursor()

            cur.execute('''SELECT id_name FROM market_names 
                            WHERE symbol=:symbol''', item)

            r = cur.fetchone()
            if r is None:
                raise Exception('null id_name for %s' % item['symbol'])
                
            id_name = r[0]

            for row in data:
                row['market_id'] = id_name

            # Remove null entries from import list
            fdata = []
            fdata[:] = itertools.filterfalse(lambda row: row['Close'] == 'null', data)
                
            cur.executemany('''INSERT OR IGNORE INTO future_prices 
            (id_name, report_date, close, volume)
            VALUES (:market_id, :Date, :Close, :Volume);''', fdata)

            con.commit()
        
        except Exception as e:
            con.rollback()
            self.log.exception(e)
        finally:
            con.close()

    def get_year_of_last_price(self, item):
        year = None
        self.log.info('get_year_of_last_price for: %s', item)

        try:
            con = sqlite3.connect(self.db_filepath, detect_types=sqlite3.PARSE_DECLTYPES |
                                                        sqlite3.PARSE_COLNAMES)
            cur = con.cursor()

            cur.execute('''SELECT id_name FROM market_names 
                            WHERE symbol=:symbol''', item)

            r = cur.fetchone()
            if r is None:
                raise Exception('null id_name for %s' % item['symbol'])
                
            param = {'id_name': r[0]}
            
            
            cur.execute('''SELECT report_date FROM future_prices 
                WHERE id_name=:id_name
                ORDER BY report_date DESC
                LIMIT 1;''', param)

            last_report = cur.fetchone()
            if last_report:
                year = last_report[0].year
                
        except Exception as e:
            con.rollback()
            self.log.exception(e)
        finally:
            con.close()

        return year