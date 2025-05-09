#ssh 파일 만들고 실행


import pandas as pd
import subprocess
import os

# 파일 경로
tsv_path = "ncbi_dataset.tsv"
script_path = "download_datasets.sh"
include_items = "GFF3,rna,cds,protein,genome,seq-report"

def generate_and_execute_script(tsv_path, script_path, include_items):
    # TSV 읽기
    df = pd.read_csv(tsv_path, sep="\t", dtype=str)

    # 필요한 컬럼 확인
    if "Assembly Accession" not in df.columns:
        raise ValueError("'Assembly Accession' 컬럼이 존재하지 않습니다.")

    # accession 목록 추출
    accessions = df["Assembly Accession"].dropna().unique()

    # 쉘 스크립트 생성
    with open(script_path, "w") as f:
        f.write("#!/bin/bash\n\n")
        for acc in accessions:
            cmd = f'datasets download genome accession {acc} --include "{include_items}" --filename {acc}.zip'
            f.write(cmd + "\n")

    # 실행 권한 부여
    os.chmod(script_path, 0o755)

    # bash 실행
    print(f"▶️ {script_path} 실행 중...\n")
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)

    # 출력 결과 확인
    if result.returncode == 0:
        print("✅ 실행 완료")
    else:
        print("❌ 오류 발생:")
        print(result.stderr)

# 실행
generate_and_execute_script(tsv_path, script_path, include_items)
