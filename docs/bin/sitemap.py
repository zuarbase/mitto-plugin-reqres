#!/usr/bin/env python3
"""
Simple script to generate a sitemap.

Example:

    sitemap.py  https://www.zuar.com/api/mitto/plugin/amazon_advertising/  build/html  _static  _sources  _templates

    Generates a sitemap of build/html to stdout.  If the directories
    `_static`, `_sources`, or `_templates` exist under `build/html`, the
    files and directories they contain will be ignored.

    ROOT_URL is the location under which the contents of SRC_DIR will appear
    when on the site.  Note that ROOT_URL has a trailing slash.

"""

import argparse
import datetime
import os
import pathlib
import sys
import textwrap

from typing import List


def header_elements():
    """
    Return sitemap prolog XML
    """

    return textwrap.dedent(
        """<?xml version="1.0" encoding="UTF-8"?>
        <urlset
           xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
           xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
           http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"
        >""")


def footer_elements():
    """
    Return sitemap epilog XML
    """

    return "</urlset>"


def url_elements(url, lastmod):
    """
    Return sitemap entry XML for single URL
    """

    return (f"   <url>\n"
            f"      <loc>{url}</loc>\n"
            f"      <lastmod>{lastmod}</lastmod>\n"
            f"   </url>")


def sitemap_files(entity: pathlib.Path, exclude_dirs: List[str]) -> str:
    """
    Generator returning files to be included in sitemap.
    """

    if entity.is_file():
        if entity.suffix.lower() == ".html":
            yield entity
        return

    for path in entity.iterdir():
        if str(path) in exclude_dirs:
            continue
        yield from sitemap_files(path, exclude_dirs)


def create_sitemap(root_url, root_dir, exclude_dirs):
    """
    Print the sitemap to stdout
    """
    lastmod = datetime.datetime.now().date().isoformat()

    root_dir = pathlib.Path(root_dir)
    os.chdir(root_dir)

    root_dir = pathlib.Path()

    print(header_elements())
    for sitemap_file in sitemap_files(root_dir, exclude_dirs):
        url = root_url + str(sitemap_file)
        print(url_elements(url, lastmod))
    print(footer_elements())

    return 0


def parse_args():
    parser = argparse.ArgumentParser(
        epilog=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("ROOT_URL", default=pathlib.Path(),
                        help="root URL for pages")
    parser.add_argument("SRC_DIR", default=pathlib.Path(), type=pathlib.Path,
                        help="directory structure containing html files")
    parser.add_argument("EXCL_DIR", default=None, type=str, nargs="*",
                        help="directory to exclude")
    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()
    sys.exit(create_sitemap(args.ROOT_URL, args.SRC_DIR, args.EXCL_DIR))
