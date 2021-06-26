import glob


def get_imports(filename, extension):
    with open(filename, "r") as file:
        code = file.read().split("\n")

    total_line_num = len(code)

    imports = {line_num + 1: line for line_num, line in enumerate(code) if extension in line}
    remaining_code_lines = {line_num + 1: line for line_num, line in enumerate(code) if extension not in line}

    return imports, remaining_code_lines, total_line_num

def parse_imports(filename, extension):
    imports, remaining_code_lines, total_line_num = get_imports(filename=filename, extension=extension)

    jinja_template_start = '<link href="{{ url_for(\'static\', filename=\''
    jinja_template_end = '\') }}" rel="stylesheet">'

    if extension == ".js":
        jinja_template_start = '<script src="{{ url_for(\'static\', filename=\''
        jinja_template_end = '\') }}" type="text/javascript"></script>'

    split_word = "href" if extension == ".css" else "src"

    for line_num, import_ in imports.items():
        file_path = import_.split(f"{split_word}=\"")[1].split("\"")[0]
        
        jinja_style_import = jinja_template_start + file_path + jinja_template_end
        
        imports[line_num] = jinja_style_import

    return imports, remaining_code_lines, total_line_num

def update_imports(filename):
    css_imports, remaining_code_lines, total_line_num = parse_imports(filename=filename, extension=".css")
    js_imports, remaining_code_lines, total_line_num = parse_imports(filename=filename, extension=".js")

    code = ""
    for i in range(total_line_num):
        if i+1 in css_imports.keys():
            code += css_imports[i+1] + "\n"
        elif i+1 in js_imports.keys():
            code += js_imports[i+1] + "\n"
        else:
            code += remaining_code_lines[i+1] + "\n"

    assert len(code.split("\n")[:-1]) == total_line_num, (len(code.split("\n")[:-1]), total_line_num)

    # modified_filename = filename.split(".")[0] + "-modified.html"
    modified_filename = filename
    with open(modified_filename, "w") as file:
        file.write(code)

if __name__ == "__main__":
    filenames = glob.glob("templates/*.html")
    filenames = [filename for filename in filenames if "-modified.html" not in filename]
    
    for filename in filenames:
        update_imports(filename=filename)