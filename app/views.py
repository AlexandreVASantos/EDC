from django.shortcuts import render, redirect
from lxml import etree

# Create your views here.

def home(request):
    return render(request, "main.html")


def ListaReceitas(request):
    doc = etree.parse("xml_database.xml")
    search = doc.xpath("//receita")

    send = {}
    index = 1

    for s in search:
        send[index] = s.find("nome").text
        index = index + 1

    return render(request, "ListaReceitas.html", {"send": send})
