if comment == 'match1' && extra.list :subsetof ['a', 'b', 'c', 'd'] {
	update comment = 'changed1'
}

if comment == 'match2' && extra.list :subsetof ['b', 'c', 'd', 'e'] {
	update comment = 'unreachable'
}

if comment == 'match3' && extra.list ! :subsetof ['b', 'c', 'd', 'e'] {
	update comment = 'changed3'
}

if comment == 'match4' && extra.list ! :subsetof ['a', 'b', 'c', 'd'] {
	update comment = 'unreachable'
}
