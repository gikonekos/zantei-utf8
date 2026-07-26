#! /usr/local/bin/perl
#
#　STRANGE UPLOADER     2002年12月23日版
#
$::COPYRIGHT = 'STRANGE UPLOADER (2002-12-23)';
#
#
#  初期設定はupload.initにあります。
#
#
# 【ファイル構成例】パーミッションは所有者権限でCGIが動く場合
#
#  [cgi-bin] (701) /
#      |
#      |-- upload.cgi         (700)
#      |-- upload.init        (600)
#      |-- style.css          (644)
#      |-- styleselector.js   (644)
#      |-- PaintBBS.jar       (644) (お絵描き機能使用時のみ)
#      |-- palette.js         (644) (お絵描き機能使用時のみ)
#      |-- shiihelp.html      (644) (お絵描き機能使用時のみ)
#      |
#      +-- [lib] (700) /
#      |     |
#      |     |-- multipart.pl (600)
#      |     |-- getpic.pl    (600) (お絵描き機能使用時のみ)
#      |     |-- imagesize.pl (600) (お絵描き機能使用時のみ)
#      |     |-- jcode.pl     (600)
#      |
#      +-- [data] (700) /
#      |     |
#      |     |-- upload.log   (600)
#      |     |-- admin.passwd (600)
#      |     |-- count.file   (600) (必要に応じて)
#      |     |-- renzoku.file (600) (必要に応じて)
#      |     |-- deny.file    (600) (必要に応じて)
#      |
#      +-- [stored] (701) /
#
#   ・掲示板初回起動時は管理者パスワード登録画面になります。
#   ・サーバを移転した時には「admin.passwd」を一端クリアしてください。
#
#
##################################################

# jcode.plなどのライブラリを別ディレクトリに置きたい時はここで指定
use lib './lib';

#use strict;
#our ($TITLE, $CGIURL, $BASE_URL, $LOG_FILE, $STORE_DIR, $STORE_URL, $INFORMATION, $LINK_BAR, $BANNER, @STYLESHEET, $BODY,
#	$PREFIX, $DEF_EXT, $LOCAL_FILENAME_SW, $MAX_UPLOAD_SIZE, $DISK_SPACE_MAX,
#	$LOGSAVE, $MSGDISP, $IMAGEDISP, $MAX_COMMENT_SIZE, $MIN_UPLOAD_SIZE,
#	$AUTOLINK, $COUNTFILE, $ADMINPASSWD,
#	$IP_REC, $UA_REC, $RENZOKU_FILE, $RENZOKU_TIME, $ACCESS_CONTROL, @EXCEPT_REFERER, $HTML_EXT,
#	$MAKE_INDEX_SW, $INDEX_FILEPATH, $OEKAKI_SW, $OEKAKI_MAX_SIZE, $OEKAKI_DEF_SIZE, $OEKAKI_ANIMATION, %APPLET_PARAMS,
#	$TMPDIR, %MIMETYPE, $MAX_FILENAME_SIZE, $MAX_PAGE_INDEX, $COOKIE_NAME, $MOJIBAKE_TAISAKU, $TEXT_BANNER,
#	%Form, %Cookie, @UploadFiles, @PictureFiles);

# 設定を読み込む
do './upload.init';
&cgidie('設定項目の記述に誤りがあります。', $@) if ($@);

$STORE_DIR =~ s|/$||;
$STORE_URL .= '/' unless ($STORE_URL =~ m|[\?\/]$|);	#gw.cgi?filename が使えるように
$BASE_URL  =~ s|/$||;
$TMPDIR    =~ s|/$||;

$SIG{__DIE__} = \&cgidie;


##################################################
# HTML上部下部

my $HeaderPrinted = 0;
sub print_header {
	
	my ($title, $is_indexpage) = @_;
	
	if (!$is_indexpage) {
		return if ($HeaderPrinted++);
	}
	
	$title = $title ? $TITLE.' - '.$title : $TITLE;
	$title =~ s/<.*?>//g;
	
	my $stylesheet = '';
	my $cssselector = '';
	if (@STYLESHEET > 2) {
		for (my $i = 0; $i < @STYLESHEET; $i +=2) {
			my $rel = $i == 0 ? 'stylesheet' : 'alternate stylesheet';
			$stylesheet .= qq|<link rel="$rel" type="text/css" href="$BASE_URL/$STYLESHEET[$i]" title="$STYLESHEET[$i+1]">\n|;
		}
		$stylesheet .= qq|<script type="text/javascript" src="$BASE_URL/styleselector.js" charset="UTF-8"></script>|;
		$cssselector = qq|<script type="text/javascript"><!--\n  writeCSSSelectForm("デザイン変更：");\n// --></script>|;
	} else {
		$stylesheet = qq|<link rel="stylesheet" type="text/css" href="$BASE_URL/$STYLESHEET[0]">|;
	}
	
	if (!$is_indexpage) {
		print <<_EOF;
Content-Type: text/html; charset=UTF-8
Content-Language: ja
Cache-Control: no-store, must-revalidate
Pragma: no-cache

_EOF
	}
	print <<_EOF;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="ja">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta http-equiv="Content-Script-Type" content="text/javascript">
$stylesheet
<title>$title</title>
</head>

$BODY
$cssselector
_EOF
}

sub print_obititle {
	my $title = @_ ? $TITLE.' - '.shift() : $TITLE;
	print <<_EOF;
<table width="100%" border="0" cellpadding="2" cellspacing="1" class="obi" summary="obi">
<tr><td><font size="4"><strong>$title</strong></font></td></tr></table>
<br>
_EOF
}

sub print_footer {
	my $applet = $OEKAKI_SW ?
	  qq|\nお絵描きアプレット <a href="http://www.gt.sakura.ne.jp/~ocosama/">PaintBBS (しぃちゃん)</a>| : '';
	print <<_EOF;
<hr>
<div align="right"><small>
<strong><a href="http://yasashiku.site.ne.jp/uploader/">$::COPYRIGHT</a></strong>
<!-- <small><a href="$CGIURL?help=disk">量</a></small> --><br>
$applet
</small></div>
$BANNER
</body>
</html>
_EOF
}


##################################################
# リスト表示

