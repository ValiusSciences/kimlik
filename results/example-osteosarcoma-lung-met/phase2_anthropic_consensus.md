# Consensus Gene-Signature Reference for Annotating scRNA-seq/snRNA-seq of a Right-Lung Biopsy in Metastatic Osteosarcoma

**Clinical context:** right lung core/wedge biopsy · metastatic conventional osteosarcoma (OS), primary distal femur
**Data assumption:** human single-cell or single-nucleus RNA-seq; HGNC gene symbols
**Purpose:** clinically recognized cell-type and cell-state signatures for cluster annotation, with discriminators, pitfalls, and validation logic
**Status:** consensus synthesis of three independent expert reports; agreements, disagreements, and low-confidence items are flagged explicitly

> **Citation-verification note.** This consensus preserves every reference supplied by the three source reports. A minority of citations (particularly those with PMIDs in the ≥41,000,000 range and 2026 publication years) could not be cross-verified and are marked **[unverified]** in the bibliography. Treat these as pointers to be confirmed in PubMed before use in a manuscript or clinical report.

---

## 1. Why this specimen needs a "multi-atlas" annotation strategy

A lung biopsy from metastatic osteosarcoma is a **chimeric tissue**. Clusters will fall into four biological families, each requiring a different reference framework. All three source reports converged on this framing.

| Family | Origin | Reference framework | Key refs |
|---|---|---|---|
| **A. Malignant OS cells** | Bone (distal femur) → disseminated | OS single-cell atlases | [1–10] |
| **B. Tumor-recruited stroma/immune** | Bone-, lung-, and blood-derived | Pan-cancer TME atlases (T cell, myeloid, CAF, EC) | [74–110] |
| **C. Resident normal lung** | Right lung parenchyma/airway/pleura | Human Lung Cell Atlas (HLCA), Travaglini atlas | [51–64] |
| **D. Injury/fibrosis-reprogrammed lung** | Metastatic niche remodeling | Lung fibrosis + metastatic-niche literature | [25, 65–73] |

**Family D is specific and clinically important here.** Osteosarcoma cells induce acute alveolar epithelial injury and a chronic, non-resolving wound-healing/fibrotic program in the metastasis-bearing lung, with accumulation of partially differentiated (transitional) epithelial intermediates and profibrotic macrophages — a state that was targetable with nintedanib in preclinical models [25]. If you annotate with a "normal lung" reference only, these transitional epithelial cells will be misassigned (usually to AT2 or basal) or, worse, called malignant.

**Two prior expectations specific to a lung metastasis** derive from the foundational OS atlas (100,987 cells; 7 primary, 2 recurrent, **2 lung metastatic** lesions) [1]:
- **Enrichment of FABP4⁺ proinflammatory macrophages** in lung metastatic lesions.
- **Lower osteoclast infiltration** in lung metastatic (and chondroblastic/recurrent) lesions vs primary osteoblastic OS. Expect a small or absent osteoclast cluster — do not force one.

---

## 2. Consensus annotation workflow

All three reports agree on the core principle: **do not call malignant osteosarcoma cells from collagen/ECM genes alone**, because OS cells, normal lung fibroblasts, and CAFs all express `COL1A1`, `COL1A2`, `COL3A1`, `SPARC`, `POSTN`, `FN1`, `THBS2`.

1. **QC and ambient-RNA control.** In lung tissue, `SFTPC`/`SFTPB`/`SFTPA1`/`SCGB1A1` are extremely abundant ambient transcripts and leak into every cluster; in OS, `COL1A1`/`COL1A2`/`SPARC` soup contaminates immune clusters. Run SoupX or CellBender [119, 122], and require ≥3 co-expressed markers for any epithelial call. Typical OS scRNA-seq QC thresholds: ~200–6,000 genes/cell, <10–15% mitochondrial reads [5].
2. **Doublet removal.** Scrublet/DoubletFinder or equivalent [120, 121]; then a manual doublet audit on collision pairs (§9).
3. **Level-1 (lineage) gating** with high-specificity parent markers (§3):
 `PTPRC` immune · `EPCAM/KRT8/KRT18/KRT19` epithelial · `PECAM1/CDH5/VWF` endothelial · `DCN/LUM/PDGFRA` fibroblast · `RGS5/PDGFRB/CSPG4` pericyte · `ACTA2/MYH11/CNN1` smooth muscle · `HBB/HBA1` erythroid · `PPBP/PF4` platelet.
4. **Malignant-cell identification by CNV inference** — the single most reliable discriminator between OS cells and normal/reactive fibroblasts. Use inferCNV, CopyKAT, SCEVAN, or the haplotype-aware Numbat [111–118], with T/NK/myeloid cells as the diploid reference. Recurrent OS CNV anchors: **chr8q gain (MYC), chr6p12–p21 amplification (RUNX2, VEGFA), chr17p loss (TP53), chr13q loss (RB1)**, and **chr12q13–15 amplification (MDM2/CDK4)** in a subset [15–17, 41].
5. **Level-2 (subtype/state) annotation by module scoring** — `AddModuleScore`, UCell, AUCell, or ssGSEA [123, 124]. Never rely on single genes; use ≥5-gene modules with a control-gene background.
6. **Subcluster each compartment separately** (tumor, immune, epithelial, stromal, vascular) before fine annotation.
7. **Reference mapping as an orthogonal check.** Project onto the integrated HLCA (2.4M cells, 49 datasets, 486 individuals) [52, 61] via Azimuth/scArches/scANVI [125, 126], and onto pan-cancer T-cell [82] and myeloid [83] references.
8. **Curated-database arbitration** for ambiguous clusters: CellMarker 2.0 (83,361 curated tissue–cell-type–marker entries, 656 tissues) [130, 131], PanglaoDB [132].
9. **Report a confidence tier per cluster** (high/medium/low) and flag clusters resolved only by CNV or only by a collision-prone gene.
10. **Validate clinically important calls** with histology/IHC/IF: SATB2, RUNX2, ALPL, osteocalcin for osteogenic tumor; CD45, CD3, CD68, CD31, EPCAM, pan-keratin, FAP, αSMA, TRAP, CTSK as needed [30, 39–48].

---

## 3. Level 1 — Broad lineage panels

| Lineage | Core positive markers | Key negatives / notes | Refs |
|---|---|---|---|
| **Malignant OS, osteoblastic** | `SATB2, RUNX2, SP7, ALPL, IBSP, BGLAP, SPP1, COL1A1, COL1A2, COL5A2, SPARC, CDH11, POSTN, COL11A1, OMD, MEPE, MMP13` | CNV⁺; `PTPRC⁻`, `EPCAM⁻`, `PECAM1⁻` | [1–10, 27–30] |
| **Malignant OS, chondroblastic** | `SOX9, SOX5, SOX6, ACAN, COL2A1, COL9A1/2/3, COL11A1, COL10A1, COMP, MATN3, CHAD, HAPLN1, CYTL1, WIF1, IHH` | Continuum with osteoblastic OS | [1, 2, 31, 32] |
| **Osteoclast / multinucleated giant cell** | `CTSK, ACP5, MMP9, ATP6V0D2, DCSTAMP, OCSTAMP, SIGLEC15, CALCR, NFATC1, TCIRG1, CA2, ITGB3, OSCAR` + myeloid (`CD68, CSF1R, TYROBP`) | Myeloid-derived, `PTPRC⁺`; **expect low abundance in lung mets** | [1, 33–38] |
| **Fibroblast / CAF** | `DCN, LUM, COL1A1, COL3A1, COL6A1/2/3, FBLN1, FBLN2, DPT, PDGFRA, C1R, C1S, MMP2, CXCL14` | CNV-neutral; `RUNX2/SP7/IBSP` low | [51, 52, 74–81] |
| **MSC / osteoprogenitor** | `CXCL12, SFRP2, MME (CD10), THY1, ENG, NT5E, LEPR, GREM1, KITLG, PDGFRB` | Bone-derived; overlaps adventitial fibroblasts | [1] |
| **Pericyte / mural** | `RGS5, PDGFRB, CSPG4, NOTCH3, MCAM, HIGD1B, KCNJ8, ABCC9, COX4I2, NDUFA4L2` | `MYH11/CNN1` high favors SMC | [51, 52, 57] |
| **Smooth muscle** | `ACTA2, TAGLN, MYH11, CNN1, DES, ACTG2, LMOD1, SMTN, PLN` | | [51, 52] |
| **Endothelial** | `PECAM1, CDH5, CLDN5, VWF, EGFL7, RAMP2, ERG, SOX17, ESAM, KDR, EMCN` | | [51, 52, 57–59] |
| **Lung epithelium** | `EPCAM, KRT8, KRT18, KRT19, CDH1, CLDN4, TACSTD2, ELF3, MUC1` | | [51–56] |
| **Mesothelium (pleura)** | `MSLN, UPK3B, WT1, CALB2, ITLN1, PRG4, LRRN4, PDPN, ALDH1A2, KRT8/18` | Common in pleural-based/wedge biopsies; often misannotated | [51, 52, 64] |
| **Myeloid (mono/macro/DC)** | `PTPRC, LYZ, CD68, CD14, AIF1, TYROBP, FCER1G, CSF1R, ITGAM, MNDA, HLA-DRA, CD74` | | [83, 90–94] |
| **Mast cell** | `TPSAB1, TPSB2, CPA3, MS4A2, KIT, CMA1, HPGDS, HDC, VWA5A` | | [51, 60, 83] |
| **Neutrophil / TAN** | `FCGR3B, CSF3R, CXCR2, S100A8, S100A9, S100A12, IL1R2, PROK2, IFITM2, SELL, MPO, ELANE` | Low RNA content, often lost in 10x | [86, 99–101] |
| **T cell** | `CD3D, CD3E, CD3G, CD2, TRAC, TRBC1, TRBC2, CD247, IL7R` | | [82, 84, 85] |
| **NK cell** | `NKG7, GNLY, KLRD1, KLRF1, PRF1, NCR1, FGFBP2, TYROBP, NCAM1` | `CD3D⁻/TRAC⁻` | [90, 106] |
| **B cell** | `MS4A1, CD79A, CD79B, CD19, CD22, BANK1, TNFRSF13C, TCL1A` | `CD74/HLA-DRA` not B-specific | [90, 108, 109] |
| **Plasma cell** | `MZB1, JCHAIN, DERL3, XBP1, SEC11C, PRDM1, TNFRSF17, SDC1, IGHG1, IGKC` | Ig ambient RNA source | [90, 108] |
| **Erythroid** | `HBB, HBA1, HBA2, HBD, ALAS2, AHSP` | Usually contamination | [60] |
| **Platelet / megakaryocyte** | `PPBP, PF4, ITGA2B, GP9, TUBB1, NRGN` | Co-expression with another lineage = adherence/doublet | [60] |
| **Skeletal myocyte/myoblast** | `MYL1, MYLPF, TNNT1, TNNT3, ACTA1, TTN, DES, MYOD1` | Discrete cluster in limb OS; **should be absent in lung** | [1] |
| **Cycling (any lineage)** | `MKI67, TOP2A, CCNB1, CENPF, UBE2C, PCNA, TYMS, STMN1, RRM2, CDK1` | Annotate as "cycling ⟨parent lineage⟩", never as its own type | [111] |

Broad-lineage combinations of this type were used in the primary OS atlas, which identified 11 major clusters (osteoblastic OS, chondroblastic OS, osteoclasts, myeloid, TILs/NK-T, B/plasma, fibroblasts, pericytes, MSCs, endothelial, myoblasts) [1], and are reproduced across subsequent OS single-cell studies [3–6, 9, 10] and OS TME reviews [19–23].

---

## 4. Malignant osteosarcoma compartment (Family A)

### 4.1 Core malignant signature

```
SATB2, RUNX2, SP7, ALPL, IBSP, BGLAP, SPP1, COL1A1, COL1A2,
SPARC, CDH11, POSTN, COL11A1, MMP13
```
Apply only within `PTPRC⁻ / EPCAM⁻ / PECAM1⁻` cells that are CNV-positive. `BGLAP` (osteocalcin) frequently drops out in 3′ scRNA-seq. `SATB2` transcript is **supportive, never definitive** (§4.3).

### 4.2 Tumor differentiation states and programs

