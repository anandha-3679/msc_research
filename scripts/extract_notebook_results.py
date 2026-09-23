import json
from pathlib import Path
import pandas as pd
import re

# ============================================================
# CONFIG
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

NOTEBOOK_DIRS = [
    PROJECT_ROOT / "notebooks" / "anandha" / "Diabetes",
    PROJECT_ROOT / "notebooks" / "anandha" / "heartdisease",
]

OUTPUT_FILE = PROJECT_ROOT / "DODA_Notebook_Output_Inventory.xlsx"


# ============================================================
# HELPERS
# ============================================================

def clean_sheet_name(name):
    """Make a valid Excel sheet name."""
    name = re.sub(r'[\\/*?:\[\]]', '_', name)
    return name[:31]


def extract_tables_from_notebook(notebook_path):
    """
    Extract all HTML tables saved in notebook outputs.
    Does NOT execute the notebook.
    """

    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    tables = []

    for cell_number, cell in enumerate(nb.get("cells", [])):

        if cell.get("cell_type") != "code":
            continue

        outputs = cell.get("outputs", [])

        for output_number, output in enumerate(outputs):

            # ------------------------------------------------
            # HTML OUTPUT
            # ------------------------------------------------
            data = output.get("data", {})

            html = data.get("text/html")

            if html:
                try:
                    html_text = "".join(html)

                    extracted = pd.read_html(html_text)

                    for table_number, df in enumerate(extracted):

                        if df.empty:
                            continue

                        tables.append({
                            "cell": cell_number,
                            "output": output_number,
                            "table": table_number,
                            "dataframe": df,
                            "source": "HTML"
                        })

                except Exception:
                    pass

    return tables


# ============================================================
# MAIN
# ============================================================

all_results = []

for notebook_dir in NOTEBOOK_DIRS:

    if not notebook_dir.exists():
        print(f"WARNING: Directory not found: {notebook_dir}")
        continue

    notebooks = sorted(notebook_dir.glob("*.ipynb"))

    print(f"\nScanning: {notebook_dir}")
    print(f"Found {len(notebooks)} notebooks")

    for notebook in notebooks:

        print(f"  → {notebook.name}")

        tables = extract_tables_from_notebook(notebook)

        print(f"     Extracted {len(tables)} saved tables")

        for item in tables:

            df = item["dataframe"].copy()

            # Add metadata
            df.insert(0, "_Notebook", notebook.stem)
            df.insert(1, "_Cell", item["cell"])
            df.insert(2, "_Output", item["output"])
            df.insert(3, "_Table", item["table"])

            all_results.append({
                "disease": (
                    "Diabetes"
                    if "Diabetes" in str(notebook_dir)
                    else "Heart Disease"
                ),
                "notebook": notebook.stem,
                "cell": item["cell"],
                "output": item["output"],
                "table": item["table"],
                "dataframe": df
            })


# ============================================================
# WRITE EXCEL
# ============================================================

if not all_results:
    print("\nNo saved HTML tables were found.")
    print("Make sure the notebooks were saved after execution.")
    raise SystemExit


with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:

    # --------------------------------------------------------
    # INVENTORY
    # --------------------------------------------------------

    inventory = []

    for i, item in enumerate(all_results):

        df = item["dataframe"]

        inventory.append({
            "ID": i,
            "Disease": item["disease"],
            "Notebook": item["notebook"],
            "Cell": item["cell"],
            "Output": item["output"],
            "Table": item["table"],
            "Rows": len(df),
            "Columns": len(df.columns),
            "Column_Names": " | ".join(
                str(c) for c in df.columns
            )
        })

    inventory_df = pd.DataFrame(inventory)

    inventory_df.to_excel(
        writer,
        sheet_name="Inventory",
        index=False
    )

    # --------------------------------------------------------
    # EACH EXTRACTED TABLE
    # --------------------------------------------------------

    for i, item in enumerate(all_results):

        df = item["dataframe"]

        sheet_name = clean_sheet_name(
            f"{i}_{item['notebook']}"
        )

        # Excel sheet names must be unique
        base_name = sheet_name
        counter = 1

        while sheet_name in writer.book.sheetnames:
            sheet_name = clean_sheet_name(
                f"{base_name[:27]}_{counter}"
            )
            counter += 1

        # Flatten MultiIndex columns before exporting to Excel
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [
                " | ".join(
                    str(level).strip()
                    for level in col
                    if str(level).strip() and str(level).strip() != "nan"
                )
                for col in df.columns
            ]

        # Make sure all column names are strings
        df.columns = [str(col) for col in df.columns]

        df.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False
        )


print("\n" + "=" * 60)
print("EXTRACTION COMPLETE")
print("=" * 60)

print(f"\nOutput:")
print(OUTPUT_FILE)

print(f"\nTotal extracted tables: {len(all_results)}")

print("\nNext step:")
print("Open DODA_Notebook_Output_Inventory.xlsx")
print("and inspect the Inventory sheet.")