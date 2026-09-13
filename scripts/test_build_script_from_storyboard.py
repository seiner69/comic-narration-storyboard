"""Deterministic text-generation regressions, not creative-quality scores."""
import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from build_script_from_storyboard import build


class ScriptBuilderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.board = Path(self.tmp.name) / 'storyboard.csv'
        self.script = Path(self.tmp.name) / 'script.md'

    def write_rows(self, rows, fields=None):
        with self.board.open('w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields or ['order', 'narration'])
            writer.writeheader()
            writer.writerows(rows)

    def test_legacy_lines_and_sort(self):
        self.write_rows([{'order': 2, 'narration': '乙。'}, {'order': 1, 'narration': '甲。\n\n第二句。'}])
        self.assertEqual(build(self.board, self.script), 3)
        self.assertEqual(self.script.read_text(encoding='utf-8'), '甲。\n第二句。\n乙。\n')

    def test_paragraphs_preserve_words_quotes_and_internal_lines(self):
        self.write_rows([{'order': 2, 'narration': '他没有回答。'}, {'order': 1, 'narration': '“为什么？”她问。\n同伴低着头。'}])
        build(self.board, self.script, paragraphs=True)
        self.assertEqual(self.script.read_text(encoding='utf-8'), '“为什么？”她问。\n同伴低着头。\n\n他没有回答。\n')

    def test_output_uses_deterministic_utf8_lf_bytes(self):
        self.write_rows([
            {'order': 1, 'narration': '“为什么？”\r\n她问。'},
            {'order': 2, 'narration': '他没有回答。'},
        ])
        build(self.board, self.script, paragraphs=True)
        self.assertEqual(self.script.read_bytes(), '“为什么？”\n她问。\n\n他没有回答。\n'.encode('utf-8'))

    def test_order_gap_and_duplicates_rejected_without_output(self):
        for orders in [(1, 3), (1, 1), (0, 1)]:
            with self.subTest(orders=orders):
                self.write_rows([{'order': n, 'narration': '正文。'} for n in orders])
                with self.assertRaises(ValueError):
                    build(self.board, self.script, paragraphs=True)
                self.assertFalse(self.script.exists())

    def test_empty_narration_rejected_without_output(self):
        self.write_rows([{'order': 1, 'narration': ' \n '}])
        with self.assertRaises(ValueError):
            build(self.board, self.script)
        self.assertFalse(self.script.exists())

    def test_missing_columns_rejected(self):
        self.board.write_text('wrong,narration\n1,text\n', encoding='utf-8')
        with self.assertRaises(ValueError):
            build(self.board, self.script)
        self.assertFalse(self.script.exists())

    def test_explicit_file_order_does_not_sort_ids(self):
        self.write_rows([
            {'paragraph_id': 'P10', 'narration': '“先听我说。”'},
            {'paragraph_id': 'P02', 'narration': '她没有回头。'},
        ], fields=['paragraph_id', 'narration'])
        build(self.board, self.script, paragraphs=True, file_order=True)
        self.assertEqual(self.script.read_text(encoding='utf-8'), '“先听我说。”\n\n她没有回头。\n')

    def test_missing_order_is_not_an_implicit_fallback(self):
        self.write_rows([{'paragraph_id': 'P01', 'narration': '正文。'}], fields=['paragraph_id', 'narration'])
        with self.assertRaisesRegex(ValueError, 'file-order'):
            build(self.board, self.script, paragraphs=True)
        self.assertFalse(self.script.exists())

    def test_file_order_rejects_duplicate_or_empty_paragraph_ids(self):
        for identifiers in [('P01', 'P01'), ('', 'P02'), (' ', 'P02')]:
            with self.subTest(identifiers=identifiers):
                self.write_rows([
                    {'paragraph_id': identifier, 'narration': '正文。'}
                    for identifier in identifiers
                ], fields=['paragraph_id', 'narration'])
                with self.assertRaisesRegex(ValueError, 'paragraph_id'):
                    build(self.board, self.script, file_order=True)
                self.assertFalse(self.script.exists())

    def test_file_order_rejects_conflicting_numbered_order(self):
        self.write_rows([{'order': 1, 'narration': '正文。'}])
        with self.assertRaisesRegex(ValueError, 'only for CSV without'):
            build(self.board, self.script, file_order=True)
        self.assertFalse(self.script.exists())

    def test_file_order_still_requires_narration(self):
        self.board.write_text('paragraph_id,wrong\nP01,text\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'narration'):
            build(self.board, self.script, file_order=True)
        self.assertFalse(self.script.exists())

    def test_synthetic_paragraphs_leave_inputs_unchanged(self):
        self.write_rows([
            {'paragraph_id': 'P10', 'narration': '灯塔失去了主电源。'},
            {'paragraph_id': 'P02', 'narration': '“备用灯还亮着。”守灯人说。'},
        ], fields=['paragraph_id', 'narration'])
        protected = Path(self.tmp.name) / 'approved-script.md'
        protected.write_bytes('上一版合成文本。\n'.encode('utf-8'))
        before = (self.board.read_bytes(), protected.read_bytes())
        build(self.board, self.script, paragraphs=True, file_order=True)
        expected = '灯塔失去了主电源。\n\n“备用灯还亮着。”守灯人说。\n'
        self.assertEqual(self.script.read_bytes(), expected.encode('utf-8'))
        self.assertEqual((self.board.read_bytes(), protected.read_bytes()), before)

    def test_all_platform_newlines_become_lf(self):
        for paragraphs in (False, True):
            for newline in ('\r', '\r\n', '\n'):
                with self.subTest(paragraphs=paragraphs, newline=repr(newline)):
                    self.write_rows([
                        {'order': 1, 'narration': '甲。' + newline + '乙。'},
                        {'order': 2, 'narration': '丙。'},
                    ])
                    build(self.board, self.script, paragraphs=paragraphs)
                    separator = '\n\n' if paragraphs else '\n'
                    expected = ('甲。\n乙。' + separator + '丙。\n').encode('utf-8')
                    self.assertEqual(self.script.read_bytes(), expected)

    def test_invalid_csv_leaves_existing_output_unchanged(self):
        for rows in ([], [{'order': 2, 'narration': '正文。'}],
                     [{'order': 1, 'narration': '   '}]):
            with self.subTest(rows=rows):
                self.write_rows(rows)
                self.script.write_bytes(b'existing protected output\n')
                with self.assertRaises(ValueError):
                    build(self.board, self.script, paragraphs=True)
                self.assertEqual(self.script.read_bytes(), b'existing protected output\n')

    def test_file_order_without_optional_ids(self):
        self.write_rows([{'narration': '甲。'}, {'narration': '乙。'}],
                        fields=['narration'])
        build(self.board, self.script, paragraphs=True, file_order=True)
        self.assertEqual(self.script.read_bytes(), '甲。\n\n乙。\n'.encode('utf-8'))

    def test_cli_paragraph_and_file_order_flags(self):
        self.write_rows([
            {'paragraph_id': 'P10', 'narration': '甲。\r乙。'},
            {'paragraph_id': 'P02', 'narration': '丙。'},
        ], fields=['paragraph_id', 'narration'])
        output = Path(self.tmp.name) / 'nested output' / 'script.md'
        before = self.board.read_bytes()
        result = subprocess.run(
            [sys.executable, '-B', str(Path(__file__).with_name('build_script_from_storyboard.py')),
             str(self.board), str(output), '--paragraphs', '--file-order'],
            capture_output=True, text=True, check=True,
        )
        self.assertIn('nonempty_narration_lines=3', result.stdout)
        self.assertEqual(output.read_bytes(), '甲。\n乙。\n\n丙。\n'.encode('utf-8'))
        self.assertEqual(self.board.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
