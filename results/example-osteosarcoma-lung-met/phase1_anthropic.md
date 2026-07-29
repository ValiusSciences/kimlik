# Gene Signatures for Cell-Type Annotation of Single-Cell RNA-seq from a Right-Lung Biopsy of Metastatic Osteosarcoma (Primary: Distal Femur)

**Report version:** 1.0 · Prepared for scRNA-seq cluster annotation
**Sample context:** Right lung core/wedge biopsy · Metastatic conventional osteosarcoma (OS), primary distal femur
**Scope:** Curated, literature-anchored marker panels for clinically recognized cell types expected in this specimen, plus annotation workflow, discriminators, pitfalls, and a therapeutic-target overlay.

---

## 1. Why this sample needs a "two-atlas" annotation strategy

A lung metastasectomy/biopsy from osteosarcoma is a **chimeric tissue**. Your clusters will fall into four biological families, and each requires a different reference framework:

| Family | Origin | Reference framework |
|---|---|---|
| **A. Malignant OS cells** | Bone (distal femur) → disseminated | Osteosarcoma scRNA-seq atlases (Zhou et al. 2020 and successors) |
| **B. Tumor-recruited stroma/immune** | Bone-derived + lung-derived + blood-derived | Pan-cancer TME atlases (T-cell, myeloid, CAF, endothelial) |
| **C. Resident normal lung** | Right lung parenchyma/airway | Human Lung Cell Atlas (HLCA) / Travaglini molecular atlas |
| **D. Injury/fibrosis-reprogrammed lung** | Metastatic niche remodeling | Lung fibrosis / metastatic-niche literature |

Family **D** is specific and clinically important here: osteosarcoma cells induce **acute alveolar epithelial injury** and a **chronic, non-resolving wound-healing/fibrotic program** in the metastasis-bearing lung, with accumulation of **partially differentiated (transitional) epithelial intermediates** and profibrotic macrophages — a state targetable with nintedanib in preclinical models (Reinecke et al., *Clin Cancer Res* 2025; PMID 39540841). If you annotate only with a "normal lung" reference, these transitional epithelial cells will be misassigned (often to AT2 or basal cells) or, worse, called "malignant."

Additionally, the foundational OS atlas (100,987 cells from 7 primary, 2 recurrent, **2 lung metastatic** lesions) reported two features directly relevant to a lung met: **enrichment of proinflammatory FABP4⁺ macrophages in lung metastatic lesions**, and **lower osteoclast infiltration in lung metastatic (and chondroblastic/recurrent) lesions** compared with primary osteoblastic OS (Zhou et al., *Nat Commun* 2020; PMID 33303760; correction PMID 33931654). Expect your osteoclast cluster to be small or absent — do not force it.

---

## 2. Recommended annotation workflow

1. **QC and ambient-RNA control.** In lung tissue, *SFTPC/SFTPB/SCGB1A1* are extremely abundant ambient transcripts and will "leak" into every cluster. Run SoupX/CellBender or at least verify epithelial calls on co-expression of ≥3 markers, not one.
2. **Level-1 (lineage) annotation** using the broad panel in §3.
3. **Malignant-cell identification** by CNV inference (inferCNV / CopyKAT / SCEVAN / Numbat), using immune cells (T/NK/myeloid) as the diploid reference. This is the single most reliable discriminator between malignant OS cells and normal lung fibroblasts/mesenchyme, because they share *COL1A1/COL1A2/COL3A1*. Recurrent OS CNV anchors to look for: **chr8q gain (MYC), chr6p12–p21 amplification (RUNX2, VEGFA), chr17p loss (TP53), chr13q loss (RB1), chr12q13–15 amplification (MDM2/CDK4)** in a subset. inferCNV-based malignant-cell definition is now standard in OS single-cell work (e.g., Zhou et al. 2020, PMID 33303760; Liu et al., *BMC Cancer* 2025, PMID 39962461; Li et al., *Front Cell Dev Biol* 2026, PMID 42272640).
4. **Level-2 (subtype) annotation** by module scoring (`AddModuleScore`, UCell, AUCell, ssGSEA) with the panels in §4–§10 — do **not** rely on single genes.
5. **Reference mapping as an orthogonal check.** Project onto the integrated HLCA (2.4M cells, 49 datasets, 486 individuals, with consensus re-annotation and matching marker genes; Sikkema et al., *Nat Med* 2023, PMID 37291214) via Azimuth/scArches/scANVI, and onto pan-cancer T-cell (Zheng et al., *Science* 2021, PMID 34914499) and myeloid (Cheng et al., *Cell* 2021, PMID 33545035) references.
6. **Curated-database cross-check.** CellMarker 2.0 provides 83,361 manually curated tissue–cell-type–marker entries across 656 tissues (PMID 36300619; original PMID 30289549) and is useful for arbitrating ambiguous clusters.
7. **Report a confidence tier** per cluster (high/medium/low) and flag clusters resolved only by CNV.

---

## 3. Level 1 — Broad lineage panels

| Lineage | Core positive markers | Notes / key negatives |
|---|---|---|
| **Malignant OS (osteoblastic)** | *COL1A1, COL1A2, COL5A2, CDH11, RUNX2, SATB2, SP7/OSX, ALPL, IBSP, SPP1, POSTN, COL11A1, OMD, MEPE* | CNV⁺; *PTPRC*(CD45)⁻, *EPCAM*⁻ |
| **Malignant OS (chondroblastic)** | *ACAN, COL2A1, COL9A1/2/3, COL11A1, SOX9, CYTL1, WIF1* | Transdifferentiation continuum with osteoblastic OS |
| **Osteoclast / multinucleated giant cell** | *CTSK, ACP5, MMP9, ATP6V0D2, DCSTAMP, SIGLEC15, OCSTAMP, CALCR, NFATC1, TCIRG1, CA2, CSF1R, ITGB3* | Myeloid-derived (*CD68⁺, TYROBP⁺*) |
| **Fibroblast / CAF** | *DCN, LUM, COL1A1, COL3A1, COL6A3, FBLN1, PDGFRA, MMP2, VIM* | CNV-neutral |
| **Mesenchymal stromal / osteoprogenitor (MSC)** | *CXCL12, SFRP2, MME(CD10), THY1, ENG, NT5E, LEPR, GREM1, KITLG, PDGFRB* | Bone-derived; overlaps adventitial fibroblasts |
| **Pericyte / mural** | *RGS5, NOTCH3, PDGFRB, ACTA2, TAGLN, HIGD1B, KCNJ8, CSPG4* | |
| **Smooth muscle** | *MYH11, ACTG2, DES, CNN1, ACTA2, LMOD1* | Airway/vascular SMC |
| **Endothelial** | *PECAM1, CDH5, CLDN5, VWF, EGFL7, RAMP2, ERG, SOX17* | |
| **Lung epithelium** | *EPCAM, KRT8, KRT18, KRT19, CDH1, SFTPB, ELF3* | |
| **Mesothelium (pleura)** | *UPK3B, MSLN, WT1, CALB2, ITLN1, PRG4, KRT5(weak)* | Common in wedge/pleural-based biopsies |
| **Myeloid (mono/macro/DC)** | *LYZ, CD68, CD14, AIF1, TYROBP, FCER1G, CSF1R, ITGAM, MNDA, HLA-DRA* | |
| **Mast cell** | *TPSAB1, TPSB2, CPA3, MS4A2, KIT, CMA1, HPGDS* | |
| **Neutrophil / TAN** | *FCGR3B, CSF3R, CXCR2, S100A8, S100A9, S100A12, IFITM2, PROK2, SELL* | Low RNA content; often lost in 10x |
| **T cell** | *CD3D, CD3E, CD3G, CD2, TRAC, TRBC2, IL7R, CD247* | |
| **NK cell** | *NKG7, GNLY, KLRD1, KLRF1, PRF1, TYROBP, NCAM1, FGFBP2* | *CD3D*⁻ |
| **B cell** | *CD79A, CD79B, MS4A1, CD19, BANK1, TNFRSF13C* | |
| **Plasma cell** | *MZB1, JCHAIN, DERL3, XBP1, SEC11C, IGHG1, IGKC, TNFRSF17, SDC1, PRDM1* | |
| **Erythrocyte / RBC** | *HBB, HBA1, HBA2, ALAS2, AHSP* | Usually removed |
| **Platelet / megakaryocyte fragment** | *PPBP, PF4, ITGA2B, GP9, TUBB1* | |
| **Skeletal myocyte / myoblast** | *MYL1, MYLPF, TNNT1, TNNT3, ACTA1, TTN, DES, MYOD1* | Reported as a discrete cluster in limb OS; usually absent in lung |
| **Cycling (any lineage)** | *MKI67, TOP2A, CCNB1, CENPF, UBE2C, PCNA, TYMS, STMN1, RRM2* | Annotate as "cycling <parent lineage>", never as its own cell type |

