# Gene Signatures for Lung-Metastatic Osteosarcoma Single Cells

- **Malignant Evidence** -> Identify malignant cells via CNV inference using Numbat or CopyKAT to distinguish tumor from normal cells and reconstruct profiles [3] [97] [100]. This addresses significant intratumoral heterogeneity [35].
- **OS Differentiation** -> Characterize differentiation states using markers for osteoblastic (RUNX2, SPP1), chondroblastic (SOX9, ACAN), fibroblastic (COL3A1), cycling (MKI67, TOP2A), and stem-like (FGF2, THY1) cells [18] [16]. SATB2 is a sensitive diagnostic marker [44].
- **Host Epithelium** -> Annotate lung cells like Basal (KRT5+), Ciliated (C20orf85+), AT1 (AGER+), AT2 (SFTPC+), Club (SCGB1A1+), Goblet (MUC5B+), Ionocyte (FOXI1+), and Neuroendocrine (CHGA+) [6] [9] [51]. Monitor rare types in niches [93].
- **Stroma** -> Delineate Alveolar (NPNT), Adventitial (PI16), and Peribronchial (FGF18) fibroblasts, pericytes (ACTA2), and MSCs (CXCL12) [83] [16] [6]. Markers like ACTA2 lack absolute specificity [82].
- **Immune** -> Identify T cells (CD3D, CD8), macrophages (CD14, SPP1), and osteoclasts (CTSK, ACP5) [16] [11] [78]. Distinguish osteoclasts by high CTSK and low CD14 [78].
- **Artifacts** -> Mitigate ambient RNA with SoupX and doublets with Scrublet to eliminate hybrid states [40] [41] Benchmarking Computational Doublet-Detection Methods ....
- **Clinical Correlation** -> Apply SATB2 for OS and TTF-1 for lung cancer [44] [88]. Evaluate prognostic SPP1+ macrophages [55] and metastasis hub genes [23].
- **Uncertainty** -> Acknowledge sample size limits and chemotherapy effects [16]. Validate metastasis pathways through clinical studies [23] [64].

## Diagnostic Architecture: Separate Malignancy, Lineage, and State

Numbat is a haplotype-aware tool that reconstructs tumor copy number profiles to differentiate and identify malignant cells within the microenvironment [97]. It outperformed other tools in tumor versus normal cell classification and subclonal structure inference [3]. CopyKAT identifies tumor cells in unbiased scRNA-seq data, even with lower sequencing depth [98].

SATB2 marks osteoblastic differentiation in neoplastic spindle and polygonal cells [45]. In lung contexts, NKX2-1 and NAPSA identify alveolar epithelial cells and lung-derived malignancies [6] [50]. TTF-1 and Napsin-A achieve 99.1% specificity for pulmonary adenocarcinoma [88].

| Layer | Feature | Markers/Tools | Source |
| :--- | :--- | :--- | :--- |
| Malignancy | CNV | Numbat | [3] |
| Lineage | Osteo | SATB2 | [46] |
| Lineage | Lung | NKX2-1 | [50] |
| State | Stress | Stem | [17] |

SATB2 shows 92.6% sensitivity for osteosarcoma but only 50.0% specificity, appearing in giant cell tumors and fibrous dysplasia [45] [44]. COL1A1 is ubiquitous in mesenchymal lineages and kidney tumors, failing to distinguish malignant osteoblasts from reactive fibroblasts [40].

Diagnosis requires integrating CNV inference with coherent gene expression and pathology [3]. Numbat precisely identifies malignant cells by reconstructing copy number profiles [97]. This multi-modal approach is essential for identifying malignant cells in single-cell transcriptomics [100].

**Accurate identification of malignant cells requires the integration of haplotype-aware CNV inference with lineage-specific marker expression to overcome the low specificity of individual markers like SATB2.**

Research use only, not diagnosis.

## Osteosarcoma Cells: Differentiation Programs, Not One Marker

Osteosarcoma (OS) shows high intratumoral heterogeneity with diverse differentiation programs [18] Single-cell RNA landscape of intratumoral heterogeneity ... [62].

