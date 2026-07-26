#! /usr/local/bin/perl

#
#	くずはすくりぷと Rev.0.1 Preview 9 (2000.9.3)
#	 (個人用環境設定画面用関数群)
#


###############################################################################
#  環境設定画面表示
###############################################################################

sub prtcustom {
	
	my ( @follow, @reload );
	$follow[$followwin] = 'checked';
	$reload[$reltype] = 'checked';
	

	if ($FORM{'target_blank'} ) {
		$target1 = 'checked';
	} elsif ($FORM{'targetlink'} ) {
		$target2 = 'checked';
	} else {
		$target0 = 'checked';
	}

	&prthtmlhead ( "$bbstitle 個人用環境設定" );
	print <<EOF;
<H3>$bbstitle 個人用環境設定</H3><BR>
<FORM method="post" action="$cgiurl">
  <INPUT type="hidden" name="m" value="c">
  <INPUT type="hidden" name="nm" value="$FORM{'m'}">
  <UL>
    <LI><STRONG>表示設定</STRONG><BR> <BR>
    <TABLE border="0" cellspacing="0" cellpadding="0">
      <TR>
        <TD>文字色　　　</TD>
        <TD><INPUT type="text" name="tc" size="7" value="$CC{'text'}"></TD>
        <TD>　背景色</TD>
        <TD><INPUT type="text" name="bc" size="7" value="$CC{'bg'}"></TD>
      </TR>
      <TR>
        <TD>リンク色</TD>
        <TD><INPUT type="text" name="lc" size="7" value="$CC{'link'}"></TD>
        <TD>　訪問済リンク色 </TD>
        <TD><INPUT type="text" name="vc" size="7" value="$CC{'vlink'}"></TD>
      </TR>
      <TR>
        <TD>引用色</TD>
        <TD><INPUT type="text" name="qc" size="7" value="$CC{'qmsgc'}"></TD>
        <TD>　題名色 </TD>
        <TD><INPUT type="text" name="sc" size="7" value="$CC{'subj'}"></TD>
      </TR>
    </TABLE>
  </UL>
  <UL>
    <LI><STRONG>付加機能設定</STRONG><BR> <BR>
    <INPUT type="checkbox" name="g" $S_gzchk[$gzipu]>
gzip圧縮転送<BR>
    <INPUT type="checkbox" name="a" $S_alchk[$autolink]>
URL自動リンク<BR>
    <INPUT type="checkbox" name="linkline" $FORM{'linkline'}>
Link行のOFF<font size="-1">（カウンターの下にあるLink行を表示しない）</font><BR>
    <INPUT type="checkbox" name="multizilla" $FORM{'multizilla'}>
multizilla専用<font size="-1">（リンクをタブで開くため、出力記事のtarget指定を"_blank"に変換する）</font><br>
    <INPUT type="checkbox" name="gikoitsuoff" $FORM{'gikoitsuoff'}>
擬古猫といっしょをOFFにする<br>
    <INPUT type="checkbox" name="zcolor" $FORM{'zcolor'}>
カラー機能をOFFにする<font color=red>(未実装)</font><br>

    <INPUT type="checkbox" name="ztree" $FORM{'ztree'}>
ツリー表示をデフォルトにする<br>

    <INPUT type="checkbox" name="zwindow"$FORM{'zwindow'}>
フォロー画面で掲示板にすぐ戻る<font color=red>(未実装)</font><br>

<P>
省略・非表示設定欄を表示<INPUT type="radio" name="limitcfg" value="1" $S_lcchk[1]>する <INPUT type="radio" name="limitcfg" value="0" $S_lcchk[0]>しない<br>
一記事内に<INPUT size="2" type="text" name="linelimit" value="$FORM{'linelimit'}"> 行以上は<INPUT type="radio" name="lineswitch" value="0" $S_lschk[0]>省略 <INPUT type="radio" name="lineswitch" value="1" $S_lschk[1]>非表示（ 0、空欄で省略・非表示しない）<br>
一行中に<INPUT size="2" type="text" name="collimit" value="$FORM{'collimit'}"> Byte以上は<INPUT type="radio" name="colswitch" value="0" $S_cschk[0]>省略 <INPUT type="radio" name="colswitch" value="1" $S_cschk[1]>非表示（ 0、空欄で省略・非表示しない）<br>

  </UL>


  <UL>
    <LI><STRONG>掲示板タイトルの変更</STRONG><BR> <BR>
    <INPUT type="text" size="70" maxlength="70" name="newtitle" value="$FORM{'newtitle'}"><br>
  </UL>

  <UL>
    <LI><STRONG>投稿者名</STRONG><BR> <BR>
    <INPUT size="20" type="text" name="u" maxlength="30" value="$FORM{'u'}"><br>
  </UL>

  <UL>
    <LI><STRONG>メール</STRONG><BR> <BR>
    <INPUT size="30" type="text" name="i" maxlength="255" value="$FORM{'i'}"><br>
  </UL>

  <UL>
    <LI><STRONG>フォロー画面の表示方法</STRONG><BR> <BR>
    <INPUT type="radio" name="fw" value="0" $follow[0]>新規ウィンドウを開いて表示<BR>
    <INPUT type="radio" name="fw" value="1" $follow[1]>新規ウィンドウを開かずに表示<font color="#ff0000">（非推奨）</font><BR>
  </UL>
  <UL>
    <LI><STRONG>０件リロード時のメッセージの表示方法</STRONG><BR> <BR>
    <INPUT type="radio" name="rt" value="0" $reload[0]>標準（投稿時刻降順表示）<BR>
    <INPUT type="radio" name="rt" value="1" $reload[1]>反転（投稿時刻昇順表示）<BR>
  </UL>
  <UL>
    <LI><STRONG>カウンターの下にあるLink行を別窓で開く</STRONG><BR> <BR>
    <INPUT type="radio" name="targetwindows" value="0" $target0>target="_self"で表示（デフォ）<BR>
    <INPUT type="radio" name="targetwindows" value="1" $target1>target="_blank"で表示<BR>
    <INPUT type="radio" name="targetwindows" value="2" $target2>target="link"で表示<BR>
  </UL>
  <BR>
  「登録」を押した後に表示されるURLをブックマークに登録しましょう。<BR>
  上記の設定で掲示板を訪問することができます。<BR> <BR>
  <INPUT type="submit" value="登録">
  <INPUT type="reset" value="リセット">
  <INPUT type="submit" name="cr" value="標準に戻す">
  <INPUT type="submit" name="cdc" value="Cookie消去">
</FORM>
</BODY>
</HTML>
EOF
}


