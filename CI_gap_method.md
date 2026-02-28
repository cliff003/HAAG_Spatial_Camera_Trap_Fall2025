# CI Gap Method: What We Have and How It Works

## Overview

The CI gap method was developed by Dr. Steven Mussmann (Georgia Tech). It answers a simple question: **given what we observed at a camera trap array, how many regularly visiting species might we have missed?**

This document walks through (1) what data from Snapshot USA feeds into the method, (2) how Dr. Mussmann's code processes it, and (3) what comes out.

---

## 1. Inputs — What Comes from Snapshot USA

The method requires **three numbers per array-year**. All three are derived from the Snapshot USA dataset (2019–2023). Each camera trap array in each year of operation is treated as an independent sampling unit ("array-year").

### 1a. Observed richness ($m$)

- **What it is:** The count of unique species detected at an array **in a given year**.
- **Where it comes from:** Snapshot USA species detection records, filtered through IUCN range maps so that only species whose ranges overlap the array location are considered "detectable."
- **Unit:** Per array-year. An array with 5 years of data yields 5 separate $m$ values.
- **Example:** An array in Virginia detects 12 mammal species in 2022 → $m = 12$.

### 1b. Sampling effort ($t$)

- **What it is:** The total number of survey nights the array was operational **in a given year**.
- **Where it comes from:** Snapshot USA deployment records (camera start and end dates).
- **Unit:** Per array-year. Effort is computed separately for each year an array was active.
- **Critical note — effort definition matters.** We evaluated three definitions:
  - **Camera-nights** = sum of each individual camera's active nights. If 5 cameras each run 30 nights, that's 150 camera-nights. This **inflates** effort ~10× and makes CI gaps collapse to zero — every array gets gap = 0, losing all discriminating power. **Rejected.**
  - **Calendar-nights** = count of unique calendar days on which at least one camera was active. Same scenario = 30 calendar-nights. **This is the metric we use.** It avoids inflation while capturing full temporal coverage, and does not penalize arrays that rotated cameras sequentially.
  - **Majority-nights** = count of unique calendar days on which >50% of cameras were active simultaneously. This is the strictest metric but produces $t = 0$ for arrays with sequential camera deployments (no temporal overlap), making those array-years unanalyzable. **Rejected.**
- **Why it matters:** The CI gap calculation uses $t$ in an exponential ($e^{-t/t_0}$). Using camera-nights (mean ~624) instead of calendar-nights (mean ~59) inflates $t$ by ~10×, making the miss probability nearly zero and hiding real sampling problems.

### 1c. Inter-visit threshold ($t_0$)

- **What it is:** A user-chosen parameter defining what "regularly visiting" means. A species with mean inter-visit interval of $t_0$ nights is the target.
- **Not from the data** — this is a researcher decision.
- **Our choice: $t_0 = 14$ days** (biweekly visitors). This was selected via sensitivity analysis (see Section 7).
- **Example values tested:**
  - $t_0 = 7$ → targets species visiting about once a week. Too conservative: 55.8% of array-years classified as Type D (insufficient), minimal Type B/C.
  - $t_0 = 14$ → targets species visiting about once every two weeks. **Our primary choice.** Keeps false-plateau risk (Type C) at 4.4% while retaining 39.6% adequate array-years.
  - $t_0 = 30$ → targets species visiting about once a month. Type C rises to 37.2% — the CI gap loses ability to detect false plateaus.
  - $t_0 = 90$ → targets species visiting about once a season. Type C at 44.0% — method becomes insensitive.

---

## 2. The Method — What Dr. Mussmann's Code Does

### Step 1: Calculate the miss probability

Given effort $t$ and threshold $t_0$, compute the probability that a single regularly visiting species goes completely undetected:

$$
p_0 = \exp\!\left(-\,\frac{t}{t_0}\right)
$$

