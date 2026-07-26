package multipart;
#
# multipart.pl (2002-11-07)
#
# multipart/form-data を受け取る
# ヘッダの処理がちょっと適当かも
#
# require 'multipart.pl';
# @uploadfiles = &multipart::get_multipart(\&func_storeform, $tmpdir);
# @uploadfiles = &multipart::upload_files();
#
#
# ファイル名に「ソ」「十」「表」などの第二バイト目が0x5C(\)の文字（シフトJISで）
# が含まれているとファイル名をうまく取り出せないバグ（仕様）があります。
#
use strict;

my $CRLF = "\x0D\x0A";
my $BLKSIZE = 4 * 1024;
@multipart::UploadFiles = ();

# マルチパートデータ読み込み
sub get_multipart {
	
	my ($func_storeform, $tmpdir) = @_;
	$tmpdir ||= '/tmp';
	
	local ($multipart::buffer, $multipart::left);
	$multipart::buffer = '';
	$multipart::left = $ENV{'CONTENT_LENGTH'};
	
	# boundaryの取得
	my ($boundary) = $ENV{'CONTENT_TYPE'} =~ /boundary=\"?([^\";,]+)\"?/;
	if ( !defined ($boundary) or length ($boundary) > 256 ) {
		die("Boundary not provided\n");
	}
	$boundary = "--" . $boundary
		unless $ENV{'HTTP_USER_AGENT'} =~ /MSIE\s+3\.0[12];\s*Mac/i;
	
	binmode(STDIN);
	
	while (<STDIN>) {
		$multipart::left -= length();
		last if /$boundary$CRLF/o;
	}
	
  Multipart:
	while (!&_end_of_multipart()) {
		my ($header, $cd, $ct);
		
		# ヘッダ読み込み
		&_readblock(\$header, "${CRLF}${CRLF}") or last Multipart;
		
		foreach (split ($CRLF, $header)) {
			/^Content-Disposition:\s+(.*)/i and do{ $cd = $1; next };
			/^Content-Type:\s+(.*)/i		and do{ $ct = $1; next };
		}
		my ($field) = $cd =~ /\bname="?([^\";]+)"?/;
		my ($fname) = $cd =~ /\bfilename="?([^\";]+)"?/;
		
		unless (defined ($field)) { $field = 'unknown'; }
		
		if ($fname) {	# 添付ファイル
			my $upload = &_new_upload_file($fname, $ct, $field, $tmpdir);
			
			open(UPLOAD, "> $upload->{tmpfile}")
				or die("添付ファイルの出力に失敗しました\n");
			binmode(UPLOAD);
			
			# ボディー読み込み
			&_readblock(\*UPLOAD, "${CRLF}$boundary") or last Multipart;
			
			close(UPLOAD);
		} else {
			my ($value);
			&_readblock (\$value, "${CRLF}$boundary") or last Multipart;
			&$func_storeform($field, $value);
		}
	}
	return @multipart::UploadFiles;
}

sub _end_of_multipart {
	# 「--CRLF」が最後に残るから 4
	($multipart::left + length($multipart::buffer) <= 4 ) ? 1 : 0;
}


# デリミタまで読み込む
sub _readblock {
	# $out はスカラーかファイルハンドルのリファレンス
	my ($out, $delimiter) = @_;
	
	my ($write, $found, $ishandle);
	$found = 0;
	$write = '';
	$ishandle = ref($out) eq 'SCALAR' ? 0 : 1;
	
	until ($found) {
		# ブロックサイズよりフォームの残りが少なくなったら、それ。
		my $readbyte = ($multipart::left < $BLKSIZE) ? $multipart::left : $BLKSIZE;
		
		if ($readbyte > 0) {		# バッファに読み込み
			my $len = read (STDIN, $multipart::buffer, $readbyte, length($multipart::buffer))
				or die ("malformed multipart POST\n");
			$multipart::left -= $len;
		}
		
		my $pos = index ($multipart::buffer, $delimiter);  # デリミタを探す
		if ($pos >= 0) {
			# デリミタまでを$writeに移す。（デリミタを除いて）
			$write = substr ($multipart::buffer, 0, $pos);
			substr ($multipart::buffer, 0, $pos + length($delimiter)) = '';
			
			$found++;
		} else {
			die ("malformed multipart POST\n") unless ($readbyte > 0);
			
			# バッファの最後にデリミタの先頭部が含まれる可能性が有るので
			# その部分を除いて$writeに移す。
			my $remove = length ($multipart::buffer) - length ($delimiter) + 1;
			$write = substr ($multipart::buffer, 0, $remove);
			substr ($multipart::buffer, 0, $remove) = '';
		}
		
		# $outに出力
		$ishandle ? print($out $write) : ($$out .= $write);
	}
	$found;
}


# アップロードファイルの情報
sub _new_upload_file {
	my ($filename, $mimetype, $field, $tmpdir, $basename, $tmpfile);
	
	($filename, $mimetype, $field, $tmpdir) = @_;
	
	# ファイル名だけ取り出す。
	($basename) = $filename =~ /^(?:.*[:\\\/])?([^:\\\/]+)/;
	
	$tmpfile = "$tmpdir/".time.$$.'_'.(@multipart::UploadFiles+1).'.tmp';
	
	my $upload_data = {
		filename => $filename,
		field    => $field,
		basename => $basename,
		mimetype => $mimetype,
		tmpfile  => $tmpfile,
	};
	push (@multipart::UploadFiles, $upload_data);
	
	return $upload_data;
}

# アップロードファイルのリスト
sub upload_files {
	return @multipart::UploadFiles;
}

# テンポラリファイルの後処理
END {
	unlink map{ $_->{tmpfile} } @multipart::UploadFiles if (@multipart::UploadFiles);
}

1;