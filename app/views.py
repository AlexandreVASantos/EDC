from builtins import iter, next

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from lxml import etree
from EDC.settings import BASE_DIR
from BaseXClient import BaseXClient

import xmltodict
import os
import feedparser


def home(request):
    return render(request, "main.html")


def listrecipes(request):
    doc = etree.parse("app/data/receitas.xml")
    search = doc.xpath("//receita")

    information = {}
    autores = []
    tags = []
    categorias = []
    dificuldade = []
    nomesRec = []
    temp = []

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        q = session.query('import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_autores()')
        autores = q.execute()
        q.close()
        autores.split("\n")
        autores = xmltodict.parse(autores)

        q = session.query('import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_tags()')
        tags = q.execute()
        q.close()
        tags = xmltodict.parse(tags)

        q = session.query('import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_categorias()')
        categorias = q.execute()
        q.close()
        categorias = xmltodict.parse(categorias)

        q = session.query(
            'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_dificuldades()')
        dificuldade = q.execute()
        q.close()
        dificuldade = xmltodict.parse(dificuldade)

        q = session.query(
            'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_nomes_receitas()')
        nomesRec = q.execute()
        q.close()
        nomesRec = xmltodict.parse(nomesRec)
        nomesRec = nomesRec["nomes"]["nome"]

        for nome in nomesRec:
            input = f'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_autores_receita("{nome}")'
            q = session.query(input)
            index = xmltodict.parse(q.execute())
            index = index["autores"]["nome_autor"]
            q.close()

            input = f'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_receita("{nome}")'
            q = session.query(input)
            temp = xmltodict.parse(q.execute())
            information[temp["receita"]["nome"]] = []
            information[temp["receita"]["nome"]].append(temp["receita"]["imagem"])
            information[temp["receita"]["nome"]].append(index)
            q.close()

    finally:
        # close session
        if session:
            session.close()

    autores = autores["autores"]["nome_autor"]
    autores = list(set(autores))
    autores.sort()
    autores.insert(0, "--")

    tags = tags["tags"]["tipo"]
    tags = list(set(tags))
    tags.sort()
    tags.insert(0, "--")

    categorias = categorias["categorias"]["categoria"]
    categorias = list(set(categorias))
    categorias.sort()
    categorias.insert(0, "--")

    dificuldade = dificuldade["dificuldades"]["dificuldade"]
    dificuldade = list(set(dificuldade))
    dificuldade.sort()
    dificuldade.insert(0, "--")

    print("autores:", autores)

    return render(request, "list_recipes.html", {"info": information, "autores": autores,
                                                 "tags": tags,
                                                 "categorias": categorias,
                                                 "dificuldade": dificuldade})


