#!/usr/bin/env python3
"""为常见表格数据文件生成一个简洁的数据概览。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_table(path: Path):
    import pandas as pd

    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".tsv", ".tab"}:
        return pd.read_csv(path, sep="\t")
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if suffix == ".json":
        return pd.read_json(path)
    if suffix == ".parquet":
        return pd.read_parquet(path)
    raise ValueError(f"暂不支持这个文件类型: {suffix}")


def safe_value(value: Any) -> Any:
    if hasattr(value, "item"):
        return value.item()
    if isinstance(value, float) and (value != value):
        return None
    return value


def profile(path: Path, sample_rows: int) -> dict[str, Any]:
    df = read_table(path)
    total_rows = len(df)
    columns = []

    for name in df.columns:
        series = df[name]
        non_null = int(series.notna().sum())
        item: dict[str, Any] = {
            "name": str(name),
            "dtype": str(series.dtype),
            "non_null": non_null,
            "missing": int(total_rows - non_null),
            "missing_pct": round((total_rows - non_null) / total_rows, 4) if total_rows else 0,
            "unique": int(series.nunique(dropna=True)),
        }

        if series.dropna().empty:
            item["sample_values"] = []
        else:
            item["sample_values"] = series.dropna().astype(str).head(5).tolist()

        if str(series.dtype).startswith(("int", "float")):
            desc = series.describe()
            item["numeric_summary"] = {
                key: safe_value(round(desc[key], 6))
                for key in ["mean", "std", "min", "25%", "50%", "75%", "max"]
                if key in desc
            }

        columns.append(item)

    return {
        "file": str(path),
        "rows": int(total_rows),
        "columns": int(len(df.columns)),
        "duplicate_rows": int(df.duplicated().sum()),
        "column_profile": columns,
        "sample": json.loads(df.head(sample_rows).to_json(orient="records", date_format="iso")),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="为表格数据文件生成概览。")
    parser.add_argument("path", type=Path)
    parser.add_argument("--out", type=Path, help="把 JSON 概览写到这个路径。")
    parser.add_argument("--sample-rows", type=int, default=5)
    args = parser.parse_args()

    result = profile(args.path, args.sample_rows)
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
