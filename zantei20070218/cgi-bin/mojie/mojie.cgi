#! /usr/local/bin/perl
use strict;
$SIG{__DIE__} = \&cgidie;

my (%C, $OwnName, %Form, @Uploaded);


%C = (
	#タイトル
	title  => 'もじえ',
	
	#画像データの一時保存ディレクトリ
	tempdir => './image',
	
	#画像データの保存期間
	temp_save => 5 * 60,
	
	#お掃除めも
	clean_dat => 'clean.dat',
	
	#画像データの最大サイズ (byte)
	max_image_size => 512 * 1024,
);


# フォームデータ取得
sub getFormdata {
	
	my ($url_encoded_data, $content_type, $content_length);
	
	$content_type   = $ENV{'CONTENT_TYPE'};
	$content_length = $ENV{'CONTENT_LENGTH'};
	
	if ($content_length > 4 * 1024 * 1024) {
		&cgidie("送信データ量が既定値を超えています。");
	}
	
	if ($content_type =~ m|multipart/form-data|) {
		require 'multipart.pl';
		@Uploaded = &multipart::get_multipart(\&storeFormdata, $C{tempdir});
	} elsif ( $content_type eq ''
		   or $content_type eq 'application/x-www-form-urlencoded') {
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
				
				&storeFormdata($name, $value);
			}
		}
	}
}

sub storeFormdata {
	
	my ($name, $value) = @_;
	
	# コントロール文字を削除
	$value =~ tr/\000-\010\013\014\020-\037\177//d;
	
	# 改行コードを統一する
	$value =~ s/\x0D\x0A/\n/g;
	$value =~ tr/\x0D\x0A/\n\n/;
	
	$value =~ s/&/&amp;/g;
	$value =~ s/"/&quot;/g;
	$value =~ s/</&lt;/g;
	$value =~ s/>/&gt;/g;
	
	$Form{$name} = $value;
}



##################################################
# HTMLヘッダ

my ($HEADER_SENT);
sub prtHeader {
	
	if ($HEADER_SENT) {
		return;
	}
	
	print <<_EOF;
Content-type: text/html; charset=UTF-8
Content-Language: ja

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta http-equiv="Content-Style-Type" content="text/css">
<title>$C{title}</title>
<style type="text/css"><!--
 BODY {
  margin: 8px 45px;
 }
 TEXTAREA {
  overflow-x: auto;
 }
--></style>
</head>
<body bgcolor="#004040" text="#ffffff" link="#eeffee" vlink="#dddddd" alink="#ff0000">
_EOF
	
	$HEADER_SENT = 1;
}



##################################################
# 文字絵変換

sub mojie {
	
	my ($up, $size, $imagetype, %options);
	
	%options = ();
	
	if (@Uploaded) {
		$up = $Uploaded[0];
		
		if ($up->{filesize} > $C{max_image_size}) {
			&cgidie("画像のサイズが大きすぎます。");
		}
		
		$imagetype = &getImageType($up);
		if (not defined($imagetype)) {
			&cgidie("アップロードされたファイルは画像と認識されませんでした。");
		} elsif ($imagetype ne 'png' and $imagetype ne 'jpg') {
			&cgidie("PNGとJPEGのみです。");
		}
		
		my $newname = time . '_' . $$ . '.' . $imagetype;
		rename ($up->{tmpfile}, "$C{tempdir}/$newname")
			or &cgidie ("画像のリネームに失敗しました。\n");
		
		$Form{temp} = $newname;
		$Form{name} = $up->{basename};
		
	} else {
		if ($Form{temp} ne '') {
			
			if (not $Form{temp} =~ /^[\d_]+\.(png|jpg)$/i) {
				&cgidie ("不正な値が入力されています。");
			}
			$imagetype = lc ($1);
			
			if (not -f "$C{tempdir}/$Form{temp}") {
				&cgidie ("画像データは削除されているようです。");
			}
			
			#更新日時を変更 (更新日時により画像の保存期間を管理する)
			my $now = time;
			utime ($now, $now, "$C{tempdir}/$Form{temp}");
			
			
			$Form{name} = $Form{temp} if ($Form{name} eq '');
			
		} else {
			return;
		}
	}
	
	$options{filename}  = "$C{tempdir}/$Form{temp}";
	$options{imagetype} = $imagetype;
	$options{pallet}    = $Form{pallet} if ($Form{pallet} ne '');
	$options{mark}      = $Form{mark}   if ($Form{mark} ne '');
	$options{cut_blank} = 1;
	
	if ($Form{resize} eq 'auto') {
		$options{resize} = 'auto';
	} elsif ($Form{resize} eq 'ratio') {
		if ($Form{ratio} !~ /^[\d\.\_]+$/) {
			&cgidie("縮小比率に数値でない値が入力されています。");
		}
		$options{resize} = $Form{ratio};
	} elsif ($Form{resize} eq 'manual') {
		if ($Form{w} !~ /^[\d\.\_]+$/ or $Form{h} !~ /^[\d\.\_]+$/) {
			&cgidie("縮小サイズに数値でない値が入力されています。");
		}
		$options{width}  = $Form{w};
		$options{height} = $Form{h};
	}
	
	
	require 'aa.pl';
	my ($textdata, $width, $height, $errmsg) = &image2asciiart(\%options);
	
	&prtHeader();
	
	if (not defined($textdata)) {
		print qq|<p style="margin: 1.5em"><font color="#F83800">$errmsg</font></p>\n|;
	} else {
		require 'change_xxx.pl';
		print "<pre>", &change_to_xxx($textdata), "</pre>\n";
		print <<_EOF;
横 $width × 縦 $height<br>
<form>
↓データ<br>
<textarea rows="4" cols="80" wrap="off">$textdata</textarea>
</form>
_EOF
	}
}

