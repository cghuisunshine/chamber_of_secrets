import re
import unittest
from pathlib import Path


READER_HTML = Path(__file__).resolve().parents[1] / "aligned_reader" / "index.html"


class AlignedReaderHtmlTests(unittest.TestCase):
    def test_reader_persists_and_restores_latest_sentence(self):
        html = READER_HTML.read_text(encoding="utf-8")

        self.assertIn("readerProgressKey", html)
        self.assertRegex(html, r"localStorage\.getItem\(readerProgressKey\)")
        self.assertRegex(html, r"localStorage\.setItem\(readerProgressKey, JSON\.stringify")
        self.assertRegex(html, r"savedProgress\?\.sentenceId")
        self.assertRegex(html, r"loadChapter\(savedProgress\?\.chapterIndex \?\? 0, false, savedProgress\?\.sentenceId")
        self.assertRegex(html, r"pendingRestoreSentence")
        self.assertRegex(html, r"audio\.addEventListener\('loadedmetadata', \(\) => \{[^}]*pendingRestoreSentence")

    def test_reader_script_does_not_mix_nullish_and_or_without_parentheses(self):
        html = READER_HTML.read_text(encoding="utf-8")

        self.assertNotRegex(html, r"\?\?[^();\n]*\|\|")

    def test_timeupdate_does_not_pass_event_as_time_override(self):
        html = READER_HTML.read_text(encoding="utf-8")

        self.assertNotIn("audio.addEventListener('timeupdate', updateTimes)", html)
        self.assertIn("audio.addEventListener('timeupdate', () => updateTimes())", html)

    def test_pending_restore_time_is_used_until_seek_finishes(self):
        html = READER_HTML.read_text(encoding="utf-8")

        self.assertIn("if (pendingRestoreSentence && localOverride === null)", html)
        self.assertIn("audio.addEventListener('seeked', () => {", html)
        self.assertIn("Math.abs(audio.currentTime - pendingRestoreSentence.localBegin) < 0.25", html)


if __name__ == "__main__":
    unittest.main()
