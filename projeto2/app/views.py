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
    endpoint = "http://localhost:7200"
    repo_name = "receitas"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)

    query = 'PREFIX aut:<http://receita/autores/pred/nome>'\
            'PREFIX cat:<http://receita/categorias/pred/nome>'\
            'PREFIX tip:<http://receita/tipos/pred/nome>'\
            'PREFIX dif:<http://receita/dificuldades/pred/nome>'\
            'PREFIX predRec:<http://receita/pred/>'\
            'Select ?nome ?imagem ?autor where{'\
            '?id predRec:nome ?nome.'\
            '?id predRec:imagem ?imagem.' \
            '?id predRec:autor ?aut_id.'\
            '?aut_id aut: ?autor.'\



    if request.GET.get("authors") != "None":
        query += ' ?aut_id aut: "'+ str(request.GET.get("authors"))+'". '

    if request.GET.get("dificuldade") != "None":
        query += '?id predRec:dificuldade ?id_d. ?dif_id dif: "' + str(request.GET.get("dificuldade")) + '". '

    if request.GET.get("categorias") != "None":
        query += '?id predRec:categoria ?cat_id. ?cat_id cat: "' + str(request.GET.get("categorias")) + '". '

    if request.GET.get("tags") != "None":
        query += '?id predRec:tipo ?id_t. ?id_t tip: "' + str(request.GET.get("tags")) + '". '

    query += '}order by asc(UCASE(str(?nome)))'

    print(query)
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    info = {}

    for rec in res["results"]["bindings"]:
        auth_list = []
        print(rec)
        info[rec["nome"]["value"]] = []
        info[rec["nome"]["value"]].append(rec["imagem"]["value"])
        if isinstance(rec["autor"]["value"], list):
            for auth in rec["autor"]["value"]:
                auth_list.append(auth)
        else:
            auth_list.append(rec["autor"]["value"])


        info[rec["nome"]["value"]].append(auth_list)

    return render(request, "list_recipes.html", {"info":info,"autores" : getAutores(), "categorias" : getCategorias(), "tags" : getTipos(), "dificuldade": getDificuldades()})



def check_if_in_list_ahead(item_list):
    tmp_list = []

    for i in range(0, len(item_list)):
        tmp_list.append(item_list[i].split(",")[0])

    for i in range(0, len(tmp_list)):

        if tmp_list[i] in tmp_list[i + 1:]:
            return True

    return False


def add_receita(request):
    autores = list()
    categorias = list()
    tipos = list()
    dificuldades = list()

    endpoint = "http://localhost:7200"
    repo_name = "receitas"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)



    query = 'PREFIX aut:<http://receita/autores/pred/nome>'\
            'SELECT ?nome{'\
            '?id aut: ?nome'\
            '}'
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    temp = res["results"]["bindings"]
    for item in temp:
        autores.append(item["nome"]["value"])
    #print(autores)

    query = 'PREFIX cat:<http://receita/categorias/pred/nome>' \
            'SELECT ?cat{' \
            '?id cat: ?cat' \
            '}'
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    temp = res["results"]["bindings"]
    for item in temp:
        categorias.append(item["cat"]["value"])
    print(categorias)

    query = 'PREFIX tip:<http://receita/tipos/pred/nome>' \
            'SELECT ?tip{' \
            '?id tip: ?tip' \
            '}'
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    temp = res["results"]["bindings"]
    for item in temp:
        tipos.append(item["tip"]["value"])
    print(tipos)

    query = 'PREFIX dif:<http://receita/dificuldades/pred/nome>' \
            'SELECT ?dif{' \
            '?id dif: ?dif' \
            '}'
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    temp = res["results"]["bindings"]
    for item in temp:
        dificuldades.append(item["dif"]["value"])
    print(dificuldades)

    return render(request, 'add.html',{"autores":autores, "categorias":categorias, "tipos":tipos, "dificuldades":dificuldades})


