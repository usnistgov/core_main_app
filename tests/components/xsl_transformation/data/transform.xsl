<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
    <xsl:template match="/">
        <html>
            <body>
                <h2>Data list</h2>
                <table>
                    <tr>
                        <th>Title</th>
                        <th>Artist</th>
                    </tr>
                    <xsl:for-each select="list/item">
                        <tr>
                            <td><xsl:value-of select="name"/></td>
                            <td><xsl:value-of select="datum"/></td>
                        </tr>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>