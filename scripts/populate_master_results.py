# ============================================================
# DODA MASTER RESULTS COLLECTOR
# ============================================================
# Purpose:
#   Extract ALL saved HTML tables from executed notebooks and
#   organize them into research-result categories.
#
# Output:
#   DODA_Master_Results.xlsx
#
# Sheets:
#   01_Prediction_Metrics
#   02_Feature_Rankings
#   03_Rank_Changes
#   04_Stability_Tests
#   05_Fusion_Results
#   06_Other_Tests
#   07_Table_Inventory
#
# IMPORTANT:
#   - No averaging
#   - No filtering of "important" results
#   - No numeric cleaning
#   - No result interpretation
#   - Original extracted values are preserved
# ============================================================


import json
import re
from io import StringIO
from pathlib import Path

import pandas as pd


# ============================================================
# 1. PROJECT ROOT
# ============================================================

def find_project_root():
    """
    Find project root by looking for the notebooks folder.
    Works both from a .py file and from a Jupyter notebook.
    """

    # If running as a Python script
    if "__file__" in globals():
        possible_root = Path(__file__).resolve().parent.parent

        if (possible_root / "notebooks").exists():
            return possible_root

    # If running inside Jupyter / VS Code notebook
    current = Path.cwd()

    for path in [current] + list(current.parents):
        if (path / "notebooks").exists():
            return path

    # Fallback
    return current


PROJECT_ROOT = find_project_root()

print("Project root:")
print(PROJECT_ROOT)


# ============================================================
# 2. NOTEBOOK DIRECTORIES
# ============================================================

NOTEBOOK_DIRS = [
    PROJECT_ROOT / "notebooks" / "anandha" / "Diabetes",
    PROJECT_ROOT / "notebooks" / "anandha" / "heartdisease",
    PROJECT_ROOT / "notebooks" / "angel" / "breast_cancer",
    PROJECT_ROOT / "notebooks" / "angel" / "kidney_disease",
]


# ============================================================
# 3. OUTPUT FILE
# ============================================================

OUTPUT_FILE = PROJECT_ROOT / "DODA_Master_Results.xlsx"


# ============================================================
# 4. DATASET DETECTION
# ============================================================

def get_dataset_name(path):
    """
    Identify dataset from notebook path/name.
    """

    text = str(path).lower()

    if "diabetes" in text:
        return "Diabetes"

    if "heartdisease" in text or "heart_disease" in text:
        return "Heart Disease"

    if "breast_cancer" in text or "breastcancer" in text:
        return "Breast Cancer"

    if "kidney_disease" in text or "kidney" in text or "ckd" in text:
        return "CKD"

    return "Unknown"


# ============================================================
# 5. METHOD DETECTION
# ============================================================

def standardize_method(method):
    """
    Standardize method names.
    """

    if not method:
        return ""

    method = str(method).strip().lower()

    mapping = {
        "anova": "ANOVA",
        "lasso": "LASSO",
        "mrmr": "mRMR",
        "boruta": "Boruta",
        "doda": "DODA",
    }

    return mapping.get(method, method.upper())


def infer_method_from_notebook(notebook_name):
    """
    Infer feature-selection method from notebook filename.
    """

    name = notebook_name.lower()

    if "anova" in name:
        return "ANOVA"

    if "lasso" in name:
        return "LASSO"

    if "mrmr" in name:
        return "mRMR"

    if "boruta" in name:
        return "Boruta"

    if "doda" in name:
        return "DODA"

    return ""


# ============================================================
# 6. FLATTEN MULTI-INDEX COLUMNS
# ============================================================

def flatten_columns(df):
    """
    Convert MultiIndex columns into simple column names.
    """

    df = df.copy()

    if isinstance(df.columns, pd.MultiIndex):

        new_columns = []

        for col in df.columns:
            parts = []

            for item in col:
                item = str(item).strip()

                if item and item.lower() != "nan":
                    parts.append(item)

            new_columns.append("_".join(parts))

        df.columns = new_columns

    else:
        df.columns = [
            str(col).strip()
            for col in df.columns
        ]

    return df


# ============================================================
# 7. MAKE COLUMN NAMES UNIQUE
# ============================================================

def make_unique_columns(df):
    """
    Prevent duplicate column names after HTML extraction.
    """

    df = df.copy()

    seen = {}
    new_columns = []

    for col in df.columns:

        col = str(col).strip()

        if col not in seen:
            seen[col] = 0
            new_columns.append(col)

        else:
            seen[col] += 1
            new_columns.append(
                f"{col}_{seen[col]}"
            )

    df.columns = new_columns

    return df


# ============================================================
# 8. CLASSIFY RESULT TYPE
# ============================================================