| Program | Marker Genes | Interpretation/Caveat |
|---|---|---|
| Osteoblastic | RUNX2, SPP1 [18], ALPL [63] | Validated human markers [18] [63]. |
| Chondroblastic | SOX9, ACAN [18] | Validated human markers [18]. |
| Chondro-transitional | RUNX2, SPP1 Single-cell RNA landscape of intratumoral heterogeneity ... | Transdifferentiating cells Single-cell RNA landscape of intratumoral heterogeneity .... |
| Fibroblastic | COL3A1, DCN [18] Single-cell RNA landscape of intratumoral heterogeneity ... | Validated human markers [18] Single-cell RNA landscape of intratumoral heterogeneity .... |
| Stem/Progenitor | FGF2, THY1 [18] | Validated human markers [18]. |
| Adipogenic | ADIPOQ, PLIN1 [18] | Stromal program [18]. |
| S phase | PCNA, RRM2 Single-cell RNA landscape of intratumoral heterogeneity ... | Proliferating cells Single-cell RNA landscape of intratumoral heterogeneity .... |
| G2/M phase | UBE2C, HMGB2 Single-cell RNA landscape of intratumoral heterogeneity ... | Proliferating cells Single-cell RNA landscape of intratumoral heterogeneity .... |
| Metastatic | Skp2, KIF20A [22], SEC16B [63] | Hub genes [22]; SEC16B loss aids invasion [63]. |

| Stage | Marker Genes | Interpretation/Caveat |
|---|---|---|
| Progenitor | CD14, CXCR4 Transcriptional reprogramming during human osteoclast ... [78] | Monocyte origin [78]. |
| Pre-osteoclast | NFATc1, RANK [78] Transcriptional reprogramming during human osteoclast ... | NFATc1 regulates lineage Transcriptional reprogramming during human osteoclast .... |
| Mature | CTSK, ACP5 [78] Transcriptional reprogramming during human osteoclast ... | CTSK/ACP5 mark maturity [78] Transcriptional reprogramming during human osteoclast .... |

Distinguish osteoclasts from macrophages via CTSK/ACP5 Transcriptional reprogramming during human osteoclast ... [78]. CD14 is lost during differentiation Transcriptional reprogramming during human osteoclast .... CALCR/DCSTAMP are specific to bone-resorption Transcriptional reprogramming during human osteoclast ....

Skp2 knockout reduces metastasis and exhaustion, upregulating IFN [24]. Caveats: Myc escape, instability, and plasticity Single cell RNA analysis of murine osteosarcoma uncovers .... IFN scores correlate with survival in human data Single cell RNA analysis of murine osteosarcoma uncovers ....

Studies (Zhou, Truong, Liu) identify malignant states and SEC16B loss [18] Single-cell RNA landscape of intratumoral heterogeneity ... [23] [63] [22]. Multi-marker panels are essential [18] Single-cell RNA landscape of intratumoral heterogeneity ... [63].

Caveats: normal tissue overlap; map gaps; chemo/small samples alter profiles [18] Single-cell RNA landscape of intratumoral heterogeneity .... Metastasis genes need validation [23] [63].

**Accurate characterization requires multi-marker panels for heterogeneity.**

## Host Lung Epithelium: A Reference Panel From AT1 to Rare Airway Cells

The Human Lung Cell Atlas (HLCA) is a foundational reference for human lung cell types, integrating 2.4 million single-cell transcriptomes from 486 individuals across 49 datasets [51] [33]. This atlas defines 61 cell identities in a five-level hierarchical framework [51]. This structure enables precise identification of common and rare cell states, including novel AT0 cells [51] [52]. Mapping new single-cell data to this reference allows rapid, accurate cell type annotation, aiding discovery of disease states and understanding lung biology [51] Mapping single-cell data to reference atlases by transfer ....

| CELL POPULATION | POSITIVE MARKERS (* = Broad) | CONTRAST/CAVEAT |
| :-------------- | :--------------------------- | :-------------- |
| AT1             | AGER, MYRF, CAV1, CLIC5, EPCAM* [6] | |
| AT2             | SFTPC*, SFTPA1, ETV5, WIF1, HHIP, CA2, WNT5A, LRP5 [6] | Proportions decrease in severe COPD [51]. |
| AT0             | SFTPB, SCGB3A2, SFTPC, SCGB3A1 [51] | Rare, novel cell state [51]. |
| Basal           | KRT5*, TP63, SERPINB3, ALOX15, ADH7, HES1, KRT7, SCGB3A2 [6] | |
| Ciliated        | C20orf85*, DHRS9, TPPP3, CAPS [6] | Present in human SMG ducts, absent in pig SMG ducts [93]. |
| Club/Mucous     | SCGB1A1, MUC5B, MUC5AC [6] | |
| Pulmonary Neuroendocrine | CHGA, ASCL1 [6] | Often enriched in specific niches [51]. |
| Ionocyte        | FOXI1, ASCL3, CFTR, BSND [6] [91] | Extremely rare (0.45% of airway epithelial cells) [91]. |
| Tuft            | GNAT3, IL25, ALOX5AP [91] | Mature tuft cells (0.002% of airway epithelial cells) often mislabeled "Other" [91]. |
| Hillock         | KRT6A, KRT13, KRT14 [51] | |
| Submucosal Gland Cells | (Niche for rare cells) [51] | Rare epithelial cells often enriched here [51]. |

