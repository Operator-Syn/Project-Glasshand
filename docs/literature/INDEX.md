# Literature index

63 PDFs across five clusters, plus one book that has no open copy. Each row gives the file, the
citation with a resolvable DOI, the licence printed on the copy held, and the paper section it
supports.

The PDFs themselves are git-ignored ([`README.md`](README.md)); this index and
[`manifest.tsv`](manifest.tsv) are the tracked record, and `uv run python scripts/fetch_literature.py`
rebuilds the files.

Every filename carries the first author printed on page one of the PDF, not the author a search
snippet attributed it to. Four files were renamed after that check: Pandora is Nushi, not Chung;
the robust-feature failure paper is Singla; GUI-PRIMITIVES is Jahin; the desktop IVG paper is
Ettifouri.

**Licence note.** Most arXiv files carry arXiv's non-exclusive distribution licence, which permits
arXiv to distribute the work — it does not grant third parties a redistribution right. Storing them
in a private repository for reading and citation is the exception recorded in
[`../references/README.md`](../references/README.md). Do not publish this repository with the PDFs
in place.

Every file was checked after download: `%PDF` magic bytes present, `pdftotext` extracts a text
layer, and the first page carries the title recorded here.

## 01-gui-grounding — the benchmark family and grounding models

| File | Citation | Licence | Supports |
|---|---|---|---|
| `li2025_screenspot-pro.pdf` | Li, K. et al. (2025). *ScreenSpot-Pro: GUI Grounding for Professional High-Resolution Computer Use.* https://doi.org/10.48550/arXiv.2504.07981 | CC BY 4.0 | §2 benchmark; §3 data provenance; the 18.9% best-model figure |
| `cheng2024_seeclick.pdf` | Cheng, K. et al. (2024). *SeeClick: Harnessing GUI Grounding for Advanced Visual GUI Agents.* ACL 2024. https://doi.org/10.18653/v1/2024.acl-long.505 | arXiv non-exclusive | §2 origin of ScreenSpot and of the text/icon taxonomy |
| `wu2024_os-atlas.pdf` | Wu, Z. et al. (2024). *OS-ATLAS: A Foundation Action Model for Generalist GUI Agents.* ICLR 2025. https://doi.org/10.48550/arXiv.2410.23218 | CC BY 4.0 | §2 ScreenSpot-v2 and the label-noise argument |
| `gou2024_uground.pdf` | Gou, B. et al. (2024). *Navigating the Digital World as Humans Do: Universal Visual Grounding for GUI Agents.* ICLR 2025. https://doi.org/10.48550/arXiv.2410.05243 | arXiv non-exclusive | §2 the pure-vision coordinate paradigm this baseline contrasts with |
| `lin2024_showui.pdf` | Lin, K. Q. et al. (2024). *ShowUI: One Vision-Language-Action Model for GUI Visual Agent.* CVPR 2025. https://doi.org/10.48550/arXiv.2411.17465 | arXiv non-exclusive | §2 high-resolution token-reduction strategies |
| `you2024_ferret-ui.pdf` | You, K. et al. (2024). *Ferret-UI: Grounded Mobile UI Understanding with Multimodal LLMs.* ECCV 2024. https://doi.org/10.1007/978-3-031-73039-9_14 | arXiv non-exclusive | §2 mobile-side ancestor of box-level UI grounding |
| `wu2025_gui-actor.pdf` | Wu, Q. et al. (2025). *GUI-Actor: Coordinate-Free Visual Grounding for GUI Agents.* NeurIPS 2025. https://doi.org/10.48550/arXiv.2506.03143 | CC BY 4.0 | §2 evidence the coordinate-generation formulation is contested |
| `ettifouri2025_ivg-desktop-grounding.pdf` | Ettifouri, E. H. et al. (2025). *Visual Grounding Methods for Efficient Interaction with Desktop Graphical User Interfaces.* https://doi.org/10.48550/arXiv.2407.01558 | arXiv non-exclusive | §2 the closest published OCR-anchored desktop baseline, and its measured shortfall against a VLM |
| `jandial2026_gui-grounders-ui-understanding.pdf` | Jandial, S. et al. (2026). *Do GUI Grounders Truly Understand UI Elements?* Findings of EACL 2026. https://aclanthology.org/2026.findings-eacl.144.pdf | ACL Anthology | §1 and §7 the gap: benchmarks skew to web and mobile and neglect Windows desktop |
| `lu2024_omniparser.pdf` | Lu, Y. et al. (2024). *OmniParser for Pure Vision Based GUI Agent.* https://doi.org/10.48550/arXiv.2408.00203 | arXiv non-exclusive | §2 pixel-only screen parsing as the alternative to text anchoring |
| `xie2025_scaling-computer-use-grounding.pdf` | Xie, T. et al. (2025). *Scaling Computer-Use Grounding via User Interface Decomposition and Synthesis.* https://doi.org/10.48550/arXiv.2505.13227 | arXiv non-exclusive | §2 separating text matching from visual reasoning as grounding capabilities |
| `wu2021_screen-parsing.pdf` | Wu, J. et al. (2021). *Screen Parsing: Towards Reverse Engineering of UI Models from Screenshots.* UIST 2021. https://doi.org/10.1145/3472749.3474763 | ACM copyright; arXiv copy held | §2 the HCI lineage of recovering UI structure from pixels |
| `deka2017_rico-dataset.pdf` | Deka, B. et al. (2017). *Rico: A Mobile App Dataset for Building Data-Driven Design Applications.* UIST 2017. https://doi.org/10.1145/3126594.3126651 | ACM copyright notice on the PDF | §2 the dataset lineage that supplied privileged view hierarchies |
| `bunian2021_vins-ui-search.pdf` | Bunian, S. et al. (2021). *VINS: Visual Search for Mobile User Interface Design.* CHI 2021. https://doi.org/10.1145/3411764.3445762 | not stated on the copy | §2 hierarchy-derived labels are weak: mAP 48.08 against 74.15 on human-annotated boxes |
| `li2021_screen2vec.pdf` | Li, T. J.-J. et al. (2021). *Screen2Vec: Semantic Embedding of GUI Screens and GUI Components.* CHI 2021. https://doi.org/10.1145/3411764.3445049 | not stated on the copy | §2 the TextOnly precursor of a text-anchored representation |

