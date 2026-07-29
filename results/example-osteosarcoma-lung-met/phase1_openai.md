# Gene-signature report for annotating scRNA-seq/snRNA-seq from a right-lung biopsy in metastatic osteosarcoma

**Assumption:** human gene-expression single-cell or single-nucleus data. Gene symbols below are HGNC-style. Literature coverage is through mid-2024.

## 1. Recommended annotation logic

For this clinical context, do **not** call malignant osteosarcoma cells using collagen/ECM genes alone, because osteosarcoma cells, lung fibroblasts, and CAFs can all express `COL1A1`, `COL1A2`, `SPARC`, `POSTN`, `FN1`, `THBS2`, etc. A robust workflow is:

1. **Gate major compartments** using high-specificity parent markers:  
   `PTPRC` immune; `EPCAM/KRT8/KRT18/KRT19` epithelial; `PECAM1/CDH5/VWF` endothelial; `DCN/LUM/PDGFRA` fibroblast; `RGS5/PDGFRB/CSPG4` pericyte; `ACTA2/MYH11/CNN1` smooth muscle; `HBA/HBB` erythroid; `PPBP/PF4` platelet.
2. **Identify malignant osteosarcoma** by combining:
   - inferred copy-number aberrations / aneuploidy from expression data,
   - absence of canonical host-lineage programs,
   - osteogenic/osteosarcoma programs: `SATB2`, `RUNX2`, `SP7`, `ALPL`, `IBSP`, `BGLAP`, `SPP1`, `COL1A1`, `COL1A2`, `SPARC`, `CDH11`, `POSTN`, `MMP13`.
3. **Subcluster tumor cells separately** to resolve osteoblastic, chondroblastic, fibroblastic/ECM-rich, hypoxic/invasive, and proliferating tumor states.
4. **Subcluster immune, epithelial, stromal, and vascular cells separately**, then annotate with lineage-specific markers.
5. Validate clinically important calls with histology/IHC/IF where possible: SATB2/RUNX2/ALPL/osteocalcin for osteogenic tumor, CD45/CD3/CD68/CD31/EPCAM/pan-keratin/FAP/αSMA/TRAP/CTSK as needed.

Key supporting literature: osteosarcoma heterogeneity and genomics [1–8], osteoblast/chondrocyte/osteoclast biology [9–17], lung cell atlases [19–31], lung tumor microenvironment atlases [32–37], immune-cell atlases [38–47], CAF/fibroblast studies [48–52], and scRNA CNV methods [53–56].

---

## 2. Major-compartment signatures

| Compartment / broad identity | Core positive markers | Useful negative/deconfounding markers | Notes |
|---|---|---|---|
| **Malignant osteosarcoma cells** | `SATB2`, `RUNX2`, `SP7`, `ALPL`, `IBSP`, `BGLAP`, `SPP1`, `COL1A1`, `COL1A2`, `SPARC`, `CDH11`, `POSTN`, `MMP13` + inferred CNV/aneuploidy | Usually `PTPRC−`, `PECAM1−`, `CDH5−`; often `EPCAM−/low`, but verify | Use CNV/aneuploidy because ECM genes overlap fibroblasts/CAFs [1–12,53–56]. |
| **Immune cells** | `PTPRC`, then lineage markers: T/NK/B/myeloid | `EPCAM`, `PECAM1`, strong collagen-only programs | PTPRC is the main parent gate. Plasma cells can be lower for `PTPRC`. |
| **Lung epithelial cells** | `EPCAM`, `KRT8`, `KRT18`, `KRT19`, `CLDN4`, `TACSTD2` | `PTPRC`, `PECAM1`, `COL1A1`-only | Subtype as AT1, AT2, club, ciliated, basal, goblet, etc. [19–27]. |
| **Endothelial cells** | `PECAM1`, `CDH5`, `VWF`, `CLDN5`, `ESAM`, `KDR`, `RAMP2` | `PTPRC`, `EPCAM` | Subtype into capillary, arterial, venous, lymphatic, angiogenic [19,20,28–30]. |
| **Fibroblasts / CAFs** | `COL1A1`, `COL1A2`, `COL3A1`, `DCN`, `LUM`, `PDGFRA`, `DPT`, `C1R`, `C1S`, `FBLN1` | Inferred CNV, strong `SATB2/RUNX2/SP7/ALPL` suggest tumor rather than host fibroblast | Critical differential diagnosis vs fibroblastic osteosarcoma [1,32,48–52]. |
| **Pericytes** | `RGS5`, `PDGFRB`, `CSPG4`, `MCAM`, `NOTCH3`, `ABCC9`, `KCNJ8` | Strong `MYH11/CNN1` favors smooth muscle | Vascular mural cells. |
| **Smooth muscle cells** | `ACTA2`, `TAGLN`, `MYH11`, `CNN1`, `DES`, `ACTG2`, `LMOD1`, `SMTN` | `RGS5/PDGFRB` high favors pericyte; tumor CNV favors malignant spindle/ECM cell | Bronchovascular smooth muscle or myofibroblast-like states. |
| **Mesothelial / pleural cells** | `MSLN`, `WT1`, `CALB2`, `UPK3B`, `KRT8`, `KRT18`, `PDPN`, `LRRN4` | `PTPRC`, `PECAM1`; epithelial carcinoma requires CNV + carcinoma markers | Relevant if pleural tissue sampled. |
| **Erythroid / RBC contamination** | `HBA1`, `HBA2`, `HBB`, `HBD`, `ALAS2`, `AHSP` | Most other lineage markers absent | Usually contamination or blood-rich biopsy. |
| **Platelet / megakaryocyte signal** | `PPBP`, `PF4`, `GP9`, `ITGA2B`, `TUBB1`, `NRGN` | Coexpression with another lineage often platelet adherence/doublet | Common in biopsies. |

---

## 3. Malignant osteosarcoma and tumor-state signatures

