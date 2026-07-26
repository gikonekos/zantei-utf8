#! /usr/local/bin/perl

# jcode.plのパス
# [2026-07-18] jcode.pl不使用化（スタンドアロン方針、猫）
#require './jcode.pl';

# CGIを設置するホストアドレス
$bbshost = 'www.ge.st98.arena.ne.jp';

# このスクリプトの名前
$mycginame = 'gikonekoadd.cgi';

# タイトル
$title = '擬古猫といっしょ 投稿画面';

# データファイル名
$data = './neko/gikoneko_kotoba.dat';

# ことばのmax値
$maxword = 128;#128なら全角で64文字



&prterror ( '呼び出し元が不正です。' )
  if ( $ENV{'HTTP_HOST'} ne '' && ! ( $ENV{'HTTP_HOST'} =~ /$bbshost/i ) );

if ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN,$buffer,$ENV{'CONTENT_LENGTH'}); } else { $buffer = $ENV{'QUERY_STRING'}; }

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

if (($FORM{'mode'} eq 'add') && ($FORM{'text'} ne '')) {
	open ( IN, "$data" );
	@fortunedata = <IN>;
	close ( IN );
	for ( 0 .. @fortunedata ) { &prterror ( 'すでに登録されています。' ) if ( "$FORM{'text'}\n" eq $fortunedata[$_] ); }
	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";
	print "<BODY bgcolor=\"#004040\" text=\"#ffffff\" link=\"#eeffee\" vlink=\"#dddddd\" alink=\"#ff0000\">\n";
	print "<h1><a href=\"$mycginame\">書き込み完了</a><p></h1><a href=\"./bbs.cgi\">掲示板に戻る</a>\n";
	print "</body></html>\n";
	open ( ADD, ">>$data" );
		print ADD "$FORM{'text'}\n";
	close ( ADD );
} else {
	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";
	print "<BODY bgcolor=\"#004040\" text=\"#ffffff\" link=\"#eeffee\" vlink=\"#dddddd\" alink=\"#ff0000\"><center>\n";
	print "<p><font size=\"+2\"><B>$title</B></font><br>\n";
	print "<P>擬古猫に喋らせたい言葉を書いてください（半角$maxword文字まで）</p>\n";
	print "<form method=\"post\" action=\"$mycginame\">\n";
	print "<input type=\"hidden\" name=\"mode\" value=\"add\">\n";
	print "<input type=\"text\" name=\"text\" size=\"30\" maxlength=\"$maxword\">\n";
	print "<input type=\"submit\" value=\"ことばを教える\" accesskey=\"R\">\n";
	print " <INPUT type=\"reset\" value=\"消す\">\n";
	print "</form><p><a href=\"./bbs.cgi\" >掲示板に戻る</a></center></body></html>\n";
}

exit;

sub prterror {
	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";
	print "<body bgcolor=\"004040\" text=\"ffffff\">\n";
	print "<h3>$_[0]</h3>\n";
	print "</body></html>\n";
	exit;
}

