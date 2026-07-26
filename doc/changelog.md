# Changelog

Summary of changes made in the zantei-utf8 project, relative to the original `zantei20070218` server image.

## 2026-07-26

- Removed the three now-unused `jcode.pl` copies (`cgi-bin/jcode.pl`, `cgi-bin/up/lib/jcode.pl`, `cgi-bin/ziten/jcode.pl`); all `require` call sites had already been commented out on 2026-07-18, and no live references remained

## 2026-07-18

- Restored `sub/bbsadmin.pl` and `sub/bbstopic.pl` from the original (dauso0001, unmodified Preview 9); both were deliberately removed from the server image for security reasons, not lost to backup gaps
- Applied vulnerability 1 fix (path traversal via `$FORM{'e'}`) to the restored `bbstopic.pl`: whitelist validation + 3-argument `open()`
- Placed `etc/bbspass.pl` (admin password file); all 3 admin password hashes nulled out
- Commented out DSBL/BBQ/proxy-check code (external services long defunct); added no-op stub functions so callers remain intact
- Live-tested on Perl 5.38.2: board display (GET), posting (POST), past-log search listing, and topic listing (using restored `bbstopic.pl`) — all confirmed working

## Earlier work

- Cleaned server image: removed logs, access logs, images, SSH private keys, counters, deny-host files, and stray backup files (judged by filename pattern only, without inspecting contents; SSH key removal confirmed with the maintainer)
- Fixed a compile-breaking bug in `change_xxx.pl` (missing closing brace in a hash literal)
- Fixed a copy-paste typo in `street.cgi` (an example URL from a comment had been copied into a live conditional)
- Removed a duplicate, broken definition of `checkProxyList` in `sub/bbslog.pl` that was shadowing the correct version in `etc/bbspass.pl`
- Fixed 89 instances of a stray backslash byte before certain double-byte CP932 characters ending in 0x5C, left over from an old mojibake workaround
- Fixed `require` failures under Perl 5.26+ (`.` no longer in `@INC`) in `bbs.cgi`, `i.cgi`, `nazo777.cgi`, and `tree.cgi` via `FindBin`/`use lib`
- Disabled use of the third-party `jcode.pl` library (fatal `defined(%hash)` error under modern Perl) by commenting out all `require` call sites; library files themselves were kept, not deleted
- Removed standard-library dependencies (`CGI.pm` in `bookquery.cgi`, `CGI::Carp` in `tree.cgi`) for standalone operation
- Applied vulnerability 2 fix (stale `$1` reuse via `$FORM{'ff'}`) across `bbs.txt`, `i.txt`, `nazo777.txt`, and `zbbs.cgi`: explicit `unless` checks, 2-argument → 3-argument `open()`
- Confirmed vulnerability 3 (attribute-value XSS) had already been mitigated on the ＠暫定 side at the time
- Converted 77 files from CP932 to UTF-8 with no decoding errors; replaced 37 `charset` meta tags from Shift_JIS to UTF-8
- Left `up/Readme_Shicyan.html` (third-party, already UTF-8) untouched
