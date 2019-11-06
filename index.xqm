module namespace funcs = "com.funcs.my.index";

declare function funcs:get_receitas_byCat($categoria) as node()*
{
  <receita>{
  let $receita := collection("receitas")//receita[categorias/categoria=$categoria]

  for $rec in $receita
  return (
    $rec/nome,
    $rec/imagem
)
  }</receita>
};

declare function funcs:get_receitas_byDif($dificuldade) as node()*
{
  <receita>{
  let $receita := collection("receitas")//receita[dificuldade=$dificuldade]

  for $rec in $receita
  return (
      $rec/nome,
      $rec/imagem
    )
  }</receita>
};

declare function funcs:get_receitas_byTags($tag) as node()*
{
  <receita>{
  let $receita := collection("receitas")//receita[tipos/tipo=$tag]

  for $rec in $receita
  return (
      $rec/nome,
      $rec/imagem
    )
    }</receita>
};

declare function funcs:get_receitas_byAut($autor) as node()*
{
  <receita>{
  let $receita := collection("receitas")//receita[autores/nome_autor=$autor]

  for $rec in $receita
  return (
      $rec/nome,
      $rec/imagem
    )
    }</receita>
};


declare function funcs:get_nomes_receitas() as node()*
{
    <nomes>{
        let $receita := collection("receitas")//receita
        let $nomes := $receita/nome
        for $n in $nomes
	order by $n
        return $n
   }</nomes>
};

declare function funcs:get_tipos_receita($nome_receita) as node()*
{
  <tipos>{
    let $receita := collection("receitas")//receita[nome=$nome_receita]
    let $tipos := $receita/tipos
    for $t in $tipos
    return $t/tipo
  }</tipos>
};

declare function funcs:get_passos_receita($nome_receita) as node()*
{
  <descriçao>{
    let $receita := collection("receitas")//receita[nome=$nome_receita]
    let $descricao := $receita/descriçao
    for $p in $descricao
    return $p
  }</descriçao>
};


declare function funcs:get_ingredientes_receita($nome_receita) as node()*
{
  <ingredientes>{
    let $receita := collection("receitas")//receita[nome=$nome_receita]
    let $ingredientes := $receita/ingredientes/ingrediente
    for $i in $ingredientes
    return $i
  }</ingredientes>
};

declare function funcs:get_categorias_receita($nome_receita) as node()*
{
  <categorias>{
    let $receita := collection("receitas")//receita[nome=$nome_receita]
    let $categorias := $receita/categorias
    for $c in $categorias
    return $c/categoria
  }</categorias>
};

declare function funcs:get_autores_receita($nome_receita) as node()*
{
  <autores>{
    let $receita := collection("receitas")//receita[nome=$nome_receita]
    let $autores := $receita/autores
    for $a in $autores
    return $a/nome_autor
  }</autores>
};




declare function funcs:get_dificuldades() as node()*
{
  <dificuldades>{
    let $receita := collection("receitas")//receita
    for $d in $receita
    return $d/dificuldade
  }</dificuldades>
  
};

declare function funcs:get_categorias() as node()*
{
  <categorias>{
    let $receita := collection("receitas")//receita
    for $c in $receita
    return $c/categorias/categoria
  }</categorias>
  
};

declare function funcs:get_tags() as node()*
{
  <tags>{
    let $receita := collection("receitas")//receita
    for $t in $receita
    return $t/tipos/tipo
  }</tags>
  
};


declare function funcs:get_autores() as node()*
{
  <autores>{
    let $receita := collection("receitas")//receita
    for $a in $receita
    return $a/autores/nome_autor
  }</autores>
};


declare function funcs:get_all_receita($nome) as node()*
{
let $receita := collection("receitas")//receita[nome=$nome]
return (<root>{$receita}</root>)
 
};

declare function funcs:get_receita($nome)as node()*
{
let $receita := collection("receitas")//receita[nome=$nome]
return (
  <receita>
    {$receita/nome}
    {$receita/data}
    {$receita/dificuldade}
    {$receita/imagem}
  </receita>)
};




declare function funcs:get_count_ingredientes($nome)
{
let $receita := collection("receitas")//receita[nome=$nome]
return count($receita/ingredientes/ingrediente)
};