The HLCA offers a robust framework for identifying common and rare epithelial cell types, including those in niches like submucosal glands [9] [51]. Its utility is shown by identifying novel AT0 cells, enhancing understanding of lung cellular diversity [51]. However, single-cell RNA sequencing requires accounting for ambient RNA contamination Mitigating ambient RNA and doublets effects on single cell .... This is critical for highly expressed genes (e.g., SFTPC, SFTPA1), where ambient RNA causes false positive marker signals [40]. Tools like SoupX are essential for removing ambient RNA from droplet-based scRNA-seq data, ensuring accurate cell type annotation and analysis [40] [42].

**Leveraging comprehensive lung cell atlases and robust computational methods is critical for accurate identification and characterization of both abundant and rare epithelial cell populations in human lung single-cell data.**

## Lung Vascular and Mesenchymal Cells: Resolve the COL1A1 Overlap

Lung mesenchymal and vascular compartments exhibit significant transcriptomic overlap, particularly regarding extracellular matrix (ECM) genes like COL1A1 [82]. While COL1A1 is a hallmark of fibroblasts, it is upregulated across all mesenchymal subtypes during fibrotic remodeling [82]. Distinguishing these populations requires specific markers like NPNT for alveolar fibroblasts or PI16 for adventitial subsets [83].

In pulmonary tumors, differentiating host fibroblasts from fibroblastic-osteosarcoma is vital for clinical research [90]. Malignant osteosarcoma cells express bone-lineage markers SATB2 and RUNX2, which are absent in healthy lung fibroblasts [44] [46]. Both cell types may express high levels of COL1A1 and ACTA2, necessitating the use of specific osteoblastic markers for accurate identification [83].

| Type | Markers | Hazard |
| :--- | :--- | :--- |
| Pan-endothelial | PECAM1, CDH5, CLDN5 | Vimentin [9] |
| Aerocyte capillary | EDNRB, SOSTDC1, TBX2 | AGER [9] |
| General capillary | CA4, PRX, FCN3 | vWF [9] |
| Arterial | EFNB2, SOX17, GJA5 | MGP [9] |
| Venous | NR2F2, VCAM1, ACKR1 | IGFBP7 [9] |
| Systemic venous | COL15A1, VWA1, PLVAP | COL15A1 [9] |
| Lymphatic | PROX1, LYVE1, PDPN | PDPN [9] |
| Alveolar fibroblast | GPC3, FGFR4, NPNT | COL1A1 [9] |
| Adventitial fibroblast | SERPINF1, PI16, DCN | PI16 [9] |
| Peribronchial fibroblast | FGF18, WIF1, ASPN | WIF1 [9] |
| Myofibroblast | ASPN, WIF1, ACTA2 | ACTA2 [9] |
| CTHRC1 fibroblast | CTHRC1, POSTN, TNC | COL1A1 [9] |
| Pericyte | COX4I2, TBX5, PDGFRB | PDGFRB [9] |
| Smooth muscle | MYH11, CNN1, ACTG2 | ACTA2 [9] |
| Lipofibroblast | APOE, PLIN2, TCF21 | PDGFRA [9] |
| Mesothelial | MSLN, PDPN, ITLN1 | PDPN [9] |

**Accurate resolution of COL1A1+ populations requires bone-specific markers like SATB2 to distinguish malignant osteosarcoma from reactive host fibroblasts.**

## Immune Compartment: Clinically Interpretable Lineages and States

Immune lineages have distinct transcriptomes [11]A pan-cancer single-cell transcriptional atlas of tumor ...[58]. Subsets: pan-T (_CD3D/E/G_) [66], naive CD4 (_SELL_, _LEF1_, _CCR7_) [11], Treg (_FOXP3_, _CTLA4_, _IL2RA_) [11], Tfh (_CXCL13_, _BCL6_) [11], and CD8 T (cytotoxic _GZMA_, _PRF1_ to exhausted _HAVCR2_, _LAG3_, _PDCD1_) [11][58]. NK cells: bright (_NCAM1_, _GZMK_) or dim (_FCGR3A_, _GZMB_) [66]. B cells: naive (_MS4A1_, _IGHD_), memory (_CD27_, _IGHG1_), and plasma (_MZB1_, _SDC1_) [67][68].

