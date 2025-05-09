#ssh파일만 만들기

import pandas as pd

# 파일 경로
input_tsv = "ncbi_dataset (2).tsv"
output_script = "download_datasets.sh"
include_items = "GFF3,rna,cds,protein,genome,seq-report"

def generate_datasets_script(tsv_path, output_path):
    df = pd.read_csv(tsv_path, sep="\t", dtype=str)

    if "Assembly Accession" not in df.columns:
        raise ValueError("'Assembly Accession' 컬럼이 없습니다.")

    accessions = df["Assembly Accession"].dropna().unique()

    with open(output_path, "w") as f:
        f.write("#!/bin/bash\n\n")
        for acc in accessions:
            cmd = (
                f"datasets download genome accession {acc} "
                f'--include "{include_items}" --filename {acc}.zip'
            )
            f.write(cmd + "\n")

    print(f"✅ 생성 완료: {output_path} ({len(accessions)}개 accession)")

# 실행
generate_datasets_script("ncbi_dataset (2).tsv", "download_datasets.sh")
