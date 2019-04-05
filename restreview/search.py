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

    url = url + "&rows=100"

    #http://localhost:8983/solr/restaurants/select?q=Restaurant%3Aupstate%20%7C%7C%20Type%3Aseafood%20%7C%7C%20Restaurant%3ABurger

    print(url)
    r = requests.get(url)
    json_data = r.json()
    doc = json_data["response"]["docs"]

    review_list = []

    for x in doc:
        a = x["ID"][0]
        url2 = "http://localhost:8983/solr/reviews/select?q=RestaurantID%3A" + str(a) + "&rows=10"
        print(url2)
        r2 = requests.get(url2)
        json_data2 = r2.json()
        doc2 = json_data2["response"]["docs"]
        if(len(doc2) == 0):
            print("doc is empty")
            first_review = ""
        else:
            first_review = doc2[0]["Reviews"][0]
            #print(first_review)
        review_list.append(first_review)

    #print(review_list)

    doc_with_reviews = zip(doc,review_list)

    return doc_with_reviews



def search_by_review(query):

    words = query.split()
    for x in words:
        print(x)

    url = "http://localhost:8983/solr/reviews/select?q="

    for i, x in enumerate(words):
        if(i == 0):
            url += "Reviews%3A"+ x
        else:
            url += "%20%7C%7C%20Reviews%3A"+ x

    #url = url + "&rows=10"
    #url = "http://localhost:8983/solr/reviews/select?q=Reviews%3A" + query +"&rows=10"
    print(url)
    r = requests.get(url)
    json_data = r.json()
    doc = json_data["response"]["docs"]
    ID_list = []
    review_list = []

    for x in doc:
        a = x["RestaurantID"][0]
        b = x["Reviews"][0]
        if a not in ID_list:
            ID_list.append(a)
            review_list.append(b)

    print(ID_list)
    #print(review_list)

    url2 ="http://localhost:8983/solr/restaurants/select?q="

    for i, x in enumerate(ID_list):
        if(i==0):
            url2 += "ID%3A"+ str(x)
        else:
            url2 += "%20%7C%7C%20ID%3A"+ str(x)

    url2 += "&rows=100"

    print(url2)
    r2 = requests.get(url2)
    json_data2 = r2.json()
    doc2 = json_data2["response"]["docs"]

    ranked_doc = []

    ##as the doc2 returns document not in the ranking order of ID_list, we need to sort it by rank
    for x in ID_list:
        for y in doc2:
            if(y["ID"][0] == x):
                ranked_doc.append(y)

    doc_with_reviews = zip(ranked_doc,review_list)

    return doc_with_reviews
