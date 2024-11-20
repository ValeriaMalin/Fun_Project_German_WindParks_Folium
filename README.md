# Fun_Project_German_WindParks_Folium
This is a small visualization project of geospatial data

The Aim for the project was to train using of Folium and additionally Web Scraping from Wikipedia
The repository consists of 4 Notebooks:
1. 1_windcrafts_scraping.ipynb  : protocol of WebScraping using BeautifulSoup Biblithek from Wikipedia of multiple table with the information
   for the Wind Crafts (cleaning , foramtting, and merge of data)
2. 2_landkreis_id_scraping.ipynb : Scraping of tables directly as pandas DataFrame , here I had to join the Landkreis ShorName and Nuts 3 ID
3. 3_offshore_windParks_scraping.ipynb : Scraping of the table from WIkipedia , I needed here the coordiantes of the Offshores Wind Parks
4. Mapping_windcrafts.ipynb  : Work with Folum, Marker Cluster for the Offshore WindParks, and two Choropleths layers to show the numbers of the Windcrafts for every Landkreis and their average Age.

   Work is on going 