| State | Signature genes | Interpretation / caveats | Refs |
|---|---|---|---|
| **Osteoblastic (OB-like)** | `RUNX2, SP7, SATB2, ALPL, IBSP, BGLAP, SPP1, COL1A1, COL1A2, COL5A1/2, SPARC, MGP, BGN, MEPE, OMD, DLX5, MSX2, PTH1R` | Dominant malignant population in most OS by CNV | [1, 6, 27–30] |
| **Chondroblastic (CB-like)** | `SOX9, SOX5, SOX6, ACAN, COL2A1, COL9A1/2/3, COL10A1, COL11A1, COMP, MATN3, HAPLN1, CYTL1, WIF1, EPYC, SNORC, PTGDS` | Trajectory/CNV analyses support transdifferentiation of osteoblastic from chondroblastic malignant cells; if **diploid**, consider entrapped benign cartilage | [1, 2, 31, 32] |
| **Fibroblastic / spindle / ECM-rich** | `COL1A1, COL1A2, COL3A1, COL5A1/2, COL6A3, FN1, TNC, THBS2, POSTN, MMP2, MMP11, MMP14, SERPINE1, FAP, PDPN, VCAN, CDH11` | **Major pitfall — overlaps CAFs.** Requires CNV and/or osteogenic TFs | [1, 2, 74–81] |
| **Proliferating** | `MKI67, TOP2A, CENPF, UBE2C, CDK1, CCNB1/2, BIRC5, TYMS, RRM2, HMGB2, PCNA, MCM2–7` | Chemo-relevant; often a distinct cluster | [5, 111] |
| **MSC-/progenitor-like ("stem-like")** | `CXCL12, SFRP2, MME, THY1, FGF2, NES, PRRX1, SOX4, KLF4, CD44, ALDH1A1, PROM1, MYC` | Candidate tumor-initiating state | [1, 2] |
| **UPR / ER-stress** | `ATF6, XBP1, HSPA5, DDIT3, ATF4, HERPUD1, EDEM1, SEL1L, MANF, PDIA4` | UPR-high malignant subcluster with **ATF6α** as top activated TF, associated with aggressiveness (110,000-cell/17-sample OS atlas) | [3] |
| **EMT / invasive-migratory** | `VIM, FN1, SPARC, TIMP1, SERPINE1, LOX, LOXL2, TNC, THBS2, ZEB1, SNAI2, CD24` | `CD24`, `LOX/SERPINE1`, and JUN–BAMBI signaling linked to OS invasion/metastasis | [20] |
| **Hypoxic / glycolytic** | `CA9, VEGFA, SLC2A1, LDHA, PDK1, PGK1, ENO1, NDRG1, ADM, BNIP3, HILPDA` | Spatially localized; not OS-specific | [1, 74] |
| **Inflammatory / matrix-remodeling** | `CXCL8, IL6, CXCL1, CXCL2, MMP9, MMP13, MMP14, LOX, SERPINE1, PLAUR, ITGA5, TNC, POSTN, COMP, CTHRC1` | `POSTN` strongly upregulated in OS vs normal osteoblasts (mRNA and protein) | [5, 74] |
| **IFN / MHC-responsive** | `HLA-A/B/C, B2M, TAP1, NLRC5, STAT1, IRF1, ISG15, IFI6, IFIT1/2/3, MX1, CXCL9, CXCL10`; sometimes `HLA-DRA, CD74` | IFN induction correlated with improved survival in an OS model system. If CNV⁺ and `PTPRC⁻`, consider MHC-II⁺ tumor state rather than APC | [8, 95, 96] |
| **Replication stress** | `CDKN1A, ATR, CHEK1, RPA2, H2AX/H2AFX, TP53BP1, GADD45A` | Murine hierarchy: multipotent progenitor → immature (replication-stress-enriched) osteoblast → mature osteoblast; p53 loss enables sustained proliferation and **lung metastasis** | [7] |
| **Hedgehog** | `GLI1, PTCH1, HHIP` | Developmental-context module | [7] |
| **Mature osteocyte-like (rare)** | `DMP1, PHEX, SOST, MEPE, FGF23` | Rarely captured; if diploid, consider entrapped bone | [27–30] |
| **MDM2/CDK4-amplified context** | `MDM2, CDK4, HMGA2` + CNV amplification | Not universal in conventional high-grade OS; relevant if pathology suggests parosteal/low-grade central/dedifferentiated OS | [11, 15–17, 41] |
| **Metastasis-associated hub genes** | `SKP2, KIF20A, SEC16B (loss)` | Hypothesis-generating; `SKP2` knockout reduced metastasis and exhaustion and upregulated IFN in a murine model; SEC16B loss aids invasion | [8, 9, 10] |

### 4.3 Discriminating malignant OS from lung fibroblasts / CAFs — the hardest call

Use a **composite rule** (unanimous across all three reports):

1. **CNV positivity** (inferCNV/CopyKAT/SCEVAN/Numbat) — primary criterion [111–118].
2. **Osteogenic transcription factors present:** `RUNX2, SP7/OSX, SATB2, DLX5, MSX2` → OS; absent/low in CAFs.
3. **Bone-matrix genes present:** `IBSP, ALPL, MEPE, OMD, COL11A1, SPP1^high` → OS.
4. **Canonical fibroblast identity genes absent/low:** `DCN, LUM, PDGFRA, FBLN1, CFD, APOD, PI16, SCARA5` → these mark CAF/normal fibroblast.
5. **Pathology corroboration with explicit caveats.** SATB2 is the accepted IHC marker of osteoblastic differentiation [29, 30, 46, 47], but published limitations are substantial:
 - Sensitivity ~92.6% but specificity as low as ~50% in some series; positive in giant cell tumor and fibrous dysplasia [44, 45].
 - Does **not** reliably separate OS from chondrosarcoma on biopsy (SOX9 positive in both) [39].
 - Positive in atypical fibroxanthoma, pleomorphic dermal sarcoma, sarcomatoid SCC/melanoma, leiomyosarcoma [40].
 - Does not distinguish jaw OS from benign fibro-osseous lesions [41]; limits documented in extraskeletal OS [42].
 - Sensitive/specific when used **in a panel** (canine validation) [43].
 - `SATB2` is also expressed in colorectal epithelium/carcinoma — if `SATB2⁺` cells are `EPCAM/KRT/CDX2⁺`, consider an epithelial metastasis differential instead [29, 30].

> **Practical implementation.** Compute three per-cell scores — `OSTEOGENIC_score`, `FIBROBLAST_score`, `CNV_score` — and plot them jointly (2D scatter or ternary). Clean malignant OS clusters sit high on osteogenic + CNV and low on fibroblast.

---

## 5. Osteoclasts and giant cells

**Core:** `CTSK, ACP5 (TRAP), MMP9, ATP6V0D2, DCSTAMP, OCSTAMP, SIGLEC15, CALCR, TCIRG1, CA2, NFATC1, ITGB3, OSCAR`
**Myeloid confirmation (required):** `PTPRC, CD68, CSF1R, TYROBP, FCER1G`
**Differentiation axis to score:** progenitor `CD14, CXCR4` → pre-osteoclast `NFATC1, TNFRSF11A (RANK)` → mature `CTSK, ACP5, DCSTAMP, ATP6V0D2, CALCR`; `CD14` is lost during maturation [36, 37, 38].
**Ligand/receptor axis:** `TNFSF11 (RANKL) – TNFRSF11A (RANK) – TNFRSF11B (OPG)`, `CSF1 – CSF1R`, `SPI1`, `FOS` [33–35].

**Caveats and consensus notes:**
- `ATP6V0D2` is shared with **pulmonary ionocytes** — always require `CTSK + ACP5 + MMP9` plus myeloid identity.
- Distinguish osteoclasts from macrophages by high `CTSK/ACP5` and low `CD14`; `CALCR/DCSTAMP` are the most bone-resorption-specific [36, 37].
- **Expect fewer osteoclasts in a lung metastasis than in the femoral primary** [1].
- Osteoclast-differentiation programs and `CSF1R` are broadly expressed across osteoblast and monocyte/macrophage lineages in OS; low-`CSF1R` tumors showed greater predicted ICI sensitivity [17].

---

## 6. Lung epithelium (Family C) and injury states (Family D)

### 6.1 Normal lung epithelium

| Cell type | Signature | Notes | Refs |
|---|---|---|---|
| **Pan-epithelial** | `EPCAM, KRT8, KRT18, KRT19, CDH1, CLDN4, TACSTD2, MUC1, ELF3` | Parent gate | [51–54] |
| **AT1** | `AGER, PDPN, CAV1, CAV2, AQP5, HOPX, CLDN18, EMP2, RTKN2, CLIC5, SPOCK2, SCEL, MYRF` | `PDPN` also lymphatic/mesothelial | [51, 52, 59] |
| **AT2** | `SFTPC, SFTPB, SFTPA1, SFTPA2, SFTPD, NAPSA, LAMP3, ABCA3, SLC34A2, PGC, ETV5, LPCAT1, WIF1, HHIP` | Surfactant genes are the dominant ambient RNA in lung — require co-expression | [51, 52] |
| **AT0 / AT2-signaling (novel, rare)** | `SFTPC + SCGB3A2, SFTPB, SCGB3A1, AXIN2, TM4SF1` | Novel state defined in HLCA | [52, 61] |
| **AT2→AT1 transitional (see 6.2)** | see below | Prioritize in this sample | [25, 65–70] |
| **Club / secretory** | `SCGB1A1, SCGB3A1, SCGB3A2, CYP2F1, BPIFA1, BPIFB1, MGP, TFF3, WFDC2, MUC5B` | `WFDC2` non-specific | [51–54] |
| **Goblet / mucous** | `MUC5AC, MUC5B, SPDEF, AGR2, TFF1, TFF3, CLCA1, FCGBP, CEACAM5` | | [51–54] |
| **Ciliated** | `FOXJ1, PIFO, TPPP3, RSPH1, DNAH5, DNAI1, CCDC39, CAPS, SNTN, HYDIN, C20orf85` | | [51–56] |
| **Basal** | `KRT5, KRT14, KRT15, KRT17, TP63, NGFR, ITGA6, S100A2, DST, MIR205HG, DLK2` | | [51–54] |
| **Suprabasal / hillock** | `KRT13, KRT4, KRT6A, SCGB3A1, S100A2` | | [52] |
| **Submucosal gland serous / mucous** | `LTF, LYZ, AZGP1, PRR4, ZG16B, BPIFB1, BPIFB2, MUC7` | Rare-cell niche | [52, 54, 63] |
| **Pulmonary ionocyte** | `FOXI1, CFTR, ASCL3, ATP6V1B1, ATP6V1G3, ATP6V0D2, BSND, TMEM61` | ~0.45% of airway epithelium | [55, 56, 62] |
| **Tuft / brush** | `POU2F3, ASCL2, TRPM5, DCLK1, AVIL, LRMP, GNAT3, IL25, ALOX5AP, GFI1B` | ~0.002% of airway epithelium; often mislabeled "Other" | [51, 62] |
| **Pulmonary neuroendocrine (PNEC)** | `ASCL1, INSM1, CHGA, CHGB, SYP, NCAM1, CALCA, GRP, SCG2` | If expanded + aneuploid, consider NE carcinoma | [51, 52] |

### 6.2 Injury / fibrosis-associated epithelial states — **prioritize in this specimen**

| State | Signature | Why it matters here | Refs |
|---|---|---|---|
| **Transitional AT2 / alveolar differentiation intermediate (ADI) / KRT8-high** | `KRT8^high, KRT18, KRT19, CLDN4, CDKN1A, SFN, KRT7, SPRR1A, SPRR1B, S100A2, LGALS3, LCN2, TACSTD2, MDK, GDF15` + reduced mature AT1/AT2 markers | `SPRR1A` marks murine Krt8⁺ ADIs and human aberrant basaloid cells; ablating Sprr1a⁺ cells reduced fibrosis | [25, 65–68] |
| **Aberrant basaloid (KRT5⁻/KRT17⁺)** | `KRT17^high, KRT5^low/neg, TP63^low, VIM, FN1, ITGB6, CDH2, PRSS2, MMP7, GDF15, SOX9, COL1A1^low` | Co-express basal and mesenchymal markers; two subsets (Krt5^low/Tp63^low vs Krt5^hi/Tp63^hi) inducible by TGF-β2 | [66, 69, 70] |
| **Metastasis-associated profibrotic epithelium** | ADI/ABC modules + `FN1, TNC, SERPINE1, TGFB1, TGFB2, ITGB6` | OS cells induce alveolar injury and accumulation of profibrotic partially differentiated intermediates; nintedanib blocked metastatic progression via antifibrotic action | [25] |

