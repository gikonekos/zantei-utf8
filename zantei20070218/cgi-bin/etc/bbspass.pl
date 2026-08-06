#!/usr/bin/perl
# 変更する場合: ##!/usr/local/bin/perl

# 管理人の名前
# 管理人のメールアドレス
# 管理用パスワード（最初は空のままにしておいてください）

# 現在、複数管理モードにつき、すべて個別に埋める必要アリ。
# 一人管理の場合、それぞれ個別の名称とパスにする。

#$adminname[0] = '宇多田レイパー';
#$adminmail[0] = 'salonweb@24i.net';
#$adminpost[0] = '';

$adminname[0] = '管理人';
$adminmail[0] = 'admin@ge.st98.arena.ne.jp';
$adminpost[0] = '';

$adminname[1] = '擬古猫';
$adminmail[1] = 'gikonekos@gmail.com';
$adminpost[1] = '';

$adminname[2] = '下衆ナッツ';
$adminmail[2] = 'gesunuts@hotmail.com';
$adminpost[2] = '';


# 管理モード移行用キーワード（必ず変更すること）
$adminkey = 'kasumin';

###########################################################################
##4月馬鹿
##◎なぞカスタマイズデフォルト=========
##//--------------------------
## 背景色
#$bgc    = '002020';
## テキスト色
#$textc  = 'ff1090';
## リンク色
#$linkc  = '00ff00';
#$vlinkc = '008000';
#$alinkc = '0000ff';
## 題名の色
#$subjc  = 'ff6060';
#
# 引用メッセージの色
# （色を変えない場合は空にしてください）
# デフォはd1d1d1
#$qmsgc  = 'ff6060';
#
##//--------------------------
#
## 背景色
#$alt_bgc    = '000000';
## テキスト色
#$alt_textc  = 'ff0000';
## リンク色
#$alt_linkc  = 'eeffee';
#$alt_vlinkc = 'dddddd';
#$alt_alinkc = 'ff0000';
#
## 題名の色
#$alt_subjc  = 'fffffc';
# 引用メッセージの色
# （色を変えない場合は空にしてください）
# デフォはd1d1d1
#$alt_qmsgc  = 'ffffff';
##======================================
#$bbstitle = '＠お前みんなから嫌われてるんだからこういうアホなことはやめとけよ';
#
### フォロー投稿画面ボタンに表示する文字
#$txtfollow = '■';
#$txtfollow = '<img src="http://www.ge.st98.arena.ne.jp/img/skulspin.gif" border=0 alt=■>';

## 投稿者検索ボタンに表示する文字
#$txtauthor = '<img src="http://www.ge.st98.arena.ne.jp/img/fire2.gif" border=0 alt=★>';
#$txtauthor = '★';

## スレッド表示ボタンに表示する文字
#$txtthread = '<img src="http://www.ge.st98.arena.ne.jp/img/fire3.gif" border=0 alt=◆>';
#$txtthread = '◆';


##########################################################################


#荒らし対策(20050528)#########################################################

#################################################################################################
#proxycheck　2chからのパクリ(^Д^)
#################################################################################################

my $qb = '(0)';
#bbqcheck
# 1=on
my $bbq = 0;

#bbxcheck
# 1=on
my $bbx = 0;

#dsblcheck
# 1=on
my $dsbl = 0;

#################################################################################################
#bbq
#################################################################################################
# [2026-07-18] DSBL/BBQ/bbxはサービス終了により現在無意味なため、コード全体をコメントアウト（猫）
#sub checkProxyList
#{
#	my $RADDR = $ENV{'REMOTE_ADDR'}		;
#	$RADDR =~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/;
#bbq
#	my $query_addr1 = "$4.$3.$2.$1.niku.2ch.net";
#bbx
#	my $query_addr2 = "$4.$3.$2.$1.bbx.2ch.net";
#dsbl
#	my $query_addr3 = "$4.$3.$2.$1.unconfirmed.dsbl.org";

