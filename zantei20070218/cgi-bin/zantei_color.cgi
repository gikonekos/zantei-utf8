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
#$script_url = "http://strange00.hp.infoseek.co.jp/cgi-bin/zantei_color.cgi";
$script_url = "http://www.ge.st98.arena.ne.jp/cgi-bin/zantei_color.cgi";

# 掲示板に戻るURL
$backbbs_url = "http://www.ge.st98.arena.ne.jp/cgi-bin/bbs.cgi";

# 参考表示のhtml
$colorchange_example_html = <<EXAMPLE_EOF;
  参考

┌───┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
│＼    │ 0  │ 1  │ 2  │ 3  │ 4  │ 5  │ 6  │ 7  │ 8  │ 9  │ w  │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│ｼx ■ │ ｼ0 │ ｼ1 │ ｼ2 │ ｼ3 │ ｼ4 │ ｼ5 │ ｼ6 │ ｼ7 │ ｼ8 │ ｼ9 │ ｼw │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│ﾏx ● │ ﾏ0 │ ﾏ1 │ ﾏ2 │ ﾏ3 │ ﾏ4 │ ﾏ5 │ ﾏ6 │ ﾏ7 │ ﾏ8 │ ﾏ9 │ ﾏw │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│ﾜx ▼ │ ﾜ0 │ ﾜ1 │ ﾜ2 │ ﾜ3 │ ﾜ4 │ ﾜ5 │ ﾜ6 │ ﾜ7 │ ﾜ8 │ ﾜ9 │ ﾜw │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│ｻx ▲ │ ｻ0 │ ｻ1 │ ｻ2 │ ｻ3 │ ｻ4 │ ｻ5 │ ｻ6 │ ｻ7 │ ｻ8 │ ｻ9 │ ｻw │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│ﾋx ◆ │ ﾋ0 │ ﾋ1 │ ﾋ2 │ ﾋ3 │ ﾋ4 │ ﾋ5 │ ﾋ6 │ ﾋ7 │ ﾋ8 │ ﾋ9 │ ﾋw │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│ﾎx ★ │ ﾎ0 │ ﾎ1 │ ﾎ2 │ ﾎ3 │ ﾎ4 │ ﾎ5 │ ﾎ6 │ ﾎ7 │ ﾎ8 │ ﾎ9 │ ﾎw │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│ﾁx 旦 │ ﾁ0 │ ﾁ1 │ ﾁ2 │ ﾁ3 │ ﾁ4 │ ﾁ5 │ ﾁ6 │ ﾁ7 │ ﾁ8 │ ﾁ9 │ ﾁw │
└───┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘

┌───┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
│H＼L■│ x0 │ x1 │ x2 │ x3 │ x4 │ x5 │ x6 │ x7 │ x8 │ x9 │ xa │ xb │ xc │ xd │ xe │ xf │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│   ｱx │ ｱ0 │ ｱ1 │ ｱ2 │ ｱ3 │ ｱ4 │ ｱ5 │ ｱ6 │ ｱ7 │ ｱ8 │ ｱ9 │ ｱa │ ｱb │ ｱc │ ｱd │ ｱe │ ｱf │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│   ｲx │ ｲ0 │ ｲ1 │ ｲ2 │ ｲ3 │ ｲ4 │ ｲ5 │ ｲ6 │ ｲ7 │ ｲ8 │ ｲ9 │ ｲa │ ｲb │ ｲc │ ｲd │ ｲe │ ｲf │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│   ｳx │ ｳ0 │ ｳ1 │ ｳ2 │ ｳ3 │ ｳ4 │ ｳ5 │ ｳ6 │ ｳ7 │ ｳ8 │ ｳ9 │ ｳa │ ｳb │ ｳc │ ｳd │ ｳe │ ｳf │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│   ｴx │ ｴ0 │ ｴ1 │ ｴ2 │ ｴ3 │ ｴ4 │ ｴ5 │ ｴ6 │ ｴ7 │ ｴ8 │ ｴ9 │ ｴa │ ｴb │ ｴc │ ｴd │ ｴe │ ｴf │
└───┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘

  おんぷたん
  うさだ
  ぷちこ
  でじこ
  ぴよこ

  ↓

