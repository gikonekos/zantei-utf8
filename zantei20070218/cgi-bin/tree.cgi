#! /usr/local/bin/perl

# 2002/05/15
# @みらい or @暫定 用のツリービュースクリプト ver0.1
# TreeNode.pmが必要ですので同じフォルダに置いてください｡
# CGI::CarpとIO::Socket,Strictも使ってます｡
#
# 2002/05/15現在には このスクリプトは
# http://saxyaka.virtualave.net/cgi-bin/a/
# においてあります｡
#
# また､以下のアドレスに実行見本があるかもしれません｡
# http://saxyaka.virtualave.net/cgi-bin/a/mirai.cgi
# http://saxyaka.virtualave.net/cgi-bin/a/zantei.cgi
#



package main;
# [2026-07-18] CGI::Carp依存除去（スタンドアロン方針、猫）。デバッグ用のブラウザエラー表示のみでコア機能に影響なし
# [2026-07-18] Perl 5.26以降、カレントディレクトリ'.'が既定で@INCから除外されたため、同じフォルダのTreeNode.pmが見つからなくなった。明示的にlib追加で対応（猫）
use FindBin;
use lib $FindBin::Bin;

$treeview::name = '＠テスト'; 
$treeview::address = 'www.ge.st98.arena.ne.jp';
$treeview::directory = 'cgi-bin/bbs.cgi';
$treeview::getnum = 200;
$treeview::log = treeview::getHTML($treeview::address);
$treeview::csv = treeview::HTMLToCSV_other($treeview::log); 

treeview::getdata();
treeview::maketree();
treeview::printtree();



package treeview;
use IO::Socket;
use TreeNode;


sub getdata 
{
	@Articles = @{$csv};
	&getformdata;
	$FORM{MaxPostid} ||= 9999999;
}

sub maketree 
{
	$TreeNodes1 = TreeNodes->new();

	# postidでソート
	@Articles = 
		map  { $_->[0] }
		sort { $a->[1] <=> $b->[1] }
		map  { [$_, $_->{postid}] }
		@Articles;

	# 記事ツリーの作成
	for my $Article (@Articles) {
		my %ArticleData = %{$Article};
	 	my $TreeNode1 = TreeNode->new($Article);
	 	$TreeNode1->ItemId($ArticleData{postid});

		# レス記事があるならば レス先の子ノードにする
		if ($ArticleData{res}) {
			my $TmpParentNode1 = $TreeNodes1->GetNode($ArticleData{res});
			if ($TmpParentNode1) {
				$TreeNodes1->AddChild($TmpParentNode1, $TreeNode1);
			} else {
				my $tmpThreadNode1 = $TreeNodes1->GetNode($ArticleData{thread});
				if ($tmpThreadNode1) {
					$TreeNodes1->AddChild($tmpThreadNode1, $TreeNode1);			
				} else {
					# レス先が見つからない場合の処理
					my %tmpArticle = (postid => $ArticleData{thread},
									  article	=> '== not found ==');
					my $tmpNode = TreeNode->new(\%tmpArticle);
					$tmpNode->ItemId($tmpArticle{postid});
					$TreeNodes1->AddChild($TreeNodes1->Root, $tmpNode);
					$TreeNodes1->AddChild($tmpNode, $TreeNode1);
				}
			}
		} else {
		# 新規投稿の場合
			$TreeNodes1->AddChild($TreeNodes1->Root, $TreeNode1);
		}
	}
	# /記事ツリーの作成

	# 記事の順番を決定
	$TreeNodes1->Root->EventSubtree(sub {
		my $self = shift;

		# $sel->Level == -1 はルートノードの特別値
		if ($self->Level == -1) {
			# サブツリー内の最新の記事番号でソート
			@{$self->Item} = 
				reverse
				map  { $_->[0] }
				sort { $a->[1] <=> $b->[1] } 
				map  { [$_, $MaxPostid = MaxPostId($_)] }
				@{$self->Item};
		} else {
			# サブツリーの大きさでソート
			if ($self->HasChildren) {
				@{$self->Item} = sort {CountRecursive($a) <=> CountRecursive($b)} @{$self->Item};
			}
		}
	});
	# /記事の順番を決定

}

