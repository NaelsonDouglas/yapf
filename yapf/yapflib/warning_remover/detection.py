import sys
import io
import json
from pylint.reporters.text import TextReporter
import parse

class DummyWritable():
    def __init__(self):
        self.content = []

    def write(self, stream):
        self.content.append(stream)

    def read(self):
        return self.content

def execute(filename:str, args:list=None) -> list:
    if not args:
        args = []
    _cmd = [filename]+args
    pylint_output = DummyWritable()
    old_stdout = sys.stdout #Hacking the stdout because pylint Run does not work properly when using the json output format
    sys.stdout = buffer = io.StringIO()
    lint.Run(_cmd, reporter=TextReporter(pylint_output), exit=False)
    sys.stdout = old_stdout
    result = json.loads(buffer.getvalue())
    return result