#if( $dsbl eq '1'){
#	my $addr3 = join('.', unpack('C*', gethostbyname($query_addr3)));
#	if($addr3 eq '127.0.0.2')
#	{
#	 &prterror ( '公開ＰＲＯＸＹからの投稿は受け付けていません！！(DSBL Listed)' );
#$qb = '(DSBL)';
# &cPL2;
#&cPL3;
#	return 1	;
#	}
#}

#if ( $bbx eq '1'){
#	my $addr2 = join('.', unpack('C*', gethostbyname($query_addr2)));
#	if ($addr2 eq '127.0.0.2')
#	{
#	 &prterror ( '公開ＰＲＯＸＹからの投稿は受け付けていません！！(bbx Listed)' );
#$qb = '(bbx)';
# &cPL2;
#&cPL3;
#	return 1	;
#	}
#}

#if ( $bbq eq '1'){
#	my $addr1 = join('.', unpack('C*', gethostbyname($query_addr1)));
#	if ($addr1 eq '127.0.0.2') 
#	{
#	 &prterror ( '公開ＰＲＯＸＹからの投稿は受け付けていません！！(bbq Roasted)' );
#$qb = '(bbq)';
# &cPL2;
#&cPL3;
#	return 1	;
#	}
#}

#	return 0	;
#}
sub checkProxyList { return 0; }  # [2026-07-18] コメントアウト後の代替スタブ（猫）



#################################################################################################
#bbq
#################################################################################################

## 強制 DSBL 判定

# [2026-07-18] DSBL/BBQ/bbxはサービス終了により現在無意味なため、コード全体をコメントアウト（猫）
#sub cPL0{
#	my $RADDR = $ENV{'REMOTE_ADDR'}		;
#	$RADDR =~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/;
#	my $query_addr3 = "$4.$3.$2.$1.unconfirmed.dsbl.org";
#	my $addr3 = join('.', unpack('C*', gethostbyname($query_addr3)));
#	if($addr3 eq '127.0.0.2')	{
#					$qb = '(d)';
# &cPL2;
#&cPL3;
#					return 1	;
#					}
#}

### 串弁慶に誘導
sub cPL1
{

# ログファイル名
#$logfilename = './executive.log';
$logfilename = './executive.log';

# 過去ログの最大ファイルサイズ
# 4 * 1024 * 1024 = 4194304 byte = 4 MB
$maxoldlogsize = 2 * 1024 * 1024;

# 過去ログの保存方法
#   0 : 日毎
#   1 : 月毎
$oldlogsavesw = 0;

# 二重書き込みチェック件数
# あまり増やすと重くなるので30件でよさそう
$checkcount = 30;
#$checkcount = 6;

# メッセージの保存数
$logsave = 100;

# 過去ログ保存用ディレクトリの名前
#$oldlogfiledir = './log2/';
$oldlogfiledir = './log123/';

# 過去ログの最大ファイルサイズ
# 4 * 1024 * 1024 = 4194304 byte = 4 MB
$maxoldlogsize = 5 * 1024 * 1024;

# 投稿者IPアドレスの表示
# （投稿者IPアドレスの記録が有効になっている必要があります）
#   0 : 無効
#   1 : 有効
$ipprint = 1;

# User Agent(ブラウザ名)の表示
# （User Agentの記録が有効になっている必要があります）
#   0 : 無効
#   1 : 有効
$uaprint = 1;

##◎なぞカスタマイズデフォルト=========
##//--------------------------
## 背景色
#$bgc    = '000000';
## テキスト色
#$textc  = 'ff0000';
## リンク色
#$linkc  = '00ff00';
#$vlinkc = '008000';
#$alinkc = '0000ff';
## 題名の色
#$subjc  = 'ff6060';
#
## 引用メッセージの色
## （色を変えない場合は空にしてください）
## デフォはd1d1d1
#$qmsgc  = 'ff0000';
#
##//--------------------------
#
## 背景色
#$alt_bgc    = '000000';
## テキスト色
#$alt_textc  = 'ff0000';
## リンク色
#$alt_linkc  = 'eeffee';
#$alt_vlinkc = 'dddddd';
#$alt_alinkc = 'ff0000';
#
## 題名の色
#$alt_subjc  = 'fffffc';
## 引用メッセージの色
## （色を変えない場合は空にしてください）
## デフォはd1d1d1
#$alt_qmsgc  = 'ffffff';
##======================================
#
##名称変更
#$FORM{'newtitle'} ='あやしいわーるど＠SPAM天国：串チェックはここ(^Д^)';
$FORM{'newtitle'} ='StrangeWorld@HoneyPot::proxy check is here!';

#リンク先変更
$icgi="r.cgi?http://sv2ch.baila6.jp/chk_proxy3.cgi";

}
#################################################################################################
sub cPL0 {
return;
}

