#! /usr/local/bin/perl

# ログのファイル名
$logfilename2 = './r1.txt';

# ログの保存件数
$logsave2 = 1000;


$| = 1;

( $sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime ( time );
$year += 1900;
$mon++;
$nowdate = sprintf ( "%d/%02d/%02d(%s)%02d時%02d分%02d秒", 
  $year, $mon, $mday, 
  ( '日', '月', '火', '水', '木', '金', '土' )[$wday],
  $hour, $min, $sec );

	%ENVLIST = (
		
		'AUTH_TYPE',				$ENV{'AUTH_TYPE'},
		'CONTENT_LENGTH',			$ENV{'CONTENT_LENGTH'},
		'CONTENT_TYPE',				$ENV{'CONTENT_TYPE'},
		'HTTP_ACCEPT',				$ENV{'HTTP_ACCEPT'},
		'HTTP_ACCEPT_CHARSET',		$ENV{'HTTP_ACCEPT_CHARSET'},
		'HTTP_ACCEPT_ENCODING',		$ENV{'HTTP_ACCEPT_ENCODING'},
		'HTTP_ACCEPT_LANGUAGE',		$ENV{'HTTP_ACCEPT_LANGUAGE'},
		'HTTP_CACHE_CONTROL',		$ENV{'HTTP_CACHE_CONTROL'},
		'HTTP_CACHE_INFO',			$ENV{'HTTP_CACHE_INFO'},
		'HTTP_CLIENT_IP',			$ENV{'HTTP_CLIENT_IP'},
		'HTTP_CONNECTION',			$ENV{'HTTP_CONNECTION'},
		'HTTP_COOKIE',				$ENV{'HTTP_COOKIE'},
		'HTTP_FORWARDED',			$ENV{'HTTP_FORWARDED'},
		'HTTP_FROM',				$ENV{'HTTP_FROM'},
		'HTTP_HOST',				$ENV{'HTTP_HOST'},
		'HTTP_PROXY_AUTHORIZATION',	$ENV{'HTTP_PROXY_AUTHORIZATION'},
		'HTTP_PROXY_CONNECTION',	$ENV{'HTTP_PROXY_CONNECTION'},
		'HTTP_REFERER',				$ENV{'HTTP_REFERER'},
		'HTTP_SP_HOST',				$ENV{'HTTP_SP_HOST'},
		'HTTP_UA_COLOR',			$ENV{'HTTP_UA_COLOR'},
		'HTTP_UA_CPU',				$ENV{'HTTP_UA_CPU'},
		'HTTP_UA_OS',				$ENV{'HTTP_UA_OS'},
		'HTTP_UA_PIXELS',			$ENV{'HTTP_UA_PIXELS'},
		'HTTP_USER_AGENT',			$ENV{'HTTP_USER_AGENT'},
		'HTTP_VIA',					$ENV{'HTTP_VIA'},
		'HTTP_X_FORWARDED_FOR',		$ENV{'HTTP_X_FORWARDED_FOR'},
		'HTTP_X_LOCKING',			$ENV{'HTTP_X_LOCKING'},
		'QUERY_STRING',				$ENV{'QUERY_STRING'},
		'REMOTE_ADDR',				$ENV{'REMOTE_ADDR'},
		'REMOTE_HOST',				$ENV{'REMOTE_HOST'},
		'REMOTE_IDENT',				$ENV{'REMOTE_IDENT'},
		'REMOTE_PORT',				$ENV{'REMOTE_PORT'},
		'REMOTE_USER',				$ENV{'REMOTE_USER'},
		'REQUEST_METHOD',			$ENV{'REQUEST_METHOD'},
		'REQUEST_URI',				$ENV{'REQUEST_URI'},
		'SCRIPT_NAME',				$ENV{'SCRIPT_NAME'},
		'SCRIPT_URI',				$ENV{'SCRIPT_URI'},
		'SCRIPT_URL',				$ENV{'SCRIPT_URL'},
	);

	if ( $ENVLIST{'REMOTE_ADDR'} eq $ENVLIST{'REMOTE_HOST'}
	  || $ENVLIST{'REMOTE_HOST'} eq '' ) {
		$ENVLIST{'REMOTE_HOST'} = gethostbyaddr
		  ( pack ( 'C4', split ( /\./, $ENVLIST{'REMOTE_ADDR'} ) ), 2 ) ||
		  $ENVLIST{'REMOTE_ADDR'};
	}
	
	if ( $ENVLIST{'HTTP_CACHE_CONTROL'} ne '' )		{ $proxyflg = 1; }
	if ( $ENVLIST{'HTTP_CACHE_INFO'} ne '' )			{ $proxyflg += 2; }
	if ( $ENVLIST{'HTTP_CLIENT_IP'} ne '' )			{ $proxyflg += 4; }
	if ( $ENVLIST{'HTTP_FORWARDED'} ne '' )			{ $proxyflg += 8; }
	if ( $ENVLIST{'HTTP_FROM'} ne '' )					{ $proxyflg += 16; }
	if ( $ENVLIST{'HTTP_PROXY_AUTHORIZATION'} ne '' )	{ $proxyflg += 32; }
	if ( $ENVLIST{'HTTP_PROXY_CONNECTION'} ne '' )		{ $proxyflg += 64; }
	if ( $ENVLIST{'HTTP_SP_HOST'} ne '' )				{ $proxyflg += 128; }
	if ( $ENVLIST{'HTTP_VIA'} ne '' )					{ $proxyflg += 256; }
	if ( $ENVLIST{'HTTP_X_FORWARDED_FOR'} ne '' )		{ $proxyflg += 512; }
	if ( $ENVLIST{'HTTP_X_LOCKING'} ne '' )			{ $proxyflg += 1024; }
	if ( $ENVLIST{'HTTP_USER_AGENT'} =~ /cache|delegate|gateway|httpd|proxy|squid|via/i ) {
		$proxyflg += 2048;
	}
	if ( $host =~ /^dns|^dummy|^ns|gate|cache|proxy|www/i ) {
		$proxyflg += 4096;
	}
	
	$realaddr = '';
	$realhost = '';
	if ( $proxyflg > 0 ) {
		
		if ( $ENVLIST{'HTTP_X_FORWARDED_FOR'} =~
		  s/^(\d+)\.(\d+)\.(\d+)\.(\d+).*/$1.$2.$3.$4/ ) {
			$realaddr = "$1.$2.$3.$4";
		} elsif ( $ENVLIST{'HTTP_FORWARDED'} =~ 
		  s/.*\s(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ ) {
			$realaddr = "$1.$2.$3.$4";
		} elsif ( $ENVLIST{'HTTP_VIA'} =~
		  s/.*\s(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ ) {
			$realaddr = "$1.$2.$3.$4";
		} elsif ( $ENVLIST{'HTTP_CLIENT_IP'} =~
		  s/(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ ) {
			$realaddr = "$1.$2.$3.$4";
		} elsif ( $ENVLIST{'HTTP_SP_HOST'} =~
		  s/(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ ) {
			$realaddr = "$1.$2.$3.$4";
		} elsif ( $ENVLIST{'HTTP_FORWARDED'} =~ s/.*\sfor\s(.+)/$1/ ) {
			$realhost = "$1";
		} elsif ( $ENVLIST{'HTTP_FROM'} =~ s/\-\@(.+)/$1/ ) {
			$realhost = "$1";
		}
		
		if ( $realaddr eq '' && $realhost ne '' ) {
			$realpackaddr = gethostbyname ( $realhost );
			( $a, $b, $c, $d ) = unpack ( 'C4', $realpackaddr );
			$realaddr = "$a.$b.$c.$d";
		}
		
		if ( $realaddr eq '' ) {
			$anonyproxyflg = 1;
		} else {
			if ( $realhost eq '' ) {
				$realhost = $realaddr;
			}
		}
	}

# ここから記録処理

$envr=$ENV{'HTTP_REFERER'};
$envh=$ENV{'REMOTE_HOST'};
$enva=$ENV{'HTTP_USER_AGENT'};
$addrk = $ENV{'REMOTE_ADDR'};
$hostk = gethostbyaddr(pack("C4", split(/\./, $addrk)), 2);


		$record = "[$nowdate] $ENVLIST{'HTTP_REFERER'} - $ENVLIST{'REMOTE_HOST'} - $ENVLIST{'REMOTE_ADDR'} - $ENVLIST{'HTTP_VIA'} - $realaddr - $ENVLIST{'HTTP_USER_AGENT'}\n";



$ENVLIST{'HTTP_USER_AGENT'} =~ s/</&lt;/g;
$ENVLIST{'HTTP_USER_AGENT'} =~ s/>/&gt;/g;
$ENVLIST{'HTTP_USER_AGENT'} =~ s/"/&quot;/g;#style対策
$ENVLIST{'HTTP_REFERER'} =~ s/</&lt;/g;
$ENVLIST{'HTTP_REFERER'} =~ s/>/&gt;/g;
$ENVLIST{'HTTP_REFERER'} =~ s/"/&quot;/g;#style対策

open ( LOG, "+<$logfilename2" );
eval 'flock ( LOG, 2 )';
seek ( LOG, 0, 0 );
@logdata = <LOG>;
if ( @logdata >= $logsave2 ) {
	@logdata = @logdata[0 .. $logsave2 - 2];
}
unshift ( @logdata, $record );
seek ( LOG, 0, 0 );
truncate ( LOG, 0 );
print LOG @logdata;
eval 'flock ( LOG, 8 )';
close ( LOG );




1;

__END__
