#!/usr/bin/perl
# 変更する場合: ##!/usr/local/bin/perl

=comment
くずはスクリプト用のtree表示スクリプト ver0.9 (03/05/12)


-- これは何ですか? --

くずはスクリプトの記事をツリー型に表示するためのモジュールです。



-- 使用法 --

このファイルをsubフォルダに置き、
bbs.cgiの1400行目付近を以下のようにします。

# tree表示
if ($FORM{'tree'}) {
	require './sub/ks_treeview.pl';
	$prtmessage = output_treeview($bmsg, $msgtop);
}

bbs.cgi?tree=on でtreeview用の表示ができます。


+ 変更(2003/09/21)
- 本家暫定むけ変更(2003/11/12)
=cut

###############################################################################
#  設定
###############################################################################

my %treeview = (
  # 枝の色
  'color_branch' => $FORM{color_branch} || 'ffffff',

  # 新規記事の色
  'color_newmsg' => $FORM{color_newmsg} || 'ffccaa',

);



###############################################################################
#  ツリー型で出力するための関数
###############################################################################

sub treeview {
	
# @logdata, %logdata, %kids, はグローバル変数
	loadmessage();
	
	@logdata = grep {
		my $log = $_;
		my $threadnum = (split m/,/)[3];
		my $postid = (split m/,/)[1];
		$threadnum == $FORM{'s'} or $postid == $FORM{'s'};
	} @logdata;
	
	&prthtmlhead ( "$bbstitle 投稿検索" );
	
	print <<EOF;
<A name="top"><A href="#bottom">$txt_go_bottom</A></A>
 <A href="$cgiurl?d=$FORM{'d'}&c=$FORM{'c'}${ZANTEI_EXTRA}${Zanzan_EXTRA}${TREE_ON}${TREE_EXTRA}" accesskey="$accesskey_reset">掲示板へ($accesskey_reset)</A>
 <A href="$cgiurl?m=g&d=$FORM{'d'}&c=$FORM{'c'}${ZANTEI_EXTRA}${Zanzan_EXTRA}${TREE_ON}${TREE_EXTRA}" accesskey="$accesskey_getlog">過去ログへ($accesskey_getlog)</A>
<HR>
EOF
	print output_treeview(0, 1);
	
	print <<EOF;
<A name="bottom"><A href="#top">$txt_go_top</A></A>
 <A href="$cgiurl?d=$FORM{'d'}&c=$FORM{'c'}${ZANTEI_EXTRA}${Zanzan_EXTRA}${TREE_ON}${TREE_EXTRA}" accesskey="$accesskey_reset">掲示板へ($accesskey_reset)</A>
 <A href="$cgiurl?m=g&d=$FORM{'d'}&c=$FORM{'c'}${ZANTEI_EXTRA}${Zanzan_EXTRA}${TREE_ON}${TREE_EXTRA}" accesskey="$accesskey_getlog">過去ログへ($accesskey_getlog)</A>
 </BODY></HTML>
EOF
	exit;
}


###############################################################################
# $head件目から $tail件目のツリーを出力する
###############################################################################

sub output_treeview {
	
	my ($head, $tail) = @_;
	my $output;
	
	%logdata		= make_hash_logdata(@logdata);
	%kids			= make_kids(@logdata);
	my @threadID	= get_threadID(@logdata);
	
	@threadID = map {$_->[0]} sort {$b->[1] <=> $a->[1]} map { [ $_ => max_postID($_) ] } @threadID;
	
	$tail = $#threadID >= $tail ? $tail : $#threadID;
	@threadID = @threadID[$head .. $tail];
	
	for my $threadID (@threadID) {
		my $max_postID = max_postID($threadID);
		my $ndate = (split m|,|, $logdata{$max_postID})[0];		
		if ( $FORM{meload} and defined $FORM{'p'} and $max_postID <= $FORM{'p'}) { last; }
		
		my @tmp = enum_postID($threadID);
		my $count = @tmp;
		
		$output .= qq|<div class="${CSSclass}Treearticle"><tt><font size="+0">　<a href="$cgiurl?m=t&s=$threadID&d=$FORM{'d'}&p=$toppostid&c=$FORM{'c'}${ZANTEI_EXTRA}${Zanzan_EXTRA}${TREE_ON}${TREE_EXTRA}" target="$searchwinname">$txtthread</a>$count [ 更新日：@{[ getnowdate($ndate) ]} ]</font></tt><br><br>|;
		@header = ('　');
		
		$output .= output_tree($threadID);
		$output .= "<hr></div>\n";
	}
	return $output;
}


