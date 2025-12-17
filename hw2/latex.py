from latex_gen_assignment import generate_table, generate_image, generate_document

import os, subprocess

if __name__ == "__main__":
    table_data = [
        ["Col 1", "Col 2"],
        [1, 2],
        [3, 4]
    ]

    table = generate_table(table_data)
    
    image = generate_image("artifacts/latex.png") 

    content = f"{table}\n\n\\vspace{{1cm}}\n\n{image}"
    document = generate_document(content)

    tex_filename = "artifacts/pdfdoc.tex"
    with open(tex_filename, "w") as f:
        f.write(document)   

    subprocess.run(["pdflatex", tex_filename], check=True)

    for ext in [".aux", ".log", ".tex"]:
        if os.path.exists("pdfdoc" + ext):
            os.remove("pdfdoc" + ext)
