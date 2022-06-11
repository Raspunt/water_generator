from Requester import Google_searcher
import asyncio


ggs = Google_searcher()
html = ggs.google_search("Почему я дебил")

googleNextPages,SitesPages = ggs.find_href_in_html(html)




SitesPages += ggs.GetUrlsNextPages(googleNextPages)
print("найдено cсылок", len(SitesPages))

asyncio.run(ggs.OpenAllLinksInList(SitesPages))
    





print("\n\n\n")
ggs.readFileText()