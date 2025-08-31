#!/usr/bin/env python3
"""
Minimal, safe splitter for chargeback-evidence-app.md → real files.

Behavior (kept intentionally simple and deterministic):
- Detect headings that look like filenames/paths (## or ###, ending with a known extension)
- Capture the FIRST fenced code block (``` ... ```) immediately after the heading
- Write it verbatim to <output_dir>/<heading-path>
- Create directories as needed
- Default is DRY RUN; use --create to actually write files

Examples:
- "## package.json" → <output_dir>/package.json
- "## supabase/migrations/core/0001_billing_entitlements.sql" → <output_dir>/supabase/migrations/core/0001_billing_entitlements.sql

This mirrors the successful pattern used in split_study_buddy.py but generalized.
"""

import os
import re
import argparse
from pathlib import Path
from typing import List, Dict, Tuple


FILE_HEADING_RE = re.compile(r"^(#{2,3})\s+(.+\.(?:ts|tsx|js|mjs|json|sql|md|css))\s*$")
FENCE_RE = re.compile(r"^```")


class ChargebackSplitter:
    def __init__(self, input_file: str, output_dir: str = "chargeback-evidence-app", dry_run: bool = True) -> None:
        self.input_file = input_file
        self.output_dir = output_dir
        self.dry_run = dry_run
        self.files_to_create: List[Dict[str, str]] = []
        self.current_file: str | None = None
        self.current_content: List[str] = []
        self.line_number: int = 0

    def parse_file(self) -> None:
        print(f"{'[DRY RUN] ' if self.dry_run else ''}Parsing {self.input_file}...")

        with open(self.input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        in_code_block = False
        saw_open_fence_for_current = False

        i = 0
        n = len(lines)
        while i < n:
            line = lines[i]
            self.line_number = i + 1

            m = FILE_HEADING_RE.match(line)
            if m:
                # On a new file heading, flush any pending file
                if self.current_file and self.current_content:
                    self._save_current_file()

                heading_path = m.group(2).strip()
                self.current_file = heading_path
                self.current_content = []
                in_code_block = False
                saw_open_fence_for_current = False
                i += 1
                continue

            # If we are expecting the first code block after a file heading
            if self.current_file:
                if FENCE_RE.match(line):
                    # Toggle fence state
                    if not saw_open_fence_for_current:
                        # First opening fence after heading starts content capture
                        saw_open_fence_for_current = True
                        in_code_block = True
                        # skip this fence line (language marker)
                        i += 1
                        continue
                    else:
                        # Closing fence for the first block → finish this file capture
                        in_code_block = False
                        saw_open_fence_for_current = False
                        # Save immediately; ignore any subsequent blocks until next heading
                        self._save_current_file()
                        # Reset current so we don't accidentally append more
                        self.current_file = None
                        self.current_content = []
                        i += 1
                        continue

                if in_code_block:
                    self.current_content.append(line)

            i += 1

        # End of file: flush any pending file with captured content
        if self.current_file and self.current_content:
            self._save_current_file()

    def _save_current_file(self) -> None:
        if not self.current_file or not self.current_content:
            return
        out_path = os.path.join(self.output_dir, self.current_file)
        content = ''.join(self.current_content)
        self.files_to_create.append({
            'path': out_path,
            'content': content,
        })

    def create_files(self) -> None:
        print(f"\n{'[DRY RUN] ' if self.dry_run else ''}Processing {len(self.files_to_create)} files...\n")
        made_dirs: set[Path] = set()

        for f in self.files_to_create:
            file_path = Path(f['path'])
            dir_path = file_path.parent

            # Ensure directory exists
            if dir_path not in made_dirs and str(dir_path) != '.':
                if self.dry_run:
                    print(f"[DRY RUN] Would create directory: {dir_path}")
                else:
                    dir_path.mkdir(parents=True, exist_ok=True)
                    print(f"Created directory: {dir_path}")
                made_dirs.add(dir_path)

            preview = f['content'][:100].replace('\n', '\\n') + ("..." if len(f['content']) > 100 else "")

            if self.dry_run:
                print(f"[DRY RUN] Would create file: {file_path}")
                print(f"          Size: {len(f['content'])} bytes")
                print(f"          Preview: {preview}")
                print()
            else:
                with open(file_path, 'w', encoding='utf-8', newline='') as out:
                    out.write(f['content'])
                print(f"Created file: {file_path} ({len(f['content'])} bytes)")

    def run(self) -> None:
        try:
            self.parse_file()
            self.create_files()
            if self.dry_run:
                print("\n[DRY RUN COMPLETE] No files were created. Run with --create to write files.")
            else:
                print(f"\n✅ Successfully created {len(self.files_to_create)} files!")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            if self.line_number:
                print(f"   Last processed line: {self.line_number}")
            raise


def main() -> int:
    parser = argparse.ArgumentParser(description='Split chargeback-evidence-app.md into project files')
    parser.add_argument('input_file', nargs='?', default='docs/chargeback-evidence-app.md', help='Input markdown file (default: docs/chargeback-evidence-app.md)')
    parser.add_argument('-o', '--output-dir', default='chargeback-evidence-app', help='Output directory (default: chargeback-evidence-app)')
    parser.add_argument('--dry-run', action='store_true', default=True, help='Preview actions without writing (default: True)')
    parser.add_argument('--create', action='store_true', help='Actually write files (overrides --dry-run)')

    args = parser.parse_args()
    if args.create:
        args.dry_run = False

    if not os.path.exists(args.input_file):
        print(f"❌ Error: Input file '{args.input_file}' not found!")
        return 1

    splitter = ChargebackSplitter(input_file=args.input_file, output_dir=args.output_dir, dry_run=args.dry_run)
    splitter.run()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

