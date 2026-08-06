#!/usr/bin/perl
# 変更する場合: ##!/usr/local/bin/perl

# zantei_color.cgi

# jcode.pl
# [2026-07-18] jcode.pl不使用化（スタンドアロン方針、猫）
#require "./jcode.pl";

# http://yasashiku.site.ne.jp/up/stored/yukarin2048.zip の change_xxx.pl
# または &change_to_xxx(処理前の文字列)   で色付き変換しreturn
# 　　　 &change_from_xxx(処理前の文字列) で元に戻しreturn する関数
require "./change_xxx.txt";

# cgiのURL
#$script_url = "http://strange00.hp.infoseek.co.jp/cgi-bin/zantei_color2.cgi";
$script_url = "http://www.ge.st98.arena.ne.jp/cgi-bin/zantei_color2.cgi";

# 掲示板に戻るURL
$backbbs_url = "http://www.ge.st98.arena.ne.jp/cgi-bin/bbs.cgi";

# 参考表示のhtml
$colorchange_example_html = <<EXAMPLE_EOF;

  参考

       0 1 2 3 4 5 6 7 8 9 w        0 1 2 3 4 5 6 7 8 9 a b c d e f          0 1 2 3 4 5 6 7 8 9 w        0 1 2 3 4 5 6 7 8 9 a b c d e f
