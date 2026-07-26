/* 
 *  代替スタイルシート切り替えスクリプト
 *
 *  ・IE4以降でスタイルシート切り替え機能をを実装する
 *  ・また、代替スタイルシートの機能を有しているブラウザではその使い勝手を向上させる
 *
 *  参考URL
 *  http://critical.s6.xrea.com/web/cssselect.shtml
 *  http://east.portland.ne.jp/~sigekazu/css/javascript9.htm
 */

/****************************************************************
  使い方
  
    通常使用するスタイル
    <link rel="stylesheet" href="normal.css" type="text/css" title="通常使用">
    
    代替スタイルを列挙する
    <link rel="alternate stylesheet" href="alter1.css" type="text/css" title="代替スタイル1">
    <link rel="alternate stylesheet" href="alter2.css" type="text/css" title="代替スタイル2">
    
    タイトル属性を書かないと共通のスタイル
    <link rel="stylesheet" href="common.css" type="text/css">
    
    このスクリプトはLINK要素の後で呼び出す
    <script type="text/javascript" src="styleselector.js" charset="UTF-8"></script>
    
    切り替えフォームを付けたい場所にこれを書く
    <script type="text/javascript"><!--
      writeCSSSelectForm('デザイン変更');
    // --></script>

*******************************************************************/

var cdays, cpath, cname, sheet, enableflag, isMozilla;
cdays = 30;		// クッキーの保存日数
				// 0ならブラウザを終了させるまでが有効期限となります。
cpath = "";		// クッキーの有効にするサイトのパス名
				// 空なら、クッキーを設定したページのパス名部になります。
cname = "StyleSheet";

sheet      = "";
enableflag = 0;
isMozilla  = navigator.product == "Gecko";


// クッキーからスタイルを読み込む
function initStyle () {
	if (sheet && isExistsCSS(sheet)) {
		changeCSS(sheet);
	}
}


// CSSのリストの中に存在するか調べる
function isExistsCSS (ssTitle) {
	
	if (!ssTitle) return false;
	
	var ss =
		(enableflag > 1) ? document.styleSheets :
			document.all ? document.all.tags('LINK') : document.getElementsByTagName('LINK');
	
	for (var i=0; i<ss.length; i++) {
		if (ss[i].type == "text/css" && ss[i].title == ssTitle)
			return true;
	}
	return false;
}


// スタイルシートを切り替える
function changeCSS (ssTitle) {
//	if (!ssTitle) return;
	
	var ss =
		(enableflag > 1) ? document.styleSheets :
			document.all ? document.all.tags('LINK') : document.getElementsByTagName('LINK');
	
	// title属性値がssTitleならスタイルシートを有効に
	// title属性の与えられていない外部スタイルシートは常に有効（飛ばしたほうがいいかも？）
	for (var i=0; i<ss.length; i++) {
		if (ss[i].type != "text/css") continue;
		ss[i].disabled = (!ss[i].title || ss[i].title == ssTitle) ? false : true;
	}
	
	setCookie(cname, ssTitle);
	sheet = ssTitle;
}


// スタイルシート切り替えフォームが選択された
function selectCSSEvent (obj) {
	changeCSS(obj.value);
	window.focus();
}


// スタイルシート選択フォームを出力する
function writeCSSSelectForm (label) {
	
	if (enableflag) {
		var html = label + ' <select name="selectss" onChange="selectCSSEvent(this);">';
		
		var ss =
			(enableflag > 1) ? document.styleSheets :
				document.all ? document.all.tags('LINK') : document.getElementsByTagName('LINK');
		
		for (var i=0; i<ss.length; i++) {
			if ((ss[i].type != "text/css") || (!ss[i].title)) continue;
			html += '<option value="'
				  + ss[i].title
				  + ((ss[i].title == sheet) ? '" selected="selected">' : '">')
				  + ss[i].title
				  + '</option>';
		}
		html += '</select>';
		document.write('<div align="right">', html, '</div>');
	}
}


