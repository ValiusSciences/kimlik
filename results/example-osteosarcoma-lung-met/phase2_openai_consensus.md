# Consensus gene-signature report for annotating scRNA-seq/snRNA-seq from a right-lung biopsy in metastatic osteosarcoma

**Sample context:** human right-lung biopsy from a patient with metastatic osteosarcoma, primary distal femur.  
**Use case:** annotation of scRNA-seq/snRNA-seq clusters and cell states.  
**Gene nomenclature:** HGNC-style human gene symbols.  
**Important limitation:** gene signatures support research annotation; they are not diagnostic by themselves. Clinically consequential calls should be reconciled with pathology, imaging, IHC/IF, and, where possible, genomic data.

---

## 1. Consensus annotation strategy

A right-lung biopsy containing metastatic osteosarcoma is a mixed tissue: malignant sarcoma cells, recruited tumor microenvironment, resident lung epithelium, vascular/stromal cells, blood-derived immune cells, and technical artifacts can all coexist. The most important consensus point across the reports is:

> **Do not identify malignant osteosarcoma using collagen/ECM genes alone.**  
> `COL1A1`, `COL1A2`, `COL3A1`, `SPARC`, `POSTN`, `FN1`, `THBS2`, `TNC`, and related ECM genes are shared by osteosarcoma cells, normal lung fibroblasts, CAFs, myofibroblasts, and wound-healing/fibrotic states.

Recommended workflow:

1. **QC and artifact mitigation**
   - Filter low-quality cells/nuclei using sample-aware UMI/gene/mitochondrial thresholds.
   - Correct or account for ambient RNA, especially lung surfactant genes and immunoglobulins.
   - Remove or flag doublets.
   - Score stress, cell cycle, hemoglobin, platelet, and ambient RNA modules.

2. **Gate broad compartments first**
   - Immune: `PTPRC`
   - Epithelial: `EPCAM`, `KRT8`, `KRT18`, `KRT19`
   - Endothelial: `PECAM1`, `CDH5`, `VWF`, `CLDN5`
   - Fibroblast/CAF: `DCN`, `LUM`, `PDGFRA`, `COL1A1`
   - Pericyte: `RGS5`, `PDGFRB`, `CSPG4`, `NOTCH3`
   - Smooth muscle: `MYH11`, `CNN1`, `ACTA2`, `TAGLN`
   - Erythroid/platelet: `HBA1/HBA2/HBB`, `PPBP/PF4`

3. **Call malignant osteosarcoma using combined evidence**
   - **Primary evidence:** inferred CNV/aneuploidy from scRNA/snRNA data, e.g. inferCNV, CopyKAT, Numbat, SCEVAN.
   - **Supportive lineage evidence:** osteogenic/osteosarcoma program:
     `SATB2`, `RUNX2`, `SP7`, `ALPL`, `IBSP`, `BGLAP`, `SPP1`, `CDH11`, `COL1A1`, `COL1A2`, `SPARC`, `POSTN`, `MMP13`.
   - **Negative/deconfounding evidence:** absence of strong canonical host-lineage programs such as `PTPRC`, `EPCAM/KRT`, `PECAM1/CDH5`, and absence of a purely diploid fibroblast profile.

4. **Subcluster malignant, immune, epithelial, stromal, and vascular compartments separately**
   - Tumor states should be annotated within CNV-positive malignant cells.
   - Cycling, hypoxia, interferon, and stress are states, not cell types.

5. **Validate key calls**
   - Osteosarcoma: SATB2, RUNX2, ALPL, osteocalcin/BGLAP, osteoid histology.
   - Immune/stromal/vascular: CD45, CD3, CD68/CD163, CD31, EPCAM/pan-keratin, FAP, αSMA, TRAP/CTSK as relevant.

---

## 2. Level-1 broad compartment signatures

| Broad identity | Positive markers | Useful negatives / caveats |
|---|---|---|
| **Malignant osteosarcoma** | `SATB2`, `RUNX2`, `SP7`, `ALPL`, `IBSP`, `BGLAP`, `SPP1`, `CDH11`, `COL1A1`, `COL1A2`, `SPARC`, `POSTN`, `MMP13` + CNV/aneuploidy | Usually `PTPRC−`, `PECAM1−`, `CDH5−`; often `EPCAM−/low`. ECM genes alone are insufficient. |
| **Immune cells** | `PTPRC`; then T/NK/B/myeloid markers | Plasma cells can have lower `PTPRC`; check full plasma-cell program. |
| **Lung epithelial cells** | `EPCAM`, `KRT8`, `KRT18`, `KRT19`, `CLDN4`, `TACSTD2`, `MUC1` | Surfactant RNA can be ambient; require coexpression of epithelial programs. |
| **Endothelial cells** | `PECAM1`, `CDH5`, `VWF`, `CLDN5`, `ESAM`, `KDR`, `RAMP2`, `EMCN` | Subtype within endothelial gate. |
| **Fibroblasts / CAFs** | `COL1A1`, `COL1A2`, `COL3A1`, `DCN`, `LUM`, `DPT`, `PDGFRA`, `C1R`, `C1S`, `FBLN1` | Distinguish from fibroblastic osteosarcoma by CNV and osteogenic TFs. |
| **Pericytes** | `RGS5`, `PDGFRB`, `CSPG4`, `MCAM`, `NOTCH3`, `ABCC9`, `KCNJ8` | `ACTA2` can be shared with smooth muscle/myofibroblasts. |
| **Smooth muscle cells** | `ACTA2`, `TAGLN`, `MYH11`, `CNN1`, `DES`, `ACTG2`, `LMOD1`, `SMTN` | Strong `MYH11/CNN1` favors true smooth muscle. |
| **Mesothelial / pleural cells** | `MSLN`, `WT1`, `CALB2`, `UPK3B`, `KRT8`, `KRT18`, `PDPN`, `LRRN4` | Relevant in pleural or wedge biopsies. |
| **Osteoclast / giant-cell lineage** | `ACP5`, `CTSK`, `MMP9`, `DCSTAMP`, `OCSTAMP`, `ATP6V0D2`, `TNFRSF11A`, `CALCR`, `CA2`, `SIGLEC15`, `ITGB3` plus myeloid genes | Should be myeloid-derived: `PTPRC`, `CSF1R`, `TYROBP`, `CD68`. Do not confuse with `SPP1+` tumor cells. |
| **Erythroid / RBC contamination** | `HBA1`, `HBA2`, `HBB`, `HBD`, `ALAS2`, `AHSP` | Usually blood/ambient contamination unless coherent erythroid program. |
| **Platelet / megakaryocyte signal** | `PPBP`, `PF4`, `GP9`, `ITGA2B`, `TUBB1`, `NRGN` | Coexpression with another lineage often indicates platelet adherence or doublet. |

---

## 3. Malignant osteosarcoma signatures and tumor states

Use these signatures **inside the putative malignant compartment**, ideally after CNV inference.

