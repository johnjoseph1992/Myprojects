# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class School(models.Model):
	schoolid = models.AutoField(primary_key=True)
	startstd = models.IntegerField(default=1)
	endstd = models.IntegerField(default=12)
	schoolname = models.CharField(max_length=50)

class QuizLogin(models.Model):
	userid = models.AutoField(primary_key=True)
	username = models.CharField(max_length=20)
	password = models.CharField(max_length=20)
	usertype = models.CharField(max_length=10)
	standard = models.IntegerField(null=True)
	city = models.CharField(max_length=50)
	schoolid = models.ForeignKey(School)

class Question(models.Model):
	qid = models.AutoField(primary_key=True)
	question = models.CharField(max_length=100)
	qtype = models.CharField(max_length=10)
	options = models.CharField(max_length=100)
	correct = models.CharField(max_length=30, null=True)

class Quizattended(models.Model):
	quizid = models.AutoField(primary_key=True)
	userid = models.ForeignKey(QuizLogin)
	score = models.IntegerField()

class Quizdetails(models.Model):
	quizdetailsid = models.AutoField(primary_key=True)
	answeredoption = models.CharField(max_length=100, null=True) #correct,incorrect,skipped(null)
	quizid = models.ForeignKey(Quizattended)
	qid = models.ForeignKey(Question)