def applyFilters(request):
    data = request.GET
    print(data)

    information = {}
    autor = data["authors"]
    dif = data["dificuldade"]
    tag = data["tags"]
    cat = data["categorias"]

    autores = []
    tags = []
    categorias = []
    dificuldade = []
    nomesRec = []
    temp = []
    recIntersect = {}
    recByCat = list()
    recByTag = list()
    recByAut = list()
    recByDif = list()
    recList = list()
    final = list()

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        q = session.query('import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_autores()')
        autores = q.execute()
        q.close()
        autores.split("\n")
        autores = xmltodict.parse(autores)

        q = session.query('import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_tags()')
        tags = q.execute()
        q.close()
        tags = xmltodict.parse(tags)

        q = session.query('import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_categorias()')
        categorias = q.execute()
        q.close()
        categorias = xmltodict.parse(categorias)

        q = session.query(
            'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_dificuldades()')
        dificuldade = q.execute()
        q.close()
        dificuldade = xmltodict.parse(dificuldade)

        q = session.query(
            'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_nomes_receitas()')
        nomesRec = q.execute()
        q.close()
        nomesRec = xmltodict.parse(nomesRec)
        nomesRec = nomesRec["nomes"]["nome"]

        for nome in nomesRec:
            input = f'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_autores_receita("{nome}")'
            q = session.query(input)
            index = xmltodict.parse(q.execute())
            index = index["autores"]["nome_autor"]
            q.close()

        if autor != "--":
            q = session.query(
                f'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_receitas_byAut("{autor}")')
            temp = xmltodict.parse(q.execute())
            if type(temp["receita"]["nome"]) is not str:
                recByAut = temp["receita"]["nome"]
            else:
                recByAut.append(temp["receita"]["nome"])
            q.close()

        if dif != "--":
            q = session.query(
                f'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_receitas_byDif("{dif}")')
            temp = xmltodict.parse(q.execute())
            if type(temp["receita"]["nome"]) is not str:
                recByDif = temp["receita"]["nome"]
            else:
                recByDif.append(temp["receita"]["nome"])
            q.close()

        if tag != "--":
            q = session.query(
                f'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_receitas_byTags("{tag}")')
            temp = xmltodict.parse(q.execute())
            if type(temp["receita"]["nome"]) is not str:
                recByTag = temp["receita"]["nome"]
            else:
                recByTag.append(temp["receita"]["nome"])
            q.close()

        if cat != "--":
            q = session.query(
                f'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_receitas_byCat("{cat}")')
            temp = xmltodict.parse(q.execute())
            if type(temp["receita"]["nome"]) is not str:
                recByCat = temp["receita"]["nome"]
            else:
                recByCat.append(temp["receita"]["nome"])
            q.close()


        if len(recByAut) > 0:
            if len(final) > 0:
                final = set(final).intersection(set(recByAut))
            else:
                final = recByAut

        if len(recByCat) > 0:
            if len(final) > 0:
                final = set(final).intersection(set(recByCat))
            else:
                final = recByCat

        if len(recByTag) > 0:
            if len(final) > 0:
                final = set(final).intersection(set(recByTag))
            else:
                final = recByTag

        if len(recByDif) > 0:
            if len(final) > 0:
                final = set(final).intersection(set(recByAut))
            else:
                final = recByDif


        if type(final) is not str:
            for nome in final:
                input = f'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_autores_receita("{nome}")'
                q = session.query(input)
                index = xmltodict.parse(q.execute())
                index = index["autores"]["nome_autor"]
                q.close()

                input = f'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_receita("{nome}")'
                q = session.query(input)
                temp = xmltodict.parse(q.execute())
                information[temp["receita"]["nome"]] = []
                information[temp["receita"]["nome"]].append(temp["receita"]["imagem"])
                information[temp["receita"]["nome"]].append(index)
                q.close()

        else:
            input = f'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_autores_receita("{final}")'
            q = session.query(input)
            index = xmltodict.parse(q.execute())
            index = index["autores"]["nome_autor"]
            q.close()

            input = f'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_receita("{final}")'
            q = session.query(input)
            temp = xmltodict.parse(q.execute())
            information[temp["receita"]["nome"]] = []
            information[temp["receita"]["nome"]].append(temp["receita"]["imagem"])
            information[temp["receita"]["nome"]].append(index)
            q.close()

    finally:
        # close session
        if session:
            session.close()

    autores = autores["autores"]["nome_autor"]
    autores = list(set(autores))
    autores.sort()
    autores.insert(0, "--")

    tags = tags["tags"]["tipo"]
    tags = list(set(tags))
    tags.sort()
    tags.insert(0, "--")

    categorias = categorias["categorias"]["categoria"]
    categorias = list(set(categorias))
    categorias.sort()
    categorias.insert(0, "--")

    dificuldade = dificuldade["dificuldades"]["dificuldade"]
    dificuldade = list(set(dificuldade))
    dificuldade.sort()
    dificuldade.insert(0, "--")

    return render(request, "list_recipes.html", {"info": information, "autores": autores,
                                                 "tags": tags,
                                                 "categorias": categorias,
                                                 "dificuldade": dificuldade})


