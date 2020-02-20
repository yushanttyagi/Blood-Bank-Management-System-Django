from django.shortcuts import render
# Create your views here.
#from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from app.models import  orderdata as orderrr,bloodtype,donor,yadmin
from django.http import HttpResponse
from django.contrib import messages
from django.db import models
from django.db.models import Avg, Count,Q
Username=""
Password=""
def home(request):
    return render(request,"index.html")
def homes(request):
    if not request.session.get('logged_in'):
        messages.add_message(request, messages.INFO, 'Please LogIn')
        return render(request,'login.html')
    return render(request,"index-3.html")
def admintask(request):
    if not request.session.get('logged_in'):
        messages.add_message(request, messages.INFO, 'Please LogIn')
        return render(request,'login.html')
    return render(request,"admintask.html")


@csrf_exempt
def loginpage(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("psw")
        obj=yadmin.objects.all()
        for i in obj:
            if(i.username==username and i.passw==password):
                global Username
                global Password
                Username=username
                Password=password
                print("username:::"+Username)
                request.session['logged_in'] = True
                if not request.session.get('logged_in'):
                    return render(request,'login.html')
                messages.add_message(request, messages.INFO, 'Login Successfull.')
                return render(request , "admintask.html")
        messages.add_message(request, messages.INFO, 'Error Incorrect Password or Username.')
        return render(request,"login.html")
    return render(request,"login.html")

def lousy_secret(request):
    if not request.session.get('logged_in'):
        return redirect('loginpage')
    messages.add_message(request, messages.INFO, 'Login Successfull.')
    return render(request , "admintask.html")


def logout(request):
    if not request.session.get('logged_in'):
        messages.add_message(request, messages.INFO, 'Please LogIn')
        return render(request,'login.html')
    try:
        print('yessss:logged oooutututuututuufucj3383jjd')
        del request.session['logged_in']
    except KeyError:
        print('yessss:logged')
        return render(request,'login.html')
    return render(request, 'index.html')


def donorr(request):
    if not request.session.get('logged_in'):
        messages.add_message(request, messages.INFO, 'Please LogIn')
        return render(request,'login.html')
    return render(request,"Add_donor.html")

@csrf_exempt
def donorsubmit(request):
    if not request.session.get('logged_in'):
        messages.add_message(request, messages.INFO, 'Please LogIn')
        return render(request,'login.html')
    if(request.method=="POST"):
        firstname=request.POST.get("firstname")
        lastname=request.POST.get("lastname")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        dob=request.POST.get("dob")
        gender=request.POST.get("gender")
        country=request.POST.get("country")
        state=request.POST.get("state")
        quantity=request.POST.get("quantity")
        address=request.POST.get("address")
        aadhar=request.POST.get("aadhar")
        if(int(quantity)>450):
            messages.add_message(request, messages.INFO, 'Cannot donate more than 450 ml.')
            return render(request,"Add_donor.html")
        if(len(aadhar)!=16):
            messages.add_message(request, messages.INFO, 'aadhar should be of 16 digits.')
            return render(request,"Add_donor.html")
        blood=request.POST.get("blood")
        obj=donor(first=firstname,last=lastname,email=email,phone=phone,
            gender=gender,dob=dob,country=country,state=state,address=address,aadhar=aadhar,
            blood=blood,quantity=quantity)
        obj.save()
        ge=bloodtype.objects.get(blood=blood)
        ge.quant=ge.quant+(int(quantity)/1000)
        ge.save()
        messages.add_message(request, messages.INFO, 'Added Successfully to the Database.')
        return render(request,"Add_donor.html")
@csrf_exempt
def order(request):
    if(request.method=="POST"):
        blood=request.POST.get("blood")
        quantity=request.POST.get("quantity")
        orderby=request.POST.get("orderby")
        address=request.POST.get("address")
        orderd=request.POST.get("orderdate")
        shipd=request.POST.get("shipdate")
        phone=request.POST.get("phone")
        ge=bloodtype.objects.get(blood=blood)
        if(int(quantity)<1):
            messages.add_message(request, messages.INFO, 'Enter amount greater than 1')
            return render(request,"placeorder.html")
        if(ge.quant<=int(quantity)):
            messages.add_message(request, messages.INFO, 'Sufficient amount not available')
            return render(request,"admintask.html")
        else:
            ge.quant=ge.quant-(int(quantity))
            ge.quant=round(ge.quant,3)
            obj=orderrr(blood=blood,quantity=quantity,by=orderby,
                address=address,orderdate=orderd,shipdate=shipd,phone=phone)
            obj.save()
            ge.save()
            messages.add_message(request, messages.INFO, 'Order Placed Successfully')
            return render(request,"placeorder.html")
            #return render(request,"placeorder.html")
@csrf_exempt
def orders(request):
    if not request.session.get('logged_in'):
        messages.add_message(request, messages.INFO, 'Please LogIn')
        return render(request,'login.html')
    return render(request,"placeorder.html")

@csrf_exempt
def displaydonor(request):
    if not request.session.get('logged_in'):
        messages.add_message(request, messages.INFO, 'Please LogIn')
        return render(request,'login.html')
    obj=donor.objects.all()
    li=[]
    for i in obj:
        dic={
        'first':i.first,
        'last':i.last,
        'email':i.email,
        'phone':i.phone,
        'gender':i.gender,
        'dob':i.dob,
        'country':i.country,
        'state':i.state,
        'address':i.address,
        'aadhar':i.aadhar,
        'blood':i.blood,
        'quantity':i.quantity,
        }
        li.append(dic)
    abn = donor.objects.filter(blood="AB-")
    bp=donor.objects.filter(blood="B+")
    abp=donor.objects.filter(blood="AB+")
    op=donor.objects.filter(blood="O+")
    ap=donor.objects.filter(blood="A+")
    an=donor.objects.filter(blood="A-")
    bn=donor.objects.filter(blood="B-")
    on=donor.objects.filter(blood="O-")
    abn=len(abn)
    bp=len(bp)
    bn=len(bn)
    ap=len(ap)
    op=len(op)
    on=len(on)
    abp=len(abp)
    an=len(an)
    dictionary={'abp':abp,'bp':bp,'abn':abn,'bn':bn,'ap':ap,'an':an,'on':on,'op':op}
    print(dictionary)
    return render(request,"service2.html",{'lisst':li,'dictionary':dictionary})
@csrf_exempt
def displaydonor2(request):
    if not request.session.get('logged_in'):
        messages.add_message(request, messages.INFO, 'Please LogIn')
        return render(request,'login.html')
    if(request.method=="POST"):
        filt=request.POST.get("filter")
        filtname=request.POST.get("filt")
        nor=request.POST.get("nor")
        nor2=-1
        obj=donor.objects.all()
        if(nor=="all"):
            nor2=len(obj)
        else:
            nor2=int(nor)
        if(filt=="blood"):
            obj=donor.objects.filter(blood=filtname)[:nor2]
        if(filt=="name"):
            obj=donor.objects.filter(first=filtname)[:nor2]
        if(filt=="date"):
            obj=donor.objects.filter(dob=filtname)[:nor2]
        if(filt=="cid"):
            obj=donor.objects.filter(address=filtname)[:nor2]
        li=[]
        for i in obj:
            dic={
            'first':i.first,
            'last':i.last,
            'email':i.email,
            'phone':i.phone,
            'gender':i.gender,
            'dob':i.dob,
            'country':i.country,
            'state':i.state,
            'address':i.address,
            'aadhar':i.aadhar,
            'blood':i.blood,
            'quantity':i.quantity,
            }
            li.append(dic)
        abn = donor.objects.filter(blood="AB-")
        bp=donor.objects.filter(blood="B+")
        abp=donor.objects.filter(blood="AB+")
        op=donor.objects.filter(blood="O+")
        ap=donor.objects.filter(blood="A+")
        an=donor.objects.filter(blood="A-")
        bn=donor.objects.filter(blood="B-")
        on=donor.objects.filter(blood="O-")
        abn=len(abn)
        bp=len(bp)
        bn=len(bn)
        ap=len(ap)
        op=len(op)
        on=len(on)
        abp=len(abp)
        an=len(an)
        dictionary={'abp':abp,'bp':bp,'abn':abn,'bn':bn,'ap':ap,'an':an,'on':on,'op':op}
        return render(request,"service2.html",{'lisst':li,'dictionary':dictionary})
@csrf_exempt
def stockrep(request):  
    if not request.session.get('logged_in'):
        messages.add_message(request, messages.INFO, 'Please LogIn')
        return render(request,'login.html')   
    obj=bloodtype.objects.all()
    li=[]
    abn = bloodtype.objects.get(blood="AB-")
    bp=bloodtype.objects.get(blood="B+")
    abp=bloodtype.objects.get(blood="AB+")
    op=bloodtype.objects.get(blood="O+")
    ap=bloodtype.objects.get(blood="A+")
    an=bloodtype.objects.get(blood="A-")
    bn=bloodtype.objects.get(blood="B-")
    on=bloodtype.objects.get(blood="O-")
    abn=abn.quant
    abp=abp.quant
    bn=bn.quant
    bp=bp.quant
    an=an.quant
    ap=ap.quant
    on=on.quant
    op=op.quant
    dictionary={'abp':abp,'bp':bp,'abn':abn,'bn':bn,'ap':ap,'an':an,'on':on,'op':op}

    abn = bloodtype.objects.get(blood="AB-")
    bp=bloodtype.objects.get(blood="B+")
    abp=bloodtype.objects.get(blood="AB+")
    op=bloodtype.objects.get(blood="O+")
    ap=bloodtype.objects.get(blood="A+")
    an=bloodtype.objects.get(blood="A-")
    bn=bloodtype.objects.get(blood="B-")
    on=bloodtype.objects.get(blood="O-")
    abn1=abn.cost
    abp1=abp.cost
    bn1=bn.cost
    bp1=bp.cost
    an1=an.cost
    ap1=ap.cost
    on1=on.cost
    op1=op.cost
   
    dictionary1={'abp':abp1,'bp':bp1,'abn':abn1,'bn':bn1,'ap':ap1,'an':an1,'on':on1,'op':op1}
    for i in obj:
        dic={
        'blood':i.blood,
        'quant':i.quant,
        'cost':i.cost,
        }
        li.append(dic)
    return render(request,"service21.html",{'dictionary':dictionary,'lisst':li,'dictionary1':dictionary1})
@csrf_exempt
def about(request):
    return render(request,"about.html")
@csrf_exempt
def abouts(request):
    if not request.session.get('logged_in'):
        messages.add_message(request, messages.INFO, 'Please LogIn')
        return render(request,'login.html')
    return render(request,"about2.html")
@csrf_exempt
def changepass(request):
    if not request.session.get('logged_in'):
        messages.add_message(request, messages.INFO, 'Please LogIn')
        return render(request,'login.html')
    if(request.method=="POST"):
        oldp=request.POST.get("oldp")
        newp=request.POST.get("psw")
        rnewp=request.POST.get("rpsw")
        if(newp!=rnewp):
            messages.add_message(request, messages.INFO, 'Re-entered password is not the same')
            return render(request, "changepassword.html")
        global Username
        userr=yadmin.objects.get(username=Username)
        if (userr.passw==oldp):
            if(oldp==newp):
                messages.add_message(request, messages.INFO, 'New and Old Passwords cannot be same')
                return render(request, "changepassword.html")
            userr.passw=newp
            userr.save()
            messages.add_message(request, messages.INFO, 'Successfully Changed\nPlease login again')
            return render(request, "index.html")
        else:
            messages.add_message(request, messages.INFO, 'Wrong Old Password\nPlease enter correct password')
            return render(request, "changepassword.html")
    return render(request,"changepassword.html")
@csrf_exempt
def addadmin(request):
    if not request.session.get('logged_in'):
        messages.add_message(request, messages.INFO, 'Please LogIn')
        return render(request,'login.html')
    if(request.method=="POST"):
        first=request.POST.get("first")
        last = request.POST.get("last")
        usern = request.POST.get("usern")
        pass1 = request.POST.get("psw")
        pass2 = request.POST.get("pass2")
        print(pass1+" "+pass2+" "+usern+" "+last)
        obj=yadmin.objects.filter(username=usern)
        if(len(obj)!=0):
            messages.add_message(request, messages.INFO, 'Username already exists')
            return render(request,"addadmin.html")
        if(pass1!=pass2):
            messages.add_message(request,messages.INFO,'Passwords do not match')
            return render(request, "addadmin.html")
        obj=yadmin(first=first,last=last,username=usern,passw=pass1)
        obj.save()
        messages.add_message(request, messages.INFO, 'Admin Added Successfully')
        return render(request,"admintask.html")
    return render(request, "addadmin.html")
@csrf_exempt
def addstock(request):
    if not request.session.get('logged_in'):
        messages.add_message(request, messages.INFO, 'Please LogIn')
        return render(request,'login.html')
    if(request.method=="POST"):
        blood=request.POST.get("blood")
        quant=request.POST.get("quantity")
        obj=bloodtype.objects.get(blood=blood)
        obj.quant+=int(quant)
        obj.save()
        return render(request,"admintask.html")
    return render(request,"Add_stock.html")

def test_session(request):
    request.session.set_test_cookie()
    return HttpResponse("Testing session cookie")
 
 
def test_delete(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        response = HttpResponse("Cookie test passed")
    else:
        response = HttpResponse("Cookie test failed")
    return response


def save_session_data(request):
    # set new data
    request.session['id'] = 1
    request.session['name'] = 'root'
    request.session['password'] = 'rootpass'
    return HttpResponse("Session Data Saved")
 
 
def access_session_data(request):
    response = ""
    if request.session.get('id'):
        response += "Id : {0} <br>".format(request.session.get('id'))
    if request.session.get('name'):
        response += "Name : {0} <br>".format(request.session.get('name'))
    if request.session.get('password'):
        response += "Password : {0} <br>".format(request.session.get('password'))
 
    if not response:
        return HttpResponse("No session data")
    else:
        return HttpResponse(response)
 
 
def delete_session_data(request):
    try:
        del request.session['id']
        del request.session['name']
        del request.session['password']
    except KeyError:
        pass
 
    return HttpResponse("Session Data cleared")