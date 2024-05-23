# https://py-xbrl.readthedocs.io/en/latest/usage.html#online

import logging
from xbrl.cache import HttpCache
from xbrl.instance import XbrlParser, XbrlInstance
# just to see which files are downloaded
logging.basicConfig(level=logging.INFO)

cache: HttpCache = HttpCache('./cache')
#cache.set_headers({'From': 'service@street-smart.ai', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'})
cache.set_headers({'User-Agent': 'service@street-smart.ai'})

parser = XbrlParser(cache)

aapl_schema_url = "https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm"

amcx_schema_url = "https://www.sec.gov/Archives/edgar/data/1514991/000151499124000007/amcx-20231231.htm"

chtr_schema_url = "https://www.sec.gov/Archives/edgar/data/1091667/000109166724000028/chtr-20231231.htm"

cmcsa_schema_url = "https://www.sec.gov/Archives/edgar/data/0001166691/000116669124000011/cmcsa-20231231.htm"

dis_schema_url = "https://www.sec.gov/Archives/edgar/data/1744489/000174448923000216/dis-20230930.htm"

msft_schema_url = "https://www.sec.gov/Archives/edgar/data/789019/000095017023035122/msft-20230630.htm"

nvda_schema_url = "https://www.sec.gov/Archives/edgar/data/1045810/000104581024000029/nvda-20240128.htm"

para_schema_url = "https://www.sec.gov/Archives/edgar/data/813828/000081382824000007/para-20231231.htm"

sats_schema_url = "https://www.sec.gov/Archives/edgar/data/1415404/000155837024002209/tmb-20231231x10k.htm"

t_schema_url = "https://www.sec.gov/Archives/edgar/data/732717/000073271724000009/t-20231231.htm"

tmus_schema_url = "https://www.sec.gov/Archives/edgar/data/1283699/000128369924000008/tmus-20231231.htm"

vz_schema_url = "https://www.sec.gov/Archives/edgar/data/732712/000073271224000010/vz-20231231.htm"

wbd_schema_url = "https://www.sec.gov/Archives/edgar/data/1437107/000143710724000017/wbd-20231231.htm"

schema_url = msft_schema_url
json_filename = schema_url.split("/")[-1:]
json_filename = json_filename[0].split(".")[0]
output_json = json_filename + ".json"
#print(json_file)

#output_json = para_output_json

inst: XbrlInstance = parser.parse_instance(schema_url)
inst.json('./json/' + output_json)

# get DocumentPeriodEndDate from json and append to end of filename
# then send it to json_to_dataframe via SQS