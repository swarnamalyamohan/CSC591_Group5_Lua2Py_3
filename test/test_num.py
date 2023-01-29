import sys
sys.path.append("./src")

from num import NUM

test_obj=NUM(2,'Hp+')

test_obj.add('?')
test_obj.add(120)
test_obj.add(44.5)
test_obj.add(100)


print("Mean = ",test_obj.mid())
print("Standard deviation = ",test_obj.div())
print("100.57358 rounded off to two decimal places = ",test_obj.rnd(100.57358,2))
print("Normalised value of 95.6 is = ",test_obj.norm(95.6))
print("Distance between 95.6 and 101.4 is = ",test_obj.dist(95.6,101.4))
print("Normalised value of 95.6 and ? is = ",test_obj.dist(95.6,'?'))