@csrf_exempt
def edit_recipe(request):

    error = False
    endpoint = "http://localhost:7200"
    repo_name = "receitas"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    #Delete ingredientes, passos e autores
    query = 'PREFIX predRec:<http://receita/pred/>' \
            'PREFIX ing:<http://receita/ingrediente/pred/>' \
            'Delete{ ?id_r predRec:passo ?o.' \
                    '?i ing:nome ?o2.'\
                    '?i ing:quantidade ?o3.'\
                    '?i ing:unidade ?o4. '\
                    '?id_r predRec:autor ?id_a.'\
                    '?id_r predRec:ingrediente ?i.'\
            '} where{'\
                    f'?id_r predRec:nome "{request.POST.get("receitas")}".'\
                    '?id_r predRec:ingrediente ?i.'\
                    '?id_r predRec:passo ?o. '\
                    '?id_r predRec:autor ?id_a.'\
                    '?i ing:nome ?o2. '\
                    '?i ing:quantidade ?o3.'\
                    'OPTIONAL{?i ing:unidade ?o4.}'\
            '}'
    payload_query = {"update": query}
    res = accessor.sparql_update(body=payload_query, repo_name=repo_name)


    query = 'PREFIX predRec:<http://receita/pred/>'\
            'Select ?id where {' \
            f'?id predRec:nome "{request.POST.get("receitas")}".' \
            '}'

    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res= json.loads(res)

    newRecId = (res["results"]["bindings"][0]["id"]["value"]).split('/')[-1].strip(">")

    autores = request.POST.get("aut")
    autores = autores.split(',')

    print(autores)

    autIds = []

    if len(autores) > 1 and type(autores) is not str:
        for aut in autores:
            query = 'PREFIX aut:<http://receita/autores/pred/nome>' \
                    'ask{' \
                    f'?id aut: "{aut}"' \
                    '}'
            payload_query = {"query": query}
            res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
            res = json.loads(res)
            if not res["boolean"]:
                query = 'PREFIX aut:<http://receita/autores/pred/nome>' \
                        'select (count(?id) as ?maxId)' \
                        'where{' \
                        '?id aut: ?name' \
                        '}'
                payload_query = {"query": query}
                res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
                res = json.loads(res)
                AutId = res["results"]["bindings"]
                temp = AutId[0]["maxId"]["value"].split("/")
                temp = str(temp[-1]).strip(">")
                AutId = int(temp) + 1
                autIds.append(AutId)

                query = 'PREFIX aut:<http://receita/autores/pred/nome>' \
                        'PREFIX autID:<http://receita/autores/>' \
                        'insert data{' \
                        f'autID:{AutId} ' + 'aut: ' + f'"{aut}"' \
                                                      '}'
                payload_query = {"update": query}
                res = accessor.sparql_update(body=payload_query, repo_name=repo_name)
            else:
                query = 'PREFIX aut:<http://receita/autores/pred/nome>' \
                        'select ?id ' \
                        'where{' \
                        '?id aut: ' + f'"{aut}"' \
                                      '}'
                payload_query = {"query": query}
                res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
                res = json.loads(res)
                AutId = res["results"]["bindings"]
                temp = AutId[0]["id"]["value"].split("/")
                temp = str(temp[-1]).strip(">")
                AutId = int(temp)
                autIds.append(AutId)
    else:
        autores = autores[0]
        query = 'PREFIX aut:<http://receita/autores/pred/nome>' \
                'ask{' \
                f'?id aut: "{autores}"' \
                '}'
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
        res = json.loads(res)
        if not res["boolean"]:
            query = 'PREFIX aut:<http://receita/autores/pred/nome>' \
                    'select (count(?id) as ?maxId)' \
                    'where{' \
                    '?id aut: ?name' \
                    '}'
            payload_query = {"query": query}
            res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
            res = json.loads(res)
            AutId = res["results"]["bindings"]
            temp = AutId[0]["maxId"]["value"].split("/")
            temp = str(temp[-1]).strip(">")
            AutId = int(temp) + 1
            autIds.append(AutId)

            query = 'PREFIX aut:<http://receita/autores/pred/nome> ' \
                    'PREFIX autId:<http://receita/autores/> ' \
                    'insert data{' \
                    f'autId:{AutId} ' + 'aut: ' + f'"{autores}"' \
                                                  '}'
            payload_query = {"update": query}
            res = accessor.sparql_update(body=payload_query, repo_name=repo_name)
            print(query)
            print("morreu", res)
        else:
            query = 'PREFIX aut:<http://receita/autores/pred/nome>' \
                    'select ?id ' \
                    'where{' \
                    '?id aut: ' + f'"{autores}"' \
                                  '}'
            payload_query = {"query": query}
            res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
            res = json.loads(res)
            AutId = res["results"]["bindings"]
            temp = AutId[0]["id"]["value"].split("/")
            temp = str(temp[-1]).strip(">")
            AutId = int(temp)
            autIds.append(AutId)


    ingredientes = request.POST.get("ingredientes")
    ingredientes = ingredientes.split("\r\n")
    if '' in ingredientes:
        ingredientes.remove('')
    ingIds = []




    if len(ingredientes) > 1 and type(ingredientes) is not str:
        query = 'PREFIX ing:<http://receita/ingrediente/pred/nome>' \
                'select ?id ' \
                'where{' \
                '?id ing: ?name' \
                '}'
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
        res = json.loads(res)
        IngId = res["results"]["bindings"]
        temp = IngId[-1]["id"]["value"].split("/")
        temp = str(temp[-1]).strip(">")
        IngId = int(temp) + 1

        for ingred in ingredientes:
            try:
                ing, quant, uni = ingred.split(",")
            except ValueError:
                ing, quant = ingred.split(",")
                uni = None
                pass


            ingIds.append(IngId)

            query = 'PREFIX ing:<http://receita/ingrediente/pred/nome>' \
                    'PREFIX ingId:<http://receita/ingrediente/>' \
                    'insert data{' \
                    f'ingId:{IngId} ' + 'ing: ' + f'"{ing}"' \
                                                  '}'
            payload_query = {"update": query}
            res = accessor.sparql_update(body=payload_query, repo_name=repo_name)


            query = 'PREFIX ing:<http://receita/ingrediente/pred/quantidade>' \
                    'PREFIX ingId:<http://receita/ingrediente/>' \
                    'insert data {' \
                    f' ingId:{IngId} ' + 'ing: ' + f'"{quant}"' \
                                                   '}'
            payload_query = {"update": query}
            res = accessor.sparql_update(body=payload_query, repo_name=repo_name)

            if uni != None:
                query = 'PREFIX ing:<http://receita/ingrediente/pred/unidade>' \
                        'PREFIX ingId:<http://receita/ingrediente/>' \
                        'insert data{' \
                        f'ingId:{IngId} ' + 'ing: ' + f'"{uni}"' \
                                                      '}'
                payload_query = {"update": query}
                res = accessor.sparql_update(body=payload_query, repo_name=repo_name)
            IngId = IngId + 1
            print(query)
    else:
        query = 'PREFIX ing:<http://receita/ingrediente/pred/nome>' \
                'select ?id ' \
                'where{' \
                '?id ing: ?name' \
                '}'
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
        res = json.loads(res)
        IngId = res["results"]["bindings"]
        temp = IngId[-1]["id"]["value"].split("/")
        temp = str(temp[-1]).strip(">")
        IngId = int(temp) + 1


        ingIds.append(IngId)

        ingredientes= ingredientes[0].split(",")

        query = 'PREFIX ing:<http://receita/ingrediente/pred/nome>' \
                'PREFIX ingId:<http://receita/ingrediente/>' \
                'insert data{' \
                f'ingId:{IngId} ' + 'ing: ' + f'"{ingredientes[0]}"' \
                                              '}'
        payload_query = {"update": query}
        res = accessor.sparql_update(body=payload_query, repo_name=repo_name)

        query = 'PREFIX ing:<http://receita/ingrediente/pred/quantidade>' \
                'PREFIX ingId:<http://receita/ingrediente/>' \
                'insert data {' \
                f' ingId:{IngId} ' + 'ing: ' + f'"{ingredientes[1]}"' \
                                               '}'
        payload_query = {"update": query}
        res = accessor.sparql_update(body=payload_query, repo_name=repo_name)

        if len(ingredientes) == 3:
            query = 'PREFIX ing:<http://receita/ingrediente/pred/unidade>' \
                    'PREFIX ingId:<http://receita/ingrediente/>' \
                    'insert data{' \
                    f'ingId:{IngId} ' + 'ing: ' + f'"{ingredientes[2]}"' \
                                                  '}'
            payload_query = {"update": query}
            res = accessor.sparql_update(body=payload_query, repo_name=repo_name)


    passos = request.POST.get("passos")
    passos = passos.split("\r\n")
    if '' in passos:
        passos.remove('')
    # PASSOS
    if len(passos) > 1 and type(passos) is not str:
        for passo in passos:
            query = 'PREFIX pass:<http://receita/pred/passo>' \
                    'PREFIX recID:<http://receita/id/>' \
                    'insert data{' \
                    f'recID:{newRecId} ' + 'pass: ' + f'"{passo}"' \
                                                      '}'
            payload_query = {"update": query}
            res = accessor.sparql_update(body=payload_query, repo_name=repo_name)
            print(query)

    else:
        query = 'PREFIX pass:<http://receita/pred/passo>' \
                'PREFIX recID:<http://receita/id/>' \
                'insert data{' \
                f'recID:{newRecId} ' + 'pass: ' + f'"{passos[0]}"' \
                                                '}'
        payload_query = {"update": query}
        res = accessor.sparql_update(body=payload_query, repo_name=repo_name)

    for id in ingIds:
        query = 'PREFIX predRec:<http://receita/pred/ingrediente>' \
                'PREFIX ingID:<http://receita/ingrediente/>' \
                'PREFIX recID:<http://receita/id/>' \
                'insert data' \
                '{' \
                f'recID:{newRecId} ' + 'predRec: ' + f'ingID:{id}' \
                                                     '}'
        print(query)
        payload_query = {"update": query}
        res = accessor.sparql_update(body=payload_query, repo_name=repo_name)

    for id in autIds:
        query = 'PREFIX predRec:<http://receita/pred/autor>' \
                'PREFIX recID:<http://receita/id/>' \
                'PREFIX autID:<http://receita/autores/>' \
                'insert data' \
                '{' \
                f'recID:{newRecId} ' + 'predRec: ' + f'autID:{id}' \
                                                     '}'
        print(query)
        payload_query = {"update": query}
        res = accessor.sparql_update(body=payload_query, repo_name=repo_name)



    return render(request, "edit.html",{"edit_occurs" : True, "error" : error, "receitas": getNomesReceitas() })


