import unittest
from pathlib import Path
from src.find_multiples.create_list_of_multiples import \
    get_list_pdfs, get_dict_of_duplicates, output_to_file

class TestFindMultiples(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_get_list_pdfs(self):
        target = Path('../test_assets/')
        exclude = {'exclude_me'}
        pdf_list = get_list_pdfs(target, exclude)
        self.assertEqual(len(pdf_list), 6)
        self.assertIn(Path('../test_assets/0000 ABCD0000 (2).pdf'), pdf_list)
        self.assertNotIn(Path('../test_assets/exclude_me/1111 ABCD0000.pdf'), pdf_list)