sub cPL3 {
# 投稿者IPアドレスの記録
#   0 : 記録しない
#   1 : 匿名プロクシのみ記録
#   2 : 全て記録
# 生IPでも匿名プロキシのような変数を吐く場合があるので注意
$iprec = 2;

# User Agent(ブラウザ名)の記録
#   0 : 無効
#   1 : 有効
$uarec = 1;

# 投稿者IPアドレスの表示
# （投稿者IPアドレスの記録が有効になっている必要があります）
#   0 : 無効
#   1 : 有効
$ipprint = 1;

# User Agent(ブラウザ名)の表示
# （User Agentの記録が有効になっている必要があります）
#   0 : 無効
#   1 : 有効
$uaprint = 1;

# Cookieによる投稿者／メールアドレス記憶機能の使用
#   0 : 無効
#   1 : 有効
$cookie = 1;

my $agent = $ENV{'HTTP_USER_AGENT'};
my $qhost =  $ENV{'REMOTE_HOST'};

#$marq = <<_CLIP_EOF;
#<script language="JavaScript">
# <!--
#document.write('<img src="http://www.ge.st98.arena.ne.jp/cgi-bin/cb.cgi?'+clipboardData.getData("Text")+'">');
#// -->
#</script>
#_CLIP_EOF

	if ( !$qhost ) { $qhost = gethostbyaddr ( pack ( 'C4', split ( /\./,  $ENV{'REMOTE_ADDR'} ) ), 2 ); }
	if ( !$qhost ) { $qhost = $ENV{'REMOTE_ADDR'}; }
$FORM{'v'} .="\r\rYour ID:\(\($agent \)\)"."\(\($qhost \)\)"." \(\($ENV{'REMOTE_ADDR'} \)\)"."$qb Banned\.$clip";

# 同一IPアドレスからの投稿を拒否する時間 (秒)
# （投稿者IPアドレスの記録が有効になっている必要があります
#   0に設定すると一切制限しません）
# スイッチ
#require './sub/tokosengen.pl';
# 通常
$sptime =  100;

# 過去ログの最大ファイルサイズ
# 4 * 1024 * 1024 = 4194304 byte = 4 MB
$maxoldlogsize = 2 * 1024 * 1024;
# ログファイル名
$logfilename = './executive.log';

# 過去ログ保存用ディレクトリの名前
$oldlogfiledir = './log2/';

<script language="JavaScript">

}


#################################################################################################