###############################################################################
#  環境設定結果画面表示
###############################################################################

sub setcustom {
	
# 新しい項目を追加

	my ( $opt5 , $opt6 , $opt1 , $opt2 , $opt3 , $opt4 , $opt7 , $opt8 , $opt9 , $opt10 , $opt11 , $opt12 );

	if ($FORM{'linkline'}) {
		$opt1 = "&linkline=checked";
	}

	if ($FORM{'multizilla'}) {
		$opt2 = "&multizilla=checked";
	}

	if ( ( $FORM{'newtitle'} ) && ( $bbstitle ne $FORM{'newtitle'} ) ) {
		$opt3 = "&newtitle=$FORM{'newtitle'}";
	}


	if ($FORM{'targetwindows'} == 0) {
		$opt4 = "";
	} elsif ($FORM{'targetwindows'} == 1) {
		$opt4 = "&target_blank=checked";
	} elsif ($FORM{'targetwindows'} == 2) {
		$opt4 = "&targetlink=checked";
	}

	if ( $FORM{'u'} ) {
		$opt5 = "&u=$FORM{'u'}";
	}

	if ( $FORM{'i'} ) {
		$opt6 = "&i=$FORM{'i'}";
	}

	if ( $FORM{'gikoitsuoff'} ) {
		$opt7 = "&gikoitsuoff=$FORM{'gikoitsuoff'}";
	}

	if ( $FORM{'zcolor'} ) {
		$opt8 = "&zcolor=$FORM{'zcolor'}";
	}

	if ( $FORM{'ztree'} ) {
		$opt8 = "&tree=$FORM{'ztree'}";
	}

	if ( $FORM{'zwindow'} ) {
		$opt9 = "&zwindow=$FORM{'zwindow'}";
	}

	if ( $FORM{'limitcfg'} ) {
		$opt10 = "&limitcfg=$FORM{'limitcfg'}";
	}

	if ( $FORM{'linelimit'} ) {
		$opt11 = "&linelimit=$FORM{'linelimit'}";
	}

	if ( $FORM{'collimit'} ) {
		$opt12 = "&collimit=$FORM{'collimit'}";
	}


$optcust = "$opt5$opt6$opt1$opt2$opt3$opt4$opt7$opt8$opt9$opt10$opt11$opt12";

	my ( $p1, $p2, $p3, $nm, %alchk, %gzchk );
	
	if ( !$FORM{'cr'} ) {
		$alchk{'checked'} = 1;
		$gzchk{'checked'} = 1;
		$p1 = sprintf ( "%x", $alchk{"$FORM{'a'}"} + $FORM{'fw'} * 2 + $FORM{'rt'} * 4 + $gzchk{"$FORM{'g'}"} * 8 );
		$p2 = 0;
		$p3 = 0;
		if ( $FORM{'nm'} eq 'op' ) {
			$nm = 'm=o&';
		} else {
			$nm = '';
		}
		$FORM{'c'} = "$FORM{'tc'}$FORM{'bc'}$FORM{'lc'}$FORM{'vc'}$FORM{'qc'}$FORM{'sc'}$p1$p2$p3";

	} else {
		$FORM{'c'} = '';
		$optcust = "";
	}
	
	if ( $FORM{'cdc'} ) {
		&putcookie ( $S_cexp - 2 );
	} else {
		&putcookie ( 0 ) if ( $cookie );
	}


	print "Location: $cgiurl?${nm}c=$FORM{'c'}$optcust\n\n";

}


1;


__END__
