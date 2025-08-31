import argparse
from pathlib import Path
import pandas as pd

CONFIG = {"categoria":"categoria","fecha":"fecha","valor":"valor","unidades":"unidades"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="data/example.csv")
    ap.add_argument("--outdir", default="outputs")
    args = ap.parse_args()

    csv_path = Path(args.csv)
    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv_path)
    fcol, vcol, ucol, ccol = CONFIG["fecha"], CONFIG["valor"], CONFIG["unidades"], CONFIG["categoria"]
    if fcol in df.columns: df[fcol] = pd.to_datetime(df[fcol], errors="coerce")
    if vcol in df.columns and ucol in df.columns: df["total"] = df[vcol] * df[ucol]
    if ucol in df.columns: df[ucol] = df[ucol].fillna(0)
    if "total" in df.columns: filtered = df.query("total > 0")
    elif vcol in df.columns: filtered = df.query(f"{vcol} > 0")
    else: filtered = df
    if fcol in filtered.columns: filtered["mes"] = filtered[fcol].dt.to_period("M").astype(str)
    else: filtered["mes"] = "NA"
    group_cols = [c for c in [ccol, "mes"] if c in filtered.columns]
    metrics = {}
    if vcol in filtered.columns: metrics.update({"valor_sum": (vcol, "sum"), "valor_avg": (vcol, "mean")})
    if "total" in filtered.columns: metrics.update({"total_sum": ("total","sum"), "total_avg": ("total","mean")})
    metrics["n"] = (filtered.columns[0], "count")
    summary = filtered.groupby(group_cols).agg(**metrics).reset_index()
    summary.to_csv(outdir/"pandas_summary.csv", index=False)
    try: summary.to_parquet(outdir/"pandas_summary.parquet", index=False)
    except Exception as e: print("parquet no disponible:", e)

if __name__ == "__main__":
    main()