| Cell Type | Gene Panel |
| :--- | :--- |
| Pan-T | _CD3D_, _CD3E_, _CD3G_, _IL7R_ [66] |
| Naive CD4 T | _SELL_, _LEF1_, _CCR7_, _TCF7_ [11] |
| Treg | _FOXP3_, _CTLA4_, _IL2RA_, _ENTPD1_ [11] |
| Tfh | _CXCL13_, _ICOS_, _BCL6_, _PDCD1_ [11] |
| Cytotoxic CD8 T | _GZMA_, _PRF1_, _GNLY_, _FGFBP2_ [58] |
| Exhausted CD8 T | _HAVCR2_, _LAG3_, _PDCD1_, _CTLA4_ [11] |
| MAIT | _TRAV1-2_, _SLC4A10_, _GZMK_, _KLRB1_ [58] |
| NK bright | _NCAM1_, _IL18_, _GZMK_, _SELL_ [66] |
| NK dim | _FCGR3A_, _PRF1_, _GZMB_, _GZMA_ [66] |
| Naive B | _MS4A1_, _IGHD_, _IGHM_, _TCL1A_ [67] |
| Memory B | _MS4A1_, _CD27_, _AIM2_, _IGHG1_ [69] |
| Plasmablast/Plasma | _IGKC_, _MZB1_, _SDC1_, _PRDM1_ [68] |

Myeloid cells (_CD74_, _CD14_) [16] include monocytes (classical _CD14_+, non-classical _CD16_+) A pan-cancer single-cell transcriptional atlas of tumor ...[12], _FABP4_+ lung-metastasis macrophages [16], and TAMs (C1QC+, SPP1+) [11]A pan-cancer single-cell transcriptional atlas of tumor .... DCs: cDC1 (_CLEC9A_), cDC2 (_CD1C_), pDC (_LILRA4_), and LAMP3+ A pan-cancer single-cell transcriptional atlas of tumor .... Osteoclasts: _CTSK_, _ACP5_ Transcriptional reprogramming during human osteoclast .... Notably, M1/M2 models are insufficient in vivo as subsets co-express signatures A pan-cancer single-cell transcriptional atlas of tumor ....

| Cell Type | Gene Panel |
| :--- | :--- |
| Pan-Myeloid | _CD74_, _CD14_, _FCGR3A_ [16] |
| Classical Monocyte | _CD14_, _FCN1_, _S100A8_, _S100A9_ A pan-cancer single-cell transcriptional atlas of tumor ... |
| Non-classical Monocyte | _FCGR3A_, _CX3CR1_, _LYN_ A pan-cancer single-cell transcriptional atlas of tumor ... |
| FABP4 Alveolar Macrophage | _FABP4_, _PPARG_, _MARCO_, _MRC1_ [16] |
| C1QC TAM | _C1QC_, _CD68_, _CD163_, _MRC1_ [11] |
| SPP1 TAM | _SPP1_, _CD68_, _CD163_ A pan-cancer single-cell transcriptional atlas of tumor ... |
| Inflammatory/IFN TAM | _CXCL8_, _ISG15_, _IFI6_ [11] |
| cDC1 | _CLEC9A_, _XCR1_, _CADM1_ A pan-cancer single-cell transcriptional atlas of tumor ... |
| cDC2 | _CD1C_, _CD1A_, _CD172A_ A pan-cancer single-cell transcriptional atlas of tumor ... |
| pDC | _LILRA4_, _TCF4_, _IRF7_, _LAMP5_ A pan-cancer single-cell transcriptional atlas of tumor ... |
| LAMP3 DC | _LAMP3_, _CCR7_, _FSCN1_ A pan-cancer single-cell transcriptional atlas of tumor ... |
| Mast | _KIT_, _TPSAB1_, _CPA3_, _TNF_ A pan-cancer single-cell transcriptional atlas of tumor ... |
| Osteoclast | _CTSK_, _ACP5_, _MMP9_, _DCSTAMP_, _CALCR_ Transcriptional reprogramming during human osteoclast ... |

**Precise identification of immune cell lineages and states, including specific TAM subsets and exhausted T cells, is critical for understanding tumor microenvironment dynamics and guiding targeted immunotherapies.**

## Quality Control and Implementation: An Auditable Seurat or Scanpy Workflow

