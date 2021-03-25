import logging
import sqlite3
import os
import pathlib
import datetime

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
            if self.config['data type'] == 'DFaO':
                self.log.info('Create db %s with DFaO format', db_filepath)
                cur.execute('''CREATE TABLE market_names 
                    (
                        id_name INTEGER NOT NULL PRIMARY KEY, 
                        display_name TEXT,
                        filter_name TEXT NOT NULL UNIQUE,
                        symbol TEXT NOT NULL UNIQUE
                    );''')

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
                        FOREIGN KEY (id_name) REFERENCES market_name (id_name) 
                            ON DELETE CASCADE ON UPDATE NO ACTION,
                        UNIQUE(id_name, report_date)
                    );''')

                cur.execute('''CREATE VIEW future_calc AS
                    SELECT t2.*, 
                        100.0 * (t2.pm_net_as_percent_oi - t2.pm_5_yr_min )/ NULLIF(t2.pm_5_yr_max - t2.pm_5_yr_min, 0) as pm_net_5_yr,
                        100.0 * (t2.mm_net_as_percent_oi - t2.mm_5_yr_min )/ nullif(t2.mm_5_yr_max - t2.mm_5_yr_min, 0) as mm_net_5_yr
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
                                100.0 * CAST (futures.pm_long-futures.pm_short as FLOAT)/futures.open_interest as pm_net_as_percent_oi,
                                (futures.mm_long-futures.mm_short) as mm_net,
                                100.0 * CAST (futures.mm_long-futures.mm_short as FLOAT)/futures.open_interest as mm_net_as_percent_oi
                            FROM futures
                            JOIN market_names on futures.id_name = market_names.id_name
                            ORDER BY futures.id_name, report_date 
                        ) as t1
                    ) as t2;''')

                cur.execute('''CREATE TABLE future_prices 
                    (
                        id_price INTEGER NOT NULL PRIMARY KEY,
                        id_name INTEGER NOT NULL,
                        report_date DATE NOT NULL,
                        open REAL,
                        high REAL,
                        low REAL,
                        close REAL,
                        volume INTEGER,
                        FOREIGN KEY (id_name) REFERENCES market_name (id_name) 
                            ON DELETE CASCADE ON UPDATE NO ACTION,
                        UNIQUE(id_name, report_date)
                    );''')


            elif self.config['data type'] == 'TiFF':
                self.log.info('Create db %s with TiFF format', self.db_filepath)

            con.commit()
        except Exception as e:
            con.rollback()
            self.log.exception(e)  
        finally:
            con.close()      

    def import_cot_data(self, data):
        fpath = pathlib.Path(self.db_filepath)

        if not fpath.exists():
            self.create_db(self.db_filepath)


        try:
            fdata = self.filter_names(data)
            con = sqlite3.connect(self.db_filepath, detect_types=sqlite3.PARSE_DECLTYPES |
                                                        sqlite3.PARSE_COLNAMES)
            cur = con.cursor()

            cur.executemany('''INSERT OR IGNORE INTO futures 
            (id_name, report_date, cftc_code, open_interest, pm_long, pm_short, mm_long, mm_short)
            VALUES (:market_id, :report_date, :CFTC_Contract_Market_Code, 
                :Open_Interest_All, :Prod_Merc_Positions_Long_All, :Prod_Merc_Positions_Short_All,
                :M_Money_Positions_Long_All, :M_Money_Positions_Short_All);''', fdata)

            con.commit()
        
        except Exception as e:
            con.rollback()
            self.log.exception(e)
        finally:
            con.close()

    

    def intialise_filters(self, fmap):
        try:
            market_names = []
            for filter in fmap:
                market_names.append({'display': None, 'filter': filter, 'symbol': fmap[filter]['symbol']})

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
                    if row[2] in fmap:
                        fmap[row[2]]['id'] = row[0]
                        fmap[row[2]]['display_name'] = row[1]
                        fmap[row[2]]['symbol'] = row[3]

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
                market_names.append({'display': fmap[filter]['display_name'], 'filter': filter})

            con = sqlite3.connect(self.db_filepath, detect_types=sqlite3.PARSE_DECLTYPES |
                                                        sqlite3.PARSE_COLNAMES)
            cur = con.cursor()

            # update the display name of existing market names to the latest representation
            cur.executemany('''UPDATE market_names SET display_name = :display
                            WHERE filter_name = :filter''', market_names)

            con.commit()
        except Exception as e:
            con.rollback()
            self.log.exception(e)
        finally:
            con.close()

    def generate_filter_names(self):
        names = {}

        for item in self.config['items']:
            names[item['filter']] = item

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

            for row in data:
                if 'Report_Date_as_YYYY-MM-DD' in row:
                    row['report_date'] = datetime.datetime.strptime(row['Report_Date_as_YYYY-MM-DD'], '%Y-%m-%d').date()
                elif 'Report_Date_as_MM_DD_YYYY' in row:
                    row['report_date'] = datetime.datetime.strptime(row['Report_Date_as_MM_DD_YYYY'], '%Y-%m-%d').date()
                else:
                    self.log.warning('Row missing a field for Report Date: %s', row)
                    continue

                # Optimisation - check if last filter used matches
                if last_filter and last_filter in row['Market_and_Exchange_Names'].upper():
                    row['market_id'] = fmap[last_filter]['id']
                    fdata.append(row)
                else:
                    # must be a new filter so scan list of filters
                    for filter in fmap:
                        if filter in row['Market_and_Exchange_Names'].upper():
                            row['market_id'] = fmap[filter]['id']
                            fdata.append(row)
                            last_filter = filter

                            if not fmap[filter]['display_name']:
                                fmap[filter]['display_name'] = row['Market_and_Exchange_Names'].upper()

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

            cur.executemany('''INSERT OR IGNORE INTO future_prices 
            (id_name, report_date, open, high, low, close, volume)
            VALUES (:market_id, :Date, :Open, 
                :High, :Low, :Close, :Volume);''', data)

            con.commit()
        
        except Exception as e:
            con.rollback()
            self.log.exception(e)
        finally:
            con.close()