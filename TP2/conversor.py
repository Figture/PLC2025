import re, sys

md_text = """# Título Principal

## Subtítulo Secundário

### Sub-subtítulo

Este é um **texto em negrito**, e este é um *texto em itálico*.  
Também podemos misturar: **um *exemplo* combinado**.  

Aqui está uma lista numerada:

1. Primeiro item
2. Segundo item
3. Terceiro item

Podemos ainda inserir um link: [página da UC](http://www.uc.pt).  

E até imagens!  
![imagem dum coelho](http://www.coellho.com)  
"""


def conversor(md_text):
    header1=re.compile(r'^#\s+(.+)',re.MULTILINE)
    header2=re.compile(r'^##\s+(.+)',re.MULTILINE)
    header3=re.compile(r'^###\s+(.+)',re.MULTILINE)

    bold=re.compile(r'\*\*(.+)\*\*')
    italic=re.compile(r'\*(.+)\*')
    

    numList=re.compile(r'^\d+\.\s+(.+)',re.MULTILINE)
    pattern = re.compile(r'(<li>.*</li>)', re.DOTALL)

    link=re.compile(r'\[(.+)\]\((.*)\)')
   

    image=re.compile(r'.*\!\[(.+)\]\((.*)\)')
    

    md_text=re.sub(header1,r'<h1>\1</h1>',md_text)
    md_text=re.sub(header2,r'<h2>\1</h2>',md_text)
    md_text=re.sub(header3,r'<h3>\1</h3>',md_text)
    md_text=re.sub(bold,r'<b>\1</b>',md_text)
    md_text=re.sub(italic,r'<i>\1</i>',md_text)

    md_text=re.sub(numList,r'<li>\1</li>',md_text)
    md_text=re.sub(pattern,r'<ol>\n\1\n</ol>',md_text)

    md_text=re.sub(image,r'<img src="\2" alt="\1"/>',md_text)
    md_text=re.sub(link,r'<a href="\2">\1</a>',md_text)
    

    return md_text
text=conversor(md_text)
print(text)