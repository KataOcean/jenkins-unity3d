import json
import os
from unittest import TestCase, mock

import requests_mock

from src.check_new_version import CheckNewVersion
from tests import utils


class TestGitlabCiGenerator(TestCase):
    class_path = 'src.check_new_version.CheckNewVersion'

    @staticmethod
    def mock_releases_json_get(mocked_request):
        with open(utils.full_path_from_relative_path('data/releases-linux.json'), 'r') as f:
            json_text = f.read()
        mocked_request.get('https://public-cdn.cloud.unity3d.com/hub/prod/releases-linux.json', text=json_text)
        return json_text

    def test_get_versions_dict(self):
        with self.subTest('test_empty.yml'):
            result = CheckNewVersion.get_versions_dict(utils.full_path_from_relative_path('data/test_empty.yml'))
            self.assertEqual(result, {})

        with self.subTest('test_unitysetup_2019.yml'):
            result = CheckNewVersion.get_versions_dict(
                utils.full_path_from_relative_path('data/test_unitysetup_2019.yml')
            )
            self.assertEqual(list(result.keys()), ['2019.1.3f1'])

    def test_get_all_unity_versions(self):
        check_new_version = CheckNewVersion()
        with mock.patch('src.check_new_version.CheckNewVersion.get_versions_dict') as mocked_get_versions_dict:
            mocked_get_versions_dict.return_value = {'test': 'value'}
            result = check_new_version.get_all_unity_versions()
        self.assertEqual(result, ['test'])

    @requests_mock.mock()
    def test_get_latest_unity_official_releases_versions(self, mocked_request):
        check_new_version = CheckNewVersion()
        self.mock_releases_json_get(mocked_request)
        result = check_new_version.get_latest_unity_official_releases_versions()
        self.assertEqual(result, ['2017.4.27f1', '2018.2.21f1', '2018.3.14f1', '2018.4.1f1', '2019.1.4f1'])

    @requests_mock.mock()
    def test_get_releases(self, mocked_request):
        check_new_version = CheckNewVersion()
        json_text = self.mock_releases_json_get(mocked_request)
        response = check_new_version.get_releases()
        self.assertEqual(response, json.loads(json_text))

    def test_generate_unity_version_block(self):
        check_new_version = CheckNewVersion()
        with open(utils.full_path_from_relative_path('data/releases-linux.json')) as f:
            json_text = f.read()
        official_release = json.loads(json_text)['official'][0]
        version_block = check_new_version.generate_unity_version_block(official_release)
        self.assertEqual(version_block, {
            '2017.4.27f1': {
                'build': 'f1',
                'dockerfile_name': 'unitysetup',
                'download_url': 'https://beta.unity3d.com/download/0c4b856e4c6e/UnitySetup-2017.4.27f1',
                'release_notes': 'https://unity3d.com/unity/whats-new/2017.4.27f1',
                'release_url': 'https://beta.unity3d.com/download/0c4b856e4c6e/public_download.html',
                'sha1': '8dae4dd18df383a598830c6e2489cdecdcb19273',
                'underscore': '2017_4_27f1',
                'version': '2017.4.27'
            }
        })

    @requests_mock.mock()
    def test_download_file(self, mocked_request):
        url = 'https://example.com'
        mocked_request.get('https://example.com', text='example')
        file_name = 'temp_file.txt'
        CheckNewVersion.download_file(url, file_name)
        with open(file_name, 'r') as f:
            downloaded_file_content = f.read()
        self.assertEqual('example', downloaded_file_content)
        os.remove(file_name)

    @requests_mock.mock()
    def test_get_sha1_from_download_url(self, mocked_request):
        check_new_version = CheckNewVersion()
        download_url = 'https://example.com'
        mocked_request.get(download_url, text='example')
        sha1 = check_new_version.get_sha1_from_download_url(download_url)
        self.assertFalse(os.path.exists('UnitySetup'),
                         msg='Downloaded file should be removed after verifying the sha1 to keep repository clean')
        self.assertEqual(sha1, 'c3499c2729730a7f807efb8676a92dcb6f8a3f8f')

    def test_sha1(self):
        file_name = utils.full_path_from_relative_path('data/releases-linux.json')
        result = CheckNewVersion.sha1(file_name)
        self.assertEqual(result, 'b0d8c80edcc0e501b4fbf7c2d09e6205e7d77ec8')

    def test_print(self):
        # TODO: complete this test using similar snapshot testing pattern from gitlab_ci_generator.py
        pass
