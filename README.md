# IRproject

install django == 1.11.4

open terminal type : "$ pipenv install requests" to import python requests library

open terminal, go to solr file type : "bin/solr start" to start solr server" (must open solr first cuz django website
is making requests to solr server for API)

NOTE: The Solr api link i am using in the codes is based on the naming i gave to my Solr cores (reviews, restaurants). If u are using ur own Solr file, can go to the respective api call link in the python code and change the naming (in views.py and search.py) OR u can use my uploaded Solr folder (might be outdated)
 
open new terminal window, go to django root folder type : "python3 manage.py runserver" to run the website"
