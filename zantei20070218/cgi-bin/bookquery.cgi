#!/usr/local/bin/perl
# Copyright furitomo

use strict;
#use lib qw(/usr/home/it/www/lib /usr/home/it/www/mt/lib /usr/home/it/www/mt/extlib);
#use LWP::Simple qw(get head);
# [2026-07-18] CGI.pm依存除去（スタンドアロン方針、猫）
my %FORM;
{
	my $qs = $ENV{'QUERY_STRING'} || '';
	if ($ENV{'REQUEST_METHOD'} eq 'POST') {
		my $len = $ENV{'CONTENT_LENGTH'} || 0;
		read(STDIN, $qs, $len) if $len;
	}
	foreach my $pair (split(/[&;]/, $qs)) {
		my ($key, $val) = split(/=/, $pair, 2);
		next unless defined $key;
		$val = '' unless defined $val;
		foreach ($key, $val) {
			tr/+/ /;
			s/%([a-fA-F0-9]{2})/pack("C", hex($1))/eg;
		}
		$FORM{$key} = $val;
	}
}
my $asins = $FORM{'asin'};
my $content = '';

my $ProductName = '';
my $Author = '';
my $Artist = '';
my $Manufacturer = '';
my $ImageUrlMedium = '';
my $ImageUrlLarge = '';
my $OurPrice = '';
my $ErrorMsg = '';
my @ImageTypeLarge = ();
my @ImageTypeMedium = ();

print "Content-Type: text/html; charset=UTF-8\n\n";
print "<html><head><title>query book data to amazon</title></head><body>\n";

print <<'FORM_END';

<form method="get" action="./bookquery.cgi">
ENTER ASINs (split by space) 
<input type="text" name="asin" size="20">
<input type="submit" value="Search"><br>
There is restriction, 10 ASIN queries at once.
</form>
<hr>

FORM_END

my $count = 0;
foreach my $asin (split ' ', $asins){
last if $count > 9;
$count++;

if($asin){
	my $xmlurl = 'http://xml.amazon.co.jp/onca/xml3?t=webservices-20&dev-t=DMV13WJTJPPRX&locale=jp&AsinSearch='.$asin.'&type=lite&f=xml';
	$content = get($xmlurl);
#	sleep 1;

	if($content =~ /<ProductName>(.+)<\/ProductName>/) {$ProductName = $1;}
	if($content =~ /<Author>(.+)<\/Author>/) {$Author = $1;}
	if($content =~ /<Artist>(.+)<\/Artist>/) {$Artist = $1;}
	if($content =~ /<Manufacturer>(.+)<\/Manufacturer>/) {$Manufacturer = $1;}
	if($content =~ /<ImageUrlMedium>(.+)<\/ImageUrlMedium>/) {$ImageUrlMedium = $1;}
	if($content =~ /<ImageUrlLarge>(.+)<\/ImageUrlLarge>/) {$ImageUrlLarge = $1;}
	if($content =~ /<OurPrice>(.+)<\/OurPrice>/) {$OurPrice = $1;}
	if($content =~ /<ErrorMsg>(.+)<\/ErrorMsg>/) {$ErrorMsg = $1;}
}


if($ErrorMsg) {
	print "<h1>$ErrorMsg</h1>\n<hr>\n";
	$ErrorMsg = '';
	next;
}


print "<table cellspacing=\"20\"><tr>\n<td>";


if($ImageUrlLarge){
	@ImageTypeLarge = head($ImageUrlLarge);
	if($ImageTypeLarge[0] eq 'image/jpeg') {print "<a href=\"$ImageUrlLarge\">";}
}

if($ImageUrlMedium){
	@ImageTypeMedium = head($ImageUrlMedium);
	if($ImageTypeMedium[0] eq 'image/jpeg') {print "<img src=\"$ImageUrlMedium\">";}
	else {print "No image";}
}

if($ImageTypeMedium[0] eq 'image/jpeg') {print "</a>";}

print "</td>\n<td>";

if($ProductName){
	print "Product: <a href=\"http://www.amazon.co.jp/exec/obidos/ASIN/$asin/gikoneko00-22\">$ProductName</a><br>\n";
}
if($Author) {print "Author: $Author<br>\n";}
if($Artist) {print "Artist: $Artist<br>\n";}
if($Manufacturer) {print "Manufacturer: $Manufacturer<br>\n";}
if($OurPrice) {print "Amazon Price: $OurPrice<br>";}

print "</td>\n</tr></table>\n<hr>\n";

$ProductName = '';
$Author = '';
$Artist = '';
$Manufacturer = '';
$ImageUrlMedium = '';
$ImageUrlLarge = '';
$OurPrice = '';

@ImageTypeLarge = ();
@ImageTypeMedium = ();
}
#end foreach

print "</body></html>\n";
exit(0);
