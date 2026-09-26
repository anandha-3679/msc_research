from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "DODA_Master_Results.xlsx"

df = pd.read_excel(MASTER, sheet_name="Predictive_Results")

print("=" * 80)
print("PREDICTIVE RESULTS — STRUCTURE DIAGNOSTIC")
print("=" * 80)

# ------------------------------------------------------------
# 1. SOURCE SHEETS
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("1. SOURCE_SHEET DISTRIBUTION")
print("=" * 80)

print(df["Source_Sheet"].value_counts().to_string())


# ------------------------------------------------------------
# 2. DISEASE × SELECTOR
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("2. DISEASE × SELECTOR")
print("=" * 80)

print(
    df.groupby(["Disease", "Selector"])
      .size()
      .to_string()
)


# ------------------------------------------------------------
# 3. DISEASE × SELECTOR × FUSION
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("3. DISEASE × SELECTOR × FUSION")
print("=" * 80)

print(
    df.groupby(["Disease", "Selector", "Fusion"])
      .size()
      .to_string()
)


# ------------------------------------------------------------
# 4. METHOD MAPPING
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("4. METHOD MAPPING")
print("=" * 80)

mapping = (
    df.groupby(["Selector", "Fusion", "Method"])
      .size()
      .reset_index(name="Rows")
      .sort_values(["Selector", "Fusion", "Method"])
)

print(mapping.to_string(index=False))


# ------------------------------------------------------------
# 5. SOURCE SHEET × METHOD
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("5. SOURCE SHEET × METHOD")
print("=" * 80)

source_method = (
    df.groupby(["Source_Sheet", "Method"])
      .size()
      .reset_index(name="Rows")
)

print(source_method.to_string(index=False))


# ------------------------------------------------------------
# 6. FULL EXPERIMENT COUNTS
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("6. DISEASE × SELECTOR × METHOD × TOP_K × MODEL")
print("=" * 80)

counts = (
    df.groupby(
        [
            "Disease",
            "Selector",
            "Method",
            "Top_K",
            "Model"
        ]
    )
    .size()
    .reset_index(name="Rows")
)

print(
    counts["Rows"]
    .value_counts()
    .sort_index()
    .to_string()
)


# ------------------------------------------------------------
# 7. SHOW ONE SELECTOR IN DETAIL
# ------------------------------------------------------------

for selector in sorted(df["Selector"].dropna().unique()):

    print("\n" + "=" * 80)
    print(f"7. DETAIL — {selector}")
    print("=" * 80)

    temp = df[df["Selector"] == selector]

    print(
        temp[
            [
                "Disease",
                "Selector",
                "Fusion",
                "Method",
                "Top_K",
                "Model",
                "Source_Sheet"
            ]
        ]
        .drop_duplicates()
        .sort_values(
            ["Disease", "Top_K", "Model", "Method"]
        )
        .to_string(index=False)
    )


print("\n" + "=" * 80)
print("DONE")
print("=" * 80)