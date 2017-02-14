from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import Image as Im
from game.models import Image, Crop, UserProfile, CropOrder
from game.forms import ImageForm, CropForm
import logging
import os
import string
import random
import json
import time
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
import re

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_ROOT=os.path.join(BASE_DIR, 'ImageFolder')

def startNewImage(index,user=None):
    used = 5
    crops=[]
    letters = ""
    level = index
    if index <= Image.objects.all().count():
        p=Image.objects.get(id=index)
        allCrops=p.crop_set.all()
        order = map(int,(CropOrder.objects.get(level=index).order.split(",")))
        for i in range(5):
            crops.append(allCrops[order[i]])
            #print order[i]
        level = p.level
        answer=p.answer
        flip_time = 120
        for i in range(len(answer)):
            letters+=" __ "
        points = 100

    #update users stats    
    if user != None:
        print "starting new game with a user"
        userProfile = UserProfile.objects.get(user=user)
        userProfile.cropNumber = used
        userProfile.level = level
        userProfile.letters = letters
        flip_time = userProfile.time_till_flip
        userProfile.lastPlayed = datetime.now()
        userProfile.save()
        
    return (crops, level, used, letters,flip_time, points)

def loadGame(userProfile):
    p=Image.objects.get(id=userProfile.level)
    letters = userProfile.letters
    if letters == p.answer:
        crops, level, used, letters,flip_time, points = startNewImage(userProfile.level+1, userProfile.user)
    else:
        crops=[]
        allCrops=p.crop_set.all()
        order = map(int,(CropOrder.objects.get(level=userProfile.level).order.split(",")))
        for i in range(userProfile.cropNumber):
            crops.append(allCrops[order[i]])
            #print order[i]
        level = userProfile.level
        answer=p.answer
        flip_time = userProfile.time_till_flip
        userProfile.lastPlayed = datetime.now()
        used = userProfile.cropNumber
        points = get_points_from_letters(userProfile.letters, answer)
    return (crops, level, used, letters,flip_time, points)

def getNewCrop(request):
    """
    Gives the information for a new crop on a flip button press
    :param String level is the current user level
    :param String used is the current number of crops used
    :returns crop position (x,y), name and errors

    """
    context = RequestContext(request)
    level = 1
    used = 4
    if request.method == 'GET':
        level = int(request.GET['level'])
        used = int(request.GET['used'])
        p=Image.objects.get(id=level)
        allCrops=p.crop_set.all()
        crops=[]
        order = map(int,(CropOrder.objects.get(level=level).order.split(",")))
        crop = allCrops[order[used]]
        print order[used]
        crop_data = {}
        crop_data['x'] = crop.position_x
        crop_data['y'] = crop.position_y
        crop_data['name'] = crop.croppedImage.name
        crop_data['error'] = ""
        if request.user.is_authenticated():
            userProfile=UserProfile.objects.get(user=request.user)
            userProfile.lastPlayed = datetime.now()
            userProfile.cropNumber = used
            userProfile.flips = request.GET['flips']
            userProfile.save()     
        return HttpResponse(json.dumps(crop_data), content_type="application/json")
    else:
        return HttpResponse("error")

def getLetters(request):
    if request.method=='GET':
        level = int(request.GET['level'])
        current = request.GET['currentState']
        answer = Image.objects.get(id=level).answer
        newHolder = ""
        print(current);
        if (current == "new"):
            for i in range(len(answer)):
                newHolder+=" __ "
            return HttpResponse(newHolder)
    return HttpResponse()


def getAllCrop(index):
    crops=[]
    p=Image.objects.get(id=index)
    allCrops=p.crop_set.all()
    return (allCrops, index, [], 0)

def getOldCrop(index, used, order):
    crops=[]
    p=Image.objects.get(id=index)
    allCrops=p.crop_set.all()
    for i in range(1,used+1):
        crops.append(allCrops[order[i]])
    return (crops, index, order, used)

def checkGuess(request):
    if request.method=='GET':
        data = {}
        level = int(request.GET['level'])
        guess = request.GET['guess'].lower()
        print guess
        letters = request.GET['letters']
        answer = Image.objects.get(id=level).answer.lower()
        data['image'] = str(Image.objects.get(id=level).wholeImage.name)
        if (guess==answer):
            data['status'] = "correct"
            data['letters'] = answer
        else:
            data['status'] = "wrong"
            letters.count('__')
            data['letters']=getNewLetters(letters, answer)
            if (letters == getNewLetters(letters,answer)):
                data['error']= "next"
                
            else:
                data['error'] = None
        
        if request.user.is_authenticated():
            userProfile=UserProfile.objects.get(user=request.user)
            userProfile.letters = data["letters"]
            userProfile.lastPlayed = datetime.now()
            if data['status'] == "correct":
                userProfile.score +=int(request.GET['points'])
            userProfile.save()     

        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return HttpResponse("error")

def get_points_from_letters(letters, answer):
    return 100 - 10*(len(answer)- letters.count("__"))