## 02-ocr-and-text — engines, detectors and the small-text problem

| File | Citation | Licence | Supports |
|---|---|---|---|
| `zhou2017_east.pdf` | Zhou, X. et al. (2017). *EAST: An Efficient and Accurate Scene Text Detector.* CVPR 2017. https://doi.org/10.1109/CVPR.2017.283 | arXiv non-exclusive | §2 detection stage; §4.1 whole-image rescaling as the first place small text is lost |
| `baek2019_craft.pdf` | Baek, Y. et al. (2019). *Character Region Awareness for Text Detection.* CVPR 2019. https://doi.org/10.1109/CVPR.2019.00959 | arXiv non-exclusive | §4.1 glyph-level versus word-level localisation |
| `du2020_pp-ocr.pdf` | Du, Y. et al. (2020). *PP-OCR: A Practical Ultra Lightweight OCR System.* https://doi.org/10.48550/arXiv.2009.09941 | arXiv non-exclusive | §4.1 the citable description of the engine RapidOCR redeploys |
| `long2020_scene-text-survey.pdf` | Long, S. et al. (2020). *Scene Text Detection and Recognition: The Deep Learning Era.* IJCV. https://doi.org/10.1007/s11263-020-01369-0 | arXiv non-exclusive | §2 field taxonomy; §4.1 small, blurred and occluded text as a standing difficulty |
| `zeng2023_mixnet.pdf` | Zeng, Y.-X. et al. (2023). *MixNet: Toward Accurate Detection of Challenging Scene Text in the Wild.* https://doi.org/10.48550/arXiv.2308.12817 | CC BY-NC-ND 4.0 | §4.2 why neighbouring small labels merge or vanish |
| `zhang2021_screen-recognition.pdf` | Zhang, X. et al. (2021). *Screen Recognition: Creating Accessibility Metadata for Mobile Applications from Pixels.* CHI 2021. https://doi.org/10.1145/3411764.3445186 | CC BY 4.0 | §4.1 precedent for pixel-only UI parsing; the icon-without-text gap |
| `smith2007_tesseract-ocr.pdf` | Smith, R. (2007). *An Overview of the Tesseract OCR Engine.* ICDAR 2007. https://doi.org/10.1109/ICDAR.2007.4376991 | IEEE copyright; no licence stated on the copy | §4.2 why PSM 3 and PSM 11 diverge on sparse screenshots |
| `boubehziz2025_ocr-resolution-impact.pdf` | Boubehziz, T. et al. (2025). *Assessing the Impact of Image Resolution on OCR Transcription Accuracy.* LangArc-2025 @ JCDL. https://doi.org/10.12794/langarc2543322 | not stated on the copy | §4.1 measured CER collapse for a Tesseract pipeline under downsampling |
| `wang2020_textzoom-super-resolution.pdf` | Wang, W. et al. (2020). *Scene Text Image Super-Resolution in the Wild.* ECCV 2020. https://doi.org/10.1007/978-3-030-58607-2_38 | arXiv non-exclusive | §4.1 paired low- and high-resolution captures: 35.7% vs 81.2% recognition |
| `akyon2022_sahi-slicing.pdf` | Akyon, F. C. et al. (2022). *Slicing Aided Hyper Inference and Fine-tuning for Small Object Detection.* ICIP 2022. https://doi.org/10.1109/ICIP46576.2022.9897990 | arXiv non-exclusive | §4.1 whole-image inference at a fixed input resolution is where small targets are lost |
| `becker2026_sliced-inference-resolution.pdf` | Becker, S. et al. (2026). *When Does Sliced Inference Pay Off? Resolution, Tiling and Dense Fusion for Small Object Detection.* arXiv:2611.12657. No DOI. | arXiv non-exclusive | §4.1 the ~6-pixel floor in the network input, and the honest caveat that resolution beats tiling |
| `meethal2023_cascaded-zoom-in.pdf` | Meethal, A. et al. (2023). *Cascaded Zoom-in Detector for High Resolution Aerial Images.* CVPRW 2023. https://doi.org/10.1109/CVPRW59228.2023.00198 | CC BY-NC-SA 4.0 | §4.1 rescaling corrupts the features of small objects |

