#!/usr/bin/python3 -O
"""check_web_response.py - uses selenium and firefox webdriver to do a simple website response check and report back time
and check vs crit/warn - intended for use with iCinga or Nagios.   """
# (c) 2022 Daniel Tate
# Intended for personal use, use at your own risk.  No promises, including regarding accuracy.
# Build 010

import argparse
from time import perf_counter
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
import os

opts = FirefoxOptions()
driver_path= '/bin/geckodriver'

opts.add_argument("--headless")

if __debug__:
    service = FirefoxService(driver_path) # we want logs in debug mode
else:
    service = FirefoxService(driver_path, log_path=os.devnull)

driver = webdriver.Firefox(
    service=service,
    options=opts
)

def run_check (sitein):

    try:
        driver.get(sitein)
        driver.quit()
    except:
        driver.close()
        driver.quit()
        print(f"UNKNOWN: Browser Exception (check URL?)")
        exit(3)


def validate_normal(time):
    if (time < args.warn):
        print(f"OK {time} | time={time}")
        exit(0)

    elif (time >= args.warn and time < args.crit):
        print(f"WARN {time} | time={time}")
        exit(1)
    else:
        print(f"CRITICAL {time} | time={time}")
        exit(2)

parser = argparse.ArgumentParser(description="bleh")
parser.add_argument('-c', '--crit', help='Critical Threshold', type=int, required=True)
parser.add_argument('-w', '--warn', help='Warning Threshold', type=int, required=True)
parser.add_argument('-s', '--site', help='site', required=True)
args = parser.parse_args()

tick = perf_counter()
run_check(args.site)
tock = perf_counter()
clock = tock - tick
short_clock = float(f'{clock:.2f}')

validate_normal(short_clock)