#!/usr/bin/python3
#-*- coding:UTF-8 -*-

class people:
  name = ''
  age = 0
  __weight = 0
  def __init__(self,n,a,w):
    self.name = n
    self.age = a
    self.__weight = w

  def speak(self):
    print("%s 说：我%d岁。"%(self.name,self.age))

#单继承实例
class student(people):
  grade = ''
  def __init__(self,n,a,w,g):
    people.__init__(self,n,a,w)
    self.grade = g

  def speak1(self):
    print("%s说：我%d岁了，我在读%d年级。"%(self.name,self.age,self.grade))

#另一个类
class speaker():
  topic = ''
  name = ''
  def __init__(self,n,t):
    self.name = n
    self.topic = t
  def speak12(self):
    print("我叫%s,我是一个演说家，我演讲的主题是%s"%(self.name,self.topic))


#多重继承
class sample(speaker,student):
  a = ''
  def __init__(self,n,a,w,g,t):
    student.__init__(self,n,a,w,g)
    speaker.__init__(self,n,t)

test = sample("Tim",15,80,4,'python')
test.speak()