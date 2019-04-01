from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from .models import Restaurant
from .models import Review
import requests
# Create your views here.

def home(request):
    return render(request,'home.html')


def result(request):
    try:
        if(request.method == "GET"):
            query = request.GET.get('search_bar', None)
            #if(request.GET.get('checkbox',None) == null):
            #    print("checkbox is unchecked")
            #else:
            #    print("checkbox is checked")
            words = query.split()
            for x in words:
                print(x)

            url = "http://localhost:8983/solr/restaurants/select?q="
            #url += "Restaurant%3A" + x

            for i, x in enumerate(words):
                if(i == 0):
                    url += "Restaurant%3A"+ x
                else:
                    url += "%20%7C%7C%20Restaurant%3A"+ x

                url += "%20%7C%7C%20Price%3A" + x
                url += "%20%7C%7C%20Number%3A" + x
                url += "%20%7C%7C%20Type%3A" + x

            url = url + "&rows=10"

            #url = "http://localhost:8983/solr/reviews/select?q=Reviews%3A" + x +"&rows=10"
            #http://localhost:8983/solr/restaurants/select?q=Restaurant%3Aupstate%20%7C%7C%20Type%3Aseafood%20%7C%7C%20Restaurant%3ABurger
            #"%20%7C%7C%20"
            print(url)
            r = requests.get(url)
            json_data = r.json()
            doc = json_data["response"]["docs"]
            print(doc)
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
