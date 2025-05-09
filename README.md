# NCBI Genome Downloader

이 프로젝트는 NCBI의 Assembly Accession 목록이 포함된 TSV 파일을 기반으로,
`datasets` CLI를 사용해 지정된 유전체 데이터를 다운로드하고, 각 ZIP 파일을 개별 폴더로 풀어 저장합니다.


## ✨ 코드 작성 목적

NCBI에서 제공하는 유전체 데이터를 수작업으로 다운로드하는 과정은 시간이 많이 들고 오류 발생 가능성도 높습니다.  
이에 따라, 여러 개의 `Assembly Accession` 값을 포함한 TSV 파일을 기반으로 다음과 같은 자동화 파이프라인을 구축하고자 본 코드를 작성하였습니다:

- **NCBI Datasets CLI**를 통해 유전체 관련 zip 파일을 자동으로 다운로드하고,
- 다운로드된 각 `.zip` 파일을 파일명과 동일한 폴더에 **하위 폴더 없이 평면적으로 압축 해제**하며,
- 전체 작업을 한 번의 Python 실행으로 처리할 수 있도록 구성했습니다.

특히, `--include` 옵션을 통해 `genome`, `gff3`, `cds`, `rna`, `protein` 등 **다양한 데이터 유형을 선택적으로 추가할 수 있다는 점**이 본 코드의 유연성과 확장성을 높이는 데 중요한 역할을 했습니다.

해당 구조는 대규모 유전체 분석, 생물정보학 파이프라인 설계, 데이터 정제 자동화 등의 목적으로 활용하기에 적합합니다.

## ✅ 요구사항

### Python

- Python >= 3.7 (권장: 3.8 ~ 3.11)

### Python 라이브러리

| 라이브러리 | 권장 버전 | 설치 명령어 |
|------------|------------|--------------|
| pandas     | >= 1.3.0   | `pip install pandas>=1.3.0` |

※ `os`, `zipfile`, `subprocess`는 Python 내장 모듈입니다.

### NCBI Datasets CLI

- CLI 도구명: `datasets`
- 설치 권장:

```bash
conda install -c conda-forge ncbi-datasets-cli
```

- 설치 확인:

```bash
datasets version
```

## 🔧 사용법

1. TSV 파일에 `'Assembly Accession'` 컬럼이 포함되어 있어야 합니다.
2. 폴더에 tsv파일과 파이썬파일(ncbi_downloader_linux.py)를 넣고 돌립니다
3. 아래와 같은 명령어가 자동으로 생성되고 실행됩니다:

```bash
datasets download genome accession GCA_000001405.28 \
  --include "GFF3,rna,cds,protein,genome,seq-report" \
  --filename GCA_000001405.28.zip
```

3. `.zip` 파일은 다운로드 후, 파일명과 같은 폴더에 하위 폴더 없이 압축이 풀립니다.

## 📁 예시 구조

```
downloads/
├── GCA_000001405.28.zip
├── GCA_000001405.28/
│   ├── genome.fna
│   ├── protein.faa
```

## 🔗 참조

- [NCBI Datasets CLI 문서](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/)