def classify_result(table_text, columns):
    """
    Classify a table into one of the master-result categories.

    This classification is ONLY for organization.
    It does NOT determine whether a result is important.
    """

    text = (
        str(table_text) + " " +
        " ".join(map(str, columns))
    ).lower()

    # --------------------------------------------------------
    # Rank changes
    # --------------------------------------------------------

    rank_change_terms = [
        "rank change",
        "rank_change",
        "rankchange",
        "final rank",
        "math rank",
        "clinical rank",
        "ranking change",
        "change in rank",
    ]

    if any(term in text for term in rank_change_terms):
        return "Rank Changes"


    # --------------------------------------------------------
    # Stability tests
    # --------------------------------------------------------

    stability_terms = [
        "jaccard",
        "kuncheva",
        "stability",
        "selection frequency",
        "selection_frequency",
        "overlap",
        "consistency",
    ]

    if any(term in text for term in stability_terms):
        return "Stability Tests"


    # --------------------------------------------------------
    # Fusion
    # --------------------------------------------------------

    fusion_terms = [
        "fusion",
        "rankfusion",
        "rank fusion",
        "hadamard",
        "fused score",
        "fusion score",
        "math score",
        "mathematical score",
        "clinical weight",
        "clinical score",
    ]

    if any(term in text for term in fusion_terms):
        return "Fusion Results"


    # --------------------------------------------------------
    # Prediction metrics
    # --------------------------------------------------------

    prediction_terms = [
        "accuracy",
        "precision",
        "recall",
        "f1",
        "f1-score",
        "f1 score",
        "roc-auc",
        "roc_auc",
        "auc",
        "specificity",
        "sensitivity",
        "balanced accuracy",
        "log loss",
    ]

    if any(term in text for term in prediction_terms):
        return "Prediction Metrics"


    # --------------------------------------------------------
    # Feature rankings / selection
    # --------------------------------------------------------

    feature_terms = [
        "feature",
        "features",
        "selected",
        "selection",
        "rank",
        "ranking",
        "top-k",
        "top k",
        "importance",
        "coefficient",
        "boruta",
        "mrmr",
        "anova",
        "lasso",
    ]

    if any(term in text for term in feature_terms):
        return "Feature Rankings"


    # --------------------------------------------------------
    # Everything else
    # --------------------------------------------------------

    return "Other Tests"


# ============================================================
# 9. EXTRACT TABLES FROM ONE NOTEBOOK
# ============================================================

def extract_tables_from_notebook(notebook_path):

    results = []

    try:

        with open(
            notebook_path,
            "r",
            encoding="utf-8"
        ) as f:

            notebook = json.load(f)

    except Exception as e:

        print(
            f"Could not read notebook: "
            f"{notebook_path.name}"
        )

        print("Error:", e)

        return results


    dataset = get_dataset_name(notebook_path)

    method = infer_method_from_notebook(
        notebook_path.name
    )


    # --------------------------------------------------------
    # Loop through notebook cells
    # --------------------------------------------------------

    for cell_number, cell in enumerate(
        notebook.get("cells", [])
    ):

        if cell.get("cell_type") != "code":
            continue


        outputs = cell.get("outputs", [])


        # ----------------------------------------------------
        # Loop through outputs
        # ----------------------------------------------------

        for output_number, output in enumerate(outputs):

            data = output.get("data", {})

            html_data = data.get("text/html")


            if not html_data:
                continue


            # ------------------------------------------------
            # HTML may be list of strings
            # ------------------------------------------------

            if isinstance(html_data, list):

                html_text = "".join(html_data)

            else:

                html_text = str(html_data)


            # ------------------------------------------------
            # Read every HTML table
            # ------------------------------------------------

            try:

                tables = pd.read_html(
                    StringIO(html_text)
                )

            except Exception:

                continue


            # ------------------------------------------------
            # Store every table
            # ------------------------------------------------

            for table_number, df in enumerate(tables):

                df = flatten_columns(df)

                df = make_unique_columns(df)

                result_type = classify_result(
                    html_text,
                    df.columns
                )


                table_id = (
                    f"T{len(results) + 1:04d}"
                )


                results.append({
                    "Table_ID": table_id,
                    "Dataset": dataset,
                    "Notebook": notebook_path.name,
                    "Method": method,
                    "Result_Type": result_type,
                    "Cell": cell_number,
                    "Output": output_number,
                    "Table": table_number,
                    "DataFrame": df,
                })


    return results


# ============================================================
# 10. FIND NOTEBOOKS
# ============================================================

notebook_files = []

for directory in NOTEBOOK_DIRS:

    if not directory.exists():

        print(
            f"WARNING: directory not found:\n"
            f"{directory}"
        )

        continue


    files = sorted(
        directory.glob("*.ipynb")
    )

    notebook_files.extend(files)


print()
print(
    f"Found {len(notebook_files)} notebooks."
)
print()


# ============================================================
# 11. EXTRACT EVERYTHING
# ============================================================

all_tables = []

for notebook_path in notebook_files:

    print(
        f"Processing: "
        f"{notebook_path.name}"
    )

    tables = extract_tables_from_notebook(
        notebook_path
    )

    print(
        f"  Tables found: {len(tables)}"
    )

    all_tables.extend(tables)


print()
print(
    f"TOTAL TABLES EXTRACTED: "
    f"{len(all_tables)}"
)


# ============================================================
# 12. PREPARE CATEGORY DATA
# ============================================================

categories = {
    "Prediction Metrics": [],
    "Feature Rankings": [],
    "Rank Changes": [],
    "Stability Tests": [],
    "Fusion Results": [],
    "Other Tests": [],
}