def applyFeed(request):
    d = feedparser.parse('https://www.bonappetit.com/feed/latest-recipes/rss')
    info = dict()
    for post in d.entries:
        info[post.title] = []
        info[post.title].append(post.links[0].href)
        info[post.title].append(post.media_thumbnail[0]["url"])

    for key,value in info.items():
        print(value[1])
    return render(request, "feed.html", {"info": info})


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
    if request.method == 'POST':
        edit_occurs = True
        if request.is_ajax():

            session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
            try:
                q = session.query(
                    'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_receita("{}")'.format(
                        request.POST.get("selected_recipe")))
                exec = q.execute()
                q.close()

                dict_recipe = xmltodict.parse(exec)

                q = session.query(
                    'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_autores_receita("{}")'.format(
                        request.POST.get("selected_recipe")))
                exec = q.execute()
                q.close()

                dict_autores = xmltodict.parse(exec)

                lista_autores = ""
                if (len(dict_autores["autores"]) > 1):
                    for aut in dict_autores["autores"]["nome_autor"]:
                        lista_autores += aut + ","
                else:
                    lista_autores = dict_autores["autores"]["nome_autor"]

                q = session.query(
                    'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_categorias_receita("{}")'.format(
                        request.POST.get("selected_recipe")))
                exec = q.execute()
                q.close()

                dict_categorias = xmltodict.parse(exec)

                lista_categorias = ""
                if (len(dict_categorias["categorias"]) > 1):
                    for cat in dict_categorias["categorias"]["categoria"]:
                        lista_categorias += cat + ","
                else:
                    lista_categorias = dict_categorias["categorias"]["categoria"]

                q = session.query(
                    'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_tipos_receita("{}")'.format(
                        request.POST.get("selected_recipe")))
                exec = q.execute()
                q.close()

                dict_tipos = xmltodict.parse(exec)

                lista_tipos = ""

                if (len(dict_tipos["tipos"]) > 1):
                    for tipo in dict_tipos["tipos"]["tipo"]:
                        lista_tipos += tipo + ","
                else:
                    lista_tipos = dict_tipos["tipos"]["tipo"]

                q = session.query(
                    'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_passos_receita("{}")'.format(
                        request.POST.get("selected_recipe")))
                exec = q.execute()
                q.close()

                dict_passos = xmltodict.parse(exec)
                lista_passos = ""
                for passo in dict_passos["descriçao"]["descriçao"]["passo"]:
                    lista_passos += passo + "\n"

                q = session.query(
                    'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_ingredientes_receita("{}")'.format(
                        request.POST.get("selected_recipe")))
                exec = q.execute()
                q.close()

                dict_ingredientes = xmltodict.parse(exec)
                lista_ingredientes = ""

                for item in dict_ingredientes["ingredientes"]["ingrediente"]:
                    item = list(item.items())
                    print(item)
                    if len(item) == 3:
                        lista_ingredientes += item[2][1] + "," + item[0][1] + "," + item[1][1] + "\n"
                    else:
                        lista_ingredientes += item[1][1] + "," + item[0][1] + "\n"

                print(lista_ingredientes)
            finally:
                # close session
                if session:
                    session.close()

            return JsonResponse({"receita": [dict_recipe["receita"]["nome"], lista_categorias,
                                             dict_recipe["receita"]["data"], lista_tipos, lista_autores,
                                             dict_recipe["receita"]["dificuldade"], lista_ingredientes, lista_passos,
                                             dict_recipe["receita"]["imagem"]]})
        else:
            try:
                error = False
                nome_receita = request.POST.get("receitas")

                session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

                q = session.query(
                    'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_receita("{}")'.format(
                        nome_receita))
                exec = q.execute()

                q.close()

                dict_recipe = xmltodict.parse(exec)

                next_nome_receita = request.POST.get("name")

                if dict_recipe["receita"]["nome"] != next_nome_receita or dict_recipe["receita"][
                    "data"] != request.POST.get("data") or dict_recipe["receita"]["dificuldade"] != request.POST.get(
                    "dificuldade") or \
                        dict_recipe["receita"]["imagem"] != request.POST.get("imagem"):
                    q = session.query(
                        'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:update_receita("{}", "{}", "{}","{}","{}")'.format(
                            nome_receita, next_nome_receita, request.POST.get("dificuldade"),
                            request.POST.get("imagem"), request.POST.get("data")))
                    exec = q.execute()
                    q.close()

                q = session.query(
                    'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_autores_receita("{}")'.format(
                        next_nome_receita))
                exec = q.execute()
                q.close()

                dict_autores = xmltodict.parse(exec)

                list_autores_original = dict_autores["autores"]["nome_autor"]

                new_list_autores = request.POST.get("aut").split(",")

                check = check_if_in_list_ahead(new_list_autores)

                if check:
                    raise Exception("ingrediente in list ahead")

                for auth in new_list_autores:
                    if auth not in list_autores_original:
                        q = session.query(
                            'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:add_autor("{}", "{}")'.format(
                                next_nome_receita, auth))
                        q.execute()
                        q.close()

                for auth in list_autores_original:
                    if auth not in new_list_autores:
                        q = session.query(
                            'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:delete_autor("{}", "{}")'.format(
                                next_nome_receita, auth))
                        q.execute()
                        q.close()

                q = session.query(
                    'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_categorias_receita("{}")'.format(
                        next_nome_receita))
                exec = q.execute()
                q.close()

                dict_categorias = xmltodict.parse(exec)

                list_categorias_original = dict_categorias["categorias"]["categoria"]

                new_list_categorias = request.POST.get("cat").split(",")

                check = check_if_in_list_ahead(new_list_categorias)

                if check:
                    raise Exception("ingrediente in list ahead")

                for cat in new_list_categorias:
                    if cat not in list_categorias_original:
                        q = session.query(
                            'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:add_categoria("{}", "{}")'.format(
                                next_nome_receita, cat))
                        q.execute()
                        q.close()

                for cat in list_categorias_original:
                    if cat not in new_list_categorias:
                        q = session.query(
                            'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:delete_categoria("{}", "{}")'.format(
                                next_nome_receita, cat))
                        q.execute()
                        q.close()

                q = session.query(
                    'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_tipos_receita("{}")'.format(
                        next_nome_receita))
                exec = q.execute()
                q.close()

                dict_tipos = xmltodict.parse(exec)

                list_tipos_original = dict_tipos["tipos"]["tipo"]

                new_list_tipos = request.POST.get("tipo").split(",")

                check = check_if_in_list_ahead(new_list_tipos)

                if check:
                    raise Exception("ingrediente in list ahead")

                for tip in new_list_tipos:
                    if tip not in list_tipos_original:
                        q = session.query(
                            'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:add_tipo("{}", "{}")'.format(
                                next_nome_receita, tip))
                        q.execute()
                        q.close()

                for tip in list_tipos_original:
                    if tip not in new_list_tipos:
                        q = session.query(
                            'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:delete_tipo("{}", "{}")'.format(
                                next_nome_receita, tip))
                        q.execute()
                        q.close()

                q = session.query(
                    'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_passos_receita("{}")'.format(
                        next_nome_receita))
                exec = q.execute()
                q.close()

                dict_passos = xmltodict.parse(exec)

                list_passos_original = dict_passos["descriçao"]["descriçao"]["passo"]

                new_list_passos = request.POST.get("passos").split("\n")

                if '' in new_list_passos:
                    new_list_passos.remove('')
                for i in range(0, len(new_list_passos)):
                    new_list_passos[i] = new_list_passos[i].replace("\r", "")

                check = check_if_in_list_ahead(new_list_passos)

                if check:
                    raise Exception("ingrediente in list ahead")

                count_passos = 0

                if len(list_passos_original) >= len(new_list_passos):
                    while count_passos != len(list_passos_original):

                        if count_passos < len(new_list_passos):

                            q = session.query(
                                'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:update_passo("{}", "{}","{}")'.format(
                                    next_nome_receita, list_passos_original[count_passos],
                                    new_list_passos[count_passos]))
                            q.execute()
                            q.close()


                        else:

                            q = session.query(
                                'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:delete_passo("{}", "{}")'.format(
                                    next_nome_receita, list_passos_original[count_passos]))
                            q.execute()
                            q.close()
                        count_passos += 1

                else:

                    while count_passos != len(new_list_passos):
                        if count_passos < len(list_passos_original):

                            q = session.query(
                                'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:update_passo("{}", "{}","{}")'.format(
                                    next_nome_receita, list_passos_original[count_passos],
                                    new_list_passos[count_passos]))
                            q.execute()
                            q.close()

                        else:

                            q = session.query(
                                'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:add_passo("{}", "{}")'.format(
                                    next_nome_receita, new_list_passos[count_passos]))
                            q.execute()
                            q.close()

                        count_passos += 1

                print("X")

                q = session.query(
                    'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_ingredientes_receita("{}")'.format(
                        next_nome_receita))
                exec = q.execute()
                q.close()

                dict_ingredientes = xmltodict.parse(exec)

                print("Y")

                list_ingredientes = dict_ingredientes["ingredientes"]["ingrediente"]

                list_ingredientes_original = []
                for ingrediente in list_ingredientes:
                    if len(ingrediente) == 3:
                        list_ingredientes_original.append(
                            ingrediente["nome_i"] + "," + ingrediente["unidade"] + "," + ingrediente["quantidade"])
                    else:
                        list_ingredientes_original.append(ingrediente["nome_i"] + "," + ingrediente["quantidade"])

                new_list_ingredientes = request.POST.get("ingredientes").split("\n")

                count_ingredientes = 0
                if '' in new_list_ingredientes:
                    new_list_ingredientes.remove('')

                for i in range(0, len(new_list_ingredientes)):
                    new_list_ingredientes[i] = new_list_ingredientes[i].replace("\r", "")

                check = check_if_in_list_ahead(new_list_ingredientes)

                if check:
                    raise Exception("ingrediente in list ahead")

                print(new_list_ingredientes)

                if len(list_ingredientes_original) >= len(new_list_ingredientes):
                    while count_ingredientes != len(list_ingredientes_original):

                        nome_ing = list_ingredientes_original[count_ingredientes].split(",")[0]
                        if count_ingredientes < len(new_list_ingredientes):
                            ing = new_list_ingredientes[count_ingredientes].split(",")
                            if len(ing) == 3:
                                q = session.query(
                                    'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:update_ingrediente3("{}", "{}", "{}","{}","{}")'.format(
                                        next_nome_receita, nome_ing, ing[0], ing[1], ing[2]))
                            else:
                                if len(ing) == 2:
                                    q = session.query(
                                        'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:update_ingrediente2("{}", "{}","{}","{}")'.format(
                                            next_nome_receita, nome_ing, ing[0], ing[1]))
                                else:
                                    raise Exception("not the right amount of arguments")

                            q.execute()
                            q.close()

                        else:
                            q = session.query(
                                'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:delete_ingrediente("{}", "{}")'.format(
                                    next_nome_receita, nome_ing))
                            q.execute()
                            q.close()
                        count_ingredientes += 1
                else:
                    while count_ingredientes != len(new_list_ingredientes):
                        ing = new_list_ingredientes[count_ingredientes].split(",")

                        if count_ingredientes < len(list_ingredientes_original):
                            nome_ing = list_ingredientes_original[count_ingredientes].split(",")[0]
                            if len(ing) == 3:

                                q = session.query(
                                    'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:update_ingrediente3("{}", "{}","{}","{}","{}")'.format(
                                        next_nome_receita, nome_ing, ing[0], ing[1], ing[2]))
                            else:
                                if len(ing) == 2:
                                    q = session.query(
                                        'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:update_ingrediente2("{}", "{}","{}","{}")'.format(
                                            next_nome_receita, nome_ing, ing[0], ing[1]))
                                else:
                                    raise Exception("not the right amount of arguments")

                            q.execute()
                            q.close()
                        else:
                            if len(ing) == 2:
                                q = session.query(
                                    'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:add_ingrediente2("{}", "{}","{}")'.format(
                                        next_nome_receita, ing[0], ing[1]))
                            else:
                                q = session.query(
                                    'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:add_ingrediente3("{}", "{}","{}","{}")'.format(
                                        next_nome_receita, ing[0], ing[1], ing[2]))

                            q.execute()
                            q.close()
                        count_ingredientes += 1
            except:
                error = True


            finally:
                q = session.query(
                    'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_nomes_receitas()')
                exec = q.execute()
                q.close()

                dict_nomes = xmltodict.parse(exec)

                if session:
                    session.close()

                return render(request, 'edit.html',
                              {"receitas": dict_nomes["nomes"]["nome"], "error": error, "edit_occurs": edit_occurs})

    return redirect("/")