> **Critical pitfall (all three reports).** Aberrant basaloid/ADI cells express `VIM`, `FN1`, collagen transcripts, and `CDKN1A`, and are readily mistaken for **EMT-like malignant OS cells**. Resolve with (i) `EPCAM/KRT8/KRT18/KRT19` positivity, (ii) absence of `RUNX2/SP7/IBSP/ALPL/SATB2`, (iii) CNV-neutral profile.

### 6.3 Epithelial malignancy differentials (rare but must be excluded)

| Differential | Signature | Refs |
|---|---|---|
| **Lung adenocarcinoma** | `EPCAM, KRT8/18/19, NKX2-1 (TTF-1), NAPSA, SFTPB, SFTPC, MUC1, CEACAM6` + CNV | [47, 48, 49, 88, 89] |
| **Squamous carcinoma** | `TP63, KRT5, KRT6A, KRT6B, KRT14, SOX2, DSG3` + CNV | [48, 88, 89] |
| **Primary pulmonary osteosarcoma** | Osteogenic program + CNV in a lung-primary clinical context | [26] |

TTF-1 plus Napsin-A reach ~99.1% specificity for pulmonary adenocarcinoma but TTF-1 is not fully specific in isolation [47].

---

## 7. Stromal and vascular compartments

### 7.1 Fibroblasts and CAFs

| Subtype | Signature | Refs |
|---|---|---|
| **Pan-fibroblast** | `COL1A1, COL1A2, COL3A1, DCN, LUM, DPT, PDGFRA, COL6A1/2/3, C1R, C1S, FBLN1, FBLN2, CXCL14, MMP2, VIM` | [51, 52, 71, 74, 80] |
| **Alveolar fibroblast / lipofibroblast-like** | `NPNT, WNT2, FGF7, FGF10, TCF21, GPC3, LIMCH1, SCN7A, ADH1B, PLIN2, APOE, FABP5` | [51, 52, 65, 66, 71] |
| **Adventitial / PI16⁺ fibroblast** | `PI16, DPP4, SCARA5, SERPINF1, MFAP5, CD34, ELN, C7, CFD, CCL11, DPT` | [51, 80] |
| **Peribronchial fibroblast** | `FGF18, WIF1, ASPN, HHIP, FGF7` | [52, 61] |
| **Myofibroblast** | `ACTA2, TAGLN, MYL9, TPM2, ASPN, WIF1, POSTN, FN1, TNC, CTGF, LOX, LOXL2, COL1A1, COL3A1` | [65, 66, 71, 76–79] |
| **myCAF / TGFβ-responsive CAF** | `ACTA2, TAGLN, MYL9, TPM2, FAP, POSTN, CTHRC1, TNC, COL10A1, COL11A1, INHBA, LRRC15, THY1, THBS2, COMP, LOX` | [74, 76–79] |
| **iCAF / inflammatory CAF** | `IL6, CXCL12, CXCL14, CXCL1, CXCL2, CXCL8, CCL2, LIF, HAS1, DPT, APOD, CLU, CFD, C3, C7, PLA2G2A, PDGFRA` | [75–78] |
| **apCAF / antigen-presenting CAF** | `HLA-DRA, HLA-DRB1, HLA-DPA1, HLA-DPB1, CD74, CIITA, SLPI`; `PTPRC⁻` | [77] |
| **Matrix-remodeling CAF** | `COL10A1, COL11A1, COMP, THBS2, MMP2, MMP11, FN1, POSTN, TNC, LOX, CTHRC1` | [74, 79–81] |
| **Fibrotic / metastatic-niche myofibroblast** | `CTHRC1, COL1A1, COL3A1, POSTN, COMP, TNC, FN1, LOX, CDH11, SFRP4` | [25, 71, 72] |

**Consensus caveat:** `COL1A1` is upregulated across *all* mesenchymal subtypes during fibrotic remodeling and is not lineage-discriminating [71, 72]. Use `NPNT` (alveolar), `PI16` (adventitial), `WIF1/FGF18` (peribronchial), and bone TFs (`SATB2/RUNX2`) to resolve the COL1A1⁺ space.

### 7.2 Mural cells

- **Pericyte:** `RGS5, NOTCH3, PDGFRB, HIGD1B, KCNJ8, CSPG4, COX4I2, NDUFA4L2, MCAM, ABCC9, TBX5, ACTA2^low`
- **Vascular SMC:** `MYH11, ACTG2, CNN1, DES, LMOD1, TAGLN, ACTA2^high`
- **Airway SMC:** `DES, ACTG2, CNN1, MYH11, PLN, CHRDL2`
 Refs: [51, 52, 57]

### 7.3 Endothelial cells — use the lung-specific taxonomy

| Subtype | Signature | Refs |
|---|---|---|
| **Pan-EC** | `PECAM1, CDH5, CLDN5, VWF, EGFL7, RAMP2, ERG, SOX17, ESAM, KDR, EMCN, ENG` | [51, 52, 57, 58] |
| **General capillary (gCap)** | `FCN3, CA4, IL7R, EDN1, GPIHBP1, SLC6A4, RGCC, BTNL9, PRX` | [51, 52, 57, 59] |
| **Aerocyte (aCap)** | `HPGD, EDNRB, S100A3, SOSTDC1, IL1RL1, TBX2, TBX3, CHRM2, CA4, APLN` | [51, 52, 59] |
| **Arterial** | `GJA5, DKK2, HEY1, SOX17, EFNB2, SERPINE2, IGFBP3, CXCL12, DLL4, BMX, NOTCH4` | [51, 52, 57] |
| **Venous / venular** | `ACKR1, NR2F2, VCAM1, SELE, SELP, PLVAP, CPE, VWF^high` | [51, 52, 57] |
| **Systemic/bronchial vessel** | `COL15A1, PLVAP, SPRY1, VWA1` | [51, 52, 61] |
| **Lymphatic** | `PROX1, PDPN, LYVE1, FLT4, CCL21, MMRN1, TFF3, TBX1` | [51, 52, 57] |
| **Tip cell / angiogenic (tumor-associated)** | `ESM1, APLN, ANGPT2, CXCR4, DLL4, NID2, PGF, MMP14, KDR^high, FLT1, INSR` | [57, 58, 74] |
| **High endothelial venule (TLS-associated)** | `ACKR1, CCL21, SELP, LTB, CHST4` | [102] |
| **Proliferating EC** | `MKI67 + PECAM1` | [111] |

**Note:** endothelial `INSR` was identified as an OS-associated, prognosis-linked target expressed predominantly in endothelial cells — worth overlaying on EC clusters [18]. Tumor-specific EC states (loss of immune-homing programs, checkpoint co-regulation) are described in lung TME profiling [74].

### 7.4 Other structural cells

- **Mesothelial:** `MSLN, UPK3B, WT1, CALB2, ITLN1, PRG4, LRRN4, PDPN, ALDH1A2, HP, KRT5^var` [51, 52, 64]
- **Schwann / peripheral nerve (rare):** `SOX10, S100B, PLP1, MPZ, PMP22, NGFR` [51, 60]
- **Adipocyte (rare contamination):** `ADIPOQ, PLIN1, LEP, FABP4, LPL, CFD` — note `FABP4` collision with alveolar macrophages [60, 80]

---

## 8. Immune compartment

Adopt the pan-cancer T-cell nomenclature (316 donors, 21 cancer types) [82] and the pan-cancer myeloid taxonomy (210 patients, 15 cancer types) [83], anchored to lung-resident identities from HLCA [52].

### 8.1 T cells

| Subset | Signature | Refs |
|---|---|---|
| **Pan-T** | `CD3D, CD3E, CD3G, CD2, TRAC, TRBC1, TRBC2, CD247, IL7R` | [82, 84] |
| **Naive CD4/CD8** | `CCR7, SELL, TCF7, LEF1, MAL, NOSIP, IL7R, FOXP1` | [82, 105] |
| **Central-memory CD4** | `IL7R, CCR7^mid, ANXA1, AQP3, S100A4, LTB` | [82] |
| **Th1 / Th1-like** | `IFNG, TBX21, CXCR3, IL2, GZMK, CCL4, CCL5` | [82] |
| **Th17** | `IL17A, IL17F, RORC, CCR6, KLRB1, IL23R, CTSH, IL26` | [82] |
| **Tfh / CXCL13⁺ CD4 (TLS-associated)** | `CXCL13, IL21, BCL6, TOX2, CD200, ICOS, PDCD1, MAF` | [82, 105] |
| **Treg** | `FOXP3, IL2RA, CTLA4, IKZF2, TIGIT, TNFRSF4, TNFRSF9, TNFRSF18, LAYN, BATF, CCR8, IL1R2, ENTPD1` | [82, 97, 105] |
| **Treg — OS-relevant overlay** | + `CXCR4` (CXCR4 inhibition nominated to target OS Tregs) | [20] |
| **GZMK⁺ effector-memory CD8** | `GZMK, GZMA, CCL5, EOMES, CST7, CXCR3, CXCR4, KLRG1, NKG7` | [82, 84] |
| **Tissue-resident memory CD8 (Trm)** | `ZNF683, ITGAE (CD103), CXCR6, CD69, ITGA1, XCL1, XCL2, NR4A2` | [82] |
| **Terminally exhausted CD8 (Tex)** | `PDCD1, HAVCR2, LAG3, CTLA4, TIGIT, TOX, LAYN, ENTPD1, CXCL13, GZMB, RBPJ, MYO7A` | [82, 95, 96, 107] |
| **Effector / Temra** | `FGFBP2, CX3CR1, GZMH, KLRG1, FCGR3A, TBX21, PRF1, NKG7, GNLY` | [82] |
| **ISG⁺ / IFN-responsive T** | `ISG15, IFIT1, IFIT3, MX1, STAT1, OAS1, IFI6` | [82, 107] |
| **Proliferating T** | `MKI67, TOP2A, STMN1, TYMS` | [82] |
| **MAIT** | `SLC4A10, KLRB1, ZBTB16, NCR3, TRAV1-2, RORC, IL7R, DPP4, IL18RAP, CEBPD` | [82] |
| **γδ T** | `TRDC, TRGC1, TRGC2, TRDV2, TRGV9, KLRC1, NKG7, CD3D` | [82] |

> **Clinically actionable in OS:** `TIGIT` is a high-priority overlay — TIGIT⁺ cells were abundant among primary OS CD3⁺ T cells, and **TIGIT blockade enhanced their cytotoxicity against osteosarcoma** [1]. Report %`TIGIT`⁺ per T-cell subset explicitly.

### 8.2 NK and ILC

| Subset | Signature | Refs |
|---|---|---|
| **CD56^dim cytotoxic NK** | `FGFBP2, FCGR3A, KLRF1, GNLY, PRF1, GZMB, SPON2, CX3CR1, KLRD1, S1PR5, TYROBP, NKG7`; `CD3D⁻/TRAC⁻` | [90, 106] |
| **CD56^bright / tissue-resident NK** | `NCAM1, XCL1, XCL2, GZMK, SELL, KLRC1, CD160, ITGA1, IL7R, IL18` | [106] |
| **ILC/ILC2-like (rare)** | `IL7R, RORA, GATA3, IL1RL1, KIT, KLRB1, AHR, IL23R`; `CD3D⁻` | [51, 52, 60] |
| **NK-ligand overlay (for CAR-NK/GD2 programs)** | `ULBP1-3, MICA, MICB, PVR, NECTIN2, HLA-E, NCR3LG1 (B7-H6)` on tumor cells | [138] |

### 8.3 B cells, plasma cells, and TLS

| Subset | Signature | Refs |
|---|---|---|
| **Naive B** | `MS4A1, IGHD, IGHM, TCL1A, FCER2, IL4R, CD79A/B, BANK1, BACH2` | [90, 108] |
| **Memory B** | `MS4A1, CD27, TNFRSF13B, AIM2, CD24, IGHG1` | [108, 109] |
| **Germinal-center B** | `AICDA, RGS13, MEF2B, LMO2, S1PR2, BCL6, MKI67` | [60, 109] |
| **Atypical / CD11c⁺ B** | `ITGAX, TBX21, FCRL5, ZEB2` — enriched in lung tumors vs normal lung/blood, localize near CD4⁺ T cells | [103] |
| **Plasmablast** | `MZB1, JCHAIN + MKI67, TOP2A` | [108] |
| **Plasma cell** | `MZB1, JCHAIN, DERL3, XBP1, SEC11C, PRDM1, TNFRSF17, SDC1, IGHG1-4, IGKC, IGLC2` | [90, 108] |
| **TLS module (neighborhood-level)** | `CXCL13, CCL19, CCL21, CR2, LTB, CXCR5, SELL, MS4A1, LAMP3, CCR7, PDCD1LG2` | [102, 104] |

