from bookmakers.Sbobet import Sbobet
from bookmakers.Marathonbet import Marathonbet

sbf = ["sb_football.html", "sb_tenis.html"]
mf = ["m_tenis.html", "m_football.html"]
sb = Sbobet()
m = Marathonbet()

for f in sbf:
    with open(f, encoding="utf8") as fa:
        sb.download_events(fa.read())

for f in mf:
    with open(f, encoding="utf8") as fa:
        m.download_events(fa.read())

