from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from newcourse.models import User, ClassComment, UserProfile, Prof, ProfComment, Course
from newcourse.forms import UserForm, UserProfileForm, ClassCommentForm, ProfCommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
import random
import requests
import json
from django.core.mail import EmailMessage

api_key = '?token=1W2mtKYd1LjylX0r1721BbWFsJOqm3'
api_base = 'http://api.penncoursereview.com/v1/'

dept_results = []


def cleanall (request):
    (Course.objects.all()).delete()
    try:
        Course.objects.all()
        return index(request)

    except:
        return HttpResponse('done')


def addurl(subject_list):
    for subject in subject_list:
        subject.url = subject.name.replace(' ', '_')

def index(request):
    context = RequestContext(request)
    return render_to_response('newcourse/index.html', {}, context)

def about(request):
    context= RequestContext(request)
    return render_to_response('newcourse/about.html', {'mymessage': "Work in progress."}, context)



def deptlist(request, thetype):
    context = RequestContext(request)
    go = api_base + thetype + api_key
    head = 'Departments'
    if not dept_results:

        response = requests.get(go)

        comp = (response.json()['result']['values'])

        for a in comp:
            dept_results.append({
            'name': a['name'],
            'path': a['path'],
            'id': a['id']
            })
    return render_to_response('newcourse/the_list.html', {'results': dept_results,
                                                         'thetype': head,
                                                         }, context)


def proflist(request, thetype, page):
    context = RequestContext(request)
    go = api_base + thetype + api_key
    head = 'Professors'
    if not Prof.objects.all():
        sortprof(go)

    sorted_prof = Prof.objects.filter(name__startswith=chr(65 + int(page)))

    return render_to_response('newcourse/the_prof_list.html', {'results': sorted_prof,
                                                         'thetype': head,
                                                         }, context)

def sortprof(go):
    response = requests.get(go)
    comp = (response.json()['result']['values'])
    for a in comp:
        Prof.objects.create(name= a['name'], path = a['path'])



def sortcourse(go, results, thetype):
    response = requests.get(go)
    val = 0
    for a in (response.json()['result']['coursehistories']):

        try:
            Course.objects.get(theid = a['id'])
        except:
            try:
                Course.objects.get(name = a['name'])
                Course.objects.create(name = str(a['name']) + ' ' + str(val) , theid = a['id'], thetype=thetype)
                val = val + 1
            except:
                Course.objects.create(name = a['name'], theid = a['id'], thetype=thetype)
                val = 0


        results.append({
            'name':a['name'],
            'id': a['id'],
            'aliases': a['aliases']
            })

def courselist(request, thetype):
    context = RequestContext(request)
    go = api_base + '/depts/' + thetype + api_key
    head = thetype

    results= []
    if not Course.objects.filter(thetype = thetype):
        sortcourse(go, results, thetype)

    else:
        response = requests.get(go)
        for a in (response.json()['result']['coursehistories']):
            results.append({
                'name':a['name'],
                'id': a['id'],
                'aliases': a['aliases']
                })

    courses = Course.objects.all()
    return render_to_response('newcourse/the_course_list.html', {
                                                         'thetype': head,
                                                         'courses': courses,
                                                         'results': results,
                                                         }, context)



def instructor(request, theid):
    context= RequestContext(request)
    prof = (Prof.objects.get(id = theid))
    thetype = prof.path
    thename = prof.name
    go = ('https://penncoursereview.com/' + thetype).replace('instructors', 'instructor')
    response = requests.get(api_base + thetype + api_key)
    results = []
    comments = (ProfComment.objects.filter(yourprof = thename)).order_by('-timeposted')
    for a in (response.json()['result']['reviews']['values']):
        add = str((a['section']['primary_alias'])[:-4])
        if not add in results:
            results.append(add)

    return render_to_response('newcourse/instructor.html', {'go': go,
                                                            'results': results,
                                                            'thename': thename,
                                                            'theid': theid,
                                                            'comments': comments,
                                                            }, context)


################################################
def coursepage(request, theid):
    context= RequestContext(request)
    course = Course.objects.get(theid = theid)

    thename = course.name
    comments = (ClassComment.objects.filter(yourclass = thename)).order_by('-timeposted')


    return render_to_response('newcourse/course.html', {
                                                            'thename': thename,
                                                            'comments': comments,
                                                            'theid': theid
                                                            }, context)
##########################################

@login_required
def add_classcomment(request, theid):
    context = RequestContext(request)
    yourclass = (Course.objects.get(theid = theid)).name

    if request.method == 'POST':
        form = ClassCommentForm(request.POST)
        if form.is_valid():
            comm = form.save(commit=False)
            profile = request.user.get_profile()
            comm.yourschool = profile.school
            comm.yourclass = yourclass
            comm.save()
            return coursepage(request, theid)
        else:
            print form.errors
    else:
        form= ClassCommentForm()
    return render_to_response('newcourse/course_comment.html', {
                                                        'form': form,
                                                        'theid': theid,

                                                        }, context)


@login_required
def add_profcomment(request, theid):
    context = RequestContext(request)
    prof = (Prof.objects.get(id = theid))
    if request.method == 'POST':
        form = ProfCommentForm(request.POST)
        if form.is_valid():
            comm = form.save(commit=False)
            profile = request.user.get_profile()
            comm.yourschool = profile.school
            comm.yourprof = prof.name
            comm.save()
            return instructor(request, theid)
        else:
            print form.errors
    else:
        form= ProfCommentForm()
    return render_to_response('newcourse/prof_comment.html', {
                                                        'form': form,
                                                        'theid': theid,
                                                        }, context)


def register(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        return HttpResponseRedirect('/localquaker/')

    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data= request.POST)
        if user_form.is_valid() and profile_form.is_valid:
            user = user_form.save()


            user.set_password(user.password)
            user.is_active = False
            user.save()
            profile = profile_form.save(commit= False)

            profile.user=user

            profile.activation_key = (str(random.randint(0, 9999999)) + str(user.id))
            email_subject = 'LocalQuaker Confirmation'
            email_body = "To activate your account, click this link: \n\n http://tahmidshahriar1994.pythonanywhere.com/localquaker/confirm/%s" % (
                profile.activation_key)
            email = EmailMessage(email_subject, email_body, to=[user.email])
            email.send()

            if ((user.email).endswith("seas.upenn.edu")):
                profile.school = 'Engineering'

            elif ((user.email).endswith("wharton.upenn.edu")):
                profile.school = 'Wharton'
            elif ((user.email).endswith("nursing.upenn.edu")):
                profile.school = 'Nursing'
            else:
                profile.school = 'College'



            profile.save()
            registered = True

        else:
            print user_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response(
            'newcourse/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)



def confirm(request, activation_key):
    userprofile = UserProfile.objects.get(activation_key=activation_key)
    userprofile.user.is_active = True
    userprofile.user.save()
    userprofile.save()

    return HttpResponseRedirect('/localquaker/login/')


def user_login(request):
    context= RequestContext(request)
    if request.user.is_authenticated():
        return HttpResponseRedirect('/localquaker/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/localquaker/')
            else:
                context_dict = {'error' :'An inactive account was used.'}
                return render_to_response('newcourse/login.html', context_dict, context)

        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            context_dict = {'error' :  'Wrong username or password.'}
            return render_to_response('newcourse/login.html', context_dict, context)

    else:
        return render_to_response('newcourse/login.html',{}, context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/localquaker/')
