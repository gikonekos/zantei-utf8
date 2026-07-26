package getpic;
#
#  画像の受け取り、記録
#
#  PaintBBS
#   http://www.gt.sakura.ne.jp/~ocosama/garakuta/soft/paintbbs/Readme_Shicyan.html
#
# require 'getpic.pl';
# ($formdata, @picture_files) = &getpic::getpics($recv_thumbnail, $tmpdir);
# @picture_files = &getpic::oekaki_pictures();
#
use strict;

require 'imagesize.pl';

# requireしただけで変更されるので注意
$SIG{__DIE__} = \&put_oekaki_error;

my $RECV_THUMBNAIL = 1;
my $MAX_FORMDATA = 4 * 1024;
my $MAX_PIC_SIZE = 512 * 1024;
my $MAX_THUMB_SIZE = 256 * 1024;
my $BLKSIZE = 4 * 1024;
my $ERROR_CONTENT_TYPE = 'text/plain';

@oekaki::Pictures = ();

sub getpics {
	my ($recv_thumbnail, $tmpdir) = @_;
	
	$recv_thumbnail = $RECV_THUMBNAIL unless (defined ($recv_thumbnail));
	$tmpdir ||= '/tmp';
	
	my ($formdata, $pic, @thumbnails);
	local $oekaki::content_left = $ENV{'CONTENT_LENGTH'};
	
	binmode (STDIN);
	
	my $header = &_read_from_stdin(9);
	
	if (substr($header, 0, 1) eq 'P') {
		# PaintBBS形式
		#   "P" (1Byteの識別文字)
		#   拡張ヘッダ長(必ず8文字8Byte)
		#   拡張ヘッダ
		#   画像の大きさ(必ず8文字8Byte)
		#   CR LF (互換性の為入れています。ここから下はバイナリ含むの意味)
		#   画像(PNGかJPEG)
		#   サムネイル長(必ず8文字8Byte)
		#   サムネイル(PNGかJPEGかPaintChatAnimationデータ)
		#   サムネイル長(必ず8文字8Byte)
		#   サムネイル(PNGかJPEGかPaintChatAnimationデータ)
		
		# フォームデータ
		my $length = int(substr($header, 1, 8));
		if ($length > 0) {
			die('フォームデータが限界量を超えました。') if ($length > $MAX_FORMDATA);
			$formdata = &_read_from_stdin($length);
		}
		
		# お絵描き画像
		my $tmp = &_read_from_stdin(10);
		substr ($tmp, -2, 2) = '';	# CR LF を取り除く
		die('画像データを受け取れませんでした。') unless (($length = int($tmp)) > 0);
		die('画像データが限界量を超えました。') if ($length > $MAX_PIC_SIZE);
		
		my $picture = &_new_oekaki_file($tmpdir);
		&_read_from_stdin_to_picture($picture->{tmpfile}, $length);
		
		# サムネイル
		my $i = $recv_thumbnail;
		while ($i > 0 and ($length = int(&_read_from_stdin(8))) > 0) {
			die('画像データが限界量を超えました。') if ($length > $MAX_THUMB_SIZE);
			
			my $thumbnail = &_new_oekaki_file($tmpdir);
			&_read_from_stdin_to_picture($thumbnail->{tmpfile}, $length);
		} continue {
			$i--;
		}
	} elsif ($header eq 'junji.gif') {
		# poo形式
		#   "junji.gif" CR LF
		#   画像 (PNG)
		
		&_read_from_stdin(2);	# CR LF を取り除く
		
		my $picture = &_new_oekaki_file($tmpdir);
		&_read_from_stdin_to_picture($picture->{tmpfile});
		
	} else {
		die('サポートされていない形式のデータです。');
	}
	
	# 画像の情報を得る
	for my $pic (@oekaki::Pictures) {
		my ($w, $h, $id) = &imagesize::analyze($pic->{tmpfile});
		if ($id eq 'Data stream is not a known image file format') {  	# PCH
			$pic->{type} = 'pch';
		} else {
			unless ($w or $h){ die ("$id\n"); }
			$pic->{width}  = $w;
			$pic->{height} = $h;
			$pic->{type} = $id;
		}
	}
	if ($oekaki::Pictures[0]->{type} eq 'pch') {
		die ('送信データが正常ではありません。');
	}
	
#open (OUT, ">> formdata.log") or die $!;
#print OUT $formdata, "\n";
#close (OUT);
	
	return ($formdata, @oekaki::Pictures);
}

sub _read_from_stdin {
	my $length = shift;
	my $buffer;
	if ($oekaki::content_left > 0) {
		unless (read(STDIN, $buffer, $length) == $length){
			die('read error');
		}
		$oekaki::content_left -= $length;
		return $buffer;
	}
	undef;
}

sub _read_from_stdin_to_picture {
	my ($file, $length) = @_;
	
	$length ||= $oekaki::content_left;
	
	open (OUT, "> $file") or die $!;
	binmode (OUT);
	
	my $buffer;
	while ($length) {
		my $nowread = read(STDIN, $buffer, ($length < $BLKSIZE ? $length : $BLKSIZE))
			or close(OUT), die('read error');
		
		$length -= $nowread;
		$oekaki::content_left -= $nowread;
		print OUT $buffer;
	}
	close (OUT);
}


sub _new_oekaki_file {
	
	my $tmpdir = shift;
	
	my $tmpfile = "$tmpdir/".time.$$.'_'.(@oekaki::Pictures+1).'.tmp';
	
	my $imagedata = { tmpfile  => $tmpfile };
	push (@oekaki::Pictures, $imagedata);
	
	return $imagedata;
}

sub oekaki_pictures {
	return @oekaki::Pictures;
}

# エラー出力
sub put_oekaki_error {
	my $errormsg = shift;
	print "Content-Type: $ERROR_CONTENT_TYPE\n\n", "error\n", $errormsg, "\n";
	exit
}

sub change_error_content_type {
	@_ ? $ERROR_CONTENT_TYPE = $_[0] : $ERROR_CONTENT_TYPE;
}

# テンポラリファイルの後処理
END {
	unlink map{ $_->{tmpfile} } @oekaki::Pictures if (@oekaki::Pictures);
}

1;

