#!/usr/bin/perl
# 変更する場合: ##!/usr/local/bin/perl

###############################################################################
#  リンク欄
###############################################################################

require './config.txt';

#

$bgc='#004040';


print  "Content-type: text/html\n\n";
print  "<HTML>\n<HEAD><TITLE>暫定リンク</TITLE></HEAD>\n";
print  "<BODY bgcolor=\"#004040\" text=\"#ffffff\" link=\"#eeffee\" vlink=\"#dddddd\" alink=\"#ff0000\">\n";

&linklineorg;

print  "</BODY>\n";
print  "</HTML>\n";

exit;

__END__
