from orionxapi.connection_manager import client#, as_completed
from gql import gql
from requests.exceptions import ConnectionError
from urllib3.exceptions import ReadTimeoutError
import ccxt
import time
import threading
import datetime

DUMMY_RESULT = {
  'orionx': {
    'data': {
      'market': [{
        'open': 2216,
        'close': 2217,
        'high': 2224,
        'low': 2194,
        'volume': 11746144713,
        'variation': 0.0004512635379061436,
        'count': 10,
        'fromDate': 1515884400000,
        'toDate': 1515888000000
      }],
      'book': {
        'buy': [{
          'limitPrice': 2202
        }],
        'sell': [{
          'limitPrice': 2210
        }],
        'spread': 8,
        'mid': 2206
      },
      'curr': {
        'close': 2217,
        'volume': 4197103521174,
        'variation': 0.021658986175115302
      }
    },
    'timestamp': datetime.datetime.now()
  },
  'southx': {
    'data': {
      'symbol': 'CHA/BTC',
      'timestamp': 1515903656840,
      'datetime': '2018-01-14T04:20:57.840Z',
      'high': None,
      'low': None,
      'bid': 0.00017112,
      'ask': 0.00023888,
      'vwap': None,
      'open': None,
      'close': None,
      'first': None,
      'last': 0.00023888,
      'change': 13.74,
      'percentage': None,
      'average': None,
      'baseVolume': 2183.84199041,
      'quoteVolume': None,
      'info': {
        'Bid': 0.00017112,
        'Ask': 0.00023888,
        'Last': 0.00023888,
        'Variation24Hr': 13.74,
        'Volume24Hr': 2183.84199041
      }
    },
    'timestamp': datetime.datetime.now()
  }
}

result_cache = DUMMY_RESULT

def get_result():
  # circular list goes here
  # list.append(timestamp)
  return result_cache

def query_loop():
  orionx_client = client(headers_filename='cache/headers.json',
                cookies_filename='cache/cookies.json')

  query = gql('''
    query getMarketStats($marketCode: ID!, $aggregation: MarketStatsAggregation!, $limit: Int) {
      market: marketStats(marketCode: $marketCode, aggregation: $aggregation, limit: $limit) {
        open
        close
        high
        low
        volume
        variation
        count
        fromDate
        toDate
      }
      book: marketOrderBook(marketCode: $marketCode, limit: $limit) {
        buy {
          limitPrice
        }
        sell {
          limitPrice
        }
        spread
        mid
      }
      
      curr: marketCurrentStats(marketCode: $marketCode, aggregation: d1) {
        close
        volume
        variation
      }
    }

  ''')

  params = {
    "marketCode": "CHACLP",
    "aggregation": "h1",
    "limit": 1
  }

  southx = ccxt.southxchange()
  southx.load_markets()

  cycle_counter = 0
  while True:
    try:
      time.sleep(1.0)
      if cycle_counter % 2 == 0:
        result_cache['orionx'] = {
          'data': orionx_client.execute(query, variable_values=params),
          'timestamp': datetime.datetime.now()
        }
      if cycle_counter % 6 == 0:
        result_cache['southx'] = {
          'data': southx.fetch_ticker('CHA/BTC'),
          'timestamp': datetime.datetime.now()
        }
        cycle_counter = 0
    except (ConnectionError, ReadTimeoutError):
      print('a timeout has ocurred!')
    cycle_counter += 1
def start():
  loop = threading.Thread(target=query_loop, daemon=True)
  loop.start()
  return loop