Broad-lineage marker combinations of this type are those used in the primary OS atlas, which identified 11 major clusters (osteoblastic OS, chondroblastic OS, osteoclasts, myeloid, TILs/NK-T, B/plasma, fibroblasts, pericytes, MSCs, endothelial, myoblasts) (PMID 33303760), and are broadly reproduced across subsequent OS single-cell studies (PMID 39962461; PMID 42424801; PMID 42472256; PMID 42272640) and in the OS TME review literature (Orrapin et al., *Front Immunol* 2024, PMID 39359731; Asmar et al., *Med Oncol* 2025, PMID 41231422).

---

## 4. Malignant osteosarcoma compartment (Family A)

### 4.1 Lineage/state subclusters

| State | Signature genes | Interpretation |
|---|---|---|
| **Osteoblastic OS (OB-like)** | *COL1A1, COL1A2, COL5A1/2, IBSP, ALPL, SP7, RUNX2, SATB2, CDH11, SPP1, MEPE, OMD, PTH1R, DLX5, MSX2, SOST(rare)* | Dominant malignant population in most OS by CNV (PMID 42272640) |
| **Chondroblastic OS (CB-like)** | *ACAN, COL2A1, COL9A3, COL11A1, SOX9, CYTL1, WIF1, EPYC, SNORC, PTGDS* | Trajectory/CNV analyses support transdifferentiation of osteoblastic from chondroblastic malignant cells (PMID 33303760) |
| **Proliferating OS** | *MKI67, TOP2A, CENPF, UBE2C, TYMS, RRM2, HMGB2, PTTG1(PTTG1IP), CDK1* | Chemo-relevant; often a distinct cluster (PMID 42472256) |
| **MSC-/progenitor-like OS ("stem-like")** | *CXCL12, SFRP2, MME, THY1, NES, PRRX1, SOX4, KLF4, CD44, ALDH1A1, PROM1(CD133), MYC* | Candidate tumor-initiating state |
| **UPR/ER-stress OS** | *ATF6, XBP1, HSPA5, DDIT3, ATF4, HERPUD1, EDEM1, SEL1L, MANF, PDIA4* | A UPR-high malignant subcluster with **ATF6α** as top activated TF was associated with aggressiveness in a 110,000-cell/17-sample OS atlas (PMID 39962461) |
| **EMT/invasive-migratory OS** | *VIM, FN1, SPARC, TIMP1, SERPINE1, LOX, LOXL2, TNC, THBS2, ZEB1, SNAI2, CD24, BAMBI/JUN axis* | *CD24*, *LOX/SERPINE1*, and JUN–BAMBI signaling have been linked to OS invasion/metastasis in single-cell work (reviewed PMID 41231422) |
| **Hypoxia/glycolytic OS** | *VEGFA, SLC2A1, LDHA, PGK1, ENO1, NDRG1, ADM, BNIP3, CA9* | Niche-dependent |
| **IFN-responsive OS** | *ISG15, IFIT1, IFIT3, MX1, STAT1, B2M, HLA-A/B/C, CXCL10* | IFN induction correlated with improved survival in an OS model system (Ferrena et al., *Cancer Res Commun* 2026; DOI 10.1158/2767-9764.CRC-25-0294) |
| **Matrix-remodeling OS** | *POSTN, LOX, MMP2, MMP14, COMP, CTHRC1, FN1, TNC* | *POSTN* strongly upregulated in OS vs normal osteoblasts at mRNA and protein level (PMID 42472256) |

### 4.2 Discriminating malignant OS cells from lung fibroblasts/CAFs

This is the hardest call in the dataset. Use a **composite rule**:

1. **CNV positivity** (inferCNV/CopyKAT) — primary criterion.
2. **Osteogenic transcription factors:** *RUNX2, SP7/OSX, SATB2, DLX5, MSX2* → OS; **absent/low** in CAFs.
3. **Bone-matrix genes:** *IBSP, ALPL, MEPE, OMD, SPP1(high), COL11A1* → OS.
4. **Canonical fibroblast identity genes:** *DCN, LUM, PDGFRA, FBLN1, CFD, APOD, PI16, SCARA5* → CAF/normal fibroblast, typically **low** in malignant OS.
5. **Pathology corroboration:** SATB2 is the accepted IHC marker of osteoblastic differentiation, but note published caveats — SATB2 has **limited specificity** (positive in atypical fibroxanthoma, pleomorphic dermal sarcoma, sarcomatoid SCC/melanoma, leiomyosarcoma; PMID 36732203), does **not** reliably separate OS from chondrosarcoma on biopsy (SOX9 is positive in both; Sharma et al., *Hum Pathol* 2022, DOI 10.1016/j.humpath.2021.12.011), and does not distinguish jaw OS from benign fibro-osseous lesions (PMID 35049602); its limits in extraskeletal OS are also documented (PMID 39568020). It is nonetheless sensitive/specific for OS when used **in a panel** (canine validation: PMID 39368249). **Conclusion: treat *SATB2* transcript as supportive, never definitive.**

> **Practical tip:** compute a 3-score matrix per cell — `OSTEOGENIC_score`, `FIBROBLAST_score`, `CNV_score` — and plot as a ternary/2D scatter. Clean malignant OS clusters sit high on osteogenic + CNV, low on fibroblast.

### 4.3 Developmental context worth scoring
A recent murine study defined a differentiation hierarchy from multipotent progenitors → immature (proliferation/replication-stress-enriched) osteoblasts → mature osteoblasts in juvenile metaphysis, with p53 loss enabling sustained proliferation and **lung metastasis** (Saito et al., *Nat Commun* 2026, PMID 42363015). Scoring **replication-stress** (*CDKN1A/p21, ATR, CHEK1, RPA2, H2AX/H2AFX, TP53BP1, GADD45A*) and **Hedgehog** (*GLI1, PTCH1, HHIP*) modules on your malignant clusters is a defensible, mechanistically grounded addition.

---

## 5. Osteoclasts and giant cells

**Core:** *CTSK, ACP5 (TRAP), MMP9, ATP6V0D2, DCSTAMP, OCSTAMP, SIGLEC15, CALCR, TCIRG1, CA2, NFATC1, ITGB3, OSCAR, CLEC11A(context)*
**Upstream/differentiation axis to score:** *TNFSF11 (RANKL) – TNFRSF11A (RANK) – TNFRSF11B (OPG)*, *CSF1 – CSF1R*, *NFATC1*, *SPI1*, *FOS*
**Caution:** *ATP6V0D2* is shared with **pulmonary ionocytes**; always require *CTSK + ACP5 + MMP9* plus myeloid identity (*CD68, TYROBP, FCER1G*).

Clinical/biological relevance: osteoclast-differentiation gene programs and **CSF1R** are widely expressed across osteoblast and monocyte/macrophage lineages in the OS microenvironment, and low-*CSF1R* tumors showed greater predicted ICI sensitivity (Zhang et al., *Oncol Lett* 2026, PMID 42100022). Osteoclast marker hierarchy (early *NFATC1*, late *CTSK/ACP5/DCSTAMP/ATP6V0D2*) is supported by recent bone single-cell/functional work (PMID 41549697). **Remember: expect fewer osteoclasts in a lung metastasis than in the femoral primary (PMID 33303760).**

---

## 6. Stromal compartment

### 6.1 Fibroblasts / CAFs

