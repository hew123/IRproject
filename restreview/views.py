from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from .models import Restaurant
from .models import Review
import requests
from .search import search_by_restaurant, search_by_review
# Create your views here.

def home(request):
    return render(request,'home.html')


def result(request):
    try:
        if(request.method == "GET"):

            query = request.GET.get('search_bar', None)
            rating = request.GET.get('rating', None)
            price = request.GET.get('price', None)

            if request.GET.get('checkbox', None) == "on":
                print("checked")
                doc, Qtime, numFound, suggestion, query = search_by_review(query,rating,price)
            else:
                print("unchecked")
                doc, Qtime, numFound, suggestion, query = search_by_restaurant(query,rating,price)
                #temp_doc, temp_time, temp_numFound = search_by_restaurant(query,rating)
                #if(temp_numFound == 0):
                #    doc, Qtime, numFound = search_by_review(query)
                #else:
                #    doc, Qtime, numFound = temp_doc, temp_time, temp_numFound
    except:
        raise Http404('restaurant/review not found')

    return render(request, 'result.html',{'doc':doc, 'Qtime':Qtime, 'numFound':numFound,'suggestion':suggestion,'query':query})
    #return render(request, 'result.html')


def info(request):
    try:
        if(request.method == "GET"):
            query = request.GET.get('RestaurantID', None)
            print("helllpooo ur query is "+query)
            #url = "http://localhost:8983/solr/reviews/select?q=RestaurantID%3A" + query +"&rows=10"
            url = "http://localhost:8983/solr/reviews/select?q=RestaurantID%3A" + query + "&rows=150"
            print(url)
            r = requests.get(url)
            json_data = r.json()
            doc = json_data["response"]["docs"]
            #print(doc)

            url2 ="http://localhost:8983/solr/restaurants/select?q=ID%3A" + query
            print(url2)
            r2 = requests.get(url2)
            json_data2 = r2.json()
            doc2 = json_data2["response"]["docs"]
    except:
        raise Http404('restaurant/review not found')
    #print(request)
    return render(request, 'info.html',{'doc':doc,'doc2':doc2})
    #return render(request, 'info.html')
