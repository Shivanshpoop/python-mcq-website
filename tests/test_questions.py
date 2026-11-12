import json
import unittest
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "questions.json"

class QuestionBankTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.questions = json.loads(DATA.read_text(encoding="utf-8"))

    def test_question_bank_is_not_empty(self):
        self.assertGreater(len(self.questions), 0)

    def test_ids_are_unique(self):
        ids = [q["id"] for q in self.questions]
        self.assertEqual(len(ids), len(set(ids)))

    def test_each_question_has_four_options_and_valid_answer(self):
        for question in self.questions:
            with self.subTest(question=question["id"]):
                self.assertEqual(len(question["options"]), 4)
                self.assertGreaterEqual(question["answer"], 0)
                self.assertLess(question["answer"], len(question["options"]))
                self.assertTrue(question["question"].strip())
                self.assertTrue(question["explanation"].strip())

if __name__ == "__main__":
    unittest.main()
