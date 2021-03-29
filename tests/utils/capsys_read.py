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
  
  
Update. This was fixed in the 0.3.0 release.  
"""


def capsys_read(capsys, streams=None):
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