**Intuition:** If an array ran for $t = 56$ calendar-nights in one year and we set $t_0 = 14$, then $t/t_0 = 4$ expected visits. The chance of zero detections from a Poisson process with mean 4 is $e^{-4} \approx 0.018$ — a 1.8% miss rate per species.

### Step 2: Frame it as a Binomial problem

Suppose the true number of regularly visiting species is $k$. Each one is independently detected with probability $1 - p_0$. So the number of species we actually observe, $S$, follows:

$$
S \sim \text{Binomial}(k,\; 1 - p_0)
$$

We observed $m$ species. The question becomes: **how large could $k$ be while still being consistent with seeing only $m$?**

### Step 3: Find the upper bound on true richness

The code tests increasing values of $k$ starting from $m$ and asks: "If there were really $k$ species, what's the probability we'd see $m$ or fewer?"

$$
\Pr(S \leq m \mid k) = \sum_{i=0}^{m} \binom{k}{i} (1 - p_0)^{i}\, p_0^{\,k-i}
$$

It keeps increasing $k$ until this probability drops below $\delta = 0.05$. The last $k$ that passes is $\hat{k}_{\max}$.

**In plain language:** $\hat{k}_{\max}$ is the most species that could plausibly be out there, given what we saw and how long we looked, at 95% confidence.

### Step 4: Compute the CI gap

$$
\text{CI gap} = \hat{k}_{\max} - m
$$

This is the **maximum number of species we might have missed**.

---

## 3. Outputs — What Comes Out Per Array-Year

For each array-year in the Snapshot USA dataset, the code produces:

| Output | Description | Example |
|--------|-------------|----------|
| $m$ | Species observed (in that year) | 12 |
| $t$ | Calendar-nights of effort (in that year) | 56 |
| $\hat{k}_{\max}$ | Upper bound on true richness (95%) | 14 |
| **CI gap** | $\hat{k}_{\max} - m$ = missed species bound | 2 |

### What the CI gap tells us

| CI gap value | Meaning |
|-------------|---------|
| **0** | We're confident we caught everything (at the $t_0$ threshold). No regularly visiting species were likely missed. |
| **1–3** | Minor uncertainty. Maybe 1–3 species slipped through. Sampling is probably adequate. |
| **Large** (e.g., 10+) | Big problem. Many species could be out there undetected. The array didn't run long enough to be confident. |

---

## 4. Worked Example

**Array X in North Carolina, 2022:**
- Detected 8 species that year ($m = 8$)
- Ran for 45 calendar-nights in 2022 ($t = 45$)
- Using $t_0 = 14$ (biweekly visitors)

**Step 1:** $p_0 = e^{-45/14} = e^{-3.21} \approx 0.040$ — each target species has a 4.0% chance of being missed entirely.

**Step 2–3:** The code asks: if $k = 8$, is seeing 8 plausible? Yes (trivially). If $k = 9$? Check $\Pr(S \leq 8 \mid k=9)$. Keep going until the probability drops below 0.05.

Suppose $\hat{k}_{\max} = 9$.

**Step 4:** CI gap $= 9 - 8 = 1$. At most 1 regularly visiting species might have been missed. This array-year is classified as **Type A** (adequate) since SAC completeness is also high.

---

## 5. How This Connects to SAC Completeness

We pair the CI gap with SAC completeness to classify each array-year:

| | CI gap ≤ 2 (confident) | CI gap > 2 (uncertain) |
|---|---|---|
| **SAC ≥ 90%** | **Type A** — Genuinely well-sampled. Both metrics agree. | **Type C** — False plateau. SAC looks good but we can't trust it. |
| **SAC < 90%** | **Type D** — Low estimated richness but the bound is tight. Unusual case. | **Type B** — Clearly undersampled. Both metrics agree. |

Thresholds: SAC completeness ≥ 90% (from Michaelis-Menten model, $m / V_m$) and CI gap ≤ 2 species.

**Type C is the key finding.** These are the arrays where SAC alone would say "you're done sampling" but the CI gap says "you might be missing a lot." That's exactly the problem the dual-metric approach catches.