### 8.4 Myeloid cells

| Subset | Signature | Notes | Refs |
|---|---|---|---|
| **Classical monocyte** | `CD14, S100A8, S100A9, S100A12, VCAN, FCN1, LYZ, SELL, CCR2, CD300E, LILRB2` | | [83, 90] |
| **Non-classical monocyte** | `FCGR3A, CX3CR1, LST1, MS4A7, CDKN1C, LILRB1/2, TCF7L2, IFITM3, RHOC` | Distinguish from NK by myeloid genes | [83, 90] |
| **Pan-macrophage** | `C1QA, C1QB, C1QC, APOE, CD68, CSF1R, AIF1, MRC1, CD163, LYZ` | | [83, 91–94] |
| **Alveolar macrophage (resident)** | `FABP4, MARCO, MCEMP1, PPARG, MSR1, MRC1, LPL, CIDEC, OLR1, SERPING1, SIGLEC1, APOC1, APOE` | **FABP4⁺ proinflammatory macrophages specifically enriched in lung-metastatic OS** — expect this cluster to be prominent | [1, 52, 86] |
| **Interstitial / FOLR2⁺ perivascular macrophage** | `C1QA/B/C, FOLR2, LYVE1, SELENOP, F13A1, MAF, MAFB, CCL13, MS4A7, MRC1` | Less `MARCO/FABP4` | [52, 83] |
| **SPP1⁺/TREM2⁺ lipid-associated profibrotic TAM** | `SPP1, TREM2, GPNMB, APOE, APOC1, CD9, LGALS3, FABP5, MMP9, MMP12, CHI3L1, ACP5, CTSB, CTSD, CTSL, LIPA` | HLCA identified SPP1⁺ profibrotic monocyte-derived macrophages as a **shared state across COVID-19, pulmonary fibrosis, and lung carcinoma**; SPP1–integrin/CD44 signaling to CAFs promotes invasion/metastasis/immune evasion; prognostic in multiple cancers | [52, 98, 110] |
| **CXCL9/10⁺ IFN-TAM ("M1-like")** | `CXCL9, CXCL10, CXCL11, GBP1, GBP5, STAT1, IDO1, ISG15, IFIT1, IFIT3, MX1, CD80` | | [83, 105] |
| **Inflammatory macrophage** | `IL1B, CXCL8, CCL3, CCL4, TNF, NLRP3, PTGS2, S100A8, S100A9` | Overlaps classical monocytes and dissociation stress | [83, 94] |
| **Angiogenic / pro-tumor TAM** | `VEGFA, VCAN, THBS1, HIF1A, SLC2A1, EREG, INHBA, CD300E, SPP1` | **Pro-angiogenic TAM markers are cancer-type-diverse — do not assume transferability** | [83] |
| **"M2"/immunoregulatory TAM** | `CD163, MRC1, MSR1, STAB1, MAF, TGFB1, IL10, VSIG4` | M1/M2 dichotomy is insufficient in vivo; subsets co-express signatures | [83, 93] |
| **MHC-II^high antigen-presenting macrophage** | `HLA-DRA, HLA-DRB1, HLA-DPA1/B1, CD74, CD86, CIITA` + macrophage genes | Separate from DC/B/apCAF/tumor by parent markers | [83, 90–93] |
| **OS-nominated TAM states** | `TXNIP`⁺; `IFIT1/IFIT3/ISG15`⁺; trajectory `SLC40A1 → MT1G → CXCL10` | Reported in OS scRNA-seq syntheses | [4, 20] |
| **cDC1** | `CLEC9A, XCR1, CADM1, BATF3, IRF8, WDFY4, CLNK, IDO1` | | [83, 90–92] |
| **cDC2** | `CD1C, FCER1A, CLEC10A, CD1E, CD1A, HLA-DQA1, FCGR2B, IRF4, ITGAX` | | [83, 90–92] |
| **LAMP3⁺ mregDC (mature/migratory)** | `LAMP3, CCR7, CD40, CD83, FSCN1, IL4I1, IDO1, CCL19, CCL17, CCL22, BIRC3, CD274, PDCD1LG2` | Derives from both cDC1 and cDC2; maps to TLS-proximal niches | [83, 102] |
| **pDC** | `LILRA4, CLEC4C, IL3RA, GZMB, JCHAIN, IRF7, TCF4, SERPINF1, LAMP5` | | [83, 90–92] |
| **Langerhans-like DC** | `CD207, CD1A` | | [83] |
| **Monocytic MDSC-like** | `S100A8, S100A9, S100A12, CD14, IL1B, VEGFA, OLR1, CD84, TREM1` | State, not a clean lineage | [83, 94] |
| **Tumor-associated neutrophil (TAN)** | `FCGR3B, CSF3R, CXCR2, IL1R2, MMP9, PROK2, S100A12, IFITM2, CD83, SELL, ARG1^low` | Continuum of states (pro-tumor, inflammatory, ISG-high, antigen-presenting) rather than discrete lineages; `CD83` proposed as a hallmark of senescent pro-tumor TANs; severe mRNA–protein discordance | [99–101] |
| **Eosinophil** | `CLC, PRG2, RNASE2, RNASE3, IL5RA, CCR3, SIGLEC8` | Rare | [60, 90] |
| **Basophil** | `MS4A2, FCER1A, IL3RA, HDC, GATA2, CLC`; `KIT^low`, `TPSB2^low` | Distinguish from mast cells | [60, 90] |
| **Mast cell** | `TPSAB1, TPSB2, CPA3, MS4A2, KIT, CMA1, HPGDS, HDC, VWA5A` | **Reported to increase in metastatic vs primary OS**; TNF⁺/VEGFA⁺ ratio has prognostic relevance | [4, 83] |

---

## 9. Technical / artifact signatures (compute, but never annotate as cell types)

| Module | Genes | Use |
|---|---|---|
| **Mitochondrial fraction** | `^MT-` | Dying/stressed cells |
| **Ribosomal fraction** | `^RP[SL]` | Metabolic/technical drift |
| **Cell cycle (S/G2M)** | `MKI67, TOP2A, UBE2C, CENPF, CDK1, CCNB1, CCNB2, BIRC5, TYMS, PCNA, STMN1, RRM2, MCM2–7` | Regress or label "cycling ⟨lineage⟩" [111] |
| **Dissociation / immediate-early stress** | `FOS, FOSB, JUN, JUNB, EGR1, ATF3, DUSP1, IER2, HSPA1A, HSPA1B, DNAJB1, HSPB1, SOCS3, ZFP36` | Strongly advised for bone/lung enzymatic digests; prevents spurious "stress cell type" clusters |
| **Interferon response** | `ISG15, IFI6, IFI27, IFIT1/2/3, MX1, MX2, OAS1, STAT1, IRF7` | Cross-lineage state |
| **Ambient surfactant RNA** | `SFTPA1, SFTPA2, SFTPB, SFTPC, SFTPD` | Require epithelial co-expression for AT2 calls [119] |
| **Ambient immunoglobulin RNA** | `IGHG*, IGHA*, IGKC, IGLC*, JCHAIN` | Check full plasma-cell program |
| **Ambient hemoglobin** | `HBA1, HBA2, HBB, HBD, ALAS2` | Blood contamination |
| **Ambient tumor collagen (OS-specific)** | `COL1A1, COL1A2, SPARC` | Contaminates immune clusters |
| **Doublet red flags** | `PTPRC`+`EPCAM`; `EPCAM`+`COL1A1`; `PECAM1`+`CD3D`; `COL1A1`+`CD3D`; `PECAM1`+`LYZ`; `PPBP/PF4`+any lineage | Review UMI counts and doublet scores [120–122] |

---

## 10. High-priority marker-collision warnings

Unanimous across the three reports; these are the dominant error sources in this specimen.

| Gene(s) | Collides across | How to resolve |
|---|---|---|
| `COL1A1, COL1A2, COL3A1, SPARC, POSTN, FN1, THBS2` | Malignant OS · fibroblasts · CAFs · myofibroblasts · fibrotic mesenchyme | CNV + `SATB2/RUNX2/SP7/ALPL/IBSP/BGLAP` vs `DCN/LUM/PDGFRA/PI16/NPNT` |
| `SPP1` | Malignant OS · SPP1⁺/TREM2⁺ TAM · injury AT2 · CAF | Parent lineage markers (`PTPRC/C1Q` vs `EPCAM/SFTPC` vs CNV) |
| `LAMP3` | AT2 epithelium · mature/migratory DC | `EPCAM/SFTPC/ABCA3` vs `PTPRC/HLA-DRA/CCR7/FSCN1` |
| `HLA-DRA, CD74` | B cells · macrophages · DCs · apCAFs · MHC-II⁺ tumor | `PTPRC` + lineage markers + CNV |
| `ACTA2, TAGLN, MYL9` | SMC · pericyte · myofibroblast · myCAF · fibroblastic OS | `MYH11/CNN1` (SMC), `RGS5/PDGFRB/NOTCH3` (pericyte), CNV + osteogenic TFs (tumor) |
| `SATB2` | Osteoblastic OS · colorectal epithelium/carcinoma · several sarcomas/carcinomas by IHC | `EPCAM/KRT/CDX2` → epithelial differential; see §4.3 caveats [39–45] |
| `ATP6V0D2` | Osteoclast · pulmonary ionocyte | Require `CTSK+ACP5+MMP9` + myeloid identity vs `FOXI1/CFTR/ASCL3` |
| `KRT17` | Basal cells · aberrant basaloid · squamous carcinoma | `KRT5/TP63` level, `VIM/FN1/ITGB6` co-expression, CNV |
| `FABP4` | Alveolar macrophage · adipocyte · some EC | `PTPRC/C1Q/MARCO` vs `ADIPOQ/PLIN1` vs `PECAM1` |
| `PDPN` | AT1 · lymphatic EC · mesothelium · fibroblast/CAF | Parent gate (`EPCAM` vs `PROX1/LYVE1` vs `MSLN/WT1` vs `DCN/LUM`) |
| `FCGR3A` | NK · non-classical monocyte · macrophage | `NKG7/GNLY/KLRF1` + absent TCR vs `LYZ/LST1/CSF1R` |
| `S100A8/A9` | Neutrophil · classical monocyte · MDSC-like | `FCGR3B/CSF3R/CXCR2` vs `CD14/VCAN/FCN1` |
| `SOX9` | Chondroblastic OS · chondrosarcoma · aberrant basaloid | Does not separate OS from chondrosarcoma on biopsy [39] |

---

## 11. Expected cluster composition for this specimen (prior expectations)

| Compartment | Expected abundance in a lung met | Basis |
|---|---|---|
| Malignant osteoblastic OS | High (dominant malignant population) | [1, 6] |
| Malignant chondroblastic OS | Variable; likely if primary had chondroblastic component | [1] |
| **Osteoclasts** | **Low** (reduced in lung mets vs primary) | [1] |
| Fibroblasts / CAFs | **Increased** vs primary | [4] |
| Mast cells | **Increased** vs primary | [4] |
| T/NK cells | **Increased** vs primary; exhaustion-skewed, TIGIT-high | [1, 4] |
| Myeloid overall | **Decreased** proportion vs primary, but with **FABP4⁺ alveolar macrophage enrichment** and SPP1⁺/TREM2⁺ profibrotic TAMs | [1, 4, 52] |
| Resident lung epithelium (AT1/AT2/club/ciliated) | Present; proportion depends on tumor:normal ratio in the core | [51, 52] |
| Transitional/aberrant basaloid epithelium | Present at the metastasis interface | [25, 68] |
| Myofibroblasts / fibrosis program | Present (metastasis-induced fibrosis) | [25] |
| Mesothelium | Present if pleural-based/wedge sampling | [64] |
| Skeletal myoblasts | Should be **absent** (bone/limb-specific cluster) | [1] |

Deviations from these priors are themselves informative and should be reported.

---

## 12. Clinically actionable gene overlay (report per cluster, not for annotation)