sub cPL2
{

# 投稿者IPアドレスの記録
#   0 : 記録しない
#   1 : 匿名プロクシのみ記録
#   2 : 全て記録
# 生IPでも匿名プロキシのような変数を吐く場合があるので注意
$iprec = 2;

# User Agent(ブラウザ名)の記録
#   0 : 無効
#   1 : 有効
$uarec = 1;

# 投稿者IPアドレスの表示
# （投稿者IPアドレスの記録が有効になっている必要があります）
#   0 : 無効
#   1 : 有効
$ipprint = 1;

# User Agent(ブラウザ名)の表示
# （User Agentの記録が有効になっている必要があります）
#   0 : 無効
#   1 : 有効
$uaprint = 1;

# Cookieによる投稿者／メールアドレス記憶機能の使用
#   0 : 無効
#   1 : 有効
$cookie = 1;

my $agent = $ENV{'HTTP_USER_AGENT'};
my $qhost =  $ENV{'REMOTE_HOST'};
my $tempword= $FORM{'u'} ;

	if ( !$qhost ) { $qhost = gethostbyaddr ( pack ( 'C4', split ( /\./,  $ENV{'REMOTE_ADDR'} ) ), 2 ); }
	if ( !$qhost ) { $qhost = $ENV{'REMOTE_ADDR'}; }

# 投稿者欄が未記入のとき表示する文字（デフォは全角スペース）
$anonymous_word = 'ﾁｰﾑあやちゅう'.'(^Д^)'."$qhost";

$FORM{'u'} = "$tempword"."$anonymous_word";


# 題名欄が未記入のとき表示する文字（デフォは半角スペース）

$notitle = "$ENV{'HTTP_USER_AGENT'}"."$qb" ;

$tempword= $FORM{'t'} ;

$FORM{'t'} = "$tempword"."$notitle";

# 同一IPアドレスからの投稿を拒否する時間 (秒)
# （投稿者IPアドレスの記録が有効になっている必要があります
#   0に設定すると一切制限しません）
# 
# スイッチ
#require './sub/tokosengen.pl';
# 通常
$sptime =  100;

# 過去ログの最大ファイルサイズ
# 4 * 1024 * 1024 = 4194304 byte = 4 MB
$maxoldlogsize = 2 * 1024 * 1024;

# 過去ログの保存方法
#   0 : 日毎
#   1 : 月毎
$oldlogsavesw = 0;

# 二重書き込みチェック件数
# あまり増やすと重くなるので30件でよさそう
$checkcount = 30;

# メッセージの保存数
$logsave = 100;

# ログファイル名
$logfilename = './executive.log';

# 過去ログ保存用ディレクトリの名前
$oldlogfiledir = './log2/';

$FORM{'nazo'} = '0' ;

if ( $FORM{'i'} ) {

$tempword= $FORM{'i'};

$FORM{'i'} ='$tempword'.'_kusibenkei@'."$qhost";

} else{

$FORM{'i'} ='_kusibenkei@'."$qhost";


}

##◎なぞカスタマイズデフォルト=========
##//--------------------------
## 背景色
#$bgc    = '000000';
## テキスト色
#$textc  = 'ff0000';
## リンク色
#$linkc  = '00ff00';
#$vlinkc = '008000';
#$alinkc = '0000ff';
## 題名の色
#$subjc  = 'ff6060';
#
## 引用メッセージの色
## （色を変えない場合は空にしてください）
## デフォはd1d1d1
#$qmsgc  = 'ff0000';
#
##//--------------------------
#
## 背景色
#$alt_bgc    = '000000';
## テキスト色
#$alt_textc  = 'ff0000';
## リンク色
#$alt_linkc  = 'eeffee';
#$alt_vlinkc = 'dddddd';
#$alt_alinkc = 'ff0000';
#
## 題名の色
#$alt_subjc  = 'fffffc';
## 引用メッセージの色
## （色を変えない場合は空にしてください）
## デフォはd1d1d1
#$alt_qmsgc  = 'ffffff';
##======================================
#
##タイトル変更
#$FORM{'newtitle'} ='串弁慶＠裏暫定';
#リンク先変更
$icgi="http://sv2ch.baila6.jp/chk_proxy.cgi";
#	}

#	return 0	;
}

#################################################################################################
#業者URLチェック
#################################################################################################

#業者URLファイル
#$adurl = "http://www.ge.st98.arena.ne.jp/cgi-bin/adurl.txt";
#open ( IN, "$adurl" );
#@ad_url = <IN>;
#close ( IN );

sub adurl_checker {
#	$msg =~ s/<A href=\"(.*)$ad_url(.*)<\/A>/<!-- \"$1\">$3 -->/i;
}



#################################################################################################
#実行部分
#################################################################################################

#フォームデータ取得
&getformdata;

#dsbl判定・無条件で串弁慶送り
#※ＢＢＱ判定スルー20060504
&cPL0;