| Tumor signature / state | Gene signature | Interpretation and caveats | Key refs |
|---|---|---|---|
| **Core malignant osteosarcoma / osteogenic sarcoma** | `SATB2`, `RUNX2`, `SP7`, `ALPL`, `IBSP`, `BGLAP`, `SPP1`, `COL1A1`, `COL1A2`, `SPARC`, `CDH11`, `POSTN`, `MMP13` | Best used in `PTPRC−/EPCAM−/PECAM1−` cells with inferred CNV. `BGLAP` may drop out. `SATB2` is not entirely specific; epithelial `SATB2+` cells with `EPCAM/KRT/CDX2` would raise colorectal differential. | [1–12] |
| **Osteoblastic / osteoid-producing program** | `RUNX2`, `SP7`, `SATB2`, `ALPL`, `COL1A1`, `COL1A2`, `SPARC`, `IBSP`, `BGLAP`, `SPP1`, `MGP`, `BGN`, `DCN`, `BMP4`, `DLX5` | Classical osteoblastic osteosarcoma-like differentiation. Collagen genes alone are insufficient. | [1,2,9–12] |
| **Chondroblastic program** | `SOX9`, `SOX5`, `SOX6`, `ACAN`, `COL2A1`, `COL9A1`, `COL9A2`, `COL9A3`, `COL10A1`, `COL11A2`, `COMP`, `MATN3`, `CHAD`, `HAPLN1`, `IHH` | Suggests chondroblastic osteosarcoma differentiation if malignant/CNV-positive. Could also mark benign cartilage-like/entrapped tissue if diploid. | [1,2,13,14] |
| **Fibroblastic / spindle-cell / ECM-rich tumor program** | `COL1A1`, `COL1A2`, `COL3A1`, `COL5A1`, `COL5A2`, `COL6A3`, `FN1`, `TNC`, `THBS2`, `POSTN`, `MMP2`, `MMP11`, `MMP14`, `SERPINE1`, `FAP`, `PDPN`, `VCAN`, `CDH11` | Major pitfall: overlaps CAFs. Tumor calls need CNV and/or osteogenic markers. | [1,2,32,48–52] |
| **Proliferating high-grade tumor state** | `MKI67`, `TOP2A`, `UBE2C`, `CENPF`, `CDK1`, `CCNB1`, `CCNB2`, `BIRC5`, `TYMS`, `MCM2`, `MCM3`, `MCM4`, `MCM5`, `MCM6`, `MCM7`, `PCNA` | Proliferation is a state, not lineage. Also appears in cycling T/B/myeloid/epithelial cells. Score within malignant cells. | [1,53–56] |
| **Hypoxic / glycolytic tumor state** | `CA9`, `VEGFA`, `SLC2A1`, `LDHA`, `PDK1`, `NDRG1`, `BNIP3`, `HILPDA`, `ENO1`, `PGK1` | Often spatially localized; may correlate with necrosis/poor perfusion. Not specific to osteosarcoma. | [1,3,32] |
| **Inflammatory / invasive / matrix-remodeling tumor state** | `CXCL8`, `IL6`, `CXCL1`, `CXCL2`, `MMP9`, `MMP13`, `MMP14`, `LOX`, `SERPINE1`, `PLAUR`, `ITGA5`, `TNC`, `POSTN` | May overlap with CAFs and inflammatory myeloid cells; use parent lineage/CNV. | [1,32,42,43] |
| **IFN/MHC-responsive tumor state** | `HLA-A`, `HLA-B`, `HLA-C`, `B2M`, `STAT1`, `IRF1`, `ISG15`, `IFI6`, `IFIT1`, `IFIT2`, `IFIT3`, `MX1`, `CXCL9`, `CXCL10`; sometimes `HLA-DRA`, `CD74` | `HLA-DRA/CD74` can also mark B cells, macrophages, DCs, or antigen-presenting CAFs. If CNV-positive and `PTPRC−`, consider MHC-II+ tumor state. | [1,35,44,45] |
| **Mature osteocyte-like / ossified-matrix program, rare** | `DMP1`, `PHEX`, `SOST`, `MEPE`, `FGF23` | Rarely captured. If CNV-positive, may represent terminal osteogenic differentiation; if diploid, consider heterotopic/entrapped bone-like cells. | [9–12] |
| **MDM2/CDK4-amplified low-grade/dedifferentiated OS context** | `MDM2`, `CDK4`, `HMGA2` plus CNV amplification | Not universal in conventional high-grade osteosarcoma; useful if pathology suggests parosteal/low-grade central/dedifferentiated osteosarcoma. | [2,6–8] |

---

## 4. Lung epithelial and lung-resident cell signatures

