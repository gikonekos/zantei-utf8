# /usr/bin/perl

use lib '/home/ax160/lib/i386-freebsd';
use strict;
use GD;

#幅
my $max_width  = 150;

#高さ
my $max_height = 150;

#ファミコンカラー
my @pallet_fam = (
	['ｱ0', '#7F7F7F'],
	['ｱ1', '#0000FF'],
	['ｱ2', '#0000BF'],
	['ｱ3', '#472BBF'],
	['ｱ4', '#970087'],
	['ｱ5', '#AB0023'],
	['ｱ6', '#AB1300'],
	['ｱ7', '#8B1700'],
	['ｱ8', '#533000'],
	['ｱ9', '#007800'],
	['ｱa', '#006B00'],
	['ｱb', '#005B00'],
	['ｱc', '#004358'],
	['ｱd', '#000000'],
	['ｱe', '#000001'],
	['ｱf', '#000002'],
	['ｲ0', '#BFBFBF'],
	['ｲ1', '#0078F8'],
	['ｲ2', '#0058F8'],
	['ｲ3', '#6B47FF'],
	['ｲ4', '#DB00CD'],
	['ｲ5', '#E7005B'],
	['ｲ6', '#F83800'],
	['ｲ7', '#E75F13'],
	['ｲ8', '#AF7F00'],
	['ｲ9', '#00B800'],
	['ｲa', '#00AB00'],
	['ｲb', '#00AB47'],
	['ｲc', '#008B8B'],
	['ｲd', '#000003'],
	['ｲe', '#000004'],
	['ｲf', '#000005'],
	['ｳ0', '#F8F8F8'],
	['ｳ1', '#3FBFFF'],
	['ｳ2', '#6B88FF'],
	['ｳ3', '#9878F8'],
	['ｳ4', '#F878F8'],
	['ｳ5', '#F85898'],
	['ｳ6', '#F87858'],
	['ｳ7', '#FFA347'],
	['ｳ8', '#F8B800'],
	['ｳ9', '#B8F818'],
	['ｳa', '#5BDB57'],
	['ｳb', '#58F898'],
	['ｳc', '#00EBDB'],
	['ｳd', '#787878'],
	['ｳe', '#000006'],
	['ｳf', '#000007'],
	['ｴ0', '#FFFFFF'],
	['ｴ1', '#A7E7FF'],
	['ｴ2', '#B8B8F8'],
	['ｴ3', '#D8B8F8'],
	['ｴ4', '#F8B8F8'],
	['ｴ5', '#FBA7C3'],
	['ｴ6', '#F0D0B0'],
	['ｴ7', '#FFE3AB'],
	['ｴ8', '#FBDB7B'],
	['ｴ9', '#D8F878'],
	['ｴa', '#B8F8B8'],
	['ｴb', '#B8F8D8'],
	['ｴc', '#00FFFF'],
	['ｴd', '#F8D8F8'],
	['ｴe', '#000008'],
	['ｴf', '#000009'],
);

#旧・色変換
my @pallet_old = (
	['0', '#000000'],  #black
	['1', '#1E90FF'],  #dodgerblue
	['2', '#DC143C'],  #crimson
	['3', '#FF1493'],  #deeppink
	['4', '#228B22'],  #forestgreen
	['5', '#008080'],  #teal
	['6', '#FFD700'],  #gold
	['7', '#FFA500'],  #orange
	['8', '#FFDAB9'],  #peachpuff
	['9', '#808080'],  #gray
	['w', '#C0C0C0'],  #silver
);


sub image2asciiart {
	
	
	my ($opt) = shift;
	
	my ($im, $srcw, $srch, $w, $h, $transparent, $zanpallet, $zpal_to_text, $textdata);
	
	
	if ($opt->{imagetype} eq 'jpg') {
		$im = GD::Image->newFromJpeg($opt->{filename}, 1);
	} else {
		$im = GD::Image->newFromPng($opt->{filename}, 1);
	}
	if (not $im) {
		die ("画像ファイルの読み込みに失敗しました。\n");
	}
	
	($srcw, $srch) = $im->getBounds();
	$w = $srcw;
	$h = $srch;
	if ($opt->{width} > 0 and $opt->{height} > 0) {
		$w = int ($opt->{width});
		$h = int ($opt->{height});
	} elsif ($opt->{resize} eq 'auto') {
		if ($w * $h > 3000) {
			my $r = sqrt (3000 / ($w * $h));
			$w = int ($srcw * $r);
			$h = int ($srch * $r);
		}
	} elsif ($opt->{resize} > 0 and $opt->{resize} != 100) {
		my $r = ($opt->{resize} / 100);
		$w = int ($srcw * $r);
		$h = int ($srch * $r);
	}
	$w = 1 if ($w < 1);
	$h = 1 if ($h < 1);
	if ($opt->{resize} ne 'auto' and ($w > $max_width or $h > $max_height)) {
		my ($r1, $r2, $r, $errmsg);
		$r1 = ($max_width  / $srcw) * 100;
		$r2 = ($max_height / $srch) * 100;
		$r = $r1 < $r2 ? $r1 : $r2;
		$r = $r >= 1 ? int($r) : int($r * 10) / 10;
		$errmsg .= "横 $max_width 桁、縦 $max_width 行以内になるように数値を調節してください。\n";
		$errmsg .= "（縮小比率 $r % 以内）\n";
		return (undef, $w, $h, $errmsg);
	}
	
	if ($w != $srcw or $h != $srch) {
		$im = &resize($im, $w, $h);
	}
	
	# パレットの読み込み
	($zanpallet, $zpal_to_text) = &load_zanpallet($opt->{pallet}, $opt->{mark});
	
	$transparent = $im->transparent();
	
	$textdata = '';
	for (my $y = 0; $y < $h; $y++) {
		my @tmp = ();
		
		for (my $x = 0; $x < $w; $x++) {
			
			my $index = $im->getPixel($x,$y);
			
			if ($transparent != -1 and $index == $transparent) {
				$tmp[$x] = '　';
				next;
			}
			
			my ($r, $g, $b) = $im->rgb($index);
			$index = $zanpallet->colorClosestHWB($r, $g, $b);
			
			if ($index != -1) {
				$tmp[$x] = $zpal_to_text->{$index};
			} else {
				$tmp[$x] = '？';
			}
		}
		$textdata .= join ('', @tmp) . "\n";
	}
	
	if ($opt->{cut_blank}) {
		$textdata =~ s/(?:\Q　\E)+\n/\n/g;
	}
	
	return ($textdata, $w, $h);
}