def getNewLetters(letters, answer):
    """
    Returns the new string of letter hints
    :param String letters is the current letters being userd
    :param String answer is the answer to the puzzle
    :returns String letters of new letter hints
    """
    current = list(letters)
    count = letters.count('__')
    if (count == len(answer)):
        place = random.randint(0,len(answer)/4)
        current[place*4+1] = answer[place]
        current[place*4] = " "
        current[place*4+2] = " "
        current[place*4+3] = " "
        return "".join(current)
    elif (count != 0):
        array = find(letters, "__")
        place = (random.choice(array)-1)/4
        current[place*4+1] = answer[place]
        current[place*4] = " "
        current[place*4+2] = " "
        current[place*4+3] = " "
        return "".join(current)
    else: return letters

def find(s, ch):
    """ 
    Find all occurances of ch in string s. Courtesy of Lev Levitsky on StackOverflow
    """
    return [m.start() for m in re.finditer(ch, s)]
    


def index(request):
    pIndex=1
    if request.method=="POST":
        form = CropForm(request.POST)
        if form.is_valid():
            # if 'guessEntered' in request.POST:
            #     flag = False
            #     guess = request.POST['guess']
            #     index = int(request.POST['level'])
            #     print type(index)
            #     print guess
            #     flips = int(request.POST['flips'])
            #     print Image.objects.get(id=index).answer
            #     if guess == Image.objects.get(id=index).answer:
            #         print "getting new image"
            #         #crops, level, order, used = startNewImage(int(request.POST['level'])+1)
            #         crops, level, order, used = getAllCrop(int(request.POST['level']))
            #         score = int(request.POST['score'])+int(request.POST['points'])
            #         points = 100
            #         guessed="correct"
            #     else:
            #         print "incorrect guess"
            #         print request.POST['level']
            #         crops, level, order, used = getOldCrop(request.POST['level'], int(request.POST['used']),  eval(request.POST['order']))
            #         points = int(request.POST['points'])-10
            #         score = int(request.POST['score'])
            #         guessed="wrong"
            if 'next' in request.POST:
                print "next called"
                flag = False
                index = int(request.POST['level'])
                flips = int(request.POST['flips'])
                if request.user.is_authenticated():
                    crops, level, used, letters, flip_time, points = startNewImage(index+1, request.user)
                else:
                    crops, level, used, letters, flip_time, points = startNewImage(index+1)
                score = int(request.POST['score'])
                guessed = ""
            return render_to_response(
                'game/index.html',{'crops':crops, 'level':level, 'used':used, 'flag':flag, 'guessed':guessed, 'letters':letters, 'flips':flips, 'score':score, 'points':points, 'form':form, 'flip_time':flip_time},
                context_instance=RequestContext(request)
            )

    else:
        print "not post"
        form = CropForm()
    if request.user.is_authenticated():
        print request.user
        userProfile = UserProfile.objects.get(user=request.user)
        index=userProfile.level
        score = userProfile.score
        flips = userProfile.flips
        crops, level, used, letters, flip_time, points = loadGame(userProfile)
    else:
        index = 1
        score = 0
        flips = 3
        crops, level, used, letters, flip_time, points = startNewImage(index)
    flag = False
    return render_to_response(
        'game/index.html',{'crops':crops, 'level':level, 'used':used, 'flag':flag, 'guessed': str(0), 'letters':letters, 'flips':flips, 'points':points, 'score':score, 'form':form, 'flip_time':flip_time},
        context_instance=RequestContext(request)
    )

def shuffleOrder():
    order = range(0,120)
    random.shuffle(order)
    order = map(str, order)
    order = ",".join(order)
    return order

def name_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def processForm(request):
    if request.method=="POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            addImage = Image(wholeImage=request.FILES['docfile'],level=request.POST['level'],answer=request.POST['answer'])
            addImage.save()
            end = Image.objects.all()
            end= end.count()
            p=Image.objects.get(id=end)
            print end
            image = Im.open(p.wholeImage)
            if int(request.POST['level']) in range(1,20):
                for i in range(0,10):
                    for j in range(0,12):
                        box = (50*i,50*j,50*(i+1),50*(j+1))
                        crop = image.crop(box)
                        ext = p.wholeImage.name.split('.')[-1]
                        filename = "%s.%s" % (name_generator(), ext)
                        print filename
                        holder = "ImageFolder/croppedImages/"+str(p.level)+"/"+filename
                        crop.save(holder)
                        p.crop_set.create(image=p, croppedImage=holder,position_x=i,position_y=j)
                        #print something.image
                        #something.save()
                        #p.crop_entry.add(something)

            cropOrder = CropOrder(level=addImage.level, order = shuffleOrder())
            cropOrder.save()
            return HttpResponseRedirect('../processImages')
    else:
        form= ImageForm()

    images= Image.objects.all()

    return render_to_response(
        'game/upload.html',{'images':images, 'form':form},
        context_instance=RequestContext(request)
    )