#!/usr/bin/python3
import argparse
from time import perf_counter
from selenium import webdriver
from selenium.webdriver import FirefoxOptions

opts = FirefoxOptions()
opts.add_argument("--headless")

def run_check (sitein):
    browser = webdriver.Firefox(options=opts)
    browser.get(sitein)
    browser.quit()

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

if __debug__: print(f"DEBUG: site is {args.site}")
tick = perf_counter()
if __debug__: print(f"DEBUG: Site check commencing, Tick is {tick}")
run_check(args.site)
tock = perf_counter()
if __debug__: print(f"DEBUG: Site check complete, tock is {tock}")
clock = tock - tick
if __debug__: print (f"DEBUG: Clock is {clock}")
short_clock = float(f'{clock:.2f}')
if __debug__: print(f"DEBUG: short_clock is {short_clock}")

validate_normal(short_clock)
