# Script to generate the `.gitlab-ci.yml`

This is a python script that will generate the `.gitlab-ci.yml` to make it easier to build desired unity versions. 

## 1. Add version meta data

Specify desired versions in `unity_versions.py`. Move already built versions to `unity_versions.old.yml`

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
$result = python generate_gitlab_ci.py
$encoding = New-Object Text.UTF8Encoding $False
[IO.File]::WriteAllLines($path, $result, $encoding)
```

### 3.2 Bash/Powershell 6+ variant

```bash
# Executed in this folder, ci-generator/
python generate_gitlab_ci.py > ../.gitlab-ci.yml
```

## 4. Done

:tada:

## Where to find hashes

There doesn't seem to be an official place for this, but one can find a lot of information in [the well maintained archlinux unity-editor AUR](https://aur.archlinux.org/cgit/aur.git/?h=unity-editor). For the latest version, you can find them at the same place where unity-hub electron application finds them: https://public-cdn.cloud.unity3d.com/hub/prod/releases-linux.json

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

## Use a different Dockerfile for the version

Do something like this:

```yaml
2018.4.0f1:
  dockerfile: my-version-specific.Dockerfile
  # ...
```

## Use a different Dockerfile for a component

The script will automatically try to use the Dockerfile for the component so if you set a `dockerfile: unitysetup.Dockerfile`, the `android` component will use `unitysetup-android.Dockerfile` if it exists, otherwise, it will fallback to `unitysetup.Dockerfile`.

## Development and testing

It would be neat if this ran in the CI, but it's getting a bit meta here. I wrote test to make it easier to maintain the generator. It's only a way to get a breakpoint quickly anywhere in the code.

### locally

```bash
pip install -r requirements.txt
coverage run -m unittest tests/test*.py
```

### docker

```bash
docker run --rm -it -v "$PWD/../:/app" python:3.7-alpine sh -c \
'cd /app/ci-generator && pip install -r requirements.txt && coverage run -m unittest tests/test*.py'
```

Coverage report is generated, open `htmlcov/index.html` :+1:
