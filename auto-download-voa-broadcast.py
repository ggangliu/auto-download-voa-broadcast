# -*- coding: utf-8 -*-
"""
This tool help to download voa broadcast automatically every day.
    1. Download all mp3 file from last time to current day.
    2. export http_proxy=''
How to implement:
    #Getting the date of last download
    #Prepare to download all mp3 file which are in this duration
    #Check whether every link of mp3 is valid
    #Download it if it is valid, or use a txt file instead
    #Save current date


Created on Fri Jun 15 14:17:40 2019

@author: ggang.liu
"""

import shutil, datetime, shelve, time, sys, os
import requests

server_error   = '404 - File or directory not found'
last_date_file = "last_date"
last_date_key  = "date"
url_template   = "http://av.voanews.com/clips/VLE/{0}-003000-VLE122-program_hq.mp3?download=1"


def is_valid_link(file_url, invalid_msg):
    """
    check if mp3_url is valid
    """
    text = ''
    return True
    with requests.get(file_url, proxies=http_proxies) as response:
        print(response.text)
        text = response.text
        
    return True if invalid_msg in text else False


def is_valid_data(date_str):
    """Check if date string is valid"""
    try:
        time.strptime(date_str, "%Y%m%d")
        return True
    except:
        return False


def download_file(file_url, file_name):
    """
    downdload file
    """
    with requests.get(file_url, stream=True, proxies=None) as response, open(file_name, 'wb') as local_file:
        shutil.copyfileobj(response.raw, local_file)


def get_file_list(begin_date, end_date):
    """
    get all file what we want to download
    """
    date_list = []
    while begin_date <= end_date:
        date_dir = begin_date.strftime("%Y/%m/%d/")
        date_str = begin_date.strftime("%Y%m%d")
        date_list.append(date_dir+date_str)
        begin_date += datetime.timedelta(days=1)
        
    return date_list


def get_last_date(file, default_date):
    """
    get last date from file
    """
    date = default_date
    if os.path.exists(file):
        s = shelve.open(file, writeback=True)
        last_date = s[last_date_key]
        s.close()
        date = datetime.datetime.strptime(last_date, "%Y%m%d")
    
    return date


def store_current_date(file, date):
    """
    store current date as the next begin date
    """
    s = shelve.open(file, writeback=True)
    s[last_date_key] = date
    s.close()


def handle_parameters(parameters):
    end_date   = datetime.datetime.strptime(time.strftime('%Y%m%d',time.localtime(time.time())), "%Y%m%d")
    begin_date = end_date
    #begin_date = datetime.datetime.strptime("20190701", "%Y%m%d")
    if len(parameters) >= 3:
        begin_date = datetime.datetime.strptime(parameters[1], "%Y%m%d") if is_valid_data(parameters[1]) else exit(-1)
        end_date   = datetime.datetime.strptime(parameters[2], "%Y%m%d") if is_valid_data(parameters[2]) else exit(-1)
    elif len(parameters) >= 2:
        begin_date = datetime.datetime.strptime(parameters[1], "%Y%m%d") if is_valid_data(sys.argv[1]) else exit(-1)
    else:
        #if there is a last time, we use it as begin_date, otherwise we use end_date as begin_date.
        begin_date = get_last_date(last_date_file, begin_date) 
 
    return begin_date, end_date


if "__main__" == __name__:
    begin_date, end_date = handle_parameters(sys.argv)
    
    #get date list
    date_list = get_file_list(begin_date, end_date)
    print(date_list)
    
    for date in date_list:
        file_url = url_template.format(date)
        if is_valid_link(file_url, server_error):
            print("Downloading: " + file_url)
            download_file(file_url, "voa_broadcast_"+date[-8:]+".mp3")
        else:
            with open(date[-8:]+'.txt', 'w') as f:
                f.write(file_url)

    

        
