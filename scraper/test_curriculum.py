import pytest

from curriculum import lex_courselist
from test_resources import *


@pytest.mark.parametrize('tag,tokens', [
    (conc_laes_cgraph, conc_laes_cgraph_lexed),
    (qs_minor, qs_minor_lexed),
    (math_major, math_major_lexed),
    (math_ge, math_ge_lexed),
    (cs_major, cs_major_lexed)
])
def test_lex_courselist(tag, tokens):
    gen = lex_courselist(tag)
    actual = list(gen)
    assert actual == tokens
