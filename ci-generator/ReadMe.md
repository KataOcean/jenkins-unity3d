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

## Where to find hashes

There doesn't seem to be an official place for this, but one can find a lot of information in [the well maintained archlinux unity-editor AUR](https://aur.archlinux.org/cgit/aur.git/?h=unity-editor). For the latest version, one can find the versions in the file used by unity-hub electron application: https://public-cdn.cloud.unity3d.com/hub/prod/releases-linux.json

pro tip: use [jq](https://stedolan.github.io/jq/)

```bash
curl https://public-cdn.cloud.unity3d.com/hub/prod/releases-linux.json | jq '.'
```

## How to get the sha1

1. Download the `UnitySetup` file manually
2. Retrieve the sha1 with `sha1sum` command

example:

```bash
wget https://beta.unity3d.com/download/dc414eb9ed43/UnitySetup-2019.1.3f1 -O unity.deb
sha1sum unity.deb | awk '{print $1}'
```
