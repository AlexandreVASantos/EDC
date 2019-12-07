from builtins import iter, next

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
from SPARQLWrapper import SPARQLWrapper,JSON


def home(request):
    return render(request, "main.html")


def listrecipes(request):

    return render(request,"list_recipes.html", {"info":getInfoReceita(),"autores" : getAutores(), "categorias" : getCategorias(), "tags" : getTipos(), "dificuldade": getDificuldades()})

def applyFilters(request):
   return None



def check_if_in_list_ahead(item_list):
    tmp_list = []

    for i in range(0, len(item_list)):
        tmp_list.append(item_list[i].split(",")[0])

    for i in range(0, len(tmp_list)):

        if tmp_list[i] in tmp_list[i + 1:]:
            return True

    return False


def add_receita(request):
    return render(request, 'add.html')


@csrf_exempt
def edit_recipe(request):
    return None


def edit_receita(request):
    print(getAutores())
    print(getDificuldades())
    print(getTipos())
    print(getCategorias())
    return render(request, 'edit.html')


def add_recipe(request):
    return None


def delete(request):
    return None

def del_recipe(request):
    return None

def show_recipe(request, recipe):
    return None


def getNomesReceitas():
    endpoint = "http://localhost:7200"
    repo_name = "receitas"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    query = 'PREFIX predRec:<http://receita/pred/>' \
            'Select ?n_receita where{' \
            '?r predRec:nome ?n_receita' \
            '}order by asc(UCASE(str(?n_receita)))'
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)

    list_nomes=[]
    for rec in res["results"]["bindings"]:
        list_nomes.append(rec["n_receita"]["value"])

    return list_nomes




def getAutores():
    endpoint = "http://localhost:7200"
    repo_name = "receitas"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    query = 'PREFIX aut:<http://receita/autores/pred/nome>' \
            'Select ?n_autor where{'\
            '?n aut: ?n_autor.' \
            '}'
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)

    list_autores = []
    for rec in res["results"]["bindings"]:
        list_autores.append(rec["n_autor"]["value"])

    return list_autores


def getTipos():

    endpoint = "http://localhost:7200"
    repo_name = "receitas"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    query = 'PREFIX tip:<http://receita/tipos/pred/nome>' \
            'Select ?n_tip where{'\
            ' ?tipo tip: ?n_tip.' \
            '}'
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)

    list_tipos = []
    for rec in res["results"]["bindings"]:
        list_tipos.append(rec["n_tip"]["value"])

    return list_tipos


def getDificuldades():
    endpoint = "http://localhost:7200"
    repo_name = "receitas"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    query = 'PREFIX dif:<http://receita/dificuldades/pred/nome>' \
            'Select ?n_dif where{' \
            ' ?d dif: ?n_dif.' \
            '}'
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)

    list_dificuldades = []
    for rec in res["results"]["bindings"]:
        list_dificuldades.append(rec["n_dif"]["value"])

    return list_dificuldades


def getCategorias():

    endpoint = "http://localhost:7200"
    repo_name = "receitas"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    query = 'PREFIX cat:<http://receita/categorias/pred/nome>' \
            'Select ?n_cat where{' \
            ' ?c cat: ?n_cat.' \
            '}'
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)

    list_categorias = []
    for rec in res["results"]["bindings"]:
        list_categorias.append(rec["n_cat"]["value"])

    return list_categorias


def getInfoReceita():
    receitas = getNomesReceitas()

   
    endpoint = "http://localhost:7200"
    repo_name = "receitas"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    receitas_info = {}
    for rec in receitas:
        print(rec)
        query = 'PREFIX predRec:<http://receita/pred/>' \
                'Select ?imagem where{' \
                ' ?r predRec:nome "' + rec + '".' \
                ' ?r predRec:imagem ?imagem. '\
                '}'
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
        res = json.loads(res)

        receitas_info[rec] = []
        receitas_info[rec].append(res["results"]["bindings"][0]["imagem"]["value"])

        query = 'PREFIX predRec:<http://receita/pred/>'\
                'PREFIX aut:<http://receita/autores/pred/nome>'\
                'Select ?autor where{'\
                '?r predRec:nome "'+ rec +'".'\
                '?r predRec:autor ?id_a.'\
                '?id_a aut: ?autor.'\
                '}'
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
        res = json.loads(res)
        autores_rec=[]

        for autor in res["results"]["bindings"]:
            autores_rec.append(autor["autor"]["value"])

        receitas_info[rec].append(autores_rec)


    return receitas_info





