#!/usr/bin/perl

###################ユーザー設定####################


#チェックするURA

$checkhost = "http://www.tcn.ne.jp/~holycure/wos/country.cgi";

$checkhost2= "http://www.tcn.ne.jp/~holycure/wos/status.cgi";

#proxy

@prokusi = ("");

#HTTP_REFERER

$referer = "http://www.tcn.ne.jp/~holycure/wos/index.cgi";


#user-agent

$agent="Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)";


#Cookie

$cookie="";


#投稿回数

$toukou_max=100000000;


#投稿間隔
$sleep1=60;


#ID
$id="HolyCure";
$pass="cima45";



##################################################


for($i=0; $i<$toukou_max; $i++){
&socket();
&formget();
&socket();
&posttest();
sleep $sleep1;
}

sub socket{

# Socket モジュールを使う
use Socket;

# HTTP プロトコルを使う
#$port = getservbyname('http', 'tcp');
$port = 80;


if ( $checkhost =~ m|^http://([-_\.a-zA-Z0-9]+)/?(.*)$| ){
     $host = $1;
     $path = $2;
     } else {
print "URLは http://host/path という形式で指定してください。\n";
exit;
}

$prokusi = $prokusi[int(rand(scalar @prokusi))];


if ( $prokusi =~ m|^([-_\.a-zA-Z0-9]+):(\d+)$| ){
         $proxy = $1;
         $port2 = $2;
         $connect_host = $proxy;
     } else {
print $proxy;
print "Proxy は host:port という形式で指定してください。\n";
         exit;
}
$connect_host = $proxy;


#$iaddr = inet_aton($host)
#        or die "$hostは存在しないホストです。\n";


$iaddr = inet_aton($connect_host)
|| die "$connect_hostは存在しないホストです。\n";


# ポート番号と IP アドレスを構造体に変換
$sock_addr = pack_sockaddr_in($port2, $iaddr);

#ipアドレスに変換
$ip_address = inet_ntoa(inet_aton($host));

# ソケット生成
socket(SOCKET, PF_INET, SOCK_STREAM, 0)
         or die "ソケットを生成できません。\n";


connect(SOCKET, $sock_addr)
        or die "$checkhostのポート$portに接続できません。$prokusi\n";

# ファイルハンドル SOCKET をバッファリングしない
select(SOCKET); $|=1; select(STDOUT);
}

sub posttest{

&socket();

#----手動で
$post_mes="id=$id&pass=$pass&town=18&mode=DEF_SET";
$length=length($post_mes);

# POST
print SOCKET "POST $checkhost HTTP/1.0\r\n";
#HTTP_REFERERを送信
print SOCKET "REFERER: $referer \r\n";
#User-Agentを送信
print SOCKET "User-Agent: $agent \r\n";
print SOCKET "Accept: */* \r\n";
print SOCKET "ACCEPT-LANGUAGE: ja\r\n";
print SOCKET "Accept-ENCODING: gzip, deflate\r\n";
print SOCKET "Content-Length: $length\r\n";
print SOCKET "Content-Type: application/x-www-form-urlencoded\r\n";
print SOCKET "\r\n";
print SOCKET "$post_mes\r\n";

print while(<SOCKET>);

}

sub formget{

#----ここも手動でお願い
$post_mes="id=$id&pass=$pass&mode=STATUS";
$length=length($post_mes);

# WWWサーバにHTTPリクエストを送る
print SOCKET "POST  $checkhost2 HTTP/1.0\r\n";

#HTTP_REFERERを送信
print SOCKET "REFERER: $referer \r\n";
#User-Agentを送信
print SOCKET "User-Agent: $agent \r\n";
print SOCKET "Accept: */* \r\n";
print SOCKET "ACCEPT-LANGUAGE: ja\r\n";
print SOCKET "Accept-ENCODING: gzip, deflate\r\n";
print SOCKET "Content-Length: $length\r\n";
print SOCKET "Content-Type: application/x-www-form-urlencoded\r\n";
print SOCKET "\r\n";
print SOCKET "$post_mes\r\n";

#print while(<SOCKET>);

}