| Cell type | Gene signature | Notes | Key refs |
|---|---|---|---|
| **Pan-epithelial** | `EPCAM`, `KRT8`, `KRT18`, `KRT19`, `CLDN4`, `TACSTD2`, `MUC1` | Parent gate for lung epithelial cells and possible epithelial malignancy. | [19–24] |
| **AT1 pneumocytes** | `AGER`, `PDPN`, `CAV1`, `CAV2`, `AQP5`, `HOPX`, `CLDN18`, `EMP2`, `RTKN2`, `CLIC5` | Gas-exchange epithelial cells. `PDPN` also occurs in lymphatics/mesothelium; use epithelial context. | [19,20,25,26] |
| **AT2 pneumocytes** | `SFTPA1`, `SFTPA2`, `SFTPB`, `SFTPC`, `SFTPD`, `ABCA3`, `SLC34A2`, `NAPSA`, `LAMP3`, `LPCAT1` | Surfactant genes can be ambient RNA in lung samples; require coexpression and epithelial identity. | [19,20,25,26] |
| **AT2/AT1 transitional or injury-associated epithelial cells** | `KRT8`, `KRT18`, `KRT19`, `CLDN4`, `CDKN1A`, `LGALS3`, `LCN2`, `SFN`, `TACSTD2` with reduced mature AT1/AT2 markers | Reactive/damage-associated state; can resemble carcinoma-like programs, so use CNV and pathology if expanded. | [25–27] |
| **Club / secretory airway cells** | `SCGB1A1`, `SCGB3A1`, `SCGB3A2`, `CYP2F1`, `BPIFA1`, `WFDC2`, `MUC5B` | Airway secretory lineage. `WFDC2` is not specific. | [19–24] |
| **Ciliated epithelial cells** | `FOXJ1`, `PIFO`, `TPPP3`, `RSPH1`, `DNAH5`, `DNAI1`, `CCDC39`, `CAPS`, `HYDIN` | Motile cilia program. | [19–24] |
| **Basal cells** | `KRT5`, `KRT14`, `KRT15`, `KRT17`, `TP63`, `NGFR`, `ITGA6`, `DST` | Proximal airway basal cells; also relevant to squamous metaplasia/carcinoma differential. | [19–24,31] |
| **Goblet / mucous cells** | `MUC5AC`, `MUC5B`, `SPDEF`, `AGR2`, `TFF3`, `CLCA1`, `FCGBP` | Secretory mucous lineage. | [19–24] |
| **Submucosal gland serous cells** | `LTF`, `LYZ`, `BPIFB1`, `MUC7`, `PRR4`, `AZGP1` | May appear if proximal airway/submucosal gland included. | [20,22] |
| **Pulmonary ionocytes** | `FOXI1`, `CFTR`, `ASCL3`, `ATP6V1B1`, `ATP6V0D2`, `BSND` | Rare CFTR-high airway epithelial cell type. | [23,24] |
| **Tuft cells** | `POU2F3`, `TRPM5`, `DCLK1`, `GFI1B`, `AVIL` | Rare chemosensory epithelial cells. | [19,20] |
| **Pulmonary neuroendocrine cells** | `ASCL1`, `INSM1`, `CHGA`, `CHGB`, `SYP`, `NCAM1`, `CALCA` | If expanded and aneuploid, consider neuroendocrine carcinoma differential. | [19,20,31] |
| **Possible lung adenocarcinoma differential** | `EPCAM`, `KRT8`, `KRT18`, `KRT19`, `NKX2-1`, `NAPSA`, `SFTPB`, `SFTPC`, `MUC1`, `CEACAM6` + CNV | Include because lung biopsy could rarely contain a second primary or epithelial metastasis. | [31–37] |
| **Possible squamous carcinoma differential** | `TP63`, `KRT5`, `KRT6A`, `KRT6B`, `KRT14`, `SOX2`, `DSG3` + CNV | Distinguish from basal cells by malignant CNV, expansion, and pathology. | [31–37] |

---

## 5. Immune-cell signatures

### 5.1 Lymphoid cells

| Cell type / state | Gene signature | Notes | Key refs |
|---|---|---|---|
| **Pan-immune** | `PTPRC` | Parent immune gate. | [38–43] |
| **Pan-T cells** | `CD3D`, `CD3E`, `CD3G`, `TRAC`, `TRBC1`, `TRBC2`, `CD2`, `CD247` | Parent T-cell gate. | [35,38,44,45] |
| **Naive / central-memory CD4 T cells** | `CD3D`, `CD4`, `IL7R`, `CCR7`, `SELL`, `TCF7`, `LEF1`, `LTB` | `CD4` is also in monocytes; require TCR/CD3 genes. | [35,44–47] |
| **CD8 cytotoxic T cells** | `CD3D`, `CD8A`, `CD8B`, `NKG7`, `PRF1`, `GZMB`, `GZMH`, `GNLY`, `CST7`, `CCL5` | Distinguish from NK by TCR/CD3 genes. | [35,44,45] |
| **GZMK+ effector-memory T cells** | `GZMK`, `CCL5`, `NKG7`, `CD8A`, `CXCR3`, `EOMES` | Common intermediate cytotoxic-memory state in tumors. | [35,44,45] |
| **Exhausted / tumor-reactive T cells** | `PDCD1`, `LAG3`, `HAVCR2`, `TIGIT`, `CTLA4`, `TOX`, `CXCL13`, `ENTPD1`, `TNFRSF9`, `ITGAE` | Activated cells can transiently express checkpoint genes; interpret with clonality/state. | [35,44,45,47] |
| **Regulatory T cells** | `FOXP3`, `IL2RA`, `CTLA4`, `IKZF2`, `TIGIT`, `TNFRSF18`, `CCR8`, `BATF` | Tumor Tregs often `CCR8/TNFRSF18` high. `FOXP3` may drop out. | [35,46,47] |
| **Tissue-resident memory T cells** | `ITGAE`, `CD69`, `CXCR6`, `ZNF683`, `XCL1`, `XCL2` | Common in lung/tumor tissue. | [35] |
| **γδ T cells** | `TRDC`, `TRGC1`, `TRGC2`, `TRDV2`, `CD3D`, `NKG7` | May be cytotoxic. | [35,38] |
| **MAIT-like T cells** | `TRAV1-2`, `KLRB1`, `SLC4A10`, `DPP4`, `IL18RAP`, `ZBTB16` | Confirm with TCR if available. | [38,58] |
| **NK cells** | `NKG7`, `GNLY`, `PRF1`, `GZMB`, `KLRD1`, `KLRF1`, `NCR1`, `FCGR3A`, `TYROBP`; `CD3D/TRAC−` | `FCGR3A` also occurs in monocytes/macrophages; require NK program and absent TCR. | [38,40,58] |
| **B cells** | `MS4A1`, `CD79A`, `CD79B`, `CD19`, `CD22`, `BANK1`, `CD74`, `HLA-DRA`, `TCL1A`, `IGHD`, `IGHM` | `CD74/HLA-DRA` are not B-specific. | [38,58] |
| **Germinal-center B cells** | `BCL6`, `AICDA`, `RGS13`, `MEF2B`, `MKI67` | May indicate tertiary lymphoid structures if accompanied by T/B organization. | [58] |
| **Plasma cells / plasmablasts** | `JCHAIN`, `MZB1`, `XBP1`, `PRDM1`, `SDC1`, `IGHG1`, `IGHG3`, `IGHA1`, `IGKC`, `IGLC2` | Often very high immunoglobulin RNA; can generate ambient Ig signal. | [38,58] |
| **ILC/ILC2-like, rare** | `IL7R`, `RORA`, `GATA3`, `IL1RL1`, `KIT`, `KLRB1`; absent `CD3D/TRAC` | Rare in tumor biopsies; use cautiously. | [19,20,58] |

### 5.2 Myeloid, granulocyte, mast, and osteoclast-lineage cells

