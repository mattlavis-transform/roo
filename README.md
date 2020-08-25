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