sub printtree 
{
	print "Content-type: text/html\n\n";
	print '<html>';
	print '<font size=-1>';
	print $name;
	print "<form method=get>";
	print "<input name=get type='submit' value='reload'>";

	# 記事の出力
	$TreeNodes1->Root->EventSubtree(sub {
		my $self = shift;

		# Rootノードの場合､なにもしない
		if ($self->Level == -1) { return }

		# $self->Level == 0は新規投稿､レス先の消えた投稿
		if ($self->Level == 0) {
			print '<br>', @{[CountRecursive($self) + 1]};

			$MaxPostidOfSubtree = MaxPostId($self);

			print "<a href =http://$address/$directory?m=t&s=$self->{Ptr}->{postid} >◆</a>";
			if ($MaxPostidOfSubtree > $FORM{MaxPostid}) {
#				print '<font color=red>', $self->{Ptr}->{date}, '</font>', "<br>";
				print '<font color=green>', $self->{Ptr}->{date}, '</font>', "<br>";
			} else {
				print $self->{Ptr}->{date}, '<br>';
			}
		}

		print "<div style='margin-left:@{[$self->Level * 10 + 10]}'>";
		print "<a href =http://$address/$directory?m=f&s=$self->{Ptr}->{postid} >■</a>";

		if ($self->{Ptr}->{postid} > $FORM{MaxPostid}) {
#			print '<font color=red>';
			print '<font color=green>';
		} else {
			print '<font size=-1>';
		}

		if ($self->{Ptr}->{article}) {
			# 投稿記事の出力書式
			$self->{Ptr}->{article} =~ s/\0/<br>/g;
			print $self->{Ptr}->{article}, "<br>";
			if (defined $self->{Ptr}->{username} 
				&& $self->{Ptr}->{username} ne ' ' 
				&& $self->{Ptr}->{username} ne '　') {
				print ' name:', $self->{Ptr}->{username};
			}
		} else {
			# 投稿記事が空の場合
			# 書き換えネタの場合が多いです｡
			$self->{Ptr}->{res_article} =~ s/\0/<br>/g;
			print $self->{Ptr}->{res_article}, "<br>";
		}

		print '</font>';
		print "</div>\n";
	});
	# /記事の出力

	# 最新の記事番号を取得
	$MaxPostid = MaxPostId($TreeNodes1->Root);

	print "<input type='hidden' name='MaxPostid' value='$MaxPostid'>";
	print "</form>";

	# debug
	for (keys %FORM) { print "$_ => $FORM{$_}<br>\n" }
	print "</html><noembed>";

}

# サブツリーの中でもっとも大きなPostIdを返す
# MaxPostId(Node: TreeNode): Integer;
sub MaxPostId
{
	my $self = shift;
	my $max = 0;

	$self->EventSubtree(sub { 
		my $self = shift;
		$max = ($self->{Ptr}->{postid}, $max)[$self->{Ptr}->{postid} <= $max];
	});
	return $max;
}

# サブツリーの大きさを返す
# CountRecursive(Node: TreeNode): Integer;
sub CountRecursive
{
	my $self = shift;
	my $count = 0;

	$self->EventSubtree(sub {
		my $self = shift;
		if ($self->HasChildren) {
			$count += $self->Count;
		}
	});
	return $count;
}


sub getformdata
{
	my $in = $ENV{QUERY_STRING};
	for (split /&/, $in) {
		my ($name, $value) = split /=/;
		$value =~ s/\+/ /g;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack ( "C", hex ( $1 ) )/eg;
		$FORM{$name} = $value;	
	}
}

sub getHTML
{
	my $addres = shift;
	my $log;

	# HTMLデータ取得準備
	my $remote = IO::Socket::INET->new( 
			Proto => 'tcp',
			PeerAddr => $addres,
			PeerPort => '80',
	) or die "error";
	$remote->autoflush(1);

	# HTMLデータ取得
	print $remote "GET /$directory?d=$getnum HTTP/1.0\n\n";
	{local $/; $log = <$remote>}
	return $log;
}

# use strict;

####
# 記事を収めたハッシュへのポインタの配列へのポインタを返す
# ハッシュの内容
#	$hash{postid}
#	$hash{title}
#	$hash{username}
#	$hash{date}
#	$hash{res}
#	$hash{thread}
#	$hash{res_article}
#	$hash{article}
####

sub HTMLToCSV_other {
	my ($log) = @_;

	# HTMLデータ加工
	$log =~ s|[\n\r]|\0|g;
	while ($log =~ m|<A name="\d*?"></A>(.*?)<!-- -->|gm) {
		$_ = $1;

		# 1件の記事を各種データに解析し、@dataにハッシュへのポインタとして挿入 #
		my %data = ();
		($data{postid})		= m|<!-- (\d*?) -->|;
		($data{title})		= m|<FONT size="+1" color="#fffffe"><B>(.*?)</B></FONT>|;
		($data{username})	= m|投稿者：<B>(.*?)</B>|;
		($data{date})		= m|<FONT size="-1">投稿日：(.*?)<A href=|;
		($data{res})		= m|m=f&c=900&s=(\d*?)&|;
		($data{thread})		= m|<A href=".*?&s=(\d*?)&ff=" target="link">◆</A>|;
		if (m|<FONT color="#d1d1d1">(.*?)</FONT>|g) {
			$data{res_article} = $1;
			$data{res_article} =~ s|&gt; &gt; .*?\0||g;
			$data{res_article} =~ s|&gt; ||g;	
			$data{res_article} =~ s|\0| |g;		
		}

		($tmp) = m|<PRE>(.*?)</PRE>|;
		$tmp =~ s|<FONT color="#d1d1d1">.*?</FONT>||g;
		$tmp =~ s|<FONT color="#ffffff">.*?</FONT>||g;
		$tmp =~ s|<A href=([^>]*?)>参考：([^>]*?)</A>||g;
		$tmp =~ s|^[\s\0]*||g;
		$tmp =~ s|[\s\0]*$||g;
#		$tmp =~ s|\0| |g;

		$data{article} = $tmp;
		push @data, \%data;
	}	

	return \@data;
}

1;