ｼx ■ ｼ0ｼ1ｼ2ｼ3ｼ4ｼ5ｼ6ｼ7ｼ8ｼ9ｼw    ｱx ｱ0ｱ1ｱ2ｱ3ｱ4ｱ5ｱ6ｱ7ｱ8ｱ9ｱaｱbｱcｱdｱeｱf   ｼx ■ <FONT color=black>■</FONT><FONT color=dodgerblue>■</FONT><FONT color=crimson>■</FONT><FONT color=deeppink>■</FONT><FONT color=forestgreen>■</FONT><FONT color=teal>■</FONT><FONT color=gold>■</FONT><FONT color=orange>■</FONT><FONT color=mistyrose>■</FONT><FONT color=gray>■</FONT><FONT color=silver>■</FONT>    ｱx <FONT color=#7F7F7F>■</FONT><FONT color=#0000FF>■</FONT><FONT color=#0000BF>■</FONT><FONT color=#472BBF>■</FONT><FONT color=#970087>■</FONT><FONT color=#AB0023>■</FONT><FONT color=#AB1300>■</FONT><FONT color=#8B1700>■</FONT><FONT color=#533000>■</FONT><FONT color=#007800>■</FONT><FONT color=#006B00>■</FONT><FONT color=#005B00>■</FONT><FONT color=#004358>■</FONT><FONT color=#000000>■</FONT><FONT color=#000001>■</FONT><FONT color=#000002>■</FONT>
ﾏx ● ﾏ0ﾏ1ﾏ2ﾏ3ﾏ4ﾏ5ﾏ6ﾏ7ﾏ8ﾏ9ﾏw    ｲx ｲ0ｲ1ｲ2ｲ3ｲ4ｲ5ｲ6ｲ7ｲ8ｲ9ｲaｲbｲcｲdｲeｲf   ﾏx ● <FONT color=black>●</FONT><FONT color=dodgerblue>●</FONT><FONT color=crimson>●</FONT><FONT color=deeppink>●</FONT><FONT color=forestgreen>●</FONT><FONT color=teal>●</FONT><FONT color=gold>●</FONT><FONT color=orange>●</FONT><FONT color=mistyrose>●</FONT><FONT color=gray>●</FONT><FONT color=silver>●</FONT>    ｲx <FONT color=#BFBFBF>■</FONT><FONT color=#0078F8>■</FONT><FONT color=#0058F8>■</FONT><FONT color=#6B47FF>■</FONT><FONT color=#DB00CD>■</FONT><FONT color=#E7005B>■</FONT><FONT color=#F83800>■</FONT><FONT color=#E75F13>■</FONT><FONT color=#AF7F00>■</FONT><FONT color=#00B800>■</FONT><FONT color=#00AB00>■</FONT><FONT color=#00AB47>■</FONT><FONT color=#008B8B>■</FONT><FONT color=#000003>■</FONT><FONT color=#000004>■</FONT><FONT color=#000005>■</FONT>
ﾜx ▼ ﾜ0ﾜ1ﾜ2ﾜ3ﾜ4ﾜ5ﾜ6ﾜ7ﾜ8ﾜ9ﾜw    ｳx ｳ0ｳ1ｳ2ｳ3ｳ4ｳ5ｳ6ｳ7ｳ8ｳ9ｳaｳbｳcｳdｳeｳf   ﾜx ▼ <FONT color=black>▼</FONT><FONT color=dodgerblue>▼</FONT><FONT color=crimson>▼</FONT><FONT color=deeppink>▼</FONT><FONT color=forestgreen>▼</FONT><FONT color=teal>▼</FONT><FONT color=gold>▼</FONT><FONT color=orange>▼</FONT><FONT color=mistyrose>▼</FONT><FONT color=gray>▼</FONT><FONT color=silver>▼</FONT>    ｳx <FONT color=#F8F8F8>■</FONT><FONT color=#3FBFFF>■</FONT><FONT color=#6B88FF>■</FONT><FONT color=#9878F8>■</FONT><FONT color=#F878F8>■</FONT><FONT color=#F85898>■</FONT><FONT color=#F87858>■</FONT><FONT color=#FFA347>■</FONT><FONT color=#F8B800>■</FONT><FONT color=#B8F818>■</FONT><FONT color=#5BDB57>■</FONT><FONT color=#58F898>■</FONT><FONT color=#00EBDB>■</FONT><FONT color=#787878>■</FONT><FONT color=#000006>■</FONT><FONT color=#000007>■</FONT>
ｻx ▲ ｻ0ｻ1ｻ2ｻ3ｻ4ｻ5ｻ6ｻ7ｻ8ｻ9ｻw    ｴx ｴ0ｴ1ｴ2ｴ3ｴ4ｴ5ｴ6ｴ7ｴ8ｴ9ｴaｴbｴcｴdｴeｴf   ｻx ▲ <FONT color=black>▲</FONT><FONT color=dodgerblue>▲</FONT><FONT color=crimson>▲</FONT><FONT color=deeppink>▲</FONT><FONT color=forestgreen>▲</FONT><FONT color=teal>▲</FONT><FONT color=gold>▲</FONT><FONT color=orange>▲</FONT><FONT color=mistyrose>▲</FONT><FONT color=gray>▲</FONT><FONT color=silver>▲</FONT>    ｴx <FONT color=#FFFFFF>■</FONT><FONT color=#A7E7FF>■</FONT><FONT color=#B8B8F8>■</FONT><FONT color=#D8B8F8>■</FONT><FONT color=#F8B8F8>■</FONT><FONT color=#FBA7C3>■</FONT><FONT color=#F0D0B0>■</FONT><FONT color=#FFE3AB>■</FONT><FONT color=#FBDB7B>■</FONT><FONT color=#D8F878>■</FONT><FONT color=#B8F8B8>■</FONT><FONT color=#B8F8D8>■</FONT><FONT color=#00FFFF>■</FONT><FONT color=#F8D8F8>■</FONT><FONT color=#000008>■</FONT><FONT color=#000009>■</FONT>
ﾋx ◆ ﾋ0ﾋ1ﾋ2ﾋ3ﾋ4ﾋ5ﾋ6ﾋ7ﾋ8ﾋ9ﾋw                                          ﾋx ◆ <FONT color=black>◆</FONT><FONT color=dodgerblue>◆</FONT><FONT color=crimson>◆</FONT><FONT color=deeppink>◆</FONT><FONT color=forestgreen>◆</FONT><FONT color=teal>◆</FONT><FONT color=gold>◆</FONT><FONT color=orange>◆</FONT><FONT color=mistyrose>◆</FONT><FONT color=gray>◆</FONT><FONT color=silver>◆</FONT>
ﾎx ★ ﾎ0ﾎ1ﾎ2ﾎ3ﾎ4ﾎ5ﾎ6ﾎ7ﾎ8ﾎ9ﾎw                                          ﾎx ★ <FONT color=black>★</FONT><FONT color=dodgerblue>★</FONT><FONT color=crimson>★</FONT><FONT color=deeppink>★</FONT><FONT color=forestgreen>★</FONT><FONT color=teal>★</FONT><FONT color=gold>★</FONT><FONT color=orange>★</FONT><FONT color=mistyrose>★</FONT><FONT color=gray>★</FONT><FONT color=silver>★</FONT>
ﾁx 旦 ﾁ0ﾁ1ﾁ2ﾁ3ﾁ4ﾁ5ﾁ6ﾁ7ﾁ8ﾁ9ﾁw                                          ﾁx 旦 <FONT color=black>旦</FONT><FONT color=dodgerblue>旦</FONT><FONT color=crimson>旦</FONT><FONT color=deeppink>旦</FONT><FONT color=forestgreen>旦</FONT><FONT color=teal>旦</FONT><FONT color=gold>旦</FONT><FONT color=orange>旦</FONT><FONT color=mistyrose>旦</FONT><FONT color=gray>旦</FONT><FONT color=silver>旦</FONT>
                                                                      
  おんぷたん                                                            <FONT color=VIOLET>おんぷたん</FONT>
  うさだ                                                                <FONT color=PINK>うさだ</FONT>
  ぷちこ                                                                <FONT color=YELLOW>ぷちこ</FONT>
  でじこ                                                                <FONT color=LIGHTSEAGREEN>でじこ</FONT>
  ぴよこ                                                                <FONT color=DARKORCHID>ぴよこ</FONT>

