# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from django.db import models


class DemoModel1(models.Model):
    CHOICES = ((1, 'Choice 1'), (2, 'Choice 2'), (3, 'Choice 3'))

    fk = models.ForeignKey(User,
                           on_delete=models.CASCADE,
                           blank=True, null=True)
    char = models.CharField(max_length=255)
    integer = models.IntegerField()
    logic = models.BooleanField(default=False)
    null_logic = models.NullBooleanField(default=None)
    date = models.DateField()
    nullable = models.CharField(max_length=255, null=True, default=None)
    choice = models.IntegerField(choices=CHOICES)


class DemoModel2(models.Model):
    fk = models.ForeignKey(DemoModel1,
                           on_delete=models.CASCADE,
                           blank=True, null=True)
    char = models.CharField(max_length=255, blank=True, null=True)
    integer = models.IntegerField(blank=True, null=True)


class DemoModel3(models.Model):
    fk = models.ForeignKey(DemoModel1,
                           on_delete=models.CASCADE)
    char = models.CharField(max_length=255, blank=True, null=True)
    integer = models.IntegerField(blank=True, null=True)

