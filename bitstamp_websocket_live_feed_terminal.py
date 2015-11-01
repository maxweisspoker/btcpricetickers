#!/usr/bin/env python

# Simple script to print Bitstamp USD short order book in realtime
# Tested on  Python 2.7 and 3.4

# Standard lib imports:
from __future__ import print_function
import time
import logging
import json

# Non-standard lib imports:
import pusherclient
  # https://github.com/ekulyk/PythonPusherClient
  # Some code taken from examples in his readme file
  # Using his code requires displaying the license, shown at the end of this file

# Bitstamp pusher websocket API info: https://www.bitstamp.net/websocket/
pusherkey = "de504dc5763aeef9ff52"
pusherevent = "data"
pusherchannel = "order_book"

global pusher

class Stream_Printer():
    @classmethod
    def write(class_obj, stream):
        stream = stream.replace("\\","")
        if "Connection: Message - {" in stream:
            if "Message: 'Connection: Message - " in stream:
                stream = stream[10:-1]
            stream = stream.strip()[22:].replace(" ","").replace('":"{"','":{"').replace(']}","',']},"')
            try:
                stream_dict = json.loads(stream)
            except:
                pass
            else:
                if stream_dict[u'event'] == u'data':
                    stream_bids_list = stream_dict[u'data'][u'bids']
                    stream_asks_list = stream_dict[u'data'][u'asks']
                    bids_dict = {}
                    bids_list = []
                    for bid in stream_bids_list:
                        current_bid = round(float(bid[0]),2)
                        bids_dict[current_bid] = round(float(bid[1]),8)
                        bids_list.append(current_bid)
                    asks_dict = {}
                    asks_list = []
                    for ask in stream_asks_list:
                        current_ask = round(float(ask[0]),2)
                        asks_dict[current_ask] = round(float(ask[1]),8)
                        asks_list.append(current_ask)
                    bids_list.sort(reverse=True)
                    asks_list.sort()
                    len_bids_list = len(bids_list)
                    len_asks_list = len(asks_list)
                    if len_asks_list > len_bids_list:
                        len_range = len_bids_list
                    else:
                        len_range = len_asks_list
                    print("Bid_Price     Bid_Amount_BTC          Ask_Price     Ask_Amount_BTC")
                    for i in range(len_range):
                        out_string = str('{0:.2f}'.format(bids_list[i]))
                        for j in range(14 - len(out_string)):
                            out_string = out_string + " "
                        out_string = out_string + str('{0:.8f}'.format(bids_dict[bids_list[i]]))
                        for j in range(38 - len(out_string)):
                            out_string = out_string + " "
                        out_string = out_string + str('{0:.2f}'.format(asks_list[i]))
                        for j in range(52 - len(out_string)):
                            out_string = out_string + " "
                        out_string = out_string + str('{0:.8f}'.format(asks_dict[asks_list[i]]))
                        print(out_string)
                    print()

def connect_handler(data):
    channel = pusher.subscribe(pusherchannel)
    channel.bind(pusherevent, callback)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_stream_handler = logging.StreamHandler(Stream_Printer)
logger.addHandler(log_stream_handler)

pusher = pusherclient.Pusher(pusherkey)
pusher.connection.bind('pusher:connection_established', connect_handler)
pusher.connect()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\nKeyboard interrupt detected, exiting...\n")
    exit(0)
except:
    exit(1)


### pusherclient code license ###
'''
Copyright (c) 2011 Erik Kulyk

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
#################################

