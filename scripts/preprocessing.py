"""Prepare GSE5281 GEO data for the Alzheimer classification lab."""

import gzip
from pathlib import Path

import numpy as np
import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
METADATA_PATH = DATA_DIR / "GSE5281_sample_characteristics.csv"
MATRIX_PATH = DATA_DIR / "GSE5281_series_matrix.txt.gz"
PLATFORM_PATH = DATA_DIR / "GPL570.annot.gz"
OUTPUT_PATH = DATA_DIR / "alzheimer_expression_processed.csv"


def find_gzip_table_lines(path: Path, start_marker: str, end_marker: str) -> tuple[int, int]:
	start_line = None
	end_line = None
	with gzip.open(path, "rt", encoding="latin1") as stream:
		for line_number, line in enumerate(stream):
			if line.startswith(start_marker):
				start_line = line_number
			elif end_marker and line.startswith(end_marker):
				end_line = line_number
				break
	if start_line is None or (end_marker and end_line is None):
		raise ValueError(f"Could not find table markers in {path.name}.")
	return start_line, end_line if end_line is not None else start_line


def clean_text(values: pd.Series) -> pd.Series:
	return values.astype(str).str.replace("\xa0", " ", regex=False).str.strip()


def main() -> None:
	metadata = pd.read_csv(METADATA_PATH, encoding="latin1")
	metadata["sample_id"] = clean_text(metadata["GEO Accession:"])
	sample_number = metadata["Sample Name:"].astype(str).str.extract(r"(\d+)\s*$")[0]
	metadata["disease_state"] = clean_text(metadata["Disease State:"])
	metadata["region"] = clean_text(metadata["Organ Region:"])

	disease_lower = metadata["disease_state"].str.lower()
	metadata["target"] = np.select(
		[disease_lower.str.startswith("normal"), disease_lower.str.startswith("alzheimer")],
		[0, 1],
		default=-1,
	)
	if (metadata["target"] < 0).any():
		labels = metadata.loc[metadata["target"] < 0, "disease_state"].unique().tolist()
		raise ValueError(f"Unexpected disease labels in metadata: {labels}")
	if sample_number.isna().any():
		raise ValueError("Could not derive a subject-number proxy from every sample name.")
	metadata["subject_id"] = np.where(metadata["target"] == 1, "affected_", "control_") + sample_number

	age_text = clean_text(metadata["Age:"])
	age_values = pd.to_numeric(age_text.str.extract(r"([0-9]+(?:\.[0-9]+)?)")[0], errors="coerce")
	metadata["age_years"] = age_values.where(~age_text.str.lower().str.contains("day"), age_values / 365.25)

	matrix_start, matrix_end = find_gzip_table_lines(
		MATRIX_PATH, "!series_matrix_table_begin", "!series_matrix_table_end"
	)
	probe_expression = pd.read_csv(
		MATRIX_PATH,
		sep="\t",
		compression="gzip",
		skiprows=matrix_start + 1,
		nrows=matrix_end - matrix_start - 2,
		index_col=0,
	)
	probe_expression.index = probe_expression.index.astype(str)
	probe_expression = probe_expression.apply(pd.to_numeric, errors="coerce").T
	probe_expression.index.name = "sample_id"

	platform_header, _ = find_gzip_table_lines(PLATFORM_PATH, "ID\t", "")
	platform = pd.read_csv(
		PLATFORM_PATH,
		sep="\t",
		compression="gzip",
		skiprows=platform_header,
		usecols=["ID", "Gene symbol"],
		dtype=str,
	)
	platform["Gene symbol"] = platform["Gene symbol"].fillna("").str.split("///").str[0].str.strip()
	platform = platform.loc[platform["Gene symbol"].ne("") & platform["Gene symbol"].ne("---")]
	probe_to_gene = platform.drop_duplicates("ID").set_index("ID")["Gene symbol"]

	mapped_symbols = pd.Series(probe_expression.columns, index=probe_expression.columns).map(probe_to_gene)
	keep_probes = mapped_symbols.notna()
	gene_expression = probe_expression.loc[:, keep_probes].copy()
	gene_expression.columns = mapped_symbols.loc[keep_probes].to_numpy()
	gene_expression = gene_expression.T.groupby(level=0, sort=True).mean().T
	gene_expression = np.log2(gene_expression.clip(lower=0) + 1)

	metadata_columns = metadata[["sample_id", "subject_id", "target", "disease_state", "region", "age_years"]]
	processed = metadata_columns.merge(
		gene_expression.reset_index(), on="sample_id", how="inner", validate="one_to_one"
	)
	if len(processed) != len(metadata):
		missing = sorted(set(metadata["sample_id"]) - set(processed["sample_id"]))
		raise ValueError(f"Expression data missing for {len(missing)} metadata samples: {missing[:5]}")

	OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
	processed.to_csv(OUTPUT_PATH, index=False)
	print(f"Prepared {len(processed)} samples and {gene_expression.shape[1]} gene features.")
	print("Target counts (0=normal, 1=Alzheimer's):")
	print(processed["target"].value_counts().sort_index().to_string())
	print(f"Saved processed data to: {OUTPUT_PATH}")


if __name__ == "__main__":
	main()
