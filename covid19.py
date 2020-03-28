#!/usr/bin/env python3
# importing the requests library 
import sys
import time
import hashlib
import json
import logging as log
import threading
import requests

from CovidRetriever import CovidRetriever
from DataStore.CovidDataStore import CovidDataStore

from display_helper import LCDScreen


OUTPUT_FILE_NAME = "COVID_19.log"
LOG_OUTPUT_FORMAT = "%(asctime)s: %(message)s"

HENNEPIN_URL = "https://www.health.state.mn.us/diseases/coronavirus/situation.html"

sleep_minutes = 120
sleep_seconds = sleep_minutes * 60

display_sleep_seconds = 30

data_retriever = None
data_store = None

lcd_screen = None

def setup():
    log.basicConfig( 
        filename=OUTPUT_FILE_NAME,
        format=LOG_OUTPUT_FORMAT, 
        level=log.DEBUG,
        datefmt="%H:%M:%S"
    )

    global data_retriever
    global data_store
    global lcd_screen

    data_retriever = CovidRetriever()
    data_store = CovidDataStore()
    lcd_screen = LCDScreen()

def display_thread_helper(name):

    current_grab_index = 0

    while True:
        log.info("hello")
        message = data_store.get_message_for_index(current_grab_index)

        if message is not None:
            current_grab_index += 1
            
            log.info("Would have logged -> %s", message)
            lcd_screen.print(message)

        time.sleep(display_sleep_seconds)

def case_count_display_string(location, count):
    return "{}\nCases {:,}".format(location, count)

if __name__ == "__main__":
    setup()

    display_thread = threading.Thread(target=display_thread_helper, args=('Display',))

    thread_started = False

    while True:

        try:
            display_messages = []

            response = requests.get(url = HENNEPIN_URL)

            #   Hennepin County
            hennepin_county_count = data_retriever.get_count_for_hennepin(response)

            display_messages.append(
                case_count_display_string(
                    "Hennepin County", 
                    hennepin_county_count
                )
            )

            #   Minnesota
            minnesota_state_count = data_retriever.get_count_for_minnesota(response)

            display_messages.append(
                case_count_display_string(
                    "Minnesota", 
                    minnesota_state_count
                )
            )

            #   Nation
            nation_count = data_retriever.get_count_for_nation()

            display_messages.append(
                case_count_display_string(
                    "U.S.", 
                    nation_count
                )
            )

            data_store.add_messages(display_messages, True)

            if thread_started == False:
                display_thread.start()

        except:
            log.exception("Failed to retrieve data")

        log.info("Will now sleep for %d seconds", sleep_seconds)
        time.sleep(sleep_seconds)