@csrf_exempt
def edit_receita(request):

    if request.method == 'POST':
        if request.is_ajax():
            rec = request.POST.get("selected_recipe")

            print(rec)
            endpoint = "http://localhost:7200"
            repo_name = "receitas"
            client = ApiClient(endpoint=endpoint)
            accessor = GraphDBApi(client)
            receitas_info = {}

            receitas_info["receita"] = []
            receitas_info["receita"].append(rec)

            query = 'PREFIX predRec:<http://receita/pred/>' \
                    'PREFIX dif:<http://receita/dificuldades/pred/nome>' \
                    'Select ?imagem ?data ?dificuldade where{' \
                    ' ?r predRec:nome "' + rec + '".' \
                     ' ?r predRec:imagem ?imagem. ' \
                     ' ?r predRec:data ?data.' \
                     ' ?r predRec:dificuldade ?d_id.' \
                     ' ?d_id dif: ?dificuldade.' \
                     '}'
            payload_query = {"query": query}
            res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
            res = json.loads(res)
            print(res)
            receitas_info["receita"].append(res["results"]["bindings"][0]["imagem"]["value"])
            receitas_info["receita"].append(res["results"]["bindings"][0]["data"]["value"])
            receitas_info["receita"].append(res["results"]["bindings"][0]["dificuldade"]["value"])

            query = 'PREFIX predRec:<http://receita/pred/>' \
                    'PREFIX aut:<http://receita/autores/pred/nome>' \
                    'Select ?autor where{' \
                    '?r predRec:nome "' + rec + '".' \
                                                '?r predRec:autor ?id_a.' \
                                                '?id_a aut: ?autor.' \
                                                '}'
            payload_query = {"query": query}
            res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
            res = json.loads(res)
            autores_rec = ""

            for autor in res["results"]["bindings"]:
                autores_rec += autor["autor"]["value"]
                if autor != res["results"]["bindings"][-1]:
                    autores_rec += ','
            receitas_info["receita"].append(autores_rec)

            query = 'PREFIX predRec:<http://receita/pred/>' \
                    'PREFIX cat:<http://receita/categorias/pred/nome>' \
                    'Select ?categoria where{' \
                    '?r predRec:nome "' + rec + '".' \
                    '?r predRec:categoria ?id_c.' \
                    '?id_c cat: ?categoria.' \
                    '}'

            payload_query = {"query": query}
            res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
            res = json.loads(res)

            categorias_rec = ""

            for categoria in res["results"]["bindings"]:
                categorias_rec += categoria["categoria"]["value"]
                if categoria != res["results"]["bindings"][-1]:
                    categorias_rec += ','

            receitas_info["receita"].append(categorias_rec)

            query = 'PREFIX predRec:<http://receita/pred/>' \
                    'PREFIX tip:<http://receita/tipos/pred/nome>' \
                    'Select ?tipo where{' \
                    '?r predRec:nome "' + rec + '".' \
                    '?r predRec:tipo ?id_t.' \
                    '?id_t tip: ?tipo.' \
                    '}'

            payload_query = {"query": query}
            res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
            res = json.loads(res)
            tipo_rec = ""

            for tipo in res["results"]["bindings"]:
                tipo_rec += tipo["tipo"]["value"]
                if tipo != res["results"]["bindings"][-1]:
                    tipo_rec += ","

            receitas_info["receita"].append(tipo_rec)

            query = 'PREFIX predRec:<http://receita/pred/>' \
                    'Select ?passo where{' \
                    '?r predRec:nome "' + rec + '".' \
                    '?r predRec:passo ?passo.' \
                    '}'

            payload_query = {"query": query}
            res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
            res = json.loads(res)
            passo_rec = ""

            for passo in res["results"]["bindings"]:
                passo_rec += passo["passo"]["value"]
                if passo != res["results"]["bindings"][-1]:
                    passo_rec +=  '\n'

            receitas_info["receita"].append(passo_rec)

            query = 'PREFIX predRec:<http://receita/pred/>' \
                    'PREFIX ing:<http://receita/ingrediente/pred/>' \
                    'Select ?nome ?quantidade ?unidade where{' \
                    '?r predRec:nome "' + rec + '".' \
                    '?r predRec:ingrediente ?id_i.' \
                    '?id_i ing:nome ?nome.' \
                    '?id_i ing:quantidade ?quantidade.' \
                    'OPTIONAL{?id_i ing:unidade ?unidade.}' \
                    '}'

            payload_query = {"query": query}
            res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
            res = json.loads(res)
            ing_rec = ""

            for ing in res["results"]["bindings"]:
                ing_rec += ing["nome"]["value"] + ","
                ing_rec += ing["quantidade"]["value"]

                if "unidade" in ing.keys():
                    ing_rec += ',' + ing["unidade"]["value"]
                if ing != res["results"]["bindings"][-1]:
                    ing_rec += "\n"

            receitas_info["receita"].append(ing_rec)

            return JsonResponse({"receita":receitas_info["receita"]})

    return render(request, 'edit.html', {"receitas": getNomesReceitas()})


