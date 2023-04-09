__AUTHOR__="Naci Caner"

import requests as req
from bs4 import BeautifulSoup as btu
from typing import Union
import logging
import datetime
from sys import exit as close_progam
import re
import json

class Zhone_Info:
    def __init__(self) -> None:
        self.domain = input("Domain:").strip()
        self.url = f"https://check-host.net/ip-info?host={self.domain}"
        self.headers = {r"User-Agnet":"Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H321 [FBAN/FBIOS;FBAV/38.0.0.6.79;FBBV/14316658;FBDV/iPad4,1;FBMD/iPad;FBSN/iPhone OS;FBSV/8.4.1;FBSS/2; FBCR/;FBID/tablet;FBLC/en_US;FBOP/1"}
        logging.basicConfig(filename="back.log",
                            format='%(asctime)s %(message)s',
                            filemode='w')
        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)
        self.log.info(f"{datetime.datetime.now()} - The Program was run")
        self.log.info(f"Host Entered, Entered Host Name:{self.url}")
        self.flags = ""
        self.__zone__(self.url)
        self.__İmg__()



    def __zone__(self, url:Union[bytes | str]) -> str:

        """
        Gets Host Status for Entered Site
        :parameter str(host,bytes)
        :return: json format
        Explanation:
        44: Submits a GET Request to the Site with the Domain Name in
        45-59: codes in this line range: Analyzes the status codes in Zone_Requests variable and writes it to the log file
        61-66 Line: Section of Tables Containing Classes with Information Related to IP Addresses
        68:I wrote this line because there are too many spaces in the incoming data:be warned though this removes "all whitespace characters (space, tab, newline, return, form feed)" . In, "this is \t a test\n" will effectively end up as "this is a test"
        69-88:The incoming data string was somehow plain. I extracted the plain data with the re module. I pulled the necessary information.
        89: To pull the flags, I shortened the country name and deleted the next () and made it smaller with upper()
        91-104:In order to make the incoming data json, I first converted it to dictionaries, then I converted it to json data with "json.dumps", as a result, the data is now Json
        """
        Zone_Requests = req.get(url=url, headers=self.headers)
        match Zone_Requests.status_code:
            case 200:
               self.log.info("200 Successful")
            case 404:
               self.log.critical("The Requested Page cannot Be Found")
               close_progam()
            case 400:
               self.log.critical("The server cannot or will not process the request due to something that is perceived to be a client error (e.g., malformed request syntax, invalid request message framing, or deceptive request routing)")
               close_progam()
            case 500:
               self.log.critical("The server has encountered a situation it does not know how to handle.")
               close_progam()
            case 504:
               self.log.critical("This error response is given when the server is acting as a gateway and cannot get a response in time.")
               close_progam()

        Zone_Html = Zone_Requests.text
        Zone_Soup = btu(Zone_Html,"html.parser")
        Div_incontent = Zone_Soup.find_all("div",id="incontent")
        for i in Div_incontent:
            Div_ipinfo = i.find("div",id="ip_info-dbip")
            Tbody = Div_ipinfo.find("table").text

        text = " ".join(Tbody.split())
        try:
            ip_address = re.search(r"IP address (\d+\.\d+\.\d+\.\d+)", text).group(1)
        except:
            ...
        try:
            host_name = re.search(r"Host name (\d+\.\d+\.\d+\.\d+)", text).group(1)
        except:
            host_name = None
        ip_range = re.search(r"IP range (\d+\.\d+\.\d+\.\d+-\d+\.\d+\.\d+\.\d+)", text).group(1)
        isp = re.search(r"ISP (.+?) Organization", text).group(1)
        try:
            organization = re.search(r"Organization (.+?) Country", text).group(1)
        except:
            organization = None
        country = re.search(r"Country (.+?) Region", text).group(1)
        region = re.search(r"Region (.+?) City", text).group(1)
        city = re.search(r"City (.+?) Time zone", text).group(1)
        time_zone = re.search(r"Time zone (.+?) Local time", text).group(1)
        local_time = re.search(r"Local time (.+?) Postal Code", text).group(1)
        postal_code = re.search(r"Postal Code (.+?) Powered by", text).group(1)
        self.flags = country.split(" ")[1].replace("(", "").replace(")", "").lower()
        data = {
               "IP address": ip_address,
               "Host name": host_name,
               "IP range": ip_range,
               "CIDR": "N/A",
               "ISP": isp,
               "Organization":organization,
               "Country": country,
               "Region": region,
               "City": city,
               "Time zone": time_zone,
               "Local time": local_time,
              "Postal Code": postal_code
            }
        return_json = json.dumps(data)
        print(return_json)





    def __İmg__(self):
        """
        118: Sends the incoming flag name to this site and receives the flag as content
        119: Writes the incoming content information to the file in the form of .png
        :return: {name of country}.png
        """
        News = req.get(f"https://flagcdn.com/w320/{self.flags}.png")
        with open(f"{self.flags}.png","wb") as f:
            f.write(News.content)

if __name__=="__main__":
    ip = Zhone_Info()