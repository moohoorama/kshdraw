#!/usr/bin/env python3
"""
Patch docs/index.html to add iOS Safari UME fix.
This script is called after pygbag build to apply necessary patches.
"""

import re
import sys
from pathlib import Path

# The iOS Safari UME fix code to insert
IOS_SAFARI_FIX = '''
        // iOS Safari touch fix for User Media Engagement
        function enableUME(e) {
            if (window.MM && !window.MM.UME) {
                window.MM.UME = true;
                console.log("UME enabled via touch/click");
            }
        }

        // Add event listeners for iOS Safari
        document.body.addEventListener('touchstart', enableUME, {passive: true});
        document.body.addEventListener('touchend', enableUME, {passive: true});
        document.body.addEventListener('click', enableUME, {passive: true});
        document.body.addEventListener('mousedown', enableUME, {passive: true});

        // Also add to canvas
        var canvas = document.getElementById('canvas');
        if (canvas) {
            canvas.addEventListener('touchstart', enableUME, {passive: true});
            canvas.addEventListener('touchend', enableUME, {passive: true});
            canvas.addEventListener('click', enableUME, {passive: true});
        }
'''

def patch_index_html(file_path: Path) -> bool:
    """Patch the index.html file with iOS Safari fix."""

    if not file_path.exists():
        print(f"Error: {file_path} not found")
        return False

    content = file_path.read_text()

    # Check if already patched
    if "iOS Safari touch fix" in content:
        print("Already patched, skipping...")
        return True

    # Find the insertion point: after "box.hidden = debug_hidden"
    pattern = r'(box\.hidden\s*=\s*debug_hidden\s*\n)'

    if not re.search(pattern, content):
        print("Error: Could not find insertion point in index.html")
        return False

    # Insert the fix after the matched line
    patched_content = re.sub(
        pattern,
        r'\1' + IOS_SAFARI_FIX,
        content
    )

    file_path.write_text(patched_content)
    print(f"Successfully patched {file_path}")
    return True


def main():
    # Default path
    script_dir = Path(__file__).parent.parent
    index_path = script_dir / "docs" / "index.html"

    # Allow custom path as argument
    if len(sys.argv) > 1:
        index_path = Path(sys.argv[1])

    success = patch_index_html(index_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