# ============================================================
# 13. BUILD MASTER ROWS
# ============================================================

inventory_rows = []

# These are reserved for our master metadata
MASTER_COLUMNS = [
    "Table_ID",
    "Dataset",
    "Notebook",
    "Method",
    "Result_Type",
    "Cell",
    "Output",
    "Table",
]


for item in all_tables:

    table_id = item["Table_ID"]

    dataset = item["Dataset"]

    notebook = item["Notebook"]

    method = item["Method"]

    result_type = item["Result_Type"]

    cell = item["Cell"]

    output = item["Output"]

    table_number = item["Table"]

    df = item["DataFrame"].copy()


    # --------------------------------------------------------
    # INVENTORY
    # --------------------------------------------------------

    inventory_rows.append({

        "Table_ID": table_id,

        "Dataset": dataset,

        "Notebook": notebook,

        "Method": method,

        "Result_Type": result_type,

        "Cell": cell,

        "Output": output,

        "Table": table_number,

        "Rows": len(df),

        "Columns": len(df.columns),

        "Column_Names":
            " | ".join(
                map(str, df.columns)
            ),
    })


    # --------------------------------------------------------
    # HANDLE COLUMN NAME CONFLICTS
    #
    # If the original notebook table already has columns such
    # as "Method", "Dataset", "Rank", etc., preserve them.
    #
    # Only columns reserved for master metadata are renamed.
    # --------------------------------------------------------

    rename_map = {}

    for col in df.columns:

        col_str = str(col).strip()

        if col_str in MASTER_COLUMNS:

            rename_map[col] = f"Source_{col_str}"


    if rename_map:

        df = df.rename(
            columns=rename_map
        )


    # --------------------------------------------------------
    # ADD MASTER METADATA
    # --------------------------------------------------------

    df.insert(
        0,
        "Table_ID",
        table_id
    )

    df.insert(
        1,
        "Dataset",
        dataset
    )

    df.insert(
        2,
        "Notebook",
        notebook
    )

    df.insert(
        3,
        "Method",
        method
    )

    df.insert(
        4,
        "Result_Type",
        result_type
    )

    df.insert(
        5,
        "Cell",
        cell
    )

    df.insert(
        6,
        "Output",
        output
    )

    df.insert(
        7,
        "Table",
        table_number
    )


    # --------------------------------------------------------
    # ADD TO CATEGORY
    # --------------------------------------------------------

    categories[result_type].append(
        df
    )

# ============================================================
# 14. COMBINE TABLES WITHIN EACH CATEGORY
# ============================================================

combined_categories = {}

for category, dataframes in categories.items():

    if dataframes:

        combined_categories[category] = pd.concat(
            dataframes,
            ignore_index=True,
            sort=False
        )

    else:

        combined_categories[category] = pd.DataFrame()


# ============================================================
# 15. TABLE INVENTORY
# ============================================================

inventory_df = pd.DataFrame(
    inventory_rows
)


# ============================================================
# 16. WRITE MASTER EXCEL FILE
# ============================================================

with pd.ExcelWriter(
    OUTPUT_FILE,
    engine="openpyxl"
) as writer:

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    combined_categories[
        "Prediction Metrics"
    ].to_excel(
        writer,
        sheet_name="01_Prediction_Metrics",
        index=False
    )


    # --------------------------------------------------------
    # Feature rankings
    # --------------------------------------------------------

    combined_categories[
        "Feature Rankings"
    ].to_excel(
        writer,
        sheet_name="02_Feature_Rankings",
        index=False
    )


    # --------------------------------------------------------
    # Rank changes
    # --------------------------------------------------------

    combined_categories[
        "Rank Changes"
    ].to_excel(
        writer,
        sheet_name="03_Rank_Changes",
        index=False
    )


    # --------------------------------------------------------
    # Stability
    # --------------------------------------------------------

    combined_categories[
        "Stability Tests"
    ].to_excel(
        writer,
        sheet_name="04_Stability_Tests",
        index=False
    )


    # --------------------------------------------------------
    # Fusion
    # --------------------------------------------------------

    combined_categories[
        "Fusion Results"
    ].to_excel(
        writer,
        sheet_name="05_Fusion_Results",
        index=False
    )


    # --------------------------------------------------------
    # Other tests
    # --------------------------------------------------------

    combined_categories[
        "Other Tests"
    ].to_excel(
        writer,
        sheet_name="06_Other_Tests",
        index=False
    )


    # --------------------------------------------------------
    # Inventory
    # --------------------------------------------------------

    inventory_df.to_excel(
        writer,
        sheet_name="07_Table_Inventory",
        index=False
    )


# ============================================================
# 17. SUMMARY
# ============================================================

print()
print("=" * 60)
print("MASTER RESULTS CREATED")
print("=" * 60)

print()
print("Output:")
print(OUTPUT_FILE)

print()
print("Tables by category:")

for category, df in combined_categories.items():

    print(
        f"  {category:<25} "
        f"{len(df):>6} rows"
    )

print()
print(
    f"Total source tables: "
    f"{len(all_tables)}"
)

print()
print("Done.")