def add_recipe(request):


    catIds = list()
    tipoIds = list()
    ingIds = list()
    autIds = list()
    print(request.POST)
    dados = request.POST




    nome = dados["name"]
    categ = dados["cat"].split(",")
    data = dados["data"]
    tipos = dados["tipo"].split(",")
    autores = dados["aut"].split(",")
    dificuldade = dados["dificuldade"]
    ingredientes = dados["ingredientes"].split("\r\n")
    passos = dados["passos"].split("\r\n")
    imagem = dados["imagem"]

    endpoint = "http://localhost:7200"
    repo_name = "receitas"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    query = 'PREFIX predRec:<http://receita/pred/>' \
            'select (max(?id) as ?maxId)' \
            'where{' \
            '?id predRec:nome ?name' \
            '}'
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    currRecId = res["results"]["bindings"]
    temp = currRecId[0]["maxId"]["value"].split("/")
    temp = str(temp[-1]).strip(">")
    newRecId = int(temp) + 1


    #CATEGORIA
    if len(categ) > 1 and type(categ) is not str:
        for cat in categ:
            query = 'PREFIX cat:<http://receita/categorias/pred/nome>' \
                    'ask{' \
                     f'?cat cat: "{cat}"' \
                    '}'
            payload_query = {"query": query}
            res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
            res = json.loads(res)
            if not res["boolean"]:
                query = 'PREFIX cat:<http://receita/categorias/pred/nome>' \
                        'select (max(?id) as ?maxId)' \
                        'where{' \
                        '?id cat: ?name' \
                        '}'
                payload_query = {"query": query}
                res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
                res = json.loads(res)
                CatId = res["results"]["bindings"]
                temp = CatId[0]["maxId"]["value"].split("/")
                temp = str(temp[-1]).strip(">")
                CatId = int(temp) + 1
                catIds.append(CatId)

                query = 'PREFIX cat:<http://receita/categorias/pred/nome>' \
                        'PREFIX catID:<http://receita/categorias/>' \
                        'insert data{' \
                         f'catID:{CatId} ' + 'cat: ' + f'"{cat}"' \
                        '}'
                payload_query = {"update": query}
                res = accessor.sparql_update(body=payload_query, repo_name=repo_name)
            else:
                query = 'PREFIX cat:<http://receita/categorias/pred/nome>' \
                        'select ?id ' \
                        'where{' \
                        '?id cat: ' + f'"{cat}"' \
                        '}'
                payload_query = {"query": query}
                res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
                res = json.loads(res)
                CatId = res["results"]["bindings"]
                temp = CatId[0]["id"]["value"].split("/")
                temp = str(temp[-1]).strip(">")
                CatId = int(temp)
                catIds.append(CatId)
    else:
        categ = categ[0]
        query = 'PREFIX cat:<http://receita/categorias/pred/nome>' \
                'ask{' \
                f'?cat cat: "{categ}"' \
                '}'
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
        res = json.loads(res)
        if not res["boolean"]:
            query = 'PREFIX cat:<http://receita/categorias/pred/nome>' \
                    'select (max(?id) as ?maxId)' \
                    'where{' \
                    '?id cat: ?name' \
                    '}'
            payload_query = {"query": query}
            res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
            res = json.loads(res)
            CatId = res["results"]["bindings"]
            temp = CatId[0]["maxId"]["value"].split("/")
            temp = str(temp[-1]).strip(">")
            CatId = int(temp) + 1
            catIds.append(CatId)

            query = 'PREFIX cat:<http://receita/categorias/pred/nome> ' \
                    'PREFIX catID:<http://receita/categorias/> ' \
                    'insert data{ ' \
                    f'catID:{CatId} ' + 'cat: ' + f'"{categ}"' \
                                            '}'
            payload_query = {"update": query}
            res = accessor.sparql_update(body=payload_query, repo_name=repo_name)
            print(query)
            print("CatId",CatId)
            print("morreu",res)
        else:
            query = 'PREFIX cat:<http://receita/categorias/pred/nome>' \
                    'select ?id ' \
                    'where{' \
                    '?id cat: ' + f'"{categ}"' \
                    '}'
            payload_query = {"query": query}
            res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
            res = json.loads(res)
            CatId = res["results"]["bindings"]
            temp = CatId[0]["id"]["value"].split("/")
            temp = str(temp[-1]).strip(">")
            CatId = int(temp)
            catIds.append(CatId)

    #TIPO
    if len(tipos) > 1 and type(tipos) is not str:
        for tipo in tipos:
            query = 'PREFIX tip:<http://receita/tipos/pred/nome>' \
                    'ask{' \
                    f'?tip tip: "{tipo}"' \
                    '}'
            payload_query = {"query": query}
            res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
            res = json.loads(res)
            if not res["boolean"]:
                query = 'PREFIX tip:<http://receita/tipos/pred/nome>' \
                        'select (max(?id) as ?maxId)' \
                        'where{' \
                        '?id tip: ?name' \
                        '}'
                payload_query = {"query": query}
                res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
                res = json.loads(res)
                TipoId = res["results"]["bindings"]
                temp = TipoId[0]["maxId"]["value"].split("/")
                temp = str(temp[-1]).strip(">")
                TipoId = int(temp) + 1
                tipoIds.append(TipoId)

                query = 'PREFIX tip:<http://receita/tipos/pred/nome>' \
                        'PREFIX tipId:<http://receita/tipos/>' \
                        'insert data{' \
                        f'tipId:{TipoId} ' + 'tip: ' + f'"{tipo}"' \
                        '}'
                payload_query = {"update": query}
                res = accessor.sparql_update(body=payload_query, repo_name=repo_name)
                print(query)
                print("morreu:",res)
            else:
                query = 'PREFIX tip:<http://receita/tipos/pred/nome>' \
                        'select ?id ' \
                        'where{' \
                        '?id tip: ' + f'"{tipo}"' \
                        '}'
                payload_query = {"query": query}
                res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
                res = json.loads(res)
                TipoId = res["results"]["bindings"]
                temp = TipoId[0]["id"]["value"].split("/")
                temp = str(temp[-1]).strip(">")
                TipoId = int(temp)
                tipoIds.append(TipoId)
    else:
        query = 'PREFIX tip:<http://receita/tipos/pred/nome>' \
                'ask{' \
                f'?tip tip: "{tipos}"' \
                '}'
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
        res = json.loads(res)
        if not res["boolean"]:
            query = 'PREFIX tip:<http://receita/tipos/pred/nome>' \
                    'select (max(?id) as ?maxId) ' \
                    'where{' \
                    '?id tip: ?name' \
                    '}'
            payload_query = {"query": query}
            res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
            res = json.loads(res)
            TipoId = res["results"]["bindings"]
            temp = TipoId[0]["maxId"]["value"].split("/")
            temp = str(temp[-1]).strip(">")
            TipoId = int(temp) + 1
            tipoIds.append(TipoId)

            tipos = tipos[0]

            query = 'PREFIX tip:<http://receita/tipos/pred/nome>' \
                    'PREFIX tipID:<http://receita/tipos/>' \
                    'insert data{' \
                    f'tipID:{TipoId} ' + 'tip: ' + f'"{tipos}"' \
                                             '}'
            payload_query = {"update": query}
            res = accessor.sparql_update(body=payload_query, repo_name=repo_name)
        else:
            query = 'PREFIX tip:<http://receita/tipos/pred/nome>' \
                    'select ?id ' \
                    'where{' \
                    '?id tip: ' + f'"{tipos}"' \
                                  '}'
            payload_query = {"query": query}
            res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
            res = json.loads(res)
            TipoId = res["results"]["bindings"]
            temp = TipoId[0]["id"]["value"].split("/")
            temp = str(temp[-1]).strip(">")
            TipoId = int(temp)
            tipoIds.append(TipoId)


    #AUTORES
    if len(autores) > 1 and type(autores) is not str:
        for aut in autores:
            query = 'PREFIX aut:<http://receita/autores/pred/nome>' \
                    'ask{' \
                    f'?id aut: "{aut}"' \
                    '}'
            payload_query = {"query": query}
            res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
            res = json.loads(res)
            if not res["boolean"]:
                query = 'PREFIX aut:<http://receita/autores/pred/nome>' \
                        'select (max(?id) as ?maxId)' \
                        'where{' \
                        '?id aut: ?name' \
                        '}'
                payload_query = {"query": query}
                res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
                res = json.loads(res)
                AutId = res["results"]["bindings"]
                temp = AutId[0]["maxId"]["value"].split("/")
                temp = str(temp[-1]).strip(">")
                AutId = int(temp) + 1
                autIds.append(AutId)

                query = 'PREFIX aut:<http://receita/autores/pred/nome>' \
                        'PREFIX autID:<http://receita/autores/>' \
                        'insert data{' \
                        f'autID:{AutId} ' + 'aut: ' + f'"{aut}"' \
                                                 '}'
                payload_query = {"update": query}
                res = accessor.sparql_update(body=payload_query, repo_name=repo_name)
            else:
                query = 'PREFIX aut:<http://receita/autores/pred/nome>' \
                        'select ?id ' \
                        'where{' \
                        '?id aut: ' + f'"{aut}"' \
                                      '}'
                payload_query = {"query": query}
                res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
                res = json.loads(res)
                AutId = res["results"]["bindings"]
                temp = AutId[0]["id"]["value"].split("/")
                temp = str(temp[-1]).strip(">")
                AutId = int(temp)
                autIds.append(AutId)
    else:
        autores = autores[0]
        query = 'PREFIX aut:<http://receita/autores/pred/nome>' \
                'ask{' \
                f'?id aut: "{autores}"' \
                '}'
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
        res = json.loads(res)
        if not res["boolean"]:
            query = 'PREFIX aut:<http://receita/autores/pred/nome>' \
                    'select (max(?id) as ?maxId)' \
                    'where{' \
                    '?id aut: ?name' \
                    '}'
            payload_query = {"query": query}
            res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
            res = json.loads(res)
            AutId = res["results"]["bindings"]
            temp = AutId[0]["maxId"]["value"].split("/")
            temp = str(temp[-1]).strip(">")
            AutId = int(temp) + 1
            autIds.append(AutId)

            query = 'PREFIX aut:<http://receita/autores/pred/nome> ' \
                    'PREFIX autId:<http://receita/autores/> ' \
                    'insert data{' \
                    f'autId:{AutId} ' + 'aut: ' + f'"{autores}"' \
                                             '}'
            payload_query = {"update": query}
            res = accessor.sparql_update(body=payload_query, repo_name=repo_name)
            print(query)
            print("morreu",res)
        else:
            query = 'PREFIX aut:<http://receita/autores/pred/nome>' \
                    'select ?id ' \
                    'where{' \
                    '?id aut: ' + f'"{autores}"' \
                                  '}'
            payload_query = {"query": query}
            res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
            res = json.loads(res)
            AutId = res["results"]["bindings"]
            temp = AutId[0]["id"]["value"].split("/")
            temp = str(temp[-1]).strip(">")
            AutId = int(temp)
            autIds.append(AutId)


    print(autIds)


    # DIFICULDADE
    query = 'PREFIX dif:<http://receita/dificuldades/pred/nome>' \
            'ask{' \
            f'?id dif: "{dificuldade}"' \
            '}'
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    if not res["boolean"]:
        query = 'PREFIX dif:<http://receita/dificuldades/pred/nome>' \
                'select (max(?id) as ?maxId)' \
                'where{' \
                '?id dif: ?name' \
                '}'
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
        res = json.loads(res)
        DifId = res["results"]["bindings"]
        temp = DifId[0]["maxId"]["value"].split("/")
        temp = str(temp[-1]).strip(">")
        DifId = int(temp) + 1

        query = 'PREFIX dif:<http://receita/dificuldades/pred/nome>' \
                'PREFIX difID:<http://receita/dificuldades/>' \
                'insert data{' \
                f'difID:{DifId} ' + 'dif: ' + f'"{dificuldade}"' \
                                        '}'
        payload_query = {"update": query}
        res = accessor.sparql_update(body=payload_query, repo_name=repo_name)

    else:
        query = 'PREFIX dif:<http://receita/dificuldades/pred/nome>' \
                'select ?id ' \
                'where{' \
                '?id dif: ' + f'"{dificuldade}"' \
                              '}'
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
        res = json.loads(res)
        print(res)
        DifId = res["results"]["bindings"]
        print(DifId)
        temp = DifId[0]["id"]["value"].split("/")
        temp = str(temp[-1]).strip(">")
        DifId = int(temp)


    # INGREDIENTES
    if len(ingredientes) > 1 and type(ingredientes) is not str:
        for ingred in ingredientes:
            try:
                ing, quant, uni = ingred.split(",")
            except ValueError:
                ing, quant = ingred.split(",")
                uni = None
                pass

            query = 'PREFIX ing:<http://receita/ingrediente/pred/nome>' \
                    'select (max(?id) as ?maxId)' \
                    'where{' \
                    '?id ing: ?name' \
                    '}'
            payload_query = {"query": query}
            res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
            res = json.loads(res)
            IngId = res["results"]["bindings"]
            temp = IngId[0]["maxId"]["value"].split("/")
            temp = str(temp[-1]).strip(">")
            IngId = int(temp) + 1
            ingIds.append(IngId)

            query = 'PREFIX ing:<http://receita/ingrediente/pred/nome>' \
                    'PREFIX ingId:<http://receita/ingrediente/>' \
                    'insert data{' \
                    f'ingId:{IngId} ' + 'ing: ' + f'"{ing}"' \
                                            '}'
            payload_query = {"update": query}
            res = accessor.sparql_update(body=payload_query, repo_name=repo_name)
            print(query)
            print("morreu",res)

            query = 'PREFIX ing:<http://receita/ingrediente/pred/quantidade>' \
                    'PREFIX ingId:<http://receita/ingrediente/>' \
                    'insert data {' \
                    f' ingId:{IngId} ' + 'ing: ' + f'"{quant}"' \
                    '}'
            payload_query = {"update": query}
            res = accessor.sparql_update(body=payload_query, repo_name=repo_name)

            if uni != None:
                query = 'PREFIX ing:<http://receita/ingrediente/pred/unidade>' \
                        'PREFIX ingId:<http://receita/ingrediente/>' \
                        'insert data{' \
                        f'ingId:{IngId} ' + 'ing: ' + f'"{uni}"' \
                        '}'
                payload_query = {"update": query}
                res = accessor.sparql_update(body=payload_query, repo_name=repo_name)
            IngId = IngId + 1
            print(query)


    # PASSOS
    if len(passos) > 1 and type(passos) is not str:
        for passo in passos:
            query = 'PREFIX pass:<http://receita/pred/passo>' \
                    'PREFIX recID:<http://receita/id/>' \
                    'insert data{' \
                    f'recID:{newRecId} ' + 'pass: ' + f'"{passo}"' \
                                            '}'
            payload_query = {"update": query}
            res = accessor.sparql_update(body=payload_query, repo_name=repo_name)
            print(query)

    else:
        query = 'PREFIX pass:<http://receita/pred/passo>' \
                'PREFIX recID:<http://receita/id/>' \
                'insert data{' \
                f'recID:{newRecId}' + 'pass:' + f'"{passos}"' \
                                            '}'
        payload_query = {"update": query}
        res = accessor.sparql_update(body=payload_query, repo_name=repo_name)

    # IMAGEM
    query = 'PREFIX im:<http://receita/pred/imagem>' \
            'PREFIX recID:<http://receita/id/>' \
            'insert data{' \
            f'recID:{newRecId} ' + 'im: ' + f'"{imagem}"' \
                                        '}'
    payload_query = {"update": query}
    res = accessor.sparql_update(body=payload_query, repo_name=repo_name)
    print(query)

    #DATA
    query = 'PREFIX dat:<http://receita/pred/data>' \
            'PREFIX recID:<http://receita/id/>' \
            'insert data{' \
            f'recID:{newRecId} ' + 'dat: ' + f'"{data}"' \
                                        '}'
    payload_query = {"update": query}
    res = accessor.sparql_update(body=payload_query, repo_name=repo_name)
    print(query)

    query = 'PREFIX predRec:<http://receita/pred/>' \
            'PREFIX recID:<http://receita/id/>' \
            'PREFIX dif:<http://receita/dificuldades/>'\
            'insert data' \
            '{' \
            f'recID:{newRecId} ' + 'predRec:dificuldade ' + f'dif:{DifId}' \
                                                     '}'
    payload_query = {"update": query}
    res = accessor.sparql_update(body=payload_query, repo_name=repo_name)

    query = 'PREFIX predRec:<http://receita/pred/>' \
            'PREFIX recID:<http://receita/id/>' \
            'insert data' \
            '{' \
             f'recID:{newRecId} ' + 'predRec:nome ' + f'"{nome}"'  \
            '}'
    payload_query = {"update": query}
    res = accessor.sparql_update(body=payload_query, repo_name=repo_name)
    print(query)
    #print("morreu:",res)


    #FINAL
    for id in catIds:
        query = 'PREFIX predRec:<http://receita/pred/categoria>' \
                'PREFIX catID:<http://receita/categorias/>'\
                'PREFIX recID:<http://receita/id/>' \
                'insert data' \
                '{' \
                f'recID:{newRecId} ' + 'predRec: ' + f'catID:{id}'  \
                '}'
        print(query)
        payload_query = {"update": query}
        res = accessor.sparql_update(body=payload_query, repo_name=repo_name)

    for id in tipoIds:
        query = 'PREFIX predRec:<http://receita/pred/tipo>' \
                'PREFIX tipID:<http://receita/tipos/>'\
                'PREFIX recID:<http://receita/id/>' \
                'insert data' \
                '{' \
                f'recID:{newRecId} ' + 'predRec: ' + f'tipID:{id}' \
                '}'
        print(query)
        payload_query = {"update": query}
        res = accessor.sparql_update(body=payload_query, repo_name=repo_name)

    for id in ingIds:
        query = 'PREFIX predRec:<http://receita/pred/ingrediente>' \
                'PREFIX ingID:<http://receita/ingrediente/>' \
                'PREFIX recID:<http://receita/id/>' \
                'insert data' \
                '{' \
                f'recID:{newRecId} ' + 'predRec: ' + f'ingID:{id}'\
                '}'
        print(query)
        payload_query = {"update": query}
        res = accessor.sparql_update(body=payload_query, repo_name=repo_name)

    for id in autIds:
        query = 'PREFIX predRec:<http://receita/pred/autor>' \
                'PREFIX recID:<http://receita/id/>' \
                'PREFIX autID:<http://receita/autores/>' \
                'insert data' \
                '{' \
                f'recID:{newRecId} ' + 'predRec: ' + f'autID:{id}' \
                '}'
        print(query)
        payload_query = {"update": query}
        res = accessor.sparql_update(body=payload_query, repo_name=repo_name)


    return render(request,"add.html")