| Cell type / state | Gene signature | Notes | Key refs |
|---|---|---|---|
| **Classical inflammatory monocytes** | `LYZ`, `LST1`, `S100A8`, `S100A9`, `S100A12`, `FCN1`, `VCAN`, `CD14`, `CCR2`, `LILRB2` | Can resemble monocytic MDSC-like states in tumors. | [38–43] |
| **Non-classical / patrolling monocytes** | `FCGR3A`, `CX3CR1`, `MS4A7`, `LST1`, `LILRB1`, `IFITM3`, `RHOC` | Distinguish from NK by myeloid genes and lack of `NKG7/GNLY` dominance. | [38–43] |
| **Pan-macrophage** | `C1QA`, `C1QB`, `C1QC`, `APOE`, `CD68`, `CSF1R`, `AIF1`, `MRC1`, `CD163`, `LYZ` | Parent macrophage program. | [29,33,40–43] |
| **Alveolar macrophages** | `MARCO`, `FABP4`, `PPARG`, `LPL`, `MRC1`, `MSR1`, `SIGLEC1`, `APOC1`, `APOE`, `MCEMP1` | Lung-resident; often abundant in lung biopsy. `FABP4` also appears in adipocytes, so use `PTPRC/C1Q` context. | [19,20,29,33,34] |
| **Interstitial / perivascular macrophages** | `F13A1`, `LYVE1`, `FOLR2`, `SELENOP`, `MRC1`, `MAFB`, `MS4A7`, `C1QA`, `C1QC` | Less `MARCO/FABP4` than alveolar macrophages. | [19,20,29,33,40] |
| **SPP1+/TREM2+ TAM / osteoclast-like macrophage program** | `SPP1`, `TREM2`, `GPNMB`, `APOE`, `LGALS3`, `CTSB`, `CTSL`, `MMP9`, `MMP12`, `CHI3L1`, `FABP5`, `LIPA` | `SPP1` is also tumor/AT2/CAF-associated; require myeloid markers. Highly relevant in tumor microenvironments. | [1,29,33,42,43] |
| **Inflammatory macrophages** | `IL1B`, `CXCL8`, `CCL3`, `CCL4`, `TNF`, `NLRP3`, `PTGS2`, `S100A8`, `S100A9` | Can overlap classical monocytes and dissociation/inflammation. | [33,40,42,43] |
| **MHC-II / antigen-presenting macrophages** | `HLA-DRA`, `HLA-DRB1`, `HLA-DPA1`, `HLA-DPB1`, `CD74`, `CD86`, `CIITA` with macrophage genes | Distinguish from DCs, B cells, apCAFs, and MHC-II+ tumor cells by parent markers. | [38–43] |
| **cDC1** | `CLEC9A`, `XCR1`, `BATF3`, `IRF8`, `CADM1`, `CLNK`, `IDO1` | Cross-presenting DC subset. | [38–41] |
| **cDC2** | `CD1C`, `FCER1A`, `CLEC10A`, `CD1E`, `HLA-DRA`, `IRF4`, `ITGAX` | Common tissue DC subset. | [38–41] |
| **Mature/migratory LAMP3+ DC** | `LAMP3`, `CCR7`, `FSCN1`, `CCL19`, `CCL17`, `CCL22`, `IDO1`, `IL4I1`, `CD83`, `CD40` | Tumor-draining/migratory DC state; `LAMP3` also in AT2 cells, so use `PTPRC/HLA` context. | [32,33,38–41] |
| **pDC** | `CLEC4C`, `LILRA4`, `IL3RA`, `TCF4`, `IRF7`, `GZMB` | Often low abundance. | [38–41] |
| **Mast cells** | `TPSAB1`, `TPSB2`, `CPA3`, `KIT`, `MS4A2`, `HDC` | Strong tryptase/chymase program. | [19,20,58] |
| **Basophils, rare** | `MS4A2`, `FCER1A`, `IL3RA`, `HDC`, `GATA2`, `CLC`; usually `KIT−/low`, `TPSB2−/low` | Distinguish from mast cells. | [38,58] |
| **Neutrophils / PMN-MDSC-like cells** | `S100A8`, `S100A9`, `FCGR3B`, `CSF3R`, `CXCR2`, `NAMPT`, `LCN2`, `CEACAM8`, `MPO`, `ELANE`, `OLR1` | Often undercaptured or fragile; `S100A8/A9` also monocytes. | [40–43] |
| **Eosinophils** | `CLC`, `PRG2`, `RNASE2`, `RNASE3`, `IL5RA`, `CCR3`, `SIGLEC8` | Rare but clinically interpretable. | [38,58] |
| **Osteoclasts / osteoclast-like giant cells** | `ACP5`, `CTSK`, `MMP9`, `DCSTAMP`, `OCSTAMP`, `ATP6V0D2`, `TNFRSF11A`, `CALCR`, `CA2`, `SIGLEC15`, `ITGB3`, `SPP1` plus myeloid genes | Important in osteosarcoma and giant-cell-rich lesions. Should be `PTPRC/CSF1R+` myeloid, not malignant OS cells. | [15–18] |

---

## 6. Stromal, vascular, and structural cell signatures

