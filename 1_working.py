import VOLTORBAnalysis as volta

b = volta.Board()
print(b) 
print(b.row(3).shown.coins)
b.update('cel',[2,3],{3})

print(b.row(3).shown.coins)
