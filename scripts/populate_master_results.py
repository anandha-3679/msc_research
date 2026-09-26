from pathlib import Path
import pandas as pd
import re


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "DODA_Notebook_Output_Inventory.xlsx"
OUTPUT_FILE = ROOT / "DODA_Master_Results.xlsx"


# ============================================================
# EXPERIMENTAL NOTEBOOKS ONLY
# ============================================================

VALID_NOTEBOOKS = [
    "diabetes_annova",
    "diabetes_lasso",
    "diabetes_mrmr",
    "diabetes_rf",
    "diabetes_boruta",

    "heartdisease_annova",
    "heartdisease_lasso",
    "heartdisease_mrmr",
    "heartdisease_rf",
    "heartdisease_boruta",
]

# ============================================================
# CANONICAL PREDICTIVE SOURCE SHEETS
# ============================================================
# Each sheet contains the combined 24-row predictive table:
#   12 Baseline rows + 12 DODA rows.
#
# The separate 12-row predictive tables are excluded here
# because they duplicate these results.

CANONICAL_PREDICTIVE_SHEETS = {
    "9_diabetes_annova",
    "28_diabetes_boruta",
    "79_diabetes_lasso",
    "96_diabetes_mrmr",
    "116_diabetes_rf",

    "142_heartdisease_annova",
    "161_heartdisease_boruta",
    "210_heartdisease_lasso",
    "228_heartdisease_mrmr",
    "249_heartdisease_rf",
}


# ============================================================
# HELPERS
# ============================================================

