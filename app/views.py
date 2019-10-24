from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from lxml import etree
import os
from EDC.settings import BASE_DIR
from BaseXClient import BaseXClient
import xmltodict


def home(request):
    return render(request, "main.html")


def handle_lista_ingredientes(req):
    lista = req.split(",")
    list_tupples = []
    count =0
    tmp = []
    for i in range(0,lista):
        tmp.append(i)
        if count == 2:
            count = 0
            list_tupples.append(tmp)
            tmp=[]
        else:
            count = count + 1
    return


def listrecipes(request):
    doc = etree.parse("app/data/receitas.xml")
    search = doc.xpath("//receita")

    information = {}
    autores=[]

    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    try:
        q = session.query('import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_autores()')
        exec = q.execute()
        q.close()
        print(exec)

        dict= xmltodict.parse(exec)

        print(dict)
    finally:
        # close session
        if session:
            session.close()

    for s in search:
        index= s.find("nome").text
        print(s.find("imagem").text)
        information[index] = []
        information[index].append(s.find("imagem").text)
        information[index].append(s.find("autores/nome_autor").text)

    return render(request, "list_recipes.html", {"info": information})


def add_receita(request):
    return render(request, 'add.html')

@csrf_exempt
def edit_recipe(request):
    if request.method == 'POST':
        if request.is_ajax():
            print(request.POST)
            session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
            try:
                q = session.query(
                    'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_receita("{}")'.format(request.POST.get("selected_recipe")))
                exec = q.execute()
                q.close()

                dict_recipe = xmltodict.parse(exec)
                print(dict_recipe)

                q = session.query(
                    'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_autores_receita("{}")'.format(
                        request.POST.get("selected_recipe")))
                exec = q.execute()
                q.close()

                dict_autores = xmltodict.parse(exec)

                lista_autores = ""
                if(len(dict_autores["autores"]) > 1):
                    for aut in dict_autores["autores"]["nome_autor"]:
                        lista_autores += aut + ","
                else:
                    lista_autores=dict_autores["autores"]["nome_autor"]


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

                if(len(dict_tipos["tipos"]) >1):
                    for tipo in dict_tipos["tipos"]["tipo"]:
                        lista_tipos += tipo + ","
                else:
                    lista_tipos= dict_tipos["tipos"]["tipo"]

                q = session.query(
                    'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_passos_receita("{}")'.format(
                        request.POST.get("selected_recipe")))
                exec = q.execute()
                q.close()

                dict_passos = xmltodict.parse(exec)
                lista_passos=""
                for passo in dict_passos["descriçao"]["descriçao"]["passo"]:
                    lista_passos+= passo + ","

                q = session.query(
                    'import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_ingredientes_receita("{}")'.format(
                        request.POST.get("selected_recipe")))
                exec = q.execute()
                q.close()

                dict_ingredientes = xmltodict.parse(exec)
                lista_ingredientes=""



                for item in dict_ingredientes["ingredientes"]["ingrediente"]:
                    item = list(item.items())
                    if len(item) == 3:
                        lista_ingredientes+= item[2][1] + ","+ item[0][1] +"," + item[1][1]+ ","
                    else:
                        lista_ingredientes += item[1][1] + "," + item[0][1] + ","


                print(lista_ingredientes)

            finally:
                # close session
                if session:
                    session.close()



            return JsonResponse({"receita": [dict_recipe["receita"]["nome"],lista_categorias,dict_recipe["receita"]["data"],lista_tipos,lista_autores,dict_recipe["receita"]["dificuldade"],lista_ingredientes,lista_passos,dict_recipe["receita"]["imagem"]]})

        return render(request)



def edit_receita(request):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    q = session.query('import module namespace funcs = "com.funcs.my.index" at "index.xqm";funcs:get_nomes_receitas()')
    exec = q.execute()
    q.close()


    dict_nomes = xmltodict.parse(exec)
    return render(request, 'edit.html', {"receitas": dict_nomes["nomes"]["nome"]})

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



def del_receita(request):

    return render(request, 'del.html')


def show_recipe(request, recipe):
    doc = etree.parse("app/data/receitas.xml")

    search_recipe_xml = doc.xpath("//receita[nome = '{}']".format(recipe))


    fn = 'receita.xslt'
    pname = os.path.join(BASE_DIR,'app/data/' + fn)
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
            return render(request, "validation.html", {"valid": valid, "validation_performed" : validation_performed})
        except:
            validation_performed = True
            valid = False
            return render(request, "validation.html", {"valid": valid, "validation_performed": validation_performed})

    else:
        return render(request, "validation.html", {'validation_performed' : validation_performed})
