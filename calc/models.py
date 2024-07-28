from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
class VaccantRacks(models.Model):
	category=models.CharField(max_length=100)
	rackname=models.TextField()
	capacity=models.IntegerField()
	#date_posted=models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.category
# for i in range(1,4):
# 	for j in range(1,6):
# 		for k in range(1,6):
# 			VaccantRacks.objects.create(category="A",rackname="A"+str(i)+"-B"+str(j)+"-C"+str(k),capacity=200000)
# for i in range(4,6):
# 	for j in range(1,6):
# 		for k in range(1,6):
# 			VaccantRacks.objects.create(category="B",rackname="A"+str(i)+"-B"+str(j)+"-C"+str(k),capacity=200000)
# for i in range(6,7):
# 	for j in range(1,6):
# 		for k in range(1,6):
# 			VaccantRacks.objects.create(category="C",rackname="A"+str(i)+"-B"+str(j)+"-C"+str(k),capacity=200000)
