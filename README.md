# ISO3_Mapping_ILOSTAT

### Mapping ISO3 Codes to ILO Unemployment Data (19th ICLS Definition)

This repository contains a Python-based manual processing pipeline for mapping ISO3 country codes to ILOSTAT’s “Unemployment rates by reference area - Current ILO definition (19th ICLS)”dataset.

Since the original ILOSTAT data does not include ISO3 codes, ISO3 identifiers were assigned by referencing the country table exported from Navicat, enabling standardized country-level analysis.

---

##  1. Background

The unemployment data based on the 19th ICLS definition from ILOSTAT only provides country names in the `Area` column and does not include ISO3 country codes.
To resolve this limitation, ISO3 codes were mapped through the following process:

* Country name normalization
* Fuzzy string matching
* Manual override for known exceptions
* Review and exclusion of unmatched entities

---

##  2. Data Sources

### **① Unemployment Data (id=24.xlsx)**

* Downloaded from ILOSTAT
* Contains country or region names in the `Area` column

### **② Country Reference Table (country.xlsx)**

* Downloaded from Navicat
* Includes the following columns:

  * `longName_EN`
  * `shortName_EN`
  * `ISO3Code`

---

##  3. Matching Logic

### 1) Normalization

All country names are normalized using the following rules:

* Convert to lowercase
* Remove parentheses and their contents
* Remove special characters
* Remove the article "the"

This preprocessing step improves the accuracy of fuzzy matching.

---

###  2) Fuzzy Matching

* The `Area` values are normalized and compared against both `longName_EN` and `shortName_EN`.
* Matching is performed using `fuzzywuzzy.process.extractOne()`.
* A match is accepted only if the similarity score is **90 or higher**.

---

### 🔹 3) Manual Override

Some country names require manual intervention. For example:

* “Czechia” is not listed in the country reference table but is equivalent to “The Czech Republic”.
  → It is therefore forcibly mapped to ISO3 code **CZE**.

---

### 🔹 4) Unmatched Countries

Countries that fail to meet the matching threshold or do not exist in the reference table are logged and excluded from the final dataset.

Examples:

* “Jersey”
* “Kosovo”

---

##  4. Python Code

```python
import pandas as pd
import re
from fuzzywuzzy import process

# Function to normalize country names for better matching
def normalize(text):
    text = str(text).lower().strip()  # Convert to lowercase and remove leading/trailing spaces
    text = re.sub(r'\(.*?\)', '', text)  # Remove content inside parentheses
    text = re.sub(r'[^a-z0-9 ]', '', text)  # Remove special characters
    text = re.sub(r'\bthe\b', '', text)  # Remove the word 'the'
    return text.strip()

# Load the ILO unemployment dataset (19th ICLS definition)
id24 = pd.read_excel("id=24.xlsx")

# Load the country reference table (from Navicat)
country = pd.read_excel("country.xlsx")

# Normalize both long and short country names for matching
country['norm_long'] = country['longName_EN'].apply(normalize)
country['norm_short'] = country['shortName_EN'].apply(normalize)

# Create a list of all normalized country names (long + short)
all_names = pd.concat([country['norm_long'], country['norm_short']]).dropna().unique()

# Function to match a country name from the ILO dataset to an ISO3 code
def match_iso3(area):
    norm_area = normalize(area)
    # Manual override for Czechia
    if norm_area == "czechia":
        return "CZE"
    # Fuzzy match against normalized country names
    match, score = process.extractOne(norm_area, all_names)
    # If the match score is high enough, return the corresponding ISO3 code
    if score >= 90:
        row = country[(country['norm_long'] == match) | (country['norm_short'] == match)]
        if not row.empty:
            return row['ISO3Code'].values[0]
    # Return None if no good match is found
    return None

# Apply the matching function to the 'Area' column to assign ISO3 codes
id24['ISO3Code'] = id24['Area'].apply(match_iso3)

# Save the result to a new Excel file
id24.to_excel("id=24_with_fuzzy_ISO3.xlsx", index=False)
```

---

##  Output

The resulting file will include an additional column:

* `ISO3Code` – mapped ISO3 country code based on fuzzy matching and manual overrides.

This enables consistent country-level analysis and integration with Navicat-based datasets and dashboards.

---

##  Notes & Limitations

* Countries not found in the Navicat reference table are excluded.
* Fuzzy matching accuracy depends on normalization rules and threshold value.
* This logic is designed specifically for single-country unemployment indicators and may not generalize to multi-entity datasets.

---

##  Author

