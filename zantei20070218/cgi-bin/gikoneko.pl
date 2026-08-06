#!/usr/bin/perl
# 変更する場合: ##!/usr/local/bin/perl

#　擬古猫といっしょ

###############################################################################
#  メッセージ処理（点取り占いのぱくり）
###############################################################################

sub fortune {
	
	my ( @fortunetext, $fortunetext );
	
	open ( IN, "./neko/gikoneko_kotoba.dat" );
	@fortunedata = <IN>;
	close ( IN );

	srand;
	rand;

	$fortunetext = "$fortunedata[int(rand(@fortunedata))]";
	$fortunetext =~ s/\n//g;
	
	return $fortunetext;
}

###############################################################################
#  メイン処理
###############################################################################

sub gikoneko {



#処理始め

	my ( $points );
	my ( @mark ) = ( 'あ', 'い', 'う', 'え', 'お', 'か', 'き', 'く', 'け', 'こ', 'さ', 'し', 'す', 'せ', 'そ', 'た', 'ち', 'つ', 'て', 'と', 'な', 'に', 'ぬ', 'ね', 'の',  );

	$points = int(rand(@mark));


if($points < 1){
print "<BLOCKQUOTE><PRE>
【小吉】
　　　 ∧ ∧
～′￣(´Д`)＜",&fortune,"
  UU￣ U  U
</PRE></BLOCKQUOTE>\n";
}
elsif ($points < 2){
print "<BLOCKQUOTE><PRE>
【中吉】
　　　 ∧ ∧
～′￣(`Д´)＜ﾊｯﾊｰﾝ!  ",&fortune,"
  UU￣ U  U
</PRE></BLOCKQUOTE>\n";
}
elsif($points <3){
print "<BLOCKQUOTE><PRE>
【凶】
　　　 ∧ ∧
～′￣(;´Д`)＜",&fortune,"
  UU￣ U  U
</PRE></BLOCKQUOTE>\n";
}
elsif($points < 4){
print "<BLOCKQUOTE><PRE>
【大吉】
          ヽ(`ー´)ノ＜",&fortune,"
       ∧ ∧｜_ ｜
      (`ー´)  < ) ～
        U  U ￣￣UU 
</PRE></BLOCKQUOTE>\n";
}
elsif($points < 5){
print "<BLOCKQUOTE><PRE>
【幼吉】
   ∧  ∧    
   ﾉ  ﾊ  ＼  
  ﾉ ∂.∂)＜",&fortune,"
    (∩∩
γ～/___|
     U U
</PRE></BLOCKQUOTE>\n";
}
elsif($points < 6){
print "<BLOCKQUOTE><PRE>
【轟吉】
                          *  . .  * (ﾟДﾟ)＜",&fortune,"
＼猫ビィィィィム！／    *  .     .    *  (ﾟДﾟ)＜",&fortune,"
       ∧ ∧       ＿＿＿＿＿※   .              *  
～′￣(     )￣￣￣        .     .  *
  UU￣ U  U                  . .  *              (ﾟДﾟ)＜",&fortune,"
</PRE></BLOCKQUOTE>\n";
}
elsif($points <7){
print "<BLOCKQUOTE><PRE>
【猫吉】
       ∧ ∧
       ■●■
      (´ー`)＜",&fortune,"
      (｜ o｜)
      U｜ o｜U
      Ｕ  Ｕ
</PRE></BLOCKQUOTE>\n";
}
elsif($points <8){
print "<BLOCKQUOTE><PRE>
【怒吉】
  |
  |
  |    ∧ ∧
  ′￣(`Д´)＜",&fortune,"
  |  ＿＿  |
  |||    |||
  UU     U U
</PRE></BLOCKQUOTE>\n";
}
elsif($points <9){
print "<BLOCKQUOTE><PRE>
【愛吉】
       ＿∧ ∧
     ／（´ー`)＜",&fortune,"
   ／  ／U  U∧ ∧
ノ’（  ￣￣(´ー`)＜",&fortune,"
  UU  UU￣￣ U  U
</PRE></BLOCKQUOTE>\n";
}
elsif($points <10){
print "<BLOCKQUOTE><PRE>
【引吉】
       ∧ ∧
    ／(´ー`)＜",&fortune,"
乙／  ) ⊃ ⊃
  ＼⊃＼⊃  ））））））））
</PRE></BLOCKQUOTE>\n";
}
elsif($points <11){
print "<BLOCKQUOTE><PRE>
【吉】
   ∧ ∧
／(´ー`)＜",&fortune,"
￣￣￣￣￣|
</PRE></BLOCKQUOTE>\n";
}
elsif($points <12){
print "<BLOCKQUOTE><PRE>
【楽吉】
       ∧ ∧
    ヽ(´ー`)ノ＜",&fortune,"
      ｜   ｜
      ﾉ  _ ﾉ
ε≡Ξ∪ ∪
</PRE></BLOCKQUOTE>\n";
}
elsif($points <13){
print "<BLOCKQUOTE><PRE>
【凶】
　 ∧∧
　/⌒ヽ)＜",&fortune,"
～(_＿)
</PRE></BLOCKQUOTE>\n";
}
elsif($points <14){
print "<BLOCKQUOTE><PRE>
【吉】
(",&fortune,")
　　 。
　　。
 ∧ ∧⌒ヽ
(´ー`)(　)～
￣￣￣￣￣￣|
</PRE></BLOCKQUOTE>\n";
}
else{
print "<BLOCKQUOTE><PRE>
【吉】
　　　 ∧ ∧
～′￣(´ー`)＜",&fortune,"
  UU￣ U  U
</PRE></BLOCKQUOTE>\n";
}

}

1;

__END__
http://www.google.co.jp/search?hs=cxr&hl=ja&client=firefox-a&rls=org.mozilla%3Aja-JP%3Aofficial&q=%E6%9D%BE%E6%B0%B8%E8%8B%B1%E6%98%8E&btnG=Google+%E6%A4%9C%E7%B4%A2&lr=lang_ja