// ブラウザのメニューからスタイルシートを選びなおしても次に引き継がれるように
// 現在適用されているスタイルシートをクッキーに保存する
function savePresentSheet () {
	if (!sheet) return;
	
	var ss =
		(enableflag > 1) ? document.styleSheets :
			document.all ? document.all.tags('LINK') : document.getElementsByTagName('LINK');
	
	var present_sheets;
	for (var i=0; i<ss.length; i++) {
		if (ss[i].type != "text/css") continue;
		if ((!ss[i].disabled) && (ss[i].title)) {
			present_sheets = ss[i].title;
			break;
		}
	}
	if (present_sheets != sheet)
		setCookie(cname, present_sheets);
}


// クッキーを取得
function getCookie (key) {
	var tmp, kstart, vstart, pos;
	
	tmp = document.cookie + ";";
	kstart = 0;
	vstart = key.length + 1;
	while (vstart < tmp.length) {
		pos = tmp.indexOf(";", vstart);
		if (pos == -1) break;
		
		if (tmp.substring(kstart, vstart) == key + "=")
			return (unescape(tmp.substring(vstart, pos)));
		else
			for (pos++; (pos < tmp.length) && (tmp.charAt(pos) == " "); pos++) ;
		kstart = pos;
		vstart = kstart + key.length + 1;
	}
	return("");
}


// クッキーを設定
function setCookie (key, val) {
	var exp = new Date();
	
	if (val != "")
		exp.setTime(exp.getTime() + cdays*24*60*60*1000);
	else
		exp.setTime(exp.getTime() - 24*60*60*1000);
	
	document.cookie = key + "=" + escape(val)
		+ ((cdays != 0) ? ("; expires=" + exp.toGMTString()) : '')
		+ ((cpath != "") ? ("; path=" + cpath) : '');
}


// document.styleSheetsかdocument.all.tags('LINK')で取得するLINK要素のdisabledプロパティを
// 変更することでスタイルシートを切り替えることができる
//
// WinIEでは、定義されたLINK要素はすべて有効に(disabled=false)なってしまうらしいので
// document.styleSheetsを使わなければならない。
// ただし、MacIE4.0は代替スタイルシートを認識しないので除外する
// MacIE4.5もstyleSheets.titleが取得できないので除外する
//
// Mozillaでは読み込み完了前にdocument.styleSheetsを取得してしまうと代替スタイルシートが
// 正しく含まれていない不完全なコレクションを参照し続ける場合があるらしい。
// 代わりにdocument.all.tags("LINK")を使う。
// if (document.styleSheets) のように論理値として評価する構文では問題ない。
//
// Opera7ではdocument.styleSheetsは定義されてないが、document.all.tags("LINK")の方は
// 問題ないのでこれを使う。
// Opera6ではdisabledプロパティが読み出し専用なので実行できない

// enableflag = 1 の時、document.all.tags('LINK')
// enableflag = 2 の時、document.styleSheets
var ua = navigator.userAgent;

if (document.styleSheets) {
	if (isMozilla)
		enableflag = 1;
	else if (!(ua.indexOf('MSIE 4.') > -1 && ua.indexOf('Mac') > -1))
		enableflag = 2;
} else if (ua.match && ua.match(/Opera[ \/]+(\d+)\./i)) {
	if (RegExp.$1 >= 7)
		enableflag = 1;
}

if (enableflag) {
	
	sheet = getCookie('StyleSheet');
	if (sheet == 'undefined') sheet = "";
	
	if (isMozilla) {
		// meta要素で既定のスタイルを設定する
		if (sheet && isExistsCSS(sheet)) {
			document.write('<meta http-equiv="Default-Style" content="'+ sheet +'">');
		}
		window.onload = initStyle;
	} else {
		initStyle();
	}
	window.onunload = savePresentSheet;
}

