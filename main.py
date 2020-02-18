import requests
import re
import json
from dataclasses import dataclass


@dataclass
class Provincia:
  nome_centralina: str
  comune: str
  provincia: str
  valore: float
  superamenti_pm10: float


def parser(text):
  all_data = []
  for x in text.split("\n"):
    if not re.match("[^;]+;[^;]+;[^;]*;[^;]*;([^;]+|;)", x) or "NomeCentralina" in x:
      continue

    parts = x.strip().split(";")[0:5]
    valore = parts[3].replace(",", ".")
    superamenti_pm10 = parts[4]

    all_data.append(Provincia(
      nome_centralina=parts[0],
      comune=parts[1],
      provincia=parts[2],
      valore=.0 if valore == "" else float(valore),
      superamenti_pm10=.0 if superamenti_pm10 == "" else float(superamenti_pm10),
    ))
  return all_data


def main():
  resp = requests.get("http://www.arpa.puglia.it/pentaho/ViewAction?solution=ARPAPUGLIA&path=portal/export&action=getCentraline_export_per_inquinante.xaction")
  data = parser(resp.text)
  with open("data.json", "w") as f:
    f.write(json.dumps(data, default=lambda x: x.__dict__, indent=2))


if __name__ == "__main__":
  main()
