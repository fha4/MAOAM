# MAOAM: MAOAM Automates Ordering of Amazing Meals

## Overview
MAOAM reduces the effort required to order a meal at a UofM dining hall.

This project is named after the candy brand MAOAM and their yummy "[Kracher](https://www.haribo.com/de-de/produkte/maoam/kracher)" candy.

## Program Architecture
MAOAM is built using the [Selenium Python Package](https://www.selenium.dev/). Selenium effectively lets a program click around on a website in the same manner that a human user can. This means that MAOAM can interact with M-Dining's websites, despite their lack of APIs.

scrape items

fill out form

## User Guide
The program can be retrieved via `wget https://fha4.github.io/assets/python/MAOAM.py`.

Program usage: `python3 MAOAM.py`

## Limitations
- only orders breakfast at bursley lol, also has my allergies and nothing else
- very susceptible to minor changes in html content


NOTE TO FRANK: NEEDS CHROMEDRIVER AND TEMPLATE CONFIGS FILE
