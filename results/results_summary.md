# GSE5281 Alzheimer’s Classification Results

## Cohort and Evaluation
- Samples: 161; genes after probe aggregation: 21755.
- Labels: 74 normal and 87 Alzheimer’s samples.
- Group-aware holdout: 127 training and 34 test samples; subject-proxy overlap: 0.
- ANOVA-selected features: 500; five-gene panel: MIR612, TUBB4B, SARS, TUBB, PSMB3.
- Imputation, feature ranking, and scaling were fitted using training data only.

## Held-Out Test Metrics
| Model | Accuracy | Sensitivity | Specificity | Precision | F1 | ROC-AUC | FN | FP |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Logistic Regression (500 genes) | 0.941 | 0.941 | 0.941 | 0.941 | 0.941 | 0.972 | 1 | 1 |
| Random Forest (500 genes) | 0.824 | 0.765 | 0.882 | 0.867 | 0.812 | 0.938 | 4 | 2 |
| RBF SVM (500 genes) | 0.912 | 0.882 | 0.941 | 0.938 | 0.909 | 0.952 | 2 | 1 |
| Logistic Regression (5 genes) | 0.765 | 0.765 | 0.765 | 0.765 | 0.765 | 0.872 | 4 | 4 |

The highest observed test ROC-AUC was for **Logistic Regression (500 genes)**. These are educational cohort results, not a clinical diagnostic test.
The subject identifiers are proxies derived from repeated sample-name suffixes because the supplied metadata has no formal patient-ID field.