| Tumor state / program | Gene signature | Interpretation / caveats |
|---|---|---|
| **Core malignant osteosarcoma / osteogenic sarcoma** | `SATB2`, `RUNX2`, `SP7`, `ALPL`, `IBSP`, `BGLAP`, `SPP1`, `COL1A1`, `COL1A2`, `SPARC`, `CDH11`, `POSTN`, `MMP13` | Best called in CNV-positive, `PTPRC−/EPCAM−/PECAM1−` cells. `SATB2` is supportive but not fully specific. |
| **Osteoblastic / osteoid-producing OS** | `RUNX2`, `SP7`, `SATB2`, `ALPL`, `COL1A1`, `COL1A2`, `SPARC`, `IBSP`, `BGLAP`, `SPP1`, `MGP`, `BGN`, `DLX5`, `MSX2`, `OMD`, `MEPE` | Classical osteoblastic differentiation. `BGLAP`, `DMP1`, `SOST` may be sparse/dropout-prone. |
| **Chondroblastic OS** | `SOX9`, `SOX5`, `SOX6`, `ACAN`, `COL2A1`, `COL9A1`, `COL9A2`, `COL9A3`, `COL10A1`, `COL11A2`, `COMP`, `MATN3`, `CHAD`, `HAPLN1`, `IHH` | Suggests chondroblastic differentiation if CNV-positive. Diploid cartilage-like cells should not be assumed malignant. |
| **Fibroblastic / spindle-cell / ECM-rich OS** | `COL1A1`, `COL1A2`, `COL3A1`, `COL5A1`, `COL5A2`, `COL6A3`, `FN1`, `TNC`, `THBS2`, `POSTN`, `MMP2`, `MMP11`, `MMP14`, `SERPINE1`, `FAP`, `PDPN`, `VCAN`, `CDH11` | Highest-risk collision with CAFs. Require CNV and/or osteogenic TFs. |
| **Proliferating high-grade OS** | `MKI67`, `TOP2A`, `UBE2C`, `CENPF`, `CDK1`, `CCNB1`, `CCNB2`, `BIRC5`, `TYMS`, `MCM2`, `MCM3`, `MCM4`, `MCM5`, `MCM6`, `MCM7`, `PCNA`, `RRM2` | Proliferation is not lineage-specific; score within malignant cells. |
| **Hypoxic / glycolytic OS** | `CA9`, `VEGFA`, `SLC2A1`, `LDHA`, `PDK1`, `NDRG1`, `BNIP3`, `HILPDA`, `ENO1`, `PGK1`, `ADM` | Shared hypoxia state across tumor and non-tumor cells. |
| **Inflammatory / invasive / matrix-remodeling OS** | `CXCL8`, `IL6`, `CXCL1`, `CXCL2`, `MMP9`, `MMP13`, `MMP14`, `LOX`, `LOXL2`, `SERPINE1`, `PLAUR`, `ITGA5`, `TNC`, `POSTN`, `FN1` | Overlaps CAFs and inflammatory myeloid cells. Use CNV/lineage context. |
| **IFN/MHC-responsive OS** | `HLA-A`, `HLA-B`, `HLA-C`, `B2M`, `STAT1`, `IRF1`, `ISG15`, `IFI6`, `IFIT1`, `IFIT2`, `IFIT3`, `MX1`, `CXCL9`, `CXCL10`; sometimes `HLA-DRA`, `CD74` | `HLA-DRA/CD74` also mark B cells, macrophages, DCs, apCAFs. CNV-positive `PTPRC−` cells may represent MHC-II+ tumor state. |
| **UPR / ER-stress-like OS** | `ATF6`, `XBP1`, `HSPA5`, `DDIT3`, `ATF4`, `HERPUD1`, `EDEM1`, `SEL1L`, `MANF`, `PDIA4` | State program; distinguish from dissociation stress. |
| **MSC-/progenitor-like OS** | `CXCL12`, `SFRP2`, `MME`, `THY1`, `NES`, `PRRX1`, `SOX4`, `KLF4`, `CD44`, `ALDH1A1`, `PROM1` | Candidate stem/progenitor-like state; overlaps host MSC/fibroblast programs, so requires CNV. |
| **Mature osteocyte-like / ossified matrix** | `DMP1`, `PHEX`, `SOST`, `MEPE`, `FGF23` | Rarely captured. If CNV-positive, may represent terminal osteogenic differentiation. |
| **MDM2/CDK4-amplified low-grade/dedifferentiated OS context** | `MDM2`, `CDK4`, `HMGA2` plus CNV amplification | Not universal in conventional high-grade OS; useful if pathology suggests parosteal/low-grade central/dedifferentiated OS. |

---

## 4. Resident lung epithelial and injury-associated signatures

| Cell type / state | Gene signature | Notes |
|---|---|---|
| **Pan-epithelial** | `EPCAM`, `KRT8`, `KRT18`, `KRT19`, `CLDN4`, `TACSTD2`, `MUC1`, `CDH1` | Parent epithelial gate. |
| **AT1 pneumocytes** | `AGER`, `PDPN`, `CAV1`, `CAV2`, `AQP5`, `HOPX`, `CLDN18`, `EMP2`, `RTKN2`, `CLIC5`, `SPOCK2` | `PDPN` is shared with lymphatics/mesothelium. |
| **AT2 pneumocytes** | `SFTPA1`, `SFTPA2`, `SFTPB`, `SFTPC`, `SFTPD`, `ABCA3`, `SLC34A2`, `NAPSA`, `LAMP3`, `LPCAT1`, `ETV5` | Surfactant genes are common ambient RNA; require coherent epithelial coexpression. |
| **AT2/AT1 transitional / injury-associated epithelial cells** | `KRT8`, `KRT18`, `KRT19`, `CLDN4`, `CDKN1A`, `LGALS3`, `LCN2`, `SFN`, `KRT7`, `TACSTD2`, `MDK`, `GDF15` | Important in damaged/fibrotic lung and metastatic niche; can resemble carcinoma-like or EMT-like states. |
| **Aberrant basaloid / KRT17-high injury-like epithelium** | `KRT17`, `KRT8`, `KRT18`, `CLDN4`, `VIM`, `FN1`, `ITGB6`, `MMP7`, `GDF15`, `SOX9`, low/variable `KRT5`, `TP63` | Resolve from malignant OS by `EPCAM/KRT+`, CNV-neutral, lacking `RUNX2/SP7/IBSP/ALPL`. |
| **Club / secretory airway cells** | `SCGB1A1`, `SCGB3A1`, `SCGB3A2`, `CYP2F1`, `BPIFA1`, `WFDC2`, `MUC5B`, `TFF3` | `SCGB1A1` can be ambient. |
| **Ciliated epithelial cells** | `FOXJ1`, `PIFO`, `TPPP3`, `RSPH1`, `DNAH5`, `DNAI1`, `CCDC39`, `CAPS`, `SNTN`, `C20orf85` | Motile cilia program. |
| **Basal cells** | `KRT5`, `KRT14`, `KRT15`, `KRT17`, `TP63`, `NGFR`, `ITGA6`, `DST`, `S100A2` | Proximal airway basal cells; distinguish from squamous carcinoma by CNV and expansion. |
| **Goblet / mucous cells** | `MUC5AC`, `MUC5B`, `SPDEF`, `AGR2`, `TFF3`, `CLCA1`, `FCGBP` | Secretory mucous lineage. |
| **Submucosal gland serous cells** | `LTF`, `LYZ`, `BPIFB1`, `MUC7`, `PRR4`, `AZGP1`, `ZG16B` | May appear if proximal airway/submucosal gland sampled. |
| **Pulmonary ionocytes** | `FOXI1`, `CFTR`, `ASCL3`, `ATP6V1B1`, `ATP6V0D2`, `BSND`, `TMEM61` | Rare; `ATP6V0D2` also appears in osteoclasts. |
| **Tuft cells** | `POU2F3`, `TRPM5`, `DCLK1`, `GFI1B`, `AVIL`, `GNAT3`, `LRMP` | Rare chemosensory epithelial cells. |
| **Pulmonary neuroendocrine cells** | `ASCL1`, `INSM1`, `CHGA`, `CHGB`, `SYP`, `NCAM1`, `CALCA`, `GRP` | If expanded and aneuploid, consider neuroendocrine carcinoma differential. |
| **Possible lung adenocarcinoma differential** | `EPCAM`, `KRT8`, `KRT18`, `KRT19`, `NKX2-1`, `NAPSA`, `SFTPB`, `SFTPC`, `MUC1`, `CEACAM6` + CNV | Include because a lung biopsy can rarely contain a second primary or epithelial metastasis. |
| **Possible squamous carcinoma differential** | `TP63`, `KRT5`, `KRT6A`, `KRT6B`, `KRT14`, `SOX2`, `DSG3` + CNV | Distinguish from normal basal cells by CNV, expansion, pathology. |

