#! /usr/local/bin/perl
#! c:/online/perl/bin/perl
use strict;
my $title       = 'すぷりくとヽ(´ー｀)ノ';
my $cgiurl      = 'dlist.cgi';
my $directory   = '.';
my $timezone    = 9*60*60;	# GMTからの時差
my $archive_dir = 0;		# ﾃﾞｨﾚｸﾄﾘをtar.gzipするかどうか
#my $tarcommand  = '/usr/bin/tar';
my $tarcommand  = 'tar';
my $archive_name = 'getlog.tar.gz';

sub getformdata {
    my $form = {};
    my $url_encoded_data;
#   if ($ENV{REQUEST_METHOD} eq "POST") { read(STDIN, $url_encoded_data, $ENV{CONTENT_LENGTH}) }
#   else { $url_encoded_data = $ENV{QUERY_STRING} }
    $url_encoded_data = $ENV{QUERY_STRING};
    $url_encoded_data =~ tr/+/ /;
    foreach my $pairs ( split /&/, $url_encoded_data ) {
	my ($key, $value) = split /=/, $pairs, 2;
	$value =~ s/%([0-9a-fA-F]{2})/chr(hex($1))/eg;
	$value =~ tr/\t\n\r//d;
	if($key eq 'file'){
	    $form->{$key} ||= [];
	    push(@{$form->{$key}}, $value);
	}
	else{
	    $form->{$key} = $value;
	}
    }
    $form;
}

sub indexpage {
    my $form = shift;

    print "Content-type: text/html; charset=UTF-8\n\n";
    print <<_HTML;
<HTML>
<HEAD><TITLE>$title</TITLE></HEAD>
<BODY bgcolor="#004040" text="#ffffff" link="#eeffee" vlink="#dddddd" alink="#ff0000">
<SCRIPT LANGAGE="JavaScript">
<!--
function allcheck(obj) {
  for(var i=0; i < obj.elements.length; i++){
    if( obj.elements[i].type == "checkbox"
        && obj.elements[i].name == "file" ){
      obj.elements[i].checked = obj.all.checked;
    }
  }
}
//-->
</SCRIPT>
<P><BIG><STRONG>$title</STRONG></BIG></P>
<FORM method="get" action="$cgiurl/$archive_name">
<INPUT type="hidden" name="mode" value="archive">
<TABLE border="0" width="80%">
_HTML

    my $sort = $form->{sort} || 'name';
    my $rev  = $form->{rev};
    my ($dirs,$files) = &filelist($sort,$rev);
    my @rev = ('','','');
    unless($rev){
	$rev[0] = '&rev=1' if $sort eq 'name';
	$rev[1] = '&rev=1' if $sort eq 'size';
	$rev[2] = '&rev=1' if $sort eq 'mod';
    }
    print <<_HTML;
<TR>
  <TD></TD>
  <TD colspan=2><A href="?sort=name$rev[0]">名前順</A></TD>
  <TD align="right"><A href="?sort=size$rev[1]">サイズ順</A></TD>
  <TD align="center"><A href="?sort=mod$rev[2]">日付順</A></TD>
<TR>
_HTML

    for( @$dirs ) {
	my ($dir,$size,$mod) = @{$_};
	$mod = &time2date($mod);
	my $checkbox = $archive_dir ?
	    qq|<INPUT type="checkbox" name="file" value="$dir">| : '<BIG>　</BIG>';
	print <<_HTML;
<TR>
  <TD>$checkbox</TD>
  <TD colspan=2><A href="$directory/$dir/">$dir/</A></TD>
  <TD align="right">-</TD>
  <TD align="center">$mod</TD>
</TR>
_HTML
    }
    for(@$files) {
	my ($file,$size,$mod) = @{$_};
#	1 while $size =~ s/(\d)(\d\d\d)(?!\d)/$1,$2/;
	1 while $size =~ s/(.*\d)(\d\d\d)/$1,$2/;
	$mod = &time2date($mod);
	my $file2 = $file;
	$file2 .= '.txt' if $file !~ /\.txt$/;
	print <<_HTML;
<TR>
  <TD><INPUT type="checkbox" name="file" value="$file"></TD>
  <TD><A href="$directory/$file">$file</A></TD>
  <TD><A href="$cgiurl/$file2?f=$file&amp;mode=get">[VIEW]</A></TD>
  <TD align="right">$size byte</TD>
  <TD align="center">$mod</TD>
</TR>
_HTML
    }
    print <<_HTML;
<TR>
  <TD><INPUT TYPE="checkbox" name="all" onClick="allcheck(this.form)"></TD>
  <TD colspan=4>すべてチェック (要JavaScript)</TD>
</TR>
<TR><TD colspan=3 align="center"></TD></TR>
</TABLE>
<INPUT type="submit" value="tar.gzで一括ダウンロード">
</FORM>
<HR>
</BODY></HTML>
_HTML
}
sub time2date {
    my $mtime = shift;
    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime($mtime + $timezone);
    return sprintf("%02d/%02d/%02d %02d:%02d",
		    $year+1900,$mon+1,$mday,$hour,$min);
}