┌───┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
│＼    │ 0  │ 1  │ 2  │ 3  │ 4  │ 5  │ 6  │ 7  │ 8  │ 9  │ w  │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│ｼx ■ │ <FONT color=black>■</FONT> │ <FONT color=dodgerblue>■</FONT> │ <FONT color=crimson>■</FONT> │ <FONT color=deeppink>■</FONT> │ <FONT color=forestgreen>■</FONT> │ <FONT color=teal>■</FONT> │ <FONT color=gold>■</FONT> │ <FONT color=orange>■</FONT> │ <FONT color=peachpuff>■</FONT> │ <FONT color=darkgray>■</FONT> │ <FONT color=silver>■</FONT> │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│ﾏx ● │ <FONT color=black>●</FONT> │ <FONT color=dodgerblue>●</FONT> │ <FONT color=crimson>●</FONT> │ <FONT color=deeppink>●</FONT> │ <FONT color=forestgreen>●</FONT> │ <FONT color=teal>●</FONT> │ <FONT color=gold>●</FONT> │ <FONT color=orange>●</FONT> │ <FONT color=peachpuff>●</FONT> │ <FONT color=darkgray>●</FONT> │ <FONT color=silver>●</FONT> │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│ﾜx ▼ │ <FONT color=black>▼</FONT> │ <FONT color=dodgerblue>▼</FONT> │ <FONT color=crimson>▼</FONT> │ <FONT color=deeppink>▼</FONT> │ <FONT color=forestgreen>▼</FONT> │ <FONT color=teal>▼</FONT> │ <FONT color=gold>▼</FONT> │ <FONT color=orange>▼</FONT> │ <FONT color=peachpuff>▼</FONT> │ <FONT color=darkgray>▼</FONT> │ <FONT color=silver>▼</FONT> │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│ｻx ▲ │ <FONT color=black>▲</FONT> │ <FONT color=dodgerblue>▲</FONT> │ <FONT color=crimson>▲</FONT> │ <FONT color=deeppink>▲</FONT> │ <FONT color=forestgreen>▲</FONT> │ <FONT color=teal>▲</FONT> │ <FONT color=gold>▲</FONT> │ <FONT color=orange>▲</FONT> │ <FONT color=peachpuff>▲</FONT> │ <FONT color=darkgray>▲</FONT> │ <FONT color=silver>▲</FONT> │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│ﾋx ◆ │ <FONT color=black>◆</FONT> │ <FONT color=dodgerblue>◆</FONT> │ <FONT color=crimson>◆</FONT> │ <FONT color=deeppink>◆</FONT> │ <FONT color=forestgreen>◆</FONT> │ <FONT color=teal>◆</FONT> │ <FONT color=gold>◆</FONT> │ <FONT color=orange>◆</FONT> │ <FONT color=peachpuff>◆</FONT> │ <FONT color=darkgray>◆</FONT> │ <FONT color=silver>◆</FONT> │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│ﾎx ★ │ <FONT color=black>★</FONT> │ <FONT color=dodgerblue>★</FONT> │ <FONT color=crimson>★</FONT> │ <FONT color=deeppink>★</FONT> │ <FONT color=forestgreen>★</FONT> │ <FONT color=teal>★</FONT> │ <FONT color=gold>★</FONT> │ <FONT color=orange>★</FONT> │ <FONT color=peachpuff>★</FONT> │ <FONT color=darkgray>★</FONT> │ <FONT color=silver>★</FONT> │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│ﾁx 旦 │ <FONT color=black>旦</FONT> │ <FONT color=dodgerblue>旦</FONT> │ <FONT color=crimson>旦</FONT> │ <FONT color=deeppink>旦</FONT> │ <FONT color=forestgreen>旦</FONT> │ <FONT color=teal>旦</FONT> │ <FONT color=gold>旦</FONT> │ <FONT color=orange>旦</FONT> │ <FONT color=peachpuff>旦</FONT> │ <FONT color=darkgray>旦</FONT> │ <FONT color=silver>旦</FONT> │
└───┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘

