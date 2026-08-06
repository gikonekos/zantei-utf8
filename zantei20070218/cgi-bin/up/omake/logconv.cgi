#!/usr/bin/perl
# 変更する場合: ##!/usr/local/bin/perl
#
#  ずるぼんあぷろだからログ形式をコンバートするCGIスクリプト
#                                    （2000年9月3日版以降のバージョンに対応）
#
#
#  使い方
#  ・変換したいファイルと同じディレクトリに置いて実行します。
#  ・ファイルと先頭文字を指定し、変換ボタンを押してください。
#
#  ・対象ファイルとそのファイルが置かれているディレクトリのパーミッションを
#    書き込み可能な状態にする必要があります。
#  ・対象ファイル名に「.bak」を付加した名前でバックアップファイルを作成します。
#  ・実行にはTime::Localモジュールが必要です。たぶん標準で入ってると思いますが
#
#  変換はご自身の責任において行なってください
#
use strict;
my ($scriptname, $dir, $logtype);

# このスクリプトのURL
$scriptname = $ENV{SCRIPT_NAME};

# ログファイルがあるディレクトリ
$dir = '.';

# 変換対象のログ形式
#  0 : STRENGE UPLOADER 2002年11月17日版以前のログ形式
#  1 : ずるぼんあぷろだ
$logtype = 1;

# タイムゾーン
$ENV{TZ} = 'JST-9';


######################################################

sub getformdata {
	my $form = {};
	my $url_encoded_data;
	
	if ($ENV{'REQUEST_METHOD'} eq 'POST') {
		read ( STDIN, $url_encoded_data, $ENV{CONTENT_LENGTH} );
	} else {
		$url_encoded_data = $ENV{QUERY_STRING};
	}
	if ($url_encoded_data ne '') {
		$url_encoded_data =~ tr/+/ /;
		
		foreach my $pair ( split (/&/, $url_encoded_data) ) {
			my ($name, $value) =  split (/=/, $pair, 2);
			$name  =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
			$value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
			
			$value =~ s/&/&amp;/g;
			$value =~ s/</&lt;/g;
			$value =~ s/>/&gt;/g;
			$value =~ tr/\r\n//d;
			
			$form->{$name} = $value;
		}
	}
	return $form;
}


# ずるぼんあぷろだデータ
# id  suffix  comment  host  ua  date  size  mimetype  passwd  md5  dcrc  \n
# ・id は四桁の数字
# ・dateは2002年11/26(火)07:34のような形式
# ・削除禁止のときはpasswdに*
# ・sizeはキロバイト単位
# ・データはタブ区切り
sub conv_from_zurubon {
	require Time::Local;
	
	my $rl_fields = @_ > 1 ? shift : [];
	my ($line, $prefix) = @_;
	
	my @zurubon = split (/\t/, $line, -1);
	
	return undef if (@zurubon < 9);
	
	my ($id, $suffix, $comment, $host, $ua, $date, $size, $mimetype, $passwd) = @zurubon;
	my ($time, $filename);
	
	$filename = "$prefix$id.$suffix";
	$id += 0;	#数字の頭の0を取る
	$suffix =~ /^\w+$/ or return undef;
	
	$passwd = '' if ($passwd eq '*');
	
	$date =~ /^(\d+)年(\d+)\/(\d+)\(\S+?\)(\d+)\:(\d+)$/ or return undef;
	$time = Time::Local::timelocal(0, $5, $4, $3, $2-1, $1-1900);
	$size =~ /^\d+$/ or return undef;
	$size *= 1024;
	
	@$rl_fields = ($id, $suffix, $filename, $filename, $comment, $time, $size, $passwd, $host, $ua, $mimetype);
	
	$rl_fields;
}

# 旧: id  suffix  name  comment  time  size  passwd  host  ua  mimetype  \n
# 新: id  suffix  filename  dispname  comment  time  size  passwd  host  ua  mimetype  \n
# （データはタブ区切り）
sub conv_from_old_version {
	my $rl_fields = @_ > 1 ? shift : [];
	my ($line, $prefix) = @_;
	
	@$rl_fields = split (/\t/, $line, -1);
	
	return undef if (@$rl_fields != 10);
	
	my $filename = sprintf("%s%04d.%s", $prefix, $rl_fields->[0], $rl_fields->[1]);
	
	splice (@$rl_fields, 2, 0, $filename);
	
	$rl_fields;
}

sub logconv {
	my ($logfile, $prefix, $convertfunc) = @_;
	
#	print STDERR "$logfile のログ形式をコンバートします。\n";
	
	my @logdata = ();
	
	open (LOG, "$dir/$logfile") or &error("ログファイルの読み込みに失敗しました。($!)\n");
	eval{ flock (LOG, 1) };
	
	while (<LOG>) {
		chop;
		my @fields;
		
		&$convertfunc(\@fields, $_, $prefix)
			or &error("ログ形式が違うようです。コンバートを中止しました。\n");
		
		push (@logdata, join("\t", @fields) . "\n");
	}
	eval{ flock (LOG, 8) };
	close (LOG);
	
	rename ($logfile, "$logfile.bak") or &error("バックアップファイルの作成に失敗しました。($!)\n");
	
#	print STDERR "$logfile.bak にバックアップを取りました。\n";
	
	open (LOG, "> $logfile") or &error("ログファイルの書き込みに失敗しました。($!)\n");
	eval{ flock (LOG, 2) };
	print LOG @logdata;
	eval{ flock (LOG, 8) };
	close (LOG);
	
#	print STDERR "コンバート終了\n";
	
	&print_msg('', "コンバートは無事終わりました。\n");
}

