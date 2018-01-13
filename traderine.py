#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, PreCheckoutQueryHandler, ShippingQueryHandler)
import logging

from orionxapi.connection_manager import client
from orionxapi.lib.dsl import DSLSchema
from gql import gql

import connvars

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# handler initialization with custom headers
orionx_client = client(headers_filename='cache/headers.json',
                cookies_filename='cache/cookies.json')

ds = DSLSchema(client)

def error(bot, update, error):
  """Log Errors caused by Updates."""
  logger.warning('Update "%s" caused error "%s"', update, error)

def start_callback(bot, update):
  msg = "Use /precio para ver el precio de la ultima transaccion."
  update.message.reply_text(msg)

def price_callback(bot, update):
  query = gql('''
    query getMarketIdleData($code: ID) {
      market(code: $code) {
        lastTrade {
          price
        }
      }
    }
  ''')

  params = {
    "code": "CHACLP"
  }

  operation_name = "getMarketIdleData"

  result = orionx_client.execute(query, variable_values=params)
  update.message.reply_text('Precio de la ultima Tx: %d' % result['market']['lastTrade']['price'])


def main():
  # Create the EventHandler and pass it your bot's token.
  updater = Updater(token=connvars.token)

  # Get the dispatcher to register handlers
  dp = updater.dispatcher

  # simple start function
  dp.add_handler(CommandHandler("start", start_callback))

  dp.add_handler(CommandHandler("precio", price_callback))

  dp.add_error_handler(error)

  # Start the Bot
  updater.start_polling()

  # Run the bot until you press Ctrl-C or the process receives SIGINT,
  # SIGTERM or SIGABRT. This should be used most of the time, since
  # start_polling() is non-blocking and will stop the bot gracefully.
  updater.idle()


if __name__ == '__main__':
  main()