sub list {
	
	my $upload_limit = '';
	$upload_limit .= &byte_calc($MIN_UPLOAD_SIZE) . 'から ' if ($MIN_UPLOAD_SIZE);
	$upload_limit .= $MAX_UPLOAD_SIZE ? &byte_calc($MAX_UPLOAD_SIZE) . 'まで' : '無制限';
	
	print <<_EOF;
<p>$INFORMATION</p>
<form name="uploadform" method="POST" enctype="multipart/form-data" action="$CGIURL">
<a href="$CGIURL?help=file">ファイル</a><small><strong> （$upload_limit）</strong></small><br>
<input type="file" size="30" name="uploadfile">
<select name="suffix"><option value="" selected>特殊拡張子選択
_EOF
	
	for (sort keys(%MIMETYPE)) {
		next if ($HTML_EXT and /^htm/);
		print qq|<option value="$_">$_\n|;
	}
	
	my $cookie_ok_checked = %Cookie ? ' checked' : '';
	
	print <<_EOF;
</select><br>
コメント<br>
<input type="text" size="60" name="comment" value="">
<input type="submit" name="act" value="Up/Reload" class="button"><input type="reset" value="Cancel" class="button"><br>
<a href="$CGIURL?help=del">del pass</a>: <input type="password" size="10" name="delpass" maxlength="10" value="@{[&htmlencode($Cookie{delpass})]}">　
<input type="checkbox" name="cookie_ok" value="on" $cookie_ok_checked><small>パスワードをクッキーに保存</small>
_EOF
	if ($LOCAL_FILENAME_SW > 0) {
		print qq|<input type="checkbox" name="hidename" value="on"><small>ファイル名を隠す</small>\n|;
	}
	
	print <<_EOF;
<input type="hidden" name="page" value="$Form{page}">
<input type="hidden" name="lm"	 value="$Form{lm}">
<input type="hidden" name="sort" value="$Form{sort}">
<input type="hidden" name="rev"  value="$Form{rev}">
<input type="hidden" name="k"    value="$MOJIBAKE_TAISAKU">
</form>
_EOF
	
	# お絵描き機能
	if ($OEKAKI_SW) {
		my $anime_sw = $OEKAKI_ANIMATION ?
			qq|<input type="checkbox" name="anime" value="on" checked><small>アニメ記録</small>| : '';
		print <<_EOF;
<form method="GET" action="$CGIURL">
<input type="hidden" name="m" value="E">
横<select name="hsize">
_EOF
		for (my $i = 100; $i <= $OEKAKI_MAX_SIZE; $i+=50) {
			my $selected = $i == $OEKAKI_DEF_SIZE ? 'selected' : '';
			print qq|<option value="$i"$selected>$i\n|;
		}
		print qq|</select> ×\n縦<select name="vsize">\n|;
		for (my $i = 100; $i <= $OEKAKI_MAX_SIZE; $i+=50) {
			my $selected = $i == $OEKAKI_DEF_SIZE ? 'selected' : '';
			print qq|<option value="$i"$selected>$i\n|;
		}
		print <<_EOF;
</select> pixel
<input type="submit" value="お絵描きする" class="button">
$anime_sw
</form>

_EOF
	}
	
	print "<small>";
	if ($COUNTFILE ne ""){	# カウンタ
		print &counter(), "　\n";
	}
	print "D : ファイル削除　";
	print "A : 描画アニメ再生　" if ($OEKAKI_ANIMATION);
#	print "最大保存数：$LOGSAVE";
	print "</small>\n";
	
	print <<_EOF;
<hr><small>
 | <a href="$CGIURL?m=I">画像閲覧</a>
 | <a href="$CGIURL?m=S">ファイル検索</a>
$LINK_BAR |
</small>
_EOF
	
	open (LOG, $LOG_FILE) or die("Open Error $LOG_FILE: $!\n");
	eval{ flock (LOG, 1) };
	my @log = <LOG>;
	eval{ flock (LOG, 8) };
	close (LOG);
	
	my $sorttype = $Form{sort};
	my $rev      = $Form{rev};
	
	my ($page_index, $first_idx, $last_idx) = &page_index($#log, $MSGDISP, "sort=$sorttype&amp;rev=$rev");
	
	my @sorted = ();
	if ($sorttype or $rev) {
		if ($sorttype eq 'N') {
			my @keys = map { (split(/\t/, $_))[3] } @log;
			@sorted = sort {$keys[$b] cmp $keys[$a]} 0 .. $#log;
		} elsif ($sorttype eq 'S') {
			my @keys = map { (split(/\t/, $_))[6] } @log;
			@sorted = sort {$keys[$b] <=> $keys[$a]} 0 .. $#log;
		} else {
			@sorted = 0 .. $#log;
		}
		if ($rev) { @sorted = reverse @sorted; }
	}
	my %revurl = (N => '', S => '', D => '');
	$revurl{$sorttype||'D'} = '&amp;rev=' . ($rev ? 0 : 1);
	
	print <<_EOF;
<hr>
$page_index
<hr>
<table border="0" cellpadding="1" class="list" summary="list">
<tr>
  <th align="left">ACT</th>
  <th><a href="$CGIURL?page=$Form{page}&amp;lm=$Form{lm}&amp;sort=N$revurl{N}">NAME</a></th>
  <th>COMMENT</th>
  <th align="right"><a href="$CGIURL?page=$Form{page}&amp;lm=$Form{lm}&amp;sort=S$revurl{S}">SIZE(KB)</a></th>
  <th><a href="$CGIURL?page=$Form{page}&amp;lm=$Form{lm}&amp;sort=D$revurl{D}">DATE</a></th>
</tr>
_EOF
	
	my @indexes = @sorted ?
		@sorted[$first_idx..$last_idx] : $first_idx..$last_idx;
	
	foreach (@log[@indexes]) {
		&print_article($_, 0);
	}
	print "</table>\n";
	
	# 検索ボタン
	print <<_EOF;
<hr>
$page_index
<hr>
<form method="POST" action="$CGIURL" style="margin: 0px">
<a href="$CGIURL?help=search">検索</a>: <input type="text" size="25" name="kwd" value="">
<input type="submit" value="Search" class="button">
<input type="hidden" name="m" value="S">
<input type="hidden" name="k" value="$MOJIBAKE_TAISAKU">
</form>
_EOF

}


##################################################
# ページのリンクを表示

sub page_index {
	
	my ($total, $msgdisp, $urlquery) = @_;
	
	my ($page_index, $s, $e, $ss, $ee, $n);
	my $page = int($Form{page}) || 0;
	my $lm   = int($Form{lm})   || $msgdisp;
	
	my $half = int (($MAX_PAGE_INDEX - 1) / 2);
	$s = ($page > $half) ? $page - $half : 0;	# 開始ページ
	$n = int($total / $lm);						# 全ページ数
	# ページ数を調整
	if ($s + $MAX_PAGE_INDEX - 1 < $n) {
		$e = $s + $MAX_PAGE_INDEX - 1; $ee++;
	} else {
		$e = $n;
	}
	if ($e - $MAX_PAGE_INDEX - 1 > 0) {
		$s = $e - $MAX_PAGE_INDEX - 1; $ss++;
	}
	
	$page_index  = "<small>ページ：";
	$page_index .= "<strong><a href=\"$CGIURL?page=0&amp;lm=$lm&amp;$urlquery\">&lt;&lt;&lt; </a></strong> \n"
		if ($ss);
	$page_index .= "<strong><a href=\"$CGIURL?page=" . ($page-1) . "&amp;lm=$lm&amp;$urlquery\">前へ</a></strong> \n"
		if ($page - 1 >= 0);
	for (my $i = $s; $i <= $e; $i++) {
		my $pagenum = $i + 1;
		if ($i == $page) {
			$page_index .= "[ <strong>$pagenum</strong> ] \n";
		} else {
			$page_index .= qq|[<a href="$CGIURL?page=$i&amp;lm=$lm&amp;$urlquery">$pagenum</a>] \n|;
		}
	}
	if ($lm == $LOGSAVE) {
		$page_index .= "[<a href=\"$CGIURL?page=0&amp;lm=$msgdisp&amp;$urlquery\">NORM</a>] \n";
	} else {
		$page_index .= "[<a href=\"$CGIURL?page=0&amp;lm=$LOGSAVE&amp;$urlquery\">ALL</a>] \n";
	}
	$page_index .= "<strong><a href=\"$CGIURL?page=" . ($page+1) . "&amp;lm=$lm&amp;$urlquery\">次へ</a></strong> \n"
		if ($page + 1 <= $n);
	$page_index .= "<strong><a href=\"$CGIURL?page=$n&amp;lm=$lm&amp;$urlquery\">&gt;&gt;&gt; </a></strong> \n"
		if ($ee);
	$page_index .= "</small><br>\n";
	
	my $first_idx = ($total +1 < $lm) ? 0 : $page * $lm;
	my $last_idx = ($total < $first_idx+$lm-1) ? $total : $first_idx+$lm-1;
	
	return ($page_index, $first_idx, $last_idx);
}


##################################################
# 記事を一件表示する

sub print_article {
	
	my ($article, $isimageview) = @_;
	
	my ($id, $suffix, $filename, $dispname, $comment, $date, $size, $passwd, $host, $ua, $mimetype, $imageinfo) = 
		ref ($article) ? @$article : split (/\t/, $article);
	
	$date = &getnowdate($date);
	$size = &ins_comma(int(($size+1023)/1024));
	
	if ($isimageview) {
		print <<_EOF;
<p><a href="$STORE_URL$filename"><img src="$STORE_URL$filename" height="250"></a><br>
<a href="$STORE_URL$filename"><b>$dispname</b></a><br>
$comment <small>$date</small></p>
_EOF
	} else {
		my $act = '';
		my @isimage = ('', '');
		
		$comment = '&nbsp;' if ($comment eq '');
		if ($imageinfo =~ /\d+:\d+(?:\:(\w+))?/) {
			@isimage = ('<i>', '</i>');
			$act .= qq|\n    <a href="$CGIURL?m=A&amp;id=$id">A</a>|
				if ($1 eq 'pch');
		}
		
		print <<_EOF;
<tr>
  <td>
    <a href="$CGIURL?m=D&amp;id=$id">D</a>$act
  </td>
  <td>[$isimage[0]<A href="$STORE_URL$filename">$dispname</A>$isimage[1]]</td>
  <td><small>$comment</small></td>
  <td align=right><small><strong>$size</strong></small></td>
  <td><small>$date</small></td>
</tr>
_EOF
	}
}


##################################################
# 日付を取得

my @Weeks = qw/日 月 火 水 木 金 土/;
sub getnowdate {
	my @time = localtime($_[0]);
	return sprintf("%d/%02d/%02d(%s)%02d:%02d",
		$time[5]+1900, $time[4]+1, $time[3], $Weeks[$time[6]], $time[2], $time[1]);
}


##################################################
# 画像閲覧

sub image_view {
	open (LOG, $LOG_FILE) or die("Open Error $LOG_FILE: $!\n");
	eval{ flock (LOG, 1) };
	my @log = <LOG>;
	eval{ flock (LOG, 8) };
	close (LOG);
	
	@log = grep {
		my $type = (split (/\t/, $_))[1];
		$type eq 'jpg' or $type eq 'gif' or $type eq 'png' or $type eq 'bmp';
	} @log;
	
	print "<a href=\"$CGIURL\">Return</a>\n";
	
	my ($page_index, $first_idx, $last_idx) = &page_index($#log, $IMAGEDISP, 'm=I');
	
	print "<hr>", $page_index;
	
	foreach (@log[$first_idx..$last_idx]) {
		&print_article($_, 1);
	}
	
	print $page_index;
}


##################################################
# ファイル検索

sub search {
	
	my @cond_selected = ('','');
	$cond_selected[ $Form{cond} eq 'or' ? 1 : 0 ] = ' selected';
	
	print <<_EOF;
<form method="POST" action="$CGIURL">
<a href="$CGIURL?help=search">検索</a>: <input type="text" size="25" name="kwd" value="$Form{kwd}">
<input type="submit" value="Search" class="button">
<select name="cond">
  <option value="and"$cond_selected[0]>AND検索</option>
  <option value="or"$cond_selected[1]>OR検索</option>
</select>
<input type="hidden" name="m" value="S">
<input type="hidden" name="k" value="$MOJIBAKE_TAISAKU">
</form>
<a href="$CGIURL">Return</a>
_EOF
	if ($Form{kwd} ne '') {
		print "<hr>\n";
		
		# 一旦ダブルクウォートに戻す
		my $tmp;
		($tmp = $Form{kwd}) =~ s/&quot;/"/g;
		
		my @words = map {
			/^"(.*)"$/ ? scalar ($_ = $1, s/""/&quot;/g, $_) : scalar (s/"/&quot;/g, $_);
		} $tmp =~ /("[^"]*(?:""[^"]*)*"|\S+)(?:\s|$)/g;
		
		print "検索結果： ";
		foreach (@words){ print "'$_'\n" }
		
		print <<_EOF;
<table border=0 class="list" summary="list">
<tr>
  <th>ACT</th>
  <th>NAME</th>
  <th>COMMENT</th>
  <th>SIZE(KB)</th>
  <th>DATE</th>
</tr>
_EOF
		open (LOG, $LOG_FILE) or die("Open Error $LOG_FILE: $!\n");
		eval{ flock (LOG, 1) };
		
		# $Form{cond}に値が無ければAND検索に
		my $cond = $Form{cond} eq 'or' ? '||' : '&&';
		my $checkfunc = &build_match_function($cond, @words);
		
		while (<LOG>) {
			my @article = split (/\t/, $_);
			$_ = join ("\t", @article[2,3,4]);	#filename  dispname  comment
			
			&print_article(\@article) if (&$checkfunc());
		}
		eval{ flock (LOG, 8) };
		close (LOG);
		print "</table>\n";
	}
}


##################################################
# $_ に対して検索を行なう関数を作る

sub build_match_function {
	my $cond = shift;
	my $expr = join ($cond, map { 'm/' . quotemeta($_) . '/i' } @_);
	my $sub = eval "sub { $expr }";		# 無名の関数を作成する
	local ($@);
	die $@ if $@;
	return ($sub);
}
#################################################################################################
#bbq
#################################################################################################
# [2026-07-18] DSBL/BBQ/bbxはサービス終了により現在無意味なため、コード全体をコメントアウト（猫）
#sub chk_proxy
#{

#bbqcheck
# 1=on
#my $bbq = 0;

#bbxcheck
# 1=on
#my $bbx = 0;

#dsblcheck
# 1=on
#my $dsbl = 0;

#	my $RADDR = $ENV{'REMOTE_ADDR'}		;
#	$RADDR =~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/;
#bbq
#	my $query_addr1 = "$4.$3.$2.$1.niku.2ch.net";
#bbx
#	my $query_addr2 = "$4.$3.$2.$1.bbx.2ch.net";
#dsbl
#	my $query_addr3 = "$4.$3.$2.$1.unconfirmed.dsbl.org";

#if( $dsbl eq '1'){
#	my $addr3 = join('.', unpack('C*', gethostbyname($query_addr3)));
#	if($addr3 eq '127.0.0.2')
#	{
#	die("Authorization Required\nDSBL\n");
#	return 1	;
#	}
#}

#if ( $bbx eq '1'){
#	my $addr2 = join('.', unpack('C*', gethostbyname($query_addr2)));
#	if ($addr2 eq '127.0.0.2')
#	{
#	die("Authorization Required\nBBX\n");
#	return 1	;
#	}
#}

#if ( $bbq eq '1'){
#	my $addr1 = join('.', unpack('C*', gethostbyname($query_addr1)));
#	if ($addr1 eq '127.0.0.2') 
#	{
#	die("Authorization Required\nBBQ\n");
#	return 1	;
#	}
#}

#	return 0	;
#}
sub chk_proxy { return 0; }  # [2026-07-18] コメントアウト後の代替スタブ（猫）



##################################################
# 投稿処理 (ファイルアップロード)

sub file_upload {

#プロクシ制限
	&chk_proxy;

#	return unless ($Referer =~ /$CGIURL/i);
	
	if (@UploadFiles > 1) {
		die("一度にアップロードできるファイルは一つだけです。\n");
	}
	my $uploadfile = $UploadFiles[0];
	
	my $size = -s $uploadfile->{tmpfile};
	return if ($size == 0);
	
	if ($MIN_UPLOAD_SIZE and $size < $MIN_UPLOAD_SIZE*1024) {
		die ("小さすぎるファイルはアップロードできません。\n");
	}
	
	my $suffix = &get_filetype($uploadfile);
	$suffix = 'txt' if ($HTML_EXT and $suffix =~ /^htm/);
	
	&post_upload_data($uploadfile, $suffix);
}


##################################################
# 投稿処理 (お絵描きデータ)

sub oekaki_upload {
#	return unless ($Referer =~ /$CGIURL/i);
	
	my ($picturefile, $suffix, $imageinfo);
	
	$picturefile = $PictureFiles[0];
	$suffix = $picturefile->{type};
	
	if ($picturefile->{width} > $OEKAKI_MAX_SIZE or $picturefile->{height} > $OEKAKI_MAX_SIZE) {
		die("画像のサイズが大きすぎます\n");
	}
	$imageinfo = [$picturefile->{width}, $picturefile->{height}];
	
	# PCH
	if (@PictureFiles > 1 && $PictureFiles[1]->{type} eq 'pch') {
		push (@$imageinfo, $PictureFiles[1]);
	}
	&post_upload_data($picturefile, $suffix, $imageinfo);
}


##################################################
# 投稿処理２

sub post_upload_data {
	my ($uploadfile, $suffix, $rl_imageinfo) = @_;
	
	my (@newlogdata, $num, $filename, $dispname,  $comment, $size, $passwd, $host, $ua, $mimetype, $imageinfo);
	
	if ($RENZOKU_FILE ne '' and &renzoku_seigen()) {
		die("連続投稿制限。時間を置いてやり直してください。\n");
	}
	
	# コメント
	$comment = $Form{comment};
	if (length($comment) > $MAX_COMMENT_SIZE) {
		die("コメントが長すぎます。\n");
	}
	&autolink(\$comment) if ($AUTOLINK);
	
	# ファイルサイズ
	$size = -s $uploadfile->{tmpfile};
	
	# 削除パス
	$passwd = ($Form{delpass} ne '') ? &encrypt($Form{delpass}) : '';
	
	# USER AGENT
	$ua = ($UA_REC > 0) ? $ENV{HTTP_USER_AGENT} : '';
	&htmlencode(\$ua);
	
	# ホスト
	$host = ($IP_REC > 0) ? &getremotehost() : '';
	
	# Mime-Type
	$mimetype = defined ($uploadfile->{mimetype}) ? $uploadfile->{mimetype} : '';
	&htmlencode(\$mimetype);
	
	
	$num = 1;
	open (LOG, "+<$LOG_FILE") or die("Open Error $LOG_FILE: $!\n");
	eval{ flock (LOG, 2) };
	
	if (defined($_ = <LOG>)) {
		my ($id) = split (/\t/, $_);
		
		$num = $id + 1;
	}
	
	# ファイル名
	if ($LOCAL_FILENAME_SW > 0 and !$Form{hidename} and defined ($uploadfile->{basename})) {
		$dispname = $uploadfile->{basename};
		# 長すぎる名前は省略
		substr ($dispname, $MAX_FILENAME_SIZE) = '..' if (length ($dispname) > $MAX_FILENAME_SIZE);
		
		if ($LOCAL_FILENAME_SW == 2) {
			$filename = &getuploadfilename($uploadfile->{basename}, $suffix);
		}
		# ローカルのファイル名が使えなかったら連番ファイル名
		$filename ||= &getrenbanfilename($num, $suffix) or die ("ログデータが壊れてる？\n");
	} else {
		# 両方とも連番ファイル名
		$dispname = $filename = &getrenbanfilename($num, $suffix) or die ("ログデータが壊れてる？\n");
	}
	&htmlencode(\$dispname);
	
	# リネームする
	rename ($uploadfile->{tmpfile}, "$STORE_DIR/$filename")
		or die("Write Error $STORE_DIR/$filename: $!\n");
	
	# お絵描きデータ
	if ($rl_imageinfo) {
		
		# PCHファイル（お絵描きアニメデータ）記録
		if ($rl_imageinfo->[2]) {
			my $pchfile = $rl_imageinfo->[2];
			my $pchfilename = &getrenbanfilename($num, 'pch') or die ("ログデータが壊れてる？\n");
			
			rename ($pchfile->{tmpfile}, $STORE_DIR.'/'.$pchfilename)
				or die ("Write Error $STORE_DIR/$filename: $!\n");
			
			$rl_imageinfo->[2] = 'pch';
		}
		$imageinfo = join (':', @$rl_imageinfo);
		
	} else {
		$imageinfo = '';
	}
	
	# ログデータの先頭に追加
	push (@newlogdata, join("\t", $num, $suffix, $filename, $dispname, $comment, time, $size, $passwd, $host, $ua, $mimetype, $imageinfo) . "\n");
	
	my $i = 1;
	seek (LOG, 0, 0);
	while (<LOG>) {
		if ($i++ < $LOGSAVE) {
			push (@newlogdata, $_);
		} else {
			my @article = split (/\t/, $_);
			
			&unlink_filedata (\@article);
		}
	}
	
	# ディスクサイズによる自動削除機能
	# 古い方から順番に消す。
	if ($DISK_SPACE_MAX) {
		my $use = &disk_used();
		my $limit = $DISK_SPACE_MAX * 1024;
		while ($use > $limit) {
			my @article = split (/\t/, pop (@newlogdata));
			
			$use -= &unlink_filedata (\@article);
		}
	}
	
	seek (LOG, 0, 0);
	print LOG @newlogdata;
	truncate (LOG, tell(LOG));
	eval{ flock (LOG, 8) };
	close (LOG);
	
#	最初のページからにする。$Form{lm}は残す
	$Form{page} = $Form{sort} = $Form{rev} = undef;
	
	&make_index_html() if ($MAKE_INDEX_SW);
}


##################################################
# アップロードデータの拡張子を得る

sub get_filetype {
	my ($uploadfile) = @_;
	my $suffix;
	
	# 拡張子手動選択
	if ($Form{suffix} =~ /^(\w+)$/) {
		$suffix = $1;
		return $suffix if (exists($MIMETYPE{$suffix}));
	}
	
	# ローカルのファイル名の拡張子
	if ($uploadfile->{basename} =~ /\.(\w+)$/) {
		$suffix = lc ($1);
		return $suffix if (exists($MIMETYPE{$suffix}));
	}
	
	# MIMEタイプから拡張子を決定する
	my $mime_type = $uploadfile->{mimetype};
	while (my($ext, $mime) = each (%MIMETYPE)) {
		next unless ($mime);
		return $ext if ($mime_type =~ /$mime/i);
	}
	return $DEF_EXT;	#デフォルト
}


##################################################
# 記録ファイルのIDと拡張子からファイル名を得る

sub getrenbanfilename {
	
	# 汚染されてないか調べる
	my $id     = $_[0] =~ /^(\d+)$/ ? $1 : return undef;
	my $suffix = $_[1] =~ /^(\w+)$/ ? $1 : return undef;
	
	return sprintf("%s%04d.%s", $PREFIX, $id, $suffix);
}


##################################################
# ローカルのファイル名からファイル名を取得する
# 許可されて無い文字が含まれていたらundefを返す

sub getuploadfilename {
	my ($filename, $suffix) = @_;
	
	if ($filename =~ /^(\w[\w\.\-]*)$/) {
		$filename = $1;
		
		# 拡張子を挿げ替える
		$filename =~ s/\.+[^\.]*$//;
		
		# 長すぎるファイル名は途中でぶった切る
		substr ($filename, $MAX_FILENAME_SIZE) = '' if (length ($filename) > $MAX_FILENAME_SIZE);
		
		# index.htmlはだめ
		return undef if ($filename =~ /^index$/i and $suffix =~ /^htm/i);
		
		return undef if ($PREFIX and $filename =~ /^$PREFIX/o);
		
		return "$filename.$suffix" unless -e "$STORE_DIR/$filename.$suffix";
		
		for (my $i=1; $i<=10; $i++) {
			return "$filename($i).$suffix" unless -e "$STORE_DIR/$filename($i).$suffix";
		}
	}
	return undef;
}


##################################################
# 自動リンク

sub autolink {
	my $s = shift;
	
	my $uric = '\w' . quotemeta(';/?:@=+$,%-.!~*\'()');	# &は除外、_は\wに含まれる
	$uric .= '\#';	# flagment
	
	$$s =~ s{
		\b (?=[hfgmnt])						# 先頭の文字を先読みさせると選択が速くなる
		( (?:https?|ftp|gopher|mailto|news|nntp|telnet) :
		  [$uric]+ (?:&amp;[$uric]*)*  )	# & は&amp;にエスケープされている
	}{<a href="$1">$1</a>}gox;
}


##################################################
# ファイル削除モード

sub delete {
	
	if ($Form{delpass} eq '') {
		print <<_EOF;
<h3>ID：$Form{id}を削除します</h3>
<form method="POST" action="$CGIURL">
<input type="hidden" name="m" value="D">
<input type="hidden" name="id" value="$Form{id}">
パスワード入力：<input type="password" size="10" name="delpass" value="@{[&htmlencode($Cookie{delpass})]}">
<input type="submit" value="削除" class="button">
<input type="radio" name="isadmin" value="off" checked>削除パス
<input type="radio" name="isadmin" value="on">管理パス
</form>
_EOF
	} else {
		
		unless ($Form{id} =~ /^\d+$/) { die ("ID：$Form{id}が見つかりませんでした。\n"); }
		
		my $newlogdata = '';
		
		open (LOG, "+< $LOG_FILE") or die ("Open Error $LOG_FILE: $!\n");
		eval { flock (LOG, 2) };
		
		my $flag;
		while (<LOG>) {
			if (/^\Q$Form{id}\E\t/o) {
				$flag++;
				my @field = split (/\t/, $_);
				if ($Form{isadmin} eq 'on') {
					my $adminpasswd;
					open (PASSWD, $ADMINPASSWD) or die ("Open Error $ADMINPASSWD: $!\n");
					chomp ($adminpasswd = <PASSWD>);
					close (PASSWD);
					die("パスワ－ドが違います。\n") unless (&checkpassword($Form{delpass}, $adminpasswd));
				} else {
					die("パスワ－ドが違います。\n") unless (&checkpassword($Form{delpass}, $field[7]));
				}
				
				&unlink_filedata (\@field);
				
				next;
			}
			$newlogdata .= $_;
		}
		unless ($flag) { die("ID：$Form{id}が見つかりませんでした。\n"); }
		
		seek (LOG, 0, 0);
		print LOG $newlogdata;
		truncate (LOG, tell(LOG));
		eval { flock (LOG, 8) };
		close (LOG);
		
		print "<h3>ファイルを削除しました。</h3>\n";
		
		&make_index_html() if ($MAKE_INDEX_SW);
		
	}
	print "<a href=\"$CGIURL\">Return</a>\n";
}


##################################################
# ファイルを削除

sub unlink_filedata {
	my $article = shift;
	
	my ($delsize, $delfile, $pchfile);
	
	$delsize = 0;
	($delfile) = $article->[2] =~ /^(\w[\w\.\-\(\)]*)$/ or return 0;
	
	if (-f "$STORE_DIR/$delfile") {
		$delsize += -s _;
		unlink ("$STORE_DIR/$delfile");
	}
	
	# imageinfo
	if ($article->[11] ne '' and $article->[11] =~ /^\d+:\d+:pch/) {
		($pchfile = $delfile) =~ s/\.+[^\.]*$/\.pch/;
		if (-f "$STORE_DIR/$pchfile") {
			$delsize += -s _;
			unlink ("$STORE_DIR/$pchfile");
		}
	}
	
	return ($delsize);
}


##################################################
# パスワード暗号化

sub encrypt {
	my $inpw = shift;
	
	my (@letters, $salt, $encrypt);
	@letters = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');
	srand;
	$salt = $letters[rand(@letters)] . $letters[rand(@letters)];
	$encrypt = crypt($inpw, $salt) || crypt ($inpw, '$1$' . $salt);
	return $encrypt;
}


##################################################
# パスワード照合

sub checkpassword {
	my ($inpw, $logpw) = @_;
	return undef if ($logpw eq '');
	return crypt($inpw, $logpw) eq $logpw;
}


##################################################
# インデックスページ作成
# かなり適当

sub make_index_html {
	open (INDEXPAGE, "> $INDEX_FILEPATH") or die ("Open Error $INDEX_FILEPATH: $!\n");
	my $savefh = select (INDEXPAGE);
	
	# 変数をいったん退避させる
	local ($COUNTFILE, %Form, %Cookie);
	
	&print_header('',1);
	&print_obititle();
	&list();
	&print_footer();
	
	select ($savefh);
	close (INDEXPAGE);
}


##################################################
# お絵描きアプレット表示

sub print_canvas {
	
	my $width  = $Form{hsize} || $OEKAKI_DEF_SIZE;
	my $height = $Form{vsize} || $OEKAKI_DEF_SIZE;
	$width  = $OEKAKI_MAX_SIZE if ($width  > $OEKAKI_MAX_SIZE);
	$height = $OEKAKI_MAX_SIZE if ($height > $OEKAKI_MAX_SIZE);
	my $applet_width  = $width  + 120;
	my $applet_height = $height + 120;
	
	my $applet_params = '';
	for (sort keys (%APPLET_PARAMS)) {
		next if ($APPLET_PARAMS{$_} eq '');
		$applet_params .= qq|      <param name="$_" value="$APPLET_PARAMS{$_}">\n|;
	}
	
	my $notice_msg = '';
	if ($OEKAKI_ANIMATION and $Form{anime} eq 'on') {
		$applet_params .= qq|      <param name="thumbnail_type" value="animation">\n|;
		$notice_msg = qq|<tr><td colspan="2"><strong>描画アニメデータ記録中</strong></td></tr>\n|;
	}
	
	my $addoption = '';
	print <<_EOF;
<script type="text/javascript" src="$BASE_URL/palette.js" charset="UTF-8"></script>
<script type="text/javascript"><!--
  // PaintBBSから特定のタイミングで呼ばれる
  function paintBBSCallback(value) {
    if (value == "header") { //送信前
      var pf = document.post_field;
      
      // Stringオブジェクトを宣言しないと駄目らしい
      var postdata = new String();
      
      for (var i=0; i < pf.elements.length; i++) {
        if (pf.elements[i].name) {
          // IE3 NN2で動かないけど無視ヽ(´ー｀)ノ
          if (pf.elements[i].type == "select-one" || pf.elements[i].type == "select-multiple") {
            for (var j=0; j < pf.elements[i].options.length; j++) {
              if (pf.elements[i].options[j].selected)
                postdata += pf.elements[i].name + "=" + pf.elements[i].options[j].value + "&";
            }
            continue;
          }
          if (pf.elements[i].type == "checkbox" || pf.elements[i].type == "radio")
            if (!pf.elements[i].checked) continue;
          postdata += pf.elements[i].name + "=" + pf.elements[i].value + "&";
        }
      }
      
      return postdata;
    }
  }
  
  // escape()がUnicodeに変換される対策
  function url_encode(str) {
    var enc = ""
    for (var i=0; i<str.length; i++) {
      var c = str.substring(i, i+1);
      // ASCIIの 0-9 A-Z a-z 以外、日本語はスキップする
      if ( c <= "\057"
        || ("\072" <= c && c <= "\100")
        || ("\133" <= c && c <= "\140")
        || ("\173" <= c && c <= "\177")
      ) {
        enc += escape(c);
      } else {
        enc += c;
      }
    }
    return enc;
  }
//--></script>
<noscript>
  <h3>JavaScriptが有効でないため一部機能\が動作致しません。</h3>
</noscript>

<a href="$CGIURL">Return</a>

<hr>
<table border=0 cellspacing=0 cellpadding=0>
  <!-- ボタンを押すと、ライブコネクトを使ってPaintBBSの送信処理をする -->
  <script type="text/javascript"><!--
    document.write(
      '<tr><td colspan="2"><form name="post_field">'
    + 'コメント<br>'
    + '<input type="text" size="60" name="comment" value="">'
    + '<input type="button" value=" Post " class="button" onClick="document.paintbbs.pExit()"><input type="reset" value="Cancel" class="button"><br>'
    + '<a href="$CGIURL?help=del">del pass</a>: <input type="password" size="10" name="delpass" maxlength="10" value="@{[&htmlencode($Cookie{delpass})]}">  '
    $addoption
    + '</form></td></tr>'
    );
  //--></script>
  
  $notice_msg
  
  <tr>
  <td valign="top">
    <applet name="paintbbs" code="pbbs.PaintBBS.class" codebase="$BASE_URL" archive="PaintBBS.jar"
            width="$applet_width" height="$applet_height" mayscript
            alt="ご使用のブラウザはJavaが非アクティブ状態になっています。そのためペイントツールが表示されません。">
      <param name="image_width"  value="$width">
      <param name="image_height" value="$height">
      <param name="image_jpeg" value="true">
      <param name="image_size"   value="65">
      <param name="compress_level" value="15">
      <param name="poo" value="false">
      <param name="send_header" value="">
      <param name="send_language" value="sjis">
      <param name="url_save" value="$CGIURL">
      <param name="url_exit" value="$CGIURL">
$applet_params
    </applet>
  </td>
  <td align="center" valign="top">
    <script type="text/javascript" charset="UTF-8"><!--
      PaletteInit();
    //--></script>
  </td>
  </tr>
  <tr>
    <td colspan="2"><br>
    <p>
      ミスしてページを変えたりウインドウを消してしまったりした場合は落ちついて同じキャンバスの幅で<br>
      編集ページを開きなおしてみて下さい。大抵は残っています。<br>
      MacIEやネスケ４.*の場合はブラウザのウインドウを全て閉じてしまったら復旧出来ません）<br>
    </p>
    <p><a href="$BASE_URL/shiihelp.html" target="_blank">お絵描きしぃアプレットの使い方</a></p>
    </td>
  </tr>
</table>
_EOF
}


##################################################
# 記事を一件取ってくる

sub get_article {
	
	my $number = shift;
	my ($flag, @msg);
	
	if ($number =~ /^\d+$/) {
		open (LOG, $LOG_FILE) or die ("Open Error $LOG_FILE: $!\n");
		eval { flock (LOG, 1) };
		while (<LOG>) {
			if (/^\Q$number\E\t/o) {
				chop;
				@msg = split (/\t/, $_);
				$flag = 1;
				last;
			}
		}
		eval { flock (LOG, 8) };
		close (LOG);
	}
	if (!$flag) { die("該当ファイルが見つかりませんでした。\n"); }
	
	return @msg;
}


##################################################
# PCHアニメを描画

sub oekaki_movie {
	
	my ($id, $suffix, $filename, $dispname, $comment, $date, $size, $passwd, $host, $ua, $mimetype, $imageinfo)
	 = &get_article ($Form{id});
	
	my ($width, $height, $pch) = split (/:/, $imageinfo);
	unless ($pch eq 'pch') { die ("このファイルにはアニメデータは記録されていません\n"); }
	
	my $pchfile;
	($pchfile = $filename) =~ s/\.+[^\.]*$/\.pch/;
	unless (-f "$STORE_DIR/$pchfile") { die ("このファイルにはアニメデータは記録されていません\n"); }
	my $datasize = &ins_comma(-s _);
	
	$pchfile = $STORE_URL . $pchfile;
	
	print <<_EOF;
<a href="$CGIURL">Return</a>

<div align="center">
  <applet name="paintbbs" code="pbbs.PaintBBS.class" codebase="$BASE_URL" archive="PaintBBS.jar"
          width="$width" height="$height" mayscript
          alt="ご使用のブラウザはJavaが非アクティブ状態になっています。そのためペイントツールが表示されません。">
  <param name="image_width" value="$width">
  <param name="image_height" value="$height">
  <param name="viewer" value="true">
  <param name="pch_file" value="$pchfile">
  <param name="speed" value="10">
  </applet><br>
  <small>Data size : $datasize byte</small><br>
  
  <script type="text/javascript"><!--
  function setSpeed (f) {
    var s = f.speed;
    document.paintbbs.speed = parseInt(s.options[s.selectedIndex].value);
  }
  document.write (
      '<form>'
    + '  <small>再生速度 '
    + '  <select name="speed">'
    + '    <option value="-1">最速</option>'
    + '    <option value="0">高速</option>'
    + '    <option value="10" selected>中速</option>'
    + '    <option value="80">鈍足</option>'
    + '    <option value="500">スロー</option>'
    + '  </select>'
    + '  <input type="button" value="変更" class="button" onClick="setSpeed(this.form)" onKeyPress="setSpeed(this.form)">'
    + '  </small>'
    + '</form>'
  );
  //--></script>
  
  <br>
</div>
_EOF

}


##################################################
# CGIフォーム情報の取得

sub read_cgistream {
	my ($content_type, $content_length, $url_encoded_data,
		$pair, $name, $value, $skip_jconv);
	
	$content_type   = $ENV{CONTENT_TYPE};
	$content_length = $ENV{CONTENT_LENGTH};
	
	if ($MAX_UPLOAD_SIZE and $content_length > $MAX_UPLOAD_SIZE*1024 + $MAX_COMMENT_SIZE) {
		die("送信データ量が既定値を超えています。\n");
	}
	
	if ($content_type =~ m|multipart/form-data|) {
		require 'multipart.pl';
		@UploadFiles = &multipart::get_multipart(\&storeformdata, $TMPDIR);
	} elsif ($OEKAKI_SW and $content_type eq 'application/octet-stream') {
		require 'getpic.pl';
		
		&getpic::change_error_content_type('application/octet-stream') if ($TEXT_BANNER);
		
		my $recv_thumbnail = $OEKAKI_ANIMATION ? 1 : 0;
		($url_encoded_data, @PictureFiles) =
			&getpic::getpics($recv_thumbnail, $TMPDIR);
		$skip_jconv++;
	} elsif (   $content_type eq ''
			 or	$content_type eq 'application/x-www-form-urlencoded') {
		if ($ENV{REQUEST_METHOD} eq 'POST') {
			read (STDIN, $url_encoded_data, $content_length);
		} else {
			$url_encoded_data = $ENV{QUERY_STRING};
		}
	} else {
		die("Invalid content type!\n");
	}
	
	if ($url_encoded_data ne '') {
		$url_encoded_data =~ tr/+/ /;
		
		foreach $pair ( split (/&/, $url_encoded_data) ) {
			($name, $value) =  split (/=/, $pair, 2);
			$name  =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
			$value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
			
			&storeformdata($name, $value);
		}
	}
	
	# 漢字コード変換
	# $Form{k}に入れた文字が文字化けしていたら変換をする
	# 特に変換を必要としない時は $Form{k} に値を入れていない
	if (!$skip_jconv and $Form{k} ne '' and $Form{k} ne $MOJIBAKE_TAISAKU) {
		# [2026-07-18] jcode.pl不使用化（スタンドアロン方針、猫）
		#require 'jcode.pl';
		#for (keys(%Form)){ &jcode::convert(\$Form{$_}, 'sjis'); }
	}
	
	&getcookie();
	
	if ($Form{act} eq 'Up/Reload') {
		# チェックボックスがONならクッキーを食べる
		if ($Form{cookie_ok}) {
			# なんか変
			my $tmp = $Form{delpass};
			$tmp =~ s/&quot;/"/g;
			$tmp =~ s/&lt;/</g;
			$tmp =~ s/&gt;/>/g;
			$tmp =~ s/&amp;/&/g;
			&setcookie('delpass' => $tmp);
		# チェックボックスがOFFなのにクッキーが存在するときはクッキーを破棄
		} elsif (%Cookie) {	
			&setcookie();
		}
	}
}
sub storeformdata {
	my ($name, $value) = @_;
	
	return if ($value eq "");
	
	# 改行コードを統一する
#	$value =~ s/\x0D\x0A/\n/g;
#	$value =~ tr/\x0D\x0A/\n\n/;
	
	$Form{$name} = &htmlencode(\$value);
}


##################################################
# 文字列中のHTMLタグを無効にする

sub htmlencode {
	my $thingy = shift;
	my $s = ref ($thingy) ? $thingy : \$thingy;
	$$s =~ s/&/&amp;/g;
	$$s =~ s/"/&quot;/g;
	$$s =~ s/</&lt;/g;
	$$s =~ s/>/&gt;/g;
	$$s =~ tr/\t\n\r//d;
	$$s;
}


##################################################
# URLエンコード

sub urlencode {
	my $thingy = shift;
	my $s = ref ($thingy) ? $thingy : \$thingy;
	$$s =~ s/(\W)/'%' . unpack('H2', $1)/eg;
	$$s;
}


##################################################
# COOKIEを送信

sub setcookie {
	my ($cookie, $expday, $gmt, $path);
	
	if (@_ == 0) {
		$cookie = ''; $gmt = 'Fri, 27-Feb-1976 00:00:00 GMT';
		%Cookie = ();
	} else {
		my @week  = qw/Sun Mon Tue Wed Thu Fri Sat/;
		my @month = qw/Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec/;
		
		$expday = 60; # クッキーの有効期限は60日間
		my @t = gmtime(time + $expday * 24 * 60 * 60);
		$gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$week[$t[6]], $t[3], $month[$t[4]], $t[5]+1900, $t[2], $t[1], $t[0]);
		
		while (@_) {
			my $key = shift(@_);
			my $val = shift(@_);
			$cookie .= $key . '=' . &urlencode($val);
			$cookie .= '&' if (@_);
			$Cookie{$key} = $val;	# 現在の値に反映させる
		}
	}
	if ($ENV{SCRIPT_NAME}) {
		$path = substr ($ENV{SCRIPT_NAME}, 0, rindex($ENV{SCRIPT_NAME}, "/")+1);
	}
	
	print "Set-Cookie: $COOKIE_NAME=$cookie; expires=$gmt" . ($path ? "; path=$path\n" : "\n");
}


##################################################
# COOKIEを取得

sub getcookie {
    
    if ($ENV{HTTP_COOKIE} =~ /(?:^|; *)$COOKIE_NAME=([^;]*)(?:;|$)/o) {
		foreach ( split(/&/, $1) ) {
			my ($key, $val) = split(/=/, $_, 2);
			$val =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
			$Cookie{$key} = $val;
		}
	}
}


##################################################
# バイトサイズに単位を付ける

sub byte_calc {
	my ($n, $m, $unit);
	$n = shift; # KB
	
	if ($n >= 1000 * 1024) {
		$m = 1024 * 1024; $unit = 'GB';
	} elsif ($n >= 1000) {
		$m = 1024; $unit = 'MB';
	} else {
		$unit = 'KB'; $n = int($n);
	}
	if ($m) {
		$n /= $m;
		if ($n != int($n)) {	# 少数
			$n = ($n < 100) ? sprintf("%.3g", $n) : int($n);
		}
	}
	return $n . $unit;
}


##################################################
# 3桁ごとにコンマで区切る

sub ins_comma {
	my $n = shift;
	$n =~ s/\G((?:^[-+])?\d{1,3})(?=(?:\d\d\d)+(?!\d))/$1,/g;
	$n;
}


##################################################
# ディスク使用量

sub disk_used {
	my $use;
	opendir (DIR, $STORE_DIR) or die("Open Error $STORE_DIR: $!\n");
	while (defined($_ = readdir(DIR))) {
		next if (/^\.\.?$/);
		next if (/\.tmp$/);		# tmpファイルの拡張子に気をつけたほうがいいかも
		$use += -s $STORE_DIR . '/' . $_;
	}
	closedir (DIR);	
	return $use;
}


##################################################
# リモートホスト名取得

my $RemoteHost;
sub getremotehost {
	unless ($RemoteHost) {
		$RemoteHost = $ENV{REMOTE_HOST} || $ENV{REMOTE_ADDR};
		if ($RemoteHost eq $ENV{REMOTE_ADDR}) {
			$RemoteHost = gethostbyaddr( pack("C4", split(/\./, $RemoteHost)) ,2) || $RemoteHost;
		}
	}
	$RemoteHost;
}


##################################################
# 連続投稿制限

sub renzoku_seigen {
	my ($myip, @list, $flag);
	$myip = $ENV{REMOTE_ADDR};
	
	open (RENZOKU, "+<$RENZOKU_FILE") or die("Open Error $RENZOKU_FILE: $!\n");
	eval{ flock (RENZOKU, 2) };
	
	my $limit = time - $RENZOKU_TIME;
	
	while (<RENZOKU>) {
		my ($ip, $t) = split(/:/, $_);
		chop($t);
		next if ($t <= $limit);
		
		$flag++ if ($myip eq $ip);
		push (@list, $_);
	}
	unless ($flag) { push (@list, join(':',$myip,time)."\n"); }
	
	seek (RENZOKU, 0, 0);
	print RENZOKU @list;
	truncate (RENZOKU, tell(RENZOKU));
	eval{ flock (RENZOKU, 8) };
	close (RENZOKU);
	
	return $flag;
}


##################################################
# 禁止ドメインか調べる (return 1:禁止ドメイン, 0:その他)

sub checkdomain {
	my ($domain, $host, $hostip, $ret);
	my $access_control_file = shift;
	
	open (AXSCTRL, $access_control_file) or die("Open Error $access_control_file: $!\n");
	while (<AXSCTRL>) {
		next if (/^#/ or /^$/);
		chomp;
		if (m#^(\d+\.\d+\.\d+\.\d+)(?:/(\d+))?$#) {
			my $mask  = $2;
			my $domip = &inetaddr2int($1);
			
			$hostip ||= &inetaddr2int($ENV{REMOTE_ADDR});
			
			if (defined($mask)) {
				$mask = ~((1<<(32-$mask))-1);
			} else {
				# 下位ビットが0で埋められているか調べる
				$mask = ~0;
				foreach (0xFFFFFFFF, 0xFFFFFF, 0xFFFF, 0xFF) {
					unless ($domip & $_) {
						$mask = ~$_;
						last;
					}
				}
			}
			if (($hostip & $mask) == ($domip & $mask)) {# 指定IP
				close (AXSCTRL); return undef;
			}
		} else {
			$host ||= &getremotehost();
			if ($host =~ m#(^|\.)\Q${_}\E$#) {			# 指定ドメイン名で終わるホスト
				close (AXSCTRL); return undef;
			}
		}
	}
	close (AXSCTRL); return 1;
}
sub inetaddr2int {
	my $addr = shift;
	my @ip = split(/\./, $addr);
	((((($ip[0]<<8)+$ip[1])<<8)+$ip[2])<<8)+$ip[3];
}


##################################################
# 参照先を調べる
sub checkreferer {
	my $rl_except = shift;
	
	my $referer = $ENV{HTTP_REFERER};
	$referer =~  s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
	
	for (@$rl_except) {
		return undef if ($referer =~ /\Q$_\E/);
	}
	return 1;
}


##################################################
# カウンタ

sub counter {
	local ($@);
	open (COUNTER, "+< $COUNTFILE") or return "ERROR";
	
	eval{ flock (COUNTER, 2) };
	# ノンブロッキング。カウンタごときでブロックさせるのも馬鹿馬鹿しいと思った
	# でもやっぱりやめた
#	if (!eval{ flock(COUNTER, 6) } and !$@) { close (COUNTER); return "BUSY"; }
	
#	my $count = <COUNTER>;
	my ($count, $date);
	if (defined($_ = <COUNTER>)) {
		($count, $date) = split (/:/, $_);
	}
	unless ($date) {
		my @lt=localtime();
		$date = sprintf ("%d/%02d/%02d", $lt[5]+1900, $lt[4]+1, $lt[3]);
	}
	$count++;
	
	seek (COUNTER, 0, 0);
	print COUNTER "$count:$date";
	truncate (COUNTER, tell(COUNTER));
	eval{ flock (COUNTER, 8) };
	close (COUNTER);
	
	return "$date から $count";
}


##################################################
# エラー出力

sub cgidie {
	my $errmsg = join('<br>', @_);
	
	&print_header('エラー');
	print "<h3>$errmsg</h3>\n<a href=\"$CGIURL\">Return</a>\n</body>\n</html>\n";
	exit;
}


##################################################
# ヘルプ表示

sub help {
	
	my $help_genre = $Form{help};
	if ($help_genre eq 'file') {
		print "<h3>対応ファイルフォーマット</h3>\n<p><tt>";
		my $i = 0;
		for (sort keys(%MIMETYPE)) {
			print "*.$_ ";
			print "<br>\n" if ((++$i % 12) == 0);
		}
		print "<br>\n</tt>\nその他のファイルフォーマットは特に指定の無い限り*.$DEF_EXTとして保存されます。<br></p>\n";
	} elsif ($help_genre eq 'del') {
		print <<_EOF;
<h3>投稿記事削除パスについて</h3>
<p>
投稿者が後々自分の投稿記事を削除したい場合に入力します。<br>
パスワードが入力されないまま投稿された記事は管理者にしか削除できなくなります。<br>
パスワードには10文字未満の英数記号を指定できます。<br>
</p>
_EOF
	} elsif ($help_genre eq 'search') {
		print <<_EOF;
<h3>検索キーワードについて</h3>
<p>
キーワードは「半角スペース」で区切って複数指定することができます。<br>
キーワードに半角スペースを使いたいときはそのキーワードを半角のダブルクウォート「"」で括ってください。<br>
コメントとファイル名のフィールドにマッチします。<br>
</p>
_EOF
	} elsif ($help_genre eq 'disk') {
		my $use = &disk_used();
		
		print <<_EOF;
<h3>ディスク使用量</h3>
<p>
現在のディスク使用量は${\(&byte_calc($use/1024))} (${\(&ins_comma($use))}バイト)です。<br>
_EOF
		if ($DISK_SPACE_MAX) {
			print "${\(&byte_calc($DISK_SPACE_MAX))} を超えると自動的にファイルが削除されます。<br>\n";
		}
		print "</p>\n";
	}
	print "<a href=\"$CGIURL\">Return</a>\n";
}


##################################################
# 管理パス設定

sub set_adimn_passwd {
	&print_header('はじめまして(^Д^)');
	
	if ($Form{admpass} ne '') {
		my $encrypt = &encrypt($Form{admpass});
		
		open (PASSWD, "> $ADMINPASSWD") or die("Open Error $ADMINPASSWD: $!\n");
		print PASSWD $encrypt;
		close (PASSWD);
		chmod (0600, $ADMINPASSWD);
		print "<h3>パスワードを設定しました。</h3>\n<a href=\"$CGIURL\">Return</a>\n";
	} else {
		print <<_EOF;
<h3>パスワード設定を行います。</h3>
これからアップローダの管理で使用する「管理用パスワード」を入力してください。<br>
<form action="$CGIURL" method="POST">
<input type="password" name="admpass" size=10>
<input type="submit" value="Set">
</form>
_EOF
	}
	&print_footer();
}


##################################################
# Main
# die ("現在メンテナンス中です。\n");

if ($ACCESS_CONTROL ne '' and !&checkdomain($ACCESS_CONTROL)) {
	die("あなたにはアクセス権限がありません。\n");
}

# 本当にそのサイトからの来客を禁止したいなら
# 一定期間アクセスを禁止するような処理に書き換えるといいかも
if (@EXCEPT_REFERER and !&checkreferer(\@EXCEPT_REFERER)) {
	print "Location: http://www5b.biglobe.ne.jp/~iwasas/pu/P-main.html\n\n";
	exit;
}

&read_cgistream();

if (!(-e $ADMINPASSWD) || -z _) {
	&set_adimn_passwd();
	exit;
}

#if ($MAKE_INDEX_SW && !(-e $INDEX_FILEPATH)) {
#	&make_index_html() 
#}

if (@UploadFiles) {
	&file_upload();
} elsif (@PictureFiles) {
	&oekaki_upload();
	print "Content-Type: text/plain\n\n", "ok\n";
	exit;
}
if ($OEKAKI_SW and $Form{m} eq 'E') {
	&print_header('お絵描き');
	&print_obititle('お絵描き');
	&print_canvas();
} elsif ($Form{m} eq 'I') {
	&print_header('画像閲覧');
	&print_obititle('画像閲覧');
	&image_view();
} elsif ($Form{m} eq 'S') {
	&print_header('ファイル検索');
	&print_obititle('ファイル検索');
	&search();
} elsif ($Form{m} eq 'D') {
	&print_header('ファイル削除');
	&print_obititle('ファイル削除');
	&delete();
} elsif ($Form{m} eq 'A') {
	&print_header('描画アニメーション再生');
	&print_obititle('描画アニメーション再生');
	&oekaki_movie();
} elsif ($Form{help} ne '') {
	&print_header('Notice！');
	&help();
} else {
	&print_header();
	&print_obititle();
	&list();
}
&print_footer();