###############################################################################
# 1つのツリーを出力する
###############################################################################

sub output_tree {
	
	my $node = shift;
	my $output = '';
	
	# 出力
	$output .= output_node($node);
	
	# 子があるなら
	if (q_article($node, 'has_child')) {
		for my $node (@{ $kids{$node} }) { $output .= output_tree($node) }
		pop @header;
	}
	return $output;
}


###############################################################################
# 1つのノードを出力する
###############################################################################

sub output_node {
	
	my $node = shift;
	my ( $msgcolor, $msg_headder, $temp, $mode, );
	
#	my ($ndate, $postid, $protect, $thread, $phost, $agent, $user, $mail, $title, $msg) = split(m|,|, $logdata{$node});
	my ($ndate, $postid, $protect, $thread, $phost, $agent, $user, $mail, $title, $msg) = getmessage_treeview($logdata{$node});
	
	if ( !$followwin ) {
		$newwin = " target=\"$followwinname\"";
	} else {
		$newwin = '';
	}
	
	my $res_button = qq(<a href="$cgiurl?m=f&d=$FORM{'d'}&p=$toppostid&s=$postid\&c=$FORM{'c'}&$ks_param->{get}" $newwin>$txtfollow</a>);	
####
$defaultuser = '　';
$defaulttitle = ' ';

	if ( $msg ne "== not_found ==" ) {
		# メールアドレス
		if ( $mail ) {
			$user = "<A href=\"mailto\:$mail\">$user<\/A>";
		}

		if ( ( $user eq $defaultuser ) && ( $title ne $defaulttitle ) && ( $title !~ /^＞/ ) ) {
			$msg_headder = qq(<FONT color="#$CC{'subj'}"> 題名: <B>$title</B></FONT>\n);
		}
		
		if ( ( $user ne $defaultuser ) && ( $title ne $defaulttitle ) && ( $title !~ /^＞/ ) ) {
			$msg_headder = qq(投稿者: $user <FONT color="#$CC{'subj'}"> 題名: <B>$title</B></FONT>\n);
		}
		
		if ( ( $user ne $defaultuser ) && ( ( $title eq $defaulttitle ) || ( $title =~ /^＞/ ) ) ) {
			$msg_headder = qq(投稿者: $user\n);
		}
	}
	# 参考を消す
#	s|<A href=[^>]*?>参考：[^>]*?</A>||g;
	if ( $thread ) {
		my @lines  = split( "\r", $msg );
		undef $lines[$#lines];
		undef $lines[$#lines - 1];
		$msg = join ( "\r", @lines );
	}
####
	$_ = $msg;
####
	s/\r/\n/g;
	
	if ( $FORM{'m'} eq 'tree' ) {
		$mode = 1;
	} else { 
		$mode = 0;
	}
	if ( $dispqmsgline[$mode] ne '2' ) {
		# 2つ前の返信を消す
#		s|&gt; &gt;.*?\0\0?||g;
		s/^&gt; &gt;.*?\n\n?//mg;
		
		# 1つ前の返信を消す
		if ( $dispqmsgline[$mode] eq '1' ) {
#			if (s|(&gt;.*?)\0\0||g) { $pre_msg = $1; }
#			if (s|(&gt; .*?)\n\n?||g) { $pre_msg = $1; }
			if (s|^(&gt; .*?)\n\n?||mg) { $pre_msg = $1; }
		} else {
#			s|&gt;.*?\0\0?||g;
			s/^&gt; .*?\n\n?//mg;
		}
	}
	
	# 記事
	my $article = $_;
	$article =~ s/\0//g;
	$article =~ s/\s//g;
	
# 掲示板表示モードかつ、投稿文が$FORM{'collimit'}桁以上なら省略・非表示する
	if ( ( $FORM{'collimit'} ) && ( ( $FORM{'m'} eq 'p' ) || ( $FORM{'m'} eq '' ) || ( $FORM{'m'} eq 'o' ) || ( $FORM{'m'} eq 'op' ) || ( $FORM{'m'} eq 'on' ) || ( $FORM{'m'} eq 'n' ) ) ) {
		$temp = $_;
		my @lines  = split( "\n", $temp );
		foreach ( @lines ) {
			if ( ( length ( $_ ) > $FORM{'collimit'} ) ) {
				if ( ( $_ =~ m|(<A href=\"m=f\S+\">).*<\/A>|i ) || ( $_ =~ m|(<A href=".*" target="link">)[^<*]|i ) ) {
					if ( ( length ( $_ ) - length ( $1 ) - 4 ) > $FORM{'collimit'} ) {
						if ( !$colswitchu ) {
							$temp = '省略'."\n";
						} else {
							$temp = "";
						}
						last;
					}
				} else {
					if ( !$colswitchu ) {
						$temp = '省略'."\n";
					} else {
						$temp = "";
					}
					last;
				}
			}
		}
		$_ = $temp;
	}
# 掲示板表示モードかつ、投稿文が$FORM{'linelimit'}行以上なら省略・非表示する
	if ( ( $FORM{'linelimit'} ) && ( ( $FORM{'m'} eq 'p' ) || ( $FORM{'m'} eq '' ) || ( $FORM{'m'} eq 'o' ) || ( $FORM{'m'} eq 'op' ) || ( $FORM{'m'} eq 'on' ) || ( $FORM{'m'} eq 'n' ) ) ) {
		my @lines  = split( "\n", $_ );
		if ( ( @lines > $FORM{'linelimit'} ) && ( @lines > 3 ) ) {
			$msg_head = $lines[0];
			$msg_body = "\n[" . ( @lines - 2 ) . '行省略]' . "\n";
			$msg_tail = $lines[$#lines];
			undef ( @lines );
			@lines = ( $msg_head, $msg_body, $msg_tail, "\n" ) if ( !$lineswitchu );
			$_ = join ( "\n", @lines );
		}
	}
	
####
#	if ( ( $ENV{'REMOTE_ADDR'} ne '220.110.236.67' ) && ( $phost eq '220.110.236.67' ) ) {
#		$_ = '';
#	}
####
	$_ = $msg_headder . $_;
	s|\n|\0|g;
	
	# 投稿文末尾の連続する改行をトリミング
#	s|[\0]{2,}$|\0|g;
	s|\0+$||g;
	
#### ノード間を一行詰めて表示する場合
	if ( !$nodeclose[$mode] ) {
		$_ .= "\0";
	}
	
	# 半角空白を&nbsp;に変換
	s/ /&nbsp;/g;
	# A、FONTタグ対応
	s/<A&nbsp;href/<A href/ig;
	s/&nbsp;target="/ target="/ig;
	s/<FONT&nbsp;/<FONT /ig;
####
	
	q_article($node, 'is_last')
		? push @header, qq(<font color="#$treeview{color_branch}">└$res_button</font>)
		: push @header, qq(<font color="#$treeview{color_branch}">├$res_button</font>);
	
	q_article($node, 'is_root')  and  $header[-1] = qq(<font color="#$treeview{color_branch}">&nbsp;&nbsp;$res_button</font>);
	
	my $head = join '', @header;
	pop @header;
	
	if (q_article($node, 'has_child') and q_article($node, 'is_last')) {
		push @header, qq(<font color="#$treeview{color_branch}">　│</font>);
	} elsif (q_article($node, 'has_child') and not q_article($node, 'is_last')) {
		push @header, qq(<font color="#$treeview{color_branch}">││</font>);	
	} elsif (not q_article($node, 'has_child') and q_article($node, 'is_last')) {
		push @header, qq(<font color="#$treeview{color_branch}">　　</font>);
	} elsif (not q_article($node, 'has_child') and not q_article($node, 'is_last')) {
		push @header, qq(<font color="#$treeview{color_branch}">│　</font>);
	}
	
	my $body = join '', @header;
	
	s|\0|<br>\n$body|g;
	
	
	# 子があるなら自分の頭を'│'に変える
	q_article($node, 'has_child')  and  $header[-1] = qq(<font color="#$treeview{color_branch}">│</font>);
	
	# 末の子なら自分の頭を'　'に変える
	q_article($node, 'is_last')  and  $header[-1] = '　';
	
	# 子がいないならポップ
	not q_article($node, 'has_child')  and  pop @header;
	
	# 新着記事なら色を変える
#### m=treeの場合は新着記事の色変えをしない
	if ( $FORM{'m'} ne 'tree' ) {
		$msgcolor = (defined $FORM{p} and $postid > $FORM{p}) ? $treeview{color_newmsg} : $CC{'text'};
	} else {
		$msgcolor = $CC{'text'};
	}
####
	
	if ($article eq '') { 
		$pre_msg .= "\0" if ( $msg_headder );
		$pre_msg =~ s|\0|<br>\n$body|g;
		if ( $msg_headder ) {
			$_ .= $pre_msg;
		} else {
			$head .= $pre_msg;
		}
	}
	return qq(\n<tt><font size="+0" color="#$msgcolor">\n$head$_<br>\n</font></tt>\n);
}


###############################################################################
# 各種問い合わせ
###############################################################################

sub q_article {
	
	my ($ID, $query) = @_;
	
	# is_root
	# is_dummy
	# get_parentID
	# is_last
	# has_child
	
	if ($query eq 'is_root') {
		return ( split m|,|, $logdata{$ID} )[3] ? 0 : 1;
	} elsif ($query eq 'is_dummy') {
		return ( split m|,|, $logdata{$ID} )[0];
	} elsif ($query eq 'has_child') {
		return defined $kids{$ID}
	} elsif ($query eq 'is_last') {
		my ($ndate, $postid, $protect, $thread, $phost, $agent, $user, $mail, $title, $msg) = split m|,|, $logdata{$ID};
		
		# ルートならreturn
		if (not $thread) { return 1 }
		
		my $parent = q_article($ID, 'get_parentID');
		if ($parent and $logdata{$parent}) {
			return ${ $kids{$parent} }[-1] == $ID ? 1 : 0;
		} else {
			my ($ndate, $postid, $protect, $thread, $phost, $agent, $user, $mail, $title, $msg) = split m|,|, $logdata{$ID};
			return ${ $kids{$thread} }[-1] == $ID ? 1 : 0;
		}
	} elsif ($query eq 'get_parentID') {
		my ($ndate, $postid, $protect, $thread, $phost, $agent, $user, $mail, $title, $msg) = split m|,|, $logdata{$ID};
		$msg =~ m|<A href=".*?&s=(\d*)[^>]*?>参考|i ?  return $1 : return undef;
#		$msg =~ m|<A href="m=f&s=(\d*)[^>]*?>参考|i ?  return $1 : return undef;
	}

}


sub max_postID { ( sort {$b <=> $a} enum_postID($_[0]) )[0] }


###############################################################################
# postid => article
###############################################################################

sub make_hash_logdata {  map { my $log = $_; (split m|,|, $log)[1] => $log } @_  }


###############################################################################
# parent_postid =>[child_postid, child_postid, ... ]
###############################################################################

sub make_kids {
	
	my @logdata = @_;
	my %kids;
	
	for (reverse @logdata) {
		my ($ndate, $postid, $protect, $thread, $phost, $agent, $user, $mail, $title, $msg) = split m|,|;
		my $parent_postid = q_article($postid, 'get_parentID');
		
		if (not exists $logdata{$thread}) { 
		# ルートが存在しない場合
		# 
		# ダミーのルートを作成し
		# その子として登録する
		# 
			$logdata{$thread} = make_dummy_article($thread);
			push @{ $kids{$thread} }, $postid;
		} elsif (q_article($thread, 'is_dummy') == -1) {
		# ダミールートが存在する場合
		# 注意: -1はTRUE
			if ($logdata{$parent_postid}) {
				push @{ $kids{$parent_postid} }, $postid;
			} else {
				push @{ $kids{$thread} }, $postid;
			}
		} elsif ($logdata{$thread}) {
		# ルートが存在する場合
		# 
			push @{ $kids{$parent_postid} }, $postid;
		}
	}
	return %kids;
}


###############################################################################
# 記事が見つからなかったときのダミー記事を提供する
###############################################################################

sub make_dummy_article {  "-1,$_[0],,,,,,,,== not_found ==\n"  }


###############################################################################
# thread => [postid, postid, .. ]
###############################################################################

sub get_threadID {
	
	my @logdata = @_;
	my @threadID;
	
	for (@logdata) {
		my ($ndate, $postid, $protect, $thread, $phost, $agent, $user, $mail, $title, $msg) = split m|,|;
		$thread  ?  push @threadID, $thread
				 :  push @threadID, $postid;
	}
	
	# @threadIDから重複した要素を削除
	return keys %{ { map {$_ => 1} @threadID} };
}


sub enum_postID {
	
	my $ID = shift;
	my @postID = ($ID);
	
	if (q_article($ID, 'has_child')) {
		for my $kid (@{ $kids{$ID} }) {
			push @postID, enum_postID($kid);
		}
	}
	
	return @postID;
}


sub getmessage_treeview {
	
	my ($ndate, $postid, $protect, $thread, $phost, $agent, $user, $mail, $title, $msg) = split(m|,|, $_[0]);
	
	$msg =~ s/\n$//;
	$title =~ s/\0/\,/g;
	$mail =~ s/\0/\,/g;
	$user =~ s/\0/\,/g;
	$msg =~ s/\0/\,/g;
	
	return ($ndate, $postid, $protect, $thread, $phost, $agent, $user, $mail, $title, $msg);
}


1;


__END__
