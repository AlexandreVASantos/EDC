from django.shortcuts import render, redirect
from lxml import etree
from BaseXClient import BaseXClient


# Create your views here.

def home(request):
    return render(request, "main.html")


def ListaReceitas(request):
    doc = etree.parse("receitas.xml")
    search = doc.xpath("//receita")

    information = {}


    for s in search:
        index= s.find("nome").text
        print(s.find("imagem").text)
        information[index] = []
        information[index].append(s.find("imagem").text)
        information[index].append(s.find("autores/nome_autor").text)

    return render(request, "ListaReceitas.html", {"info": information})

def add_receita(request):
    return render(request, 'add.html')


def edit_receita(request):
    return render(request, 'edit.html')

def add_recipe(request):
    requiredToAdd = ['name', 'cat', 'data', 'tipo', 'aut', 'dificuldade', 'ingredientes', 'passos', 'imagem']
    for req in requiredToAdd:
        if req not in request.POST:
            return render(request, 'add.html', {'error': True})
    # create session
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        session.execute("""xquery import module namespace local = "com.local.my.index" at 'index.xqm';
local:add_receita("""+request.POST.get('name',' ')+','+request.POST.get('dificuldade',' ')+','+request.POST.get('imagem',' ')+','+request.POST.get('data',' ')+')')
        print(session.info())
    finally:
        # close session
        if session:
            session.close()
    return render(request, 'main.html',{'error':False})


