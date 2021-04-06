import re


def compound_para(nodes, text):
    # https://docutils.sourceforge.io/docs/ref/doctree.html
    """
    Expands :code:`words here` rst syntax embedded inside living documentation text.
    """
    para = nodes.paragraph(text="")
    regex = re.compile(r':code:`(?P<content>.*?)`')
    for part in re.split(r'(:code:`.*?`)', text):
        match = regex.match(part)
        if match is None:
            div = nodes.inline(text=part)
        else:
            div = nodes.inline(text=match.group('content'))
            div.update_basic_atts({"classes": ['inline-code']})
        para += div

    return para
