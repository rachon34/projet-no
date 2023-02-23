import unittest
from unittest.mock import MagicMock, patch

from app.data_scraper import scrape_data


class TestDataScraper(unittest.TestCase):
    
    def setUp(self):
        self.url = 'https://example.com'
    
    @patch('app.data_scraper.requests.Session')
    @patch('app.data_scraper.ImageToTextTask')
    @patch('app.data_scraper.parse_html')
    def test_scrape_data(self, mock_parse_html, mock_ImageToTextTask, mock_Session):
        # Mock response object
        response = MagicMock()
        response.content = b'<html><body>test</body></html>'
        response.status_code = 200
        
        # Mock captcha image url
        mock_soup = MagicMock()
        mock_soup.find.return_value.get.return_value = 'captcha_url'
        mock_Session.return_value.get.return_value = response
        mock_Session.return_value.headers = {}
        mock_Session.return_value.headers.update.return_value = None
        mock_parse_html.return_value = {'Title': 'Test', 'Author': 'John Doe', 'Date': '2022-02-23', 'Content': 'Test content'}
        
        # Mock captcha response
        mock_solver = MagicMock()
        mock_ImageToTextTask.return_value = mock_solver
        mock_solver.captcha_handler.return_value = 'captcha_response'
        
        # Call function
        data = scrape_data(self.url)
        
        # Assertions
        mock_Session.assert_called_once()
        mock_Session.return_value.get.assert_called_once_with(self.url)
        mock_soup.find.assert_called_once_with('img', {'id': 'captcha_image'})
        mock_solver.captcha_handler.assert_called_once_with('captcha_url')
        mock_parse_html.assert_called_once_with('<html><body>test</body></html>')
        self.assertEqual(data, {'Title': 'Test', 'Author': 'John Doe', 'Date': '2022-02-23', 'Content': 'Test content'})
