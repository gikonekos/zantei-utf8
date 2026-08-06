#!/usr/bin/perl
# 変更する場合: ##!/usr/local/bin/perl

# ---------------------------------------------------------------------------- #
$CGI_VER = '辞典CGI ver 1.01 by 川原 千種' ;	# 書替えないこと
# ---------------------------------------------------------------------------- #

# 日本語コードjcode.plのURL
# [2026-07-18] jcode.pl不使用化（スタンドアロン方針、猫）
#require 'jcode.pl';

# このperlファイルのURL
$main_url = 'http://www.ge.st98.arena.ne.jp/cgi-bin/ziten/ziten.cgi';

# 画面の「旦~」リンク先URL
$modoru = 'http://www.ge.st98.arena.ne.jp/cgi-bin/bbs.cgi';

# 書込ファイル
$data_file = "ziten.dat";

# 辞典のタイトル
$main_title = '＠暫定辞典' ;

# 分類名(この順番に表示されます)
@genre_n = ('人物名','ネタ','旦~') ;
# 分類色(分類名と順番を合わせること)
@genre_c = ('#FF0000','#ffff00','#00ffff') ;

# 画面の色や背景の設定 (BODYタグ HTML書式)
$body = '<body bgcolor="004040" text="FFFFFF">';

# 画面上部に表示するメッセージ
$mes_top1 = '<b>読みはひらがなでヽ(`Д´)ﾉ</b><br>' ;

# 入力形式の設定　標準='POST' その他'GET'
#　登録ボタンを押して Method not implemented.. 等というエラーが出る場合は GET で試すこと
#　GETの場合は不要な悪戯を受けてしまう環境になりますので、注意してください.
$method = 'POST';

# ---------------------------------------------------------------------------- #
# ここまでがユーザー設定。ここから下はいじらない。                             #
# ---------------------------------------------------------------------------- #

# 一覧表示用配列（項目名、始まり文字、終わり文字）
@list_index = ('全項目','あ行','か行','さ行','た行','な行','は行','ま行','や行','ら行','わ行、ん') ;
@list_start = ('0','あ','か','さ','た','な','は','ま','や','ら','わ') ;
@list_end = ('0','か','さ','た','な','は','ま','や','ら','わ','んんんんん') ;

