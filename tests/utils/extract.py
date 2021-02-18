import re


def extract_blurb(output):
    blurb, _, _, _ = extract_blurb_method_payload_url(output)
    return blurb


def extract_blurb_method_payload_url(output):
    """
    Splits output so each part can be asserted individually.
    """
    other_lines = []
    payload_lines = []
    in_payload = False
    for line in output.splitlines(False):
        if line == "{" or line == "}" or in_payload:
            payload_lines.append(line)
            if line == "{":
                in_payload = True
            if line == "}":
                in_payload = False
        else:
            other_lines.append(line)
            in_payload = False

    import json
    payload = json.loads("".join(payload_lines))
    *blurb, method_line, to_url_line, _dry_run_line = other_lines
    method = method_line.split()[0]
    url = to_url_line.split()[-1]

    """
    URL_REGEX = re.compile(r'To this url: (?P<url>.*)')
    for line in other_lines:
        match = URL_REGEX.match(line)
        if match is not None:
            url = match.group('url')

    for line in other_lines:
        if line == 'Putting this payload:':
            method = 'Putting'
        if line == 'Posting this payload':
            method = 'Posting'
    """
    
    return blurb, method, payload, url
