import argparse
from pathlib import Path
import duckdb

CONFIG = {"categoria":"categoria","fecha":"fecha","valor":"valor","unidades":"unidades"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="data/example.csv")
    ap.add_argument("--outdir", default="outputs")
    args = ap.parse_args()

    csv_path = Path(args.csv)
    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)

    c = duckdb.connect()
    fcol, vcol, ucol, ccol = CONFIG["fecha"], CONFIG["valor"], CONFIG["unidades"], CONFIG["categoria"]
    query = f"""
        with src as (select * from read_csv_auto('{csv_path.as_posix()}')),
        base as (
          select *, try_cast({fcol} as timestamp) as fecha_dt,
                 coalesce({ucol}, 0) as unidades_ok,
                 case when {vcol} is not null and {ucol} is not null then {vcol} * {ucol} else null end as total
          from src
        ),
        filtrado as (
          select * from base
          where (total is null and {vcol} > 0) or (total is not null and total > 0)
        ),
        con_grupo as (
          select coalesce({ccol}, 'NA') as categoria,
                 case when fecha_dt is not null then strftime(fecha_dt, '%Y-%m') else 'NA' end as mes,
                 {vcol}, total
          from filtrado
        )
        select categoria, mes,
               sum({vcol}) as valor_sum, avg({vcol}) as valor_avg,
               sum(coalesce(total,0)) as total_sum, avg(coalesce(total,0)) as total_avg,
               count(*) as n
        from con_grupo
        group by 1,2
        order by 1,2
    """
    df = c.execute(query).df()
    df.to_csv(outdir/"duckdb_summary.csv", index=False)
    try: c.execute(f"copy ({query}) to '{(outdir/'duckdb_summary.parquet').as_posix()}' (format parquet)")
    except Exception as e: print("parquet no disponible:", e)

if __name__ == "__main__":
    main()
