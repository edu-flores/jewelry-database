<!-- purchase.xsl -->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="purchase">
    <html>
      <head>
        <style>
          body {
            font-family: Monospace, sans-serif;
            margin: 2rem 4rem;
          }

          table {
            border-collapse: collapse;
            width: 100%;
          }

          th, td {
            border: 1px solid #dddddd;
            padding: 8px;
          }

          tr:nth-child(even) {
            background-color: #f2f2f2;
          }

          .flex {
            display: flex;
          }

          a {
            display: block;
            margin-top: 2rem;
          }
        </style>
      </head>
      <body>
        <!-- Details -->
        <h1>Detalles de la Orden</h1>
        <div class="flex">
        <table>
          <tr>
            <th>Cliente</th>
            <td><xsl:value-of select="details/client"/></td>
          </tr>
          <tr>
            <th>Destinatario</th>
            <td><xsl:value-of select="details/receiver"/></td>
          </tr>
          <tr>
            <th>Fecha</th>
            <td><xsl:value-of select="details/date"/></td>
          </tr>
          <tr>
            <th>Estatus</th>
            <td><xsl:value-of select="details/status"/></td>
          </tr>
          <tr>
            <th>Comentarios</th>
            <td><xsl:value-of select="details/comments"/></td>
          </tr>
          <tr>
            <th>Total</th>
            <td>$<xsl:value-of select="details/total"/></td>
          </tr>
        </table>
        <!-- Addresses -->
        <table>
          <!-- Shipping -->
          <tr>
            <th colspan="2">Dirección de Envío</th>
          </tr>
          <tr>
            <th>Calle</th>
            <td><xsl:value-of select="details/addresses/shipping/street"/></td>
          </tr>
          <tr>
            <th>Ciudad</th>
            <td><xsl:value-of select="details/addresses/shipping/city"/></td>
          </tr>
          <tr>
            <th>País</th>
            <td><xsl:value-of select="details/addresses/shipping/country"/></td>
          </tr>
          <tr>
            <th>Código postal</th>
            <td><xsl:value-of select="details/addresses/shipping/postalCode"/></td>
          </tr>
          <!-- Billing -->
          <tr>
            <th colspan="2">Dirección de Facturación</th>
          </tr>
          <tr>
            <th>Calle</th>
            <td><xsl:value-of select="details/addresses/billing/street"/></td>
          </tr>
          <tr>
            <th>Ciudad</th>
            <td><xsl:value-of select="details/addresses/billing/city"/></td>
          </tr>
          <tr>
            <th>País</th>
            <td><xsl:value-of select="details/addresses/billing/country"/></td>
          </tr>
          <tr>
            <th>Código Postal</th>
            <td><xsl:value-of select="details/addresses/billing/postalCode"/></td>
          </tr>
        </table>
        </div>
        <!-- List of Products -->
        <h2>Products (<xsl:value-of select="count(products/product)"/>)</h2>
        <table>
          <tr>
            <th>Code</th>
            <th>Description</th>
            <th>Price</th>
            <th>Quantity</th>
            <th>Subtotal</th>
          </tr>
          <xsl:for-each select="products/product">
            <tr>
              <td><xsl:value-of select="code"/></td>
              <td><xsl:value-of select="description"/></td>
              <td>$<xsl:value-of select="price"/></td>
              <td><xsl:value-of select="quantity"/></td>
              <td>$<xsl:value-of select="subtotal"/></td>
            </tr>
          </xsl:for-each>
        </table>
        <!-- Go Back -->
        <a href="/">↻ Regresar a la página principal</a>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
