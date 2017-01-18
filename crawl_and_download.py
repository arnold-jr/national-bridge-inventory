#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import zipfile
import io

def main():
  base_url = "http://www.fhwa.dot.gov/bridge/nbi/"
  regexes = {0: re.compile("[0-9]\s+Data"),
             1: re.compile("zip file"),
             2: re.compile("Proceed to Data")
             }

  def follow(url_leaf, level):
    url = urljoin(base_url, url_leaf)
    resp = requests.get(url, stream=True)
    if resp.status_code != 200:
      raise ValueError("Invalid response from url {0} at level {1}".format(url, level))
      
    if level == 3:
      # Download the zip file
      z = zipfile.ZipFile(io.BytesIO(resp.content))
      z.extractall()
    else:
      soup = BeautifulSoup(resp.text, "lxml")
      anchors = soup.find_all("a", text=regexes[level])
      if level == 1:
        # Only follow the last zip link
        anchors = [anchors[-1]]
      for a in anchors:
        follow(a['href'], level+1)
  
  follow("ascii.cfm", 0)

if __name__ == "__main__":
  main()
