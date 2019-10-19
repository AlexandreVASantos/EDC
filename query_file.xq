
(:
declare function local:get_tipos_receita($nome_receita)
{
let $receita := collection("receitas")//receita[nome=$nome_receita]
let $tipos := $receita/tipos
for $t in $tipos
return $t/tipo/text()
};






declare function local:get_categorias_receita($nome_receita)
{
let $receita := collection("receitas")//receita[nome=$nome_receita]
let $categorias := $receita/categorias
for $c in $categorias
return $c/categoria/text()
};

declare function local:get_autores_receita($nome_receita)
{
let $receita := collection("receitas")//receita[nome=$nome_receita]
let $autores := $receita/autores
for $a in $autores
return $a/nome_autor/text()
};




declare function local:get_dificuldades()
{
  let $receita := collection("receitas")//receita
  return distinct-values($receita/dificuldade)
};

declare function local:get_categorias()
{
  let $receita := collection("receitas")//receita
  return distinct-values( $receita/categorias/categoria)
};

declare function local:get_tags()
{
  let $receita := collection("receitas")//receita
  return distinct-values($receita/tipos/tipo)
};


declare function local:get_autores()
{
let $receita := collection("receitas")//receita
return distinct-values($receita/autores/nome_autor)
};


declare function local:get_receita($nome)
{
let $receita := collection("receitas")//receita[nome=$nome]
return ($receita/nome, $receita/data,$receita/dificuldade,$receita/imagem)
};




declare function local:get_count_ingredientes($nome)
{
let $receita := collection("receitas")//receita[nome=$nome]
return count($receita/ingredientes/ingrediente)
};


declare updating function local:add_receita($nome, $dificuldade, $imagem, $data)
{
  let $receitas := collection("receitas")
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


declare updating function local:add_autor($nome,$autor)
{
  let $receita := collection("receitas")//receita[nome=$nome]
  return insert node(
    <nome_autor>{$autor}</nome_autor>) as last into $receita/autores
};

declare updating function local:add_categoria($nome,$categoria)
{
  let $receita := collection("receitas")//receita[nome=$nome]
  return insert node(
    <categoria>{$categoria}</categoria>) as last into $receita/categorias
};

declare updating function local:add_tipo($nome,$tipo)
{
  let $receita := collection("receitas")//receita[nome=$nome]
  return insert node(
    <tipo>{$tipo}</tipo>) as last into $receita/tipos
};


declare updating function local:add_passo($nome,$passo)
{
  let $receita := collection("receitas")//receita[nome=$nome]
  return insert node(
    <passo>{$passo}</passo>) as last into $receita/descriçao
};

declare updating function local:add_ingrediente($nome,$ingrediente, $unidade, $quantidade)
{
  let $receita := collection("receitas")//receita[nome=$nome]
  return insert node(
    <ingrediente>
        <quantidade>{$quantidade}</quantidade>
        <unidade>{$unidade}</unidade>
        <nome_i>{$ingrediente}</nome_i>
    </ingrediente>) as last into $receita/ingredientes
};


declare updating function local:delete_receita($nome)
{
  let $receita := collection("receitas")//receita[nome=$nome]
  return delete node $receita
};


declare updating function local:delete_ingrediente($nome_receita, $ingrediente)
{
   let $receita := collection("receitas")//receita[nome=$nome_receita]
   let $i := $receita/ingredientes/ingrediente[nome_i = $ingrediente]
   return delete node  $i
};

declare updating function local:update_receita($nome_atual, $next_nome, $dificuldade, $imagem, $data)
{
  
  let $receita := collection('receitas')//receita[nome=$nome_atual]
  return( replace node $receita/nome with $next_nome,
          replace node $receita/dificuldade with $dificuldade,
          replace node $receita/imagem with $imagem,
          replace node $receita/data with $data
  )
  
};


declare updating function local:update_data($nome, $data, $new_data)
{
  let $receita := collection('receitas')//receita[nome=$nome]
  return( replace node $receita/data with $new_data
  )
};

declare updating function local:update_ingrediente($nome_receita, $ingrediente, $novo_ingrediente, $unidade, $quantidade)
{
  let $receita := collection('receitas')//receita[nome=$nome_receita]
  let $ingrediente := $receita/ingredientes/ingrediente[nome_i = $ingrediente]
  return( replace node $ingrediente/nome_i with $novo_ingrediente,
          replace node $ingrediente/unidade with $unidade,
          replace node $ingrediente/quantidade with $quantidade
  )
  
};
:)