1. **Sample-aware QC**: Observe high mitochondrial counts; mechanism is cell lysis; implication is noise; action is filtering by UMI/MT thresholds [5].
2. **Ambient RNA**: Observe background signal; mechanism is cell-free RNA leakage; implication is false marker detection; action is SoupX decontamination [40].
3. **Doublets**: Observe artifactual bridges; mechanism is co-encapsulation; implication is false cell states; action is Scrublet simulation [41].
4. **Lineage**: Observe markers like CD27 (B-cells) or COL1A1 (fibroblasts); mechanism is lineage transcription; implication is identity; action is labeling [41] [40].
5. **Mapping**: Observe query distance; mechanism is anchor transfer; implication is standardized labels; action is Azimuth mapping to the Human Lung Cell Atlas [109] [9].
6. **UCell**: Observe cluster separation; mechanism is rank-based scoring; implication is robust states; action is scoring MAIT (KLRB1) signatures [39].
7. **Malignancy**: Observe aberrations; mechanism is somatic CNV; implication is tumor distinction; action is Numbat or CopyKAT [3] [99].
8. **Validation**: Observe SATB2 expression; mechanism is osteoblastic differentiation; implication is osteosarcoma confirmation; action is pseudobulk check [47] [46].

| Mode | Mechanism | Implication | Action |
| :--- | :--- | :--- | :--- |
| Ambient RNA | UMI leakage | False markers | SoupX [40] |
| Doublets | Co-encapsulation | Artifactual states | Scrublet [41] |
| CNV Error | Low precision | False subclones | Numbat [3] |

**Integrating rank-based signature scoring with haplotype-aware CNV inference ensures robust identification of malignant lineages within complex tumor microenvironments.**

## Synthesis: A Hierarchical Decision Tree for This Right-Lung Biopsy

Malignant cells are identified by inferring copy number variations (CNVs) using Numbat or CopyKAT to distinguish tumor cells from diploid host cells [3] [97]. Host epithelium is annotated via markers like SFTPC (AT2) and AGER (AT1) using the Human Lung Cell Atlas [51] [6]. Rare cells like ionocytes (FOXI1+) require high-resolution mapping to avoid misclassification [91]. Mesenchymal cells (COL1A1+) require NPNT or PI16 to resolve fibroblast subsets [83] [82]. Immune cells are delineated by CD3D (T cells) and CD14 (Myeloid), with osteoclasts marked by CTSK/ACP5 [11] Transcriptional reprogramming during human osteoclast ....

| Category | Mechanism | Evidence | Overlap Risk | Validation |
| :--- | :--- | :--- | :--- | :--- |
| Malignant OS | Somatic CNV | Numbat [3] | Fibroblasts | SATB2 [44] |
| Epithelium | Lineage | SFTPC [6] | Ambient RNA | HLCA [51] |
| Mesenchymal | ECM | NPNT [9] | COL1A1 | PI16 [83] |
| Immune | Hematopoietic | CD3D [11] | Doublets | CTSK Transcriptional reprogramming during human osteoclast ... |

1. Remove ambient RNA with SoupX to ensure marker specificity [40].
2. Separate malignant cells from host cells using Numbat CNV inference [97].
3. Map host cells to the HLCA for lineage annotation [51].
4. Identify OS states (osteoblastic/chondroblastic) using RUNX2 and COL2A1 Single-cell RNA landscape of intratumoral heterogeneity ....
5. Profile immune states like exhausted T cells or SPP1+ macrophages [11].

**Integrating haplotype-aware CNV inference with lineage-specific markers is essential to distinguish malignant osteosarcoma from the host lung microenvironment.**

Research use only, not diagnosis.

## References

