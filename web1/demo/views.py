from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import RegisterForm
from .models import Customer,order,p_order


# Create your views here.
def index(request):
    return render(request,"home.html")
def about(request):
    return render(request,"about.html")
def logout_view(request):
    logout(request)
    return render(request,"home.html")
def use(request):
    form = RegisterForm()

    if request.method =='POST':
        form = RegisterForm(request.POST)
        un=request.POST['Name']
        em=request.POST['Mail']
        pn=request.POST['Phnno']
        wk=request.POST.get('worker',False)
        wrk=request.POST['work']
        uid=request.POST['user_ID']
        pw=request.POST['password']
        print(wk)
        if Customer.objects.filter(user_ID=uid).exists():
            messages.info(request,"user id already taken")
            return redirect('/user')
        elif len(pw)<=6:
            messages.info(request,"password must be greater than 6")
            return redirect('/user')
        elif len(pn)!=10 and len(pn)!=11:
            messages.info(request,"please enter valid phone number")
            return redirect('/user')
        elif len(em)<=7 and "@" not in em and em[-4:0:-1]!=".com":
            messages.info(request,"enter valid email")
            return redirect('/user')
        else:
            if form.is_valid():
                form.save()
            u=User.objects.create_user(uid,em,pw)
            u.save()

        return render(request,"home.html")
    context = {'form':form}
    return render(request,"user.html",context)
def wor(request):
    if request.method =='POST':
        print("after login")
        uid=request.POST['user_ID']
        ps=request.POST['password']
        user = authenticate(username=uid,password=ps)
        """rq=Customer.objects.all()
        for zx in rq:
            if zx.user_ID==uid and zx.password==ps:
                cuid=uid
                return render(request,"aflogin.html")"""
        if user is not None:
            login(request,user)
            return redirect('/login')
        else:
            messages.info(request,"enter valid details")
            return render(request,"work.html")
        #return render(request,"aflogin.html")
    else:
        return render(request,"work.html")
def aflogin(request):
    print(request.user)
    return render(request,"aflogin.html")
def detail(request):
    query_result=Customer.objects.filter(worker=True)
    print(request.user)
    context={'query_result':query_result}
    return render(request,"detail.html",context)
def book(request):
    if request.method=="POST":
        uid=request.POST['user_ID']
        wk=request.POST['work']
        dt=request.POST['date']
        t=request.POST['time']
        ob=p_order()
        ob.user=request.user
        ob.work=wk
        ob.worker=uid
        ob.date=dt
        ob.slot=t
        ob.part="sample"
        ob.save()
        za=0
        zx=Customer.objects.all()
        for ot in zx:
            if ot.user_ID==uid:
                za+=1
        print(zx)
        if za!=0:
            zs=0
            q=order.objects.all()
            for ot in q:
                #print(ot.work,ot.worker,ot.date,ot.slot)
                #print(wk,uid,dt,t)
                #print(len(str(dt)),len(str(ot.date)))
                if ot.work==wk and ot.worker==uid and str(ot.date)==str(dt) and ot.slot==t:
                    print("avinash")
                    zs=1 
            if zs==1:
                messages.info(request,"please try another slot.this slot is already booked")
                print(p_order.objects.all().filter(user=request.user,worker=uid,work=wk,date=dt,slot=t))
                p_order.objects.all().filter(user=request.user,worker=uid,work=wk,date=dt,slot=t).delete()
                return render(request,"book.html")
            else:
                q=p_order.objects.all()
                zx=0
                print(p_order.objects.all().filter(user=request.user,worker=uid,work=wk,date=dt,slot=t))
                for ot in q:
                    if ot.user!=request.user and ot.work==wk and ot.worker==uid and ot.date==dt and ot.slot==t:
                        zx+=1
                if zx==0:
                    ob.delete()
                    print(q)
                    messages.info(request,"your slot is booked")
                    sl=order(worker=uid,work=wk,user=request.user,date=dt,slot=t)
                    sl.save()
                    return render(request,"book.html")
                else:
                    ob.delete()
                    messages.info(request,"please try after few seconds")
                    return render(request,"book.html")
        else:
            ob.delete()
            messages.info(request,"please enter a valid user-ID")
            return render(request,"book.html")
    else:
        return render(request,"book.html")