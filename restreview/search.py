import requests

def search_by_restaurant(query, rating, price):

    words = query.split()

    if(len(words)==0):
        url = "http://localhost:8983/solr/restaurants/select?q=&rows=100"

    else:
        for x in words:
            print(x)

        url = "http://localhost:8983/solr/restaurants/spell?q=("

        for i, x in enumerate(words):
            if(i == 0):
                url += "Restaurant%3A"+ x
            else:
                url += "%20%7C%7C%20Restaurant%3A"+ x

            url += "%20%7C%7C%20Type%3A" + x

        url += ")"

        if(rating!="none"):
            url += "%20%26%26%20Number%3A" + rating

        if(price!="none"):
            url += "%20%26%26%20Price2%3A" + price

        url += "&rows=100&spellcheck=on"
        #http://localhost:8983/solr/restaurants/select?q=Restaurant%3Aupstate%20%7C%7C%20Type%3Aseafood%20%7C%7C%20Restaurant%3ABurger

    print(url)
    r = requests.get(url)
    json_data = r.json()
    doc = json_data["response"]["docs"]
    Qtime = json_data["responseHeader"]["QTime"]
    numFound = json_data["response"]["numFound"]

    if numFound==0:
        if len(json_data["spellcheck"]["suggestions"])==0:
            suggestion = ""
        else:
            suggestion = json_data["spellcheck"]["suggestions"][1]["suggestion"][0]["word"]
    else:
        suggestion = ""

    print("Qtime: "+ str(Qtime)+"milliseconds")
    print("numFound:" + str(numFound))

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
            #first_review = doc2[0]["Reviews"][0]
            first_review = doc2[0]["Reviews"]
            #print(first_review)
        review_list.append(first_review)

    #print(review_list)

    doc_with_reviews = zip(doc,review_list)

    return doc_with_reviews, Qtime, numFound, suggestion, query



def search_by_review(query,rating,price):

    words = query.split()
    for x in words:
        print(x)

    url = "http://localhost:8983/solr/reviews/spell?q="

    for i, x in enumerate(words):
        if(i == 0):
            url += "Reviews%3A"+ x
        else:
            url += "%20%7C%7C%20Reviews%3A"+ x

    url += "&rows=15000&spellcheck=on"
    #url = "http://localhost:8983/solr/reviews/select?q=Reviews%3A" + query +"&rows=10"
    print(url)
    r = requests.get(url)
    json_data = r.json()
    doc = json_data["response"]["docs"]
    ID_list = []
    review_list = []

    Qtime = json_data["responseHeader"]["QTime"]
    #numFound = json_data["response"]["numFound"]

    print("Qtime: "+ str(Qtime)+"milliseconds")
    #print("numFound:" + str(numFound))

    if len(json_data["spellcheck"]["suggestions"])==0:
        suggestion = ""
    else:
        suggestion = json_data["spellcheck"]["suggestions"][1]["suggestion"][0]["word"]

    for x in doc:
        a = x["RestaurantID"][0]
        #b = x["Reviews"][0]
        b = x["Reviews"]
        if a not in ID_list:
            ID_list.append(a)
            review_list.append(b)

    print(ID_list)
    #print(review_list)

    #numFound = len(ID_list)

    #print("numFound:" + str(numFound))

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

    ##if doc price and rating do not match query, filter out
    final_doc = []
    final_review = []
    Rating = rating + " star rating"

    print("query: "+Rating+ " , "+price)

    if(rating == "none" and price == "none"):
        final_doc = ranked_doc
        final_review = review_list
    elif(rating != "none" and price != "none"):
        for i, x in enumerate(ranked_doc):
            #print("doc: "+ x["Number"][0] + "," + str(x["Price2"][0]))
            if(x["Number"][0] == Rating and str(x["Price2"][0])==price):
                #print("they are the same")
                final_doc.append(x)
                final_review.append(review_list[i])
    elif(rating == "none" and price != "none"):
        for i, x in enumerate(ranked_doc):
            #print("doc: "+ x["Number"][0] + "," + str(x["Price2"][0]))
            if(str(x["Price2"][0])==price):
                #print("they are the same")
                final_doc.append(x)
                final_review.append(review_list[i])
    elif(rating != "none" and price == "none"):
        for i, x in enumerate(ranked_doc):
            #print("doc: "+ x["Number"][0] + "," + str(x["Price2"][0]))
            if(x["Number"][0] == Rating):
                #print("they are the same")
                final_doc.append(x)
                final_review.append(review_list[i])

    numFound = len(final_doc)

    #doc_with_reviews = zip(ranked_doc,review_list)
    doc_with_reviews = zip(final_doc,final_review)

    return doc_with_reviews, Qtime, numFound, suggestion, query