1. *Mitigating ambient RNA and doublets effects on single cell ...*. https://www.sciencedirect.com/science/article/abs/pii/S0304383525002599
2. *Hierarchical and automated cell-type annotation and ... - PMC*. https://pmc.ncbi.nlm.nih.gov/articles/PMC10713118/
3. *Benchmarking copy number aberrations inference tools using ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC11879432/
4. *How we tackle cell type annotation*. https://www.scdiscoveries.com/blog/featured/how-we-tackle-cell-type-annotation/
5. *13. Annotation*. https://www.sc-best-practices.org/cellular_structure/annotation.html
6. *A molecular cell atlas of the human lung from single cell RNA ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC7704697/
7. *Single-cell division tracing and transcriptomics reveal ...*. https://www.nature.com/articles/s41467-024-46469-4
8. *Single-cell RNA sequencing of mouse lower respiratory ...*. https://www.sciencedirect.com/science/article/pii/S2667290123000232
9. *Human Lung Cell Atlas*. https://hlca.sf.czbiohub.org/
10. *AT1/AT2 Cell*. https://research.cchmc.org/pbge/lunggens/tools/lung_at_glance.html?tab=cell&spe=Mouse&cell=T009
11. *A single-cell tumor immune atlas for precision oncology - PMC*. https://pmc.ncbi.nlm.nih.gov/articles/PMC8494216/
12. *Single-cell RNA-seq reveals new types of human blood ... - PMC*. https://pmc.ncbi.nlm.nih.gov/articles/PMC5775029/
13. *Assessing GPT-4 for cell type annotation in single-cell RNA ...*. https://www.nature.com/articles/s41592-024-02235-4
14. *Human Immune Cell Marker Guide*. https://www.cellsignal.com/pathways/immune-cell-markers-human?srsltid=AfmBOoqnM3mCFRPg6sPFZb3lkWlEoE-eeaiZknVvaQ1mbd0Tq6pjjcrl
15. *New Details of Tumor Microenvironment Revealed by Pan- ...*. https://www.insideprecisionmedicine.com/news-and-features/new-details-of-tumor-microenvironment-revealed-by-pan-cancer-t-cell-atlas/
16. *Single-cell RNA landscape of intratumoral heterogeneity ...*. https://www.nature.com/articles/s41467-020-20059-6
17. *Hypoxia increases the expression of stem cell markers ... - PMC*. https://pmc.ncbi.nlm.nih.gov/articles/PMC7856697/
18. *Mapping the Single-cell Differentiation Landscape of ... - PMC*. https://pmc.ncbi.nlm.nih.gov/articles/PMC10515803/
19. *Analysis of intercellular communication in the ...*. https://www.sciencedirect.com/science/article/pii/S221213742300026X
20. *Mapping the Single-Cell Differentiation Landscape of ...*. https://digitalcommons.library.tmc.edu/cgi/viewcontent.cgi?article=4132&context=uthgsbs_docs
21. *Single-Cell RNA Sequencing Reveals the Critical Role of ...*. https://pubmed.ncbi.nlm.nih.gov/40735296/
22. *Single-cell RNA sequencing reveals the communications ...*. https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2024.1445555/full
23. *Single-cell RNA sequencing reveals the communications ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC11422128/
24. *Single cell RNA analysis of murine osteosarcoma uncovers ...*. https://pubmed.ncbi.nlm.nih.gov/41877584/
25. *Targeting tumor‑associated macrophages in osteosarcoma*. https://www.sciencedirect.com/science/article/pii/S1043661826002094
26. *Single-cell RNA datasets and bulk RNA datasets analysis ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC9939514/
27. *Osteosarcoma immune microenvironment: cellular struggle ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC12174160/
28. *Integrated analysis of single-cell and bulk RNA-sequencing*. https://www.jcancer.org/v16p1873.htm
29. *Integrated Single-Cell Atlas of Endothelial Cells of the ...*. https://www.ahajournals.org/doi/10.1161/CIRCULATIONAHA.120.052318
30. *Integrated Single-Cell Atlas of Endothelial Cells of the Human ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC8300155/
31. *Single-cell analysis reveals prognostic fibroblast ... - PMC - NIH*. https://pmc.ncbi.nlm.nih.gov/articles/PMC9889778/
32. *A Guide to Fibroblast Markers*. https://www.biocompare.com/Editorial-Articles/616968-A-Guide-to-Fibroblast-Markers/
33. *Human Lung Cell Atlas 1.0*. https://chanzuckerberg.com/science/programs-resources/cell-science/seednetworks/human-lung-cell-atlas-1-0/
34. *Pulmonary tumor with osteosarcomatous and ... - PMC*. https://pmc.ncbi.nlm.nih.gov/articles/PMC12306883/
35. *Osteosarcoma*. https://www.pathologyoutlines.com/topic/boneosteosarcomageneral.html
36. *Serum Osteopontin as a Potential Marker for Metastasis ... - PMC*. https://pmc.ncbi.nlm.nih.gov/articles/PMC11181102/
37. *Bone, metaphysis: Osteosarcoma, Belgian Malinois, canine.*. https://www.askjpc.org/vspo/show_page.php?id=cUluNDFtS215VUFVWis1bDJ3bFI5UT09
38. *Understanding Your Lung Pathology Report*. https://www.cancer.org/cancer/diagnosis-staging/tests/pathology-reports/lung-pathology.html
39. *UCell: Robust and scalable single-cell gene signature scoring*. https://pmc.ncbi.nlm.nih.gov/articles/PMC8271111/
40. *SoupX removes ambient RNA contamination from droplet ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC7763177/
41. *Scrublet: Computational Identification of Cell Doublets in ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC6625319/
42. *Review of SoupX removes ambient RNA contamination from ...*. https://publons.com/wos-op/review/6584651/
43. *Benchmarking Computational Doublet-Detection Methods ...*. https://www.sciencedirect.com/science/article/pii/S2405471220304592
44. *The utility of SATB2 immunohistochemical expression in ...*. https://pubmed.ncbi.nlm.nih.gov/27465835/
45. *Special AT-rich sequence-binding protein 2 (SATB2) in ... - PMC*. https://pmc.ncbi.nlm.nih.gov/articles/PMC9510043/
46. *The use of alkaline phosphatase and runx2 to distinguish ...*. https://journals.sagepub.com/doi/10.1177/03009858221083035
47. *Study Shows SATB2 as Effective Immunohistochemical ...*. https://www.stagebio.com/content-library/study-shows-satb2-as-effective-immunohistochemical-marker-for-accurate-diagnosis-of-osa-in-canines
48. *Immunohistochemistry Panel for Osteosarcoma*. https://www.droracle.ai/articles/1123383/what-immunohistochemistry-panel-is-recommended-for-the-workup-of
49. *An integrated cell atlas of the lung in health and disease*. https://pubmed.ncbi.nlm.nih.gov/37291214/
50. *An integrated cell atlas of the lung in health and disease*. https://www.nature.com/articles/s41591-023-02327-2
51. *An integrated cell atlas of the lung in health and disease - PMC*. https://pmc.ncbi.nlm.nih.gov/articles/PMC10287567/
52. *Lung Cell Atlas Created*. https://www.insideprecisionmedicine.com/news-and-features/lung-cell-atlas-created/
53. *A pan-cancer single-cell transcriptional atlas of tumor ...*. https://www.sciencedirect.com/science/article/pii/S0092867421000106
54. *Pan-cancer single-cell transcriptomic analysis reveals ...*. https://www.sciencedirect.com/science/article/pii/S200103702500457X
55. *SPP1+ macrophages in colorectal cancer: Markers of ... - PMC*. https://pmc.ncbi.nlm.nih.gov/articles/PMC11907465/
56. *A Guide to Myeloid Cell Markers*. https://www.biocompare.com/Editorial-Articles/612866-A-Guide-to-Myeloid-Cell-Markers/
57. *Macrophage diversity in cancer revisited in the era of ...*. https://www.cell.com/trends/immunology/fulltext/S1471-4906(22)00094-1
58. *Pan-cancer T Cell Atlas Links a Cellular Stress Response ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC11421770/
59. *CD8+ T cell states in human cancer - PMC - NIH*. https://pmc.ncbi.nlm.nih.gov/articles/PMC7115982/
60. *A pan-cancer single-cell panorama of human natural killer ...*. https://www.cell.com/cell/fulltext/S0092-8674(23)00849-8
61. *New Pan-Cancer T-Cell Atlas Reveals New Ways for ...*. https://www.cd-genomics.com/case-pan-cancer-t-cell-atlas.html
62. *Decoding osteosarcoma from heterogeneity to precision therapy*. https://pmc.ncbi.nlm.nih.gov/articles/PMC12858688/
63. *Single‐Cell RNA Sequencing Reveals the Critical Role of ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC12301935/
64. *Single-cell RNA-seq reveals intratumoral heterogeneity in ...*. https://pure.johnshopkins.edu/en/publications/single-cell-rna-seq-reveals-intratumoral-heterogeneity-in-osteosa
65. *Tumor microenvironment in osteosarcoma: From cellular ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC12211857/
66. *A pan-cancer single-cell panorama of human natural killer cells: Cell*. https://www.cell.com/cell/fulltext/S0092-8674%2823%2900849-8
67. *An Integrated Multi-omic Single-Cell Atlas of Human B ... - PMC*. https://pmc.ncbi.nlm.nih.gov/articles/PMC7369630/
68. *Paired single-B-cell transcriptomics and receptor sequencing ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC10910691/
69. *A pan-cancer single-cell RNA-seq atlas of intratumoral B ...*. https://www.sciencedirect.com/science/article/pii/S1535610824003593
70. *B cells and Plasma cells*. https://apps.allenimmunology.org/aifi/resources/imm-health-atlas/cell-type-descriptions/b-cells-and-plasma-cells/
71. *Single-cell Atlas of common variable immunodeficiency ...*. https://cellxgene.cziscience.com/collections/bf325905-5e8e-42e3-933d-9a9053e9af80
72. *Biology of lung macrophages in health and disease - PMC - NIH*. https://pmc.ncbi.nlm.nih.gov/articles/PMC9533769/
73. *Single-cell resolution characterization of myeloid-derived ...*. https://www.nature.com/articles/s41467-024-49916-4
74. *Single-Cell Transcriptomics of Human and Mouse Lung ...*. https://csb.mgh.harvard.edu/highlights/single-cell-transcriptomics
75. *Alveolar macrophages gene expression markers*. https://panglaodb.se/markers.html?cell_type='Alveolar%20macrophages'
76. *Transcriptional reprogramming during human osteoclast ...*. https://www.nature.com/articles/s41413-023-00312-6
77. *Single-cell RNA sequencing revealed PPARG promoted ...*. https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2024.1506225/full
78. *Interspecies Single‐Cell RNA‐Seq Analysis Reveals ... - PMC*. https://pmc.ncbi.nlm.nih.gov/articles/PMC9289986/
79. *Effects of Melandrium firmum Rohrbach on RANKL ...*. https://www.spandidos-publications.com/10.3892/mmr.2021.12248
80. *Single-cell RNA sequencing analysis dissected the osteo ...*. https://www.sciencedirect.com/science/article/abs/pii/S156757692200786X
81. *Single Cell Transcriptomic Analysis Reveals Organ Specific ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC9199463/
82. *Categorization of lung mesenchymal cells in development and ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC8188567/
83. *Collagen-producing lung cell atlas identifies multiple ...*. https://www.nature.com/articles/s41467-020-15647-5
84. *Single-cell transcriptomic analysis of human pleura reveals ...*. https://publications.ersnet.org/content/erj/63/1/2300143
85. *Pericytes gene expression markers*. https://panglaodb.se/markers.html?cell_type=%27Pericytes%27
86. *Transcriptional profiling of single tumour cells from pleural ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC9271990/
87. *Metachronous Osteosarcoma, A Differential Diagnosis to be ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC10030169/
88. *TTF-1 is a highly sensitive but not fully specific marker for ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC11564378/
89. *Lung cancer biomarkers for IHC research*. https://www.abcam.com/en-us/technical-resources/research-areas/marker-guides/lung-cancer-markers
90. *Primary pulmonary osteosarcoma - Chapman - 2001 - Cancer*. https://acsjournals.onlinelibrary.wiley.com/doi/full/10.1002/1097-0142%2820010215%2991%3A4%3C779%3A%3AAID-CNCR1064%3E3.0.CO%3B2-J
91. *Single cell profiling of human airway identifies tuft-ionocyte ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC12137820/
92. *Single cell profiling of human airway identifies tuft-ionocyte ...*. https://www.nature.com/articles/s41467-025-60441-w
93. *Cellular and molecular architecture of submucosal glands in ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC8794846/
94. *Single cell profiling of human airway identifies tuft-ionocyte ...*. https://www.researchgate.net/publication/392405923_Single_cell_profiling_of_human_airway_identifies_tuft-ionocyte_progenitor_cells_displaying_cytokine-dependent_differentiation_bias_in_vitro
95. *GSE240168 - GEO Accession viewer - NIH*. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE240168
96. *A Comparison of Tools That Identify Tumor Cells by Inferring ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC11351975/
97. *Haplotype-aware analysis of somatic copy number variations ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC10289836/
98. *Delineating copy number and clonal substructure in human ...*. https://pmc.ncbi.nlm.nih.gov/articles/PMC8122019/
99. *numbat: Haplotype-Aware CNV Analysis from scRNA-Seq*. https://cran.r-project.org/web/packages/numbat/numbat.pdf
100. *Identification of malignant cells in single ...*. https://www.nature.com/articles/s42003-025-08695-4
101. *Adjusted Neighborhood Scoring to improve gene signature ...*. https://www.biorxiv.org/content/10.1101/2023.09.20.558114v2.full-text
102. *UCell and pyUCell: single-cell gene signature scoring for R ...*. https://academic.oup.com/bioinformatics/article/42/2/btag055/8471616
103. *UCell: Rank-based signature enrichment analysis for ...*. https://bioconductor.posit.co/packages/3.22/bioc/manuals/UCell/man/UCell.pdf
104. *Gene signature scoring with UCell*. https://bioconductor.statistik.tu-dortmund.de/packages/3.19/bioc/vignettes/UCell/inst/doc/UCell_vignette_basic.html
105. *Mapping single-cell data to reference atlases by transfer ...*. https://www.nature.com/articles/s41587-021-01001-7
106. *An overview of computational methods in single-cell ... - PMC*. https://pmc.ncbi.nlm.nih.gov/articles/PMC12065632/
107. *Azimuth*. https://azimuth.hubmapconsortium.org/
108. *Single-cell reference mapping to construct and extend ...*. https://brainscapes.nl/news/single-cell-reference-mapping-to-construct-and-extend-cell-type-hierarchies/
109. *Azimuth annotation*. https://satijalab.github.io/azimuth/articles/run_azimuth_tutorial.html