sub getImageType {
	
	my $up = shift;
	my (%mimetype, $type);
	
	%mimetype = (
		'bmp'	=> 'image/(?:x-(?:MS-)?)?bmp',
		'gif'	=> 'image/gif',
		'ico'	=> 'image/x-icon',
		'jpg'	=> 'image/.*jpeg',
		'mag'	=> 'image/.*mag',
		'png'	=> 'image/(?:x-)?png',
		'psd'	=> 'image/x-photoshop',
		'tif'	=> 'image/(?:x-)?tiff',
		'jpeg'  => '',
	);
	
	# MIMEタイプから
	while (my ($suffix, $mime) = each (%mimetype)) {
		if ($mime) {
			if ($up->{mimetype} =~ /$mime/i) {
				$type = $suffix;
				last;
			}
		}
	}
	
	# ローカルのファイル名の拡張子から
	if (not defined($type)) {
		if ($up->{basename} =~ /\.(\w+)$/) {
			if (exists ($mimetype{lc($1)})) {
				$type = lc ($1);
				$type = 'jpg' if ($type eq 'jpeg');
			}
		}
	}
	
	return ($type);
}



sub prtMainHTML {
	
	&prtHeader();
	
	my ($html_1, $html_2, $html_3, $html_4, @radiobox_1, @radiobox_2, @wh);
	$html_1 = '';
	$html_2 = '';
	$html_3 = '';
	$html_4 = '';
	if ($Form{temp} ne '') {
		$html_1 = qq|<a href="$C{tempdir}/$Form{temp}">$Form{name}</a> を処理中です。|;
		$html_2 .= qq|<input type="hidden" name="temp" value="$Form{temp}">\n|;
		$html_2 .= qq|<input type="hidden" name="name" value="$Form{name}">\n|;
		$html_3 = qq|<p><a href="$OwnName">やりなおし</a></p>|;
	} else {
		$html_1 = qq|<input type="file" name="upfile">&nbsp;&nbsp;を文字絵に変換します。|;
	}
	
	@radiobox_1 = ('','','');
	$radiobox_1[ $Form{resize} eq 'ratio' ? 1 : $Form{resize} eq 'manual' ? 2 : 0 ] = ' checked';
	
	@radiobox_2 = ('','','');
	$radiobox_2[ $Form{pallet} eq 'fam' ? 1 : $Form{pallet} eq 'old' ? 2 : 0 ] = ' checked';
	
	$html_4 .= qq|..<select name="mark">\n|;
	$html_4 .= qq| <option value="">記号</option>\n|;
	for (qw(■ ● ▲ ▼ ◆ ★ 旦)) {
		my $selected = ($Form{mark} eq $_) ? ' selected' : '';
		$html_4 .= qq| <option value="$_"$selected>$_</option>\n|;
	}
	$html_4 .= qq|</select>|;
	
	@wh = (48, 32);
	$wh[0] = $Form{w} if ($Form{w} ne '');
	$wh[1] = $Form{h} if ($Form{h} ne '');
	
	print <<_EOF;
<form action="$OwnName" method="POST" enctype="multipart/form-data">
<input type="hidden" name="m" value="mojie">
$html_2
<table border="0" cellpadding="4" cellspacing="0">
 <tbody>
  <tr>
   <td>
    <font color="#02ffff">画像：</font>
   </td>
   <td>
    $html_1
   </td>
  </tr>
  <tr>
   <td>
    <font color="#02ffff">縮小率：</font>
   </td>
   <td>
    自動<input type="radio" name="resize" value="auto"$radiobox_1[0]>
   </td>
  </tr>
  <tr>
   <td rowspan="2">&nbsp;</td>
   <td>
    比率<input type="radio" name="resize" value="ratio"$radiobox_1[1]>
    ..<input type="text" name="ratio" value="$Form{ratio}" size="4"> % （100%でpixel等倍）
    </select>
    </td>
  </tr>
  <tr>
   <td>
    指定<input type="radio" name="resize" value="manual"$radiobox_1[2]>
    ..横<input type="text" name="w" value="$wh[0]" size="4">桁 ／
      縦<input type="text" name="h" value="$wh[1]" size="4">行
   </td>
  </tr>
  <tr>
   <td>
    <font color="#02ffff">使用色：</font>
   </td>
   <td>
    すべて<input type="radio" name="pallet" value="all"$radiobox_2[0]>
   </td>
  </tr>
  <tr>
   <td rowspan="2">&nbsp;</td>
   <td>
    ファミコンカラー<input type="radio" name="pallet" value="fam"$radiobox_2[1]>
   </td>
  </tr>
  <tr>
   <td>
    旧・色変換<input type="radio" name="pallet" value="old"$radiobox_2[2]>
$html_4
   </td>
  </tr>
  <tr>
   <td colspan="2">
    <input type="submit" value="文字絵作成">
   </td>
  </tr>
 </tbody>
</table>
</form>

$html_3
<hr>

<ul>

 <li><small>PNGとJPEGが変換できます。GIF不可。</small></li>
 <li><small>横 150 桁、縦 150 行以内。</small></li>
 <li><small>画像はいったんアプすると文字絵作成後@{[ int($C{temp_save}/60) ]}分間はテンポラリが有効。</small></li>
</ul>
<hr>

<body>
</html>
_EOF

}


