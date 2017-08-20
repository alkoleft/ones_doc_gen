import re


def text_indents(text):
    indents = []
    prev_indent = None

    for match in re.finditer(r'^([ \t]*)(\S?)', text, re.MULTILINE):
        indent = match.regs[1][1] - match.regs[1][0]
        indent = {
            'indent': indent,
            'isEmpty': indent == (match.regs[0][1] - match.regs[0][0]),
            'start': match.regs[0][0]
        }
        if prev_indent is None \
                or indent['isEmpty'] != prev_indent['isEmpty'] \
                or indent['indent'] != prev_indent['indent']:
            if not prev_indent is None:
                prev_indent['end'] = indent['start']
            prev_indent = indent
            indents.append(indent)
    if not prev_indent is None:
        prev_indent['end'] = len(text)

    return indents


def clear_indent(text, indent=None):
    if indent is None:
        match = re.search(r'^\s+', text, re.MULTILINE)

        if match is None:
            return text
        indent = match.regs[0][1] - match.regs[0][0]

    return re.sub(r'^\s{%d}' % indent, '', text, 0, re.MULTILINE)