| Subtype | Signature | Source of definition |
|---|---|---|
| **myCAF (myofibroblastic)** | *ACTA2, TAGLN, MYL9, POSTN, CTHRC1, TNC, COL10A1, COL11A1, INHBA, LRRC15, FAP, THBS2, COMP, LOX, SERPINE1* | myCAF/iCAF dichotomy defined in vivo by scRNA-seq (Elyada et al., *Cancer Discov* 2019, PMID 31197017); *LOX*/*SERPINE1* CAF axis nominated in OS (PMID 41231422) |
| **iCAF (inflammatory)** | *CXCL12, CXCL14, IL6, CXCL1, CXCL2, CFD, C3, C7, HAS1, DPT, APOD, CLU, PDGFRA, PLA2G2A* | PMID 31197017; PMID 32561858 |
| **apCAF (antigen-presenting)** | *HLA-DRA, HLA-DRB1, HLA-DPA1, CD74, SLPI, SAA3(mouse)* | MHC-II⁺/CD74⁺ CAFs without classic costimulatory molecules; activate CD4⁺ T cells (PMID 31197017) |
| **Alveolar fibroblast (normal lung)** | *NPNT, WNT2, FGF10, TCF21, GPC3, LIMCH1, SPINT2, MACF1, SCN7A* | HLCA (PMID 37291214); Travaglini (PMID 33208946) |
| **Adventitial fibroblast** | *PI16, SCARA5, SERPINF1, MFAP5, CD34, ELN, DPT* | PMID 33208946 |
| **Peribronchial fibroblast** | *ASPN, HHIP, FGF7, WIF1* | PMID 37291214 |
| **Fibrotic/metastatic-niche myofibroblast** | *CTHRC1, COL1A1, COL3A1, POSTN, COMP, TNC, FN1, LOX, CDH11, SFRP4* | Directly relevant: OS-driven lung fibrosis with ECM/fibronectin deposition (PMID 39540841) |
| **Lipofibroblast** | *PLIN2, FABP5, APOE, TCF21* | Low confidence in human |

Stromal heterogeneity nomenclature and 52-/68-subtype catalogs from lung and pan-cancer stromal blueprints are the best cross-checks here (Lambrechts et al., *Nat Med* 2018, PMID 29988129; Qian et al., *Cell Res* 2020, PMID 32561858).

### 6.2 Mural cells
- **Pericyte:** *RGS5, NOTCH3, PDGFRB, HIGD1B, KCNJ8, CSPG4, ACTA2(low), COX4I2, NDUFA4L2*
- **Vascular SMC:** *MYH11, ACTG2, CNN1, DES, LMOD1, TAGLN, ACTA2(high)*
- **Airway SMC:** *DES, ACTG2, CNN1, MYH11, PLN, CHRDL2*

### 6.3 Endothelial cells (use the lung-specific taxonomy — it matters)

| Subtype | Signature |
|---|---|
| **General capillary (gCap)** | *FCN3, CA4, IL7R, EDN1, GPIHBP1, SLC6A4, PLVAP(low)* |
| **Aerocyte (aCap, alveolar gas-exchange)** | *HPGD, EDNRB, S100A3, SOSTDC1, IL1RL1, TBX2, CHRM2* |
| **Arterial** | *GJA5, DKK2, HEY1, SOX17, EFNB2, SERPINE2, IGFBP3, CXCL12* |
| **Venous** | *ACKR1, PLVAP, VCAM1, SELP, CPE, NR2F2, VWF(high)* |
| **Systemic/bronchial vessel** | *COL15A1, PLVAP, SPRY1, VWA1* |
| **Lymphatic** | *PROX1, PDPN, LYVE1, CCL21, MMRN1, FLT4, TFF3, TBX1* |
| **Tip cell / angiogenic (tumor-associated)** | *ESM1, APLN, ANGPT2, CXCR4, DLL4, NID2, PGF, KDR(high), INSR* |
| **High endothelial venule (TLS-associated)** | *ACKR1, CCL21, SELP, LTB, CHST4* |
| **Proliferating EC** | *MKI67 + PECAM1* |

Aerocyte/gCap distinction is from the human lung molecular atlas (58 populations; PMID 33208946) and is consolidated in HLCA (PMID 37291214). Tumor-specific EC states (immune-homing downregulation, checkpoint co-regulation) are from lung TME profiling (PMID 29988129). Notably, **endothelial *INSR*** was identified as an OS-associated, prognosis-linked target expressed predominantly in endothelial cells (PMID 40846806) — worth overlaying on your EC clusters.

### 6.4 Mesothelium
*UPK3B, MSLN, WT1, CALB2, ITLN1, PRG4, LRRN4, KRT5(variable), HP*
Frequently present in pleural-based lung biopsies; commonly misannotated as epithelium or CAF.

---

## 7. Resident lung epithelium (Family C)

| Cell type | Signature |
|---|---|
| **AT1 (alveolar type 1)** | *AGER, PDPN, CAV1, CLIC5, SPOCK2, EMP2, HOPX, RTKN2, SCEL, VEGFA* |
| **AT2 (alveolar type 2)** | *SFTPC, SFTPB, SFTPA1, SFTPA2, NAPSA, LAMP3, PGC, ABCA3, ETV5, SLC34A2* |
| **AT2-signaling / AT0-like** | *SFTPC + SCGB3A2, AXIN2, TM4SF1, CTNNB1-target module* |
| **Club / secretory** | *SCGB1A1, SCGB3A2, SCGB3A1, BPIFB1, MGP, TFF3, CYP2F1, WFDC2* |
| **Goblet** | *MUC5AC, MUC5B, SPDEF, TFF1, TFF3, BPIFB1, AGR2, CEACAM5* |
| **Ciliated** | *FOXJ1, TPPP3, PIFO, CAPS, SNTN, DNAI1, RSPH1, TUBA1A, C20orf85* |
| **Basal** | *KRT5, KRT14, KRT15, TP63, S100A2, DLK2, MIR205HG, KRT17* |
| **Suprabasal / hillock** | *KRT13, KRT4, SCGB3A1, S100A2* |
| **Pulmonary neuroendocrine (PNEC)** | *CALCA, ASCL1, CHGA, CHGB, SYP, INSM1, GRP, SCG2* |
| **Ionocyte** | *FOXI1, CFTR, ASCL3, ATP6V1G3, ATP6V0D2, TMEM61* |
| **Tuft / brush** | *POU2F3, ASCL2, TRPM5, AVIL, LRMP, GNAT3* |
| **Submucosal gland serous/mucous** | *LTF, LYZ, AZGP1, PRR4, ZG16B / MUC5B, BPIFB2* |

All from the two canonical human lung references (PMID 33208946; PMID 37291214).

### 7.1 Injury/fibrosis-associated epithelial states — **prioritize these in this sample**

| State | Signature | Why |
|---|---|---|
| **Transitional AT2 / alveolar differentiation intermediate (ADI) / KRT8-high** | *KRT8(high), KRT18, CLDN4, CDKN1A, SFN, KRT7, **SPRR1A**, SPRR1B, S100A2, MDK, GDF15, TP53 targets* | **SPRR1A** was defined as a marker shared by murine Krt8⁺ ADIs and human KRT5⁻/KRT17⁺ aberrant basaloid cells, distinguishing them from other lung populations; ablating *Sprr1a*⁺ cells reduced fibrosis (PMID 41519994) |
| **Aberrant basaloid (KRT5⁻/KRT17⁺)** | *KRT17(high), KRT5(neg/low), TP63(low), VIM, FN1, ITGB6, CDH2, COL1A1(low), PRSS2, MMP7, GDF15, SOX9* | Atypically present in alveolar space in fibrosis; co-express basal (*KRT17*) and mesenchymal (*VIM, FN1*) markers (Khan et al., *Cells* 2022, DOI 10.3390/cells11111820); two ABC subsets (*Krt5^low/Tp63^low* vs *Krt5^hi/Tp63^hi*) described in organoid models with TGF-β2 induction (PMID 41168897) |
| **Metastasis-associated profibrotic epithelium** | Combine ADI/ABC modules + *FN1, TNC, SERPINE1, TGFB1/2, ITGB6* | Osteosarcoma cells induce acute alveolar injury and accumulation of pathogenic, profibrotic, partially differentiated epithelial intermediates and macrophages; nintedanib blocked metastatic progression by inhibiting this fibrosis (PMID 39540841) |

> **Critical pitfall:** aberrant basaloid / ADI cells express *VIM, FN1, COL* transcripts and *CDKN1A*, and can be mistaken for **EMT-like malignant OS cells**. Resolve with (i) *EPCAM/KRT8/KRT18/KRT19* positivity, (ii) absence of *RUNX2/SP7/IBSP/ALPL*, (iii) CNV-neutral profile.

---

## 8. Myeloid compartment

Use the pan-cancer myeloid taxonomy (210 patients, 15 cancer types; Cheng et al., *Cell* 2021, PMID 33545035) plus lung-resident macrophage identity from HLCA (PMID 37291214).

### 8.1 Macrophages

| Subset | Signature | Notes |
|---|---|---|
| **Alveolar macrophage (resident)** | *FABP4, MARCO, MCEMP1, PPARG, MSR1, MRC1, CIDEC, OLR1, SERPING1, INHBA(var), APOC1* | **FABP4⁺ proinflammatory macrophage infiltration was specifically noted in lung metastatic OS lesions** (PMID 33303760) — expect this cluster to be prominent |
| **Interstitial / FOLR2⁺ resident-like macrophage** | *C1QA, C1QB, C1QC, FOLR2, LYVE1, SELENOP, F13A1, MAF, CCL13, MRC1* | |
| **SPP1⁺ / TREM2⁺ lipid-associated, profibrotic TAM** | *SPP1, TREM2, GPNMB, APOE, APOC1, CD9, LGALS3, FABP5, MMP9, CHI3L1, ACP5, CTSD* | HLCA identified **SPP1⁺ profibrotic monocyte-derived macrophages as a shared cell state across COVID-19, pulmonary fibrosis and lung carcinoma** (PMID 37291214). SPP1–integrin/CD44 signaling to CAFs promotes invasion/metastasis/immune evasion in a 28-subtype pan-cancer TAM atlas (Nie et al., *Cell Discov* 2026, PMID 42156717) |
| **CXCL9/10⁺ "M1-like" / IFN-TAM** | *CXCL9, CXCL10, CXCL11, GBP1, GBP5, STAT1, IDO1, ISG15, IFIT1/3, MX1, CD80* | |
| **Angiogenic / pro-tumor TAM** | *VEGFA, VCAN, THBS1, HIF1A, SLC2A1, EREG, INHBA, CD300E, SPP1* | Pro-angiogenic TAMs use **cancer-type-diverse markers** — do not assume one marker generalizes (PMID 33545035) |
| **"M2"/immunoregulatory TAM** | *CD163, MRC1, MSR1, STAB1, MAF, TGFB1, IL10, VSIG4* | |
| **TXNIP⁺ / IFIT1⁺ OS-associated macrophages** | *TXNIP* / *IFIT1, IFIT3, ISG15* | Nominated as therapeutic targets in OS scRNA-seq synthesis (PMID 41231422) |
| **Macrophage trajectory in OS metastasis** | *SLC40A1 → MT1G → CXCL10* | Reported TAM differentiation trajectory during OS progression under immunosuppression (PMID 42424801) |

### 8.2 Monocytes, DCs, granulocytes

| Subset | Signature |
|---|---|
| **Classical monocyte (CD14⁺)** | *CD14, S100A8, S100A9, S100A12, VCAN, FCN1, LYZ, SELL, CD300E* |
| **Non-classical monocyte (CD16⁺)** | *FCGR3A, LST1, MS4A7, CDKN1C, LILRB2, TCF7L2, CSF1R* |
| **cDC1** | *CLEC9A, XCR1, CADM1, BATF3, WDFY4, IDO1* |
| **cDC2** | *CD1C, FCER1A, CLEC10A, CD1E, HLA-DQA1, FCGR2B* |
| **LAMP3⁺ mregDC (mature/regulatory DC)** | *LAMP3, CCR7, CD40, CD83, FSCN1, IL4I1, IDO1, CCL19, CCL22, BIRC3, CD274, PDCD1LG2* |
| **pDC** | *LILRA4, CLEC4C, IL3RA, GZMB, JCHAIN, IRF7, TCF4, SERPINF1* |
| **Langerhans-like DC** | *CD207, CD1A* |
| **Monocytic MDSC-like** | *S100A8/9/12, CD14, IL1B, VEGFA, OLR1, CD84, TREM1* |
| **Tumor-associated neutrophil (TAN)** | *FCGR3B, CSF3R, CXCR2, IL1R2, MMP9, PROK2, S100A12, IFITM2, CD83, ARG1(low in scRNA)* |
| **Mast cell** | *TPSAB1, TPSB2, CPA3, MS4A2, KIT, CMA1, HPGDS, VWA5A* |

Notes:
- **LAMP3⁺ cDCs** can derive from both cDC1 and cDC2, and differ in transcription factors and stimuli (PMID 33545035); a *LAMP3⁺CCR7⁺* mregDC program has been mapped to tertiary-lymphoid-structure-proximal niches (PMID 42512324).
- **Mast cells** deserve attention in this sample: a multi-cohort OS single-cell + spatial integration reported a **significant increase in fibroblasts, mast cells and T/NK cells in metastatic vs primary OS**, with decreased osteoblast and myeloid proportions (PMID 42424801). Mast-cell phenotype (TNF⁺/VEGFA⁺ ratio) has prognostic relevance in pan-cancer myeloid analysis (PMID 33545035).
- **TANs** exist as a continuum of states (pro-tumor, inflammatory, ISG-high, antigen-presenting) rather than discrete lineages (Bi et al., *BBA Rev Cancer* 2026, PMID 41571211); *CD83* has been proposed as a hallmark of senescent, pro-tumor TANs (Wang et al., *Comput Struct Biotechnol J* 2025, DOI 10.1016/j.csbj.2025.10.056). Because neutrophil mRNA–protein discordance is severe, low RNA-based confidence is expected (Sadiku et al., *Nat Commun* 2025, PMID 41397978).

---

## 9. T / NK / innate lymphoid compartment

Adopt the pan-cancer T-cell nomenclature from 316 donors across 21 cancer types (Zheng et al., *Science* 2021, PMID 34914499), which also defined multiple CD8⁺ exhaustion state-transition paths.

### 9.1 CD4⁺ T cells

| Subset | Signature |
|---|---|
| **Naive CD4** | *CCR7, SELL, TCF7, LEF1, MAL, IL7R, FOXP1, NOSIP* |
| **Central memory CD4** | *IL7R, CCR7(mid), ANXA1, AQP3, S100A4, LTB* |
| **Th1 / Th1-like** | *IFNG, TBX21, CXCR3, IL2, GZMK, CCL4, CCL5* |
| **Th17** | *IL17A, IL17F, RORC, CCR6, KLRB1, IL23R, CTSH, IL26* |
| **Tfh / CXCL13⁺ CD4 (TLS-associated)** | *CXCL13, IL21, BCL6, TOX2, CD200, ICOS, PDCD1, MAF* |
| **Treg (activated/tumor)** | *FOXP3, IL2RA, IKZF2, CTLA4, TIGIT, TNFRSF4, TNFRSF9, LAYN, BATF, CCR8, IL1R2* |
| **Treg — OS-relevant axis** | overlay *CXCR4* | CXCR4 inhibition to target Tregs has been nominated from OS scRNA-seq (PMID 41231422) |

### 9.2 CD8⁺ T cells

| Subset | Signature |
|---|---|
| **Naive CD8** | *CCR7, SELL, TCF7, LEF1, IL7R* |
| **GZMK⁺ effector-memory (Tem)** | *GZMK, GZMA, CCL5, EOMES, CST7, CXCR4, KLRG1* |
| **Tissue-resident memory (Trm)** | *ZNF683, ITGAE(CD103), CXCR6, CD69, ITGA1, XCL1, XCL2, NR4A2* |
| **Terminally exhausted (Tex)** | *PDCD1, HAVCR2, LAG3, CTLA4, **TIGIT**, TOX, LAYN, ENTPD1, CXCL13, GZMB, RBPJ, MYO7A* |
| **Effector/Temra (cytotoxic circulating)** | *FGFBP2, CX3CR1, GZMH, KLRG1, FCGR3A, TBX21, PRF1, NKG7, GNLY* |
| **ISG⁺ / IFN-responsive T** | *ISG15, IFIT1, IFIT3, MX1, STAT1, OAS1* |
| **Proliferating T** | *MKI67, TOP2A, STMN1, TYMS* |
| **MAIT** | *SLC4A10, KLRB1, ZBTB16, NCR3, TRAV1-2, RORC, IL7R, CEBPD* |
| **γδ T** | *TRDC, TRGC1, TRGC2, TRDV2, TRGV9, KLRC1, NKG7* |

> **Clinically actionable in OS:** *TIGIT* is a high-priority overlay — TIGIT⁺ cells were abundant among primary CD3⁺ T cells in OS, and **TIGIT blockade enhanced their cytotoxicity against osteosarcoma** (PMID 33303760). Report %*TIGIT*⁺ per T-cell subset explicitly.

### 9.3 NK / ILC

| Subset | Signature |
|---|---|
| **CD56^dim cytotoxic NK** | *FGFBP2, FCGR3A, KLRF1, GNLY, PRF1, SPON2, CX3CR1, TYROBP, NKG7, KLRD1, S1PR5* |
| **CD56^bright / tissue-resident NK** | *NCAM1, XCL1, XCL2, GZMK, SELL, KLRC1, CD160, ITGA1, IL7R* |
| **ILC1/ILC3-like** | *KIT, IL1R1, RORC, AHR, LST1, IL23R* |

NK-relevant target overlay for sarcoma immunotherapy (GD2 synthesis, IL1RAP, TGF-β resistance) is discussed in a recent combinatorial CAR-NK study in Ewing sarcoma that used scRNA-seq + mass cytometry to map response/resistance (PMID 42398968) — useful methodological precedent if you intend to score NK ligand/receptor axes (*ULBP1-3, MICA/MICB, PVR, NECTIN2, HLA-E, B7-H6/NCR3LG1*).

---

## 10. B / plasma cells and tertiary lymphoid structures

| Subset | Signature |
|---|---|
| **Naive B** | *MS4A1, IGHD, TCL1A, FCER2, IL4R, CD79A/B, BACH2* |
| **Memory B** | *CD27, TNFRSF13B, AIM2, CD24, IGHG1/IGHA1(surface class-switched)* |
| **Germinal-center B** | *AICDA, RGS13, MEF2B, LMO2, S1PR2, BCL6, MKI67* |
| **Atypical / CD11c⁺ B** | *ITGAX, TBX21, FCRL5, ZEB2* |
| **Plasmablast** | *MZB1, JCHAIN + MKI67, TOP2A* |
| **Plasma cell** | *MZB1, JCHAIN, DERL3, XBP1, SEC11C, PRDM1, TNFRSF17, SDC1, IGHG1-4, IGKC, IGLC* |
| **TLS module (spot/neighborhood-level)** | *CXCL13, CCL19, CCL21, CR2, LTB, CXCR5, SELL, MS4A1, PDCD1LG2, LAMP3, CCR7* |

CD11c⁺ tumor-infiltrating B cells are enriched in lung tumors versus normal lung/blood and localize near CD4⁺ T cells, with *CD79A* a robust B-lineage quantifier (Sambanthamoorthy et al., *Cancer Immunol Res* 2026, PMID 41686183). B-cell/plasma-cell/TLS/IgA axes as favorable-prognosis TME features are also documented (PMID 41381565).

---

## 11. Technical / artifact signatures to compute (not cell types)

| Module | Genes | Use |
|---|---|---|
| **Mitochondrial fraction** | `^MT-` | Dying cells |
| **Ribosomal fraction** | `^RP[SL]` | Metabolic/technical drift |
| **Hemoglobin** | *HBB, HBA1, HBA2, HBD, ALAS2* | RBC/ambient |
| **Dissociation/stress ("early response")** | *FOS, FOSB, JUN, JUNB, EGR1, ATF3, HSPA1A, HSPA1B, DNAJB1, HSPB1, SOCS3, ZFP36, IER2* | Prevents spurious "stress cell type" clusters — **strongly advised for bone/lung enzymatic digests** |
| **Ambient lung RNA** | *SFTPC, SFTPB, SCGB1A1, SFTPA1* | Correct before epithelial subtyping |
| **Ambient collagen (OS-specific)** | *COL1A1, COL1A2, SPARC* | Malignant OS soup contaminates immune clusters |
| **Cell cycle (S/G2M)** | Standard Tirosh/Seurat lists | Regress or annotate as "cycling <lineage>" |
| **Doublet flags** | *EPCAM+PTPRC*, *COL1A1+CD3D*, *PECAM1+LYZ* | Manual doublet audit |

QC thresholds used in OS scRNA-seq are typically ~200–6,000 genes/cell and <10–15% mitochondrial reads (e.g., PMID 42472256).

---

## 12. Clinically actionable gene overlay (report per cluster)

These are not annotation markers but should be reported as **per-cell-type expression tables**, because they drive trial eligibility discussions in metastatic OS.

| Target axis | Genes | Cell types to quantify | Reference |
|---|---|---|---|
| **B7-H3 / CD276** | *CD276* | Malignant OS (primary), TAMs | High tumor expression, links to aggressiveness/poor prognosis; mAb, CAR-T, ADC, bsAb strategies (PMID 41463642); B7-H3–TAM/CCL2–CCR2 axis (PMID 40385054); B7-H3.CAR-T homing enhanced by *CXCR2/CXCR6* — so also quantify OS-secreted *CXCL8/CXCL1/CXCL2/CXCL16* (PMID 39101835; DOI 10.1136/jitc-2024-009221); cross-species B7-H3 CAR platform in sarcoma (PMID 40944715) |
| **GD2** | *B4GALNT1, ST8SIA1* (synthases; GD2 itself is a glycolipid) | Malignant OS | Anti-GD2 antibody combinations in sarcoma (PMID 42398968) |
| **Checkpoints** | *PDCD1, CTLA4, LAG3, HAVCR2, TIGIT, CD274, PDCD1LG2, VSIR, BTLA* | T/NK, TAM, malignant | PMID 33303760 (TIGIT); PMID 41231422 |
| **Myeloid targeting** | *CSF1R, CSF1, CCR2, CCL2, TREM2, MARCO, SIRPA, CD47* | TAM/monocyte/osteoclast | PMID 42100022; PMID 42156717 |
| **Bone-directed therapy** | *TNFSF11 (RANKL), TNFRSF11A, TNFRSF11B* | Osteoblastic OS, osteoclasts, MSC | *TNFSF11* nominated in OS scRNA-seq (PMID 41231422) |
| **Antiangiogenic TKI targets** | *KDR, FLT1, FLT4, PDGFRA, PDGFRB, FGFR1, MET, RET, KIT* | EC, pericyte, malignant | PMID 40846806 (endothelial *INSR*); nintedanib targets *FGFR/PDGFR/VEGFR* and blocked OS lung metastasis via antifibrotic action (PMID 39540841) |
| **Growth-factor axes** | *IGF1R, IGF1, IGF2, ERBB2, EGFR* | Malignant OS | PMID 41231422 |
| **Apoptosis / TRAIL** | *MCL1, BCL2, BCL2L1, TNFRSF10A, TNFRSF10B, TNFSF10* | Malignant OS in metastatic niche | *MCL1* in metastatic niches; TRAIL receptors as targets (PMID 41231422) |
| **Amplification-linked** | *MDM2, CDK4, MYC, RUNX2, VEGFA* | Malignant OS | Diagnostic/therapeutic relevance (PMID 35049602) |
| **Fibrosis/niche** | *FN1, TGFB1, TGFB2, ITGB6, LOX, SERPINE1, CTHRC1* | Epithelial ADI/ABC, myofibroblast, malignant | PMID 39540841; PMID 41168897 |
| **Antigen presentation / IFN** | *HLA-A/B/C, B2M, TAP1, NLRC5, STAT1, ISG15* | Malignant OS | IFN induction correlated with improved OS survival (DOI 10.1158/2767-9764.CRC-25-0294) |

---

## 13. Copy-paste ready signature object (R / Seurat)

```r
sigs <- list(
  # ---- Malignant osteosarcoma ----
  OS_osteoblastic   = c("COL1A1","COL1A2","COL5A2","CDH11","RUNX2","SATB2","SP7","ALPL","IBSP","SPP1","POSTN","OMD","MEPE","COL11A1"),
  OS_chondroblastic = c("ACAN","COL2A1","COL9A1","COL9A3","COL11A1","SOX9","CYTL1","WIF1","EPYC","SNORC"),
  OS_proliferating  = c("MKI67","TOP2A","CENPF","UBE2C","TYMS","RRM2","CDK1","HMGB2"),
  OS_MSClike        = c("CXCL12","SFRP2","MME","THY1","NES","PRRX1","CD44","ALDH1A1","PROM1"),
  OS_UPR            = c("ATF6","XBP1","HSPA5","DDIT3","ATF4","HERPUD1","EDEM1","SEL1L","MANF","PDIA4"),
  OS_EMT_invasive   = c("VIM","FN1","SPARC","TIMP1","SERPINE1","LOX","LOXL2","TNC","THBS2","ZEB1","SNAI2","CD24"),
  OS_hypoxia        = c("VEGFA","SLC2A1","LDHA","PGK1","ENO1","NDRG1","ADM","BNIP3","CA9"),

  # ---- Bone-lineage / osteoclast ----
  Osteoclast        = c("CTSK","ACP5","MMP9","ATP6V0D2","DCSTAMP","OCSTAMP","SIGLEC15","CALCR","TCIRG1","CA2","NFATC1","ITGB3"),

  # ---- Stroma ----
  Fibroblast_pan    = c("DCN","LUM","COL1A1","COL3A1","COL6A3","FBLN1","PDGFRA","MMP2"),
  CAF_myCAF         = c("ACTA2","TAGLN","MYL9","POSTN","CTHRC1","TNC","COL10A1","COL11A1","INHBA","LRRC15","FAP","THBS2","COMP","LOX"),
  CAF_iCAF          = c("CXCL12","CXCL14","IL6","CXCL1","CXCL2","CFD","C3","C7","HAS1","DPT","APOD","CLU","PLA2G2A"),
  CAF_apCAF         = c("HLA-DRA","HLA-DRB1","HLA-DPA1","CD74","SLPI"),
  Fib_alveolar      = c("NPNT","WNT2","FGF10","TCF21","GPC3","LIMCH1","SCN7A"),
  Fib_adventitial   = c("PI16","SCARA5","SERPINF1","MFAP5","CD34","ELN","DPT"),
  MSC_osteoprog     = c("CXCL12","SFRP2","MME","THY1","ENG","NT5E","LEPR","GREM1","KITLG","PDGFRB"),
  Pericyte          = c("RGS5","NOTCH3","PDGFRB","HIGD1B","KCNJ8","CSPG4","COX4I2","NDUFA4L2"),
  SMC               = c("MYH11","ACTG2","CNN1","DES","LMOD1","TAGLN"),
  Mesothelial       = c("UPK3B","MSLN","WT1","CALB2","ITLN1","PRG4","LRRN4"),

  # ---- Endothelium ----
  EC_pan            = c("PECAM1","CDH5","CLDN5","VWF","EGFL7","RAMP2","ERG","SOX17"),
  EC_gCap           = c("FCN3","CA4","IL7R","EDN1","GPIHBP1","SLC6A4"),
  EC_aerocyte       = c("HPGD","EDNRB","S100A3","SOSTDC1","IL1RL1","TBX2"),
  EC_arterial       = c("GJA5","DKK2","HEY1","SOX17","EFNB2","SERPINE2","IGFBP3"),
  EC_venous         = c("ACKR1","PLVAP","VCAM1","SELP","CPE","NR2F2"),
  EC_lymphatic      = c("PROX1","PDPN","LYVE1","CCL21","MMRN1","FLT4","TFF3"),
  EC_tip            = c("ESM1","APLN","ANGPT2","CXCR4","DLL4","NID2","PGF","INSR"),

  # ---- Lung epithelium ----
  AT1               = c("AGER","PDPN","CAV1","CLIC5","SPOCK2","EMP2","HOPX","RTKN2","SCEL"),
  AT2               = c("SFTPC","SFTPB","SFTPA1","SFTPA2","NAPSA","LAMP3","PGC","ABCA3","ETV5","SLC34A2"),
  Club              = c("SCGB1A1","SCGB3A2","SCGB3A1","BPIFB1","MGP","TFF3","WFDC2"),
  Goblet            = c("MUC5AC","MUC5B","SPDEF","TFF1","AGR2","CEACAM5"),
  Ciliated          = c("FOXJ1","TPPP3","PIFO","CAPS","SNTN","DNAI1","RSPH1","C20orf85"),
  Basal             = c("KRT5","KRT14","KRT15","TP63","S100A2","DLK2","MIR205HG"),
  PNEC              = c("CALCA","ASCL1","CHGA","CHGB","SYP","INSM1","GRP"),
  Ionocyte          = c("FOXI1","CFTR","ASCL3","ATP6V1G3","TMEM61"),
  Tuft              = c("POU2F3","ASCL2","TRPM5","AVIL","LRMP"),
  Epi_ADI_KRT8      = c("KRT8","KRT18","CLDN4","CDKN1A","SFN","KRT7","SPRR1A","SPRR1B","MDK","GDF15"),
  Epi_aberrantBasal = c("KRT17","VIM","FN1","ITGB6","CDH2","PRSS2","MMP7","GDF15","SOX9","TP63"),

  # ---- Myeloid ----
  Mac_alveolar      = c("FABP4","MARCO","MCEMP1","PPARG","MSR1","MRC1","CIDEC","OLR1","SERPING1"),
  Mac_FOLR2_C1QC    = c("C1QA","C1QB","C1QC","FOLR2","LYVE1","SELENOP","F13A1","MAF","CCL13"),
  TAM_SPP1_TREM2    = c("SPP1","TREM2","GPNMB","APOE","APOC1","CD9","LGALS3","FABP5","MMP9","CHI3L1"),
  TAM_IFN           = c("CXCL9","CXCL10","CXCL11","GBP1","GBP5","STAT1","IDO1","ISG15","IFIT1","IFIT3","MX1"),
  TAM_angiogenic    = c("VEGFA","VCAN","THBS1","HIF1A","SLC2A1","EREG","INHBA","CD300E"),
  Mono_classical    = c("CD14","S100A8","S100A9","S100A12","VCAN","FCN1","LYZ","SELL"),
  Mono_nonclassical = c("FCGR3A","LST1","MS4A7","CDKN1C","LILRB2","TCF7L2"),
  cDC1              = c("CLEC9A","XCR1","CADM1","BATF3","WDFY4"),
  cDC2              = c("CD1C","FCER1A","CLEC10A","CD1E","FCGR2B"),
  mregDC_LAMP3      = c("LAMP3","CCR7","CD40","CD83","FSCN1","IL4I1","IDO1","CCL19","CCL22","BIRC3"),
  pDC               = c("LILRA4","CLEC4C","IL3RA","GZMB","JCHAIN","IRF7","TCF4","SERPINF1"),
  Mast              = c("TPSAB1","TPSB2","CPA3","MS4A2","KIT","CMA1","HPGDS"),
  Neutrophil_TAN    = c("FCGR3B","CSF3R","CXCR2","IL1R2","MMP9","PROK2","S100A12","IFITM2","CD83"),

  # ---- Lymphoid ----
  Tcell_pan         = c("CD3D","CD3E","CD3G","CD2","TRAC","TRBC2","IL7R"),
  T_naive           = c("CCR7","SELL","TCF7","LEF1","MAL","NOSIP"),
  Treg              = c("FOXP3","IL2RA","IKZF2","CTLA4","TIGIT","TNFRSF4","TNFRSF9","LAYN","CCR8","IL1R2"),
  CD4_Tfh_CXCL13    = c("CXCL13","IL21","BCL6","TOX2","CD200","ICOS","PDCD1","MAF"),
  CD4_Th17          = c("IL17A","IL17F","RORC","CCR6","KLRB1","IL23R","CTSH"),
  CD8_Tem_GZMK      = c("GZMK","GZMA","CCL5","EOMES","CST7","CXCR4","KLRG1"),
  CD8_Trm           = c("ZNF683","ITGAE","CXCR6","CD69","ITGA1","XCL1","XCL2"),
  CD8_Tex           = c("PDCD1","HAVCR2","LAG3","CTLA4","TIGIT","TOX","LAYN","ENTPD1","CXCL13","GZMB"),
  CD8_Temra         = c("FGFBP2","CX3CR1","GZMH","KLRG1","FCGR3A","TBX21","PRF1","NKG7"),
  MAIT              = c("SLC4A10","KLRB1","ZBTB16","NCR3","TRAV1-2","RORC"),
  gdT               = c("TRDC","TRGC1","TRGC2","TRDV2","TRGV9","KLRC1"),
  NK_cytotoxic      = c("FGFBP2","FCGR3A","KLRF1","GNLY","PRF1","SPON2","CX3CR1","KLRD1","S1PR5"),
  NK_resident       = c("NCAM1","XCL1","XCL2","GZMK","SELL","KLRC1","CD160","ITGA1"),
  B_naive           = c("MS4A1","IGHD","TCL1A","FCER2","IL4R","CD79A","CD79B"),
  B_memory          = c("CD27","TNFRSF13B","AIM2","CD24"),
  B_GC              = c("AICDA","RGS13","MEF2B","LMO2","S1PR2","BCL6"),
  Plasma            = c("MZB1","JCHAIN","DERL3","XBP1","SEC11C","PRDM1","TNFRSF17","SDC1","IGHG1","IGKC"),
  TLS_module        = c("CXCL13","CCL19","CCL21","CR2","LTB","CXCR5","SELL","MS4A1","LAMP3","CCR7"),

  # ---- Other / technical ----
  Erythroid         = c("HBB","HBA1","HBA2","ALAS2","AHSP"),
  Platelet          = c("PPBP","PF4","ITGA2B","GP9","TUBB1"),
  Myocyte           = c("MYL1","MYLPF","TNNT1","TNNT3","ACTA1","TTN","MYOD1"),
  Cycling           = c("MKI67","TOP2A","CCNB1","CENPF","UBE2C","PCNA","TYMS","STMN1","RRM2"),
  DissocStress      = c("FOS","FOSB","JUN","JUNB","EGR1","ATF3","HSPA1A","HSPA1B","DNAJB1","HSPB1","SOCS3","ZFP36")
)
```

---

## 14. Expected cluster composition for *this* specimen (prior expectations)

| Compartment | Expected abundance | Basis |
|---|---|---|
| Malignant osteoblastic OS | High (dominant malignant population) | PMID 42272640; PMID 33303760 |
| Malignant chondroblastic OS | Variable; possible if primary had chondroblastic component | PMID 33303760 |
| Osteoclasts | **Low** (reduced in lung mets vs primary) | PMID 33303760 |
| Fibroblasts / CAFs | **Increased** vs primary | PMID 42424801 |
| Mast cells | **Increased** vs primary | PMID 42424801 |
| T/NK cells | **Increased** vs primary; exhaustion-skewed, TIGIT-high | PMID 42424801; PMID 33303760 |
| Myeloid overall | **Decreased** proportion vs primary, but with **FABP4⁺ macrophage enrichment** and SPP1⁺ profibrotic TAMs | PMID 42424801; PMID 33303760; PMID 37291214 |
| Resident lung epithelium (AT1/AT2/club/ciliated) | Present, proportion depends on tumor:normal ratio in the core | PMID 33208946; PMID 37291214 |
| Transitional/aberrant basaloid epithelium | Present at metastasis interface | PMID 39540841; PMID 41519994 |
| Myofibroblasts/fibrosis | Present (metastasis-induced fibrosis) | PMID 39540841 |
| Skeletal myoblasts | Should be **absent** (bone/limb-specific cluster) | PMID 33303760 |

Deviations from these priors are themselves informative and worth reporting.

---

## 15. Key caveats

1. **No single gene is definitive.** Use ≥5-gene modules with a permutation/control-gene background (UCell/AUCell), and report score distributions, not binary calls.
2. **Marker sharing across lineages** is the main source of error here: *SPP1* (OS cells, TAMs, AT2 injury), *ACTA2* (myCAF, pericyte, SMC, myoblast), *ATP6V0D2* (osteoclast, ionocyte), *KRT17* (basal, aberrant basaloid), *FABP4* (alveolar macrophage, adipocyte-like stroma, endothelium), *LAMP3* (AT2 and mregDC — a classic and dangerous collision in lung samples), *CD74/HLA-DR* (apCAF, myeloid, B).
3. **Pro-angiogenic TAM markers are cancer-type-specific**, so panels transferred from other tumors may fail (PMID 33545035).
4. **SATB2/SOX9 caveats** (see §4.2) apply equally at the transcript level.
5. **Neutrophils** are systematically under-captured and transcriptomically shallow (PMID 41397978); consider protein-based or CITE-seq confirmation.
6. **Osteosarcoma is CNV-driven, not fusion-driven** — CNV-based malignant calling is more informative here than in translocation sarcomas, but subclonal CNV heterogeneity can split one tumor into several "cell types." Always sanity-check malignant subclusters against patient/sample identity and doublet scores.
7. **Prefer patient-matched, consortium-level references** (HLCA; pan-cancer T/myeloid atlases) over ad hoc marker lists from small single-sample studies, several of which are based on a single public sample (e.g., PMID 42472256 uses one GSM from GSE152048) and should be treated as hypothesis-generating.

---

## 16. References (peer-reviewed)

**Osteosarcoma single-cell atlases and biology**
1. Zhou Y, Yang D, Yang Q, et al. Single-cell RNA landscape of intratumoral heterogeneity and immunosuppressive microenvironment in advanced osteosarcoma. *Nat Commun.* 2020;11:6322. **PMID 33303760**. (Author Correction: *Nat Commun.* 2021;12:2567. **PMID 33931654**.)
2. Liu F, Zhang T, Yang Y, et al. Integrated analysis of single-cell and bulk transcriptomics reveals cellular subtypes and molecular features associated with osteosarcoma prognosis. *BMC Cancer.* 2025;25:280. **PMID 39962461**.
3. Li X, Liu J, Wang Y, Hu J, Wang Q. Molecular characterization of cell dynamics during osteosarcoma progression. *Transl Oncol.* 2026;71:102899. **PMID 42424801**.
4. Li H, Sun C, Yang M. Single-cell transcriptomic profiling reveals cellular heterogeneity and identifies novel therapeutic targets in osteosarcoma. *Int J Genomics.* 2026;2026:4040246. **PMID 42472256**.
5. Li X, Li G, Peng T, et al. Heterogeneity-based stratification identifies CKMT2 as a prognostic marker in osteosarcoma. *Front Cell Dev Biol.* 2026;14:1822741. **PMID 42272640**.
6. Saito M, Nakasuka F, Sankoda N, et al. Inherent tissue homeostasis of the juvenile metaphysis provides a foundation for osteosarcoma development. *Nat Commun.* 2026;17:6241. **PMID 42363015**.
7. Ferrena A, Zhang R, Wang J, et al. Single-cell RNA analysis of murine osteosarcoma uncovers Skp2 function in metastasis, genomic instability, and immune activation and reveals additional target pathways. *Cancer Res Commun.* 2026;6:923–945. DOI 10.1158/2767-9764.CRC-25-0294.
8. Orrapin S, Moonmuang S, Udomruk S, et al. Unlocking the tumor-immune microenvironment in osteosarcoma: insights into the immune landscape and mechanisms. *Front Immunol.* 2024;15:1394284. **PMID 39359731**.
9. Asmar C, Awad G, Boutros M, et al. Single-cell RNA sequencing in osteosarcoma: applications in diagnosis, prognosis, and treatment. *Med Oncol.* 2025;42:551. **PMID 41231422**.
10. Zhang H, Wu S, Luo D, Guo J. Computational discovery of novel colony-stimulating factor-1 receptor as a potential therapeutic biomarker in osteosarcoma and a novel inhibitor from herbal sources. *Oncol Lett.* 2026;31:263. **PMID 42100022**.
11. Yingkai X, Jianfeng J, Zhiyong H, Zhifeng Z, Lei W. Identification of endothelial INSR as an osteosarcoma-related biomarker and therapeutic target based on WGCNA. *Discov Oncol.* 2025;16:1594. **PMID 40846806**.

**Osteosarcoma lung metastatic niche**
12. Reinecke JB, Jimenez Garcia L, Gross AC, et al. Aberrant activation of wound-healing programs within the metastatic niche facilitates lung colonization by osteosarcoma cells. *Clin Cancer Res.* 2025;31:414–429. **PMID 39540841**. (Preprint: *bioRxiv* 2024. **PMID 38260361**.)

**Human lung references**
13. Travaglini KJ, Nabhan AN, Penland L, et al. A molecular cell atlas of the human lung from single-cell RNA sequencing. *Nature.* 2020;587:619–625. **PMID 33208946**.
14. Sikkema L, Ramírez-Suástegui C, Strobl DC, et al. An integrated cell atlas of the lung in health and disease. *Nat Med.* 2023;29:1563–1577. **PMID 37291214**.

**Injury/fibrosis epithelial states**
15. Peng F, Jiang CS, Zheng Z, et al. Transcriptomic signature-guided depletion of intermediate alveolar epithelial cells ameliorates pulmonary fibrosis in mice. *Nat Commun.* 2026;17:1636. **PMID 41519994**.
16. Wu B, Shichino S, Ueha S, et al. Ex vivo lung-organoid model for aberrant basaloid cell induction and activation. *Inflamm Regen.* 2025;45:33. **PMID 41168897**.
17. Khan P, Roux J, Blumer S, et al. Alveolar basal cells differentiate towards secretory epithelial- and aberrant basaloid-like cells in vitro. *Cells.* 2022;11:1820. DOI 10.3390/cells11111820.

**Tumor stroma / CAF / endothelium**
18. Lambrechts D, Wauters E, Boeckx B, et al. Phenotype molding of stromal cells in the lung tumor microenvironment. *Nat Med.* 2018;24:1277–1289. **PMID 29988129**.
19. Qian J, Olbrecht S, Boeckx B, et al. A pan-cancer blueprint of the heterogeneous tumor microenvironment revealed by single-cell profiling. *Cell Res.* 2020;30:745–762. **PMID 32561858**.
20. Elyada E, Bolisetty M, Laise P, et al. Cross-species single-cell analysis of pancreatic ductal adenocarcinoma reveals antigen-presenting cancer-associated fibroblasts. *Cancer Discov.* 2019;9:1102–1123. **PMID 31197017**.

**Immune references**
21. Zheng L, Qin S, Si W, et al. Pan-cancer single-cell landscape of tumor-infiltrating T cells. *Science.* 2021;374:abe6474. **PMID 34914499**.
22. Cheng S, Li Z, Gao R, et al. A pan-cancer single-cell transcriptional atlas of tumor infiltrating myeloid cells. *Cell.* 2021;184:792–809.e23. **PMID 33545035**.
23. Nie RC, Hu GS, Cao SQ, Wang A, Wang DC, Liu W. Spatial single-cell landscape of tumor-associated macrophages and their crosstalk with the tumor microenvironment. *Cell Discov.* 2026;12:35. **PMID 42156717**.
24. Bi W, Li X, Zhao H, Han Q, Zhang J. Heterogeneous neutrophils: key players in regulating tumor immunity. *Biochim Biophys Acta Rev Cancer.* 2026;1881:189538. **PMID 41571211**.
25. Wang Y, Meng Y, Chen K, et al. Pan-cancer single-cell transcriptomic analysis reveals CD83 as a hallmark of tumor-associated neutrophils with senescent and pro-tumor properties. *Comput Struct Biotechnol J.* 2025;27:4615–4632. DOI 10.1016/j.csbj.2025.10.056.
26. Sadiku P, Brenes AJ, Mayer RL, et al. Single cell proteomic analysis defines discrete neutrophil functional states in human glioblastoma. *Nat Commun.* 2025;17:621. **PMID 41397978**.
27. Lu F, Zhang T, Li Z, et al. Integrative single-cell and spatial transcriptomic analysis identifies a tertiary lymphoid structure-associated LAMP3⁺CCR7⁺ mregDC antigen-presentation program in ovarian cancer. *Cancers (Basel).* 2026;18:2259. **PMID 42512324**.
28. Sambanthamoorthy S, Ren Y, Galvez TK, et al. The presence of CD11c⁺ B cells with potent effector memory phenotype in lung adenocarcinoma correlates with overall patient survival. *Cancer Immunol Res.* 2026;14:811–826. **PMID 41686183**.
29. Tao T, Zhu L, Shen D, et al. A B cell–IgA–epithelial axis enhances antitumor immunity and improves outcome in HPV-associated penile squamous cell carcinoma. *Nat Commun.* 2025;17:624. **PMID 41381565**.

**Osteoclast biology**
30. Aol L, Zhou X, Cao Z, et al. LncRNA ZFAS1 promotes alveolar bone resorption by enhancing osteoclastogenesis in periodontitis. *J Cell Physiol.* 2026;241:e70134. **PMID 41549697**.

**Diagnostic marker validity (SATB2/SOX9/MDM2)**
31. Sharma AE, Pytel P, Cipriani NA. SOX9 and SATB2 immunohistochemistry cannot reliably distinguish between osteosarcoma and chondrosarcoma on biopsy material. *Hum Pathol.* 2022;121:56–64. DOI 10.1016/j.humpath.2021.12.011.
32. Szczepanski JM, Siddiqui J, Patel RM, et al. Expression of SATB2 in primary cutaneous sarcomatoid neoplasms: a potential diagnostic pitfall. *Pathology.* 2023;55:350–354. **PMID 36732203**.
33. Owosho AA, Ladeji AM, Adesina OM, et al. SATB2 and MDM2 immunoexpression and diagnostic role in primary osteosarcomas of the jaw. *Dent J (Basel).* 2021;10:4. **PMID 35049602**.
34. Ichikawa J, Kawasaki T, Onohara K, et al. Diagnostic challenges in imaging and immunohistopathological profiles in extraskeletal osteosarcoma. *World J Surg Oncol.* 2024;22:307. **PMID 39568020**.
35. Shank AMM, Snook E, Cavender K, et al. Special AT-rich sequence-binding protein 2 immunohistochemistry in the diagnosis of osteosarcoma in dogs. *J Comp Pathol.* 2024;215:14–29. **PMID 39368249**.

**Therapeutic target context**
36. Xie Y, Wang H, Zeng F, et al. Exploiting B7-H3: molecular insights and immunotherapeutic strategies for osteosarcoma. *Bioengineering (Basel).* 2025;12:1344. **PMID 41463642**.
37. Talbot LJ, Chabot A, Ross AB, et al. Redirecting B7-H3.CAR T cells to chemokines expressed in osteosarcoma enhances homing and antitumor activity in preclinical models. *Clin Cancer Res.* 2024;30:4434–4449. **PMID 39101835**.
38. Lake JA, Woods E, Hoffmeyer E, et al. Directing B7-H3 chimeric antigen receptor T cell homing through IL-8 induces potent antitumor activity against pediatric sarcoma. *J Immunother Cancer.* 2024;12:e009221. DOI 10.1136/jitc-2024-009221.
39. Luan S, Zhao Y, Yu Y, et al. The relevance of B7-H3 and tumor-associated macrophages in the tumor immune microenvironment of solid tumors. *Am J Transl Res.* 2025;17:2835–2849. **PMID 40385054**.
40. De Maria R, Donini C, Capellero S, et al. Development and activity of canine B7-H3-CAR.CIK lymphocytes against sarcomas. *Cancer Immunol Immunother.* 2025;74:306. **PMID 40944715**.
41. Luo W, Zhang HF, Li W, et al. Circumventing Ewing sarcoma tumor microenvironment resistance by IL1RAP CAR-modified TGFβ1-imprinted natural killer cells in combination with IL-15 agonist and anti-GD2 antibody. *J Immunother Cancer.* 2026;14:e014633. **PMID 42398968**.

**Marker databases**
42. Hu C, Li T, Xu Y, et al. CellMarker 2.0: an updated database of manually curated cell markers in human/mouse and web tools based on scRNA-seq data. *Nucleic Acids Res.* 2023;51:D870–D876. **PMID 36300619**.
43. Zhang X, Lan Y, Xu J, et al. CellMarker: a manually curated resource of cell markers in human and mouse. *Nucleic Acids Res.* 2019;47:D721–D728. **PMID 30289549**.

---

## 17. Suggested deliverable per cluster

For each cluster, report: `cluster_id | n_cells | top-20 DEGs | best-matching signature (score, z) | second-best (score) | CNV status | reference-mapping label (HLCA / pan-cancer T / myeloid) | final call | confidence | notes/caveat`.

Flag as **"requires orthogonal validation"** any cluster where (a) top and second-best module scores differ by <1 SD, (b) CNV status is ambiguous, or (c) the call depends on a single collision-prone gene (*LAMP3, SPP1, ACTA2, KRT17, ATP6V0D2, FABP4*).