# 分類データを連想配列に格納
for ($h = 0 ; $h <= $#genre_n ; $h++)
{
	$genre{@genre_n[$h]} = @genre_c[$h] ;
}

# フォームからのデータを取得 ここは定型処理
if ($method eq 'POST' && $ENV{'QUERY_STRING'} ne '')
{
	&error('request_method');
}
if ($method eq 'POST')
{
	read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	@pairs = split(/&/, $buffer);
}
elsif ($method eq 'GET')
{
	@pairs = split(/&/, $ENV{'QUERY_STRING'});
}
else
{
	&error('request_method');
}

foreach $pair (@pairs)
{
	($name, $value) = split(/=/, $pair);
	$name =~ tr/+/ /;
	$name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

	#&jcode'convert(*name,'sjis');
	#&jcode'convert(*value,'sjis');

	# 入力データのチェック
	# タグが入力されていれば、それを無効にする。&ltなどに置き換え表示してる
	$value =~ s/</&lt;/g;
	$value =~ s/>/&gt;/g;

	# 区切り文字の”,”があれば”、”に変換
	$value =~ s/\,/、/g;

	# 連想配列に格納
	$FORM{$name} = $value;
}

# //////////////////////////////////////////////////////////////////////////// #
# メインルーチン 処理の振り分け                                                #
# //////////////////////////////////////////////////////////////////////////// #
# 「登録」ボタンを押したとき
if ($FORM{'action'} eq 'regist')
{
	&load_file ;
	&error_ck;
	&confirm;
}
# 書きこみ「確認」ボタンを押したとき
elsif ($FORM{'action'} eq 'conf')
{
	&load_file ;
	&register;
	print "Location: $main_url" . '?' . "\n\n";
}
# 「全表示」ボタンを押したとき
elsif ($FORM{'submit'} eq '全項目') 
{
	&out_inputform ;
	&out_alldat;
	&out_fetter ;
}
# 「行」表示ボタンを押したとき
elsif ($FORM{'submit'} =~ /行/) 
{
	&out_inputform ;
	&out_gyoudat;
	&out_fetter ;
}
# 「検索」ボタンを押したとき
elsif ($FORM{'submit'} eq '検索') 
{
	&out_inputform ;
	&out_searchdat;
	&out_fetter ;
}
# はじめの呼び出しなど通常表示
else
{
	&out_inputform ;
	&out_index;
	&out_fetter ;
}

# //////////////////////////////////////////////////////////////////////////// #
# 書込みファイルの読み込み
# //////////////////////////////////////////////////////////////////////////// #
sub load_file
{
	open (IN,"$data_file") || &error('open_error');
	@LINES = <IN>;
	close (IN);
}

# //////////////////////////////////////////////////////////////////////////// #
# HTMLの出力処理
# //////////////////////////////////////////////////////////////////////////// #
# 先頭-入力フォーム部-表示操作ボタン部までを表示。
sub out_inputform
{
	&load_file ;

	print "Content-type: text/html\n\n";
	print "<html><head><title>$main_title</title></head>\n";
	print "$body\n";

	print "<center>\n";
	print "<font color=\"#ee0077\" size=5><b>$main_title</b></font>\n";
	print "<hr width=40\%><br>\n";
	print "$mes_top1\n";
	print "$mes_top2\n";
	print "$mes_top3\n";
	print "<form method=$method action=\"$main_url\">\n";
	print "<table border width=80%>\n";
	print "<tr>\n";
	print "<th>項目選択</th>\n";
	print "<td>\n";
	print "<select name=\"sel_title\" size=1>\n" ;
	print "<option value=\"新規登録\">（新規登録）</option>\n" ;
	foreach $line (@LINES)
	{
		($out_text,$out_yomi,@out_comment) = split(/,/, $line);
		print "<option value=\"$out_text\">$out_text</option>\n" ;
	}
	print "</select>\n" ;
	print "</td>\n";
	print "<th>新規項目<br>の場合</th>\n";
	print "<td>\n";
	print "項目 <input type=\"text\" size=30 maxlength=255 name=new_title><br>\n";
	print "読み(全角ひらがな) <input type=\"text\" size=30 maxlength=255 name=new_yomi><br>\n";
	print "分類 \n";
	print "<select name=\"sel_genre\" size=1>\n" ;

	foreach $tmp_genre (@genre_n)
	{
		print "<option value=\"$tmp_genre\">$tmp_genre</option>\n" ;
	}
	print "</select>\n" ;
	print "</td>\n";
	print "</tr>\n";
	print "<tr>\n";
	print "<td colspan=4>\n";
	print "<b>コメント</b> <input type=\"text\" size=100 maxlength=255 name=comment>\n";
	print "</td>\n";
	print "</tr>\n";
	print "<tr>\n";
	print "<td colspan=4 align=\"right\">\n";
	print "<input type=\"hidden\" name=\"action\" value=\"regist\">\n";
	print "<input type=submit name=\"submit\" value=\"登録\"> <input type=reset value=\"リセット\">\n";
	print "</td>\n";
	print "</tr>\n";
	print "</table>\n";
	print "</form>\n";
	print "</center>\n";
	print "<hr>\n";
	# 表示用のボタンを表示
	print "<form method=$method action=\"$main_url\">\n";
	foreach $tmp_index (@list_index)
	{
		print "<input type=submit name=\"submit\" value=\"$tmp_index\">\n" ;
	}

	# 検索用ボタンを表示
	print "分類で検索\n" ;
	print "<select name=\"sel_genre\" size=1>\n" ;
	foreach $tmp_genre (@genre_n)
	{
		print "<option value=\"$tmp_genre\">$tmp_genre</option>\n" ;
	}
	print "</select>\n" ;
	print "<input type=submit name=\"submit\" value=\"検索\">\n" ;
	print "</form>\n";
	print "<p>\n" ;
}

# データの一覧表示
sub out_index
{
	# 項目名のみをすべて表示
	foreach $line (@LINES)
	{
		($out_text,$out_yomi,$out_genre,@out_comment) = split(/,/, $line);
		print "$out_text<br>\n" ;
	}
	print "\n" ;
}

# データの全表示
sub out_alldat
{
	print "<dl>\n" ;
	foreach $line (@LINES)
	{
		# （文末の）改行を消去
		$line =~ s/\n//g;

		($out_text,$out_yomi,$out_genre,@out_comment) = split(/,/, $line);
		print "<p>\n" ;
		print "<dt><font color=$genre{$out_genre}><b>$out_text （$out_yomi）</b> $out_genre</font>\n" ;
		print "<dd>\n" ;
		foreach $tmp_comment (@out_comment)
		{
			print "・$tmp_comment<br>\n" ;
		}
	}
	# データが無い時
	if (($#LINES + 1) == 0)
	{
		print "<b>データは1件もありません。</b>\n" ;
	}
	print "</dl>\n" ;
}

# データの行表示
sub out_gyoudat
{
	# 行などの区切りの定義、表示表題を出力
	for ($i = 0 ; $i <= @list_index ; $i++)
	{
		if ($FORM{'submit'} eq @list_index[$i] ) 
		{
			print "<b><u>○@list_index[$i]のデータ○</u></b>\n" ;
			$str_start = @list_start[$i] ;
			$str_end = @list_end[$i] ;
			last ;
		}
	}

	# 書込みファイルのデータを出力
	print "<dl>\n" ;

	# 各「行」にある項目数をカウント
	$out_count = 0 ;

	foreach $line (@LINES)
	{
		# （文末の）改行を消去
		$line =~ s/\n//g;

		($out_text,$out_yomi,$out_genre,@out_comment) = split(/,/, $line);
		if ($str_start le $out_yomi && $out_yomi lt $str_end)
		{
			# 項目名を表示
			$out_count++ ;
			print "<p>\n" ;
			print "<dt><font color=$genre{$out_genre}><b>$out_text （$out_yomi）</b> $out_genre</font>\n" ;
			print "<dd>\n" ;

			# コメントを表示
			foreach $tmp_comment (@out_comment)
			{
				print "・$tmp_comment<br>\n" ;
			}
		}
	}
	# 指定「行」にひとつも項目が無かったとき
	if ($out_count == 0)
	{
		print "<b>このデータは1件もありませんでした。</b>\n" ;
	}
	print "</dl>\n" ;
}

# データの検索表示
sub out_searchdat
{
	# 書込みファイルのデータを出力
	print "<b><u>○分類＝$FORM{'sel_genre'}のデータ○</u></b>\n" ;

	print "<dl>\n" ;

	# 各「行」にある項目数をカウント
	$out_count = 0 ;

	foreach $line (@LINES)
	{
		# （文末の）改行を消去
		$line =~ s/\n//g;

		($out_text,$out_yomi,$out_genre,@out_comment) = split(/,/, $line);
		if ($out_genre eq $FORM{'sel_genre'} )
		{
			# 項目名を表示
			$out_count++ ;
			print "<p>\n" ;
			print "<dt>$out_text （$out_yomi） $out_genre\n" ;
			print "<dd>\n" ;

			# コメントを表示
			foreach $tmp_comment (@out_comment)
			{
				print "・$tmp_comment<br>\n" ;
			}
		}
	}
	# 指定「分類」にひとつも項目が無かったとき
	if ($out_count == 0)
	{
		print "<b>このデータは1件もありませんでした。</b>\n" ;
	}
	print "</dl>\n" ;
}

# フッターを表示。
sub out_fetter
{
	print "<p>\n<hr>\n";
	print "<form method=$method action=\"$main_url\">\n";
	print "<input type=submit name=\"submit\" value=\"一覧画面\">\n" ;
	print "</form>\n";
	print "<a href=\"$modoru\">終了</a>\n";
	# このスクリプトの著作権表示（かならず表示してください）
	print "<div align=\"right\">\n";
	print "<A HREF=\"http://www.k-collect.net/cgi_lab/ziten/index.htm\">$CGI_VER</A>\n";
	print "</div>\n";

	print "</body></html>\n";
}

# //////////////////////////////////////////////////////////////////////////// #
# エラーチェック
# //////////////////////////////////////////////////////////////////////////// #
sub error_ck
{
	$title_check = 0 ;
	foreach $line (@LINES)
	{
		($out_text,$out_yomi,@out_comment) = split(/,/, $line);
		if ($FORM{'sel_title'} eq "新規登録" && $FORM{'new_title'} eq $out_text)
		{
			$title_check = 1 ;
		}
	}
	if ($title_check == 1)
	{
		push(@ERROR,$FORM{'new_title'});
		&error('already_title',@ERROR);
	}

	if ($FORM{'comment'} eq "")
	{
		push(@ERROR,"●コメント") ;
	}
	if ($FORM{'sel_title'} eq "新規登録" && $FORM{'new_title'} eq "")
	{
		push(@ERROR,"●新規登録する項目名");
	}
	if ($FORM{'sel_title'} eq "新規登録" && $FORM{'new_yomi'} eq "")
	{
		push(@ERROR,"●新規登録する項目の読みがな");
	}
	if (@ERROR)
	{
		&error('missing_fields',@ERROR);
	}
}

# //////////////////////////////////////////////////////////////////////////// #
# 書込み確認処理
# //////////////////////////////////////////////////////////////////////////// #
sub confirm
{
	print "Content-type: text/html\n\n";
	print "<html><head><title>$main_title</title></head>\n";
	print "$body\n";
	print "<font color=\"\#ee0077\" size=5><b>$main_title</b></font>\n";
	print "<hr width=40\%><br>\n";
	print "次のデータを書きこみます。よろしければ「確認」ボタンを押してください<br>\n";
	print "変更するときは、ブラウザの「戻る」ボタンで戻ってください\n<p>\n";
	if ($FORM{'sel_title'} eq "新規登録")
	{
		print "<b>新規に項目を登録</b><br>\n";
		print "<b>項目：</b>$FORM{'new_title'}<br>\n";
		print "<b>読み(全角ひらがな)：</b>$FORM{'new_yomi'}<br>\n";
		print "<b>分類：</b>$FORM{'sel_genre'}<br>\n";
		print "<b>コメント：</b>$FORM{'comment'}\n";
	}
	else
	{
		print "<b>コメント登録</b><br>\n";
		print "<b>項目：</b>$FORM{'sel_title'} <b>に</b><br>\n";
		print "<b>コメント：</b>$FORM{'comment'}<br>\n";
		print "<b>を追加</b>\n";
	}
	print "<form method=$method action=\"$main_url\">\n";
	print "<input type=hidden name=sel_title value=\"$FORM{\"sel_title\"}\">" ;
	print "<input type=hidden name=new_title value=\"$FORM{\"new_title\"}\">" ;
	print "<input type=hidden name=new_yomi value=\"$FORM{\"new_yomi\"}\">" ;
	print "<input type=hidden name=sel_genre value=\"$FORM{\"sel_genre\"}\">" ;
	print "<input type=hidden name=comment value=\"$FORM{\"comment\"}\">" ;
	print "<input type=\"hidden\" name=\"action\" value=\"conf\">\n";
	print "<input type=submit name=submit value=\"確認\">\n";
	print "</form>\n";

	print "</body></html>\n";
}

# //////////////////////////////////////////////////////////////////////////// #
# 書込み処理
# //////////////////////////////////////////////////////////////////////////// #
sub register
{
	# 書きこんだかをチェックする変数
	$write_check = 0 ;

	# 新規項目登録の場合
	if ($FORM{'sel_title'} eq "新規登録")
	{
		# 追加する行の作成
		$new_line = "$FORM{'new_title'},$FORM{'new_yomi'},$FORM{'sel_genre'},$FORM{'comment'}\n";

		foreach $line (@LINES)
		{
			if ($write_check == 0)
			{
				($out_text,$out_yomi,$out_genre,@out_comment) = split(/,/, $line);
				if ($FORM{'new_yomi'} lt $out_yomi)
				{
					push (@OUT_LINES,$new_line);
					push (@OUT_LINES,$line);
					$write_check = 1 ;
				}
				else
				{
					push (@OUT_LINES,$line);
				}
			}
			else
			{
				push (@OUT_LINES,$line);
			}
		}
		# 新規項目をファイルの末尾に登録
		if ($write_check == 0)
		{
			push (@OUT_LINES,$new_line);
		}
	}
	# 既存の項目にコメントを追加する場合。
	else
	{
		foreach $line (@LINES)
		{
			($out_text,$out_yomi,$out_genre,@out_comment) = split(/,/, $line);
			if ($FORM{'sel_title'} eq $out_text)
			{

				$line = "$out_text,$out_yomi,$out_genre" ;

				foreach $tmp_comment (@out_comment)
				{
					$line = "$line,$tmp_comment" ;
				}
				$line =~ s/\n//g;
				$line = "$line,$FORM{'comment'}\n" ;
			}
			push (@OUT_LINES,$line);
		}
	}

	# 辞書ファイルに書きこみ（ロック処理あり）
	#perlのプロセス番号のテンポラリーを作成・書込
	$tmp_dummy = "$$\.tmp";
	open(TMP,">$tmp_dummy") || die "Can't create tmp file.\n";
	close(TMP);
	#パーミッションを変更
	chmod 0666,$tmp_dummy;
	open(TMP,">$tmp_dummy") || die "Can't open tmp file.\n";
	print TMP (@OUT_LINES);
	close(TMP);
	rename($tmp_dummy,$data_file);
}

# //////////////////////////////////////////////////////////////////////////// #
# エラー処理
# //////////////////////////////////////////////////////////////////////////// #
sub error
{
	($error,@error_fields) = @_;

	print "Content-type: text/html\n\n";

	if ($error eq 'missing_fields')
	{
		print "<html><head><title>空白エラー</title></head>\n";
		print "$body\n";
		print "<center>\n";
		print "<h1>必要な項目が入力されていません。</h1>\n";
		foreach $error_field (@error_fields)
		{
			print "<b>$error_field</b><br>\n";
		}
		print "<hr width=75\%><p>\n";
		print "<br>以上の項目をチェックしてみてください。\n";
		print "</center>\n";
		print "</body></html>\n";
	}
	elsif ($error eq 'already_title')
	{
		print "<html><head><title>既存項目エラー</title></head>\n";
		print "$body\n";
		print "<center>\n";
		print "<h1>登録しようとした項目はすでに存在します</h1>\n";
		print "入力した項目＝<b>@error_fields</b><br>\n";
		print "<hr width=75\%><p>\n";
		print "</center>\n";
		print "</body></html>\n";
	}
	elsif ($error eq 'request_method')
	{
		print "<html><head><title>要求エラー</title></head>\n";
		print "$body\n";
		print "<center>\n";
		print "<h1>要求エラーです。</h1>\n\n";
		print "\"POST\" か \"GET\" しか受け取れません。<br>\n";
		print "不正利用の可能性があります<p>\n";
		print "<hr width=75\%><p>\n";
		print "</center>\n";
		print "</body></html>\n";
	}
	elsif ($error eq 'open_error')
	{
		print "<html><head><title>ファイルのオープンエラー</title></head>\n";
		print "$body\n";
		print "<center>\n";
		print "<h1>ファイルのオープンエラー</h1>\n";
		print "書込みファイルが開けません、ファイルの場所を確認してください。\n";
		print "<hr width=75\%><p>\n";
		print "</center>\n";
		print "</body></html>\n";
	}
	exit;
}
