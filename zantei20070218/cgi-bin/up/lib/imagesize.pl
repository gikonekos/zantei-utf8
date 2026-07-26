package imagesize;
#
#  require 'imagesize.pl';
#  my ($w, $h, $id) = &imagesize::analyze('./hoehoe.png');
#
#  use FileHandle;
#  $image = new FileHandle ('./hoehoe.png', 'r');
#  my ($w, $h, $id) = &imagesize::analyze($image);
#
#  unless ($w or $h){ die ("$id\n"); }
#
use strict;

my %TypeMap = ( "^\x89PNG\x0D\x0A\x1A\x0A"	=> \&pngsize,
				"^\xFF\xD8"					=> \&jpegsize,
				'^GIF8[7,9]a'				=> \&gifsize);

sub analyze {
	my $stream = shift;
	
	my ($handle, $header, $save_pos, $need_close);
	
	if (ref ($stream)) {
		$handle = $stream;
		$save_pos = tell ($handle);
		seek ($handle, 0, 0);
	} else {
		$need_close = 1;
		open (FH, "< $stream") or return (undef, undef, "Can't open image file $stream: $!");
		$handle = \*FH;
	}
	
	binmode ($handle);
	my ($w, $h, $id);
	
	Analyze: {
		read ($handle, $header, 16) == 16 or ($id = 'An IO error occurred'), last Analyze;
		for (keys (%TypeMap)) {
			if ($header =~ /$_/) {
				($w, $h, $id) = &{$TypeMap{$_}}($handle);
				unless ($w or $h) {
					$id = 'Could not determine ' . uc($id) . ' size';
				}
				last Analyze;
			}
		}
		$id ||= 'Data stream is not a known image file format';
	}
	
	seek ($handle, $save_pos, 0) if ($save_pos);
	close ($handle) if ($need_close);
	
	return ($w, $h, $id);
}

sub gifsize {
	my $handle = shift;
	
	my $id = 'gif';
	
	my $SKIP_OFFSET = 6;
	my $SIZE_INFO_LENGTH = 4;
	
	my ($size_info);
	seek ($handle, $SKIP_OFFSET, 0) or return (undef, undef, $id);
	unless (read( $handle, $size_info, $SIZE_INFO_LENGTH ) == $SIZE_INFO_LENGTH) {
		return (undef, undef, $id);
	}
	
	my ($x, $y) = unpack("vv", $size_info);
	return ($x, $y, $id);
}

sub pngsize {
	my $handle = shift;
	
	my $SKIP_OFFSET = 12;
	my $CHUNK_LENGTH = 4;
	my $SIZE_INFO_LENGTH = 8;
	
	my $header;
	my $id = 'png';
	
	seek ($handle, $SKIP_OFFSET, 0) or return (undef, undef, $id);
	
	my $readlen = $CHUNK_LENGTH + $SIZE_INFO_LENGTH;
	unless (read ($handle, $header, $readlen) == $readlen) {
		return (undef, undef, $id);
	}
	my ($ihdr, $x, $y) = unpack("a4NN", $header);
	
	if ($ihdr eq 'IHDR') {	# Image Header
		return ($x, $y, 'png');
	}
	return (undef, undef, $id);
}

sub jpegsize {
	my $handle = shift;
	
	my $MARKER		= "\xFF";		# Section marker.
	
	my $SIZE_FIRST	= 0xC0; 		# Range of segment identifier codes
	my $SIZE_LAST	= 0xC3; 		#  that hold size info.
	
	my $SKIP_OFFSET = 2;
	my $SEGMENT_HEADER_LENGTH = 4;
	
	my ($segheader, $marker, $code, $length);
	my $id = 'jpg';
	
	# Dummy read to skip header ID
	seek ($handle, $SKIP_OFFSET, 0) or return (undef, undef, $id);
	
	while (1) {
		unless (read ($handle, $segheader, $SEGMENT_HEADER_LENGTH) == $SEGMENT_HEADER_LENGTH) {
			last;
		}
		# Extract the segment header.
		($marker, $code, $length) = unpack("a a n", $segheader);
		
		if ($marker ne $MARKER) {
			last;
		} elsif ((ord($code) >= $SIZE_FIRST) && (ord($code) <= $SIZE_LAST)) {
			# Segments that contain size info
			my ($size_info);
			unless (read ($handle, $size_info, 5) == 5) { last; }
			
			my ($y, $x) = unpack("xnn", $size_info);
			return ($x, $y, 'jpg');
		} else {
			seek ($handle, $length - 2, 1) or last;
		}
	}
	return (undef, undef, $id);
}

1;
