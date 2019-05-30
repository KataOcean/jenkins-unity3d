import hashlib
import os

import yaml
from requests import get


class CheckNewVersion(object):
    release_url = 'https://public-cdn.cloud.unity3d.com/hub/prod/releases-linux.json'

    @staticmethod
    def get_parent_full_path(file_name):
        # TODO: move to utils
        base_dirname = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
        return os.path.join(base_dirname, file_name)

    @staticmethod
    def get_versions_dict(unity_versions):
        with open(unity_versions, "r") as f:
            unity_versions = yaml.safe_load(f.read())
        if unity_versions is None:
            unity_versions = {}
        return unity_versions

    def get_all_unity_versions(self):
        return list(
            {
                **self.get_versions_dict(self.get_parent_full_path("unity_versions.yml")),
                **self.get_versions_dict(self.get_parent_full_path("unity_versions.old.yml")),
            }.keys()
        )

    def get_latest_unity_official_releases_versions(self):
        releases = self.get_releases()
        official_releases = []
        for official_release in releases['official']:
            official_releases.append(official_release['version'])
        return official_releases

    def get_releases(self):
        return get(self.release_url).json()

    def generate_unity_version_block(self, detailed_missing_version):
        original_download_url = detailed_missing_version['downloadUrl']
        version_key = detailed_missing_version['version']
        build = 'f1'
        version = version_key.replace(build, '')
        underscore = version_key.replace('.', '_')
        download_url_hash = original_download_url. \
            replace('https://download.unity3d.com/download_unity/', '').split('/')[0]
        download_url = f'https://beta.unity3d.com/download/{download_url_hash}/UnitySetup-{version_key}'
        sha1 = self.get_sha1_from_download_url(download_url)
        release_notes = f'https://unity3d.com/unity/whats-new/{version_key}'
        release_url = f'https://beta.unity3d.com/download/{download_url_hash}/public_download.html'

        return {
            version_key: {
                'dockerfile_name': 'unitysetup',
                'version': version,
                'underscore': underscore,
                'download_url': download_url,
                'sha1': sha1,
                'build': build,
                'release_notes': release_notes,
                'release_url': release_url
            }
        }

    @staticmethod
    def download_file(url, file_name):
        with open(file_name, "wb") as file:
            response = get(url)
            file.write(response.content)

    def get_sha1_from_download_url(self, download_url):
        file_name = 'UnitySetup'
        self.download_file(download_url, file_name)
        sha1 = self.sha1(file_name)
        os.remove(file_name)
        return sha1

    @staticmethod
    def sha1(file_name):
        block_size = 65536
        hashing_algorithm = hashlib.sha1()
        with open(file_name, 'rb') as afile:
            buf = afile.read(block_size)
            while len(buf) > 0:
                hashing_algorithm.update(buf)
                buf = afile.read(block_size)
        return hashing_algorithm.hexdigest()

    def print(self):
        official_releases = self.get_latest_unity_official_releases_versions()
        current_versions = self.get_all_unity_versions()
        missing_versions = [version for version in official_releases if version not in current_versions]

        releases = self.get_releases()

        missing_versions_details = []
        for missing_version in missing_versions:
            for release in releases['official']:
                if release['version'] == missing_version:
                    missing_versions_details.append(release)

        unity_version_objects = []
        for detailed_missing_version in missing_versions_details:
            unity_version_objects.append(self.generate_unity_version_block(detailed_missing_version))

        for unity_version_object in unity_version_objects:
            print(yaml.dump(unity_version_object))


if __name__ == '__main__':
    CheckNewVersion().print()
