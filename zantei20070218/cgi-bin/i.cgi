#!/usr/bin/perl
# 変更する場合: ##!/usr/local/bin/perl

# [2026-07-18] Perl 5.26以降、カレントディレクトリ'.'が既定で@INCから除外されたため、拡張子なしのrequireが失敗する。明示的にlib追加で対応（猫）
use FindBin;
use lib $FindBin::Bin;
require "i.txt";

exit;


__END__
