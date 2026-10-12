import os
import sys
import unittest
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import statusline  # noqa: E402


class FitTest(unittest.TestCase):
    def test_short_text_unchanged(self):
        self.assertEqual(statusline.fit("/a/b", 10), "/a/b")

    def test_long_text_truncated_with_ellipsis(self):
        out = statusline.fit("/home/user/projects/tmp", 10)
        self.assertEqual(out, "/home/use…")
        self.assertLessEqual(sum(statusline.char_width(c) for c in out), 10)

    def test_wide_characters_count_as_two_columns(self):
        out = statusline.fit("中文目录名字很长", 7)
        self.assertLessEqual(sum(statusline.char_width(c) for c in out), 7)
        self.assertTrue(out.endswith("…"))


class FmtLeftTest(unittest.TestCase):
    def test_empty_and_invalid(self):
        self.assertEqual(statusline.fmt_left(None), "")
        self.assertEqual(statusline.fmt_left("not a date"), "")

    def test_epoch_seconds(self):
        end = datetime.now(timezone.utc) + timedelta(hours=2, minutes=5)
        self.assertRegex(statusline.fmt_left(int(end.timestamp())), r" ↻2h0[45]m")

    def test_iso_string(self):
        end = datetime.now(timezone.utc) + timedelta(days=3, hours=1)
        self.assertRegex(statusline.fmt_left(end.isoformat()), r" ↻3d[01]h")

    def test_past_reset(self):
        past = datetime.now(timezone.utc) - timedelta(minutes=1)
        self.assertEqual(statusline.fmt_left(past.isoformat()), " ↻now")


class BarTest(unittest.TestCase):
    def test_bar_width_and_bounds(self):
        for pct in (-5, 0, 50, 100, 150):
            text = statusline.bar(pct)
            visible = text.replace("\033[31m", "").replace("\033[33m", "").replace("\033[32m", "")
            visible = visible.replace(statusline.DIM, "").replace(statusline.RESET, "")
            self.assertEqual(len(visible), statusline.BAR_WIDTH)

    def test_color_thresholds(self):
        self.assertEqual(statusline.color(10), "\033[32m")
        self.assertEqual(statusline.color(75), "\033[33m")
        self.assertEqual(statusline.color(95), "\033[31m")


if __name__ == "__main__":
    unittest.main()
