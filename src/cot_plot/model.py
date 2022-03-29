
import src.common.program as program
import os
import sqlite3
import logging

class DBmodel():
    def __init__(self, file_name):
        self.log = logging.getLogger(__name__)
        self.db_filepath = os.path.join(program.get_base_dir('store'), file_name)


    def get_commodity_data(self, com_code):
        data = {
            'future_name': '',
            'cot': [],
            'price': [],
        }
        try:
            param = {'code': com_code}
            con = sqlite3.connect(self.db_filepath, detect_types=sqlite3.PARSE_DECLTYPES |
                                                        sqlite3.PARSE_COLNAMES)
            cur = con.cursor()

            cur.execute('''SELECT display_name FROM market_names WHERE symbol = :code ''', param)
            result = cur.fetchone()
            if result:
                data['future_name'] = result[0]

            cur.execute('''SELECT report_date, open_interest, dealer_net_5_yr, spec_net_5_yr
                    FROM future_calc
                    JOIN market_names on future_calc.id_name=market_names.id_name
                    WHERE market_names.symbol = :code;
                ''', param)

            result = cur.fetchall()
            for r in result:
                if r[0] is not None and r[1] is not None and r[2] is not None and r[3] is not None:
                    data['cot'].append({
                        'date': str(r[0]),
                        'oi': r[1],
                        'dealer5': round(r[2]),
                        'spec5': round(r[3])
                    })

            # Get price data
            cur.execute('''SELECT report_date, round(close,2), volume
                    FROM future_prices
                    JOIN market_names on future_prices.id_name=market_names.id_name
                    WHERE market_names.symbol = :code;
                ''', param)

            result = cur.fetchall()
            for r in result:
                if r[0] is not None and r[1] is not None and r[2] is not None:
                    data['price'].append({
                        'date': str(r[0]),
                        'close': r[1],
                        'volume': r[2]
                    })

        except Exception as e:
            self.log.exception(e)

        return data