**Minsol Cho**
IFPRI MTI Unit
Data Integration & Dashboard Development


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ISO3_Mapping_ILOSTAT  
### Mapping ISO3 Codes to ILO Unemployment Data (19th ICLS Definition)


-----------------
#korean

이 저장소는 ILOSTAT의 **“Unemployment rates by reference area – Current ILO definition (19th ICLS)”** 데이터에 ISO3 국가코드를 매핑하기 위한 Python 기반 매뉴얼 처리 로직을 포함합니다.  
ILOSTAT 데이터에는 ISO3 코드가 기본적으로 제공되지 않기 때문에, 표준화된 국가 단위 분석을 위해 Navicat에서 내려받은 국가 테이블을 참조하여 ISO3 코드를 할당했습니다.

---

## 📌 1. 배경 (Background)

ILOSTAT의 19th ICLS 기준 실업률 데이터는 국가명(`Area`)만 포함하고 ISO3 코드가 제공되지 않습니다.  
이를 해결하기 위해 다음 단계로 ISO3 국가 코드를 매핑하였습니다:

- 국가명 정규화 (Normalization)
- Fuzzy string matching
- 매뉴얼 수기 보정 (Manual override)
- 미매칭 국가 검토 및 제외

---

## 📁 2. 데이터 소스 (Data Sources)

### **① Unemployment Data (id=24.xlsx)**  
- ILOSTAT에서 다운로드  
- `Area` 컬럼에 국가 또는 지역 이름 포함  

### **② Country Reference Table (country.xlsx)**  
Navicat에서 다운로드  
포함된 컬럼:
- `longName_EN`
- `shortName_EN`
- `ISO3Code`

---

## ⚙️ 3. 매핑 로직 (Matching Logic)

### 🔹 **1) Normalization**
모든 국가명을 아래 규칙으로 정규화함:
- 소문자로 변환  
- 괄호() 제거  
- 특수문자 제거  
- 관사 “the” 제거  
→ fuzzy matching 정확도를 높이기 위한 전처리

---

### 🔹 **2) Fuzzy Matching**
- `Area` 데이터와 `longName_EN`, `shortName_EN`을 모두 정규화하여 비교  
- `fuzzywuzzy.process.extractOne()` 사용  
- similarity score **90 이상일 때만 매칭 승인**

---

### 🔹 **3) Manual Override**
- “Czechia”는 country 테이블에 없었으나  
  “The Czech Republic”과 동일 의미  
→ ISO3 코드 **“CZE”** 로 강제 매핑

---

### 🔹 **4) Unmatched Countries**
매칭 실패한 국가 출력  
예시:
- “Jersey”
- “Kosovo”

이들은 country reference table에 없어 최종 데이터에서 제외됨.

---

## 🧪 4. 코드 (Python Code)

```python
import pandas as pd
import re
from fuzzywuzzy import process

# Function to normalize country names for better matching
def normalize(text):
    text = str(text).lower().strip()  # Convert to lowercase and remove leading/trailing spaces
    text = re.sub(r'\(.*?\)', '', text)  # Remove content inside parentheses
    text = re.sub(r'[^a-z0-9 ]', '', text)  # Remove special characters
    text = re.sub(r'\bthe\b', '', text)  # Remove the word 'the'
    return text.strip()

# Load the ILO unemployment dataset (19th ICLS definition)
id24 = pd.read_excel("id=24.xlsx")

# Load the country reference table (from Navicat)
country = pd.read_excel("country.xlsx")

# Normalize both long and short country names for matching
country['norm_long'] = country['longName_EN'].apply(normalize)
country['norm_short'] = country['shortName_EN'].apply(normalize)

# Create a list of all normalized country names (long + short)
all_names = pd.concat([country['norm_long'], country['norm_short']]).dropna().unique()

# Function to match a country name from the ILO dataset to an ISO3 code
def match_iso3(area):
    norm_area = normalize(area)
    # Manual override for Czechia
    if norm_area == "czechia":
        return "CZE"
    # Fuzzy match against normalized country names
    match, score = process.extractOne(norm_area, all_names)
    # If the match score is high enough, return the corresponding ISO3 code
    if score >= 90:
        row = country[(country['norm_long'] == match) | (country['norm_short'] == match)]
        if not row.empty:
            return row['ISO3Code'].values[0]
    # Return None if no good match is found
    return None

# Apply the matching function to the 'Area' column to assign ISO3 codes
id24['ISO3Code'] = id24['Area'].apply(match_iso3)

# Save the result to a new Excel file
id24.to_excel("id=24_with_fuzzy_ISO3.xlsx", index=False)
