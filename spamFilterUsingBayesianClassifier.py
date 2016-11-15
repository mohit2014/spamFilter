import glob
import json
import tkinter
from tkinter import *
from tkinter.filedialog import askdirectory
top = tkinter.Tk(className="spamFilter")
filename=""
paths={}
output=open("output.txt","w")
def getf(text,i):
    text.delete('1.0', END)
    filename=askdirectory()
    if i==1:
        path=filename+"/*.txt"
        paths['path1']=path
    
    elif i==2:
        path=filename+"/*.txt"
        paths['path2']=path
    elif i==3:
        path=filename+"/*.txt"
        paths['path3']=path
    elif i==4:
        path=filename+"/*.txt"
        paths['path4']=path
    text.insert(INSERT,filename)
def mk_dict(file):
    dict_doc={}
    try:
        text=open(file,'r',encoding='utf-8').read()
    except UnicodeDecodeError:
        text=open(file,'r',encoding='latin-1').read()
    text=text.lower()
    text=text.split()
    for word in text:
        if not(word in dict_doc):
             dict_doc[word]=1  
    return dict_doc
def classify(text):
    path = paths['path1']
    files = glob.glob(path)
    dict_spam={}
    dict_glob={}
    i=0
    for file in files:
        i=i+1
        dict_doc = mk_dict(file)
        for key in dict_doc:
            if key in dict_spam:
                dict_spam[key]=dict_spam[key]+1
            else:
                dict_spam[key]=1
            if key in dict_glob:
                dict_glob[key]=dict_glob[key]+1
            else:
                dict_glob[key]=1
    spamfiles=i
    path=paths['path2']
    files = glob.glob(path)
    dict_ham={}
    i=0
    for file in files:
        i=i+1
        dict_doc = mk_dict(file)
        for key in dict_doc:
            if key in dict_ham:
                dict_ham[key]=dict_ham[key]+1
            else:
                dict_ham[key]=1
            if key in dict_glob:
                dict_glob[key]=dict_glob[key]+1
            else:
                dict_glob[key]=1
    hamfiles=i
    total=0
    stop_words={}
    for key in dict_glob:
        if(dict_glob[key]>=(spamfiles+hamfiles)/2):
            total=total+1
            stop_words[key]=dict_glob[key]
    path = paths['path3']
    output.write("spam test starts\n")
    files = glob.glob(path)
    correct_spam=0
    total=0
    for file in files:
        output.write(file)     
        total=total+1
        p_s=1.0
        p_h=1.0
        dict_doc = mk_dict(file)
        p3=0.5
        p5=0.5
        for key in dict_doc:
            if(key not in stop_words):
                if(key in dict_spam or key in dict_ham):
                    if (key in dict_spam):
                        p2=(float(dict_spam[key])/spamfiles)
                    else:
                        p2=1/spamfiles
                    if (key in dict_ham):
                        p4=(float(dict_ham[key])/hamfiles)
                    else:
                        p4=1/hamfiles
                else:
                    p2=0.5
                    p4=0.5
                p1=(p2*p3)/(p2*p3+p4*p5)
                p6=(p4*p5)/(p2*p3+p4*p5)
                p_s=p_s*p1
                p_h=p_h*p6
        
        if p_s>p_h:
            correct_spam=correct_spam+1
            output.write(" 0\n")
        else:
            output.write(" 1\n")
    print("total spam=%d"%total)
    print("false positive=%d"%correct_spam)
    path = paths['path4']
    output.write("Ham test starts\n")
    files = glob.glob(path)
    correct_ham=0
    for file in files:
        output.write(file)
        total=total+1
        p_s=1.0
        p_h=1.0
        dict_doc = mk_dict(file)
        for key in dict_doc:
            if(key not in stop_words):
                if(key in dict_spam or key in dict_ham):
                    if (key in dict_spam):
                        p2=(float(dict_spam[key])/spamfiles)
                    else:
                        p2=1/spamfiles
                    if (key in dict_ham):
                        p4=(float(dict_ham[key])/hamfiles)
                    else:
                        p4=1/hamfiles
                else:
                    p2=0.5
                    p4=0.5
                p1=(p2*p3)/(p2*p3+p4*p5)
                p6=(p4*p5)/(p2*p3+p4*p5)
                p_s=p_s*p1
                p_h=p_h*p6
        if p_h>p_s:
            correct_ham=correct_ham+1
            output.write(" 1\n")
        else:
            output.write(" 0\n")
    print("total=%d"%total)
    print("true positive=%d"%correct_ham)
    accuracy=((float(correct_spam+correct_ham))/total)*100
    print("acc=%f"%accuracy)
    text.delete('1.0', END)
    acc=str(accuracy)
    text.insert(INSERT,"accuracy=")
    text.insert(INSERT,accuracy)
text=Text(top,height=1)
text.pack()
w=Button(top,text="Select folder of your Spam train data",command=lambda:getf(text,i=1))
w.pack()
text2=Text(top,height=1)
text2.pack()
w2=Button(top,text="Select folder of your Ham train data",command=lambda: getf(text2,i=2))
w2.pack()
text3=Text(top,height=1)
text3.pack()
w3=Button(top,text="Select folder of your Spam test data",command=lambda: getf(text3,i=3))
w3.pack()
text4=Text(top,height=1)
text4.pack()
w4=Button(top,text="Select folder of your Ham train data",command=lambda: getf(text4,i=4))
w4.pack()
text5=Text(top,height=1)
text5.pack()
w5=Button(top,text="classify",command=lambda:classify(text5))
w5.pack()
top.mainloop()
