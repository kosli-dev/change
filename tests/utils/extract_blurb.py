
def extract_blurb(output):
    other_lines = []
    in_payload = False
    for line in output.splitlines(False):
        if line == "{" or line == "}" or in_payload:
            if line == "{":
                in_payload = True
            if line == "}":
                in_payload = False
        else:
            other_lines.append(line)
            in_payload = False

    *blurb, _method_line, _to_url_line, _dry_run_line = other_lines
    return blurb
