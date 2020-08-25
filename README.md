# Scrapes the Rules of Origin from the EU's Trade Helpdesk

There are (at the time of writing) 21 rules of origin schemes

1. FTA South Korea
2. Generalised System of Preferences
3. Pan-Euro-Mediterranean Convention
4. Euro-Mediterranean Free Trade Area
5. FTA Chile - Mexico
6. FTA Deep and Comprehensive Trade Agreement
7. FTA Japan
8. FTA Singapore
9. EPA Cariforum
10. FTA Central America
11. FTA Colombia, Ecuador and Peru
12. EPA Pacific
13. EPA South African Development Community (SADC)
14. FTA European Economic Area (EEA)
15. Overseas Countries and Territories
16. GSP Plus
17. EPA Market Access Regulation
18. FTA Canada
19. Specific Measures - Jordan
20. Autonomous Trade Preferences
21. EPA Eastern and Southern Africa

## Notes on schemes

- Each of these schemes have countries that belong to them

- A country can belong to multiple schemes, such as Norway (NO), which belongs to 2  (3. Pan-Euro-Mediterranean Convention and 14. FTA European Economic Area (EEA))

- If you look on the Trade Helpdesk, you can see this duality for Norway:
  https://trade.ec.europa.eu/tradehelp/myexport#?product=0702000007&partner=NO&reporter=AT
  - It lists the RoO schemes as "Rules of Origin EEA" and "Rules of Origin PEM Convention", but they are the same things

## Data structure

Is documented in sql.md

## What the scraper does

- Get a list of the schemes from the database
- Against each scheme, one country code is specified as being the country code to scrape to get the data
- To scrape every country would be take forever and would just repeat itself for no gain
- For each scheme:
  - select the code_to_scrape (which is the geographical_area_code)
  - this is just the first alphabetically
  - Loop through all chapters of the tariff (1 to 99, omitting 77, which is not used)
    - Because screen-scraping is slow, take copies of the JSON, so that this can be run locally if needed
    - Otherwise, go to https://webgate.ec.europa.eu/roo/public/v1//classic/chapter/" + chapter + "/country/" + my_country.country + "?language=EN"
      - this is the URL called by the Trade Helpdesk angular app to populate the RoO tabs
    - Grab the rules node of the JSON and cleanse it: the HTML is a full of errors - we need to remove all the duff HTML
    - Write the unfiltered and the filtered JSON to local folders that can be used instead of always scraping data
  - After all 99 chapters have been scraped and cleansed, write a single JSON file to the country's subfolder
  - Also write a Word document equivalent