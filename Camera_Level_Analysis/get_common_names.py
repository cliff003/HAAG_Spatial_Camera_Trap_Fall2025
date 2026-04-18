import time
import requests

ITIS_BASE = "https://www.itis.gov/ITISWebService/jsonservice"
INAT_BASE = "https://api.inaturalist.org/v1"

def get_common_names(species_list):
    result = {}

    for sci in species_list:
        sci = str(sci).strip().lower()
        common = None

        if not sci:
            result[sci] = None
            continue

        try:
            r = requests.get(f"{ITIS_BASE}/searchByScientificName",
                             params={"srchKey": sci}, timeout=10)
            candidates = r.json().get("scientificNames", [])

            tsn = None
            for c in candidates:
                if (c.get("combinedName") or "").lower() == sci:
                    tsn = c.get("tsn")
                    break
            if not tsn and candidates:
                tsn = candidates[0].get("tsn")

            if tsn:
                r2 = requests.get(f"{ITIS_BASE}/getCommonNamesFromTSN",
                                  params={"tsn": tsn}, timeout=10)
                names = r2.json().get("commonNames", [])

                for n in names:
                    if "english" in (n.get("language") or "").lower():
                        common = n.get("commonName")
                        break

                if not common and names:
                    common = names[0].get("commonName")

        except:
            pass

        time.sleep(0.2)

        if not common:
            try:
                r = requests.get(f"{INAT_BASE}/taxa",
                                 params={"q": sci, "rank": "species", "per_page": 1},
                                 timeout=10)
                results = r.json().get("results", [])
                if results:
                    common = results[0].get("preferred_common_name")
            except:
                pass

            time.sleep(1)

        result[sci] = common

    return result