---

## 5. Immune-cell signatures

### 5.1 Lymphoid compartment

| Cell type / state | Gene signature | Notes |
|---|---|---|
| **Pan-immune** | `PTPRC` | Parent immune gate. |
| **Pan-T cells** | `CD3D`, `CD3E`, `CD3G`, `TRAC`, `TRBC1`, `TRBC2`, `CD2`, `CD247` | Parent T-cell gate. |
| **Naive / central-memory CD4 T** | `CD3D`, `CD4`, `IL7R`, `CCR7`, `SELL`, `TCF7`, `LEF1`, `LTB`, `MAL` | `CD4` also occurs in monocytes; require CD3/TCR genes. |
| **CD8 cytotoxic T** | `CD3D`, `CD8A`, `CD8B`, `NKG7`, `PRF1`, `GZMB`, `GZMH`, `GNLY`, `CST7`, `CCL5` | Distinguish from NK by TCR/CD3 genes. |
| **GZMK+ effector-memory T** | `GZMK`, `GZMA`, `CCL5`, `NKG7`, `CD8A`, `CXCR3`, `EOMES`, `CST7` | Common intermediate cytotoxic-memory state. |
| **Exhausted / tumor-reactive T** | `PDCD1`, `LAG3`, `HAVCR2`, `TIGIT`, `CTLA4`, `TOX`, `CXCL13`, `ENTPD1`, `TNFRSF9`, `ITGAE`, `LAYN` | Activation can transiently express checkpoint genes; interpret with state/clonality. |
| **Regulatory T cells** | `FOXP3`, `IL2RA`, `CTLA4`, `IKZF2`, `TIGIT`, `TNFRSF18`, `TNFRSF4`, `CCR8`, `BATF`, `LAYN` | Tumor Tregs often `CCR8/TNFRSF18/TNFRSF4` high. |
| **Tissue-resident memory T** | `ITGAE`, `CD69`, `CXCR6`, `ZNF683`, `XCL1`, `XCL2`, `ITGA1` | Common in lung/tumor tissue. |
| **Tfh / CXCL13+ CD4 T** | `CXCL13`, `IL21`, `BCL6`, `TOX2`, `CD200`, `ICOS`, `PDCD1`, `MAF` | Often associated with TLS-like niches. |
| **Th17-like** | `IL17A`, `IL17F`, `RORC`, `CCR6`, `KLRB1`, `IL23R`, `IL26` | Usually low abundance in many tumors. |
| **γδ T cells** | `TRDC`, `TRGC1`, `TRGC2`, `TRDV2`, `TRGV9`, `CD3D`, `NKG7` | May be cytotoxic. |
| **MAIT-like T cells** | `TRAV1-2`, `KLRB1`, `SLC4A10`, `DPP4`, `IL18RAP`, `ZBTB16`, `NCR3` | Confirm with TCR if available. |
| **NK cells** | `NKG7`, `GNLY`, `PRF1`, `GZMB`, `KLRD1`, `KLRF1`, `NCR1`, `FCGR3A`, `TYROBP`; `CD3D/TRAC−` | `FCGR3A` also occurs in myeloid cells; require NK program and absent TCR. |
| **CD56 bright / resident NK-like** | `NCAM1`, `XCL1`, `XCL2`, `GZMK`, `SELL`, `KLRC1`, `CD160`, `ITGA1` | Tissue-resident NK-like state. |
| **CD56 dim / cytotoxic NK-like** | `FGFBP2`, `FCGR3A`, `KLRF1`, `GNLY`, `PRF1`, `SPON2`, `CX3CR1`, `KLRD1`, `NKG7` | Cytotoxic circulating-like NK state. |
| **B cells** | `MS4A1`, `CD79A`, `CD79B`, `CD19`, `CD22`, `BANK1`, `CD74`, `HLA-DRA`, `TCL1A`, `IGHD`, `IGHM` | `CD74/HLA-DRA` are not B-specific. |
| **Germinal-center B** | `BCL6`, `AICDA`, `RGS13`, `MEF2B`, `LMO2`, `S1PR2`, `MKI67` | May suggest TLS if accompanied by T/B/DC organization. |
| **Plasma cells / plasmablasts** | `JCHAIN`, `MZB1`, `XBP1`, `PRDM1`, `SDC1`, `TNFRSF17`, `DERL3`, `IGHG1`, `IGHA1`, `IGKC`, `IGLC2` | Very high Ig RNA can contaminate other clusters. |
| **TLS module** | `CXCL13`, `CCL19`, `CCL21`, `CR2`, `LTB`, `CXCR5`, `SELL`, `MS4A1`, `LAMP3`, `CCR7` | Prefer spatial/neighborhood interpretation if spatial data are available. |

### 5.2 Myeloid, granulocyte, mast, and osteoclast-lineage cells

