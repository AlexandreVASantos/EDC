<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:xslt="http://www.w3.org/1999/XSL/Transform">


<xsl:output method="html" indent="yes"/>



<xsl:template match="/receita">

    <div  style = "padding-top:8%; padding-left:10%; padding-right:10%">

        <div class= "row" style = "height:40vh">

            <div class="col-md-4" style="tex-align:center">
                <table>
                    <tr>
                      <td><h2><xsl:value-of select="nome"/></h2></td>
                    </tr>
                </table>
                <table>
                    <xsl:for-each select="autores/nome_autor">
                   <tr>
                      <td><h3><xsl:value-of select="."/></h3></td>
                       <br></br>
                    </tr>
                    </xsl:for-each>
                </table>

                <br></br>
                <table>
                    <xsl:for-each select="categorias/categoria">
                   <tr>
                      <td><h3><xsl:value-of select="."/></h3></td>
                       <br></br>
                    </tr>
                    </xsl:for-each>
                </table>

                 <table>
                    <xsl:for-each select="tipos/tipo">
                   <tr>
                      <td><h4><xsl:value-of select="."/></h4></td>
                       <br></br>
                    </tr>
                    </xsl:for-each>
                </table>

                <br></br>

                 <table>
                    <tr>
                      <td><h4><xsl:value-of select="data"/></h4></td>
                    </tr>
                 </table>



            </div>
            <div class="col-md-8"  style="text-align:center">
                <img style="width:90%">
                    <xsl:attribute name="src">
                        <xsl:value-of select='imagem' />
                    </xsl:attribute>
                </img>
            </div>
        </div>
    </div>

        <div class="row" style = "padding-top:10%; padding-left:10%; padding-right:10%">
            <div class = "col-md-8">

                <table>
                    <tr>
                      <th style="text-align:left"><h4>Descrição</h4></th>
                    </tr>
                    <xsl:for-each select="descriçao/passo">
                   <tr>
                       <td><p><xsl:value-of select="."/></p></td>

                    </tr>
                    </xsl:for-each>
                </table>
            </div>
            <div class = "col-md-4">
                <table class="table table-striped">
                    <tr>
                      <th style="text-align:center"><h4>Ingredientes</h4></th>
                    </tr>
                    <xsl:for-each select="ingredientes/ingrediente">
                   <tr>
                      <td><p><xsl:value-of select="nome_i"/></p></td>
                      <td><p><xsl:value-of select="quantidade"/></p></td>
                      <td><p><xsl:value-of select="unidade"/></p></td>
                    </tr>
                    </xsl:for-each>
                </table>
            </div>

        </div>




</xsl:template>


</xsl:stylesheet>