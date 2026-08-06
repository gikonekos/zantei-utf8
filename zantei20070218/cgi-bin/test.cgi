#!/usr/bin/perl
# 変更する場合: ##!/usr/local/bin/perl

###############################################################################
#  だうそ
###############################################################################

#

$bgc='#004040';
require './gikoneko.pl';

print  "Content-type: text/html\n\n";
print  "<HTML>\n<HEAD><TITLE>だうそ！</TITLE></HEAD>\n";
print  "<BODY bgcolor=\"#004040\" text=\"#ffffff\" link=\"#eeffee\" vlink=\"#dddddd\" alink=\"#ff0000\">\n";

print '<blockquote><pre>';

for ( $i = 0 ; $i < 40 ; $i++ ) {

$k= (rand(20) * 4) + 1 ;
$l= 100 ;

print "<Marquee behavior=\"alternate\" direction=\"up\" height=\"$l\"><Marquee direction=\"right\" scrollamount=\"$k\" truespeed>";
&gikoneko;
print  "</marquee></marquee>\n\n";
}

print '</pre></blockquote>';
print  "</BODY>\n";
print  "</HTML>\n";

exit;

__END__