def edit_receita(request):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    q = session.query('import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_nomes_receitas()')
    exec = q.execute()
    q.close()

    edit_occurs = False
    dict_nomes = xmltodict.parse(exec)
    return render(request, 'edit.html', {"receitas": dict_nomes["nomes"]["nome"], "edit_occurs": edit_occurs})


def add_recipe(request):
    requiredToAdd = ['name', 'cat', 'data', 'tipo', 'aut', 'dificuldade', 'ingredientes', 'passos', 'imagem']
    for req in requiredToAdd:
        if req not in request.POST:
            return render(request, 'add.html', {'error': True})
    # create session
    categorias = request.POST['cat'].split(',')
    if (len(categorias) != len(set(categorias))):
        return render(request, 'add.html', {'error': True})
    tipos = request.POST['tipo'].split(',')
    if (len(tipos) != len(set(tipos))):
        return render(request, 'add.html', {'error': True})
    ingredientes = request.POST['ingredientes'].split('\n')
    if (len(ingredientes) != len(set(ingredientes))):
        return render(request, 'add.html', {'error': True})
    if '' in ingredientes:
        ingredientes.remove('')

    for i in range(0, len(ingredientes)):
        ingredientes[i] = ingredientes[i].replace("\r", "")

    autores = request.POST['aut'].split(',')
    if (len(autores) != len(set(autores))):
        return render(request, 'add.html', {'error': True})
    passos = request.POST['passos'].split('\n')
    if (len(passos) != len(set(passos))):
        return render(request, 'add.html', {'error': True})

    if '' in passos:
        passos.remove('')

    for i in range(0, len(passos)):
        passos[i] = passos[i].replace("\r", "")

    print(categorias)
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    try:
        session.execute("""xquery import module namespace funcs = "com.funcs.my.index" at 'index.xqm';
funcs:add_receita(""" + '"' + request.POST.get('name', ' ') + '","' + request.POST.get('dificuldade',
                                                                                       ' ') + '","' + request.POST.get(
            'imagem', ' ') + '","' + request.POST.get('data', ' ') + '")')
        for categoria in categorias:
            print(categoria)
            session.execute("""xquery import module namespace funcs = "com.funcs.my.index" at 'index.xqm';
                       funcs:add_categoria(""" + '"' + request.POST.get('name', ' ') + '","' + categoria + '")')
        for tipo in tipos:
            print(tipo)
            session.execute("""xquery import module namespace funcs = "com.funcs.my.index" at 'index.xqm';
                       funcs:add_tipo(""" + '"' + request.POST.get('name', ' ') + '","' + tipo + '")')
        for ingrediente in ingredientes:
            it = ingrediente.split(",")
            if len(it) == 3:
                ingrediente = it[0]
                unidade = it[2]
                quantidade = it[1]
                session.execute("""xquery import module namespace funcs = "com.funcs.my.index" at 'index.xqm';
                           funcs:add_ingrediente3(""" + '"' + request.POST.get('name',
                                                                               ' ') + '","' + ingrediente + '","' + unidade
                                + '","' + quantidade + '")')
            else:
                ingrediente = it[0]
                quantidade = it[1]
                session.execute("""xquery import module namespace funcs = "com.funcs.my.index" at 'index.xqm';
                                           funcs:add_ingrediente2(""" + '"' + request.POST.get('name',
                                                                                               ' ') + '","' + ingrediente + '","' + quantidade + '")')

        for autor in autores:
            print(autor)
            session.execute("""xquery import module namespace funcs = "com.funcs.my.index" at 'index.xqm';
                       funcs:add_autor(""" + '"' + request.POST.get('name', ' ') + '","' + autor + '")')
        for passo in passos:
            print(passo)
            session.execute("""xquery import module namespace funcs = "com.funcs.my.index" at 'index.xqm';
                       funcs:add_passo(""" + '"' + request.POST.get('name', ' ') + '","' + passo + '")')
    finally:
        # close session
        if session:
            session.close()

    return render(request, 'main.html', {'error': False})


