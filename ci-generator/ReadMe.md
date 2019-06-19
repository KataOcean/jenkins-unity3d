# Script to generate the `.gitlab-ci.yml`

This is a python script that will generate the `.gitlab-ci.yml` to make it easier to build desired unity versions. For easier usage, use `docker-compose`.

## 1. Move existing versions from `unity_versions.py` to unity_versions.old.yml`

```bash
# move existing versions to old versions
cat unity_versions.py >> unity_versions.old.yml

# empty unity_versions.py
echo '' > unity_versions.py

# grab latest versions from unity
docker-compose run --rm update

# generate .gitlab-ci.yml using updated versions
docker-compose run --rm generate
```

## Where to find hashes

There doesn't seem to be an official place for this, but one can find a lot of information in [the well maintained archlinux unity-editor AUR](https://aur.archlinux.org/cgit/aur.git/?h=unity-editor). For the latest version, you can find them at the same place where unity-hub electron application finds them: https://public-cdn.cloud.unity3d.com/hub/prod/releases-linux.json

Pro tip: use [jq](https://stedolan.github.io/jq/)

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

Set something like this in `unity_versions.yml`:

```yaml
2018.4.0f1:
  dockerfile: my-version-specific.Dockerfile
  # ...
```

Then generate the `.gitlab-ci.yml` file again.

## Use a different Dockerfile for a component

The generator script will automatically try to use the `Dockerfile` for the component so if you set a `dockerfile: unitysetup.Dockerfile`, the `android` component will use `unitysetup-android.Dockerfile` if it exists, otherwise, it will fallback to `unitysetup.Dockerfile`.

## Development and testing

I wrote these tests to make it easier to maintain the generator. It's only a way to get a breakpoint anywhere in the code, don't be scared ;)

```bash
docker-compose run --rm test
```

### Failing snapshot tests

If tests are failing due to updated ci template, you can generate snapshot tests using the following command:

```bash
docker-compose run --rm update-test-snapshots
```

### Get code coverage report

```bash
docker-compose run --rm test
docker-compose run --rm test-report
docker-compose run --rm test-report-html
```

Then open `htmlcov/index.html` :+1:
