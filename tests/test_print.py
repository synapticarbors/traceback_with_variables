import logging
from io import StringIO

import pytest

from traceback_with_variables.print import printing_tb, prints_tb, LoggerAsFile

from tests.utils import assert_smart_equals_ref, run_code


def test_printing_tb():
    out = StringIO()
    with printing_tb(reraise=False, file_=out, flush=True):
        f(10)

    assert_smart_equals_ref('test_print.printing_tb', out.getvalue())


def test_printing_tb_stderr(tmp_path):
    code = '''from traceback_with_variables import printing_tb
def f(n):
    return n / 0
    
def main():
    try:
        with printing_tb():
            return f(10)
    except:
        pass
         
main()'''

    assert_smart_equals_ref('test_print.printing_tb_stderr', run_code(tmp_path, [], code, [], False))


def test_printing_tb_reraise():
    out = StringIO()
    with pytest.raises(ZeroDivisionError):
        with printing_tb(reraise=True, file_=out):
            f(10)


def test_printing_tb_skip_cur_frame():
    out = StringIO()
    with printing_tb(reraise=False, file_=out, skip_cur_frame=True):
        f(10)

    assert_smart_equals_ref('test_print.printing_tb_skip_cur_frame', out.getvalue())


def test_prints_tb():
    out = StringIO()
    with pytest.raises(ZeroDivisionError):
        prints_tb(file_=out)(f)(10)

    assert_smart_equals_ref('test_print.prints_tb', out.getvalue())


def test_prints_tb_noncall(tmp_path):
    code = '''from traceback_with_variables import prints_tb
@prints_tb
def f(n):
    return n / 0
try:
    f(10)
except:
    pass'''

    assert_smart_equals_ref('test_print.prints_tb_noncall', run_code(tmp_path, [], code, [], False))


def test_logger_as_file(caplog):
    with printing_tb(reraise=False, file_=LoggerAsFile(logging.getLogger('test-logger'))):
        f(10)

    assert_smart_equals_ref('test_print.logger_as_file', caplog.text)


def f(n):
    return n / 0
