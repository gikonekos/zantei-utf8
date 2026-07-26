# パラメータ管理用モジュール
# 2003/11/16
# さやか
=comment

$ks_param = ks_param->new->set_param(
	tree	=> $FORM{tree},
	foo		=> 'bar',
);

上記のように値をセットしておき
以下のように使います

print qq{
<form>
	<INPUT type="submit" name="reload" value="リロード">
	$ks_param->{post}
</form>
};

print qq{ <a href="$cgiurl?$ks_param->{get}">リンク</a> };

=cut
package ks_param;

sub new { bless({}, $_[0]); }

sub set_param {
	my $me = shift;

	# 要素を上書き
	%{ $me->{param} } = (%{ $me->{param} }, @_,);

	# 要素が''のハッシュを削除
	for my $param (keys %{ $me->{param} }) {
		if ($me->{param}{$param} eq '') { delete $me->{param}{$param} }
	}

	$me->{post} = join("\n", map { qq~<input type="hidden" name="$_" value="$me->{param}{$_}">~ } keys %{ $me->{param} } );
	$me->{get}  = join('&', map { "$_=$me->{param}{$_}" } keys %{ $me->{param} });

	return $me;
}

sub get_param {
	my $me = shift;
	my $key = shift;

	return $me->{param}{$key};
}

1;
