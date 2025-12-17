def generate_table(data):
    return "\n".join((
        f"\\begin{{tabular}}{{|{'|'.join(['c'] * len(data[0]))}|}}",
        "\\hline",
        "\n".join(map(lambda row: f"{' & '.join(map(str, row))} \\\\ \\hline", data)),
        "\\end{tabular}"
    )) if data else ""

def generate_image(filepath, width="0.5\\textwidth"):
    return f"\\includegraphics[width={width}]{{{filepath}}}"

def generate_document(content):
    return "\n".join((
        "\\documentclass{article}",
        "\\usepackage{graphicx}",
        "\\begin{document}",
        content,
        "\\end{document}"
    ))