def clean(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def flatten_columns(df):

    if isinstance(df.columns, pd.MultiIndex):

        df.columns = [
            " | ".join(
                str(x).strip()
                for x in col
                if str(x).strip()
                and str(x).strip().lower() != "nan"
            )
            for col in df.columns
        ]

    df.columns = [str(c).strip() for c in df.columns]

    return df


def get_notebook(source):

    source = str(source)

    for notebook in VALID_NOTEBOOKS:

        if notebook in source.lower():
            return notebook

    return ""


def get_disease(notebook):

    if notebook.startswith("diabetes"):
        return "Diabetes"

    if notebook.startswith("heartdisease"):
        return "Heart Disease"

    return ""


def get_selector(notebook):

    if notebook.endswith("_annova"):
        return "ANOVA"

    if notebook.endswith("_lasso"):
        return "LASSO"

    if notebook.endswith("_mrmr"):
        return "mRMR"

    if notebook.endswith("_rf"):
        return "Random Forest"

    if notebook.endswith("_boruta"):
        return "Boruta"

    return ""


def get_fusion(notebook):

    if notebook.startswith("diabetes"):
        return "Hadamard Fusion"

    if notebook.startswith("heartdisease"):
        return "Rank Fusion"

    return ""

def normalize_predictive_method(method):
    """
    Normalize notebook-specific method names.

    Anything containing 'DODA' -> DODA
    Everything else -> Baseline
    """

    method = clean(method)

    if "DODA" in method:
        return "DODA"

    return "Baseline"


def get_top_k(df):

    for col in ["Top-K", "Top_K"]:

        if col in df.columns:

            values = pd.to_numeric(
                df[col],
                errors="coerce"
            ).dropna()

            return values.tolist()

    return []


def remove_metadata_columns(df):

    metadata = [
        "_Notebook",
        "_Cell",
        "_Output",
        "_Table",
        "Unnamed: 0"
    ]

    return df.drop(
        columns=[
            c for c in metadata
            if c in df.columns
        ],
        errors="ignore"
    )


# ============================================================
# TABLE IDENTIFICATION
# ============================================================

def identify_table(df):

    cols = set(df.columns)

    # --------------------------------------------------------
    # Predictive main table
    # --------------------------------------------------------

    if {
        "Method",
        "Top-K",
        "Model",
        "Selected Features",
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "ROC-AUC"
    }.issubset(cols):

        return "Predictive_Results"


    # --------------------------------------------------------
    # Repeated predictive results
    # --------------------------------------------------------

    if {
        "Run",
        "Method",
        "Top_K",
        "Model",
        "Accuracy",
        "Precision",
        "Recall",
        "F1",
        "ROC_AUC",
        "Selected_Features"
    }.issubset(cols):

        return "Predictive_Repeated"


    # --------------------------------------------------------
    # Predictive mean/std
    # --------------------------------------------------------

    if {
        "Method",
        "Top_K",
        "Model",
        "Accuracy_Mean",
        "Accuracy_STD"
    }.issubset(cols):

        return "Predictive_Summary"

    # --------------------------------------------------------
    # Baseline selector scores
    # --------------------------------------------------------

    if {
        "Feature",
        "ANOVA Score"
    }.issubset(cols):

        return "Baseline_Scores"


    # --------------------------------------------------------
    # Raw math score
    # --------------------------------------------------------

    if {
        "Feature",
        "Raw Math Score",
        "Normalized Math Score"
    }.issubset(cols):

        return "Clinical_Raw_Math"


    # --------------------------------------------------------
    # Clinical weight
    # --------------------------------------------------------

    if {
        "Feature",
        "Clinical Weight"
    }.issubset(cols):

        return "Clinical_Weights"


    # --------------------------------------------------------
    # DODA final score
    # Supports both fusion implementations
    # --------------------------------------------------------

    if {
        "Feature",
        "Final DODA Score"
    }.issubset(cols):

        return "Clinical_Final_Score"

    if {
        "Feature",
        "Final Rank Fusion Score"
    }.issubset(cols):

        return "Clinical_Final_Score"

    # --------------------------------------------------------
    # DODA rank comparison
    # --------------------------------------------------------

    if {
        "Feature",
        "Math Rank",
        "Normalized Math Score",
        "Clinical Rank",
        "Clinical Weight",
        "Final Rank",
        "Final Score",
        "Rank Change"
    }.issubset(cols):

        return "Clinical_Ranking"


    # --------------------------------------------------------
    # Feature set by run
    # --------------------------------------------------------

    if {
        "Run",
        "Method",
        "Top_K",
        "Feature_Set"
    }.issubset(cols):

        return "Feature_Set"


    # --------------------------------------------------------
    # Feature frequency
    # --------------------------------------------------------

    if {
        "Method",
        "Top_K",
        "Feature",
        "Selected_Count",
        "Total_Runs",
        "Selection_Frequency_Percentage"
    }.issubset(cols):

        return "Feature_Frequency"


    # --------------------------------------------------------
    # Feature count
    # --------------------------------------------------------

    if {
        "Method",
        "Top_K",
        "Feature_Count"
    }.issubset(cols):

        return "Feature_Count"


    # --------------------------------------------------------
    # Jaccard pairwise
    # --------------------------------------------------------

    if {
        "Method",
        "Top_K",
        "Run_A",
        "Run_B",
        "Intersection",
        "Union",
        "Jaccard_Similarity"
    }.issubset(cols):

        return "Jaccard_Pairwise"


    # --------------------------------------------------------
    # Jaccard summary
    # --------------------------------------------------------

    if {
        "Method",
        "Top_K",
        "Mean_Jaccard"
    }.issubset(cols):

        return "Jaccard_Summary"


    # --------------------------------------------------------
    # Kuncheva pairwise
    # --------------------------------------------------------

    if {
        "Method",
        "Top_K",
        "Run_A",
        "Run_B",
        "Intersection",
        "Kuncheva_Index"
    }.issubset(cols):

        return "Kuncheva_Pairwise"


    # --------------------------------------------------------
    # Kuncheva summary
    # --------------------------------------------------------

    if {
        "Method",
        "Top_K",
        "Mean_Kuncheva"
    }.issubset(cols):

        return "Kuncheva_Summary"


    # --------------------------------------------------------
    # DODA agreement
    # --------------------------------------------------------

    agreement_markers = [
        "ANOVA_Features",
        "LASSO_Features",
        "mRMR_Features",
        "RF_Features",
        "Boruta_Features"
    ]

    if (
        "DODA_Features" in cols
        and any(x in cols for x in agreement_markers)
    ):

        return "Agreement_Pairwise"


    # --------------------------------------------------------
    # Aggregate agreement
    # --------------------------------------------------------

    if (
        "Top_K" in cols
        and (
            "Mean_Agreement" in cols
            or "Mean_Jaccard_Agreement" in cols
        )
    ):

        return "Agreement_Summary"


    return "Other"


# ============================================================
# MAIN
# ============================================================

print("=" * 70)
print("STEP 4 — BUILDING MASTER RESULTS")
print("=" * 70)


if not INPUT_FILE.exists():

    raise FileNotFoundError(
        f"Input file not found:\n{INPUT_FILE}"
    )


xls = pd.ExcelFile(INPUT_FILE)


# ============================================================
# STORAGE
# ============================================================

predictive_rows = []
predictive_repeated_rows = []
predictive_summary_rows = []

clinical_rows = []
baseline_score_rows = []

feature_set_rows = []
feature_frequency_rows = []
feature_count_rows = []

jaccard_pairwise_rows = []
jaccard_summary_rows = []

kuncheva_pairwise_rows = []
kuncheva_summary_rows = []

agreement_pairwise_rows = []
agreement_summary_rows = []

source_rows = []


# ============================================================
# PROCESS TABLES
# ============================================================

for sheet in xls.sheet_names:

    if sheet.lower() == "inventory":
        continue

    notebook = get_notebook(sheet)

    if not notebook:
        continue

    # IMPORTANT:
    # Ignore EDA completely because no EDA notebook is in
    # VALID_NOTEBOOKS.

    df = pd.read_excel(
        INPUT_FILE,
        sheet_name=sheet
    )

    df = flatten_columns(df)

    table_type = identify_table(df)

    df = remove_metadata_columns(df)

    disease = get_disease(notebook)
    selector = get_selector(notebook)
    fusion = get_fusion(notebook)

    source_rows.append({
        "Source_Sheet": sheet,
        "Notebook": notebook,
        "Disease": disease,
        "Selector": selector,
        "Fusion": fusion,
        "Table_Type": table_type,
        "Rows": len(df),
        "Columns": len(df.columns),
        "Column_Names": " | ".join(df.columns)
    })


    # ========================================================
    # PREDICTIVE MAIN
    # ========================================================
    #
    # IMPORTANT:
    # Only canonical combined 24-row sheets are used.
    #
    # Each canonical sheet contains:
    #   12 Baseline rows
    #   12 DODA rows
    #
    # This prevents duplicate predictive results.
    #

    if (
        table_type == "Predictive_Results"
        and sheet in CANONICAL_PREDICTIVE_SHEETS
    ):

        for _, row in df.iterrows():

            predictive_rows.append({

                "Disease": disease,
                "Selector": selector,
                "Fusion": fusion,

                "Method":
                    normalize_predictive_method(
                        row["Method"]
                    ),

                "Top_K": row["Top-K"],

                "Model":
                    clean(row["Model"]),

                "Selected_Features":
                    clean(row["Selected Features"]),

                "Accuracy":
                    row["Accuracy"],

                "Precision":
                    row["Precision"],

                "Recall":
                    row["Recall"],

                "F1":
                    row["F1 Score"],

                "ROC_AUC":
                    row["ROC-AUC"],

                "Source_Sheet":
                    sheet
            })

    # ========================================================
    # PREDICTIVE REPEATED
    # ========================================================

    elif table_type == "Predictive_Repeated":

        for _, row in df.iterrows():

            predictive_repeated_rows.append({

                "Disease": disease,
                "Selector": selector,
                "Fusion": fusion,

                "Run":
                    row["Run"],

                "Method":
                    normalize_predictive_method(
                        row["Method"]
                    ),

                "Top_K":
                    row["Top_K"],

                "Model":
                    clean(row["Model"]),

                "Accuracy":
                    row["Accuracy"],

                "Precision":
                    row["Precision"],

                "Recall":
                    row["Recall"],

                "F1":
                    row["F1"],

                "ROC_AUC":
                    row["ROC_AUC"],

                "Selected_Features":
                    clean(row["Selected_Features"]),

                "Source_Sheet":
                    sheet
            })

    # ========================================================
    # PREDICTIVE SUMMARY
    # ========================================================

    elif table_type == "Predictive_Summary":

        for _, row in df.iterrows():

            predictive_summary_rows.append({

                "Disease": disease,
                "Selector": selector,
                "Fusion": fusion,

                "Method":
                    normalize_predictive_method(
                        row["Method"]
                    ),

                "Top_K":
                    row["Top_K"],

                "Model":
                    clean(row["Model"]),

                "Accuracy_Mean":
                    row["Accuracy_Mean"],

                "Accuracy_STD":
                    row["Accuracy_STD"],

                "Precision_Mean":
                    row["Precision_Mean"],

                "Precision_STD":
                    row["Precision_STD"],

                "Recall_Mean":
                    row["Recall_Mean"],

                "Recall_STD":
                    row["Recall_STD"],

                "F1_Mean":
                    row["F1_Mean"],

                "F1_STD":
                    row["F1_STD"],

                "ROC_AUC_Mean":
                    row["ROC_AUC_Mean"],

                "ROC_AUC_STD":
                    row["ROC_AUC_STD"],

                "Source_Sheet":
                    sheet
            })

    # ========================================================
    # BASELINE SELECTOR SCORES
    # ========================================================

    elif table_type == "Baseline_Scores":

        for _, row in df.iterrows():

            baseline_score_rows.append({

                "Disease": disease,
                "Selector": selector,
                "Fusion": fusion,

                "Feature":
                    clean(row["Feature"]),

                "Score_Type":
                    "ANOVA",

                "Baseline_Score":
                    row["ANOVA Score"],

                "Source_Sheet":
                    sheet

            })

    # ========================================================
    # CLINICAL TABLES
    # ========================================================

    elif table_type in [
        "Clinical_Raw_Math",
        "Clinical_Weights",
        "Clinical_Final_Score",
        "Clinical_Ranking"
    ]:

        for _, row in df.iterrows():

            record = {
                "Disease": disease,
                "Selector": selector,
                "Fusion": fusion,
                "Record_Type": table_type,
                "Feature": clean(row["Feature"]),
                "Raw_Math_Score": "",
                "Normalized_Math_Score": "",
                "Clinical_Weight": "",
                "Final_DODA_Score": "",
                "Math_Rank": "",
                "Clinical_Rank": "",
                "Final_Rank": "",
                "Final_Score": "",
                "Rank_Change": "",
                "Source_Sheet": sheet
            }

            if "Raw Math Score" in df.columns:
                record["Raw_Math_Score"] = row["Raw Math Score"]

            if "Normalized Math Score" in df.columns:
                record["Normalized_Math_Score"] = \
                    row["Normalized Math Score"]

            if "Clinical Weight" in df.columns:
                record["Clinical_Weight"] = \
                    row["Clinical Weight"]

            if "Final DODA Score" in df.columns:
                record["Final_DODA_Score"] = \
                    row["Final DODA Score"]

            if "Final Rank Fusion Score" in df.columns:
                record["Final_DODA_Score"] = \
                    row["Final Rank Fusion Score"]

            if "Math Rank" in df.columns:
                record["Math_Rank"] = row["Math Rank"]

            if "Clinical Rank" in df.columns:
                record["Clinical_Rank"] = row["Clinical Rank"]

            if "Final Rank" in df.columns:
                record["Final_Rank"] = row["Final Rank"]

            if "Final Score" in df.columns:
                record["Final_Score"] = row["Final Score"]

            if "Rank Change" in df.columns:
                record["Rank_Change"] = row["Rank Change"]

            clinical_rows.append(record)


    # ========================================================
    # FEATURE SET
    # ========================================================

    elif table_type == "Feature_Set":

        for _, row in df.iterrows():

            feature_set_rows.append({

                "Disease": disease,
                "Selector": selector,
                "Fusion": fusion,

                "Run": row["Run"],
                "Method": clean(row["Method"]),
                "Top_K": row["Top_K"],
                "Feature_Set": clean(row["Feature_Set"]),

                "Source_Sheet": sheet
            })


    # ========================================================
    # FEATURE FREQUENCY
    # ========================================================

    elif table_type == "Feature_Frequency":

        for _, row in df.iterrows():

            feature_frequency_rows.append({

                "Disease": disease,
                "Selector": selector,
                "Fusion": fusion,

                "Method": clean(row["Method"]),
                "Top_K": row["Top_K"],
                "Feature": clean(row["Feature"]),
                "Selected_Count": row["Selected_Count"],
                "Total_Runs": row["Total_Runs"],
                "Selection_Frequency_Percentage":
                    row["Selection_Frequency_Percentage"],

                "Source_Sheet": sheet
            })


    # ========================================================
    # FEATURE COUNT
    # ========================================================

    elif table_type == "Feature_Count":

        for _, row in df.iterrows():

            feature_count_rows.append({

                "Disease": disease,
                "Selector": selector,
                "Fusion": fusion,

                "Method": clean(row["Method"]),
                "Top_K": row["Top_K"],
                "Feature_Count": row["Feature_Count"],

                "Source_Sheet": sheet
            })


    # ========================================================
    # JACCARD PAIRWISE
    # ========================================================

    elif table_type == "Jaccard_Pairwise":

        for _, row in df.iterrows():

            jaccard_pairwise_rows.append({

                "Disease": disease,
                "Selector": selector,
                "Fusion": fusion,

                "Method": clean(row["Method"]),
                "Top_K": row["Top_K"],
                "Run_A": row["Run_A"],
                "Run_B": row["Run_B"],
                "Intersection": row["Intersection"],
                "Union": row["Union"],
                "Jaccard_Similarity":
                    row["Jaccard_Similarity"],

                "Source_Sheet": sheet
            })


    # ========================================================
    # JACCARD SUMMARY
    # ========================================================

    elif table_type == "Jaccard_Summary":

        for _, row in df.iterrows():

            jaccard_summary_rows.append({

                "Disease": disease,
                "Selector": selector,
                "Fusion": fusion,

                "Method": clean(row["Method"]),
                "Top_K": row["Top_K"],

                "Mean_Jaccard":
                    row["Mean_Jaccard"],
                "Std_Jaccard":
                    row["Std_Jaccard"],

                "Min_Jaccard":
                    row.get("Minimum_Jaccard",
                            row.get("Min_Jaccard", "")),

                "Max_Jaccard":
                    row.get("Maximum_Jaccard",
                            row.get("Max_Jaccard", "")),

                "Source_Sheet": sheet
            })


    # ========================================================
    # KUNCHEVA PAIRWISE
    # ========================================================

    elif table_type == "Kuncheva_Pairwise":

        for _, row in df.iterrows():

            kuncheva_pairwise_rows.append({

                "Disease": disease,
                "Selector": selector,
                "Fusion": fusion,

                "Method": clean(row["Method"]),
                "Top_K": row["Top_K"],
                "Run_A": row["Run_A"],
                "Run_B": row["Run_B"],
                "Intersection": row["Intersection"],
                "Kuncheva_Index":
                    row["Kuncheva_Index"],

                "Source_Sheet": sheet
            })


    # ========================================================
    # KUNCHEVA SUMMARY
    # ========================================================

    elif table_type == "Kuncheva_Summary":

        for _, row in df.iterrows():

            kuncheva_summary_rows.append({

                "Disease": disease,
                "Selector": selector,
                "Fusion": fusion,

                "Method": clean(row["Method"]),
                "Top_K": row["Top_K"],

                "Mean_Kuncheva":
                    row["Mean_Kuncheva"],
                "Std_Kuncheva":
                    row["Std_Kuncheva"],

                "Min_Kuncheva":
                    row.get("Minimum_Kuncheva",
                            row.get("Min_Kuncheva", "")),

                "Max_Kuncheva":
                    row.get("Maximum_Kuncheva",
                            row.get("Max_Kuncheva", "")),

                "Source_Sheet": sheet
            })


    # ========================================================
    # AGREEMENT PAIRWISE
    # ========================================================

    elif table_type == "Agreement_Pairwise":

        for _, row in df.iterrows():

            baseline_feature_col = next(
                (
                    c for c in [
                        "ANOVA_Features",
                        "LASSO_Features",
                        "mRMR_Features",
                        "RF_Features",
                        "Boruta_Features"
                    ]
                    if c in df.columns
                ),
                ""
            )

            agreement_pairwise_rows.append({

                "Disease": disease,
                "Selector": selector,
                "Fusion": fusion,

                "Run": row.get("Run", ""),
                "Top_K": row["Top_K"],

                "Baseline_Features":
                    clean(row[baseline_feature_col])
                    if baseline_feature_col else "",

                "DODA_Features":
                    clean(row["DODA_Features"]),

                "Common_Features":
                    clean(row.get(
                        "Common_Features",
                        row.get("Common_Feature_Count", "")
                    )),

                "Common_Feature_Count":
                    row.get("Common_Feature_Count", ""),

                "Same_Feature_Set":
                    row.get("Same_Feature_Set", ""),

                "Jaccard_Agreement":
                    row.get("Jaccard_Agreement", ""),

                "Source_Sheet": sheet
            })


    # ========================================================
    # AGREEMENT SUMMARY
    # ========================================================

    elif table_type == "Agreement_Summary":

        for _, row in df.iterrows():

            agreement_summary_rows.append({

                "Disease": disease,
                "Selector": selector,
                "Fusion": fusion,

                "Top_K": row["Top_K"],

                "Same_Feature_Set_Percentage":
                    row.get(
                        "Same_Feature_Set_Percentage",
                        ""
                    ),

                "Mean_Agreement":
                    row.get(
                        "Mean_Agreement",
                        row.get(
                            "Mean_Jaccard_Agreement",
                            ""
                        )
                    ),

                "Std_Agreement":
                    row.get(
                        "Std_Agreement",
                        row.get(
                            "Std_Jaccard_Agreement",
                            ""
                        )
                    ),

                "Mean_Common_Features":
                    row.get(
                        "Mean_Common_Features",
                        ""
                    ),

                "Min_Agreement":
                    row.get(
                        "Min_Agreement",
                        ""
                    ),

                "Max_Agreement":
                    row.get(
                        "Max_Agreement",
                        ""
                    ),

                "Source_Sheet": sheet
            })


# ============================================================
# DATAFRAMES
# ============================================================

source_df = pd.DataFrame(source_rows)

predictive_df = pd.DataFrame(predictive_rows)

predictive_repeated_df = pd.DataFrame(
    predictive_repeated_rows
)

predictive_summary_df = pd.DataFrame(
    predictive_summary_rows
)

clinical_df = pd.DataFrame(clinical_rows)

baseline_score_df = pd.DataFrame(
    baseline_score_rows
)

feature_set_df = pd.DataFrame(
    feature_set_rows
)

feature_frequency_df = pd.DataFrame(
    feature_frequency_rows
)

feature_count_df = pd.DataFrame(
    feature_count_rows
)

jaccard_pairwise_df = pd.DataFrame(
    jaccard_pairwise_rows
)

jaccard_summary_df = pd.DataFrame(
    jaccard_summary_rows
)

kuncheva_pairwise_df = pd.DataFrame(
    kuncheva_pairwise_rows
)

kuncheva_summary_df = pd.DataFrame(
    kuncheva_summary_rows
)

agreement_pairwise_df = pd.DataFrame(
    agreement_pairwise_rows
)

agreement_summary_df = pd.DataFrame(
    agreement_summary_rows
)


# ============================================================
# EXPERIMENT SETUP
# ============================================================

experiment_rows = []

for notebook in VALID_NOTEBOOKS:

    experiment_rows.append({

        "Disease": get_disease(notebook),

        "Notebook": notebook,

        "Selector": get_selector(notebook),

        "Fusion": get_fusion(notebook),

        "Dataset_Type":
            "Survey" if notebook.startswith("diabetes")
            else "Clinical",

        "Status": "Included"

    })

experiment_df = pd.DataFrame(experiment_rows)


# ============================================================
# WRITE MASTER WORKBOOK
# ============================================================

with pd.ExcelWriter(
    OUTPUT_FILE,
    engine="openpyxl"
) as writer:

    experiment_df.to_excel(
        writer,
        sheet_name="Experiment_Setup",
        index=False
    )

    source_df.to_excel(
        writer,
        sheet_name="Source_Index",
        index=False
    )

    predictive_df.to_excel(
        writer,
        sheet_name="Predictive_Results",
        index=False
    )

    predictive_repeated_df.to_excel(
        writer,
        sheet_name="Predictive_Repeated",
        index=False
    )

    predictive_summary_df.to_excel(
        writer,
        sheet_name="Predictive_Summary",
        index=False
    )

    clinical_df.to_excel(
        writer,
        sheet_name="Clinical_Feature_Analysis",
        index=False
    )

    baseline_score_df.to_excel(
        writer,
        sheet_name="Baseline_Scores",
        index=False
    )

    feature_set_df.to_excel(
        writer,
        sheet_name="Feature_Sets",
        index=False
    )

    feature_frequency_df.to_excel(
        writer,
        sheet_name="Feature_Frequency",
        index=False
    )

    feature_count_df.to_excel(
        writer,
        sheet_name="Feature_Count",
        index=False
    )

    jaccard_pairwise_df.to_excel(
        writer,
        sheet_name="Jaccard_Pairwise",
        index=False
    )

    jaccard_summary_df.to_excel(
        writer,
        sheet_name="Jaccard_Summary",
        index=False
    )

    kuncheva_pairwise_df.to_excel(
        writer,
        sheet_name="Kuncheva_Pairwise",
        index=False
    )

    kuncheva_summary_df.to_excel(
        writer,
        sheet_name="Kuncheva_Summary",
        index=False
    )

    agreement_pairwise_df.to_excel(
        writer,
        sheet_name="Agreement_Pairwise",
        index=False
    )

    agreement_summary_df.to_excel(
        writer,
        sheet_name="Agreement_Summary",
        index=False
    )


# ============================================================
# REPORT
# ============================================================

print("\n" + "=" * 70)
print("STEP 4 COMPLETE")
print("=" * 70)

print(f"\nCreated:")
print(OUTPUT_FILE)

print("\nRecord counts:")

print(
    f"Predictive Results       : "
    f"{len(predictive_df)}"
)

print(
    f"Predictive Repeated      : "
    f"{len(predictive_repeated_df)}"
)

print(
    f"Predictive Summary       : "
    f"{len(predictive_summary_df)}"
)

print(
    f"Clinical Analysis        : "
    f"{len(clinical_df)}"
)

print(
    f"Baseline Scores          : "
    f"{len(baseline_score_df)}"
)

print(
    f"Feature Sets             : "
    f"{len(feature_set_df)}"
)

print(
    f"Feature Frequency        : "
    f"{len(feature_frequency_df)}"
)

print(
    f"Jaccard Pairwise         : "
    f"{len(jaccard_pairwise_df)}"
)

print(
    f"Jaccard Summary          : "
    f"{len(jaccard_summary_df)}"
)

print(
    f"Kuncheva Pairwise        : "
    f"{len(kuncheva_pairwise_df)}"
)

print(
    f"Kuncheva Summary         : "
    f"{len(kuncheva_summary_df)}"
)

print(
    f"Agreement Pairwise       : "
    f"{len(agreement_pairwise_df)}"
)

print(
    f"Agreement Summary        : "
    f"{len(agreement_summary_df)}"
)

print("\nSource classification:")

print(
    source_df[
        [
            "Source_Sheet",
            "Table_Type",
            "Rows",
            "Columns"
        ]
    ].to_string(index=False)
)