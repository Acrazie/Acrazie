"""Structural regression checks for the GitHub profile; no dependencies."""
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from generate_banners import ROOT, hero, wordmark


class ProfileTests(unittest.TestCase):
    def test_assets_match_generator(self):
        for name, render in [('hero-banner.svg', hero), ('skills-wordmark.svg', wordmark)]:
            actual = (ROOT / 'assets' / name).read_text()
            self.assertEqual(actual, render())
            ET.fromstring(actual)
            self.assertNotIn('<script', actual)
            self.assertNotIn('#10B981', actual)

    def test_native_content_and_links(self):
        text = (ROOT / 'README.md').read_text()
        for obsolete in ['shields.io', 'snake', 'surface.svg', 'divider.svg', 'Linktree', 'style=']:
            self.assertNotIn(obsolete, text)
        self.assertLess(text.index('## Agent Skills Ecosystem'), text.index('## Engineering Stack'))
        for link_text in re.findall(r'<a [^>]+>(.*?)</a>', text, re.S):
            self.assertEqual(link_text, link_text.strip())
        for src in re.findall(r'src="(\./[^"]+)"', text):
            self.assertTrue((ROOT / src).is_file(), src)
        for slug in ['svg-icon-designer-acrazie', 'skill-refiner-acrazie', 'audit-repository-acrazie']:
            self.assertIn('https://www.skills.sh/acrazie/skills/' + slug, text)
        self.assertIn('\nnpx skills add acrazie/skills\n', text)

    def test_accessible_motion(self):
        self.assertIn('prefers-reduced-motion:reduce', hero())


if __name__ == '__main__':
    unittest.main()
