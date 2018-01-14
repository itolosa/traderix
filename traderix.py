#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, PreCheckoutQueryHandler, ShippingQueryHandler)
import logging

import connvars
import fetcher
import telegram

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# handler initialization with custom headers

fetcher_thread = fetcher.start()

def get_emoji(value):
  if value < -2.0:
    return '😷'
  if value < -1.0:
    return '😔'
  if value < 0.0:
    return '😒'
  if value < 1.0:
    return '😏'
  if value < 2:
    return '🤤'
  if 2 <= value:
    return '🤑'


def error(bot, update, error):
  """Log Errors caused by Updates."""
  logger.warning('Update "%s" caused error "%s"', update, error)

def start_callback(bot, update):
  msg = "Use /precio para ver el precio de la ultima transaccion."
  update.message.reply_text(msg)

def price_callback(bot, update):
  result = fetcher.get_result()
  msg = '*Orionx:*\n'
  #print(result)
  orionx_price = result['orionx']['data']['book']['sell'][0]['limitPrice']
  msg += '  Precio: %d CLP\n' % orionx_price
  msg += '  Variación 1H: %.2f%% %s\n' % (result['orionx']['data']['market'][0]['variation']*100.0, get_emoji(result['orionx']['data']['market'][0]['variation']*100.0))
  msg += '  Volumen 1H: %s\n' % "{:,.8}".format(result['orionx']['data']['market'][0]['volume']/(10**8))
  msg += '  Variacion 24H: %.2f%% %s\n' % (result['orionx']['data']['curr']['variation']*100.0, get_emoji(result['orionx']['data']['curr']['variation']*100.0))
  msg += '  Volumen 24H: %s\n' % "{:,.8}".format(result['orionx']['data']['curr']['volume']/(10**8))
  msg += '  Spread: %d\n' % result['orionx']['data']['book']['spread']
  msg += '  _Ultima actualizacion: %s_\n\n' % result['orionx']['timestamp'].strftime('%H:%M:%S %d/%m/%Y')
  msg += '*SouthxChange:*\n'
  msg += '  Precio: %.6f BTC\n' % result['southx']['data']['info']['Last']
  msg += '  Variación 24H: %.2f%% %s\n' % (result['southx']['data']['info']['Variation24Hr'], get_emoji(result['southx']['data']['info']['Variation24Hr']))
  msg += '  Volumen 24H: %s\n' % "{:,.2f}".format(result['southx']['data']['info']['Volume24Hr'])
  msg += '  Deposito 1 CHA<=(OrionX: %f CHA<= %d CLP)\n' % ((1+0.0004048), round((1+0.0004048)*(1-(0.29/100.0))*orionx_price,0))
  msg += '  Retiro 1 CHA=>(OrionX: %f CHA=> %d CLP)\n' % ((1-0.01), round((1-0.01)*(1-(0.29/100.0))*orionx_price, 0))
  msg += '  _Ultima actualizacion: %s_\n\n' % result['southx']['timestamp'].strftime('%H:%M:%S %d/%m/%Y')
  msg += 'Traderix 2018 | [Donate](https://github.com/itolosa/traderix#donations) | [Fork me on Github](https://github.com/itolosa/traderix'
  update.message.reply_text(msg, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)

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