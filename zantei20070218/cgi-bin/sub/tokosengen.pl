#! /usr/local/bin/perl

# 環境変数

	$addr01 = $ENV{'REMOTE_ADDR'};
	$host01 = $ENV{'REMOTE_HOST'};
	$agent01 = $ENV{'HTTP_USER_AGENT'};

		if ( $addr01 eq $host01 || !$host01 ) {
			$host01 = gethostbyaddr ( pack ( 'C4', split ( /\./, $addr01 ) ), 2 ) || $addr01;
		}

# 配列

	@holidayhost = ('remotehost');

	local($match) = 0;
	foreach (@holidayhost) {
		if ($host01 =~ /$_/) { $match=1; }#ここでスイッチ
	}

# 制限

	if ($match) {
		$sptime =  15;
	}

1;

__END__
