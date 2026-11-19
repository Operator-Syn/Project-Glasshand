#!/usr/bin/env python3
"""nbstripout_safe.py — git clean filter and textconv driver for .ipynb files.

Registered per clone by ``setup_notebook_filters.py``; copied into a repository's
``scripts/`` directory. Deliberately Python rather than a shell script so the same
file works on Linux, macOS and Windows: the filter command names the project
interpreter explicitly, so nothing here depends on a writable POSIX shell.

Compared with invoking ``nbstripout`` directly, three differences:

1. ``SIGPIPE`` is restored to ``SIG_DFL`` where the platform has it. Python ignores
   the signal and raises ``BrokenPipeError``, so when a pager, a diff viewer or an
   early-closing reader stops reading, the filter would print a traceback over the
   diff. Windows has no ``SIGPIPE``, so the reset is guarded.
2. nbformat warnings are silenced in textconv mode only. Historical blobs committed
   before cell ids were required would otherwise reprint ``MissingIDFieldWarning``
   on every view. The clean-filter path keeps the warning, so a notebook that is
   genuinely missing ids still complains when it is staged.
3. The ``--quiet`` flag belongs to this wrapper, not to nbstripout: it is accepted
   and removed before the real argument parser sees it, which keeps one registration
   working across nbstripout versions that do not define it.

The output bytes are identical to plain nbstripout; only stderr and the
exit-on-EPIPE behaviour differ.

Usage: ``<project interpreter> nbstripout_safe.py [--quiet] [-t|--textconv] [files...]``
"""

from __future__ import annotations

import signal
import sys
import warnings


def configure_signal(signal_module=signal) -> None:
    """Make the process exit quietly when its reader closes the pipe.

    POSIX only: Windows has no SIGPIPE, so the attribute check is what keeps this
    importable there rather than a platform test.
    """
    if hasattr(signal_module, "SIGPIPE"):
        signal_module.signal(signal_module.SIGPIPE, signal_module.SIG_DFL)


def split_wrapper_args(argv: list[str]) -> tuple[list[str], bool]:
    """Remove the wrapper's own flags, reporting whether warnings should be silenced.

    ``--quiet`` is ours. ``-t``/``--textconv`` is nbstripout's and is passed through,
    but it also means git is rendering a diff rather than staging, which is when
    historical blobs would otherwise reprint warnings on every view.
    """
    quiet = "--quiet" in argv
    forwarded = [arg for arg in argv if arg != "--quiet"]
    textconv = quiet or any(arg in ("-t", "--textconv") for arg in forwarded)
    return forwarded, textconv


def main(argv: list[str] | None = None) -> int:
    configure_signal()

    forwarded, textconv = split_wrapper_args(list(sys.argv[1:] if argv is None else argv))
    if textconv:
        warnings.filterwarnings("ignore")

    try:
        from nbstripout._nbstripout import main as nbstripout_main
    except ImportError:
        print(
            "nbstripout_safe: nbstripout is not importable by "
            f"{sys.executable}; run 'uv sync' (or set NBSTRIPOUT_PYTHON) "
            "and re-run scripts/setup_notebook_filters.py",
            file=sys.stderr,
        )
        return 1

    # nbstripout parses sys.argv, so the forwarded arguments replace ours
    sys.argv = [sys.argv[0]] + forwarded
    result = nbstripout_main()
    # nbstripout's entry point returns None on success; argparse-style ints pass through
    return 0 if result is None else int(result)


if __name__ == "__main__":
    sys.exit(main())