declare updating function funcs:add_receita($nome, $dificuldade, $imagem, $data)
{
  let $receitas := collection("receitas")/receitas
  return insert node(
    <receita>
      <nome>{$nome}</nome>
      <categorias>
      </categorias>
      <tipos>
      </tipos>
      <data>{$data}</data>
      <autores>
      </autores>
      <ingredientes>
      </ingredientes>
      <dificuldade>{$dificuldade}</dificuldade>
      <imagem>{$imagem}</imagem>
      <descriçao>
      </descriçao>
        
    </receita>
  ) as last into $receitas
  
};


declare updating function funcs:add_autor($nome,$autor)
{
  let $receita := collection("receitas")//receita[nome=$nome]
  return insert node(
    <nome_autor>{$autor}</nome_autor>) as last into $receita/autores
};

declare updating function funcs:add_categoria($nome,$categoria)
{
  let $receita := collection("receitas")//receita[nome=$nome]
  return insert node(
    <categoria>{$categoria}</categoria>) as last into $receita/categorias
};

declare updating function funcs:add_tipo($nome,$tipo)
{
  let $receita := collection("receitas")//receita[nome=$nome]
  return insert node(
    <tipo>{$tipo}</tipo>) as last into $receita/tipos
};


declare updating function funcs:add_passo($nome,$passo)
{
  let $receita := collection("receitas")//receita[nome=$nome]
  return insert node(
    <passo>{$passo}</passo>) as last into $receita/descriçao
};

declare updating function funcs:add_ingrediente3($nome,$ingrediente, $unidade, $quantidade)
{
  let $receita := collection("receitas")//receita[nome=$nome]
  return insert node(
    <ingrediente>
        <quantidade>{$quantidade}</quantidade>
        <unidade>{$unidade}</unidade>
        <nome_i>{$ingrediente}</nome_i>
    </ingrediente>) as last into $receita/ingredientes
};


declare updating function funcs:add_ingrediente2($nome,$ingrediente, $quantidade)
{
  let $receita := collection("receitas")//receita[nome=$nome]
  return insert node(
    <ingrediente>
        <quantidade>{$quantidade}</quantidade>
        <nome_i>{$ingrediente}</nome_i>
    </ingrediente>) as last into $receita/ingredientes
};

declare updating function funcs:delete_receita($nome)
{
  let $receita := collection("receitas")//receita[nome=$nome]
  return delete node $receita
};


declare updating function funcs:delete_ingrediente($nome_receita, $ingrediente)
{
   let $receita := collection("receitas")//receita[nome=$nome_receita]
   let $i := $receita/ingredientes/ingrediente[nome_i = $ingrediente]
   return delete node $i
};

declare updating function funcs:update_receita($nome_atual, $next_nome, $dificuldade, $imagem, $data)
{
  
  let $receita := collection('receitas')//receita[nome=$nome_atual]
  return( replace node $receita/nome/text() with $next_nome,
          replace node $receita/dificuldade/text() with $dificuldade,
          replace node $receita/imagem/text() with $imagem,
          replace node $receita/data/text() with $data
  )
  
};



declare updating function funcs:delete_autor($nome_receita, $autor)
{
  let $receita := collection('receitas')//receita[nome=$nome_receita]
  let $aut := $receita/autores/nome_autor[text() = $autor]
  return delete node $aut
  
};

declare updating function funcs:delete_categoria($nome_receita, $categoria)
{
  let $receita := collection('receitas')//receita[nome=$nome_receita]
  let $cat := $receita/categorias/categoria[text() = $categoria]
  return delete node $cat
  
};


declare updating function funcs:delete_tipo($nome_receita, $tipo)
{
  let $receita := collection('receitas')//receita[nome=$nome_receita]
  let $tipo := $receita/tipos/tipo[text() = $tipo]
  return delete node $tipo
  
};


declare updating function funcs:delete_passo($nome_receita, $passo)
{
  let $receita := collection('receitas')//receita[nome=$nome_receita]
  let $passo := $receita/descriçao/passo[contains(., $passo)]
  return delete node $passo
  
};