| Target axis | Genes | Cell types to quantify | Refs |
|---|---|---|---|
| **B7-H3 / CD276** | `CD276` | Malignant OS (primary), TAMs | [133, 136, 137] |
| **B7-H3 CAR-T homing** | Tumor `CXCL8, CXCL1, CXCL2, CXCL16`; T-cell `CXCR2, CXCR6` | Malignant OS, T cells | [134, 135] |
| **GD2** | `B4GALNT1, ST8SIA1` (synthases; GD2 is a glycolipid) | Malignant OS | [138] |
| **Checkpoints** | `PDCD1, CTLA4, LAG3, HAVCR2, TIGIT, CD274, PDCD1LG2, VSIR, BTLA` | T/NK, TAM, malignant | [1, 20, 95, 96] |
| **Myeloid targeting** | `CSF1R, CSF1, CCR2, CCL2, TREM2, MARCO, SIRPA, CD47` | TAM, monocyte, osteoclast | [17, 98] |
| **Bone-directed therapy** | `TNFSF11 (RANKL), TNFRSF11A, TNFRSF11B` | Osteoblastic OS, osteoclasts, MSC | [20, 33] |
| **Antiangiogenic TKI targets** | `KDR, FLT1, FLT4, PDGFRA, PDGFRB, FGFR1, MET, RET, KIT, INSR` | EC, pericyte, malignant | [18, 25] |
| **Growth-factor axes** | `IGF1R, IGF1, IGF2, ERBB2, EGFR` | Malignant OS | [16, 20] |
| **Apoptosis / TRAIL** | `MCL1, BCL2, BCL2L1, TNFRSF10A, TNFRSF10B, TNFSF10` | Malignant OS in metastatic niche | [20] |
| **Amplification-linked** | `MDM2, CDK4, MYC, RUNX2, VEGFA` | Malignant OS | [15–17, 41] |
| **Fibrosis / niche (nintedanib rationale)** | `FN1, TGFB1, TGFB2, ITGB6, LOX, SERPINE1, CTHRC1` + FGFR/PDGFR/VEGFR | ADI/ABC epithelium, myofibroblast, malignant | [25, 69] |
| **Antigen presentation / IFN** | `HLA-A/B/C, B2M, TAP1, NLRC5, STAT1, ISG15` | Malignant OS | [8] |

---

## 13. Copy-paste signature dictionary (R / Seurat)

```r
sigs <- list(
  # ---------------- Malignant osteosarcoma ----------------
  OS_core            = c("SATB2","RUNX2","SP7","ALPL","IBSP","BGLAP","SPP1","COL1A1","COL1A2",
                         "SPARC","CDH11","POSTN","COL11A1","MMP13"),
  OS_osteoblastic    = c("RUNX2","SP7","SATB2","ALPL","IBSP","BGLAP","SPP1","COL1A1","COL1A2","COL5A2",
                         "SPARC","MGP","BGN","MEPE","OMD","DLX5","MSX2","PTH1R","CDH11"),
  OS_chondroblastic  = c("SOX9","SOX5","SOX6","ACAN","COL2A1","COL9A1","COL9A2","COL9A3","COL10A1",
                         "COL11A1","COMP","MATN3","HAPLN1","CYTL1","WIF1","EPYC","SNORC"),
  OS_fibroblastic_ecm= c("COL1A1","COL1A2","COL3A1","COL5A1","COL5A2","COL6A3","FN1","TNC","THBS2",
                         "POSTN","MMP2","MMP11","MMP14","SERPINE1","FAP","VCAN","CDH11"),
  OS_proliferating   = c("MKI67","TOP2A","CENPF","UBE2C","CDK1","CCNB1","CCNB2","BIRC5","TYMS",
                         "RRM2","HMGB2","PCNA"),
  OS_MSClike         = c("CXCL12","SFRP2","MME","THY1","FGF2","NES","PRRX1","SOX4","CD44",
                         "ALDH1A1","PROM1","MYC"),
  OS_UPR             = c("ATF6","XBP1","HSPA5","DDIT3","ATF4","HERPUD1","EDEM1","SEL1L","MANF","PDIA4"),
  OS_EMT_invasive    = c("VIM","FN1","SPARC","TIMP1","SERPINE1","LOX","LOXL2","TNC","THBS2",
                         "ZEB1","SNAI2","CD24"),
  OS_hypoxia         = c("CA9","VEGFA","SLC2A1","LDHA","PDK1","PGK1","ENO1","NDRG1","ADM","BNIP3","HILPDA"),
  OS_IFN_MHC         = c("HLA-A","HLA-B","HLA-C","B2M","TAP1","NLRC5","STAT1","IRF1","ISG15",
                         "IFIT1","IFIT3","MX1","CXCL9","CXCL10"),
  OS_replstress      = c("CDKN1A","ATR","CHEK1","RPA2","H2AFX","TP53BP1","GADD45A"),
  OS_osteocyte_like  = c("DMP1","PHEX","SOST","MEPE","FGF23"),

  # ---------------- Bone lineage / osteoclast ----------------
  Osteoclast         = c("CTSK","ACP5","MMP9","ATP6V0D2","DCSTAMP","OCSTAMP","SIGLEC15","CALCR",
                         "TCIRG1","CA2","NFATC1","ITGB3","OSCAR"),
  MSC_osteoprog      = c("CXCL12","SFRP2","MME","THY1","ENG","NT5E","LEPR","GREM1","KITLG","PDGFRB"),

  # ---------------- Stroma ----------------
  Fibroblast_pan     = c("DCN","LUM","COL1A1","COL3A1","COL6A3","FBLN1","FBLN2","DPT","PDGFRA",
                         "C1R","C1S","CXCL14","MMP2"),
  Fib_alveolar       = c("NPNT","WNT2","FGF10","FGF7","TCF21","GPC3","LIMCH1","SCN7A","ADH1B"),
  Fib_adventitial    = c("PI16","DPP4","SCARA5","SERPINF1","MFAP5","CD34","ELN","C7","CFD","DPT"),
  Fib_peribronchial  = c("FGF18","WIF1","ASPN","HHIP"),
  Myofibroblast      = c("ACTA2","TAGLN","MYL9","TPM2","ASPN","WIF1","POSTN","FN1","TNC","LOX","LOXL2"),
  CAF_myCAF          = c("ACTA2","TAGLN","MYL9","TPM2","FAP","POSTN","CTHRC1","TNC","COL10A1",
                         "COL11A1","INHBA","LRRC15","THY1","THBS2","COMP","LOX"),
  CAF_iCAF           = c("IL6","CXCL12","CXCL14","CXCL1","CXCL2","CXCL8","CCL2","LIF","HAS1",
                         "DPT","APOD","CLU","C3","C7","PLA2G2A","PDGFRA"),
  CAF_apCAF          = c("HLA-DRA","HLA-DRB1","HLA-DPA1","HLA-DPB1","CD74","CIITA","SLPI"),
  Fib_fibroticNiche  = c("CTHRC1","COL1A1","COL3A1","POSTN","COMP","TNC","FN1","LOX","CDH11","SFRP4"),
  Pericyte           = c("RGS5","PDGFRB","CSPG4","NOTCH3","MCAM","HIGD1B","KCNJ8","ABCC9",
                         "COX4I2","NDUFA4L2"),
  SMC                = c("MYH11","ACTG2","CNN1","DES","LMOD1","TAGLN","ACTA2","SMTN","PLN"),
  Mesothelial        = c("MSLN","UPK3B","WT1","CALB2","ITLN1","PRG4","LRRN4","PDPN","ALDH1A2"),
  Schwann            = c("SOX10","S100B","PLP1","MPZ","PMP22","NGFR"),
  Adipocyte          = c("ADIPOQ","PLIN1","LEP","FABP4","LPL","CFD"),

  # ---------------- Endothelium ----------------
  EC_pan             = c("PECAM1","CDH5","CLDN5","VWF","EGFL7","RAMP2","ERG","SOX17","ESAM","KDR","EMCN"),
  EC_gCap            = c("FCN3","CA4","IL7R","EDN1","GPIHBP1","SLC6A4","RGCC","BTNL9","PRX"),
  EC_aerocyte        = c("HPGD","EDNRB","S100A3","SOSTDC1","IL1RL1","TBX2","TBX3","APLN"),
  EC_arterial        = c("GJA5","DKK2","HEY1","SOX17","EFNB2","SERPINE2","IGFBP3","DLL4","BMX"),
  EC_venous          = c("ACKR1","NR2F2","VCAM1","SELE","SELP","PLVAP","CPE"),
  EC_systemic        = c("COL15A1","PLVAP","SPRY1","VWA1"),
  EC_lymphatic       = c("PROX1","PDPN","LYVE1","FLT4","CCL21","MMRN1","TFF3","TBX1"),
  EC_tip_angiogenic  = c("ESM1","APLN","ANGPT2","CXCR4","DLL4","NID2","PGF","MMP14","INSR"),
  EC_HEV             = c("ACKR1","CCL21","SELP","LTB","CHST4"),

  # ---------------- Lung epithelium ----------------
  Epi_pan            = c("EPCAM","KRT8","KRT18","KRT19","CDH1","CLDN4","TACSTD2","MUC1","ELF3"),
  AT1                = c("AGER","PDPN","CAV1","CAV2","AQP5","HOPX","CLDN18","EMP2","RTKN2","CLIC5",
                         "SPOCK2","SCEL"),
  AT2                = c("SFTPC","SFTPB","SFTPA1","SFTPA2","SFTPD","NAPSA","LAMP3","ABCA3","SLC34A2",
                         "PGC","ETV5","LPCAT1"),
  AT0                = c("SFTPC","SFTPB","SCGB3A2","SCGB3A1","AXIN2","TM4SF1"),
  Club               = c("SCGB1A1","SCGB3A1","SCGB3A2","CYP2F1","BPIFA1","BPIFB1","MGP","TFF3","WFDC2"),
  Goblet             = c("MUC5AC","MUC5B","SPDEF","AGR2","TFF1","TFF3","CLCA1","FCGBP","CEACAM5"),
  Ciliated           = c("FOXJ1","PIFO","TPPP3","RSPH1","DNAH5","DNAI1","CAPS","SNTN","C20orf85"),
  Basal              = c("KRT5","KRT14","KRT15","KRT17","TP63","NGFR","ITGA6","S100A2","MIR205HG","DLK2"),
  Hillock            = c("KRT13","KRT4","KRT6A","SCGB3A1","S100A2"),
  SMG_serous         = c("LTF","LYZ","AZGP1","PRR4","ZG16B","MUC7","BPIFB2"),
  Ionocyte           = c("FOXI1","CFTR","ASCL3","ATP6V1B1","ATP6V1G3","BSND","TMEM61"),
  Tuft               = c("POU2F3","ASCL2","TRPM5","DCLK1","AVIL","LRMP","GNAT3","IL25"),
  PNEC               = c("ASCL1","INSM1","CHGA","CHGB","SYP","NCAM1","CALCA","GRP"),
  Epi_ADI_KRT8       = c("KRT8","KRT18","KRT19","CLDN4","CDKN1A","SFN","KRT7","SPRR1A","SPRR1B",
                         "S100A2","LGALS3","LCN2","MDK","GDF15"),
  Epi_aberrantBasal  = c("KRT17","VIM","FN1","ITGB6","CDH2","PRSS2","MMP7","GDF15","SOX9","TP63"),
  LUAD_differential  = c("EPCAM","KRT8","KRT18","KRT19","NKX2-1","NAPSA","SFTPB","SFTPC","MUC1","CEACAM6"),
  LUSC_differential  = c("TP63","KRT5","KRT6A","KRT6B","KRT14","SOX2","DSG3"),

  # ---------------- Myeloid ----------------
  Myeloid_pan        = c("PTPRC","LYZ","CD68","CD14","AIF1","TYROBP","FCER1G","CSF1R","ITGAM","MNDA"),
  Mono_classical     = c("CD14","S100A8","S100A9","S100A12","VCAN","FCN1","LYZ","SELL","CCR2","CD300E"),
  Mono_nonclassical  = c("FCGR3A","CX3CR1","LST1","MS4A7","CDKN1C","LILRB2","TCF7L2","IFITM3"),
  Mac_pan            = c("C1QA","C1QB","C1QC","APOE","CD68","CSF1R","AIF1","MRC1","CD163"),
  Mac_alveolar       = c("FABP4","MARCO","MCEMP1","PPARG","MSR1","MRC1","LPL","CIDEC","OLR1",
                         "SERPING1","SIGLEC1","APOC1"),
  Mac_FOLR2_C1QC     = c("C1QA","C1QB","C1QC","FOLR2","LYVE1","SELENOP","F13A1","MAF","MAFB","CCL13","MS4A7"),
  TAM_SPP1_TREM2     = c("SPP1","TREM2","GPNMB","APOE","APOC1","CD9","LGALS3","FABP5","MMP9",
                         "MMP12","CHI3L1","ACP5","CTSB","CTSD"),
  TAM_IFN            = c("CXCL9","CXCL10","CXCL11","GBP1","GBP5","STAT1","IDO1","ISG15","IFIT1","IFIT3","MX1"),
  TAM_inflammatory   = c("IL1B","CXCL8","CCL3","CCL4","TNF","NLRP3","PTGS2"),
  TAM_angiogenic     = c("VEGFA","VCAN","THBS1","HIF1A","SLC2A1","EREG","INHBA","CD300E"),
  TAM_M2like         = c("CD163","MRC1","MSR1","STAB1","MAF","TGFB1","IL10","VSIG4"),
  cDC1               = c("CLEC9A","XCR1","CADM1","BATF3","IRF8","WDFY4","CLNK"),
  cDC2               = c("CD1C","FCER1A","CLEC10A","CD1E","CD1A","FCGR2B","IRF4"),
  mregDC_LAMP3       = c("LAMP3","CCR7","CD40","CD83","FSCN1","IL4I1","IDO1","CCL19","CCL17",
                         "CCL22","BIRC3","CD274","PDCD1LG2"),
  pDC                = c("LILRA4","CLEC4C","IL3RA","GZMB","JCHAIN","IRF7","TCF4","SERPINF1","LAMP5"),
  Mast               = c("TPSAB1","TPSB2","CPA3","MS4A2","KIT","CMA1","HPGDS","HDC","VWA5A"),
  Basophil           = c("MS4A2","FCER1A","IL3RA","HDC","GATA2","CLC"),
  Eosinophil         = c("CLC","PRG2","RNASE2","RNASE3","IL5RA","CCR3","SIGLEC8"),
  Neutrophil_TAN     = c("FCGR3B","CSF3R","CXCR2","IL1R2","MMP9","PROK2","S100A12","IFITM2",
                         "CD83","SELL","MPO","ELANE"),

  # ---------------- Lymphoid ----------------
  Tcell_pan          = c("CD3D","CD3E","CD3G","CD2","TRAC","TRBC1","TRBC2","CD247","IL7R"),
  T_naive            = c("CCR7","SELL","TCF7","LEF1","MAL","NOSIP","IL7R"),
  Treg               = c("FOXP3","IL2RA","CTLA4","IKZF2","TIGIT","TNFRSF4","TNFRSF9","TNFRSF18",
                         "LAYN","BATF","CCR8","IL1R2","ENTPD1"),
  CD4_Tfh_CXCL13     = c("CXCL13","IL21","BCL6","TOX2","CD200","ICOS","PDCD1","MAF"),
  CD4_Th1            = c("IFNG","TBX21","CXCR3","IL2","GZMK","CCL4","CCL5"),
  CD4_Th17           = c("IL17A","IL17F","RORC","CCR6","KLRB1","IL23R","CTSH","IL26"),
  CD8_Tem_GZMK       = c("GZMK","GZMA","CCL5","EOMES","CST7","CXCR3","CXCR4","KLRG1","NKG7"),
  CD8_Trm            = c("ZNF683","ITGAE","CXCR6","CD69","ITGA1","XCL1","XCL2","NR4A2"),
  CD8_Tex            = c("PDCD1","HAVCR2","LAG3","CTLA4","TIGIT","TOX","LAYN","ENTPD1","CXCL13","GZMB"),
  CD8_Temra          = c("FGFBP2","CX3CR1","GZMH","KLRG1","FCGR3A","TBX21","PRF1","NKG7","GNLY"),
  T_ISG              = c("ISG15","IFIT1","IFIT3","MX1","STAT1","OAS1","IFI6"),
  MAIT               = c("SLC4A10","KLRB1","ZBTB16","NCR3","TRAV1-2","RORC","DPP4","IL18RAP"),
  gdT                = c("TRDC","TRGC1","TRGC2","TRDV2","TRGV9","KLRC1","NKG7"),
  NK_cytotoxic       = c("FGFBP2","FCGR3A","KLRF1","GNLY","PRF1","GZMB","SPON2","CX3CR1","KLRD1",
                         "S1PR5","NCR1"),
  NK_resident        = c("NCAM1","XCL1","XCL2","GZMK","SELL","KLRC1","CD160","ITGA1","IL7R"),
  ILC                = c("IL7R","RORA","GATA3","IL1RL1","KIT","KLRB1","AHR","IL23R"),
  B_naive            = c("MS4A1","IGHD","IGHM","TCL1A","FCER2","IL4R","CD79A","CD79B","BANK1"),
  B_memory           = c("MS4A1","CD27","TNFRSF13B","AIM2","CD24"),
  B_GC               = c("AICDA","RGS13","MEF2B","LMO2","S1PR2","BCL6","MKI67"),
  B_atypical_CD11c   = c("ITGAX","TBX21","FCRL5","ZEB2"),
  Plasma             = c("MZB1","JCHAIN","DERL3","XBP1","SEC11C","PRDM1","TNFRSF17","SDC1","IGHG1","IGKC"),
  TLS_module         = c("CXCL13","CCL19","CCL21","CR2","LTB","CXCR5","SELL","MS4A1","LAMP3","CCR7"),

  # ---------------- Other / technical ----------------
  Erythroid          = c("HBB","HBA1","HBA2","HBD","ALAS2","AHSP"),
  Platelet           = c("PPBP","PF4","ITGA2B","GP9","TUBB1","NRGN"),
  Myocyte            = c("MYL1","MYLPF","TNNT1","TNNT3","ACTA1","TTN","MYOD1","DES"),
  Cycling            = c("MKI67","TOP2A","CCNB1","CENPF","UBE2C","PCNA","TYMS","STMN1","RRM2","CDK1"),
  DissocStress       = c("FOS","FOSB","JUN","JUNB","EGR1","ATF3","DUSP1","IER2","HSPA1A","HSPA1B",
                         "DNAJB1","HSPB1","SOCS3","ZFP36"),
  IFN_response       = c("ISG15","IFI6","IFI27","IFIT1","IFIT2","IFIT3","MX1","MX2","OAS1","STAT1","IRF7")
)
```

