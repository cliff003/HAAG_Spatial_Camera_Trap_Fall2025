# Data Cleaning Report

Generated: 2026-04-15 23:49:47

## Raw data
- SSUSA sequences: 987,979 rows
- SSUSA deployments: 9,679 rows
- IUCN polygons (after bbox load): 767 (580 species)
- IUCN polygons (after filter + exclusion): 733 (575 species)
- COMBINE ([Soria et al. 2021](https://doi.org/10.1002/ecy.3344)): 5,961 species, 5,744 with body mass

## SSUSA cleaning waterfall
| Stage | Rows |
|---|---|
| raw sequences | 987,979 |
| after dropna on taxonomy | 891,947 |
| after Class == mammalia | 863,436 |
| after merge with deployments | 857,003 |
| after dedup | 857,003 |
| after exclusion lists | 713,319 |

## IUCN bbox (computed from SSUSA footprint)
```
minx, miny, maxx, maxy = (-158.74962, 20.355811, -67.61159314, 60.452635)
padding = 1.0 degrees
```

## Taxonomy reconciliation
- Total unique species across all three sources: **5982**
- Present in all three sources: **110**
- In SSUSA but not IUCN (20 species):

- bos taurus
- boselaphus tragocamelus
- canis lupus familiaris
- capra hircus
- castor canadensis
- equus asinus
- equus caballus
- felis catus
- homo sapiens
- lama glama
- lariscus insignis
- lontra canadensis
- neogale vison
- ondatra zibethicus
- oryx gazella
- ovis aries
- rattus rattus
- sus scrofa
- urva javanica
- zalophus californianus

- In SSUSA but missing body mass (10 species):

- bos taurus
- canis lupus familiaris
- capra hircus
- equus asinus
- equus caballus
- felis catus
- homo sapiens
- lama glama
- ovis aries
- urva javanica

- Synonyms applied (9):

- `mustela frenata` -> `neogale frenata`
- `myodes gapperi` -> `clethrionomys gapperi`
- `neovison vison` -> `neogale vison`
- `pekania pennanti` -> `martes pennanti`
- `arizona black-tailed prairie dog` -> `black-tailed prairie dog`
- `canis familiaris` -> `canis lupus familiaris`
- `capra aegagrus hircus` -> `capra hircus`
- `cervus canadensis` -> `cervus elaphus`
- `sus scrofa scrofa` -> `sus scrofa`


## Exclusion tallies
### SSUSA records dropped
| List | Records |
|---|---|
| SEMI_AQUATIC_MARINE | 1,510 |
| DOMESTIC_SPECIES | 57,370 |
| NON_NATIVE_EXOTICS | 279 |
| HUMANS | 84,525 |

### IUCN polygons dropped
| List | Polygons |
|---|---|
| SEMI_AQUATIC_MARINE | 0 |
| DOMESTIC_SPECIES | 2 |
| NON_NATIVE_EXOTICS | 0 |
| HUMANS | 0 |

## Scope-flagged species (retained, not excluded)
- `bison bison` -> managed_population


## Cleaned outputs
- `ssusa_cleaned.csv`: **713,319 rows**, 29 columns, 109 species
- `iucn_cleaned.shp`: **733 polygons**, 27 attribute columns, 575 species

## Body-mass threshold summary
- Threshold: **500 g**
- SSUSA records: 713,319
- Records above threshold: 673,198
- Records below threshold: 40,121