declare updating function funcs:update_passo($nome_receita, $passo, $new_passo)
{
  let $receita := collection('receitas')//receita[nome=$nome_receita]
  let $p := $receita/descriçao/passo[contains(.,$passo)]
  for $t in $p
  return ( replace node $p/text() with $new_passo )
  
};

declare function funcs:get_xslt($xml) as node()*
{
  let $i := $xml
  let $w :=
<xsl:stylesheet version='1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:xslt='http://www.w3.org/1999/XSL/Transform'>
<xsl:output method='html' indent='yes'/>



<xsl:template match='/receita'>

    <div  style = 'padding-top:8%; padding-left:10%; padding-right:10%'>

        <div class= 'row' style = 'height:40vh'>

            <div class='col-md-4' style='tex-align:center'>
                <table>
                    <tr>
                      <td><h2><xsl:value-of select='nome'/></h2></td>
                    </tr>
                </table>
                <table>
                    <xsl:for-each select='autores/nome_autor'>
                   <tr>
                      <td><h3><xsl:value-of select='.'/></h3></td>
                       <br></br>
                    </tr>
                    </xsl:for-each>
                </table>

                <br></br>
                <table>
                    <xsl:for-each select='categorias/categoria'>
                   <tr>
                      <td><h3><xsl:value-of select='.'/></h3></td>
                       <br></br>
                    </tr>
                    </xsl:for-each>
                </table>

                 <table>
                    <xsl:for-each select='tipos/tipo'>
                   <tr>
                      <td><h4><xsl:value-of select='.'/></h4></td>
                       <br></br>
                    </tr>
                    </xsl:for-each>
                </table>

                <br></br>

                 <table>
                    <tr>
                      <td><h4><xsl:value-of select='data'/></h4></td>
                    </tr>
                 </table>



            </div>
            <div class='col-md-8'  style='text-align:center'>
                <img style='width:90%'>
                    <xsl:attribute name='src'>
                        <xsl:value-of select='imagem' />
                    </xsl:attribute>
                </img>
            </div>
        </div>
    </div>

        <div class='row' style = 'padding-top:10%; padding-left:10%; padding-right:10%'>
            <div class = 'col-md-8'>

                <table>
                    <tr>
                      <th style='text-align:left'><h4>Descrição</h4></th>
                    </tr>
                    <xsl:for-each select='descriçao/passo'>
                   <tr>
                       <td><p><xsl:value-of select='.'/></p></td>
                       <br></br>
                    </tr>
                    </xsl:for-each>
                </table>
            </div>
            <div class = 'col-md-4'>
                <table class='table table-striped'>
                    <tr>
                      <th style='text-align:center'><h4>Ingredientes</h4></th>
                    </tr>
                    <xsl:for-each select='ingredientes/ingrediente'>
                   <tr>
                      <td><p><xsl:value-of select='nome_i'/></p></td>
                      <td><p><xsl:value-of select='quantidade'/></p></td>
                      <td><p><xsl:value-of select='unidade'/></p></td>
                    </tr>
                    </xsl:for-each>
                </table>
            </div>

        </div>




</xsl:template>


</xsl:stylesheet>
  

return xslt:transform($i,$w) 
};


declare updating function funcs:update_ingrediente2($nome_receita, $ingrediente, $novo_ingrediente, $quantidade)
{
  let $receita := collection('receitas')//receita[nome=$nome_receita]
  let $ingrediente := $receita/ingredientes/ingrediente[nome_i = $ingrediente]
  return( replace node $ingrediente/nome_i/text() with $novo_ingrediente,
          replace node $ingrediente/quantidade/text() with $quantidade
  )
  
};

declare updating function funcs:update_ingrediente3($nome_receita, $ingrediente, $novo_ingrediente, $unidade, $quantidade)
{
  let $receita := collection('receitas')//receita[nome=$nome_receita]
  let $ingrediente := $receita/ingredientes/ingrediente[nome_i = $ingrediente]
  return( replace node $ingrediente/nome_i/text() with $novo_ingrediente,
          replace node $ingrediente/unidade/text() with $unidade,
          replace node $ingrediente/quantidade/text() with $quantidade
  )
  
};

