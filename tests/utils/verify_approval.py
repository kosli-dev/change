from approvaltests.approvals import verify
from approvaltests.reporters import PythonNativeReporter


"""
According to https://github.com/approvals/ApprovalTests.Python
you can setup the approval-test reporter at the command line 
like this:

    pytest --approvaltests-use-reporter='PythonNative' ...

Unfortunately this is currently broken with the latest release
of pytest-approvals. You get a DiffReporter. So, for now you have 
to specify the reporter individually on each verify() call. 
For example:

   from approvaltests.approvals import verify
   from approvaltests.reporters import PythonNativeReporter
   ...
   verify(actual, PythonNativeReporter())

If you don't do this you _lose_ output, eg for a new test the
name of the missing approval file does _not_ appear.

Emily Bache says "this problem should be fixed now in the 
0.2.0 release. note it also needs the updated approvaltests version 0.3.1"
A [pip list] command confirms we are using approvaltests 0.3.1 
But these two lines in requirements.txt do not yet work:
  git+git://github.com/approvals/ApprovalTests.Python.git@master#egg=approvaltests
  pytest-approvaltests==0.2.0 
"""


def verify_approval(capsys, streams=None):
    actual = full_capsys(capsys, streams)
    verify(actual, PythonNativeReporter())


def verify_payload_and_url(capsys, streams=None):
    actual = full_capsys(capsys, streams)
    payload_and_url = ""
    inside = False
    for line in actual.splitlines(True):
        inside = line.startswith("Putting this payload:") or inside
        inside = line.startswith("Posting this payload:") or inside
        if inside:
            payload_and_url += line
    verify(payload_and_url, PythonNativeReporter())


def full_capsys(capsys, streams=None):
    out, err = capsys.readouterr()
    if streams is None:
        streams = ["out", "err"]
    actual = ""
    for stream in streams:
        if stream == "out":
            actual += out
        if stream == "err":
            actual += err
    return actual


def blurb(output):
    blurb,_,_,_ = blurb_method_payload_url(output)
    return blurb


def blurb_method_payload_url(output):
    """
    Splits capsys output so each part can be asserted individually.
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
    return blurb, method, payload, url
