from os import path
from app.logic.snp500 import _do_parse_snp500_wiki_html
from app.models import Snp500

MOCKS_DIR = path.realpath(path.join(__file__, '../mocks'))

app = None

def test_wiki_snp500_html_parse():
    """
    dirt
    """
    from app import app
    global app
    app.app_context().push()

    mock_realpath = path.join(MOCKS_DIR, 'snp500-raw.html')
    with open(mock_realpath, 'r') as f:
        html = f.read()
        res = _do_parse_snp500_wiki_html(html)
        assert type(res) == dict
        print(res)