| Cell type / state | Gene signature | Notes | Key refs |
|---|---|---|---|
| **Pan-fibroblast** | `COL1A1`, `COL1A2`, `COL3A1`, `DCN`, `LUM`, `DPT`, `PDGFRA`, `COL6A1`, `COL6A2`, `COL6A3`, `C1R`, `C1S`, `FBLN1`, `FBLN2`, `CXCL14` | Diploid host fibroblasts. Distinguish from tumor by CNV and osteogenic markers. | [19,20,32,48–52] |
| **Alveolar fibroblast / lipofibroblast-like** | `PDGFRA`, `TCF21`, `WNT2`, `FGF7`, `ADH1B`, `PLIN2`, `LUM`, `DCN` | Normal lung mesenchyme. | [19,20,25,26] |
| **Adventitial / PI16+ fibroblast** | `PI16`, `DPP4`, `C7`, `CFD`, `SCARA5`, `CD34`, `CCL11`, `DPT` | Common fibroblast subtype across tissues. | [20,52] |
| **Myofibroblast** | `ACTA2`, `TAGLN`, `MYL9`, `TPM2`, `COL1A1`, `COL3A1`, `POSTN`, `FN1`, `TNC`, `CTGF`, `LOX`, `LOXL2` | Overlaps smooth muscle and fibroblastic tumor programs. | [25,26,48–52] |
| **myCAF / TGFβ-responsive CAF** | `ACTA2`, `TAGLN`, `MYL9`, `TPM2`, `FAP`, `POSTN`, `COL1A1`, `COL3A1`, `COL11A1`, `LRRC15`, `ITGA11`, `THY1` | CAF phenotype in many cancers; malignant osteosarcoma can mimic this. | [32,48–51] |
| **iCAF / inflammatory CAF** | `IL6`, `CXCL12`, `CXCL14`, `CXCL1`, `CXCL2`, `CXCL8`, `CCL2`, `LIF`, `HAS1`, `PDGFRA` | Cytokine-rich CAF state. | [48–50] |
| **apCAF / antigen-presenting CAF** | `HLA-DRA`, `HLA-DRB1`, `HLA-DPA1`, `HLA-DPB1`, `CD74`, `CIITA`; `PTPRC−` | Do not confuse with DCs/B cells/macrophages. | [49] |
| **Matrix-remodeling CAF** | `COL10A1`, `COL11A1`, `COMP`, `THBS2`, `MMP2`, `MMP11`, `FN1`, `POSTN`, `TNC`, `LOX` | Strong overlap with fibroblastic osteosarcoma; CNV is key. | [32,48–52] |
| **Pericytes** | `RGS5`, `PDGFRB`, `CSPG4`, `MCAM`, `NOTCH3`, `ABCC9`, `KCNJ8`, `COX4I2` | Vascular mural cells. | [19,20,28–30] |
| **Vascular smooth muscle cells** | `ACTA2`, `TAGLN`, `MYH11`, `CNN1`, `DES`, `ACTG2`, `LMOD1`, `SMTN` | Bronchovascular smooth muscle. | [19,20,28] |
| **Pan-endothelial** | `PECAM1`, `CDH5`, `VWF`, `CLDN5`, `ESAM`, `KDR`, `RAMP2`, `EMCN`, `ENG` | Parent EC gate. | [19,20,28–30] |
| **Alveolar capillary EC, general/gCap-like** | `FCN3`, `GPIHBP1`, `IL7R`, `RGCC`, `BTNL9` within EC gate | Capillary subset nomenclature varies across atlases; use EC context. | [19,20,28–30] |
| **Alveolar aerocyte/aCap-like EC** | `CA4`, `EDNRB`, `SOSTDC1`, `TBX2`, `TBX3`, `APLN` within EC gate | Specialized gas-exchange capillary EC. | [19,20,28–30] |
| **Arterial EC** | `GJA5`, `EFNB2`, `SOX17`, `HEY1`, `DLL4`, `BMX`, `NOTCH4` | Arterial vascular identity. | [19,20,28–30] |
| **Venous / venular EC** | `ACKR1`, `NR2F2`, `VCAM1`, `SELE`, `PLVAP`, `VWF` | Venous/post-capillary venule-like identity. | [19,20,28–30] |
| **Lymphatic EC** | `PROX1`, `PDPN`, `LYVE1`, `FLT4`, `CCL21`, `MMRN1`, `TBX1` | `PDPN` also AT1/mesothelial/fibroblast; use EC/lymphatic context. | [19,20,28] |
| **Angiogenic / tip-like EC** | `ESM1`, `KDR`, `FLT1`, `APLN`, `ANGPT2`, `DLL4`, `CXCR4`, `MMP14` | Tumor-associated angiogenesis state. | [28–32] |
| **Mesothelial cells** | `MSLN`, `WT1`, `CALB2`, `UPK3B`, `KRT8`, `KRT18`, `PDPN`, `LRRN4`, `ALDH1A2` | Pleural contamination/involvement. | [19,20] |
| **Schwann / peripheral nerve cells, rare** | `SOX10`, `S100B`, `PLP1`, `MPZ`, `PMP22`, `NGFR` | Rare structural component. | [19,20,58] |
| **Adipocyte / mature adipose contamination, rare** | `ADIPOQ`, `PLIN1`, `LEP`, `FABP4`, `LPL`, `CFD` | `FABP4` also alveolar macrophage; use parent identity. | [20,52,58] |

---

## 7. Technical/QC and non-cell-type signatures

| Signature | Genes | Interpretation |
|---|---|---|
| **Cell cycle** | `MKI67`, `TOP2A`, `UBE2C`, `CENPF`, `CDK1`, `CCNB1`, `CCNB2`, `BIRC5`, `TYMS`, `MCM2-7` | Proliferation state; annotate within each lineage. |
| **Immediate-early/dissociation stress** | `FOS`, `JUN`, `JUNB`, `DUSP1`, `IER2`, `ATF3`, `HSPA1A`, `HSPA1B`, `DNAJB1` | Tissue processing/stress; do not use as lineage. |
| **Interferon response** | `ISG15`, `IFI6`, `IFI27`, `IFIT1`, `IFIT2`, `IFIT3`, `MX1`, `MX2`, `OAS1`, `STAT1`, `IRF7` | State shared across immune, tumor, epithelial, stromal cells. |
| **Ambient surfactant RNA** | `SFTPA1`, `SFTPA2`, `SFTPB`, `SFTPC`, `SFTPD` | Common in lung; require epithelial coexpression for AT2 calls. |
| **Ambient immunoglobulin RNA** | `IGHG*`, `IGHA*`, `IGKC`, `IGLC*`, `JCHAIN` | Common near plasma cells; check whether a cell has full plasma-cell program. |
| **Ambient hemoglobin/RBC** | `HBA1`, `HBA2`, `HBB`, `HBD` | Blood contamination or erythroid cells. |
| **Doublet red flags** | `PTPRC` with strong epithelial/endothelial/tumor ECM markers; `EPCAM` + `COL1A1`; `PECAM1` + `CD3D`; `PPBP/PF4` with another lineage | Review UMI counts, doublet scores, and marker coexpression. |

---

## 8. High-priority marker-collision warnings

