from django.db import models

class GeneInfo(models.Model):
    genename=models.CharField(max_length=500)
    genedescription=models.CharField()
    genesectiongroup=models.CharField()
    geneprobetype=models.CharField(max_length=500)
    createtime=models.DateTimeField()