sub print_html_header {
	my $title = shift || 'logconv';
	
	print <<_EOF;
Content-type: text/html; charset=UTF-8
Content-Language: ja

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>$title</title>
</head>
<body text="#ffffff" bgcolor="#004040" link="#eeffee" vlink="#dddddd" alink="#ff0000">
_EOF
}

sub html {
	
	&print_html_header();
	
	print <<_EOF;
<h2>ログコンバータ</h2>


<form method="POST" action="$scriptname">
<input type="hidden" name="act" value="confirm">

ファイルを選択してください。
<hr>
<table border="0" width="60%">
<tr>
  <th>File</th>
  <th>Size</th>
  <th>Last-Modified</th>
</tr>
_EOF
	
	opendir (DIR, $dir);
	my @files = sort {$a cmp $b} grep(!/^\.\.?$/, readdir (DIR));
	closedir (DIR);
	
	foreach my $file (@files) {
		next unless (-f "$dir/$file");
		my ($size, $mtime) = (stat(_))[7,9];
		
		my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($mtime);
		my $date = sprintf("%d/%02d/%02d %02d:%02d:%02d",
			$year+1900, $mon+1, $mday, $hour, $min, $sec);
		
		print<<_EOF
<tr>
  <td align="left"><input type="radio" name="fn" value="$file"> $file</td>
  <td align="right">$size byte</td>
  <td align="center">$date</td>
</tr>
_EOF
	}
	
	print <<_EOF;
</table>
<hr>

先頭文字 (\$prefix) <input type="text" name="prefix" size="8" value="up">　
<input type="submit" value="変換">

</form>

</body>
</html>
_EOF
}

sub confirm {
	my $formdata = shift;
	
	my $backup = $formdata->{fn} . '.bak';
	my $msg;
	
	if (-e "$dir/$backup") {
		$msg = qq|$backupを<font color="red">上書きして</font>バックアップファイルを作成します|;
	} else {
		$msg = qq|$backupにバックアップファイルを作成します|;
	}
	
	&print_html_header();
	
	my $prefix = $formdata->{prefix};
	$prefix = '<i>(無し)</i>' if ($prefix eq '');
	
	print <<_EOF;
<h2>ログコンバータ</h2>
<table border="0">
<tr><td nowrap>ファイル名</td><td nowrap>： $formdata->{fn}</td></tr>
<tr><td nowrap>先頭文字</td><td nowrap>： $prefix</td></tr>
<tr><td colspan="2">$msg</td></tr>
<tr><td colspan="2">よろしいですか？</td></tr>
</table>

<form method="POST" action="$scriptname">
<input type="hidden" name="act"    value="convert">
<input type="hidden" name="fn"     value="$formdata->{fn}">
<input type="hidden" name="prefix" value="$formdata->{prefix}">
<input type="submit" value="変換">

</form>
</body>
</html>
_EOF
	
}

# データチェック
sub datacheck {
	my $formdata = shift;
	($formdata->{fn}) = $formdata->{fn} =~ /^([^:\\\/|<>+&]+)$/;
	
#	&error("先頭文字が入力されていません。\n") if ($formdata->{prefix} eq '');
	&error("ファイルが選択されていません。\n") if ($formdata->{fn} eq '');
	&error("ファイルが存在しません。\n") unless (-f "$dir/$formdata->{fn}");
	&error("ファイルに読み込み属性がありません。\n") unless (-r _);
	&error("ファイルに書き込み属性がありません。\n") unless (-w _);
	&error("ディレクトリに書き込み属性が無いためバックアップファイルが作成できません。\n")
		unless (-w $dir);
}


# エラー処理
sub error { &print_msg('ERROR', @_); }

sub print_msg {
	my $title  = shift;
	my $errmsg = join('', @_);
	
	&print_html_header($title);
	
	print <<_EOF;
<p><big><strong>$errmsg</strong></big></p>
<hr>
<a href="$scriptname">戻る</a>
</body>
</html>
_EOF
	exit;
}


Main: {
	my $formdata = &getformdata();
	my $act = $formdata->{act};
	
	if ($act eq 'confirm') {
		&datacheck($formdata);
		&confirm($formdata);
	} elsif ($act eq 'convert') {
		&datacheck($formdata);
		my $f = $logtype ? \&conv_from_zurubon : \&conv_from_old_version;
		&logconv($formdata->{fn}, $formdata->{prefix}, $f);
	} else {
		&html();
	}
	exit;
}

