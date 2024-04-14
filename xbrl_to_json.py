# https://py-xbrl.readthedocs.io/en/latest/usage.html#online

import logging
from xbrl.cache import HttpCache
from xbrl.instance import XbrlParser, XbrlInstance
# just to see which files are downloaded
logging.basicConfig(level=logging.INFO)

cache: HttpCache = HttpCache('./cache')
cache.set_headers({'From': 'service@street-smart.ai', 'User-Agent': 'py-xbrl/2.1.0'})
parser = XbrlParser(cache)

chtr_schema_url = "https://www.sec.gov/Archives/edgar/data/1091667/000109166724000028/chtr-20231231.htm"
chtr_output_json = "chtr-20231231.json"

para_schema_url = "https://www.sec.gov/Archives/edgar/data/813828/000081382824000007/para-20231231.htm"
para_output_json = "para-20231231.json"

t_schema_url = "https://www.sec.gov/Archives/edgar/data/732717/000073271724000009/t-20231231.htm"
t_output_json = "t-20231231.json"

tmus_schema_url = "https://www.sec.gov/Archives/edgar/data/1283699/000128369924000008/tmus-20231231.htm"
tmus_output_json = "tmus-20231231.json"

vz_schema_url = "https://www.sec.gov/Archives/edgar/data/732712/000073271224000010/vz-20231231.htm"
vz_output_json = "vz-20231231.json"

schema_url = para_schema_url
output_json = para_output_json
inst: XbrlInstance = parser.parse_instance(schema_url)

inst.json('./json/' + output_json)