---

## 14. Suggested deliverable and confidence rules

For each cluster report:

`cluster_id | n_cells | top-20 DEGs | best-matching signature (score, z) | second-best (score) | CNV status | reference-mapping label (HLCA / pan-cancer T / pan-cancer myeloid) | final call | confidence tier | notes/caveats`

Flag as **"requires orthogonal validation"** any cluster where:
- (a) top and second-best module scores differ by <1 SD;
- (b) CNV status is ambiguous;
- (c) the call depends on a single collision-prone gene (`LAMP3, SPP1, ACTA2, KRT17, ATP6V0D2, FABP4, SATB2, PDPN, SOX9`);
- (d) the cluster is a proliferation-, IFN-, or stress-defined state rather than a lineage.

---

## 15. Consensus caveats and limitations

1. **No single gene is definitive.** Use ≥5-gene modules with a permutation/control-gene background (UCell/AUCell) and report score distributions rather than binary calls [123, 124].
2. **CNV inference is the anchor, not a formality.** Osteosarcoma is CNV-driven rather than fusion-driven, so CNV-based malignant calling is more informative here than in translocation sarcomas. But subclonal CNV heterogeneity can artificially split one tumor into several "cell types" — always sanity-check malignant subclusters against sample identity and doublet scores [111–118].
3. **Cell-state modules are not cell types.** Proliferation, hypoxia, IFN, UPR, and dissociation-stress modules appear across lineages; score them *within* an annotated lineage.
4. **Pro-angiogenic TAM markers are cancer-type-specific** and may not transfer from other tumors [83].
5. **M1/M2 is insufficient in vivo** — subsets co-express both signatures [83, 93].
6. **Neutrophils are systematically under-captured** and transcriptomically shallow, with severe mRNA–protein discordance; consider protein-based or CITE-seq confirmation [99–101].
7. **SATB2/SOX9 IHC caveats apply equally at the transcript level** (§4.3) [39–45].
8. **Prefer consortium-level references** (HLCA, pan-cancer T/myeloid atlases) over ad hoc marker lists from small single-sample studies; several cited OS studies are hypothesis-generating (e.g., analyses based on a single public GSM from GSE152048) [5].
9. **Chemotherapy effects and sample-size limits** alter OS transcriptional profiles; metastasis-associated hub genes require clinical validation [1, 9, 10].
10. **Ambient RNA is the single most common cause of false-positive epithelial and tumor calls in lung samples** — decontaminate before, not after, annotation [119, 122].
11. **Research use only.** These signatures support exploratory annotation and are not a diagnostic device; clinically consequential calls must be corroborated by histopathology and IHC.

---

## 16. Consolidated references

*(Merged and deduplicated across the three source reports. Entries marked **[unverified]** could not be cross-verified and should be confirmed before citation.)*

### I. Osteosarcoma: biology, genomics, and single-cell atlases
1. Zhou Y, Yang D, Yang Q, et al. **Single-cell RNA landscape of intratumoral heterogeneity and immunosuppressive microenvironment in advanced osteosarcoma.** *Nat Commun.* 2020;11:6322. PMID 33303760. (Author Correction: *Nat Commun.* 2021;12:2567. PMID 33931654.)
2. **Mapping the single-cell differentiation landscape of osteosarcoma.** PMC10515803. https://pmc.ncbi.nlm.nih.gov/articles/PMC10515803/
3. Liu F, Zhang T, Yang Y, et al. **Integrated analysis of single-cell and bulk transcriptomics reveals cellular subtypes and molecular features associated with osteosarcoma prognosis.** *BMC Cancer.* 2025;25:280. PMID 39962461.
4. Li X, Liu J, Wang Y, Hu J, Wang Q. **Molecular characterization of cell dynamics during osteosarcoma progression.** *Transl Oncol.* 2026;71:102899. PMID 42424801. **[unverified]**
5. Li H, Sun C, Yang M. **Single-cell transcriptomic profiling reveals cellular heterogeneity and identifies novel therapeutic targets in osteosarcoma.** *Int J Genomics.* 2026;2026:4040246. PMID 42472256. **[unverified]**
6. Li X, Li G, Peng T, et al. **Heterogeneity-based stratification identifies CKMT2 as a prognostic marker in osteosarcoma.** *Front Cell Dev Biol.* 2026;14:1822741. PMID 42272640. **[unverified]**
7. Saito M, Nakasuka F, Sankoda N, et al. **Inherent tissue homeostasis of the juvenile metaphysis provides a foundation for osteosarcoma development.** *Nat Commun.* 2026;17:6241. PMID 42363015. **[unverified]**
8. Ferrena A, Zhang R, Wang J, et al. **Single-cell RNA analysis of murine osteosarcoma uncovers Skp2 function in metastasis, genomic instability, and immune activation.** *Cancer Res Commun.* 2026;6:923–945. DOI 10.1158/2767-9764.CRC-25-0294. (PMID 41877584) **[unverified]**
9. **Single-cell RNA sequencing reveals the communications between tumour and microenvironment in osteosarcoma metastasis.** *Front Immunol.* 2024;15:1445555. PMC11422128.
10. **Single-cell RNA sequencing reveals the critical role of SEC16B in osteosarcoma.** PMID 40735296 / PMC12301935.
11. Klein MJ, Siegal GP. **Osteosarcoma: anatomic and histologic variants.** *Am J Clin Pathol.* 2006;125:555–581.
12. Kansara M, Teng MWL, Smyth MJ, Thomas DM. **Translational biology of osteosarcoma.** *Nat Rev Cancer.* 2014;14:722–735.
13. Isakoff MS, Bielack SS, Meltzer P, Gorlick R. **Osteosarcoma: current treatment and a collaborative pathway to success.** *J Clin Oncol.* 2015;33:3029–3035.
14. Gill J, Gorlick R. **Advancing therapy for osteosarcoma.** *Nat Rev Clin Oncol.* 2021;18:609–624.
15. Rickel K, Fang F, Tao J. **Molecular genetics of osteosarcoma.** *Bone.* 2017;102:69–79.
16. Behjati S, Tarpey PS, Haase K, et al. **Recurrent mutation of IGF signalling genes and distinct patterns of genomic rearrangement in osteosarcoma.** *Nat Commun.* 2017;8:15936.
17. Chen X, Bahrami A, Pappo A, et al. **Recurrent somatic structural variations contribute to tumorigenesis of osteosarcoma.** *Cell Rep.* 2014;7:104–112.
18. Buddingh EP, Kuijjer ML, Duim RAJ, et al. **Tumor-infiltrating macrophages are associated with metastasis suppression in high-grade osteosarcoma.** *Clin Cancer Res.* 2011;17:2110–2119.
19. Orrapin S, Moonmuang S, Udomruk S, et al. **Unlocking the tumor-immune microenvironment in osteosarcoma.** *Front Immunol.* 2024;15:1394284. PMID 39359731.
20. Asmar C, Awad G, Boutros M, et al. **Single-cell RNA sequencing in osteosarcoma: applications in diagnosis, prognosis, and treatment.** *Med Oncol.* 2025;42:551. PMID 41231422. **[unverified]**
21. **Decoding osteosarcoma from heterogeneity to precision therapy.** PMC12858688. **[unverified]**
22. **Tumor microenvironment in osteosarcoma: from cellular mechanisms to therapy.** PMC12211857. **[unverified]**
23. **Osteosarcoma immune microenvironment: cellular struggle and therapeutic opportunity.** PMC12174160. **[unverified]**
24. PathologyOutlines. **Osteosarcoma (general).** https://www.pathologyoutlines.com/topic/boneosteosarcomageneral.html
25. Reinecke JB, Jimenez Garcia L, Gross AC, et al. **Aberrant activation of wound-healing programs within the metastatic niche facilitates lung colonization by osteosarcoma cells.** *Clin Cancer Res.* 2025;31:414–429. PMID 39540841. (Preprint: *bioRxiv* 2024, PMID 38260361.)
26. Chapman AD, et al. **Primary pulmonary osteosarcoma.** *Cancer.* 2001;91:779–784.
27. Zhang H, Wu S, Luo D, Guo J. **Computational discovery of CSF1R as a potential therapeutic biomarker in osteosarcoma.** *Oncol Lett.* 2026;31:263. PMID 42100022. **[unverified]**
28. Yingkai X, Jianfeng J, Zhiyong H, Zhifeng Z, Lei W. **Identification of endothelial INSR as an osteosarcoma-related biomarker and therapeutic target based on WGCNA.** *Discov Oncol.* 2025;16:1594. PMID 40846806.

