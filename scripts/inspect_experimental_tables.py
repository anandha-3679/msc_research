from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "DODA_Notebook_Output_Inventory.xlsx"
OUTPUT_FILE = ROOT / "DODA_Table_Inspection.xlsx"

EXPERIMENTAL_METHODS = [
    "annova",
    "anova",
    "lasso",
    "mrmr",
    "_rf",
    "boruta",
]

def is_experimental(sheet_name):
    name = sheet_name.lower()

    if "_eda" in name:
        return False

    return any(method in name for method in EXPERIMENTAL_METHODS)


xls = pd.ExcelFile(INPUT_FILE)

inspection_rows = []

with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:

    for sheet in xls.sheet_names:

        if sheet.lower() == "inventory":
            continue

        if not is_experimental(sheet):
            continue

        df = pd.read_excel(INPUT_FILE, sheet_name=sheet)

        # Flatten MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [
                " | ".join(
                    str(x).strip()
                    for x in col
                    if str(x).strip().lower() != "nan"
                )
                for col in df.columns
            ]

        df.columns = [str(c).strip() for c in df.columns]

        # Record metadata
        inspection_rows.append({
            "Source_Sheet": sheet,
            "Rows": len(df),
            "Columns": len(df.columns),
            "Column_Names": " | ".join(df.columns),
        })

        # Write actual table
        safe_name = sheet[:31]

        df.to_excel(
            writer,
            sheet_name=safe_name,
            index=False
        )

    # Summary first
    summary_df = pd.DataFrame(inspection_rows)

    summary_df.to_excel(
        writer,
        sheet_name="Inspection_Summary",
        index=False
    )


print("=" * 70)
print("EXPERIMENTAL TABLE INSPECTION COMPLETE")
print("=" * 70)

print(f"\nOutput:")
print(OUTPUT_FILE)

print(f"\nExperimental sheets inspected: {len(inspection_rows)}")

print("\nSummary:")
print(
    pd.DataFrame(inspection_rows).to_string(index=False)
)