import requests

def search_by_restaurant(query):

    words = query.split()
    for x in words:
        print(x)

    url = "http://localhost:8983/solr/restaurants/select?q="

    for i, x in enumerate(words):
        if(i == 0):
            url += "Restaurant%3A"+ x
        else:
            url += "%20%7C%7C%20Restaurant%3A"+ x

        url += "%20%7C%7C%20Price%3A" + x
        url += "%20%7C%7C%20Number%3A" + x
        url += "%20%7C%7C%20Type%3A" + x

    url = url + "&rows=10"

    #http://localhost:8983/solr/restaurants/select?q=Restaurant%3Aupstate%20%7C%7C%20Type%3Aseafood%20%7C%7C%20Restaurant%3ABurger

    print(url)
    r = requests.get(url)
    json_data = r.json()
    doc = json_data["response"]["docs"]
    return doc

def search_by_review(query):

    url = "http://localhost:8983/solr/reviews/select?q=Reviews%3A" + query +"&rows=10"
    print(url)
    r = requests.get(url)
    json_data = r.json()
    doc = json_data["response"]["docs"]
    return doc
