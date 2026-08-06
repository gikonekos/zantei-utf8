#!/usr/bin/perl
# 変更する場合: ##!/usr/local/bin/perl

# 特殊変換
# 今のところファミコン色変換とか ｻ1 とかの変換

#
# 単純変換データ
#
# q[ｱx] => q[■], とか書くと逆変換の時に「■」が「ｱx」に置換されるので注意。
# 不可逆な変換等は下方のchange_to_xxx/change_from_xxxの中に直接書くこと。
#
# ======ここから============================================================
my %xxx_data = (
# ファミコン $00 - $0f
	q[ｱ0] => q[<FONT color=#7F7F7F>■</FONT>],
	q[ｱ1] => q[<FONT color=#0000FF>■</FONT>],
	q[ｱ2] => q[<FONT color=#0000BF>■</FONT>],
	q[ｱ3] => q[<FONT color=#472BBF>■</FONT>],

	q[ｱ4] => q[<FONT color=#970087>■</FONT>],
	q[ｱ5] => q[<FONT color=#AB0023>■</FONT>],
	q[ｱ6] => q[<FONT color=#AB1300>■</FONT>],
	q[ｱ7] => q[<FONT color=#8B1700>■</FONT>],

	q[ｱ8] => q[<FONT color=#533000>■</FONT>],
	q[ｱ9] => q[<FONT color=#007800>■</FONT>],
	q[ｱa] => q[<FONT color=#006B00>■</FONT>],
	q[ｱb] => q[<FONT color=#005B00>■</FONT>],

	q[ｱc] => q[<FONT color=#004358>■</FONT>],
	q[ｱd] => q[<FONT color=#000000>■</FONT>],
	q[ｱe] => q[<FONT color=#000001>■</FONT>],
	q[ｱf] => q[<FONT color=#000002>■</FONT>],

# ファミコン $10 - $1f
	q[ｲ0] => q[<FONT color=#BFBFBF>■</FONT>],
	q[ｲ1] => q[<FONT color=#0078F8>■</FONT>],
	q[ｲ2] => q[<FONT color=#0058F8>■</FONT>],
	q[ｲ3] => q[<FONT color=#6B47FF>■</FONT>],

	q[ｲ4] => q[<FONT color=#DB00CD>■</FONT>],
	q[ｲ5] => q[<FONT color=#E7005B>■</FONT>],
	q[ｲ6] => q[<FONT color=#F83800>■</FONT>],
	q[ｲ7] => q[<FONT color=#E75F13>■</FONT>],

	q[ｲ8] => q[<FONT color=#AF7F00>■</FONT>],
	q[ｲ9] => q[<FONT color=#00B800>■</FONT>],
	q[ｲa] => q[<FONT color=#00AB00>■</FONT>],
	q[ｲb] => q[<FONT color=#00AB47>■</FONT>],

	q[ｲc] => q[<FONT color=#008B8B>■</FONT>],
	q[ｲd] => q[<FONT color=#000003>■</FONT>],
	q[ｲe] => q[<FONT color=#000004>■</FONT>],
	q[ｲf] => q[<FONT color=#000005>■</FONT>],

# ファミコン $20 - $2f
	q[ｳ0] => q[<FONT color=#F8F8F8>■</FONT>],
	q[ｳ1] => q[<FONT color=#3FBFFF>■</FONT>],
	q[ｳ2] => q[<FONT color=#6B88FF>■</FONT>],
	q[ｳ3] => q[<FONT color=#9878F8>■</FONT>],

	q[ｳ4] => q[<FONT color=#F878F8>■</FONT>],
	q[ｳ5] => q[<FONT color=#F85898>■</FONT>],
	q[ｳ6] => q[<FONT color=#F87858>■</FONT>],
	q[ｳ7] => q[<FONT color=#FFA347>■</FONT>],

	q[ｳ8] => q[<FONT color=#F8B800>■</FONT>],
	q[ｳ9] => q[<FONT color=#B8F818>■</FONT>],
	q[ｳa] => q[<FONT color=#5BDB57>■</FONT>],
	q[ｳb] => q[<FONT color=#58F898>■</FONT>],

	q[ｳc] => q[<FONT color=#00EBDB>■</FONT>],
	q[ｳd] => q[<FONT color=#787878>■</FONT>],
	q[ｳe] => q[<FONT color=#000006>■</FONT>],
	q[ｳf] => q[<FONT color=#000007>■</FONT>],

# ファミコン $30 - $3f
	q[ｴ0] => q[<FONT color=#FFFFFF>■</FONT>],
	q[ｴ1] => q[<FONT color=#A7E7FF>■</FONT>],
	q[ｴ2] => q[<FONT color=#B8B8F8>■</FONT>],
	q[ｴ3] => q[<FONT color=#D8B8F8>■</FONT>],

	q[ｴ4] => q[<FONT color=#F8B8F8>■</FONT>],
	q[ｴ5] => q[<FONT color=#FBA7C3>■</FONT>],
	q[ｴ6] => q[<FONT color=#F0D0B0>■</FONT>],
	q[ｴ7] => q[<FONT color=#FFE3AB>■</FONT>],

	q[ｴ8] => q[<FONT color=#FBDB7B>■</FONT>],
	q[ｴ9] => q[<FONT color=#D8F878>■</FONT>],
	q[ｴa] => q[<FONT color=#B8F8B8>■</FONT>],
	q[ｴb] => q[<FONT color=#B8F8D8>■</FONT>],

	q[ｴc] => q[<FONT color=#00FFFF>■</FONT>],
	q[ｴd] => q[<FONT color=#F8D8F8>■</FONT>],
	q[ｴe] => q[<FONT color=#000008>■</FONT>],
	q[ｴf] => q[<FONT color=#000009>■</FONT>],

# 旧・色変換 ■
	q[ｼ0] => q[<FONT color=black>■</FONT>],
	q[ｼ1] => q[<FONT color=dodgerblue>■</FONT>],
	q[ｼ2] => q[<FONT color=crimson>■</FONT>],
	q[ｼ3] => q[<FONT color=deeppink>■</FONT>],
	q[ｼ4] => q[<FONT color=forestgreen>■</FONT>],
	q[ｼ5] => q[<FONT color=teal>■</FONT>],
	q[ｼ6] => q[<FONT color=gold>■</FONT>],
	q[ｼ7] => q[<FONT color=orange>■</FONT>],
	q[ｼ8] => q[<FONT color=mistyrose>■</FONT>],
	q[ｼ9] => q[<FONT color=gray>■</FONT>],
	q[ｼw] => q[<FONT color=silver>■</FONT>],

# 旧・色変換 ●
	q[ﾏ0] => q[<FONT color=black>●</FONT>],
	q[ﾏ1] => q[<FONT color=dodgerblue>●</FONT>],
	q[ﾏ2] => q[<FONT color=crimson>●</FONT>],
	q[ﾏ3] => q[<FONT color=deeppink>●</FONT>],
	q[ﾏ4] => q[<FONT color=forestgreen>●</FONT>],
	q[ﾏ5] => q[<FONT color=teal>●</FONT>],
	q[ﾏ6] => q[<FONT color=gold>●</FONT>],
	q[ﾏ7] => q[<FONT color=orange>●</FONT>],
	q[ﾏ8] => q[<FONT color=mistyrose>●</FONT>],
	q[ﾏ9] => q[<FONT color=gray>●</FONT>],
	q[ﾏw] => q[<FONT color=silver>●</FONT>],

# 旧・色変換 ▲
	q[ｻ0] => q[<FONT color=black>▲</FONT>],
	q[ｻ1] => q[<FONT color=dodgerblue>▲</FONT>],
	q[ｻ2] => q[<FONT color=crimson>▲</FONT>],
	q[ｻ3] => q[<FONT color=deeppink>▲</FONT>],
	q[ｻ4] => q[<FONT color=forestgreen>▲</FONT>],
	q[ｻ5] => q[<FONT color=teal>▲</FONT>],
	q[ｻ6] => q[<FONT color=gold>▲</FONT>],
	q[ｻ7] => q[<FONT color=orange>▲</FONT>],
	q[ｻ8] => q[<FONT color=mistyrose>▲</FONT>],
	q[ｻ9] => q[<FONT color=gray>▲</FONT>],
	q[ｻw] => q[<FONT color=silver>▲</FONT>],

# 旧・色変換 ▼
	q[ﾜ0] => q[<FONT color=black>▼</FONT>],
	q[ﾜ1] => q[<FONT color=dodgerblue>▼</FONT>],
	q[ﾜ2] => q[<FONT color=crimson>▼</FONT>],
	q[ﾜ3] => q[<FONT color=deeppink>▼</FONT>],
	q[ﾜ4] => q[<FONT color=forestgreen>▼</FONT>],
	q[ﾜ5] => q[<FONT color=teal>▼</FONT>],
	q[ﾜ6] => q[<FONT color=gold>▼</FONT>],
	q[ﾜ7] => q[<FONT color=orange>▼</FONT>],
	q[ﾜ8] => q[<FONT color=mistyrose>▼</FONT>],
	q[ﾜ9] => q[<FONT color=gray>▼</FONT>],
	q[ﾜw] => q[<FONT color=silver>▼</FONT>],

# 旧・色変換 ◆
	q[ﾋ0] => q[<FONT color=black>◆</FONT>],
	q[ﾋ1] => q[<FONT color=dodgerblue>◆</FONT>],
	q[ﾋ2] => q[<FONT color=crimson>◆</FONT>],
	q[ﾋ3] => q[<FONT color=deeppink>◆</FONT>],
	q[ﾋ4] => q[<FONT color=forestgreen>◆</FONT>],
	q[ﾋ5] => q[<FONT color=teal>◆</FONT>],
	q[ﾋ6] => q[<FONT color=gold>◆</FONT>],
	q[ﾋ7] => q[<FONT color=orange>◆</FONT>],
	q[ﾋ8] => q[<FONT color=mistyrose>◆</FONT>],
	q[ﾋ9] => q[<FONT color=gray>◆</FONT>],
	q[ﾋw] => q[<FONT color=silver>◆</FONT>],

# 旧・色変換 ★
	q[ﾎ0] => q[<FONT color=black>★</FONT>],
	q[ﾎ1] => q[<FONT color=dodgerblue>★</FONT>],
	q[ﾎ2] => q[<FONT color=crimson>★</FONT>],
	q[ﾎ3] => q[<FONT color=deeppink>★</FONT>],
	q[ﾎ4] => q[<FONT color=forestgreen>★</FONT>],
	q[ﾎ5] => q[<FONT color=teal>★</FONT>],
	q[ﾎ6] => q[<FONT color=gold>★</FONT>],
	q[ﾎ7] => q[<FONT color=orange>★</FONT>],
	q[ﾎ8] => q[<FONT color=mistyrose>★</FONT>],
	q[ﾎ9] => q[<FONT color=gray>★</FONT>],
	q[ﾎw] => q[<FONT color=silver>★</FONT>],

# 旧・色変換 旦
	q[ﾁ0] => q[<FONT color=black>旦</FONT>],
	q[ﾁ1] => q[<FONT color=dodgerblue>旦</FONT>],
	q[ﾁ2] => q[<FONT color=crimson>旦</FONT>],
	q[ﾁ3] => q[<FONT color=deeppink>旦</FONT>],
	q[ﾁ4] => q[<FONT color=forestgreen>旦</FONT>],
	q[ﾁ5] => q[<FONT color=teal>旦</FONT>],
	q[ﾁ6] => q[<FONT color=gold>旦</FONT>],
	q[ﾁ7] => q[<FONT color=orange>旦</FONT>],
	q[ﾁ8] => q[<FONT color=mistyrose>旦</FONT>],
	q[ﾁ9] => q[<FONT color=gray>旦</FONT>],
	q[ﾁw] => q[<FONT color=silver>旦</FONT>],

# 初期・お茶変換
	q[oa!] => q[<FONT color=crimson>旦~</FONT>],
	q[ob!] => q[<FONT color=dodgerblue>旦~</FONT>],
	q[oc!] => q[<FONT color=orange>旦~</FONT>],
	q[od!] => q[<FONT color=deeppink>旦~</FONT>],
	q[oe!] => q[<FONT color=teal>旦~</FONT>],
	q[of!] => q[<FONT color=forestgreen>旦~</FONT>],
	q[og!] => q[<FONT color=gold>旦~</FONT>],

# 特定文字列
	q[おんぷたん] => q[<FONT color=VIOLET>おんぷたん</FONT>],
	q[うさだ] => q[<FONT color=PINK>うさだ</FONT>],
	q[ぷちこ] => q[<FONT color=yellow>ぷちこ</FONT>],
	q[でじこ] => q[<FONT color=green>でじこ</FONT>],
);

#業者URI(20060701)
# ======ここまで============================================================

# 処理用のパターン
my %xxx_back = map { $xxx_data{$_}, $_ } keys(%xxx_data);
my $xxx_data_pattern = "(?:" . join("|", map { quotemeta($_) } keys(%xxx_data)) . ")";
my $xxx_back_pattern = "(?:" . join("|", map { quotemeta($_) } keys(%xxx_back)) . ")";

# 特殊な変換を行う(色付けとか)
sub change_to_xxx {
	my($message) = @_;

	# %xxx_dataの分を変換 (SJIS対応済み)
	$message =~ s/($xxx_data_pattern)|([\x81-\x9f\xe0-\xfc].|.)/$1 ? $xxx_data{$1} : $2/geo;

	# その他の変換を行う場合はこの辺に記述する


	return $message;
}

# 特殊な変換を戻す(色付けとか)
sub change_from_xxx {
	my($message) = @_;

	# %xxx_dataの分を戻す
	$message =~ s/($xxx_back_pattern)/$xxx_back{$1}/go;

	# その他の変換を戻す場合はこの辺に記述する

	return $message;
}

# html関連の正規表現
my $xtag_rx_name = qr#[a-zA-Z0-9\.\_\:\-]+#;
my $xtag_rx_aval = qr#\s*=\s*(?:"[^"]*"|[^\s]*?)#;
my $xtag_rx_attr = qr#\s+$xtag_rx_name$xtag_rx_aval?#;

# タグ許可ルーチン
sub tag_change {
	my($message, $nazomode) = @_;

	if($nazomode) {
		# なぞモード

		# "と&を戻す
		$message =~ s#&quot;#"#go;
		$message =~ s#&amp;#&#go;
		# 画像展開
		$message =~ s#<A href="([^"]*(?:jpg|jpeg|png|gif))" target="link">(.*?)</A>#<IMG src="$1">#goi;
		# タグっぽいものをタグに戻す
		$message =~ s#&lt;(/?$xtag_rx_name$xtag_rx_attr*\s*/?)&gt;#<$1>#gos;
	} else {
		# 通常モード
		# (未実装)
	}

	return $message;
}

1;

__END__
