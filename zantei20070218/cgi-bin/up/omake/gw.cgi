#!/usr/bin/perl
# 変更する場合: ##!/usr/local/bin/perl
#
# gw.cgi
#   何らかの理由で直接ファイルをダウンロードさせたくない場合に使用する
#
# 使用方法
#   upload.cgiの設定を以下のように変更します
#   $STORE_URL = "http://hoehoe.com/uploader/gw.cgi/";
#
#   $ENV{PATH_INFO}が使えないとき
#   $STORE_URL = "http://hoehoe.com/uploader?gw.cgi/";
#
#
use strict;
my ($STORE_DIR, $ACCESS_CONTROL, @EXCEPT_REFERER);

### 初期設定 ###

# アップロードデータの格納先ディレクトリ
$STORE_DIR = './stored';

# アクセス制限用データファイル
$ACCESS_CONTROL = './data/deny.file';

# 指定したサイトから参照を禁止する
@EXCEPT_REFERER = (
#	'http://ime.nu/',
);

################
$STORE_DIR =~ s|/$||;


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


# 拡張子からMIMEタイプを取得
sub getmimetype_bysuffix {
	my $name = shift;
	my $suffix = $name =~ /\.([^\.]+)$/ ? lc ($1) : lc ($name);
	
	while (<DATA>) {
		s/\#.*//;
		next if /^$/;
		chop;
		my ($type, @extensions) = split (/\s/, $_);
		
		if (grep { $_ eq $suffix } @extensions) {
			return $type;
		}
	}
	return undef;
}


# エラーページを表示
sub error_page {
	my $status = shift || 200;
	
	my $server_software = 
		$ENV{SERVER_SOFTWARE} =~ /([^\/]+\/\d[\d\.]*)/ ? $1 : $ENV{SERVER_SOFTWARE};
	
	my %reason_phrase = (
		200 => 'OK',
		400 => 'Bad Request',
		403 => 'Forbidden',
		404 => 'Not Found',
		500 => 'Internal Server Error',
	);
	print <<_EOF;
Content-Type: text/html
Status: $status $reason_phrase{$status}

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<HTML><HEAD>
<TITLE>$status $reason_phrase{$status}</TITLE>
</HEAD><BODY>
<H1>$reason_phrase{$status}</H1>
<HR>
<ADDRESS>$server_software Server at $ENV{SERVER_NAME} Port $ENV{SERVER_PORT}</ADDRESS>
</BODY></HTML>
_EOF
	exit;
}


GATEWAY: {
	
	if ($ACCESS_CONTROL ne '' and !&checkdomain($ACCESS_CONTROL)) {
		&error_page(403);
	}
	if (@EXCEPT_REFERER and !&checkreferer(\@EXCEPT_REFERER)) {
		&error_page(403);
	}
	
	my ($filename, $use_querystring);
	if ($ENV{QUERY_STRING} ne '') {
		unless ($ENV{QUERY_STRING} =~ m{^([^:\\\/|<>+&]+)$}) {
			&error_page(400);
		}
		$use_querystring = 1;
		$filename = $1;
	} elsif ($ENV{PATH_INFO} ne '') {
		unless ($ENV{PATH_INFO} =~ m{^/([^:\\\/|<>+&]+)$}) {
			&error_page(400);
		}
		$filename = $1;
	} else {
		&error_page(400);
	}
	
	my $filepath = $STORE_DIR . '/' . $filename;
	
	unless ((-f $filepath) && open (FILE, "< $filepath\0")) {
		&error_page(404);
	}
	binmode (FILE);
	
	my $size = -s _;
	my $type = &getmimetype_bysuffix($filename) || 'application/octet-stream';
	
	print "Content-type: $type\n";
	print "Content-Disposition: inline; filename=\"$filename\"\n" if ($use_querystring);
	print "Content-Length: $size\n\n";
	
	my $blksize = 1024*16;
	my $buf = '';
	while (read (FILE, $buf, $blksize)) {
		print $buf;
	}
	close (FILE);
	exit;
}


