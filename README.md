# Alzheimer's Disease Classification

## Project Overview

This project focuses on Alzheimer's Disease Classification using gene expression data and machine learning techniques.

The objective is to process gene expression data, build classification models, evaluate their performance, and identify important genes associated with Alzheimer's Disease.

## Dataset

The project includes the following data files:

- `GSE5281_sample_characteristics.csv`
- `GSE5281_series_matrix.txt.gz`
- `GPL570.annot.gz`
- `alzheimer_expression_processed.csv`

## Project Structure

```text
Alzheimers/
│
├── data/
│   ├── GPL570.annot.gz
│   ├── GSE5281_sample_characteristics.csv
│   ├── GSE5281_series_matrix.txt.gz
│   └── alzheimer_expression_processed.csv
│
├── results/
│   ├── logistic_regression_confusion_matrix.png
│   ├── model_benchmark.csv
│   ├── model_roc_curves.png
│   ├── random_forest_confusion_matrix.png
│   ├── random_forest_top_genes.png
│   ├── results_summary.md
│   ├── svm_confusion_matrix.png
│   ├── test_set_predictions.csv
│   ├── top_gene_rankings.csv
│   └── training_gene_rankings.csv
│
└── scripts/
    └── preprocessing.py
```

## Machine Learning Models

The project includes evaluation outputs for:

1. Logistic Regression
2. Random Forest
3. Support Vector Machine (SVM)

## Project Workflow

1. Load the gene expression dataset.
2. Preprocess the data.
3. Prepare the data for machine learning.
4. Train classification models.
5. Evaluate model performance.
6. Generate confusion matrices and ROC curves.
7. Identify and rank important genes.
8. Save predictions and model evaluation results.

## Results and Evaluation

The project includes:

- Model benchmarking results
- Confusion matrices
- ROC curves
- Test set predictions
- Top gene rankings
- Random Forest feature importance visualizations

Refer to the `results/` directory for detailed evaluation outputs.

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Machine Learning
- Bioinformatics

## Repository

GitHub: https://github.com/Gundrathi-Prathyusha/Alzheimers-Disease-Classification

---

**Note:** This project is intended for educational and research purposes. Its classification outputs should not be used as a substitute for clinical diagnosis.
