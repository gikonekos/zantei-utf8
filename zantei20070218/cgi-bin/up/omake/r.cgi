#! /usr/local/bin/perl
#
# りだいれくたー
#
# 使用方法
#   r.cgi?転送先URL で呼び出す
#
my $url = $ENV{QUERY_STRING} || "http://$ENV{SERVER_NAME}/";
$url =~ s/&/&amp;/g;
$url =~ s/</&lt;/g;
$url =~ s/>/&gt;/g;

print <<_EOF;
Content-Type: text/html; charset=UTF-8
Content-Language: ja

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<meta http-equiv="Content-type" content="text/html; charset=UTF-8">
<meta http-equiv="Refresh" content="0;URL=$url">
<title>りだいれくたー</title>
</head>

<body bgcolor="#004040" text="#ffffff" link="#eeffee" vlink="#dddddd" alink="#ff0000">
<p>
 $url に転送中ε＝Ξヽ(´ー｀)ノ
</p>
</body>
</html>
_EOF