┌───┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
│H＼L■│ x0 │ x1 │ x2 │ x3 │ x4 │ x5 │ x6 │ x7 │ x8 │ x9 │ xa │ xb │ xc │ xd │ xe │ xf │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│   ｱx │ <FONT color=#7F7F7F>■</FONT> │ <FONT color=#0000FF>■</FONT> │ <FONT color=#0000BF>■</FONT> │ <FONT color=#472BBF>■</FONT> │ <FONT color=#970087>■</FONT> │ <FONT color=#AB0023>■</FONT> │ <FONT color=#AB1300>■</FONT> │ <FONT color=#8B1700>■</FONT> │ <FONT color=#533000>■</FONT> │ <FONT color=#007800>■</FONT> │ <FONT color=#006B00>■</FONT> │ <FONT color=#005B00>■</FONT> │ <FONT color=#004358>■</FONT> │ <FONT color=#000001>■</FONT> │ <FONT color=#000002>■</FONT> │ <FONT color=#000000>■</FONT> │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│   ｲx │ <FONT color=#BFBFBF>■</FONT> │ <FONT color=#0078F8>■</FONT> │ <FONT color=#0058F8>■</FONT> │ <FONT color=#6B47FF>■</FONT> │ <FONT color=#DB00CD>■</FONT> │ <FONT color=#E7005B>■</FONT> │ <FONT color=#F83800>■</FONT> │ <FONT color=#E75F13>■</FONT> │ <FONT color=#AF7F00>■</FONT> │ <FONT color=#00B800>■</FONT> │ <FONT color=#00AB00>■</FONT> │ <FONT color=#00AB47>■</FONT> │ <FONT color=#008B8B>■</FONT> │ <FONT color=#000003>■</FONT> │ <FONT color=#000004>■</FONT> │ <FONT color=#000005>■</FONT> │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│   ｳx │ <FONT color=#F8F8F8>■</FONT> │ <FONT color=#3FBFFF>■</FONT> │ <FONT color=#6B88FF>■</FONT> │ <FONT color=#9878F8>■</FONT> │ <FONT color=#F878F8>■</FONT> │ <FONT color=#F85898>■</FONT> │ <FONT color=#F87858>■</FONT> │ <FONT color=#FFA347>■</FONT> │ <FONT color=#F8B800>■</FONT> │ <FONT color=#B8F818>■</FONT> │ <FONT color=#5BDB57>■</FONT> │ <FONT color=#58F898>■</FONT> │ <FONT color=#00EBDB>■</FONT> │ <FONT color=#787878>■</FONT> │ <FONT color=#000006>■</FONT> │ <FONT color=#000007>■</FONT> │
├───┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
│   ｴx │ <FONT color=#FFFFFF>■</FONT> │ <FONT color=#A7E7FF>■</FONT> │ <FONT color=#B8B8F8>■</FONT> │ <FONT color=#D8B8F8>■</FONT> │ <FONT color=#F8B8F8>■</FONT> │ <FONT color=#FBA7C3>■</FONT> │ <FONT color=#F0D0B0>■</FONT> │ <FONT color=#FFE3AB>■</FONT> │ <FONT color=#FBDB7B>■</FONT> │ <FONT color=#D8F878>■</FONT> │ <FONT color=#B8F8B8>■</FONT> │ <FONT color=#B8F8D8>■</FONT> │ <FONT color=#00FFFF>■</FONT> │ <FONT color=#F8D8F8>■</FONT> │ <FONT color=#000008>■</FONT> │ <FONT color=#000009>■</FONT> │
└───┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘

  <FONT color=VIOLET>おんぷたん</FONT>
  <FONT color=PINK>うさだ</FONT>
  <FONT color=YELLOW>ぷちこ</FONT>
  <FONT color=LIGHTSEAGREEN>でじこ</FONT>
  <FONT color=DARKORCHID>ぴよこ</FONT>
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
$fchangeddata


  <A href="$backbbs_url">掲示板に戻る</A> / <A href="$script_url?f=$fsize">やり直す</A>

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

$colorchange_example_html

  <A href="$backbbs_url">掲示板に戻る</A>

</PRE>
</BODY>
</HTML>

HTML_EOF

}

exit;