| Cell type / state | Gene signature | Notes |
|---|---|---|
| **Classical inflammatory monocytes** | `LYZ`, `LST1`, `S100A8`, `S100A9`, `S100A12`, `FCN1`, `VCAN`, `CD14`, `CCR2`, `LILRB2`, `SELL` | Can resemble monocytic MDSC-like states. |
| **Non-classical / patrolling monocytes** | `FCGR3A`, `CX3CR1`, `MS4A7`, `LST1`, `LILRB1`, `IFITM3`, `RHOC`, `CDKN1C` | Distinguish from NK by myeloid genes and lack of `NKG7/GNLY` dominance. |
| **Pan-macrophage** | `C1QA`, `C1QB`, `C1QC`, `APOE`, `CD68`, `CSF1R`, `AIF1`, `MRC1`, `CD163`, `LYZ`, `TYROBP` | Parent macrophage program. |
| **Alveolar macrophages** | `MARCO`, `FABP4`, `PPARG`, `LPL`, `MRC1`, `MSR1`, `SIGLEC1`, `APOC1`, `APOE`, `MCEMP1`, `CIDEC` | Lung-resident; often abundant in lung biopsy. |
| **Interstitial / FOLR2+ macrophages** | `F13A1`, `LYVE1`, `FOLR2`, `SELENOP`, `MRC1`, `MAFB`, `MS4A7`, `C1QA`, `C1QC` | Less `MARCO/FABP4` than alveolar macrophages. |
| **SPP1+/TREM2+ TAM / profibrotic macrophage** | `SPP1`, `TREM2`, `GPNMB`, `APOE`, `LGALS3`, `CTSB`, `CTSL`, `MMP9`, `MMP12`, `CHI3L1`, `FABP5`, `LIPA`, `CD9` | `SPP1` is also tumor/AT2/CAF-associated; require myeloid context. |
| **Inflammatory macrophages** | `IL1B`, `CXCL8`, `CCL3`, `CCL4`, `TNF`, `NLRP3`, `PTGS2`, `S100A8`, `S100A9` | Overlaps classical monocytes and dissociation/inflammation. |
| **IFN/MHC macrophages** | `HLA-DRA`, `HLA-DRB1`, `HLA-DPA1`, `HLA-DPB1`, `CD74`, `CD86`, `CIITA`, `STAT1`, `ISG15`, `IFIT1`, `CXCL9`, `CXCL10` | Distinguish from DCs, B cells, apCAFs, and MHC-II+ tumor cells. |
| **Angiogenic TAM** | `VEGFA`, `VCAN`, `THBS1`, `HIF1A`, `SLC2A1`, `EREG`, `INHBA`, `SPP1` | Cancer-type-specific; interpret cautiously. |
| **cDC1** | `CLEC9A`, `XCR1`, `BATF3`, `IRF8`, `CADM1`, `CLNK`, `WDFY4`, `IDO1` | Cross-presenting DC subset. |
| **cDC2** | `CD1C`, `FCER1A`, `CLEC10A`, `CD1E`, `HLA-DRA`, `IRF4`, `ITGAX`, `FCGR2B` | Common tissue DC subset. |
| **Mature/migratory LAMP3+ DC / mregDC** | `LAMP3`, `CCR7`, `FSCN1`, `CCL19`, `CCL17`, `CCL22`, `IDO1`, `IL4I1`, `CD83`, `CD40`, `BIRC3` | `LAMP3` also in AT2 cells; require `PTPRC/HLA/CCR7/FSCN1`. |
| **pDC** | `CLEC4C`, `LILRA4`, `IL3RA`, `TCF4`, `IRF7`, `GZMB`, `JCHAIN`, `SERPINF1` | Often low abundance. |
| **Mast cells** | `TPSAB1`, `TPSB2`, `CPA3`, `KIT`, `MS4A2`, `HDC`, `CMA1`, `HPGDS` | Strong tryptase/chymase program. |
| **Basophils** | `MS4A2`, `FCER1A`, `IL3RA`, `HDC`, `GATA2`, `CLC`; usually `KIT−/low`, `TPSB2−/low` | Distinguish from mast cells. |
| **Neutrophils / PMN-MDSC-like cells** | `S100A8`, `S100A9`, `FCGR3B`, `CSF3R`, `CXCR2`, `NAMPT`, `LCN2`, `CEACAM8`, `MPO`, `ELANE`, `OLR1`, `PROK2`, `IL1R2` | Fragile/undercaptured in scRNA-seq; `S100A8/A9` also monocytes. |
| **Eosinophils** | `CLC`, `PRG2`, `RNASE2`, `RNASE3`, `IL5RA`, `CCR3`, `SIGLEC8` | Rare but interpretable. |
| **Osteoclasts / osteoclast-like giant cells** | `ACP5`, `CTSK`, `MMP9`, `DCSTAMP`, `OCSTAMP`, `ATP6V0D2`, `TNFRSF11A`, `CALCR`, `CA2`, `SIGLEC15`, `ITGB3`, `TCIRG1`, `NFATC1`, `SPP1` plus myeloid genes | Should be `PTPRC/CSF1R/TYROBP/CD68+`; not malignant OS cells. |

---

## 6. Stromal, vascular, and structural cell signatures

| Cell type / state | Gene signature | Notes |
|---|---|---|
| **Pan-fibroblast** | `COL1A1`, `COL1A2`, `COL3A1`, `DCN`, `LUM`, `DPT`, `PDGFRA`, `COL6A1`, `COL6A2`, `COL6A3`, `C1R`, `C1S`, `FBLN1`, `FBLN2`, `CXCL14` | Diploid host fibroblasts; distinguish from tumor by CNV and osteogenic markers. |
| **Alveolar fibroblast / lipofibroblast-like** | `PDGFRA`, `TCF21`, `WNT2`, `FGF7`, `FGF10`, `ADH1B`, `PLIN2`, `LUM`, `DCN`, `NPNT`, `GPC3` | Normal lung mesenchyme. |
| **Adventitial / PI16+ fibroblast** | `PI16`, `DPP4`, `C7`, `CFD`, `SCARA5`, `CD34`, `CCL11`, `DPT`, `SERPINF1`, `MFAP5` | Common fibroblast subtype across tissues. |
| **Peribronchial fibroblast** | `ASPN`, `HHIP`, `FGF7`, `FGF18`, `WIF1` | Lung airway-associated fibroblast subtype. |
| **Myofibroblast** | `ACTA2`, `TAGLN`, `MYL9`, `TPM2`, `COL1A1`, `COL3A1`, `POSTN`, `FN1`, `TNC`, `CTGF`, `LOX`, `LOXL2` | Overlaps smooth muscle and fibroblastic tumor programs. |
| **myCAF / TGFβ-responsive CAF** | `ACTA2`, `TAGLN`, `MYL9`, `TPM2`, `FAP`, `POSTN`, `COL1A1`, `COL3A1`, `COL11A1`, `LRRC15`, `ITGA11`, `THY1`, `CTHRC1`, `COMP`, `INHBA` | CAF phenotype; malignant OS can mimic this. |
| **iCAF / inflammatory CAF** | `IL6`, `CXCL12`, `CXCL14`, `CXCL1`, `CXCL2`, `CXCL8`, `CCL2`, `LIF`, `HAS1`, `PDGFRA`, `DPT`, `APOD`, `CLU` | Cytokine-rich CAF state. |
| **apCAF / antigen-presenting CAF** | `HLA-DRA`, `HLA-DRB1`, `HLA-DPA1`, `HLA-DPB1`, `CD74`, `CIITA`; `PTPRC−` | Do not confuse with DCs/B cells/macrophages. |
| **Matrix-remodeling CAF** | `COL10A1`, `COL11A1`, `COMP`, `THBS2`, `MMP2`, `MMP11`, `FN1`, `POSTN`, `TNC`, `LOX`, `CTHRC1` | Strong overlap with fibroblastic OS; CNV is key. |
| **Pericytes** | `RGS5`, `PDGFRB`, `CSPG4`, `MCAM`, `NOTCH3`, `ABCC9`, `KCNJ8`, `COX4I2`, `HIGD1B`, `NDUFA4L2` | Vascular mural cells. |
| **Vascular / airway smooth muscle** | `ACTA2`, `TAGLN`, `MYH11`, `CNN1`, `DES`, `ACTG2`, `LMOD1`, `SMTN`, `PLN` | Strong `MYH11/CNN1` supports smooth muscle. |
| **Pan-endothelial** | `PECAM1`, `CDH5`, `VWF`, `CLDN5`, `ESAM`, `KDR`, `RAMP2`, `EMCN`, `ENG`, `ERG` | Parent EC gate. |
| **General capillary EC / gCap-like** | `FCN3`, `GPIHBP1`, `IL7R`, `RGCC`, `BTNL9`, `EDN1` within EC gate | Capillary subset nomenclature varies. |
| **Aerocyte / aCap-like EC** | `CA4`, `EDNRB`, `SOSTDC1`, `TBX2`, `TBX3`, `APLN`, `HPGD` within EC gate | Specialized gas-exchange capillary EC. |
| **Arterial EC** | `GJA5`, `EFNB2`, `SOX17`, `HEY1`, `DLL4`, `BMX`, `NOTCH4`, `DKK2` | Arterial identity. |
| **Venous / venular EC** | `ACKR1`, `NR2F2`, `VCAM1`, `SELE`, `SELP`, `PLVAP`, `VWF` | Venous/post-capillary venule-like identity. |
| **Lymphatic EC** | `PROX1`, `PDPN`, `LYVE1`, `FLT4`, `CCL21`, `MMRN1`, `TBX1` | `PDPN` is shared; use EC/lymphatic context. |
| **Angiogenic / tip-like EC** | `ESM1`, `KDR`, `FLT1`, `APLN`, `ANGPT2`, `DLL4`, `CXCR4`, `MMP14`, `PGF` | Tumor-associated angiogenesis state. |
| **Mesothelial cells** | `MSLN`, `WT1`, `CALB2`, `UPK3B`, `KRT8`, `KRT18`, `PDPN`, `LRRN4`, `ALDH1A2`, `ITLN1`, `PRG4` | Pleural contamination/involvement. |
| **Schwann / peripheral nerve cells** | `SOX10`, `S100B`, `PLP1`, `MPZ`, `PMP22`, `NGFR` | Rare structural component. |
| **Adipocyte / mature adipose contamination** | `ADIPOQ`, `PLIN1`, `LEP`, `FABP4`, `LPL`, `CFD` | `FABP4` also alveolar macrophage; use parent identity. |