def delete(request):
    receitas = getNomesReceitas()
    return render(request,"del.html", {"receitas":receitas,"delete_occurs" : False})

def del_recipe(request):
    try:
        delete_occurs=True
        error = False
        receita = request.POST.get("receitas")
        endpoint = "http://localhost:7200"
        repo_name = "receitas"
        client = ApiClient(endpoint=endpoint)
        accessor = GraphDBApi(client)


        query = 'PREFIX predRec:<http://receita/pred/>' \
                'PREFIX ing:<http://receita/ingrediente/pred/>'\
                ' Delete {?id_r ?p ?o. ?id_r ?p2 ?o5. ?o ing:nome ?o2. ?o ing:quantidade ?o3.  ?o ing:unidade ?o4.  } where{' \
                '?id_r predRec:nome "' + str(receita) +'".' \
                '?id_r ?p ?o.'\
                '?id_r ?p2 ?o5.'\
                '?o ing:nome ?o2.' \
                '?o ing:quantidade ?o3.' \
                'OPTIONAL{?o ing:unidade ?o4.}'\
                '}'
        payload_query = {"update": query}
        res = accessor.sparql_update(body=payload_query, repo_name=repo_name)

    except:
        error = True

    receitas = getNomesReceitas()

    return render(request, "del.html", {"receitas":receitas,"delete_occurs":delete_occurs, "error":error})