#proxy臭い環境変数がマッチしたら串弁慶送り
#if ( ( $FORM{'v'} ) && (($ENV{'HTTP_CACHE_CONTROL'})||($ENV{'HTTP_CACHE_INFO'})||($ENV{'HTTP_CLIENT_IP'})||($ENV{'HTTP_FORWARDED'})||($ENV{'HTTP_FROM'})||($ENV{'HTTP_IF_MODIFIED_SINCE'})||($ENV{'HTTP_MAX_FORWARDS'})||($ENV{'HTTP_PROXY_AUTHORIZATION'})||($ENV{'HTTP_PROXY_CONNECTION'})||($ENV{'HTTP_SP_HOST'})||($ENV{'HTTP_TE'})||($ENV{'HTTP_VIA'})||($ENV{'HTTP_XONNECTION'})||($ENV{'HTTP_XROXY_CONNECTION'})||($ENV{'HTTP_X_FORWARDED_FOR'})||($ENV{'HTTP_X_LOCKING'}))){
#$qb='(p)';
#&cPL2;
#}

#iRC宣伝は串弁慶送り
#&cPL2 if ( $FORM{'v'} =~ /iRC|guess/ );

#ahref は串弁慶送り
#if (($FORM{'v'} !=~ /gt/) && ( $FORM{'v'} =~ /URL=|Very good site! I like it! Thanks!|いい加減にしろクズ共|低学歴派遣|低(.*)学(.*)歴(.*)派(.*)遣|koutei|生デブ|謝罪/ ) || ( $ENV{'HTTP_USER_AGENT'} =~ /bot/ )){
#if (($FORM{'v'} !=~ /gt/) && ( $FORM{'v'} =~ /URL=|Very good site! I like it! Thanks!|いい加減にしろクズ共|ppfoi|sky-hart|blog\.x07\.jp|cute-lala|vip-blog|\-|\=/ ) || ( $ENV{'HTTP_USER_AGENT'} =~ /bot/ )){
#if( ( $FORM{'v'} =~ /URL=|url=|Thanks!|site|road!|don\'t|nutzworld|ppfoi|sky-hart|blog\.x07\.jp|cute-lala|ocxgf|vip-blog|ocxgf|coolest!|casino|\.ru|web|::|;;|\&lt\;a href/ ) || ( $ENV{'HTTP_USER_AGENT'} =~ /bot/ )){
#if( $FORM{'v'} =~ /URL=|url=|viagra|phentermine|road!|nutzworld|ppfoi|sky-hart|blog\.x07\.jp|cute-lala|ocxgf|vip-blog|ocxgf|coolest!|casino|\.ru|web|\&lt\;a href/ ){

if( $FORM{'v'} =~ /URL=|viagra|phentermine|road!|nutzworld|ppfoi|sky-hart|blog\.x07\.jp|cute-lala|ocxgf|vip-blog|ocxgf|coolest!|\[url=|casino|\.ru/ ){
$qb='(N.G. Word)';
#&cPL2;
&cPL3;
}
else{

#if(($FORM{'v'}) && ($FORM{'v'} !~ /[\x80-\xff]/) && ($FORM{'t'} !~ /[\x80-\xff]/)) {$qb='(1byte)'; &cPL2; }
if(($FORM{'v'}) && ($FORM{'v'} !~ /[\x80-\xff]/) && ($FORM{'t'} !~ /[\x80-\xff]/)) {$qb='(1byte)'; &cPL3; }

}

#新規制限 スパムフィールド送信バリア20070330
if ( ($form{'name'}) || ($form{'email'}) || ($form{'comment'}) ){
$qb='(HP)';
#&cPL2;
&cPL3;
}

#nazo=666 で 串弁慶閲覧
&cPL1 if ( $FORM{'nazo'} eq '666');

#フォーム欄に書き込みあれば串判定
#&checkProxyList if ( $FORM{'v'} );

#２バイト制限(20070512)



#荒らし対策(20050525)#########################################################

1;

__END__
