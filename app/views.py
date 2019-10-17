from django.shortcuts import render, redirect
from lxml import etree

# Create your views here.

def home(request):
    return render(request, "main.html")


def ListaReceitas(request):
    doc = etree.parse("xml_database.xml")
    search = doc.xpath("//receita")

    information = {}


    for s in search:
        index= s.find("nome").text
        print(s.find("imagem").text)
        information[index] = []
        information[index].append(s.find("imagem").text)
        information[index].append(s.find("autores/nome_autor").text)

    return render(request, "ListaReceitas.html", {"info": information})
