#! /usr/local/bin/perl

# 引数にジャンプ先のURLを与えてください
# ↓は使用例です(設置URLがhttp://www.ge.st98.arena.ne.jp/cgi-bin/r.cgiの場合)
#http://www.ge.st98.arena.ne.jp/cgi-bin/r.cgi?http://tools.geocities.co.jp/cgi-bin/homestead/hood_addr?Bookend-Ango1250
#待ち時間
$wait = 3;

&decode;
&html if($buffer);
&error;

sub html{

print "Content-type: text/html\n\n";
print <<"_HTML_";
<HTML><HEAD>
<TITLE>$bufferにジャンプ</TITLE>
<meta http-equiv=refresh content="$wait; url=$buffer">
<body bgcolor="#004040" text="#ffffff" link="#eeffee" vlink="#dddddd"
alink="#ff0000">
$wait秒後に自動的に飛ばない場合は<br>
<input size="99" type="text" name="l" maxlength="255" value="$buffer"><br>
をブラウザのアドレス欄にコピーアンドペーストしてください<br>
_HTML_
exit;
}#html END

sub decode{	#一般的なデコード＆変数への代入
	$buffer = $ENV{'QUERY_STRING'};
	$buffer =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$buffer =~ s/\n|\r//g;
}#decode END

sub error{
print "Content-type: text/html\n\n";
print <<"_HTML_";
<HTML><HEAD>
<TITLE>エラー</TITLE>
</HEAD>
エラー<br>
URLが指定されていません
</HTML>
_HTML_
exit;
}
