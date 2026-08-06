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

## Related Projects

| Repository | Relationship |
|------------|-------------|
| [kuzuhascript-utf8](https://github.com/gikonekos/kuzuhascript-utf8) | Parallel modernization of the original kuzuhascript codebase (Perl, CP932→UTF-8) |
| [kuzuhascript-archive](https://github.com/gikonekos/kuzuhascript-archive) | Historical archive of original kuzuhascript distribution files |
| [legacy-bbs-toolkit](https://github.com/gikonekos/legacy-bbs-toolkit) | Preprocessing toolkit for legacy Japanese BBS archives |
| [ksphp-plus-gikonekos](https://github.com/gikonekos/ksphp-plus-gikonekos) | PHP successor in the same BBS tradition |

## Requirements

Perl 5.38 or later. No CPAN or XS modules are required for core functionality.

**Optional:** The [`GD`](https://metacpan.org/pod/GD) module (CPAN/XS, requires libgd) is needed only for the mojie image-to-AA conversion feature (`mojie/aa.pl`). Without GD, all other features work normally; the image-to-AA feature returns a "GD not installed" message.

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

| リポジトリ | 関係 |
|------------|------|
| [kuzuhascript-utf8](https://github.com/gikonekos/kuzuhascript-utf8) | くずはすくりぷと原本を対象とした並行モダナイズプロジェクト |
| [kuzuhascript-archive](https://github.com/gikonekos/kuzuhascript-archive) | くずはすくりぷと配布ファイルの歴史的アーカイブ |
| [legacy-bbs-toolkit](https://github.com/gikonekos/legacy-bbs-toolkit) | 旧日本語BBSアーカイブの前処理ツールキット |
| [ksphp-plus-gikonekos](https://github.com/gikonekos/ksphp-plus-gikonekos) | 同じBBS文化の流れを汲むPHP後継プロジェクト |

## 動作要件

Perl 5.38以降。コア機能の利用にCPAN/XSモジュールの追加導入は不要です。

**オプション：** [`GD`](https://metacpan.org/pod/GD)モジュール（CPAN/XS、libgd必須）は、文字絵の画像変換機能（`mojie/aa.pl`）を使う場合のみ必要です。GDが未導入の場合でも他の全機能は正常に動作します（画像変換時に「GDが導入されていません」旨のメッセージを返します）。

## 変更履歴

このプロジェクトでの変更点のサマリーは[doc/changelog.md](doc/changelog.md)を参照してください。

---

## Installation / 導入方法

### English

1. Clone or download this repository.
2. Upload the contents of `zantei20070218/cgi-bin/` to your server's CGI directory.
3. Set executable permissions (`chmod 755`) on all `.cgi` files.
4. Edit `bbsset.txt` to match your environment. Key settings:

| Variable | Description | Default |
|----------|-------------|---------|
| `$bbshost` | Hostname or IP of your server | `example.com` ← **change this** |
| `$gzip` | Path to gzip binary (leave empty to disable compression) | `''` |
| `$logfilename` | Path to the log file | `./bbs.log` |
| `$countfile` | Path prefix for counter files | `./count/count` |
| `$logsave` | Number of messages to retain | `2000` |
| `$difftime` | Time offset from JST in hours (0 = Japan) | `0` |
| `$protect_a` | Anti-double-post code part A — **change before deployment** | sample value |
| `$protect_b` | Anti-double-post code part B — **change before deployment** | sample value |

5. If you want the mojie image-to-AA conversion feature, install the `GD` module (see Requirements above). Otherwise all other features work without it.

---

### 日本語

1. このリポジトリをクローンまたはダウンロードします。
2. `zantei20070218/cgi-bin/` の中身をサーバーのCGIディレクトリにアップロードします。
3. すべての `.cgi` ファイルに実行権限（`chmod 755`）を設定します。
4. `bbsset.txt` を環境に合わせて編集します。主な設定項目：

| 変数 | 説明 | デフォルト |
|------|------|-----------|
| `$bbshost` | サーバーのホスト名またはIPアドレス | `example.com` ← **要変更** |
| `$gzip` | gzip バイナリのパス（空のままで圧縮転送無効） | `''` |
| `$logfilename` | ログファイルのパス | `./bbs.log` |
| `$countfile` | カウンターファイルのパスの先頭部分 | `./count/count` |
| `$logsave` | 保持するメッセージ数 | `2000` |
| `$difftime` | JSTとの時差（0＝日本） | `0` |
| `$protect_a` | 連続投稿防止コードA — **導入前に必ず変更** | サンプル値 |
| `$protect_b` | 連続投稿防止コードB — **導入前に必ず変更** | サンプル値 |

5. 文字絵の画像変換機能（mojie）を使う場合は `GD` モジュールを導入してください（上記「動作要件」参照）。それ以外の機能はGDなしで動作します。
