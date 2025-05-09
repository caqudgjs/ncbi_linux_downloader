#ssh파일만들고 실행 후 압축풀기
import pandas as pd
import subprocess
import os
import zipfile

# 설정
tsv_path = "ncbi_dataset.tsv"
include_items = "GFF3,rna,cds,protein,genome,seq-report"
download_dir = "downloads"  # 다운로드 zip 및 폴더 저장 경로
os.makedirs(download_dir, exist_ok=True)

def download_and_extract(tsv_path, include_items):
    df = pd.read_csv(tsv_path, sep="\t", dtype=str)

    if "Assembly Accession" not in df.columns:
        raise ValueError("'Assembly Accession' 컬럼이 없습니다.")

    accessions = df["Assembly Accession"].dropna().unique()

    for acc in accessions:
        zip_name = f"{acc}.zip"
        zip_path = os.path.join(download_dir, zip_name)

        # datasets 명령어 실행
        cmd = [
            "datasets", "download", "genome", "accession", acc,
            "--include", include_items,
            "--filename", zip_path
        ]
        print(f"▶️ 다운로드 중: {acc}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"❌ 실패: {acc}\n{result.stderr}")
            continue

        # 압축 해제 경로
        extract_dir = os.path.join(download_dir, acc)
        os.makedirs(extract_dir, exist_ok=True)

        # 하위폴더 없이 압축 해제
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for member in zip_ref.infolist():
                    # 파일명만 추출하여 평면적으로 저장
                    filename = os.path.basename(member.filename)
                    if not filename:  # 디렉토리 스킵
                        continue
                    source = zip_ref.open(member)
                    target_path = os.path.join(extract_dir, filename)
                    with open(target_path, "wb") as target:
                        target.write(source.read())
            print(f"✅ 압축 해제 완료: {acc}")
        except zipfile.BadZipFile:
            print(f"❌ 잘못된 zip 파일: {zip_path}")

# 실행
download_and_extract(tsv_path, include_items)
# 압축 해제 후 zip 파일 삭제
for acc in df["Assembly Accession"].dropna().unique():
    zip_name = f"{acc}.zip"
    zip_path = os.path.join(download_dir, zip_name)
    if os.path.exists(zip_path):
        os.remove(zip_path)
        print(f"🗑️ 삭제 완료: {zip_path}")
    else:
        print(f"❌ 삭제 실패: {zip_path} (존재하지 않음)")