---

## 6. Computation Details

- **Algorithm:** Exact enumeration (no approximation). Loop $k = m, m+1, m+2, \ldots$ and evaluate the cumulative binomial CDF at each step. Stop when $\Pr(S \leq m \mid k) < 0.05$.
- **Speed:** Negligible per array. The full Snapshot USA dataset processes in seconds.
- **Confidence level:** $\delta = 0.05$ (95% confidence) throughout.
- **Code location:** Implemented in `SAC/SAC array CI.ipynb`.

---

## 7. Choosing $t_0$: Sensitivity Analysis and Final Decision

We swept $t_0$ from 7 to 120 days and classified all 570 valid array-years into Types A/B/C/D at each value (using calendar-nights as effort).

### Sensitivity results

| $t_0$ | Type A (adequate) | Type B (undersampled) | Type C (false plateau) | Type D (insufficient) |
|---:|---:|---:|---:|---:|
| 7 | 250 (43.9%) | 1 (0.2%) | 1 (0.2%) | 318 (55.8%) |
| **14** | **226 (39.6%)** | **49 (8.6%)** | **25 (4.4%)** | **270 (47.4%)** |
| 30 | 39 (6.8%) | 283 (49.6%) | 212 (37.2%) | 36 (6.3%) |
| 60 | 0 (0%) | 319 (56.0%) | 251 (44.0%) | 0 (0%) |
| 90 | 0 (0%) | 319 (56.0%) | 251 (44.0%) | 0 (0%) |

### Selection criterion

We chose the smallest $t_0$ where **Type C (false plateau) stays below 5%** of array-years, while maintaining a healthy proportion of Type A (adequate) classifications. The goal is to minimize false plateaus — the most dangerous misclassification — without being so conservative that most arrays become Type D.

### Decision: $t_0 = 14$ days

- **Type C = 4.4%** — below the 5% safety threshold. Only 25 out of 570 array-years are false plateaus.
- **Type A = 39.6%** — 226 array-years are confidently well-sampled.
- **Ecological interpretation:** A "regularly visiting" species is one expected to visit the array area at least once every 14 days. This is ecologically reasonable for medium-to-large mammals at Snapshot USA camera trap arrays.
- **Why not $t_0 = 7$?** Too conservative — 55.8% Type D, meaning the method flags most arrays as insufficient even when they have decent coverage.
- **Why not $t_0 = 30$?** Type C explodes to 37.2%. The CI gap method becomes insensitive — it tells you "sampling is adequate" even when the SAC hasn't plateaued.

---

## 8. Final Results Summary

**Parameters used:**
- Effort metric: **Calendar-nights** (unique days with ≥1 camera active per array-year)
- Visitation threshold: **$t_0 = 14$ days**
- Unit of analysis: **Array-year** (each array in each year treated independently)
- SAC threshold: **90%** completeness ($m / V_m$ from Michaelis-Menten model)
- CI gap threshold: **≤ 2 species**

**Classification of 570 valid array-years:**

| Type | Count | % | Description |
|------|------:|---:|-------------|
| A — Adequate | 226 | 39.6% | Both SAC and CI gap agree: well-sampled |
| B — Undersampled | 49 | 8.6% | Both metrics agree: needs more survey effort |
| C — False Plateau | 25 | 4.4% | SAC looks complete but CI gap says species were missed |
| D — Insufficient | 270 | 47.4% | Low SAC completeness with tight CI bound |

**Key findings:**
1. **SAC alone is insufficient** for assessing sampling adequacy. 25 array-years (4.4%) have false plateaus that only the CI gap method detects.
2. **Calendar-nights** is the correct effort metric. Camera-nights inflates effort ~10× and eliminates all CI gaps. Majority-nights is too strict.
3. Forest and grassland habitats dominate the dataset and show similar Type distributions.
4. The adequacy rate (Type A %) is relatively stable across years (36–45%), suggesting consistent survey design.
