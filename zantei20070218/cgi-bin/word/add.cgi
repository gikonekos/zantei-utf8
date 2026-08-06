#!/usr/bin/perl
# 変更する場合: ##!/usr/local/bin/perl

# jcode.plのパス
# [2026-07-18] jcode.pl不使用化（スタンドアロン方針、猫）
#require '../jcode.pl';

# CGIを設置するホストアドレス
$bbshost = 'www.ge.st98.arena.ne.jp';

# このスクリプトの名前
$mycginame = 'add.cgi';

# タイトル
$title = 'リンク登録';

# データファイル名
$data = 'link.dat';

# ことばのmax値

$maxword_t = 12;#128なら全角で64文字
$maxword_c = 128;#128なら全角で64文字
$maxword_u = 256;#128なら全角で64文字

###########################################
&prterror ( '呼び出し元が不正です。' ) if ( $ENV{'HTTP_HOST'} ne '' && ! ( $ENV{'HTTP_HOST'} =~ /$bbshost/i ) );

###########################################
if ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN,$buffer,$ENV{'CONTENT_LENGTH'}); } else { $buffer = $ENV{'QUERY_STRING'}; }

###########################################
@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {
	($name, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$value =~ s/</&lt;/g;
	$value =~ s/>/&gt;/g;
	$value =~ s/"/&quot;/g;#style対策
	$value =~ s/\n//g;
	$value =~ s/\r//g;
	$FORM{$name} = $value;
}

###########################################

$text = $FORM{'t'};
$comment = $FORM{'c'};
$url = $FORM{'u'};
$convdata="<a href=\"$url\">$text</a>:$comment";

$wdate = &getnowdate ( $ndate );

###########################################


if (($FORM{'mode'} eq 'add') && ($FORM{'t'} ne '') && ($FORM{'c'} ne '') && ($FORM{'u'} ne '') && ($FORM{'regist'} ne '')) {

	for ( 0 .. @linkdata ) { &prterror ( 'すでに登録されています。' ) if ( "$FORM{'t'}\n" eq $linkdata[$_] ); }

	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";

	print "<BODY bgcolor=\"#004040\" text=\"#ffffff\" link=\"#eeffee\" vlink=\"#dddddd\" alink=\"#ff0000\">\n";
	print "<h1><a href=\"$mycginame\">書き込み完了</a><p></h1><a href=\"./bbs.cgi\">掲示板に戻る</a>\n";

	print "</body></html>\n";
	open ( ADD, ">>$data" );


		print ADD "$FORM{'t'}\,$FORM{'c'}\,$FORM{'u'}\,0\n";

	close ( ADD );
} else {
	print <<EOF;
Content-type: text/html

<html><head><title>$title</title></head>
<BODY bgcolor="#004040" text="#ffffff" link="#eeffee" vlink="#dddddd" alink="#ff0000">
<p><font size="+2"><B>$title</B></font><br>
<P>投稿</p>
<form method="post" action="$mycginame">
<input type="hidden" name="mode" value="add">
名<input  type="text" value="$text" name="t" size="20" maxlength="$maxword_t">
コメント<input type="textbox" value="$comment" name="c" size="30" maxlength="$maxword_c"><BR>
ＵＲＬ<input type="text" value="$url" name="u" size="30" maxlength="$maxword_u"><BR>
<input type="submit" value="作成" accesskey="R">
<INPUT type="reset" value="消す">
<HR>
$convdata $buffer
<HR>
<input type="submit" name="regist" value="登録" accesskey="R">
<HR>
</form><p><a href="./bbs.cgi" >掲示板に戻る</a>
</body></html>
EOF
}
exit;

###########################################

sub prterror {
	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";
	print "<body bgcolor=\"004040\" text=\"ffffff\">\n";
	print "<h3>$_[0]</h3>\n";
	print "</body></html>\n";
	exit;
}

###########################################


###############################################################################
#  時刻フォーマット変換
###############################################################################

sub getnowdate {

	( $sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdat )
		= localtime ( $_[0] );
	$year += 1900;
	$mon++;
	$nowdate = sprintf ( "%d/%02d/%02d(%s)%02d時%02d分%02d秒",
	  $year, $mon, $mday,
	  ( '日', '月', '火', '水', '木', '金', '土' )[$wday],
	  $hour, $min, $sec );
}

###########################################