---

## 7. Technical, QC, and non-cell-type signatures

| Signature | Genes | Interpretation |
|---|---|---|
| **Cell cycle / proliferation** | `MKI67`, `TOP2A`, `UBE2C`, `CENPF`, `CDK1`, `CCNB1`, `CCNB2`, `BIRC5`, `TYMS`, `MCM2`, `MCM3`, `MCM4`, `MCM5`, `MCM6`, `MCM7`, `PCNA`, `RRM2` | State; annotate as “cycling T cell”, “cycling tumor”, etc. |
| **Immediate-early / dissociation stress** | `FOS`, `FOSB`, `JUN`, `JUNB`, `DUSP1`, `IER2`, `ATF3`, `EGR1`, `HSPA1A`, `HSPA1B`, `DNAJB1`, `HSPB1`, `SOCS3`, `ZFP36` | Processing/stress; not lineage. |
| **Interferon response** | `ISG15`, `IFI6`, `IFI27`, `IFIT1`, `IFIT2`, `IFIT3`, `MX1`, `MX2`, `OAS1`, `STAT1`, `IRF7` | Shared state across lineages. |
| **Ambient surfactant RNA** | `SFTPA1`, `SFTPA2`, `SFTPB`, `SFTPC`, `SFTPD` | Common in lung; require epithelial coexpression for AT2 calls. |
| **Ambient immunoglobulin RNA** | `IGHG*`, `IGHA*`, `IGKC`, `IGLC*`, `JCHAIN` | Common near plasma cells. |
| **Ambient hemoglobin / RBC** | `HBA1`, `HBA2`, `HBB`, `HBD` | Blood contamination or erythroid cells. |
| **Platelet adherence** | `PPBP`, `PF4`, `GP9`, `ITGA2B`, `TUBB1`, `NRGN` | If coexpressed with another lineage, likely adherence/doublet. |
| **Doublet red flags** | `PTPRC` with strong epithelial/endothelial/tumor ECM markers; `EPCAM + COL1A1`; `PECAM1 + CD3D`; `PPBP/PF4` with another lineage | Review UMI counts, doublet scores, and marker coexpression. |

---

## 8. High-priority marker-collision warnings

| Collision-prone marker/program | Why it is dangerous | Resolution |
|---|---|---|
| `COL1A1`, `COL1A2`, `SPARC`, `POSTN`, `FN1`, `THBS2`, `TNC` | Osteosarcoma, fibroblasts, CAFs, myofibroblasts all express ECM genes. | Use CNV + `SATB2/RUNX2/SP7/ALPL/IBSP/BGLAP`. |
| `SPP1` | Osteosarcoma, SPP1+ TAMs, AT2/injury epithelium, CAFs. | Use parent markers: tumor CNV/osteogenic vs myeloid `PTPRC/CSF1R` vs epithelial `EPCAM/KRT/SFTPC`. |
| `LAMP3` | AT2 cells and mature/migratory DCs. | `EPCAM/SFTPC/ABCA3` versus `PTPRC/HLA-DRA/CCR7/FSCN1`. |
| `HLA-DRA`, `CD74` | B cells, macrophages, DCs, apCAFs, IFN/MHC-II+ tumor. | Use `PTPRC`, B/T/myeloid markers, fibroblast markers, and CNV. |
| `ACTA2`, `TAGLN`, `MYL9` | Smooth muscle, pericyte/myofibroblast, myCAF, fibroblastic tumor. | `MYH11/CNN1` for SMC; `RGS5/PDGFRB` for pericyte; CNV/osteogenic markers for tumor. |
| `SATB2` | Osteoblastic differentiation, but also colorectal lineage/carcinoma and other diagnostic pitfalls. | If `SATB2+` cells are `EPCAM/KRT/CDX2+`, consider epithelial metastasis differential. Use OS panel + CNV. |
| `ATP6V0D2` | Osteoclasts and pulmonary ionocytes. | Osteoclasts: `CTSK/ACP5/MMP9/DCSTAMP/CSF1R`; ionocytes: `FOXI1/CFTR/ASCL3`. |
| `FABP4` | Alveolar macrophages, adipocytes, some stromal/endothelial contexts. | Use `PTPRC/C1Q/MARCO/PPARG` for macrophages; `ADIPOQ/PLIN1/LEP` for adipocytes. |
| `KRT17` | Basal cells, aberrant basaloid injury epithelium, squamous carcinoma differential. | Use CNV, `EPCAM/KRT` context, `TP63/KRT5`, and pathology. |

---

## 9. Compact consensus signature dictionary