### II. Bone lineage: osteoblast, chondrocyte, osteoclast biology
29. Komori T, Yagi H, Nomura S, et al. **Targeted disruption of Cbfa1 results in a complete lack of bone formation owing to maturational arrest of osteoblasts.** *Cell.* 1997;89:755–764.
30. Nakashima K, Zhou X, Kunkel G, et al. **The novel zinc finger-containing transcription factor osterix is required for osteoblast differentiation and bone formation.** *Cell.* 2002;108:17–29.
31. Dobreva G, Chahrour M, Dautzenberg M, et al. **SATB2 is a multifunctional determinant of craniofacial patterning and osteoblast differentiation.** *Cell.* 2006;125:971–986.
32. Conner JR, Hornick JL. **SATB2 is a novel marker of osteoblastic differentiation in bone and soft tissue tumours.** *Histopathology.* 2013;63:36–49.
33. Akiyama H, Chaboissier MC, Martin JF, Schedl A, de Crombrugghe B. **The transcription factor Sox9 has essential roles in successive steps of the chondrocyte differentiation pathway.** *Genes Dev.* 2002;16:2813–2828.
34. Bi W, Deng JM, Zhang Z, Behringer RR, de Crombrugghe B. **Sox9 is required for cartilage formation.** *Nat Genet.* 1999;22:85–89.
35. Boyle WJ, Simonet WS, Lacey DL. **Osteoclast differentiation and activation.** *Nature.* 2003;423:337–342.
36. Teitelbaum SL. **Bone resorption by osteoclasts.** *Science.* 2000;289:1504–1508.
37. Yagi M, Miyamoto T, Sawatani Y, et al. **DC-STAMP is essential for cell-cell fusion in osteoclasts and foreign body giant cells.** *J Exp Med.* 2005;202:345–351.
38. **Transcriptional reprogramming during human osteoclast differentiation.** *Bone Res.* 2023;11. https://www.nature.com/articles/s41413-023-00312-6
39. **Interspecies single-cell RNA-seq analysis of osteoclast differentiation.** PMC9289986.
40. Aol L, Zhou X, Cao Z, et al. **LncRNA ZFAS1 promotes alveolar bone resorption by enhancing osteoclastogenesis in periodontitis.** *J Cell Physiol.* 2026;241:e70134. PMID 41549697. **[unverified]**

### III. Diagnostic marker validity (SATB2, SOX9, MDM2, TTF-1)
41. Sharma AE, Pytel P, Cipriani NA. **SOX9 and SATB2 immunohistochemistry cannot reliably distinguish between osteosarcoma and chondrosarcoma on biopsy material.** *Hum Pathol.* 2022;121:56–64. DOI 10.1016/j.humpath.2021.12.011.
42. Szczepanski JM, Siddiqui J, Patel RM, et al. **Expression of SATB2 in primary cutaneous sarcomatoid neoplasms: a potential diagnostic pitfall.** *Pathology.* 2023;55:350–354. PMID 36732203.
43. Owosho AA, Ladeji AM, Adesina OM, et al. **SATB2 and MDM2 immunoexpression and diagnostic role in primary osteosarcomas of the jaw.** *Dent J (Basel).* 2021;10:4. PMID 35049602.
44. Ichikawa J, Kawasaki T, Onohara K, et al. **Diagnostic challenges in imaging and immunohistopathological profiles in extraskeletal osteosarcoma.** *World J Surg Oncol.* 2024;22:307. PMID 39568020.
45. Shank AMM, Snook E, Cavender K, et al. **SATB2 immunohistochemistry in the diagnosis of osteosarcoma in dogs.** *J Comp Pathol.* 2024;215:14–29. PMID 39368249.
46. **The utility of SATB2 immunohistochemical expression in distinguishing osteosarcoma.** PMID 27465835.
47. **Special AT-rich sequence-binding protein 2 (SATB2) in bone and soft tissue tumours.** PMC9510043.
48. **The use of alkaline phosphatase and RUNX2 to distinguish osteosarcoma.** *Vet Pathol.* DOI 10.1177/03009858221083035.
49. **TTF-1 is a highly sensitive but not fully specific marker for pulmonary adenocarcinoma.** PMC11564378.
50. Travis WD, Brambilla E, Nicholson AG, et al. **The 2015 WHO classification of lung tumors.** *J Thorac Oncol.* 2015;10:1243–1260.
51. Abcam. **Lung cancer biomarkers for IHC research.** https://www.abcam.com/en-us/technical-resources/research-areas/marker-guides/lung-cancer-markers

### IV. Human lung atlases and normal lung cell types
52. Travaglini KJ, Nabhan AN, Penland L, et al. **A molecular cell atlas of the human lung from single-cell RNA sequencing.** *Nature.* 2020;587:619–625. PMID 33208946.
53. Sikkema L, Ramírez-Suástegui C, Strobl DC, et al. **An integrated cell atlas of the lung in health and disease.** *Nat Med.* 2023;29:1563–1577. PMID 37291214.
54. Vieira Braga FA, Kar G, Berg M, et al. **A cellular census of human lungs identifies novel cell states in health and in asthma.** *Nat Med.* 2019;25:1153–1163.
55. Deprez M, Zaragosi LE, Truchi M, et al. **A single-cell atlas of the human healthy airways.** *Am J Respir Crit Care Med.* 2020;202:1636–1645.
56. Plasschaert LW, Žilionis R, Choo-Wing R, et al. **A single-cell atlas of the airway epithelium reveals the CFTR-rich pulmonary ionocyte.** *Nature.* 2018;560:377–381.
57. Montoro DT, Haber AL, Biton M, et al. **A revised airway epithelial hierarchy includes CFTR-expressing ionocytes.** *Nature.* 2018;560:319–324.
58. Schupp JC, Adams TS, Cosme C Jr, et al. **Integrated single-cell atlas of endothelial cells of the human lung.** *Circulation.* 2021;144:286–302.
59. Kalucka J, de Rooij LPMH, Goveia J, et al. **Single-cell transcriptome atlas of murine and human endothelial cells.** *Cell.* 2020;180:764–779.e20.
60. Gillich A, Zhang F, Farmer CG, et al. **Capillary cell-type specialization in the alveolus.** *Nature.* 2020;586:785–789.
61. The Tabula Sapiens Consortium. **The Tabula Sapiens: a multiple-organ, single-cell transcriptomic atlas of humans.** *Science.* 2022;376:eabl4896.
62. Human Lung Cell Atlas portal. https://hlca.sf.czbiohub.org/
63. **Single-cell profiling of human airway identifies tuft-ionocyte progenitor cells.** *Nat Commun.* 2025. PMC12137820 / https://www.nature.com/articles/s41467-025-60441-w
64. **Cellular and molecular architecture of submucosal glands in human and pig airways.** PMC8794846.
65. **Single-cell transcriptomic analysis of human pleura reveals mesothelial heterogeneity.** *Eur Respir J.* 2024;63:2300143.

### V. Lung injury, fibrosis, and mesenchymal remodeling
66. Habermann AC, Gutierrez AJ, Bui LT, et al. **Single-cell RNA sequencing reveals profibrotic roles of distinct epithelial and mesenchymal lineages in pulmonary fibrosis.** *Sci Adv.* 2020;6:eaba1972.
67. Adams TS, Schupp JC, Poli S, et al. **Single-cell RNA-seq reveals ectopic and aberrant lung-resident cell populations in idiopathic pulmonary fibrosis.** *Sci Adv.* 2020;6:eaba1983.
68. Kobayashi Y, Tata A, Konkimalla A, et al. **Persistence of a regeneration-associated, transitional alveolar epithelial cell state in pulmonary fibrosis.** *Nat Cell Biol.* 2020;22:934–946.
69. Peng F, Jiang CS, Zheng Z, et al. **Transcriptomic signature-guided depletion of intermediate alveolar epithelial cells ameliorates pulmonary fibrosis in mice.** *Nat Commun.* 2026;17:1636. PMID 41519994. **[unverified]**
70. Wu B, Shichino S, Ueha S, et al. **Ex vivo lung-organoid model for aberrant basaloid cell induction and activation.** *Inflamm Regen.* 2025;45:33. PMID 41168897. **[unverified]**
71. Khan P, Roux J, Blumer S, et al. **Alveolar basal cells differentiate towards secretory epithelial- and aberrant basaloid-like cells in vitro.** *Cells.* 2022;11:1820. DOI 10.3390/cells11111820.
72. Tsukui T, et al. **Collagen-producing lung cell atlas identifies multiple subsets with distinct localization and relevance to fibrosis.** *Nat Commun.* 2020;11:1920. https://www.nature.com/articles/s41467-020-15647-5
73. **Categorization of lung mesenchymal cells in development and fibrosis.** PMC8188567.
74. Aran D, Looney AP, Liu L, et al. **Reference-based analysis of lung single-cell sequencing reveals a transitional profibrotic macrophage.** *Nat Immunol.* 2019;20:163–172.

### VI. Tumor microenvironment: stroma, CAF, endothelium
75. Lambrechts D, Wauters E, Boeckx B, et al. **Phenotype molding of stromal cells in the lung tumor microenvironment.** *Nat Med.* 2018;24:1277–1289. PMID 29988129.
76. Qian J, Olbrecht S, Boeckx B, et al. **A pan-cancer blueprint of the heterogeneous tumor microenvironment revealed by single-cell profiling.** *Cell Res.* 2020;30:745–762. PMID 32561858.
77. Öhlund D, Handly-Santana A, Biffi G, et al. **Distinct populations of inflammatory fibroblasts and myofibroblasts in pancreatic cancer.** *J Exp Med.* 2017;214:579–596.
78. Elyada E, Bolisetty M, Laise P, et al. **Cross-species single-cell analysis of pancreatic ductal adenocarcinoma reveals antigen-presenting cancer-associated fibroblasts.** *Cancer Discov.* 2019;9:1102–1123. PMID 31197017.
79. Kieffer Y, Hocine HR, Gentric G, et al. **Single-cell analysis reveals fibroblast clusters linked to immunotherapy resistance in cancer.** *Cancer Discov.* 2020;10:1330–1351.
80. Dominguez CX, Müller S, Keerthivasan S, et al. **Single-cell RNA sequencing reveals stromal evolution into LRRC15+ myofibroblasts as a determinant of patient response to cancer immunotherapy.** *Cancer Discov.* 2020;10:232–253.
81. Buechler MB, Pradhan RN, Krishnamurty AT, et al. **Cross-tissue organization of the fibroblast lineage.** *Nature.* 2021;593:575–579.
82. **Single-cell analysis reveals prognostic fibroblast subsets.** PMC9889778.
83. Biocompare. **A guide to fibroblast markers.** https://www.biocompare.com/Editorial-Articles/616968-A-Guide-to-Fibroblast-Markers/

