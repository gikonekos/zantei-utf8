# zantei-utf8

A UTF-8 conversion, security hardening, and modern Perl (5.38+) compatibility update for the CGI script set of a preserved server image (`zantei20070218`) from あやしいわーるど＠暫定, a 2002–2007 Japanese textboard community. The original scripts are based on kuzuhascript Rev.0.1 Preview 9 (2000, by kuzuha), as modified by the ＠暫定 community over the years.

This project follows a strict "do not alter the archive" (アーカイブは弄らない) principle: only the CGI script set itself is modified for continued operability. No community-generated content (posts, logs) is included or altered.

## What this is

- Original: kuzuhascript Rev.0.1 Preview 9 (2000, kuzuha)
- Base image: zantei20070218, as customized by the あやしいわーるど＠暫定 community (2002–2007)
- This project: CP932→UTF-8 conversion, security fixes, and Perl 5.38+ compatibility fixes, preserving original behavior and folder structure

## License

The script set is released under the MIT License — see [LICENSE.md](LICENSE.md).
Character-art (AA) assets by 擬古猫 are released separately under AAAPS — see [gikonekos/aaaps](https://github.com/gikonekos/aaaps).
Copyright layers and contributor credits are listed in [NOTICE.md](NOTICE.md).

## Related projects

- [kuzuhascript-utf8](https://github.com/gikonekos/kuzuhascript-utf8) — a parallel modernization of the original kuzuhascript codebase (Perl, CP932→UTF-8)

## Changelog

See [doc/changelog.md](doc/changelog.md) for a summary of changes made in this project.

---

# zantei-utf8（日本語）

あやしいわーるど＠暫定（2002〜2007年、日本のテキスト掲示板コミュニティ）で運用されていたサーバーイメージ（`zantei20070218`）のCGIスクリプト群を対象とした、UTF-8化・脆弱性対策・モダンPerl（5.38以降）対応プロジェクトです。元となるスクリプトは、くずはすくりぷと Rev.0.1 Preview 9（2000年、くずは氏作）を、＠暫定コミュニティが年月をかけて改造したものです。

本プロジェクトは「アーカイブは弄らない」の原則を厳守し、稼働継続に必要なCGIスクリプト本体のみを対象とします。コミュニティが生成したコンテンツ（投稿・ログ等）は一切含まれず、改変もしていません。

## これは何か

- 原本：くずはすくりぷと Rev.0.1 Preview 9（2000年、くずは氏）
- ベースイメージ：zantei20070218（あやしいわーるど＠暫定コミュニティによる改造版、2002〜2007年）
- 本プロジェクトの内容：CP932→UTF-8変換、脆弱性対策、Perl 5.38以降への対応（元の動作・フォルダ構造は維持）

## ライセンス

スクリプト本体はMITライセンスで公開します。詳細は[LICENSE.md](LICENSE.md)を参照してください。
擬古猫による文字絵（AA）素材は別途AAAPSライセンスで公開しています（[gikonekos/aaaps](https://github.com/gikonekos/aaaps)参照）。
著作権表記の階層および貢献者クレジットは[NOTICE.md](NOTICE.md)に記載しています。

## 関連プロジェクト

- [kuzuhascript-utf8](https://github.com/gikonekos/kuzuhascript-utf8) — くずはすくりぷと原本を対象とした並行モダナイズプロジェクト（Perl、CP932→UTF-8）

## 変更履歴

このプロジェクトでの変更点のサマリーは[doc/changelog.md](doc/changelog.md)を参照してください。
