from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
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