<a href="/source/zcoloraco.lzh">PhotoShop用 色見本ダウンロード<br>
<img src="/source/zcoloraco.gif" border="0" alt="色見本">
</a>

                                                                      
EXAMPLE_EOF

#--------------------------------------------------------------------

if($ENV{'REQUEST_METHOD'} eq 'POST'){
	read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	$printmode = 2; # result
}else{
	$buffer = $ENV{'QUERY_STRING'};
	$printmode = 1; # form
}
@pairs = split(/&/,$buffer);
foreach $pair (@pairs){
	($name, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
#	&jcode'convert(*value,'sjis');
	$value =~ s/&/&amp;/g;
	$value =~ s/\"/&quot;/g;
	$value =~ s/</&lt;/g;
	$value =~ s/>/&gt;/g;
	$form{$name} = $value;
}

# textarea
$formdata_n = $form{'v'};
$formdata_t = $form{'v'};

# formsize
$formsize = $form{'f'};
$formsize = 1 if($formsize eq "");
if($formsize == 2){
	$formsize_cols = 110; # 横サイズ
	$formsize_rows = 50;  # 行数
	$formsize_changehtml = "<A href=\"$script_url?f=1\">普通の大きさに戻す</A>";
}else{
	$formsize_cols = 70;  # 横サイズ
	$formsize_rows = 25;  # 行数
	$formsize_changehtml = "<A href=\"$script_url?f=2\">大きいサイズで描く</A>";
}

# 表示
if($printmode == 2){
	$formdata_changed = &change_to_xxx($formdata_t);
	&changeout($formsize,$formsize_cols,$formsize_rows,$formdata_n,$formdata_changed);
	exit;
}else{
	&formprint($formsize,$formsize_cols,$formsize_rows,$formsize_changehtml);
	exit;
}

exit;

#--------------------------------------------------------------------

# 結果表示
sub changeout{
	local($fsize,$fcols,$frows,$folddata,$fchangeddata) = @_;
	print "Content-type: text/html\n\n";
	print <<HTML_EOF;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">

<HTML>

<HEAD>
<TITLE>暫定カラーチェッカ 結果\表\示</TITLE>
</HEAD>

<BODY bgcolor="#004040" text="#ffffff" link="#eeffee" vlink="#dddddd" alink="#ff0000">

<PRE>

  結果\表\示

</PRE>

<FORM method="post" action="$script_url">
<TEXTAREA rows="$frows" cols="$fcols" wrap="off" name="v">$folddata</TEXTAREA>
<INPUT type="hidden" name="f" value="$fsize"><BR>
&nbsp;&nbsp;<INPUT type="submit" value="プレビュー">

<PRE>

<hr>
$fchangeddata
<hr>

  <A href="$backbbs_url">掲示板に戻る</A> / <A href="$script_url?f=$fsize">やり直す</A>

$colorchange_example_html

</PRE>

</BODY>
</HTML>

HTML_EOF

}

# フォームを表示
sub formprint{
	local($fsize,$fcols,$frows,$fschtml) = @_;
	print "Content-type: text/html\n\n";
	print <<HTML_EOF;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">

<HTML>

<HEAD>
<TITLE>暫定カラーチェッカ</TITLE>
</HEAD>

<BODY bgcolor="#004040" text="#ffffff" link="#eeffee" vlink="#dddddd" alink="#ff0000">

<PRE>

  暫定カラーチェッカ $fschtml

</PRE>

<FORM method="post" action="$script_url">
<TEXTAREA rows="$frows" cols="$fcols" wrap="off" name="v"></TEXTAREA>
<INPUT type="hidden" name="f" value="$fsize"><BR>
&nbsp;&nbsp;<INPUT type="submit" value="プレビュー">
</FORM>

<PRE>

  <A href="$backbbs_url">掲示板に戻る</A>

$colorchange_example_html

</PRE>
</BODY>
</HTML>

HTML_EOF

}

exit;
