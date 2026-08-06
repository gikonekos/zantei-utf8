#!/usr/bin/perl  --           # Access Counter Version 2.2
# 変更する場合: ##!/usr/local/bin/perl

$COUNT_FILE   = 'counter.dat';
$COUNT_FILE2  = 'counter.bak';
$IPDB_DIR     = 'counterdb';

$IPDB_TIMER_UNIT  = 600;
$IPDB_LIFETIME    = 6;

$GARBAGE_COLLECTION_TIMER   = 100;
$IMAGE_DIR  = '/diary';
$IMAGE_MINI = 6;

#######################################################################

umask(066);
use strict;
use vars qw( $COUNT_FILE $COUNT_FILE2 $IPDB_DIR $IPDB_TIMER_UNIT );
use vars qw( $GARBAGE_COLLECTION_TIMER $IMAGE_DIR $IMAGE_MINI $IPDB_LIFETIME );

sub LOCK_SH { 1 }
sub LOCK_EX { 2 }
sub LOCK_NB { 4 }
sub LOCK_UN { 8 }

my ($number,@counter,$status);
$status = 0;

$number = read_counter($COUNT_FILE,$COUNT_FILE2);
if ($IPDB_DIR) {
    if (!-d $IPDB_DIR) {
mkdir($IPDB_DIR,0700);
    }
    ($status,$number) = remote_addr_check($IPDB_DIR, $ENV{REMOTE_ADDR},
  $number,
  $IPDB_TIMER_UNIT, $IPDB_LIFETIME);
}
else {
    $number++;
}

if ($status == 0) {
    write_counter($COUNT_FILE,$COUNT_FILE2,$number);

    if (-d $IPDB_DIR &&
($number % $GARBAGE_COLLECTION_TIMER) == 0)
    {
garbage_collection($IPDB_DIR,$IPDB_TIMER_UNIT,$IPDB_LIFETIME);
    }
}

@counter = ($number=~ /(\d)/g);
for (my $n=$#counter + 1;$n < $IMAGE_MINI;$n++) {
    unshift(@counter,0);
}

$IMAGE_DIR=~ s#/$##;
$|=1;
print "Content-type: image/gif\r\n\r\n";
foreach my $key (@counter){
    print qq<<IMG SRC="$IMAGE_DIR/$key.gif" ALT="$key">>;
}

exit(0);

###################################################################

sub read_counter ($$) {
    my $master_file = shift;
    my $slave_file = shift;
    my $master_nu  = 0;
    my $slave_nu = 0;
    my $t   = 0;

    if (-f $master_file) {
      READ: {
  if ($t < 10) {
      open(F,$master_file)
  or $t++ and sleep(0.1) and redo READ;
      $master_nu = <F>;
      close(F);
      $master_nu=~ s/\D//g;
  }
  else {
      $master_nu = -1;
  }
      }
    }

    $t   = 0;
    if (-f $slave_file) {
      READ: {
  if ($t < 10) {
      open(F,$slave_file)
  or $t++ and sleep(0.1) and redo READ;
      $slave_nu = <F>;
      close(F);
      $slave_nu=~ s/\D//g;
  }
  else {
      $slave_nu = -1;
  }
      }
    }

    if ($master_nu < $slave_nu) {
$master_nu = $slave_nu;
    }

    return $master_nu;
}


sub write_counter ($$$) {
    my $master_file = shift;
    my $slave_file  = shift;
    my $nu   = shift;

    my $t = 0;
    
    if ($nu > 0) {
      WRITE: {
  if ($t < 10) {
      open(F,">$master_file")
  or $t++ and sleep(0.1) and redo WRITE;
      flock(F,LOCK_EX);
      seek(F,0,0);
      printf F "%10d\n",$nu;
      close(F);
  }
      }
    }

    if ($nu > 0 && $nu % 4 == 0) {
      WRITE: {
  if ($t < 10) {
      open(F,">$slave_file")
  or $t++ and sleep(0.1) and redo WRITE;
      flock(F,LOCK_EX);
      seek(F,0,0);
      printf F "%10d\n",$nu;
      close(F);
  }
      }
    }

    return $nu;
}


sub remote_addr_check ($$$$$) {
    my $dbdir= shift;
    my $ip   = shift;
    my $number    = shift;
    my $timer_unit = shift;
    my $lifetime   = shift;

    my $status = 0;
    my $time = time;
    my $now_filename = int($time/($timer_unit/$lifetime));

    my $pattern_ip= $ip;
    $pattern_ip=~ s/\./\./g;

  CHECK_DATA:
    for (my $n=0;$n <= $lifetime;$n++) {
my $filename=$now_filename - $n;
if (-f "$dbdir/$filename") {
    open(F,"$dbdir/$filename");
    while (<F>) {
if (/^$pattern_ip;(\d+)/o) {
    $status = 1;
    $number = $1;
    close(F);
    last CHECK_DATA;
}
    }
    close(F);
} 
    }

    if ($status == 0) {
$number++;
open(F,">>$dbdir/$now_filename");
flock(F,LOCK_EX | LOCK_NB) or
    flock(F,LOCK_EX);
seek(F,0,2);
print F "$ip;$number\n";
close(F);
    }

    return($status,$number);
}


sub garbage_collection ($$$) {
    my $dbdir= shift;
    my $timer_unit = shift;
    my $lifetime = shift;

    my $time = time;
    my $need_data =    int($time/($timer_unit/$lifetime)) - $lifetime;

    opendir(DIR,$dbdir);
    foreach my $file (grep(/^\d+$/,readdir(DIR))) {
if ($file < $need_data) {
    unlink("$dbdir/$file");
}
    }
    closedir(DIR);
}


sub sleep ($) {
    select(undef,undef,undef,$_[0]);
}


__END__