def show_recipe(request, recipe):
    endpoint = "http://localhost:7200"
    repo_name = "receitas"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)

    query=' PREFIX predRec:<http://receita/pred/> Select * where{ ?s ?p "'+ recipe +'". ?s predRec:data ?data. ?s predRec:imagem ?imagem. ?s predRec:passo ?passos.}'
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)

    print(res)
    nome = []
    nome.append(recipe)
    nome.append(res["results"]["bindings"][0]["s"]["value"])
    data = res["results"]["bindings"][0]["data"]["value"]
    imagem=res["results"]["bindings"][0]["imagem"]["value"]
    passos = []
    for p in res["results"]["bindings"]:
        passos.append(p["passos"]["value"])



    ingredientes = []

    query = ' PREFIX predRec:<http://receita/pred/> PREFIX ing:<http://receita/ingrediente/pred/> Select * where{ ?s ?p "' + recipe + '". ?s predRec:ingrediente ?id_i. ?id_i ing:nome ?nome. ?id_i ing:quantidade ?quantidade. OPTIONAL{?id_i ing:unidade ?unidade.}}'
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)

    if isinstance(res["results"]["bindings"], list):
        for i in res["results"]["bindings"]:
            nome_i = i["nome"]["value"]
            quantidade=i["quantidade"]["value"]
            if "unidade" in i.keys():
                unidade = i["unidade"]["value"]
                tup = nome_i,quantidade, i["id_i"]["value"],unidade
            else:
                tup = nome_i,quantidade,i["id_i"]["value"]

            ingredientes.append(tup)
    else:
        if len(res["results"]["bindings"][0]) == 3:
            tup = res["results"]["bindings"][0]["nome"]["value"],res["results"]["bindings"][0]["quantidade"]["value"], res["results"]["bindings"][0]["id_i"]["value"],res["results"]["bindings"][0]["unidade"]["value"]
        else:
            tup = res["results"]["bindings"][0]["nome"]["value"],res["results"]["bindings"][0]["quantidade"]["value"],res["results"]["bindings"][0]["id_i"]["value"]
        ingredientes.append(tup)

    query = ' PREFIX predRec:<http://receita/pred/> PREFIX aut:<http://receita/autores/pred/nome> Select * where{ ?s ?p "' + recipe + '". ?s predRec:autor ?id_a. ?id_a aut: ?nome. }'
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)

    autores =[]

    if isinstance(res["results"]["bindings"],list):

        for a in res["results"]["bindings"]:

            autor_data = wikidata(a["nome"]["value"])
            print(autor_data)
            if autor_data != None:
                for a1 in autor_data["results"]["bindings"]:
                    tup = a["nome"]["value"], a["id_a"]["value"], a1["item"]["value"], a1["i2"]["value"]
                    autores.append(tup)
            else:
                tup = a["nome"]["value"], a["id_a"]["value"]
                print(tup)
                autores.append(tup)
    else:
        tup = res["results"]["bindings"]["nome"]["value"],res["results"]["bindings"]["id_a"]["value"]
        autores.append(tup)



    tipos=[]

    query = ' PREFIX predRec:<http://receita/pred/> PREFIX tip:<http://receita/tipos/pred/nome> Select * where{ ?s ?p "' + recipe + '". ?s predRec:tipo ?id_t. ?id_t tip: ?nome. }'
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)

    if isinstance(res["results"]["bindings"],list):
        for t in res["results"]["bindings"]:
            tup = t["nome"]["value"], t["id_t"]["value"]
            tipos.append(tup)
    else:
        tipos.append((res["results"]["bindings"]["nome"]["value"],res["results"]["bindings"]["id_t"]["value"] ))

    categorias = []

    query = ' PREFIX predRec:<http://receita/pred/> PREFIX cat:<http://receita/categorias/pred/nome> Select * where{ ?s ?p "' + recipe + '". ?s predRec:categoria ?id_c. ?id_c cat: ?nome. }'
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)

    if isinstance(res["results"]["bindings"],list):
        for c in res["results"]["bindings"]:
            categorias.append((c["nome"]["value"],c["id_c"]["value"]))
    else:
        categorias.append((res["results"]["bindings"]["nome"]["value"],res["results"]["bindings"]["id_c"]["value"]))



    return render(request, "show_rec.xhtml", {"nome":nome, "data":data, "imagem":imagem, "passos":passos, "ingredientes":ingredientes, "categorias":categorias, "tipos":tipos, "autores": autores})


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


    #print("asdasda",res["results"]["bindings"])
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

        print("aqui ",res)
        receitas_info[rec] = []
        receitas_info[rec].append(res["results"]["bindings"][0]["imagem"]["value"])

        query = 'PREFIX predRec:<http://receita/pred/>'\
                'PREFIX aut:<http://receita/autores/pred/nome>'\
                'Select ?autor where{'\
                '?r predRec:nome "'+ str(rec) +'".'\
                '?r predRec:autor ?id_a.'\
                '?id_a aut: ?autor.'\
                '}'

        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
        res = json.loads(res)
        autores_rec=[]



        if isinstance(res["results"]["bindings"], list):
            for auth in res["results"]["bindings"]:
                print(auth)
                autores_rec.append(auth["autor"]["value"])
        else:
            autores_rec.append(res["results"]["bindings"]["autor"]["value"])

        receitas_info[rec].append(autores_rec)

        print(receitas_info)


    return receitas_info


def wikidata(author):
    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setQuery('ask {?s ?p "' + author + '"}')

        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()

        print(result)
        if(result["boolean"]== False):

            return None

        sparql.setQuery('SELECT * WHERE{ ?i wdt:P373 "'+ author + '". ?item ?p ?i. OPTIONAL{?i wdt:P18 ?i2. } FILTER regex(str(?item),"https://en.wikipedia.org/wiki/"). SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }.  }')
        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()

        if result["results"]["bindings"] == []:
            return None
        return result
    except:
        return None