def delete(request):
    try:
        session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

        q = session.query(
            'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_nomes_receitas()')
        exec = q.execute()
        q.close()
        dict_nomes = xmltodict.parse(exec)
        print(dict_nomes)

    finally:
        if session:
            session.close()

    return render(request, 'del.html', {"receitas": dict_nomes["nomes"]["nome"], "error": False})


def del_recipe(request):
    if 'receitas' not in request.POST:
        session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
        q = session.query(
            'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_nomes_receitas()')
        exec = q.execute()
        q.close()

        dict_nomes = xmltodict.parse(exec)
        print(dict_nomes)
        if session:
            session.close()

        return render(request, 'del.html', {"receitas": dict_nomes["nomes"]["nome"], "error": True})

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    q = session.query(
        "import module namespace funcs = 'com.funcs.my.index' at 'index.xqm'; "
        "funcs:delete_receita('" + request.POST.get('receitas', ' ') + "')")
    exec = q.execute()

    q.close()

    print("erro")

    q = session.query('import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_nomes_receitas()')
    exec = q.execute()
    q.close()

    dict_nomes = xmltodict.parse(exec)
    print(dict_nomes)
    if session:
        session.close()

    return render(request, 'del.html', {"receitas": dict_nomes["nomes"]["nome"], "error": False})
    # return render(request, 'main.html', {'error': False})


def show_recipe(request, recipe):
    doc = etree.parse("app/data/receitas.xml")

    search_recipe_xml = doc.xpath("//receita[nome = '{}']".format(recipe))

    fn = 'receita.xslt'
    pname = os.path.join(BASE_DIR, 'app/data/' + fn)
    xslt = etree.parse(pname)
    transform = etree.XSLT(xslt)
    html = transform(search_recipe_xml[0])
    return render(request, 'show_recipe.html', {'xslt_to_html': html})


@csrf_exempt
def validatexml(request):
    validation_performed = False
    if request.method == 'POST':
        try:

            xml_to_verify = request.FILES["xml"]

            xsd_file = etree.parse("app/data/receitas.xsd")

            xmlschema = etree.XMLSchema(xsd_file)

            doc = etree.parse(xml_to_verify)

            valid = xmlschema.validate(doc)

            validation_performed = True
            return render(request, "validation.html", {"valid": valid, "validation_performed": validation_performed})
        except:
            validation_performed = True
            valid = False
            return render(request, "validation.html", {"valid": valid, "validation_performed": validation_performed})

    else:
        return render(request, "validation.html", {'validation_performed': validation_performed})
