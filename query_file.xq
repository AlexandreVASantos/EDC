module namespace funcs = "com.funcs.my.index";

declare function funcs:get_tipos_receita($nome_receita) as node()*
{
  <tipos>{
    let $receita := collection("receitas")//receita[nome=$nome_receita]
    let $tipos := $receita/tipos
    for $t in $tipos
    return $t/tipo
  }</tipos>
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

declare updating function funcs:add_ingrediente($nome,$ingrediente, $unidade, $quantidade)
{
  let $receita := collection("receitas")//receita[nome=$nome]
  return insert node(
    <ingrediente>
        <quantidade>{$quantidade}</quantidade>
        <unidade>{$unidade}</unidade>
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


declare updating function funcs:update_data($nome, $data, $new_data)
{
  let $receita := collection('receitas')//receita[nome=$nome]
  return( replace node $receita/data/text() with $new_data
  )
};

declare updating function funcs:update_ingrediente($nome_receita, $ingrediente, $novo_ingrediente, $unidade, $quantidade)
{
  let $receita := collection('receitas')//receita[nome=$nome_receita]
  let $ingrediente := $receita/ingredientes/ingrediente[nome_i = $ingrediente]
  return( replace node $ingrediente/nome_i/text() with $novo_ingrediente,
          replace node $ingrediente/unidade/text() with $unidade,
          replace node $ingrediente/quantidade/text() with $quantidade
  )
  
};