## 03-computer-use-agents — the task-level frame this paper does not compete on

| File | Citation | Licence | Supports |
|---|---|---|---|
| `xie2024_osworld.pdf` | Xie, T. et al. (2024). *OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments.* NeurIPS 2024. https://doi.org/10.48550/arXiv.2404.07972 | CC BY 4.0 | §1 motivation; §2 end-to-end benchmark context (task success, not grounding) |
| `bonatti2024_windows-agent-arena.pdf` | Bonatti, R. et al. (2024). *Windows Agent Arena: Evaluating Multi-Modal OS Agents at Scale.* https://doi.org/10.48550/arXiv.2409.08264 | arXiv non-exclusive | §1 the Windows-specific end-to-end frame |
| `zheng2024_seeact.pdf` | Zheng, B. et al. (2024). *GPT-4V(ision) is a Generalist Web Agent, if Grounded.* ICML 2024. https://doi.org/10.48550/arXiv.2401.01614 | arXiv non-exclusive | §1 grounding as an isolable stage; §2 grounding versus task success |
| `hong2024_cogagent.pdf` | Hong, W. et al. (2024). *CogAgent: A Visual Language Model for GUI Agents.* CVPR 2024. https://doi.org/10.48550/arXiv.2312.08914 | arXiv non-exclusive | §2 screenshot-only VLM grounders |
| `qin2025_ui-tars.pdf` | Qin, Y. et al. (2025). *UI-TARS: Pioneering Automated GUI Interaction with Native Agents.* https://doi.org/10.48550/arXiv.2501.12326 | arXiv non-exclusive | §1 the grounding-versus-task-success gap |
| `zhang2024_llm-gui-agents-survey.pdf` | Zhang, C. et al. (2024). *Large Language Model-Brained GUI Agents: A Survey.* TMLR 2025. https://doi.org/10.48550/arXiv.2411.18279 | arXiv non-exclusive | §2 field map; §7 boundary of a grounding-only study |
| `nguyen2024_gui-agents-survey.pdf` | Nguyen, D. et al. (2024). *GUI Agents: A Survey.* Findings of ACL 2025. https://doi.org/10.18653/v1/2025.findings-acl.1158 | CC BY-NC-ND 4.0 | §2 perception-versus-planning decomposition |

## 04-interpretable-failure — why a tree, and the baseline it must beat