sub filelist {
    my ($sort,$reverse) = @_;
    my (@dirs, @files);
    for my $file ( &directory() ){
	my ($type,$size,$mod) = &filestat("$directory/$file");
	if   ( $type =~ /d/ ){ push(@dirs, [$file, $size, $mod]); }
	elsif( $type =~ /f/ ){ push(@files,[$file, $size, $mod]); }
    }
    my $subroutine =
	$sort eq 'size' ? sub{$b->[1] <=> $a->[1]} :
	$sort eq 'mod'  ? sub{$b->[2] <=> $a->[2]} :
			  sub{$a->[0] cmp $b->[0]};
    @dirs  = sort $subroutine @dirs;
    @files = sort $subroutine @files;
    if($reverse){
	@dirs  = reverse @dirs;
	@files = reverse @files;
    }
    return( \@dirs, \@files );
}

sub filestat{
    my $file  = shift;
    my @stat  = stat $file;
    my $size  = $stat[7];
    my $mtime = $stat[9];
    my $type  = -d _ ? 'd' :
		-f _ ? 'f' : undef;
    return($type,$size,$mtime);
}

sub directory {
    opendir(DIR, $directory)
	or &error_html('ディレクトリが開けませんでした。');
    my @list = grep !/^\.\.?$/, readdir(DIR);
    closedir(DIR);
    return(@list);
}

sub printfile {
    my $file = shift;
    if( $file =~ m#[/|<>+&\\:]#){ &error_html( 'ファイルが開けませんでした。' ) }
    if(! -f "$directory/$file" ){ &error_html( 'ファイルが開けませんでした。' ) }
    open (FILE, "< $directory/$file\0")	or die $!;

    my $buf; my $bufsize = 4*1024;
    print "Content-type: text/plain\n\n";
    while( read (FILE, $buf, $bufsize) ){
	print $buf;
    }
    close (FILE);
}

sub archive {
    my $form = shift;
    my @list;
    my %checked = map{ $_, 1 } @{ $form->{file} };
    for( &directory() ){
	next unless( $checked{$_} );
	if (-f "$directory/$_" or ($archive_dir && -d _)){
	    push(@list,$_);
	}
    }
    if(@list == 0){ &error_html( 'ファイルが指定されていません。' ); }

    $| = 1;
    print "Content-type: application/x-tar\n";
    print "Content-encoding: x-gzip\n\n";
    system( $tarcommand, '-cvzf', '-', @list );
}

sub error_html {
    my $errmsg = shift;
    print "Content-type: text/html\n\n";
    print <<_HTML;
<HTML>
<HEAD><TITLE>エラー</TITLE></HEAD>
<BODY bgcolor="#004040" text="#ffffff" link="#eeffee" vlink="#dddddd" alink="#ff0000">
<BIG>$errmsg</BIG>
</BODY></HTML>
_HTML

    exit;
}

Main:{
    my $form = &getformdata();
    if   ($form->{mode} eq 'archive') {
	&archive($form);
    }
    elsif($form->{mode} eq 'get') {
#	my $file = $ENV{'PATH_INFO'};
#       $file =~ s#^/##;
	my $file = $form->{f};
	&printfile($file);
    }
    else {
	&indexpage($form);
    }
    exit;
}

