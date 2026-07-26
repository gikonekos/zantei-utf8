# TreeNode オブジェクトはツリーの個々のノードを記述します。
package TreeNode;
use strict;
sub new
{
	my ($pkg, $ptr) = @_;

	my $class =	bless{
		Ptr			=> $ptr,
		ItemId		=> '',
		Parent		=> undef,
		Index		=> undef,
		Count		=> '0',
		HasChild	=> '0',
		Level		=> '0',
		Item		=> [],
	},$pkg;
}

# ItemID プロパティを使うと, TreeNodes の GetNode メソッドで
# ノードを取得することができます。
sub ItemId
{
	my $self = shift;
	if (@_) { $self->{ItemId} = shift }
	return $self->{ItemId};
}

# Parent プロパティはノードの親ノードを識別します。
sub Parent
{
	my $self = shift;
	if (@_) { $self->{Parent} = shift }
	return $self->{Parent};
}

# Count プロパティは，ノードの直接の下位項目の数を示します。
sub Count
{
	my $self = shift;
	if (@_) { $self->{Count} = shift }
	return $self->{Count};
}

# Level プロパティは,TreeNodes内のノードの深さを示します。
# TreeNodes->Rootのレベルは-1です｡
sub Level
{
	my $self = shift;
	if (@_) { $self->{Level} = shift }
	return $self->{Level};
}

# Index プロパティは，親ノードが保守する子ノードリストでのノードの位置を指定します。
sub Index
{
	my $self = shift;
	if (@_) { $self->{Index} = shift }
	return $self->{Index};
}

# Item プロパティは､子ノードリストへのリファレンスを返します｡
# 引数があれば子ノードリストへ引数のノードを加えます｡
sub Item
{
	my $self = shift;
	if (@_) {
		# Itemリスト Indexの設定 Countプロパティ､の更新
		my $NewItem = shift;
		push @{$self->{Item}}, $NewItem;
		my $ItemVal = @{$self->{Item}};
		$NewItem->Index($ItemVal - 1);
		$self->Count($self->Count + 1);
	}
	return $self->{Item};
}

# HasChildrenはノードに子があるかどうかを示します。
sub HasChildren
{
	my $self = shift;
	($self->Count > 0) ? return 1 : return 0;
}

# EventSubtreeは自分の配下ノードすべてに
# 引数で渡されたイベントを起こします｡
# イベントは､該当ノードを一番目の引数に持ちます｡
#
# 例
# すべての配下ノードの深さを書き出す｡
#
# $TreeNode1->EventSubtree(sub {
# 	my $self = shift;
#	print $self->Level, "\n";
#});
#

sub EventSubtree {
	my ($self, $Event) = @_;

	&$Event($self);
	for my $ChildNode (@{$self->Item}) { $ChildNode->EventSubtree($Event) }
}


# TreeNodes オブジェクトはTreeNodeのリストを保持します。
package TreeNodes;
use strict;
sub new
{
	my ($pkg) = @_;

	# Rootノードの作成
	my $Root = TreeNode->new();
	$Root->ItemId(-1);
	$Root->Level(-1);

	my $class = bless{
		Count 	=> '0',
		ItemId	=> {},
	}, $pkg;

	$class->_AddRoot($Root);
	return $class;
}

# AddChild メソッドは，新しいツリーノードをツリービューに追加します。
# AddChild(ParentNode, Node: TreeNode): TreeNode;
sub AddChild
{
	my ($self, $ParentNode, $Node) = @_;

	$Node->Parent($ParentNode);
	$Node->Level($ParentNode->Level + 1);
	$ParentNode->Item($Node);
	$self->_Item($Node);
	return $Node;
}

# Count プロパティは，TreeNodes オブジェクトが保守するノード数を示します。
sub Count
{
	my $self = shift;
	if (@_) { $self->{Count} = shift }
	return $self->{Count};
}

# GetNode メソッドは，ノードの指定された ItemId パラメータからツリーノードを返します。
# 見つからない場合､undefを返します｡
# GetNode(ItemId: integer): TreeNode;
sub GetNode
{
	my ($self, $ItemId) = @_;
	if (exists $self->{ItemId}->{$ItemId}) {
		return $self->{ItemId}->{$ItemId};
	} else {
		return undef;
	}
}

# Rootノードを返します
sub Root
{
	my $self = shift;
	if (@_) { $self->{Root} = shift; }
	return $self->{Root};
}

sub _AddRoot
{
	my ($self, $Root) = @_;

	push @{$self->{Item}}, $Root;
	$self->Root($Root);
}

sub _Item
{
	my $self = shift;
	if (@_) { 
		my $Item = shift;
		my $ItemId = $Item->{ItemId};
		$self->{ItemId}->{$ItemId} = $Item;
		push @{$self->{Item}}, $Item;
		$self->Count($self->Count + 1);
	}
	return $self->{Item};
}


1;
