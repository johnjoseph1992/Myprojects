from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^loginrequest$', views.loginrequest, name='loginrequest'),
    url(r'^homeviewurl$', views.homeviewurl, name='homeviewurl'),
    url(r'^signuppage$', views.signuppage, name='signuppage'),
    url(r'^signuprequest$', views.signuprequest, name='signuprequest'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^getschools$', views.getschools, name='getschools'),
    url(r'^loginpage$', views.loginpage, name='loginpage'),
    url(r'^startquizpage$', views.startquizpage, name='startquizpage'),
    url(r'^startaquiz$', views.startaquiz, name='startaquiz'),
    url(r'^submitnext$', views.submitnext, name='submitnext'),
    url(r'^skipanswer$', views.skipanswer, name='skipanswer'),

#quiz report
    url(r'^quizreportpage$', views.quizreportpage, name='quizreportpage'),
    url(r'^getallquiz$', views.getallquiz, name='getallquiz'),
    url(r'^getquizdetails$', views.getquizdetails, name='getquizdetails'),


#teacher's page
    url(r'^teacherhomeviewurl$', views.teacherhomeviewurl, name='teacherhomeviewurl'),
    url(r'^performance$', views.performance, name='performance'),
    url(r'^getstudents$', views.getstudents, name='getstudents'),
    url(r'^getallquizforuid$', views.getallquizforuid, name='getallquizforuid'),
    url(r'^leaderboard$', views.leaderboard, name='leaderboard'),
    url(r'^getleaderdata$', views.getleaderdata, name='getleaderdata'),
    url(r'^loadcities$', views.loadcities, name='loadcities'),
    #url(r'^loadschools$', views.loadschools, name='loadschools'),
    url(r'^getfilteredleaderdata$', views.getfilteredleaderdata, name='getfilteredleaderdata'),
    url(r'^pdf_view$', views.pdf_view, name='pdf_view'),fsdf



]
