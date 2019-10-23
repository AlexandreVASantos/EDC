from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from lxml import etree
import os
from EDC.settings import BASE_DIR
from BaseXClient import BaseXClient
import xmltodict


def home(request):
    return render(request, "main.html")


def listrecipes(request):
    doc = etree.parse("app/data/receitas.xml")
    search = doc.xpath("//receita")

    information = {}


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