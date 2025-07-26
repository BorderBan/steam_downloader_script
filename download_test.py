import unittest
from unittest.mock import patch
from download import fetch_contentid, fetch_appid, download

class TestSteamDownloader(unittest.TestCase):
    def setUp(self):
        # Пример валидных ссылок
        self.urls = [
            "https://steamcommunity.com/sharedfiles/filedetails/?id=1111111111",
            "https://steamcommunity.com/sharedfiles/filedetails/?id=2222222222",
            "https://steamcommunity.com/sharedfiles/filedetails/?id=3333333333"
        ]

    def test_fetch_contentid(self):
        for idx, url in enumerate(self.urls, start=1):
            self.assertEqual(fetch_contentid(url), int(url.split('=')[1]))

    @patch('download.requests.post')
    def test_fetch_appid(self, mock_post):
        # Мокаем ответ Steam API
        mock_post.return_value.json.return_value = {
            'response': {
                'publishedfiledetails': [
                    {'consumer_app_id': 480}
                ]
            }
        }
        self.assertEqual(fetch_appid(1111111111), 480)

    @patch('download.os.system')
    def test_download(self, mock_system):
        pairs = [(480, 1111111111), (480, 2222222222), (480, 3333333333)]
        download(pairs)
        self.assertTrue(mock_system.called)
        # Проверяем, что команда содержит все contentid
        cmd = mock_system.call_args[0][0]
        self.assertIn("1111111111", cmd)
        self.assertIn("2222222222", cmd)
        self.assertIn("3333333333", cmd)

if __name__ == "__main__":
    unittest.main()