import codecs
from email import message
from itertools import count
import json
from array import array

import requests
from bs4 import BeautifulSoup
from termcolor import colored


import aiohttp
import asyncio
import nest_asyncio


nest_asyncio.apply()



google_url = "https://www.google.com"



request_file ='response.html'
water_res = "water.txt"



headersFile = open("google_headers.json","r")
headers = json.load(headersFile)
headersFile.close()

file = open(request_file,'w')
file.write('')
file.close()

file = open(water_res,'w')
file.write('')
file.close()
    
class Google_searcher():


    


    def google_search(self,SearchWords):

        

        url = f"{google_url}/search?q={SearchWords}"


        response = requests.get(url,headers=headers)

        print(colored(f"\n\n Запрос {url} \n\n", 'blue'))

        
        if response.status_code == 429:
            yellow_status_code = colored(str(response.status_code),'yellow')
            messageRed = colored("Много запросов чел",'red')
            print(f"Status:{yellow_status_code} {messageRed}")




        return response.content

        


    def find_href_in_html(self,html):
        GoogleNextPages = []
        SitesPages = []

        soup = BeautifulSoup(html, "html.parser")


        for a in soup.find_all('a',href=True):
            
            # проверяет наличие строки http в ссылке 
            if a['href'].find("http") != -1:
                
                # проверяет пердая строка это http  
                if a['href'][0:4] == "http":
                    SitesPages.append(a['href'])

            else:
                if a['href'].find("start") != -1:
                    GoogleNextPages.append(f"{google_url}{a['href']}")
        
        return (GoogleNextPages,SitesPages)


    async def MakeGetAsyncRequest(self,url):

        try:

            async with aiohttp.ClientSession() as session:
                async with session.get(url,timeout=5) as response:
                    
                    stargreen = colored("*","green")
                    print(f"[{stargreen}]",end="")

                    color_status = colored(response.status,'yellow')

                    print(f"Status:{color_status} {url}")

                    html = await response.text()

                    content = [
                        "\n<><><><><><>\n",
                        response.host.join("\n"),
                        html,
                        "\n<><><><><><>\n"
                    ]


                    file = open(request_file,'a')
                    file.write("".join(content))
                    file.close()

        except asyncio.TimeoutError as e:
            print(e)

        except aiohttp.ClientOSError as e:
            print (e)

        except aiohttp.ServerDisconnectedError as e:

            print(e)
    
    
                
    
    async def OpenAllLinksInList(self,SitesPages:array):

        tasks = []        
        for siteUrl in SitesPages:
            task = asyncio.create_task(self.MakeGetAsyncRequest(siteUrl))
            tasks.append(task)
        

        
        await asyncio.gather(*tasks)


    def GetUrlsNextPages(self,GooglePages:array):

        urls = []
        count = 0

        for url in GooglePages:
            count += 1
            print(f"сканирую страницу {count} из  {len(GooglePages)}")
            req = requests.get(url)
            xz,SitesPages = self.find_href_in_html(req.content)


            urls = SitesPages

        return urls    





    def readFileText(self):
        
        file = open(request_file,'r')
        html = file.read()
        file.close()

        water = open(water_res,'a')

        soup = BeautifulSoup(html, "html.parser")
        for p in soup.find_all(['p','li']):
            water.write(p.text)

