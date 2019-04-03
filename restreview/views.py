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
            #query2 = request.GET.get('checkbox', None)
            #print("checkbox1111 is "+query2)
            if request.GET.get('checkbox', None) == "on":
                print("checked")
                doc = search_by_review(query)
            else:
                print("unchecked")
                doc = search_by_restaurant(query)
            #print(doc)
    except:
        raise Http404('restaurant/review not found')

    return render(request, 'result.html',{'doc':doc})
    #return render(request, 'result.html')


def info(request):
    try:
        if(request.method == "GET"):
            query = request.GET.get('RestaurantID', None)
            print("helllpooo ur query is "+query)
            url = "http://localhost:8983/solr/reviews/select?q=RestaurantID%3A" + query +"&rows=10"
            print(url)
            r = requests.get(url)
            json_data = r.json()
            doc = json_data["response"]["docs"]
            print(doc)
    except:
        raise Http404('restaurant/review not found')
    #print(request)
    return render(request, 'info.html',{'doc':doc})
    #return render(request, 'info.html')