```yaml
osteosarcoma_core:
  [SATB2, RUNX2, SP7, ALPL, IBSP, BGLAP, SPP1, COL1A1, COL1A2, SPARC, CDH11, POSTN, MMP13]

osteosarcoma_osteoblastic:
  [RUNX2, SP7, SATB2, ALPL, COL1A1, COL1A2, SPARC, IBSP, BGLAP, SPP1, MGP, BGN, DLX5, MSX2, OMD, MEPE]

osteosarcoma_chondroblastic:
  [SOX9, SOX5, SOX6, ACAN, COL2A1, COL9A1, COL9A2, COL9A3, COL10A1, COL11A2, COMP, MATN3, HAPLN1]

osteosarcoma_fibroblastic_ecm:
  [COL1A1, COL1A2, COL3A1, COL5A1, COL5A2, FN1, TNC, THBS2, POSTN, MMP2, MMP11, MMP14, SERPINE1, CDH11]

osteosarcoma_proliferation:
  [MKI67, TOP2A, UBE2C, CENPF, CDK1, CCNB1, CCNB2, BIRC5, TYMS, MCM2, MCM3, MCM4, MCM5, MCM6, MCM7, PCNA, RRM2]

osteosarcoma_hypoxia:
  [CA9, VEGFA, SLC2A1, LDHA, PDK1, NDRG1, BNIP3, HILPDA, ENO1, PGK1, ADM]

osteosarcoma_invasive_matrix:
  [CXCL8, IL6, CXCL1, CXCL2, MMP9, MMP13, MMP14, LOX, LOXL2, SERPINE1, PLAUR, ITGA5, TNC, POSTN]

AT1:
  [AGER, PDPN, CAV1, CAV2, AQP5, HOPX, CLDN18, EMP2, RTKN2, CLIC5]

AT2:
  [SFTPA1, SFTPA2, SFTPB, SFTPC, SFTPD, ABCA3, SLC34A2, NAPSA, LAMP3, LPCAT1, ETV5]

epithelial_injury_transition:
  [KRT8, KRT18, KRT19, CLDN4, CDKN1A, LGALS3, LCN2, SFN, KRT7, TACSTD2, MDK, GDF15]

club:
  [SCGB1A1, SCGB3A1, SCGB3A2, CYP2F1, BPIFA1, WFDC2, MUC5B, TFF3]

ciliated:
  [FOXJ1, PIFO, TPPP3, RSPH1, DNAH5, DNAI1, CCDC39, CAPS, SNTN, C20orf85]

basal:
  [KRT5, KRT14, KRT15, KRT17, TP63, NGFR, ITGA6, DST, S100A2]

goblet:
  [MUC5AC, MUC5B, SPDEF, AGR2, TFF3, CLCA1, FCGBP]

ionocyte:
  [FOXI1, CFTR, ASCL3, ATP6V1B1, ATP6V0D2, BSND, TMEM61]

tuft:
  [POU2F3, TRPM5, DCLK1, GFI1B, AVIL, GNAT3, LRMP]

T_cells:
  [CD3D, CD3E, CD3G, TRAC, TRBC1, TRBC2, CD2, CD247]

CD8_cytotoxic_T:
  [CD8A, CD8B, NKG7, PRF1, GZMB, GZMH, GNLY, CST7, CCL5]

exhausted_T:
  [PDCD1, LAG3, HAVCR2, TIGIT, CTLA4, TOX, CXCL13, ENTPD1, TNFRSF9, ITGAE]

Treg:
  [FOXP3, IL2RA, CTLA4, IKZF2, TIGIT, TNFRSF18, TNFRSF4, CCR8, BATF]

NK:
  [NKG7, GNLY, PRF1, GZMB, KLRD1, KLRF1, NCR1, FCGR3A, TYROBP]

B_cells:
  [MS4A1, CD79A, CD79B, CD19, CD22, BANK1, CD74, HLA-DRA, TCL1A, IGHD, IGHM]

plasma_cells:
  [JCHAIN, MZB1, XBP1, PRDM1, SDC1, TNFRSF17, IGHG1, IGHA1, IGKC]

classical_monocytes:
  [LYZ, LST1, S100A8, S100A9, S100A12, FCN1, VCAN, CD14, CCR2]

alveolar_macrophages:
  [MARCO, FABP4, PPARG, LPL, MRC1, MSR1, SIGLEC1, APOC1, APOE, MCEMP1]

SPP1_TREM2_TAM:
  [SPP1, TREM2, GPNMB, APOE, LGALS3, CTSB, CTSL, MMP9, MMP12, CHI3L1, FABP5, CD9]

cDC1:
  [CLEC9A, XCR1, BATF3, IRF8, CADM1, CLNK, WDFY4]

cDC2:
  [CD1C, FCER1A, CLEC10A, CD1E, HLA-DRA, IRF4, FCGR2B]

LAMP3_migratory_DC:
  [LAMP3, CCR7, FSCN1, CCL19, CCL17, CCL22, IDO1, IL4I1, CD83, CD40]

pDC:
  [CLEC4C, LILRA4, IL3RA, TCF4, IRF7, GZMB, JCHAIN]

mast_cells:
  [TPSAB1, TPSB2, CPA3, KIT, MS4A2, HDC, CMA1]

neutrophils:
  [S100A8, S100A9, FCGR3B, CSF3R, CXCR2, LCN2, CEACAM8, MPO, ELANE, OLR1]

osteoclasts:
  [ACP5, CTSK, MMP9, DCSTAMP, OCSTAMP, ATP6V0D2, TNFRSF11A, CALCR, CA2, SIGLEC15, ITGB3, TCIRG1, NFATC1]

fibroblasts:
  [COL1A1, COL1A2, COL3A1, DCN, LUM, DPT, PDGFRA, COL6A1, C1R, C1S, FBLN1]

myCAF:
  [ACTA2, TAGLN, MYL9, TPM2, FAP, POSTN, COL1A1, COL3A1, COL11A1, LRRC15, ITGA11, CTHRC1, COMP]

iCAF:
  [IL6, CXCL12, CXCL14, CXCL1, CXCL2, CXCL8, CCL2, LIF, HAS1, PDGFRA]

apCAF:
  [HLA-DRA, HLA-DRB1, HLA-DPA1, HLA-DPB1, CD74, CIITA]

pericytes:
  [RGS5, PDGFRB, CSPG4, MCAM, NOTCH3, ABCC9, KCNJ8, COX4I2]

smooth_muscle:
  [ACTA2, TAGLN, MYH11, CNN1, DES, ACTG2, LMOD1, SMTN]

endothelial:
  [PECAM1, CDH5, VWF, CLDN5, ESAM, KDR, RAMP2, EMCN]

gCap_endothelial:
  [FCN3, GPIHBP1, IL7R, RGCC, BTNL9]

aCap_endothelial:
  [CA4, EDNRB, SOSTDC1, TBX2, TBX3, APLN]

arterial_endothelial:
  [GJA5, EFNB2, SOX17, HEY1, DLL4, BMX, NOTCH4]

venous_endothelial:
  [ACKR1, NR2F2, VCAM1, SELE, SELP, PLVAP, VWF]

lymphatic_endothelial:
  [PROX1, PDPN, LYVE1, FLT4, CCL21, MMRN1]

mesothelial:
  [MSLN, WT1, CALB2, UPK3B, KRT8, KRT18, PDPN, LRRN4, ITLN1]

erythroid:
  [HBA1, HBA2, HBB, HBD, ALAS2, AHSP]

platelet:
  [PPBP, PF4, GP9, ITGA2B, TUBB1, NRGN]

dissociation_stress:
  [FOS, FOSB, JUN, JUNB, DUSP1, IER2, ATF3, EGR1, HSPA1A, HSPA1B, DNAJB1, HSPB1]
```

---

## 10. Suggested cluster-level deliverable

For each cluster, report:

```text
cluster_id
n_cells
top_DE_genes
broad_lineage_call
best_signature_score
second_best_signature_score
CNV_status
reference_mapping_label
final_annotation
confidence: high / medium / low
notes / caveats / collision markers
```

Flag clusters as **requires orthogonal validation** if:

- CNV status is ambiguous.
- Top two signature scores are close.
- Annotation depends heavily on collision-prone genes such as `SPP1`, `LAMP3`, `ACTA2`, `SATB2`, `KRT17`, `ATP6V0D2`, or `FABP4`.
- A cluster coexpresses markers from incompatible parent lineages, e.g. `PTPRC + EPCAM`, `CD3D + PECAM1`, `COL1A1 + EPCAM`, or `PF4/PPBP` with a strong non-platelet lineage.

---

# References

The merged bibliography below preserves the key literature and tool references cited across the three supplied reports. Items after mid-2024 or tool/web resources should be verified against the final manuscript or database record before formal publication use.