| File | Citation | Licence | Supports |
|---|---|---|---|
| — *(no open copy)* | Breiman, L. et al. (1984). *Classification and Regression Trees.* Wadsworth. https://doi.org/10.1201/9781315139470 | Proprietary (Taylor & Francis) | §4.4 origin of CART; cite the book, not a file |
| `loh2011_classification-regression-trees.pdf` | Loh, W.-Y. (2011). *Classification and regression trees.* WIREs DMKD 1(1):14-23. https://doi.org/10.1002/widm.8 | Wiley VOR, author-hosted | §4.4 induction, depth and leaf-size control |
| `rudin2019_stop-explaining-black-box.pdf` | Rudin, C. (2019). *Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead.* Nature Machine Intelligence 1(5):206-215. https://doi.org/10.1038/s42256-019-0048-x | CC BY-SA 4.0 (arXiv) | §4.4 and §5.2 why an inherently interpretable model |
| `perlich2003_tree-vs-logistic.pdf` | Perlich, C. et al. (2003). *Tree Induction vs. Logistic Regression: A Learning-Curve Analysis.* JMLR 4:211-255. No DOI issued. | JMLR open access | §5.2 answering "why a tree and not a line", including the caveat |
| `geifman2017_selective-classification.pdf` | Geifman, Y. & El-Yaniv, R. (2017). *Selective Classification for Deep Neural Networks.* NeurIPS 2017. https://doi.org/10.48550/arXiv.1705.08500 | arXiv non-exclusive | §5.2 the score-threshold baseline by its formal name |
| `ribeiro2020_beyond-accuracy.pdf` | Ribeiro, M. T. et al. (2020). *Beyond Accuracy: Behavioral Testing of NLP Models with CheckList.* ACL 2020. https://doi.org/10.18653/v1/2020.acl-main.442 | arXiv non-exclusive | §4.4 classifying failures by condition, not just error rate |
| `liao2020_questioning-the-ai.pdf` | Liao, Q. V. et al. (2020). *Questioning the AI: Informing Design Practices for Explainable AI User Experiences.* CHI 2020. https://doi.org/10.1145/3313831.3376590 | arXiv non-exclusive | §5.2 what the reader of an explanation actually needs |
| `grinsztajn2022_trees-tabular.pdf` | Grinsztajn, L. et al. (2022). *Why do tree-based models still outperform deep learning on tabular data?* https://doi.org/10.48550/arXiv.2207.08815 | arXiv non-exclusive | §4.4 tree-based learners on small heterogeneous tabular inputs |
| `nushi2018_pandora-system-failure.pdf` | Nushi, B., Kamar, E., & Horvitz, E. (2018). *Towards Accountable AI: Hybrid Human-Machine Analyses for Characterizing System Failure.* https://doi.org/10.48550/arXiv.1809.07424 | arXiv non-exclusive | §4.4 the closest published precedent: interpretable decision trees that summarise conditions of failure, chosen for interpretability |
| `singla2021_failures-robust-features.pdf` | Singla, S. et al. (2021). *Understanding Failures of Deep Networks via Robust Feature Extraction.* https://doi.org/10.48550/arXiv.2012.01750 | arXiv non-exclusive | §4.4 depth-limited trees for failure prediction, and a metric for whether a tree explains rather than classifies |
| `chen2004_failure-diagnosis-decision-trees.pdf` | Chen, M. et al. (2004). *Failure Diagnosis Using Decision Trees.* ICAC 2004. No DOI verified; author-hosted PDF. | IEEE copyright; author-hosted copy | §4.4 the systems-side ancestor of tree-based failure diagnosis |
| `holte1993_simple-rules-1r.pdf` | Holte, R. C. (1993). *Very Simple Classification Rules Perform Well on Most Commonly Used Datasets.* Machine Learning 11:63-91. https://doi.org/10.1023/A:1022631118932 | not stated on the copy | §5.2 the published template for benchmarking a shallow threshold rule against a learned model |

## 05-evaluation-methods — metric choice, validity and leakage