sub resize {
	
	my ($src_image, $width, $height) = @_;
	
	my ($dst_image, $srcw, $srch, $transparent);
	
	($srcw, $srch) = $src_image->getBounds();
	
	if ($transparent = $src_image->transparent() != -1) {
		$src_image->transparent(-1);
	}
	
	$dst_image = new GD::Image($width, $height, 1);
	
	if ($dst_image->copyResampled($src_image, 0, 0, 0, 0, $width, $height, $srcw, $srch) == -1) {
		die ("リサイズエラー\n");
	}
	
#&imageout($dst_image, 'resize.png');
	
	# TRUEカラーだとうまくいかない
#	if ($transparent = $src_image->transparent() != -1) {
#		my ($r, $g, $b) = $src_image->rgb($transparent);
#		my $index = $dst_image->colorExact($r, $g, $b);
#		if ($index != -1) {
#			$dst_image->transparent($index);
#		}
#	}
	
	return ($dst_image);
}


sub load_zanpallet {
	
	my ($palletname, $mark) = @_;
	
	my ($zanpallet, %zpal_to_text, %flags);
	
	$zanpallet = new GD::Image(1, 1);
	
	$palletname ||= 'all';
	if ($palletname =~ /^fam/ or $palletname =~ /^all/) {
		for (@pallet_fam) {
			my ($code, $color) = @{$_};
			if ($flags{$color}++ == 0) {
				my $index = $zanpallet->colorAllocate(&htmlc2rgb($color));
				$zpal_to_text{$index} = $code if ($index != -1);
			}
		}
		$mark = '■';
	}
	if ($palletname =~ /^old/ or $palletname =~ /^all/) {
		if ($flags{'#FFFFFF'} == 0) {
			my $index = $zanpallet->colorAllocate(255, 255, 255);
			$zpal_to_text{$index} = $mark if ($index != -1);
		}
		my $code1 = $mark eq '■' ? 'ｼ'
				  : $mark eq '●' ? 'ﾏ'
				  : $mark eq '▲' ? 'ｻ'
				  : $mark eq '▼' ? 'ﾜ'
				  : $mark eq '◆' ? 'ﾋ'
				  : $mark eq '★' ? 'ﾎ'
				  : $mark eq '旦' ? 'ﾁ' : 'ｼ';
		for (@pallet_old) {
			my ($code2, $color) = @{$_};
			if ($flags{$color}++ == 0) {
				my $index = $zanpallet->colorAllocate(&htmlc2rgb($color));
				$zpal_to_text{$index} = $code1 . $code2 if ($index != -1);
			}
		}
	}
	
	return ($zanpallet, \%zpal_to_text);
	
}


sub htmlc2rgb {
	
	my $htmlc = shift;
	my ($r, $g, $b);
	
	if ($htmlc =~ /^\#?([0-9A-Fa-f][0-9A-Fa-f])([0-9A-Fa-f][0-9A-Fa-f])([0-9A-Fa-f][0-9A-Fa-f])$/) {
		$r = hex($1);
		$g = hex($2);
		$b = hex($3);
	} else {
		warn ("&htmlc2rgb(): Invalid argument\n");
	}
	
	return ($r, $g, $b);
}


sub imageout {
	my ($im, $filename) = @_;
	open (OUT, "> $filename") or die;
	binmode (OUT);
	print OUT $im->png;
	close (OUT);
}

=debug

my %options = (
	#ファイル名
	filename => './1.png',
	
	#画像の種類
	imagetype => 'png',
	
	#幅、高さ
#	width  => 100,
#	height => 50,
	
	# 拡大比率
	resize => 'auto',
	
	#パレット名 (fam, old, all)
	pallet => 'all',
	
	#記号 (■●▲▼◆★旦)
	mark => '■',
	
	#行末の空白を除去する
	cut_blank	 => 1,
);

my $textdata = &image2asciiart(\%options);

print $textdata;

=cut

1;