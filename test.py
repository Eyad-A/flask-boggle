from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class BoggleTests(TestCase):

    def setUp(self):
        """setup before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        """test initial board"""

        with self.client:
            response = self.client.get('/')
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn('board', session)
            self.assertIn(b'High Score', response.data)
            self.assertIn(b'Seconds Left', response.data)

    def test_valid_word(self):
        """Test words that are on the board"""

        with self.client as client:
            with client.session_transaction() as ses:
                ses['board'] = [["A", "R", "T", "D"], 
                                 ["N", "E", "Z", "J", "S"], 
                                 ["Q", "L", "P", "V", "C"], 
                                 ["K", "S", "H", "B", "H"], 
                                 ["I", "A", "R", "U", "Z"]]
        response = self.client.get('/check-word?word=art')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test words that are not on the board"""

        self.client.get('/')
        response = self.client.get('/check-word?word=painting')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test words that do not exist"""

        self.client.get('/')
        response = self.client.get('/check-word?word=whoaaaaeeeeoa')
        self.assertEqual(response.json['result'], 'not-word')