1. Zhou Y, Yang D, Yang Q, et al. Single-cell RNA landscape of intratumoral heterogeneity and immunosuppressive microenvironment in advanced osteosarcoma. *Nature Communications.* 2020;11:6322.  
2. Klein MJ, Siegal GP. Osteosarcoma: anatomic and histologic variants. *American Journal of Clinical Pathology.* 2006;125:555–581.  
3. Kansara M, Teng MWL, Smyth MJ, Thomas DM. Translational biology of osteosarcoma. *Nature Reviews Cancer.* 2014;14:722–735.  
4. Isakoff MS, Bielack SS, Meltzer P, Gorlick R. Osteosarcoma: current treatment and a collaborative pathway to success. *Journal of Clinical Oncology.* 2015;33:3029–3035.  
5. Gill J, Gorlick R. Advancing therapy for osteosarcoma. *Nature Reviews Clinical Oncology.* 2021;18:609–624.  
6. Rickel K, Fang F, Tao J. Molecular genetics of osteosarcoma. *Bone.* 2017;102:69–79.  
7. Behjati S, Tarpey PS, Haase K, et al. Recurrent mutation of IGF signalling genes and distinct patterns of genomic rearrangement in osteosarcoma. *Nature Communications.* 2017;8:15936.  
8. Chen X, Bahrami A, Pappo A, et al. Recurrent somatic structural variations contribute to tumorigenesis of osteosarcoma. *Cell Reports.* 2014;7:104–112.  
9. Komori T, Yagi H, Nomura S, et al. Targeted disruption of Cbfa1 results in a complete lack of bone formation owing to maturational arrest of osteoblasts. *Cell.* 1997;89:755–764.  
10. Nakashima K, Zhou X, Kunkel G, et al. The novel zinc finger-containing transcription factor osterix is required for osteoblast differentiation and bone formation. *Cell.* 2002;108:17–29.  
11. Dobreva G, Chahrour M, Dautzenberg M, et al. SATB2 is a multifunctional determinant of craniofacial patterning and osteoblast differentiation. *Cell.* 2006;125:971–986.  
12. Conner JR, Hornick JL. SATB2 is a novel marker of osteoblastic differentiation in bone and soft tissue tumours. *Histopathology.* 2013;63:36–49.  
13. Akiyama H, Chaboissier MC, Martin JF, Schedl A, de Crombrugghe B. The transcription factor Sox9 has essential roles in successive steps of the chondrocyte differentiation pathway. *Genes & Development.* 2002;16:2813–2828.  
14. Bi W, Deng JM, Zhang Z, Behringer RR, de Crombrugghe B. Sox9 is required for cartilage formation. *Nature Genetics.* 1999;22:85–89.  
15. Boyle WJ, Simonet WS, Lacey DL. Osteoclast differentiation and activation. *Nature.* 2003;423:337–342.  
16. Teitelbaum SL. Bone resorption by osteoclasts. *Science.* 2000;289:1504–1508.  
17. Yagi M, Miyamoto T, Sawatani Y, et al. DC-STAMP is essential for cell-cell fusion in osteoclasts and foreign body giant cells. *Journal of Experimental Medicine.* 2005;202:345–351.  
18. Buddingh EP, Kuijjer ML, Duim RAJ, et al. Tumor-infiltrating macrophages are associated with metastasis suppression in high-grade osteosarcoma. *Clinical Cancer Research.* 2011;17:2110–2119.  
19. Travaglini KJ, Nabhan AN, Penland L, et al. A molecular cell atlas of the human lung from single-cell RNA sequencing. *Nature.* 2020;587:619–625.  
20. Sikkema L, Ramírez-Suástegui C, Strobl DC, et al. An integrated cell atlas of the lung in health and disease. *Nature Medicine.* 2023;29:1563–1577.  
21. Vieira Braga FA, Kar G, Berg M, et al. A cellular census of human lungs identifies novel cell states in health and in asthma. *Nature Medicine.* 2019;25:1153–1163.  
22. Deprez M, Zaragosi LE, Truchi M, et al. A single-cell atlas of the human healthy airways. *American Journal of Respiratory and Critical Care Medicine.* 2020;202:1636–1645.  
23. Plasschaert LW, Žilionis R, Choo-Wing R, et al. A single-cell atlas of the airway epithelium reveals the CFTR-rich pulmonary ionocyte. *Nature.* 2018;560:377–381.  
24. Montoro DT, Haber AL, Biton M, et al. A revised airway epithelial hierarchy includes CFTR-expressing ionocytes. *Nature.* 2018;560:319–324.  
25. Habermann AC, Gutierrez AJ, Bui LT, et al. Single-cell RNA sequencing reveals profibrotic roles of distinct epithelial and mesenchymal lineages in pulmonary fibrosis. *Science Advances.* 2020;6:eaba1972.  
26. Adams TS, Schupp JC, Poli S, et al. Single-cell RNA-seq reveals ectopic and aberrant lung-resident cell populations in idiopathic pulmonary fibrosis. *Science Advances.* 2020;6:eaba1983.  
27. Kobayashi Y, Tata A, Konkimalla A, et al. Persistence of a regeneration-associated, transitional alveolar epithelial cell state in pulmonary fibrosis. *Nature Cell Biology.* 2020;22:934–946.  
28. Schupp JC, Adams TS, Cosme C Jr, et al. Integrated single-cell atlas of endothelial cells of the human lung. *Circulation.* 2021;144:286–302.  
29. Kalucka J, de Rooij LPMH, Goveia J, et al. Single-cell transcriptome atlas of murine and human endothelial cells. *Cell.* 2020;180:764–779.e20.  
30. Gillich A, Zhang F, Farmer CG, et al. Capillary cell-type specialization in the alveolus. *Nature.* 2020;586:785–790.  
31. Travis WD, Brambilla E, Nicholson AG, et al. The 2015 WHO classification of lung tumors. *Journal of Thoracic Oncology.* 2015;10:1243–1260.  
32. Lambrechts D, Wauters E, Boeckx B, et al. Phenotype molding of stromal cells in the lung tumor microenvironment. *Nature Medicine.* 2018;24:1277–1289.  
33. Zilionis R, Engblom C, Pfirschke C, et al. Single-cell transcriptomics of human and mouse lung cancers reveals conserved myeloid populations across individuals and species. *Immunity.* 2019;50:1317–1334.e10.  
34. Lavin Y, Kobayashi S, Leader A, et al. Innate immune landscape in early lung adenocarcinoma by paired single-cell analyses. *Cell.* 2017;169:750–765.e17.  
35. Guo X, Zhang Y, Zheng L, et al. Global characterization of T cells in non-small-cell lung cancer by single-cell sequencing. *Nature Medicine.* 2018;24:978–985.  
36. Maynard A, McCoach CE, Rotow JK, et al. Therapy-induced evolution of human lung cancer revealed by single-cell RNA sequencing. *Cell.* 2020;182:1232–1251.e22.  
37. Leader AM, Grout JA, Maier BB, et al. Single-cell analysis of human non-small cell lung cancer lesions refines tumor classification and patient stratification. *Cancer Cell.* 2021;39:1594–1609.e12.  
38. Villani AC, Satija R, Reynolds G, et al. Single-cell RNA-seq reveals new types of human blood dendritic cells, monocytes, and progenitors. *Science.* 2017;356:eaah4573.  
39. See P, Dutertre CA, Chen J, et al. Mapping the human DC lineage through the integration of high-dimensional techniques. *Science.* 2017;356:eaag3009.  
40. Dutertre CA, Becht E, Irac SE, et al. Single-cell analysis of human mononuclear phagocytes reveals subset-defining markers and identifies circulating inflammatory dendritic cells. *Immunity.* 2019;51:573–589.e8.  
41. Guilliams M, Ginhoux F, Jakubzick C, et al. Dendritic cells, monocytes and macrophages: a unified nomenclature based on ontogeny. *Nature Reviews Immunology.* 2014;14:571–578.  
42. Cheng S, Li Z, Gao R, et al. A pan-cancer single-cell transcriptional atlas of tumor infiltrating myeloid cells. *Cell.* 2021;184:792–809.e23.  
43. Cassetta L, Fragkogianni S, Sims AH, et al. Human tumor-associated macrophage and monocyte transcriptional landscapes reveal cancer-specific reprogramming. *Cancer Cell.* 2019;35:588–602.e10.  
44. Wherry EJ, Kurachi M. Molecular and cellular insights into T cell exhaustion. *Nature Reviews Immunology.* 2015;15:486–499.  
45. Thommen DS, Schumacher TN. T cell dysfunction in cancer. *Cancer Cell.* 2018;33:547–562.  
46. Sakaguchi S, Yamaguchi T, Nomura T, Ono M. Regulatory T cells and immune tolerance. *Cell.* 2008;133:775–787.  
47. Zheng C, Zheng L, Yoo JK, et al. Landscape of infiltrating T cells in liver cancer revealed by single-cell sequencing. *Cell.* 2017;169:1342–1356.e16.  
48. Öhlund D, Handly-Santana A, Biffi G, et al. Distinct populations of inflammatory fibroblasts and myofibroblasts in pancreatic cancer. *Journal of Experimental Medicine.* 2017;214:579–596.  
49. Elyada E, Bolisetty M, Laise P, et al. Cross-species single-cell analysis of pancreatic ductal adenocarcinoma reveals antigen-presenting cancer-associated fibroblasts. *Cancer Discovery.* 2019;9:1102–1123.  
50. Kieffer Y, Hocine HR, Gentric G, et al. Single-cell analysis reveals fibroblast clusters linked to immunotherapy resistance in cancer. *Cancer Discovery.* 2020;10:1330–1351.  
51. Dominguez CX, Müller S, Keerthivasan S, et al. Single-cell RNA sequencing reveals stromal evolution into LRRC15+ myofibroblasts as a determinant of patient response to cancer immunotherapy. *Cancer Discovery.* 2020;10:232–253.  
52. Buechler MB, Pradhan RN, Krishnamurty AT, et al. Cross-tissue organization of the fibroblast lineage. *Nature.* 2021;593:575–579.  
53. Tirosh I, Izar B, Prakadan SM, et al. Dissecting the multicellular ecosystem of metastatic melanoma by single-cell RNA-seq. *Science.* 2016;352:189–196.  
54. Patel AP, Tirosh I, Trombetta JJ, et al. Single-cell RNA-seq highlights intratumoral heterogeneity in primary glioblastoma. *Science.* 2014;344:1396–1401.  
55. Puram SV, Tirosh I, Parikh AS, et al. Single-cell transcriptomic analysis of primary and metastatic tumor ecosystems in head and neck cancer. *Cell.* 2017;171:1611–1624.e24.  
56. Gao R, Bai S, Henderson YC, et al. Delineating copy number and clonal substructure in human tumors from single-cell transcriptomes. *Nature Biotechnology.* 2021;39:599–608.  
57. Aran D, Looney AP, Liu L, et al. Reference-based analysis of lung single-cell sequencing reveals a transitional profibrotic macrophage. *Nature Immunology.* 2019;20:163–172.  
58. The Tabula Sapiens Consortium. The Tabula Sapiens: a multiple-organ, single-cell transcriptomic atlas of humans. *Science.* 2022;376:eabl4896.  
59. Gao R, et al. CopyKAT / copy-number inference approaches for malignant-cell identification from scRNA-seq. See also Ref. 56.  
60. Numbat: haplotype-aware analysis of somatic copy-number variations from single-cell RNA-seq, as cited in the supplied reports.  
61. Wolock SL, Lopez R, Klein AM. Scrublet: computational identification of cell doublets in single-cell transcriptomic data. *Cell Systems.* 2019;8:281–291.e9.  
62. Young MD, Behjati S. SoupX removes ambient RNA contamination from droplet-based single-cell RNA sequencing data. *GigaScience.* 2020;9:giaa151.  
63. Andreatta M, Carmona SJ. UCell: robust and scalable single-cell gene signature scoring. *Computational and Structural Biotechnology Journal.* 2021;19:3796–3798.  
64. Zheng L, Qin S, Si W, et al. Pan-cancer single-cell landscape of tumor-infiltrating T cells. *Science.* 2021;374:abe6474.  
65. Qian J, Olbrecht S, Boeckx B, et al. A pan-cancer blueprint of the heterogeneous tumor microenvironment revealed by single-cell profiling. *Cell Research.* 2020;30:745–762.  
66. Hu C, Li T, Xu Y, et al. CellMarker 2.0: an updated database of manually curated cell markers in human/mouse and web tools based on scRNA-seq data. *Nucleic Acids Research.* 2023;51:D870–D876.  
67. Zhang X, Lan Y, Xu J, et al. CellMarker: a manually curated resource of cell markers in human and mouse. *Nucleic Acids Research.* 2019;47:D721–D728.  
68. Sharma AE, Pytel P, Cipriani NA. SOX9 and SATB2 immunohistochemistry cannot reliably distinguish between osteosarcoma and chondrosarcoma on biopsy material. *Human Pathology.* 2022;121:56–64.  
69. Szczepanski JM, Siddiqui J, Patel RM, et al. Expression of SATB2 in primary cutaneous sarcomatoid neoplasms: a potential diagnostic pitfall. *Pathology.* 2023;55:350–354.  
70. Owosho AA, Ladeji AM, Adesina OM, et al. SATB2 and MDM2 immunoexpression and diagnostic role in primary osteosarcomas of the jaw. *Dentistry Journal.* 2021;10:4.  
71. Reinecke JB, Jimenez Garcia L, Gross AC, et al. Aberrant activation of wound-healing programs within the metastatic niche facilitates lung colonization by osteosarcoma cells. *Clinical Cancer Research.* 2025;31:414–429. Source-supplied reference; verify details before formal use.  
72. Liu F, Zhang T, Yang Y, et al. Integrated analysis of single-cell and bulk transcriptomics reveals cellular subtypes and molecular features associated with osteosarcoma prognosis. *BMC Cancer.* 2025. Source-supplied reference; verify details before formal use.  
73. Li X, Liu J, Wang Y, Hu J, Wang Q. Molecular characterization of cell dynamics during osteosarcoma progression. *Translational Oncology.* 2026. Source-supplied reference; verify details before formal use.  
74. Li H, Sun C, Yang M. Single-cell transcriptomic profiling reveals cellular heterogeneity and identifies novel therapeutic targets in osteosarcoma. *International Journal of Genomics.* 2026. Source-supplied reference; verify details before formal use.  
75. Peng F, Jiang CS, Zheng Z, et al. Transcriptomic signature-guided depletion of intermediate alveolar epithelial cells ameliorates pulmonary fibrosis in mice. *Nature Communications.* 2026. Source-supplied reference; verify details before formal use.  
76. Wu B, Shichino S, Ueha S, et al. Ex vivo lung-organoid model for aberrant basaloid cell induction and activation. *Inflammation and Regeneration.* 2025. Source-supplied reference; verify details before formal use.