from pathlib import Path
import pandas as pd
import re


# ============================================================
# CONFIG
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "DODA_Notebook_Output_Inventory.xlsx"
OUTPUT_FILE = ROOT / "DODA_Master_Results.xlsx"


# ============================================================
# HELPERS
# ============================================================

def clean_name(value):
    """Convert a value into a safe, readable string."""
    value = str(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def flatten_columns(df):
    """Flatten MultiIndex columns."""
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            " | ".join(
                str(x).strip()
                for x in col
                if str(x).strip() and str(x).strip().lower() != "nan"
            )
            for col in df.columns
        ]

    df.columns = [clean_name(c) for c in df.columns]

    return df


def classify_table(df, sheet_name):
    """
    Classify an extracted notebook table into one of the
    master-result categories.
    """

    text = " ".join(
        [str(c).lower() for c in df.columns]
        + [sheet_name.lower()]
    )

    # --------------------------------------------------------
    # Predictive performance
    # --------------------------------------------------------

    predictive_terms = [
        "accuracy",
        "precision",
        "recall",
        "f1",
        "roc",
        "auc",
        "model",
        "classifier",
    ]

    predictive_score = sum(term in text for term in predictive_terms)

    # --------------------------------------------------------
    # Stability
    # --------------------------------------------------------

    stability_terms = [
        "jaccard",
        "kuncheva",
        "stability",
        "selection stability",
    ]

    stability_score = sum(term in text for term in stability_terms)

    # --------------------------------------------------------
    # Agreement
    # --------------------------------------------------------

    agreement_terms = [
        "agreement",
        "similarity",
        "overlap",
        "feature set agreement",
    ]

    agreement_score = sum(term in text for term in agreement_terms)

    # --------------------------------------------------------
    # Feature selection
    # --------------------------------------------------------

    feature_terms = [
        "feature",
        "rank",
        "selected",
        "selection",
        "importance",
    ]

    feature_score = sum(term in text for term in feature_terms)

    # --------------------------------------------------------
    # Clinical feature analysis
    # --------------------------------------------------------

    clinical_terms = [
        "clinical",
        "weight",
        "doda score",
        "math score",
        "final score",
    ]

    clinical_score = sum(term in text for term in clinical_terms)

    # --------------------------------------------------------
    # Decide
    # --------------------------------------------------------

    scores = {
        "Predictive_Results": predictive_score,
        "Stability": stability_score,
        "Agreement": agreement_score,
        "Clinical_Feature_Analysis": clinical_score,
        "Feature_Selection": feature_score,
    }

    category = max(scores, key=scores.get)

    # Avoid classifying very weak matches
    if scores[category] == 0:
        category = "Unclassified"

    return category


# ============================================================
# READ INVENTORY
# ============================================================

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Could not find:\n{INPUT_FILE}"
    )

print(f"Reading: {INPUT_FILE}")

xls = pd.ExcelFile(INPUT_FILE)

print(f"\nFound {len(xls.sheet_names)} sheets:")
for sheet in xls.sheet_names:
    print(" -", sheet)


# ============================================================
# LOAD + CLASSIFY
# ============================================================

classified_tables = []

for sheet in xls.sheet_names:

    # Inventory itself is metadata, not an experimental table
    if sheet.lower() == "inventory":
        continue

    try:
        df = pd.read_excel(INPUT_FILE, sheet_name=sheet)

        df = flatten_columns(df)

        category = classify_table(df, sheet)

        classified_tables.append({
            "Sheet": sheet,
            "Category": category,
            "Rows": len(df),
            "Columns": len(df.columns),
            "Column_Names": " | ".join(df.columns),
        })

        print(
            f"\n[{category}] {sheet}"
            f"  ({len(df)} rows × {len(df.columns)} cols)"
        )

    except Exception as e:

        print(
            f"\nERROR reading {sheet}: {e}"
        )

        classified_tables.append({
            "Sheet": sheet,
            "Category": "ERROR",
            "Rows": None,
            "Columns": None,
            "Column_Names": str(e),
        })


classification_df = pd.DataFrame(classified_tables)


# ============================================================
# BUILD MASTER WORKBOOK
# ============================================================

with pd.ExcelWriter(
    OUTPUT_FILE,
    engine="openpyxl"
) as writer:

    # --------------------------------------------------------
    # 1. Classification
    # --------------------------------------------------------

    classification_df.to_excel(
        writer,
        sheet_name="Classification",
        index=False
    )

    # --------------------------------------------------------
    # 2. Experiment Setup
    # --------------------------------------------------------

    experiment_setup = pd.DataFrame(
        columns=[
            "Disease",
            "Dataset",
            "Selector",
            "DODA",
            "Fusion",
            "Top_K",
            "Model",
            "Source_Sheet",
            "Status",
        ]
    )

    experiment_setup.to_excel(
        writer,
        sheet_name="Experiment_Setup",
        index=False
    )

    # --------------------------------------------------------
    # 3. Predictive Results
    # --------------------------------------------------------

    predictive_results = pd.DataFrame(
        columns=[
            "Disease",
            "Selector",
            "DODA",
            "Fusion",
            "Top_K",
            "Model",
            "Accuracy",
            "Precision",
            "Recall",
            "F1",
            "ROC_AUC",
            "Source_Sheet",
        ]
    )

    predictive_results.to_excel(
        writer,
        sheet_name="Predictive_Results",
        index=False
    )

    # --------------------------------------------------------
    # 4. Feature Selection
    # --------------------------------------------------------

    feature_selection = pd.DataFrame(
        columns=[
            "Disease",
            "Selector",
            "DODA",
            "Fusion",
            "Top_K",
            "Rank",
            "Feature",
            "Source_Sheet",
        ]
    )

    feature_selection.to_excel(
        writer,
        sheet_name="Feature_Selection",
        index=False
    )

    # --------------------------------------------------------
    # 5. Stability
    # --------------------------------------------------------

    stability = pd.DataFrame(
        columns=[
            "Disease",
            "Selector",
            "DODA",
            "Fusion",
            "Top_K",
            "Metric",
            "Score",
            "Source_Sheet",
        ]
    )

    stability.to_excel(
        writer,
        sheet_name="Stability",
        index=False
    )

    # --------------------------------------------------------
    # 6. Agreement
    # --------------------------------------------------------

    agreement = pd.DataFrame(
        columns=[
            "Disease",
            "Selector",
            "Fusion",
            "Top_K",
            "Agreement_Metric",
            "Score",
            "Source_Sheet",
        ]
    )

    agreement.to_excel(
        writer,
        sheet_name="Agreement",
        index=False
    )

    # --------------------------------------------------------
    # 7. Clinical Feature Analysis
    # --------------------------------------------------------

    clinical = pd.DataFrame(
        columns=[
            "Disease",
            "Selector",
            "Top_K",
            "Feature",
            "Statistical_Score",
            "Clinical_Weight",
            "DODA_Score",
            "Rank",
            "Source_Sheet",
        ]
    )

    clinical.to_excel(
        writer,
        sheet_name="Clinical_Feature_Analysis",
        index=False
    )

    # --------------------------------------------------------
    # 8. Raw Table Index
    # --------------------------------------------------------

    classification_df.to_excel(
        writer,
        sheet_name="Raw_Table_Index",
        index=False
    )


print("\n" + "=" * 60)
print("STEP 2 COMPLETE")
print("=" * 60)

print(f"\nCreated:")
print(OUTPUT_FILE)

print("\nTable classification:")
print(
    classification_df[
        ["Sheet", "Category", "Rows", "Columns"]
    ].to_string(index=False)
)