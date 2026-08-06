# Changelog

Summary of changes made in the zantei-utf8 project, relative to the original `zantei20070218` server image.

## 2026-08-06

- Made `GD` an optional dependency in `mojie/aa.pl` (the mojie image-to-AA feature): replaced the compile-time `use GD;` with a runtime `our $HAS_GD = eval { require GD; 1 } ? 1 : 0;`, and added an early guard in `image2asciiart` that returns the existing `(undef, ..., $errmsg)` failure tuple with a "GD not installed" message when GD is unavailable (no change needed at the single call site in `mojie.cgi`, which already displays `$errmsg`). With this, the entire suite runs on a bare Perl install with no CPAN/XS modules; GD is now only required by installers who want the image-to-AA conversion
- Removed the hardcoded `use lib '/home/ax160/lib/i386-freebsd';` line from `mojie/aa.pl` — a FreeBSD-specific absolute path from the original hosting environment that would break on any other host
- Unified shebang line to `#!/usr/bin/perl` across all `.cgi` and `.pl` files (40 files); added a comment on the following line `# 変更する場合: ##!/usr/local/bin/perl` so the alternative path is documented but cannot be accidentally executed (double `#` neutralises the shebang); removed two Windows-path shebang lines (`#! c:/online/perl/bin/perl`) that had been left as a second line in `dlist.cgi` and `sub/index.cgi`
- Added `ttp://`/`ttps://` display-time link conversion in `prtmessage` of `bbs.txt`, `zbbs.cgi`, and `nazo777.txt`: rewritten as `<A href="http(s)://...">ttp://...</A>` at render time without modifying the stored log; lookbehind `(?<![hH"'])` prevents conversion inside existing HTML attribute values (e.g. in nazo/tag-permit mode) and avoids double-converting `http(s)://`; motivated by the community convention of writing `ttp://` to deter URL-pasting spam and bots
- Fixed vulnerability 4 (dangerous URL scheme injection via `$FORM{'l'}`) in `bbs.txt`, `i.txt`, `nazo777.txt`, and `zbbs.cgi`: replaced the previous `javascript/i` keyword check (which could be bypassed via `vbscript:`, `data:`, leading whitespace, etc., and broke `&xx;` character references by converting `:` to a fullwidth colon) with a whitelist approach that only allows `https?://` and `ftp://` prefixes; any other value is cleared to an empty string

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
