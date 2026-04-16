# 🐾 Project HAAG Spatial Cameratrap
HAAG OMSCS Fall 2025  
- [About HAAG](https://sites.gatech.edu/human-augmented-analytics-group/)
- [Project Wiki](https://humanaugmentedanalyticsgroup.miraheze.org/wiki/Project-haag-spatial-cameratrap)

## 📌 Overview
Welcome to **HAAG Spatial Cameratrap**. This repository contains everything you need to know about the project, along with links to important resources and contributors.

## ✍️ Project Description
The team is investigating how **spatial scaling and averaging** influence the apparent composition of **terrestrial mammal** communities captured through camera trap data.

**Data sources**:
- [Snapshot USA](https://datadryad.org/dataset/doi:10.5061/dryad.k0p2ngfhn#methods) — a multi-institutional camera trap survey across the United States (2019–2024).
- [IUCN Red List Spatial Data](https://www.iucnredlist.org/resources/spatial-data-download#mammals) — terrestrial mammal range map polygons.
- [COMBINE: a coalesced mammal database of intrinsic and extrinsic traits](https://doi.org/10.1002/ecy.3344) (Soria et al. 2021, *Ecology*) — functional traits for 6,110 terrestrial mammal species (replaces PanTHERIA).

## 🎯 Goals

### Completed
- ✅ Download and clean **SnapShot USA** data — *Summer 2025, refined Fall 2025, rebuilt Spring 2026*
- ✅ Compile species that comprise individual "communities" by:
  - ✅ Using single-site data in **1-year** and **multi-year** intervals — *Summer 2025*
  - ✅ Spatially clustering cameras within **50 km** and aggregating data across all years — *Summer 2025, Agglomerative Clustering*
- ✅ Compare the **compositions of these communities** — *Summer 2025, Jaccard Index & Shannon Diversity*
- ✅ Compare communities from camera trap data with communities derived from **IUCN range maps** — *Summer 2025 initial, Fall 2025 full spatial comparison*
- ✅ Build a **parameterized cleaning pipeline** combining SSUSA + IUCN + COMBINE traits — *Spring 2026*
- ✅ Replace PanTHERIA with **COMBINE** as the trait source, closing the 34% body-mass coverage gap — *Spring 2026*
- ✅ **SAC analysis** at body-mass thresholds (50, 100, 500, 1000 g) via `vegan::specaccum` — *Spring 2026*

### In Progress (Spring 2026)
- 🔄 Classify array-year sampling quality using **SAC + Poisson CI gap** method
- 🔄 Compare **IUCN expected species** with **SSUSA observed species** to quantify detection bias at each mass threshold

---

## 🧪 Current Primary Pipeline (Spring 2026)

The canonical workflow lives at the repo root and produces a single set of cleaned artifacts that all downstream analyses consume.

### Notebooks

| Notebook | Role |
|---|---|
| [`data_cleaning.ipynb`](data_cleaning.ipynb) | **Primary cleaning pipeline.** Ingests raw SSUSA + IUCN + COMBINE, applies taxonomy normalization and synonym mapping, drops domestic/exotic/semi-aquatic/human records, merges body mass, writes canonical outputs and an auto-generated markdown report. All tunable parameters (paths, thresholds, exclusion lists, scope flags) live in Cell 2. |
| [`SAC_Combine_MassThresholds.ipynb`](SAC_Combine_MassThresholds.ipynb) | Species accumulation curves (SSUSA vs IUCN) at body-mass thresholds of 50 / 100 / 500 / 1000 g. Consumes the cleaned outputs. Uses R `vegan::specaccum` via `rpy2`. |
| [`DataCleaning_old.ipynb`](DataCleaning_old.ipynb) | Previous cleaning notebook — kept as historical reference. Superseded by `data_cleaning.ipynb`. |

### Cleaned Outputs (`cleaned/`)

| File | Contents |
|---|---|
| `ssusa_cleaned.csv` | ~713K SSUSA records × 29 cols (109 species), Pascal_Case. Includes `Species_Name` (normalized binomial), `Body_Mass_g`, `Above_Threshold`, `Scope_Flag`. |
| `iucn_cleaned.shp` (+ .dbf/.shx/.prj/.cpg) | ~733 IUCN polygons × 27 attribute cols (575 species). Includes `sci_name`, `body_mass`, `ab_thres`, `scope_flag`. Wide attribute retention (not just species+geometry). |
| `data_cleaning_report.md` | Auto-generated summary: waterfall, IUCN bbox, taxonomy reconciliation, exclusion tallies, body-mass threshold counts. |

### Key Design Decisions

- **IUCN bbox is derived from SSUSA footprint** (not hard-coded CONUS) so Alaska + Hawaii deployments are covered.
- **IUCN filter:** `presence=1` (extant), `origin ∈ {1,2,3}` (native, reintroduced, introduced), `seasonal ∈ {1,2}` (resident, breeding). Includes reintroduced to capture endangered species (e.g. black-footed ferret, red wolf).
- **Exclusions** split into separate audited lists: `SEMI_AQUATIC_MARINE`, `DOMESTIC_SPECIES`, `NON_NATIVE_EXOTICS`, `HUMANS`.
- **Trait source is swappable.** COMBINE is loaded in Section 1c only; changing `TRAIT_PATH` and the Section 1c loader is all it takes to plug in a different trait database.

---

## 📂 Archive — 2025 Work

All prior work from Summer and Fall 2025 is stored in `Archive/`. Below is a summary of each module.

### 1. EDA & Data Cleaning (`Summer2025/EDA_and_data_cleaning/`)

| Notebook | Description |
|----------|-------------|
| `EDA.ipynb` | Comprehensive exploratory data analysis — univariate histograms, bivariate scatterplots, correlation heatmaps, spatial distribution maps, and temporal trends. |
| `EDA_Taxonomy.ipynb` | Explores taxonomic breakdown (Mammalia vs. Aves, etc.), visualizes class distributions over years, and filters the dataset to mammals only. |
| `DataCleaning.ipynb` | Merges sequences and deployments CSVs, drops rows with missing taxonomy, normalizes text to lowercase, handles missing Age/Sex/Group_Size, and exports a cleaned CSV. |
| `Deduplication.ipynb` | Identifies potential duplicate detections — same species at the same deployment within short time windows (1–60 min). Exports candidates for manual review. |

### 2. Defining Communities & Clustering (`Summer2025/Define_communities/`)

| Notebook | Description |
|----------|-------------|
| `Clustering.ipynb` | Early exploration of KMeans (k = 2–20) with elbow/silhouette plots to find optimal k. |
| `Clustering2.ipynb` | Side-by-side comparison of KMeans (k = 100), Agglomerative (50 km threshold), and DBSCAN (50 km haversine). Includes cluster-size distributions. |
| `Clustering_DBSCAN.ipynb` | DBSCAN clustering with 50 km haversine threshold. Computes centroids and maps deployments vs. centroids. |
| `Clustering_final.ipynb` | End-to-end pipeline: load → clean → merge → filter to Mammalia → Agglomerative Clustering (50 km distance threshold). |
| `Clustering_final_revised.ipynb` | Revised version of the final pipeline with improved data loading (dtype specs, NA handling). |
| `Clustering_vizualization.ipynb` | Maps clusters with basemaps, plots centroids, and reassigns small clusters (< 5 points) to the nearest large cluster. |
| `ClusteringValidate.ipynb` | Validates clustering by computing each deployment's haversine distance to its cluster centroid; generates summary stats and spatial maps. |
| `Species_List_Cluster.ipynb` | Generates per-cluster and per-cluster-year species lists. Creates one-hot presence/absence matrices and exports CSVs to `Species_List_Cluster/`. |

### 3. Analysis (`Summer2025/Analysis/`)

| Notebook | Description |
|----------|-------------|
| `Jaccard_Index.ipynb` | Computes Jaccard similarity in two directions: **species movement** (stability of a species' cluster membership across years) and **location stability** (stability of a cluster's species composition across years). |
| `Jaccard_Index_Revised.ipynb` | Revised Jaccard analysis — filters to clusters with ≥ 5 years of data, adds heatmaps and animated GIF maps. |
| `Richness_Shannon_Index.ipynb` | Calculates species richness and Shannon diversity index per array per year. Produces animated Cartopy maps across 2019–2023 plus aggregated 5-year metrics. |
| `OccupancyModel.ipynb` | Bayesian single-season occupancy model for a focal species (brown bear) using PyMC. Estimates occupancy (ψ) and detection (p) probabilities, then adds environmental covariates. |

### 4. Proximity Analysis (`Summer2025/ProximityAnalysis/`)

| Notebook | Description |
|----------|-------------|
| `Camera_Trap_Sites_5Km.ipynb` | Groups deployments by array and computes pairwise geodesic distances. Filters to sites within 5 km of each other, calculates array centroids. |
| `Camera_Trap_5Km_Full_Data.ipynb` | Identifies arrays with complete data across consecutive year spans (2–5 years from 2019). Exports arrays meeting each temporal coverage level. |
| `Camera_Trap_Species_List.ipynb` | Creates per-array, per-year species lists using the 5 km filtered data, includes habitat types and coordinates. |
| `Camera_Trap_Species_Richness.ipynb` | Calculates species richness per array across individual years, 3-year, and 5-year windows using proximity data. |
| `Species_List_Presence_Absence.ipynb` | Generates a one-hot presence/absence matrix (~130 species) per array-year. Identifies focal species present at > 100 sites. |

### 5. IUCN Range Map Comparison (`Summer2025/`)

| Notebook | Description |
|----------|-------------|
| `IUCN.ipynb` | Compares Snapshot USA observations against IUCN range maps. Buffers cluster centroids by 50 km and performs spatial intersection with IUCN polygons to identify range overlaps. |

### 6. IUCN & SAC — Fall 2025 (`Fall 2025/`)

| File | Description |
|------|-------------|
| `Accumulation_R.ipynb` | R-based SAC analysis — predecessor to the Python SAC notebooks. Uses R `vegan::specaccum` with Michaelis-Menten/Clench NLS fit for sampling completeness. |
| `IUCN_SSUSA_comparison_and_HTML_map/SSUSA_IUCN_comparison.ipynb` | Compares SSUSA detections against IUCN range polygons via spatial point-in-polygon tests. Identifies species detected outside expected ranges and computes distances to nearest polygon boundary. |
| `IUCN_SSUSA_comparison_and_HTML_map/OutsideSSUSA_vs_IUCN_html_tool.py` | Generates an interactive Folium HTML map showing detections outside IUCN ranges, with per-species toggleable layers, search, and measurement tools. |

### 7. Output Data (`Summer2025/Species_List_Cluster/`)

| File | Description |
|------|-------------|
| `species_cluster_table.csv` | Species lists per cluster |
| `species_cluster_onehot_table.csv` | One-hot encoded species × cluster matrix |
| `species_list_cluster_df.csv` | Cluster-level species list dataframe |
| `species_list_cluster_one_hot.csv` | One-hot species presence per cluster |
| `species_year_cluster_table.csv` | Species lists per cluster per year |
| `species_year_cluster_onehot_table.csv` | One-hot species × cluster-year matrix |
| `species_list_cluster_year_df.csv` | Cluster-year species list dataframe |
| `species_list_cluster_year_one_hot.csv` | One-hot species presence per cluster-year |

---

## 👥 Contributors
| Name            | Email                        |
|-----------------|------------------------------|
| Jacquie Carroll | <jacq@udel.edu>              |
| Kefei Yan       | <kyan66@gatech.edu>          |
| Neelima Pandey  | <nsrivastava44@gatech.edu>   |
| John Hiedo      | <jhiedo3@gatech.edu>         |

##  Built With
[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![R](https://img.shields.io/badge/R-4.x-blue?logo=r&logoColor=white)](https://www.r-project.org/)

**Core dependencies:** `pandas`, `geopandas`, `rpy2` (+ R `vegan`), `matplotlib`. The data-cleaning notebook runs on any generic `python3` Jupyter kernel; the SAC notebook requires an R-enabled kernel with `vegan` installed.

![Visitors](https://img.shields.io/badge/visitors-∞-blue?style=flat-square&logo=github)

------------------------