| File | Citation | Licence | Supports |
|---|---|---|---|
| `reinke2024_metric-pitfalls.pdf` | Reinke, A. et al. (2024). *Understanding metric-related pitfalls in image analysis validation.* Nature Methods 21:182-194. https://doi.org/10.1038/s41592-023-02150-0 | CC BY 4.0 | §4.3 why near-miss distances accompany strict point-in-box |
| `tao2025_logit-sharpness.pdf` | Tao, X. et al. (2025). *Understanding GUI Agent Localization Biases through Logit Sharpness.* https://doi.org/10.48550/arXiv.2506.15425 | arXiv non-exclusive | §4.3 disaggregating hits into near-miss and wrong-target |
| `hutchinson2022_evaluation-gaps.pdf` | Hutchinson, B. et al. (2022). *Evaluation Gaps in Machine Learning Practice.* FAccT 2022. https://doi.org/10.1145/3531146.3533233 | CC BY 4.0 | §7 construct validity of a benchmark score |
| `gebru2021_datasheets.pdf` | Gebru, T. et al. (2021). *Datasheets for Datasets.* CACM 64(12):86-92. https://doi.org/10.1145/3458723 | ACM copyright (CACM); arXiv licence on the stored copy | §3 documenting release-derived annotations |
| `kapoor2023_leakage-reproducibility.pdf` | Kapoor, S. & Narayanan, A. (2023). *Leakage and the reproducibility crisis in machine-learning-based science.* Patterns 4(9):100804. https://doi.org/10.1016/j.patter.2023.100804 | CC BY 4.0 | §4.4 grouped folds and the duplicate-pair treatment |
| `roberts2017_cross-validation.pdf` | Roberts, D. R. et al. (2017). *Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure.* Ecography 40(8):913-929. https://doi.org/10.1111/ecog.02881 | Wiley VOR, author-hosted | §4.4 why folds group by application |
| `yuan2026_right-click-wrong-box.pdf` | Yuan, X. et al. (2026). *Right Click, Wrong Box: Grading GUI Grounding by What a Click Does.* https://doi.org/10.48550/arXiv.2610.36831 | arXiv non-exclusive | §4.3 point-in-box under-counts correct clicks and biases results one-sidedly |
| `jahin2026_gui-primitives.pdf` | Jahin, M. A. et al. (2026). *GUI-PRIMITIVES: Diagnosing Spatial Reasoning Failures in Vision-Language GUI Grounding.* EMNLP 2026. https://aclanthology.org/2026.emnlp-main.2620.pdf | ACL Anthology | §4.3 strict point-in-box beside a loose metric; failures are localisation, not comprehension |
| `zhang2026_conclick-error-types.pdf` | Zhang, R. et al. (2026). *ConClick: Element-wise Contrastive Learning Improves GUI Grounding.* https://doi.org/10.48550/arXiv.2610.13268 | arXiv non-exclusive | §4.3 click accuracy hides four separable error types |
| `kumar2026_uncertainty-computer-use.pdf` | Kumar, D. et al. (2026). *Uncertainty Quantification for Computer-Use Agents: A Benchmark across Vision-Language Models and GUI Grounding Datasets.* https://doi.org/10.48550/arXiv.2606.25760 | arXiv non-exclusive | §5.2 graded miss severity, and the limits of confidence as a signal |
| `northcutt2021_label-errors.pdf` | Northcutt, C. G. et al. (2021). *Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks.* NeurIPS 2021 Datasets and Benchmarks. No DOI. | proceedings PDF; no separate licence stated | §7 benchmark labels carry a measurable error rate and can reorder model rankings |
| `reiss2020_conll-label-errors.pdf` | Reiss, F. et al. (2020). *Identifying Incorrect Labels in the CoNLL-2003 Corpus.* CoNLL 2020. https://doi.org/10.18653/v1/2020.conll-1.16 | CC BY 4.0 | §7 the honest counterpoint: ~7.5% test-fold label errors did not reorder results |
| `artstein2008_inter-coder-agreement.pdf` | Artstein, R. & Poesio, M. (2008). *Survey Article: Inter-Coder Agreement for Computational Linguistics.* Computational Linguistics 34(4):555-596. https://doi.org/10.1162/coli.07-034-r2 | ACL copyright; no open licence stated | §7 kappa methodology, and why this study cannot claim inter-annotator agreement |
| `saito2015_precision-recall-imbalance.pdf` | Saito, T. & Rehmsmeier, M. (2015). *The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets.* PLOS ONE 10(3):e0118432. https://doi.org/10.1371/journal.pone.0118432 | CC BY 4.0 | §5.2 why accuracy and ROC-AUC mislead at an 81% base rate, and the 0.19 PR baseline |
| `brodersen2010_balanced-accuracy.pdf` | Brodersen, K. H. et al. (2010). *The Balanced Accuracy and Its Posterior Distribution.* ICPR 2010. https://doi.org/10.1109/ICPR.2010.764 | not stated on the copy | §5.2 balanced accuracy defined, and the constant-majority failure mode |
| `niculescu2005_probability-calibration.pdf` | Niculescu-Mizil, A. & Caruana, R. (2005). *Predicting Good Probabilities With Supervised Learning.* ICML 2005. https://doi.org/10.1145/1102351.1102430 | not stated on the copy | §5.2 single decision trees are among the weakest probability estimators — the warrant for refusing the word calibrated |
| `brier1950_probability-verification.pdf` | Brier, G. W. (1950). *Verification of Forecasts Expressed in Terms of Probability.* Monthly Weather Review 78(1):1-3. https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2 | not stated on the copy | §5.2 the score the paper states it never computed |
| `silvafilho2023_calibration-survey.pdf` | Silva Filho, T. et al. (2023). *Classifier calibration: a survey on how to assess and improve predicted class probabilities.* Machine Learning 112(9):3211-3260. https://doi.org/10.1007/s10994-023-06336-7 | CC BY 4.0 | §5.2 the protocol that would be required to earn the word calibrated |