- **`COL1A1/COL1A2/SPARC/POSTN/FN1/THBS2`**: osteosarcoma, fibroblasts, CAFs, myofibroblasts. Use CNV and `SATB2/RUNX2/SP7/ALPL/IBSP/BGLAP`.
- **`SPP1`**: osteosarcoma, SPP1+ TAMs, AT2/injury epithelial cells, CAFs. Use parent lineage markers.
- **`LAMP3`**: AT2 cells and mature DCs. Use `EPCAM/SFTPC/ABCA3` versus `PTPRC/HLA-DRA/CCR7/FSCN1`.
- **`HLA-DRA/CD74`**: B cells, macrophages, DCs, apCAFs, IFN/MHC-II+ tumor cells. Use `PTPRC`, B/T/myeloid markers, and CNV.
- **`ACTA2/TAGLN/MYL9`**: smooth muscle, pericyte/myofibroblast, myCAF, fibroblastic tumor. Use `MYH11/CNN1` for smooth muscle, `RGS5/PDGFRB` for pericyte, CNV/osteogenic markers for tumor.
- **`SATB2`**: osteoblastic differentiation marker, but also expressed in colorectal epithelium/carcinoma. If `SATB2+` cells are `EPCAM/KRT/CDX2+`, consider epithelial metastasis differential rather than osteosarcoma.

---

## 9. Compact copy/paste core signature dictionary

```yaml
osteosarcoma_core:
  [SATB2, RUNX2, SP7, ALPL, IBSP, BGLAP, SPP1, COL1A1, COL1A2, SPARC, CDH11, POSTN, MMP13]
osteosarcoma_osteoblastic:
  [RUNX2, SP7, SATB2, ALPL, COL1A1, COL1A2, SPARC, IBSP, BGLAP, SPP1, MGP, BGN, DLX5]
osteosarcoma_chondroblastic:
  [SOX9, SOX5, SOX6, ACAN, COL2A1, COL9A1, COL9A2, COL9A3, COL10A1, COMP, MATN3, HAPLN1]
osteosarcoma_fibroblastic_ecm:
  [COL1A1, COL1A2, COL3A1, COL5A1, COL5A2, FN1, TNC, THBS2, POSTN, MMP2, MMP11, SERPINE1]
proliferation:
  [MKI67, TOP2A, UBE2C, CENPF, CDK1, CCNB1, CCNB2, BIRC5, TYMS, MCM2, MCM3, MCM4, MCM5, MCM6, MCM7]

AT1:
  [AGER, PDPN, CAV1, CAV2, AQP5, HOPX, CLDN18, EMP2, RTKN2]
AT2:
  [SFTPA1, SFTPA2, SFTPB, SFTPC, SFTPD, ABCA3, SLC34A2, NAPSA, LAMP3, LPCAT1]
club:
  [SCGB1A1, SCGB3A1, SCGB3A2, CYP2F1, BPIFA1, WFDC2]
ciliated:
  [FOXJ1, PIFO, TPPP3, RSPH1, DNAH5, DNAI1, CAPS]
basal:
  [KRT5, KRT14, KRT15, KRT17, TP63, NGFR, ITGA6]
goblet:
  [MUC5AC, MUC5B, SPDEF, AGR2, TFF3, CLCA1, FCGBP]
ionocyte:
  [FOXI1, CFTR, ASCL3, ATP6V1B1, ATP6V0D2, BSND]

T_cells:
  [CD3D, CD3E, CD3G, TRAC, TRBC1, TRBC2, CD2, CD247]
CD8_cytotoxic_T:
  [CD8A, CD8B, NKG7, PRF1, GZMB, GZMH, GNLY, CST7, CCL5]
Treg:
  [FOXP3, IL2RA, CTLA4, IKZF2, TIGIT, TNFRSF18, CCR8]
exhausted_T:
  [PDCD1, LAG3, HAVCR2, TIGIT, CTLA4, TOX, CXCL13, ENTPD1]
NK:
  [NKG7, GNLY, PRF1, GZMB, KLRD1, KLRF1, NCR1, FCGR3A]
B_cells:
  [MS4A1, CD79A, CD79B, CD19, CD22, BANK1, CD74, HLA-DRA]
plasma_cells:
  [JCHAIN, MZB1, XBP1, PRDM1, SDC1, IGHG1, IGHA1, IGKC]

classical_monocytes:
  [LYZ, LST1, S100A8, S100A9, S100A12, FCN1, VCAN, CD14, CCR2]
alveolar_macrophages:
  [MARCO, FABP4, PPARG, LPL, MRC1, MSR1, SIGLEC1, APOC1, APOE, MCEMP1]
SPP1_TREM2_TAM:
  [SPP1, TREM2, GPNMB, APOE, LGALS3, CTSB, CTSL, MMP9, MMP12, CHI3L1]
cDC1:
  [CLEC9A, XCR1, BATF3, IRF8, CADM1, CLNK]
cDC2:
  [CD1C, FCER1A, CLEC10A, CD1E, HLA-DRA, IRF4]
LAMP3_migratory_DC:
  [LAMP3, CCR7, FSCN1, CCL19, CCL17, CCL22, IDO1, IL4I1, CD83]
pDC:
  [CLEC4C, LILRA4, IL3RA, TCF4, IRF7, GZMB]
mast_cells:
  [TPSAB1, TPSB2, CPA3, KIT, MS4A2, HDC]
neutrophils:
  [S100A8, S100A9, FCGR3B, CSF3R, CXCR2, LCN2, CEACAM8, MPO, ELANE]
osteoclasts:
  [ACP5, CTSK, MMP9, DCSTAMP, OCSTAMP, ATP6V0D2, TNFRSF11A, CALCR, CA2, SIGLEC15, ITGB3]

fibroblasts:
  [COL1A1, COL1A2, COL3A1, DCN, LUM, DPT, PDGFRA, COL6A1, C1R, C1S, FBLN1]
myCAF:
  [ACTA2, TAGLN, MYL9, TPM2, FAP, POSTN, COL1A1, COL3A1, COL11A1, LRRC15, ITGA11]
iCAF:
  [IL6, CXCL12, CXCL14, CXCL1, CXCL2, CXCL8, CCL2, LIF, HAS1, PDGFRA]
pericytes:
  [RGS5, PDGFRB, CSPG4, MCAM, NOTCH3, ABCC9, KCNJ8]
smooth_muscle:
  [ACTA2, TAGLN, MYH11, CNN1, DES, ACTG2, LMOD1]
endothelial:
  [PECAM1, CDH5, VWF, CLDN5, ESAM, KDR, RAMP2, EMCN]
lymphatic_endothelial:
  [PROX1, PDPN, LYVE1, FLT4, CCL21, MMRN1]
mesothelial:
  [MSLN, WT1, CALB2, UPK3B, KRT8, KRT18, PDPN, LRRN4]
erythroid:
  [HBA1, HBA2, HBB, HBD, ALAS2, AHSP]
platelet:
  [PPBP, PF4, GP9, ITGA2B, TUBB1, NRGN]
```