##################################################
# 画像データのお掃除

sub clean {
	
	my ($oldest, $time);
	
	$time = time;
	
	open (FILE, "+< $C{clean_dat}")
		or &cgidie("ファイルが開けませんでした。");
	eval {flock (FILE, 2)};
	
	chomp ($oldest = <FILE>);
	
	if ($oldest < $time - $C{temp_save}) {
		
		my (@files);
		$oldest = 0;
		
		opendir (DIR, $C{tempdir})
			or &cgidie("ディレクトリが開けませんでした。");
		@files = grep !/^\./, readdir (DIR);
		closedir (DIR);
		
		for (@files) {
			my ($mtime) = (stat ("$C{tempdir}/$_"))[9];
			
			if ($mtime < $time - $C{temp_save}) {
				unlink ("$C{tempdir}/$_");
				next;
			}
			$oldest = $mtime if ($oldest == 0 or $mtime < $oldest);
		}
	}
	
	truncate (FILE, 0);
	seek (FILE, 0, 0);
	print FILE $oldest;
	eval {flock (FILE, 8)};
	close (FILE);
}


##################################################
# エラー出力

sub cgidie {
	
	my $errmsg = join('', @_);
	
	&prtHeader();
	
    print <<_EOF;
<table border="0" cellpadding="5" cellspacing="5" width="90%">
 <tbody>
  <tr>
   <td align="left" valign="top">
    <h3><font color="#F83800">エラーが発生した為処理を中断しました。</font></h3>
    <p>詳細: $errmsg</p>
   </td>
  </tr>
 </tbody>
</table>
</body>
</html>
_EOF
	
	exit;
}


MainRoutine: {
	
	$OwnName = $ENV{SCRIPT_NAME} || ($0 =~ m|^(?:.*\/)?(.*)|, $1);
	
	&getFormdata();
	
	if ($Form{m} eq 'mojie') {
		
		&mojie();
		&prtMainHTML();
		
	} else {
		
		&prtMainHTML();
		
	}
	
	&clean();
	
}

