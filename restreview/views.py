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
            print(query)
            url = "http://localhost:8983/solr/reviews/select?q=Reviews%3A" + query +"&rows=10"
            print(url)
            r = requests.get(url)
            json_data = r.json()
            doc = json_data["response"]["docs"]
            print(doc)
    except:
        raise Http404('restaurant/review not found')
    return render(request, 'result.html',{'doc':doc})