### VII. Immune atlases and immune-cell states
84. Zheng L, Qin S, Si W, et al. **Pan-cancer single-cell landscape of tumor-infiltrating T cells.** *Science.* 2021;374:abe6474. PMID 34914499.
85. Cheng S, Li Z, Gao R, et al. **A pan-cancer single-cell transcriptional atlas of tumor infiltrating myeloid cells.** *Cell.* 2021;184:792–809.e23. PMID 33545035.
86. Guo X, Zhang Y, Zheng L, et al. **Global characterization of T cells in non-small-cell lung cancer by single-cell sequencing.** *Nat Med.* 2018;24:978–985.
87. Zheng C, Zheng L, Yoo JK, et al. **Landscape of infiltrating T cells in liver cancer revealed by single-cell sequencing.** *Cell.* 2017;169:1342–1356.e16.
88. Zilionis R, Engblom C, Pfirschke C, et al. **Single-cell transcriptomics of human and mouse lung cancers reveals conserved myeloid populations across individuals and species.** *Immunity.* 2019;50:1317–1334.e10.
89. Lavin Y, Kobayashi S, Leader A, et al. **Innate immune landscape in early lung adenocarcinoma by paired single-cell analyses.** *Cell.* 2017;169:750–765.e17.
90. Maynard A, McCoach CE, Rotow JK, et al. **Therapy-induced evolution of human lung cancer revealed by single-cell RNA sequencing.** *Cell.* 2020;182:1232–1251.e22.
91. Leader AM, Grout JA, Maier BB, et al. **Single-cell analysis of human non-small cell lung cancer lesions refines tumor classification and patient stratification.** *Cancer Cell.* 2021;39:1594–1609.e12.
92. Villani AC, Satija R, Reynolds G, et al. **Single-cell RNA-seq reveals new types of human blood dendritic cells, monocytes, and progenitors.** *Science.* 2017;356:eaah4573.
93. See P, Dutertre CA, Chen J, et al. **Mapping the human DC lineage through the integration of high-dimensional techniques.** *Science.* 2017;356:eaag3009.
94. Dutertre CA, Becht E, Irac SE, et al. **Single-cell analysis of human mononuclear phagocytes reveals subset-defining markers and identifies circulating inflammatory dendritic cells.** *Immunity.* 2019;51:573–589.e8.
95. Guilliams M, Ginhoux F, Jakubzick C, et al. **Dendritic cells, monocytes and macrophages: a unified nomenclature based on ontogeny.** *Nat Rev Immunol.* 2014;14:571–578.
96. Cassetta L, Fragkogianni S, Sims AH, et al. **Human tumor-associated macrophage and monocyte transcriptional landscapes reveal cancer-specific reprogramming.** *Cancer Cell.* 2019;35:588–602.e10.
97. Wherry EJ, Kurachi M. **Molecular and cellular insights into T cell exhaustion.** *Nat Rev Immunol.* 2015;15:486–499.
98. Thommen DS, Schumacher TN. **T cell dysfunction in cancer.** *Cancer Cell.* 2018;33:547–562.
99. Sakaguchi S, Yamaguchi T, Nomura T, Ono M. **Regulatory T cells and immune tolerance.** *Cell.* 2008;133:775–787.
100. Nieto P, et al. **A single-cell tumor immune atlas for precision oncology.** *Genome Res.* 2021. PMC8494216.
101. **A pan-cancer single-cell panorama of human natural killer cells.** *Cell.* 2023. https://www.cell.com/cell/fulltext/S0092-8674(23)00849-8
102. **Pan-cancer T cell atlas links a cellular stress response state to immunotherapy resistance.** PMC11421770.
103. **An integrated multi-omic single-cell atlas of human B cell identity.** PMC7369630.
104. **A pan-cancer single-cell RNA-seq atlas of intratumoral B cells.** *Cancer Cell.* 2024. https://www.sciencedirect.com/science/article/pii/S1535610824003593
105. **SPP1+ macrophages in colorectal cancer: markers of prognosis and therapy.** PMC11907465.
106. Nie RC, Hu GS, Cao SQ, Wang A, Wang DC, Liu W. **Spatial single-cell landscape of tumor-associated macrophages and their crosstalk with the tumor microenvironment.** *Cell Discov.* 2026;12:35. PMID 42156717. **[unverified]**
107. Bi W, Li X, Zhao H, Han Q, Zhang J. **Heterogeneous neutrophils: key players in regulating tumor immunity.** *Biochim Biophys Acta Rev Cancer.* 2026;1881:189538. PMID 41571211. **[unverified]**
108. Wang Y, Meng Y, Chen K, et al. **Pan-cancer single-cell transcriptomic analysis reveals CD83 as a hallmark of tumor-associated neutrophils with senescent and pro-tumor properties.** *Comput Struct Biotechnol J.* 2025;27:4615–4632. DOI 10.1016/j.csbj.2025.10.056. **[unverified]**
109. Sadiku P, Brenes AJ, Mayer RL, et al. **Single-cell proteomic analysis defines discrete neutrophil functional states in human glioblastoma.** *Nat Commun.* 2025;17:621. PMID 41397978. **[unverified]**
110. Lu F, Zhang T, Li Z, et al. **Integrative single-cell and spatial transcriptomic analysis identifies a TLS-associated LAMP3⁺CCR7⁺ mregDC antigen-presentation program in ovarian cancer.** *Cancers (Basel).* 2026;18:2259. PMID 42512324. **[unverified]**
111. Sambanthamoorthy S, Ren Y, Galvez TK, et al. **CD11c⁺ B cells with potent effector memory phenotype in lung adenocarcinoma correlate with overall patient survival.** *Cancer Immunol Res.* 2026;14:811–826. PMID 41686183. **[unverified]**
112. Tao T, Zhu L, Shen D, et al. **A B cell–IgA–epithelial axis enhances antitumor immunity in HPV-associated penile squamous cell carcinoma.** *Nat Commun.* 2025;17:624. PMID 41381565. **[unverified]**
113. Cell Signaling Technology. **Human immune cell marker guide.** https://www.cellsignal.com/pathways/immune-cell-markers-human
114. Biocompare. **A guide to myeloid cell markers.** https://www.biocompare.com/Editorial-Articles/612866-A-Guide-to-Myeloid-Cell-Markers/
115. **Macrophage diversity in cancer revisited in the era of single-cell omics.** *Trends Immunol.* 2022. https://www.cell.com/trends/immunology/fulltext/S1471-4906(22)00094-1
116. **Biology of lung macrophages in health and disease.** PMC9533769.
117. **Single-cell resolution characterization of myeloid-derived suppressor cells.** *Nat Commun.* 2024;15. https://www.nature.com/articles/s41467-024-49916-4

### VIII. Computational methods: CNV inference, QC, scoring, reference mapping
118. Tirosh I, Izar B, Prakadan SM, et al. **Dissecting the multicellular ecosystem of metastatic melanoma by single-cell RNA-seq.** *Science.* 2016;352:189–196.
119. Patel AP, Tirosh I, Trombetta JJ, et al. **Single-cell RNA-seq highlights intratumoral heterogeneity in primary glioblastoma.** *Science.* 2014;344:1396–1401.
120. Puram SV, Tirosh I, Parikh AS, et al. **Single-cell transcriptomic analysis of primary and metastatic tumor ecosystems in head and neck cancer.** *Cell.* 2017;171:1611–1624.e24.
121. Gao R, Bai S, Henderson YC, et al. **Delineating copy number and clonal substructure in human tumors from single-cell transcriptomes (CopyKAT).** *Nat Biotechnol.* 2021;39:599–608. PMC8122019.
122. Gao T, et al. **Haplotype-aware analysis of somatic copy number variations from single-cell transcriptomes (Numbat).** *Nat Biotechnol.* 2023. PMC10289836. Package: https://cran.r-project.org/web/packages/numbat/numbat.pdf
123. **Benchmarking copy number aberration inference tools using single-cell multi-omic sequencing data.** PMC11879432.
124. **A comparison of tools that identify tumor cells by inferring copy number variation from single-cell data.** PMC11351975.
125. **Identification of malignant cells in single-cell transcriptomics.** *Commun Biol.* 2025. https://www.nature.com/articles/s42003-025-08695-4
126. Young MD, Behjati S. **SoupX removes ambient RNA contamination from droplet-based single-cell RNA sequencing data.** *GigaScience.* 2020. PMC7763177.
127. Wolock SL, Lopez R, Klein AM. **Scrublet: computational identification of cell doublets in single-cell transcriptomic data.** *Cell Syst.* 2019. PMC6625319.
128. Xi NM, Li JJ. **Benchmarking computational doublet-detection methods for single-cell RNA sequencing data.** *Cell Syst.* 2021. https://www.sciencedirect.com/science/article/pii/S2405471220304592
129. **Mitigating ambient RNA and doublet effects on single-cell analysis.** 2025. https://www.sciencedirect.com/science/article/abs/pii/S0304383525002599
130. Andreatta M, Carmona SJ. **UCell: robust and scalable single-cell gene signature scoring.** *Comput Struct Biotechnol J.* 2021. PMC8271111. (Also: **UCell and pyUCell.** *Bioinformatics.* 2026.)
131. Lotfollahi M, Naghipourfar M, Luecken MD, et al. **Mapping single-cell data to reference atlases by transfer learning (scArches).** *Nat Biotechnol.* 2022;40:121–130.
132. Hao Y, et al. **Azimuth reference-based single-cell annotation.** https://azimuth.hubmapconsortium.org/ ; https://satijalab.github.io/azimuth/
133. **Hierarchical and automated cell-type annotation and integration.** PMC10713118.
134. **Single-cell best practices: annotation.** https://www.sc-best-practices.org/cellular_structure/annotation.html
135. Hou W, Ji Z. **Assessing GPT-4 for cell type annotation in single-cell RNA-seq analysis.** *Nat Methods.* 2024.

### IX. Marker databases
136. Hu C, Li T, Xu Y, et al. **CellMarker 2.0: an updated database of manually curated cell markers in human/mouse and web tools based on scRNA-seq data.** *Nucleic Acids Res.* 2023;51:D870–D876. PMID 36300619.
137. Zhang X, Lan Y, Xu J, et al. **CellMarker: a manually curated resource of cell markers in human and mouse.** *Nucleic Acids Res.* 2019;47:D721–D728. PMID 30289549.
138. PanglaoDB. https://panglaodb.se/

### X. Therapeutic-target context
139. Xie Y, Wang H, Zeng F, et al. **Exploiting B7-H3: molecular insights and immunotherapeutic strategies for osteosarcoma.** *Bioengineering (Basel).* 2025;12:1344. PMID 41463642. **[unverified]**
140. Talbot LJ, Chabot A, Ross AB, et al. **Redirecting B7-H3.CAR T cells to chemokines expressed in osteosarcoma enhances homing and antitumor activity in preclinical models.** *Clin Cancer Res.* 2024;30:4434–4449. PMID 39101835.
141. Lake JA, Woods E, Hoffmeyer E, et al. **Directing B7-H3 CAR T cell homing through IL-8 induces potent antitumor activity against pediatric sarcoma.** *J Immunother Cancer.* 2024;12:e009221. DOI 10.1136/jitc-2024-009221.
142. Luan S, Zhao Y, Yu Y, et al. **The relevance of B7-H3 and tumor-associated macrophages in the tumor immune microenvironment of solid tumors.** *Am J Transl Res.* 2025;17:2835–2849. PMID 40385054.
143. De Maria R, Donini C, Capellero S, et al. **Development and activity of canine B7-H3-CAR.CIK lymphocytes against sarcomas.** *Cancer Immunol Immunother.* 2025;74:306. PMID 40944715.
144. Luo W, Zhang HF, Li W, et al. **Circumventing Ewing sarcoma tumor microenvironment resistance by IL1RAP CAR-modified TGFβ1-imprinted NK cells combined with IL-15 agonist and anti-GD2 antibody.** *J Immunother Cancer.* 2026;14:e014633. PMID 42398968. **[unverified]**
145. **Targeting tumor-associated macrophages in osteosarcoma.** https://www.sciencedirect.com/science/article/pii/S1043661826002094 **[unverified]**

---

**Research use only. Not a diagnostic device.** Clinically consequential cell-identity calls (particularly malignant vs reactive stroma, and any epithelial-malignancy differential) must be corroborated by histopathology, IHC, and, where indicated, orthogonal molecular testing.