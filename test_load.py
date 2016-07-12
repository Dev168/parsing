from bookmakers.Sbobet import Sbobet
from bookmakers.Marathonbet import Marathonbet

sb = Sbobet()
m = Marathonbet()

sbf = sb.get_scraping_urls()
mf = m.get_scraping_urls()

for f in sbf:
    sb.download_events(f)

for f in mf:
    m.download_events(f)