__DATA__
application/EDI-Consent
application/EDI-X12
application/EDIFACT
application/activemessage
application/andrew-inset	ez
application/applefile
application/atomicmail
application/batch-SMTP
application/cals-1840
application/commonground
application/cybercash
application/dca-rft
application/dec-dx
application/eshop
application/http
application/hyperstudio
application/iges
application/index
application/index.cmd
application/index.obj
application/index.response
application/index.vnd
application/iotp
application/ipp
application/mac-binhex40	hqx
application/mac-compactpro	cpt
application/macwriteii
application/marc
application/mathematica
application/mathematica-old
application/msword		doc
application/news-message-id
application/news-transmission
application/ocsp-request
application/ocsp-response
application/octet-stream	bin dms lha lzh exe class
application/oda			oda
application/pdf			pdf
application/pgp-encrypted
application/pgp-keys
application/pgp-signature
application/pkcs10
application/pkcs7-mime
application/pkcs7-signature
application/pkix-cert
application/pkix-crl
application/pkixcmp
application/postscript		ai eps ps
application/prs.alvestrand.titrax-sheet
application/prs.cww
application/prs.nprend
application/remote-printing
application/riscos
application/sdp
application/set-payment
application/set-payment-initiation
application/set-registration
application/set-registration-initiation
application/sgml
application/sgml-open-catalog
application/slate
application/smil		smi smil
application/vemmi
application/vnd.3M.Post-it-Notes
application/vnd.FloGraphIt
application/vnd.accpac.simply.aso
application/vnd.accpac.simply.imp
application/vnd.acucobol
application/vnd.anser-web-certificate-issue-initiation
application/vnd.anser-web-funds-transfer-initiation
application/vnd.audiograph
application/vnd.businessobjects
application/vnd.bmi
application/vnd.canon-cpdl
application/vnd.canon-lips
application/vnd.claymore
application/vnd.commerce-battelle
application/vnd.commonspace
application/vnd.comsocaller
application/vnd.contact.cmsg
application/vnd.cosmocaller
application/vnd.cups-postscript
application/vnd.cups-raster
application/vnd.cups-raw
application/vnd.ctc-posml
application/vnd.cybank
application/vnd.dna
application/vnd.dpgraph
application/vnd.dxr
application/vnd.ecdis-update
application/vnd.ecowin.chart
application/vnd.ecowin.filerequest
application/vnd.ecowin.fileupdate
application/vnd.ecowin.series
application/vnd.ecowin.seriesrequest
application/vnd.ecowin.seriesupdate
application/vnd.enliven
application/vnd.epson.esf
application/vnd.epson.msf
application/vnd.epson.quickanime
application/vnd.epson.salt
application/vnd.epson.ssf
application/vnd.ericsson.quickcall
application/vnd.eudora.data
application/vnd.fdf
application/vnd.ffsns
application/vnd.framemaker
application/vnd.fujitsu.oasys
application/vnd.fujitsu.oasys2
application/vnd.fujitsu.oasys3
application/vnd.fujitsu.oasysgp
application/vnd.fujitsu.oasysprs
application/vnd.fujixerox.ddd
application/vnd.fujixerox.docuworks
application/vnd.fujixerox.docuworks.binder
application/vnd.fut-misnet
application/vnd.grafeq
application/vnd.groove-account
application/vnd.groove-identity-message
application/vnd.groove-injector
application/vnd.groove-tool-message
application/vnd.groove-tool-template
application/vnd.groove-vcard
application/vnd.hp-HPGL
application/vnd.hp-PCL
application/vnd.hp-PCLXL
application/vnd.hp-hpid
application/vnd.hp-hps
application/vnd.httphone
application/vnd.hzn-3d-crossword
application/vnd.ibm.MiniPay
application/vnd.ibm.modcap
application/vnd.informix-visionary
application/vnd.intercon.formnet
application/vnd.intertrust.digibox
application/vnd.intertrust.nncp
application/vnd.intu.qbo
application/vnd.intu.qfx
application/vnd.is-xpr
application/vnd.japannet-directory-service
application/vnd.japannet-jpnstore-wakeup
application/vnd.japannet-payment-wakeup
application/vnd.japannet-registration
application/vnd.japannet-registration-wakeup
application/vnd.japannet-setstore-wakeup
application/vnd.japannet-verification
application/vnd.japannet-verification-wakeup
application/vnd.koan
application/vnd.lotus-1-2-3
application/vnd.lotus-approach
application/vnd.lotus-freelance
application/vnd.lotus-notes
application/vnd.lotus-organizer
application/vnd.lotus-screencam
application/vnd.lotus-wordpro
application/vnd.mcd
application/vnd.mediastation.cdkey
application/vnd.meridian-slingshot
application/vnd.mif		mif
application/vnd.minisoft-hp3000-save
application/vnd.mitsubishi.misty-guard.trustweb
application/vnd.mobius.daf
application/vnd.mobius.dis
application/vnd.mobius.msl
application/vnd.mobius.plc
application/vnd.mobius.txf
application/vnd.motorola.flexsuite
application/vnd.motorola.flexsuite.adsi
application/vnd.motorola.flexsuite.fis
application/vnd.motorola.flexsuite.gotap
application/vnd.motorola.flexsuite.kmr
application/vnd.motorola.flexsuite.ttc
application/vnd.motorola.flexsuite.wem
application/vnd.mozilla.xul+xml
application/vnd.ms-artgalry
application/vnd.ms-asf
application/vnd.ms-excel	xls
application/vnd.ms-lrm
application/vnd.ms-powerpoint	ppt
application/vnd.ms-project
application/vnd.ms-tnef
application/vnd.ms-works
application/vnd.msign
application/vnd.music-niff
application/vnd.musician
application/vnd.netfpx
application/vnd.noblenet-directory
application/vnd.noblenet-sealer
application/vnd.noblenet-web
application/vnd.novadigm.EDM
application/vnd.novadigm.EDX
application/vnd.novadigm.EXT
application/vnd.osa.netdeploy
application/vnd.pg.format
application/vnd.pg.osasli
application/vnd.powerbuilder6
application/vnd.powerbuilder6-s
application/vnd.powerbuilder7
application/vnd.powerbuilder7-s
application/vnd.powerbuilder75
application/vnd.powerbuilder75-s
application/vnd.previewsystems.box
application/vnd.publishare-delta-tree
application/vnd.rapid
application/vnd.s3sms
application/vnd.seemail
application/vnd.shana.informed.formdata
application/vnd.shana.informed.formtemplate
application/vnd.shana.informed.interchange
application/vnd.shana.informed.package
application/vnd.street-stream
application/vnd.svd
application/vnd.swiftview-ics
application/vnd.triscape.mxs
application/vnd.trueapp
application/vnd.truedoc
application/vnd.ufdl
application/vnd.uplanet.alert
application/vnd.uplanet.alert-wbxml
application/vnd.uplanet.bearer-choi-wbxml
application/vnd.uplanet.bearer-choice
application/vnd.uplanet.cacheop
application/vnd.uplanet.cacheop-wbxml
application/vnd.uplanet.channel
application/vnd.uplanet.channel-wbxml
application/vnd.uplanet.list
application/vnd.uplanet.list-wbxml
application/vnd.uplanet.listcmd
application/vnd.uplanet.listcmd-wbxml
application/vnd.uplanet.signal
application/vnd.vcx
application/vnd.vectorworks
application/vnd.visio
application/vnd.wap.sic
application/vnd.wap.slc
application/vnd.wap.wbxml	wbxml
application/vnd.wap.wmlc	wmlc
application/vnd.wap.wmlscriptc	wmlsc
application/vnd.webturbo
application/vnd.wrq-hp3000-labelled
application/vnd.wt.stf
application/vnd.xara
application/vnd.xfdl
application/vnd.yellowriver-custom-menu
application/whoispp-query
application/whoispp-response
application/wita
application/wordperfect5.1
application/x-bcpio		bcpio
application/x-cdlink		vcd
application/x-chess-pgn		pgn
application/x-compress
application/x-cpio		cpio
application/x-csh		csh
application/x-director		dcr dir dxr
application/x-dvi		dvi
application/x-futuresplash	spl
application/x-gtar		gtar
application/x-gzip
application/x-hdf		hdf
application/x-javascript	js
application/x-koan		skp skd skt skm
application/x-latex		latex
application/x-netcdf		nc cdf
application/x-sh		sh
application/x-shar		shar
application/x-shockwave-flash	swf
application/x-stuffit		sit
application/x-sv4cpio		sv4cpio
application/x-sv4crc		sv4crc
application/x-tar		tar
application/x-tcl		tcl
application/x-tex		tex
application/x-texinfo		texinfo texi
application/x-troff		t tr roff
application/x-troff-man		man
application/x-troff-me		me
application/x-troff-ms		ms
application/x-ustar		ustar
application/x-wais-source	src
application/x400-bp
application/xml
application/zip			zip
audio/32kadpcm
audio/basic			au snd
audio/l16
audio/midi			mid midi kar
audio/mpeg			mpga mp2 mp3
audio/prs.sid
audio/telephone-event
audio/tone
audio/vnd.cns.anp1
audio/vnd.cns.inf1
audio/vnd.digital-winds
audio/vnd.everad.plj
audio/vnd.lucent.voice
audio/vnd.nortel.vbk
audio/vnd.nuera.ecelp4800
audio/vnd.nuera.ecelp7470
audio/vnd.octel.sbc
audio/vnd.qcelp
audio/vnd.rhetorex.32kadpcm
audio/vnd.vmx.cvsd
audio/x-aiff			aif aiff aifc
audio/x-pn-realaudio		ram rm
audio/x-pn-realaudio-plugin	rpm
audio/x-realaudio		ra
audio/x-wav			wav
chemical/x-pdb			pdb
chemical/x-xyz			xyz
image/bmp			bmp
image/cgm
image/g3fax
image/gif			gif
image/ief			ief
image/jpeg			jpeg jpg jpe
image/naplps
image/png			png
image/prs.btif
image/prs.pti
image/tiff			tiff tif
image/vnd.cns.inf2
image/vnd.dwg
image/vnd.dxf
image/vnd.fastbidsheet
image/vnd.fpx
image/vnd.fst
image/vnd.fujixerox.edmics-mmr
image/vnd.fujixerox.edmics-rlc
image/vnd.mix
image/vnd.net-fpx
image/vnd.svf
image/vnd.wap.wbmp		wbmp
image/vnd.xiff
image/x-cmu-raster		ras
image/x-portable-anymap		pnm
image/x-portable-bitmap		pbm
image/x-portable-graymap	pgm
image/x-portable-pixmap		ppm
image/x-rgb			rgb
image/x-xbitmap			xbm
image/x-xpixmap			xpm
image/x-xwindowdump		xwd
message/delivery-status
message/disposition-notification
message/external-body
message/http
message/news
message/partial
message/rfc822
message/s-http
model/iges			igs iges
model/mesh			msh mesh silo
model/vnd.dwf
model/vnd.flatland.3dml
model/vnd.gdl
model/vnd.gs-gdl
model/vnd.gtw
model/vnd.mts
model/vnd.vtu
model/vrml			wrl vrml
multipart/alternative
multipart/appledouble
multipart/byteranges
multipart/digest
multipart/encrypted
multipart/form-data
multipart/header-set
multipart/mixed
multipart/parallel
multipart/related
multipart/report
multipart/signed
multipart/voice-message
text/calendar
text/css			css
text/directory
text/enriched
text/html			html htm
text/plain			asc txt
text/prs.lines.tag
text/rfc822-headers
text/richtext			rtx
text/rtf			rtf
text/sgml			sgml sgm
text/tab-separated-values	tsv
text/t140
text/uri-list
text/vnd.DMClientScript
text/vnd.IPTC.NITF
text/vnd.IPTC.NewsML
text/vnd.abc
text/vnd.curl
text/vnd.flatland.3dml
text/vnd.fly
text/vnd.fmi.flexstor
text/vnd.in3d.3dml
text/vnd.in3d.spot
text/vnd.latex-z
text/vnd.motorola.reflex
text/vnd.ms-mediapackage
text/vnd.wap.si
text/vnd.wap.sl
text/vnd.wap.wml		wml
text/vnd.wap.wmlscript		wmls
text/x-setext			etx
text/xml			xml
video/mpeg			mpeg mpg mpe
video/pointer
video/quicktime			qt mov
video/vnd.fvt
video/vnd.motorola.video
video/vnd.motorola.videop
video/vnd.vivo
video/x-msvideo			avi
video/x-sgi-movie		movie
x-conference/x-cooltalk		ice
