from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
REQUIRED = ["order_id", "order_date", "region", "product", "quantity", "unit_price", "source"]

def main():
    OUT.mkdir(exist_ok=True)
    df = pd.read_csv(ROOT / "data/sales_orders.csv")
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    invalid = df[df[["order_date", "quantity", "unit_price"]].isna().any(axis=1)].copy()
    clean = df.drop(index=invalid.index).copy()
    clean = clean[(clean["quantity"] >= 0) & (clean["unit_price"] >= 0)]
    clean["sales_amount"] = clean["quantity"] * clean["unit_price"]
    clean = clean.drop_duplicates(subset=["order_id"], keep="last")
    summary = clean.groupby("region", as_index=False).agg(
        orders=("order_id", "nunique"), units=("quantity", "sum"), sales_amount=("sales_amount", "sum")
    ).sort_values("sales_amount", ascending=False)
    clean.to_csv(OUT / "normalized_sales.csv", index=False)
    summary.to_csv(OUT / "regional_summary.csv", index=False)
    (OUT / "run_quality.md").write_text(
        "# Run quality\n\n"
        f"- Input rows: {len(df)}\n- Clean rows after validation/deduplication: {len(clean)}\n"
        f"- Invalid rows excluded: {len(invalid)}\n- Regions reported: {summary['region'].nunique()}\n",
        encoding="utf-8")
    print(summary.to_string(index=False))
    print(f"\nWrote report files to {OUT}")

if __name__ == "__main__":
    main()
