import xmltodict


def main():
    dictautores ={}
    dictdificuldades ={}
    dicttipos = {}
    dictcategorias = {}
    count_ing =0

    categorias_id = '<http://receita/categorias/'
    categorias_pred='<http://receita/categorias/pred/nome>'

    tipos_id = '<http://receita/tipos/'
    tipos_pred = '<http://receita/tipos/pred/nome>'

    dificuldades_id = '<http://receita/dificuldades/'
    dificuldades_pred = '<http://receita/dificuldades/pred/nome>'

    ingrediente_id = '<http://receita/ingrediente/'
    ingrediente_pred = '<http://receita/ingrediente/pred/'

    autores_id = '<http://receita/autores/'
    autores_pred = '<http://receita/autores/pred/nome>'

    with open('receitas.xml') as f:
        d = xmltodict.parse(f.read())

    strreceitas = ''

    strautores = ''

    string = ''
    strtipos = ''

    strcategorias = ''

    strdificuldades = ''


    new_file= open('test.nt', 'a')
    receita_pred = '<http://receita/pred/'
    count = 0
    for receita in d['receitas']['receita']:
        count +=1
        id = '<http://receita/id/' + str(count) + '> '

        strreceitas+= id + receita_pred + 'nome> "' +receita['nome'] + '".\n'


        if isinstance(receita['categorias']['categoria'], list):
            for x in receita['categorias']['categoria']:
                if x not in dictcategorias.keys():
                    dictcategorias[x] = categorias_id + str(len(dictcategorias.keys())+1) + '> '
                    strcategorias += dictcategorias[x] + categorias_pred + ' "' + x + '".\n'

                strreceitas += id + receita_pred + 'categoria> ' + dictcategorias[x] + '.\n'



        else:
            if receita['categorias']['categoria'] not in dictcategorias.keys():
                dictcategorias[receita['categorias']['categoria']] = categorias_id + str(len(dictcategorias.keys()) + 1) + '> '
                strcategorias += dictcategorias[receita['categorias']['categoria']] + categorias_pred + ' "' + receita['categorias']['categoria'] + '".\n'

            strreceitas += id + receita_pred + 'categoria> ' + dictcategorias[receita['categorias']['categoria']] + '.\n'

        if isinstance(receita['tipos']['tipo'], list):
            for x in receita['tipos']['tipo']:
                if x not in dicttipos.keys():
                    dicttipos[x] = tipos_id + str(len(dicttipos.keys()) + 1) + '> '
                    strtipos += dicttipos[x] + tipos_pred + ' "' + x + '".\n'

                strreceitas+= id + receita_pred + 'tipo> ' + dicttipos[x] + '.\n'



        else:
            if receita['tipos']['tipo'] not in dicttipos.keys():
                dicttipos[receita['tipos']['tipo']] = tipos_id + str(len(dicttipos.keys()) + 1) + '> '
                strtipos +=  dicttipos[receita['tipos']['tipo']] + tipos_pred + ' "' + receita['tipos']['tipo'] + '".\n'

            strreceitas+= id + receita_pred + 'tipo> ' + dicttipos[receita['tipos']['tipo']] + '.\n'



        if isinstance(receita['autores']['nome_autor'], list):
            for x in receita['autores']['nome_autor']:
                if x not in dictautores.keys():
                    dictautores[x] = autores_id + str(len(dictautores.keys()) + 1) + '> '
                    strautores += dictautores[x] + autores_pred + ' "' + x + '".\n'

                strreceitas += id + receita_pred + 'autor> ' + dictautores[x] + '.\n'



        else:
            if receita['autores']['nome_autor'] not in dictautores.keys():
                dictautores[receita['autores']['nome_autor']] = autores_id + str(len(dictautores.keys()) + 1) + '> '
                strautores += dictautores[receita['autores']['nome_autor']] + autores_pred + ' "' + receita['autores']['nome_autor'] + '".\n'

            strreceitas += id + receita_pred + 'autor> ' + dictautores[receita['autores']['nome_autor']] + '.\n'


        if receita['dificuldade'] not in dictdificuldades.keys():
            dictdificuldades[receita['dificuldade']] = dificuldades_id + str(len(dictdificuldades.keys()) + 1) + '> '
            strdificuldades += dictdificuldades[receita['dificuldade']] + dificuldades_pred + ' "' + receita['dificuldade'] + '".\n'

        strreceitas += id + receita_pred + 'dificuldade> ' + dictdificuldades[receita['dificuldade']] + '.\n'





        if isinstance(receita['ingredientes']['ingrediente'], list):


            for x in receita['ingredientes']['ingrediente']:
                count_ing +=1
                strreceitas += id + receita_pred + 'ingrediente> ' + ingrediente_id + str(count_ing) + '. \n'
                strreceitas += ingrediente_id + str(count_ing) + "> " + ingrediente_pred + 'nome> "' + x["nome_i"]+ '" .\n'
                strreceitas += ingrediente_id + str(count_ing) + "> " + ingrediente_pred + 'quantidade> "' + x["quantidade"] + '" .\n'
                if len(x) == 3:
                    strreceitas += ingrediente_id + str(count_ing) + "> " + ingrediente_pred + 'unidade> "' + x["unidade"] + '" .\n'

        if isinstance(receita['descriçao']['passo'], list):
            for x in receita['descriçao']['passo']:
                strreceitas += id + receita_pred + 'passo> "' + x + '".\n'
        else:
            strreceitas += id + receita_pred + 'passo> "' + receita['descriçao']['passo'] + '".\n'


        strreceitas += id + receita_pred + 'data> "' + receita["data"] + '".\n'
        strreceitas += id + receita_pred + 'imagem> "' + receita["imagem"] + '".\n'


    new_file.write(strautores)
    new_file.write(strcategorias)
    new_file.write(strtipos)
    new_file.write(strdificuldades)

    new_file.write(strreceitas)
    new_file.write(string)


main()