---

## 10. References

1. Zhou Y, Yang D, Yang Q, et al. **Single-cell RNA landscape of intratumoral heterogeneity and immunosuppressive microenvironment in advanced osteosarcoma.** *Nature Communications.* 2020;11:6322.  
2. Klein MJ, Siegal GP. **Osteosarcoma: anatomic and histologic variants.** *American Journal of Clinical Pathology.* 2006;125:555–581.  
3. Kansara M, Teng MWL, Smyth MJ, Thomas DM. **Translational biology of osteosarcoma.** *Nature Reviews Cancer.* 2014;14:722–735.  
4. Isakoff MS, Bielack SS, Meltzer P, Gorlick R. **Osteosarcoma: current treatment and a collaborative pathway to success.** *Journal of Clinical Oncology.* 2015;33:3029–3035.  
5. Gill J, Gorlick R. **Advancing therapy for osteosarcoma.** *Nature Reviews Clinical Oncology.* 2021;18:609–624.  
6. Rickel K, Fang F, Tao J. **Molecular genetics of osteosarcoma.** *Bone.* 2017;102:69–79.  
7. Behjati S, Tarpey PS, Haase K, et al. **Recurrent mutation of IGF signalling genes and distinct patterns of genomic rearrangement in osteosarcoma.** *Nature Communications.* 2017;8:15936.  
8. Chen X, Bahrami A, Pappo A, et al. **Recurrent somatic structural variations contribute to tumorigenesis of osteosarcoma.** *Cell Reports.* 2014;7:104–112.  
9. Komori T, Yagi H, Nomura S, et al. **Targeted disruption of Cbfa1 results in a complete lack of bone formation owing to maturational arrest of osteoblasts.** *Cell.* 1997;89:755–764.  
10. Nakashima K, Zhou X, Kunkel G, et al. **The novel zinc finger-containing transcription factor osterix is required for osteoblast differentiation and bone formation.** *Cell.* 2002;108:17–29.  
11. Dobreva G, Chahrour M, Dautzenberg M, et al. **SATB2 is a multifunctional determinant of craniofacial patterning and osteoblast differentiation.** *Cell.* 2006;125:971–986.  
12. Conner JR, Hornick JL. **SATB2 is a novel marker of osteoblastic differentiation in bone and soft tissue tumours.** *Histopathology.* 2013;63:36–49.  
13. Akiyama H, Chaboissier MC, Martin JF, Schedl A, de Crombrugghe B. **The transcription factor Sox9 has essential roles in successive steps of the chondrocyte differentiation pathway.** *Genes & Development.* 2002;16:2813–2828.  
14. Bi W, Deng JM, Zhang Z, Behringer RR, de Crombrugghe B. **Sox9 is required for cartilage formation.** *Nature Genetics.* 1999;22:85–89.  
15. Boyle WJ, Simonet WS, Lacey DL. **Osteoclast differentiation and activation.** *Nature.* 2003;423:337–342.  
16. Teitelbaum SL. **Bone resorption by osteoclasts.** *Science.* 2000;289:1504–1508.  
17. Yagi M, Miyamoto T, Sawatani Y, et al. **DC-STAMP is essential for cell-cell fusion in osteoclasts and foreign body giant cells.** *Journal of Experimental Medicine.* 2005;202:345–351.  
18. Buddingh EP, Kuijjer ML, Duim RAJ, et al. **Tumor-infiltrating macrophages are associated with metastasis suppression in high-grade osteosarcoma.** *Clinical Cancer Research.* 2011;17:2110–2119.  
19. Travaglini KJ, Nabhan AN, Penland L, et al. **A molecular cell atlas of the human lung from single-cell RNA sequencing.** *Nature.* 2020;587:619–625.  
20. Sikkema L, Ramírez-Suástegui C, Strobl DC, et al. **An integrated cell atlas of the lung in health and disease.** *Nature Medicine.* 2023;29:1563–1577.  
21. Vieira Braga FA, Kar G, Berg M, et al. **A cellular census of human lungs identifies novel cell states in health and in asthma.** *Nature Medicine.* 2019;25:1153–1163.  
22. Deprez M, Zaragosi LE, Truchi M, et al. **A single-cell atlas of the human healthy airways.** *American Journal of Respiratory and Critical Care Medicine.* 2020;202:1636–1645.  
23. Plasschaert LW, Žilionis R, Choo-Wing R, et al. **A single-cell atlas of the airway epithelium reveals the CFTR-rich pulmonary ionocyte.** *Nature.* 2018;560:377–381.  
24. Montoro DT, Haber AL, Biton M, et al. **A revised airway epithelial hierarchy includes CFTR-expressing ionocytes.** *Nature.* 2018;560:319–324.  
25. Habermann AC, Gutierrez AJ, Bui LT, et al. **Single-cell RNA sequencing reveals profibrotic roles of distinct epithelial and mesenchymal lineages in pulmonary fibrosis.** *Science Advances.* 2020;6:eaba1972.  
26. Adams TS, Schupp JC, Poli S, et al. **Single-cell RNA-seq reveals ectopic and aberrant lung-resident cell populations in idiopathic pulmonary fibrosis.** *Science Advances.* 2020;6:eaba1983.  
27. Kobayashi Y, Tata A, Konkimalla A, et al. **Persistence of a regeneration-associated, transitional alveolar epithelial cell state in pulmonary fibrosis.** *Nature Cell Biology.* 2020;22:934–946.  
28. Schupp JC, Adams TS, Cosme C Jr, et al. **Integrated single-cell atlas of endothelial cells of the human lung.** *Circulation.* 2021;144:286–302.  
29. Kalucka J, de Rooij LPMH, Goveia J, et al. **Single-cell transcriptome atlas of murine and human endothelial cells.** *Cell.* 2020;180:764–779.e20.  
30. Gillich A, Zhang F, Farmer CG, et al. **Capillary cell-type specialization in the alveolus.** *Nature.* 2020;586:785–789.  
31. Travis WD, Brambilla E, Nicholson AG, et al. **The 2015 World Health Organization classification of lung tumors: impact of genetic, clinical and radiologic advances since the 2004 classification.** *Journal of Thoracic Oncology.* 2015;10:1243–1260.  
32. Lambrechts D, Wauters E, Boeckx B, et al. **Phenotype molding of stromal cells in the lung tumor microenvironment.** *Nature Medicine.* 2018;24:1277–1289.  
33. Zilionis R, Engblom C, Pfirschke C, et al. **Single-cell transcriptomics of human and mouse lung cancers reveals conserved myeloid populations across individuals and species.** *Immunity.* 2019;50:1317–1334.e10.  
34. Lavin Y, Kobayashi S, Leader A, et al. **Innate immune landscape in early lung adenocarcinoma by paired single-cell analyses.** *Cell.* 2017;169:750–765.e17.  
35. Guo X, Zhang Y, Zheng L, et al. **Global characterization of T cells in non-small-cell lung cancer by single-cell sequencing.** *Nature Medicine.* 2018;24:978–985.  
36. Maynard A, McCoach CE, Rotow JK, et al. **Therapy-induced evolution of human lung cancer revealed by single-cell RNA sequencing.** *Cell.* 2020;182:1232–1251.e22.  
37. Leader AM, Grout JA, Maier BB, et al. **Single-cell analysis of human non-small cell lung cancer lesions refines tumor classification and patient stratification.** *Cancer Cell.* 2021;39:1594–1609.e12.  
38. Villani AC, Satija R, Reynolds G, et al. **Single-cell RNA-seq reveals new types of human blood dendritic cells, monocytes, and progenitors.** *Science.* 2017;356:eaah4573.  
39. See P, Dutertre CA, Chen J, et al. **Mapping the human DC lineage through the integration of high-dimensional techniques.** *Science.* 2017;356:eaag3009.  
40. Dutertre CA, Becht E, Irac SE, et al. **Single-cell analysis of human mononuclear phagocytes reveals subset-defining markers and identifies circulating inflammatory dendritic cells.** *Immunity.* 2019;51:573–589.e8.  
41. Guilliams M, Ginhoux F, Jakubzick C, et al. **Dendritic cells, monocytes and macrophages: a unified nomenclature based on ontogeny.** *Nature Reviews Immunology.* 2014;14:571–578.  
42. Cheng S, Li Z, Gao R, et al. **A pan-cancer single-cell transcriptional atlas of tumor infiltrating myeloid cells.** *Cell.* 2021;184:792–809.e23.  
43. Cassetta L, Fragkogianni S, Sims AH, et al. **Human tumor-associated macrophage and monocyte transcriptional landscapes reveal cancer-specific reprogramming.** *Cancer Cell.* 2019;35:588–602.e10.  
44. Wherry EJ, Kurachi M. **Molecular and cellular insights into T cell exhaustion.** *Nature Reviews Immunology.* 2015;15:486–499.  
45. Thommen DS, Schumacher TN. **T cell dysfunction in cancer.** *Cancer Cell.* 2018;33:547–562.  
46. Sakaguchi S, Yamaguchi T, Nomura T, Ono M. **Regulatory T cells and immune tolerance.** *Cell.* 2008;133:775–787.  
47. Zheng C, Zheng L, Yoo JK, et al. **Landscape of infiltrating T cells in liver cancer revealed by single-cell sequencing.** *Cell.* 2017;169:1342–1356.e16.  
48. Öhlund D, Handly-Santana A, Biffi G, et al. **Distinct populations of inflammatory fibroblasts and myofibroblasts in pancreatic cancer.** *Journal of Experimental Medicine.* 2017;214:579–596.  
49. Elyada E, Bolisetty M, Laise P, et al. **Cross-species single-cell analysis of pancreatic ductal adenocarcinoma reveals antigen-presenting cancer-associated fibroblasts.** *Cancer Discovery.* 2019;9:1102–1123.  
50. Kieffer Y, Hocine HR, Gentric G, et al. **Single-cell analysis reveals fibroblast clusters linked to immunotherapy resistance in cancer.** *Cancer Discovery.* 2020;10:1330–1351.  
51. Dominguez CX, Müller S, Keerthivasan S, et al. **Single-cell RNA sequencing reveals stromal evolution into LRRC15+ myofibroblasts as a determinant of patient response to cancer immunotherapy.** *Cancer Discovery.* 2020;10:232–253.  
52. Buechler MB, Pradhan RN, Krishnamurty AT, et al. **Cross-tissue organization of the fibroblast lineage.** *Nature.* 2021;593:575–579.  
53. Tirosh I, Izar B, Prakadan SM, et al. **Dissecting the multicellular ecosystem of metastatic melanoma by single-cell RNA-seq.** *Science.* 2016;352:189–196.  
54. Patel AP, Tirosh I, Trombetta JJ, et al. **Single-cell RNA-seq highlights intratumoral heterogeneity in primary glioblastoma.** *Science.* 2014;344:1396–1401.  
55. Puram SV, Tirosh I, Parikh AS, et al. **Single-cell transcriptomic analysis of primary and metastatic tumor ecosystems in head and neck cancer.** *Cell.* 2017;171:1611–1624.e24.  
56. Gao R, Bai S, Henderson YC, et al. **Delineating copy number and clonal substructure in human tumors from single-cell transcriptomes.** *Nature Biotechnology.* 2021;39:599–608.  
57. Aran D, Looney AP, Liu L, et al. **Reference-based analysis of lung single-cell sequencing reveals a transitional profibrotic macrophage.** *Nature Immunology.* 2019;20:163–172.  
58. The Tabula Sapiens Consortium. **The Tabula Sapiens: a multiple-organ, single-cell transcriptomic atlas of humans.** *Science.* 2022;376:eabl4896.