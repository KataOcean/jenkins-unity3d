# Script to generate the `.gitlab-ci.yml`

## 1. Add version meta data

Specify versions in `unity_versions.py`.
Uncomment the desired versions to include them in the build.

## 2. Install requirements

- Install python
- Install script requirements

```bash
# Executed in this folder, ci-generator/
pip install -r requirements.txt
```

## 3. Generate new gitlab-ci.yml config

### 3.1 Powershell 5.1 variant

This is only if you're using powershell 5.1. The commands below are specific to ensure the output `.gitlab-ci.yml` file is encoded with UTF-8 without BOM.

```powershell
# Executed in this folder, ci-generator/
$path = Resolve-Path ../.gitlab-ci.yml
$result = python generate-gitlab-ci.py
$encoding = New-Object Text.UTF8Encoding $False
[IO.File]::WriteAllLines($path, $result, $encoding)
```

### 3.2 Bash/Powershell 6+ variant

```bash
# Executed in this folder, ci-generator/
python generate-gitlab-ci.py > ../.gitlab-ci.yml
```

## 4. Done

:tada:
