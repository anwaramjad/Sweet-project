from tkinter import *
import mysql.connector
from tkinter import messagebox
import webbrowser
import os
import sys
import random
import math
pro=Tk()
pro.geometry('800x450+280+50')
pro.resizable(False,False)
pro.title('SWEETSHOP')
pro.iconbitmap('C:\\Users\\User\\OneDrive\\Desktop\\super.ico')
title=Label(pro,text='Sweet shop',fg='gold',bg='black',font=('tajawal',16,'bold'))
title.pack(fill=X)

u1='https://www.facbook.com/username'
u2='url-telgram'
u3='url-youtube'

class sweet:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1300x700+30+10")
        self.root.title("Sweet shop")
        self.root.resizable(FALSE,FALSE)
        self.root.iconbitmap("C:\\Users\\User\\OneDrive\\Desktop\\download.ico")
        title=Label(self.root,text="Sweet shop",fg='white',bg='#0B2F3A',font=("tajawal",15,))
        title.pack(fill=X)

        #---- var ----
        self.total=StringVar()
        self.name=StringVar()
        self.fatora=StringVar()
        x=random.randint(1000,9999)
        self.fatora.set(str(x))
        self.phone=StringVar()
        self.Purposes1 = IntVar()
        self.Purposes2 = IntVar()
        self.Purposes3 = IntVar()
        self.Purposes4 = IntVar()
        self.Purposes5 = IntVar()
        self.Purposes6 = IntVar()
        self.Purposes7 = IntVar()
        self.Purposes8 = IntVar()
        self.Purposes9 = IntVar()
        self.Purposes10 = IntVar()
        self.Purposes11 = IntVar()
        self.Purposes12 = IntVar()
        self.Purposes13 = IntVar()
        self.Purposes14 = IntVar()
        self.Purposes15 = IntVar()
        self.Purposes16 = IntVar()
        self.Purposes17 = IntVar()
        self.Purposes18 = IntVar()
        self.Purposes19 = IntVar()
        self.Purposes20 = IntVar()
        self.Purposes21 = IntVar()
        self.Purposes22 = IntVar()
        self.Purposes23 = IntVar()
        self.Purposes24 = IntVar()
        self.Purposes25 = IntVar()
        self.Purposes26 = IntVar()
        self.Purposes27 = IntVar()
        self.Purposes28 = IntVar()
        self.Purposes29 = IntVar()
        self.Purposes30 = IntVar()
        self.Purposes31 = IntVar()
        self.Purposes32 = IntVar()
        self.Purposes33 = IntVar()
        self.Purposes34 = IntVar()
        self.Purposes35 = IntVar()
        self.Purposes36 = IntVar()
        self.Purposes37 = IntVar()
        self.Purposes38 = IntVar()
        self.Purposes39 = IntVar()
        self.Purposes40 = IntVar()
        self.Purposes41 = IntVar()
        self.Purposes42 = IntVar()
        self.Purposes43 = IntVar()
        self.Purposes44 = IntVar()
        self.Purposes45 = IntVar()
        #----Customer DATA----
        f1=Frame(root,bd=2,width=338,height=260,bg='#0B4C5F')
        f1.place(x=966,y=29)

        tit=Label(f1,text=" Buyer Data ",font=("tajawal",15,'bold'),bg='#0B4C5F',fg='tomato')
        tit.place(x=95,y=0)

        his_name=Label(f1,text=' Buyers name ',font=("tajawal",12,'bold'),bg='#0B4C5F',fg='white')
        his_name.place(x=15,y=50)

        his_phone=Label(f1,text=' Buyer Number ',font=("tajawal",12,'bold'),bg='#0B4C5F',fg='white')
        his_phone.place(x=15,y=90)

        his_id=Label(f1,text=' Invoice number ',font=("tajawal",12,'bold'),bg='#0B4C5F',fg='white')
        his_id.place(x=15,y=130)

        ent_name=Entry(f1,textvariable=self.name,justify='center')
        ent_name.place(x=155,y=50)

        ent_phone=Entry(f1,textvariable=self.phone,justify='center')
        ent_phone.place(x=155,y=90)

        ent_id=Entry(f1,textvariable=self.fatora,justify='center')
        ent_id.place(x=155,y=130)

        btn_customer=Button(f1,text="research",font=("tajawal",12),width=10,height=2,bg='white')
        btn_customer.place(x=112,y=165)

        #-----bill----
        titdd=Label(f1,text='[ Invoices ]',font=("tajawal",13,'bold'),bg='#0B4C5F',fg='gold')
        titdd.place(x=114,y=225)

        f3=Frame(root,bd=2,width=338,height=399,bg='black')
        f3.place(x=966,y=290)

        scrol_y=Scrollbar(f3,orient=VERTICAL,)
        self.textarea=Text(f3,yscrollcommand=scrol_y.set)
        scrol_y.pack(side=LEFT,fill=Y)
        scrol_y.config(command=self.textarea.yview)
        self.textarea.pack(fill=BOTH,expand=1)

        #----Price----
        f4=Frame(root,bd=2,width=963,height=112,bg='#0B4C5F',)
        f4.place(x=0.2,y=587)

        hesab=Button(f4,text='Bill Calculation',width=13,height=1,font=("tajawal"),bg='#DBA901',command=self.tot)
        hesab.place(x=12,y=12)

        fatora=Button(f4,text=" Invoice Export ",width=13,height=1,font=("tajawal"),bg='#DBA901',command=self.billing)
        fatora.place(x=12,y=60)

        clear=Button(f4,text='Clear',width=13,height=1,font=("tajawal"),bg='#DBA901',command=self.clear)
        clear.place(x=155,y=12)

        exite=Button(f4,text='Exite',width=13,height=1,font=("tajawal"),bg='#DBA901',command=quit)
        exite.place(x=155,y=60)

        lblo1=Label(f4,text='Total Bill Calculation',font=("tajawal",13,'bold'),bg='#0B4C5F',fg='gold')
        lblo1.place(x=290,y=45)

        ento1=Entry(f4,textvariable=self.total,width=24,justify='center')
        ento1.place(x=459,y=48)

        #----items[1]----

        ff1=Frame(root,bd=2,width=318,height=559,bg='#0B4C5F')
        ff1.place(x=0.2,y=29)

        t=Label(ff1,text='Cold sweets',font=("tajawal",13,'bold'),bg='#0B4C5F',fg='gold')
        t.place(x=102,y=0)

        sc1=Label(ff1,text='Cheesecake',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sc1.place(x=10,y=40)

        sc2=Label(ff1,text='Brownie',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sc2.place(x=10,y=80)

        sc3=Label(ff1,text='Tiramisu',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sc3.place(x=10,y=120)

        sc4=Label(ff1,text='Pavlova',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sc4.place(x=10,y=160)

        sc5=Label(ff1,text='Macarons',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sc5.place(x=10,y=200)

        sc6=Label(ff1,text='Cupcake',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sc6.place(x=10,y=240)

        sc7=Label(ff1,text='Eclair',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sc7.place(x=10,y=280)

        sc8=Label(ff1,text='Muffin',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sc8.place(x=10,y=320)

        sc9=Label(ff1,text='Panna Cotta',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sc9.place(x=10,y=360)

        sc10=Label(ff1,text='Donuts',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sc10.place(x=10,y=400)

        sc11=Label(ff1,text='Crepes',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sc11.place(x=10,y=440)

        sc12=Label(ff1,text='Churros',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sc12.place(x=10,y=480)

        sc13=Label(ff1,text='Baklava',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sc13.place(x=10,y=520)

        sc14=Label(ff1,text='Soufflé',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sc14.place(x=10,y=560)

        sc15=Label(ff1,text='Fruit Tart',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sc15.place(x=10,y=600)

        sc_en1=Entry(ff1,width=12,textvariable=self.Purposes1,justify="center")
        sc_en1.place(x=120,y=40)

        sc_en2=Entry(ff1,width=12,textvariable=self.Purposes2,justify="center")
        sc_en2.place(x=120,y=80)

        sc_en3=Entry(ff1,width=12,textvariable=self.Purposes3,justify="center")
        sc_en3.place(x=120,y=120)

        sc_en4=Entry(ff1,width=12,textvariable=self.Purposes4,justify="center")
        sc_en4.place(x=120,y=160)

        sc_en5=Entry(ff1,width=12,textvariable=self.Purposes5,justify="center")
        sc_en5.place(x=120,y=200)

        sc_en6=Entry(ff1,width=12,textvariable=self.Purposes6,justify="center")
        sc_en6.place(x=120,y=240)

        sc_en7=Entry(ff1,width=12,textvariable=self.Purposes7,justify="center")
        sc_en7.place(x=120,y=280)

        sc_en8=Entry(ff1,width=12,textvariable=self.Purposes8,justify="center")
        sc_en8.place(x=120,y=320)

        sc_en9=Entry(ff1,width=12,textvariable=self.Purposes9,justify="center")
        sc_en9.place(x=120,y=360)

        sc_en10=Entry(ff1,width=12,textvariable=self.Purposes10,justify="center")
        sc_en10.place(x=120,y=400)

        sc_en11=Entry(ff1,width=12,textvariable=self.Purposes11,justify="center")
        sc_en11.place(x=120,y=440)

        sc_en12=Entry(ff1,width=12,textvariable=self.Purposes12,justify="center")
        sc_en12.place(x=120,y=480)

        sc_en13=Entry(ff1,width=12,textvariable=self.Purposes13,justify="center")
        sc_en13.place(x=120,y=520)

        sc_en14=Entry(ff1,width=12,textvariable=self.Purposes14,justify="center")
        sc_en14.place(x=120,y=560)

        sc_en15=Entry(ff1,width=12,textvariable=self.Purposes15,justify="center")
        sc_en15.place(x=120,y=600)

         #----items[2]----

        ff2=Frame(root,bd=2,width=318,height=559,bg='#0B4C5F')
        ff2.place(x=318,y=29)
        
        t2=Label(ff2,text='Cold Sweets',font=("tajawal",13,'bold'),bg='#0B4C5F',fg='gold')
        t2.place(x=102,y=0)

        sh1=Label(ff2,text='Soufflé',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sh1.place(x=10,y=40)

        sh2=Label(ff2,text='Apple Pie',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sh2.place(x=10,y=80)

        sh3=Label(ff2,text='Bread Pudding',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sh3.place(x=10,y=120)

        sh4=Label(ff2,text='Sticky Toffee Pudding',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sh4.place(x=10,y=160)

        sh5=Label(ff2,text='Churros',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sh5.place(x=10,y=200)

        sh6=Label(ff2,text='Crepes Suzette',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sh6.place(x=10,y=240)

        sh7=Label(ff2,text='Rice Pudding',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sh7.place(x=10,y=280)

        sh8=Label(ff2,text='Hot Brownie with Ice Cream',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sh8.place(x=10,y=320)

        sh9=Label(ff2,text='Molten Lava Cake',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sh9.place(x=10,y=360)

        sh10=Label(ff2,text='Cinnamon Rolls',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sh10.place(x=10,y=400)

        sh11=Label(ff2,text='Baked Alaska',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sh11.place(x=10,y=440)

        sh12=Label(ff2,text='Hot Fudge Sundae',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sh12.place(x=10,y=480)

        sh13=Label(ff2,text='Peach Cobbler',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sh13.place(x=10,y=520)

        sh14=Label(ff2,text='Banana Foster',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sh14.place(x=10,y=560)

        sh15=Label(ff2,text='Chip Cookie',font=("tajawal",11),bg='#0B4C5F',fg='white')
        sh15.place(x=10,y=600)

        sh_en1=Entry(ff2,width=12,textvariable=self.Purposes16,justify="center")
        sh_en1.place(x=120,y=40)

        sh_en2=Entry(ff2,width=12,textvariable=self.Purposes17,justify="center")
        sh_en2.place(x=120,y=80)

        sh_en3=Entry(ff2,width=12,textvariable=self.Purposes18,justify="center")
        sh_en3.place(x=120,y=120)

        sh_en4=Entry(ff2,width=12,textvariable=self.Purposes19,justify="center")
        sh_en4.place(x=167,y=160)

        sh_en5=Entry(ff2,width=12,textvariable=self.Purposes20,justify="center")
        sh_en5.place(x=120,y=200)

        sh_en6=Entry(ff2,width=12,textvariable=self.Purposes21,justify="center")
        sh_en6.place(x=120,y=240)

        sh_en7=Entry(ff2,width=12,textvariable=self.Purposes22,justify="center")
        sh_en7.place(x=120,y=280)

        sh_en8=Entry(ff2,width=12,textvariable=self.Purposes23,justify="center")
        sh_en8.place(x=210,y=320)

        sh_en9=Entry(ff2,width=12,textvariable=self.Purposes24,justify="center")
        sh_en9.place(x=147,y=360)

        sh_en10=Entry(ff2,width=12,textvariable=self.Purposes25,justify="center")
        sh_en10.place(x=120,y=400)

        sh_en11=Entry(ff2,width=12,textvariable=self.Purposes26,justify="center")
        sh_en11.place(x=120,y=440)

        sh_en12=Entry(ff2,width=12,textvariable=self.Purposes27,justify="center")
        sh_en12.place(x=120,y=480)

        sh_en13=Entry(ff2,width=12,textvariable=self.Purposes28,justify="center")
        sh_en13.place(x=120,y=520)

        sh_en14=Entry(ff2,width=12,textvariable=self.Purposes29,justify="center")
        sh_en14.place(x=300,y=560)

        sh_en15=Entry(ff2,width=12,textvariable=self.Purposes30,justify="center")
        sh_en15.place(x=120,y=600)


         #----items[3]----

        ff3=Frame(root,bd=2,width=330,height=559,bg='#0B4C5F')
        ff3.place(x=636,y=29)
        
        t3=Label(ff3,text='Hot and cold juices',font=("tajawal",13,'bold'),bg='#0B4C5F',fg='gold')
        t3.place(x=102,y=0)

        j1=Label(ff3,text='Orange Juice',font=("tajawal",11),bg='#0B4C5F',fg='white')
        j1.place(x=10,y=40)

        j2=Label(ff3,text='Lemon Mint Juice',font=("tajawal",11),bg='#0B4C5F',fg='white')
        j2.place(x=10,y=80)

        j3=Label(ff3,text='Watermelon Juice',font=("tajawal",11),bg='#0B4C5F',fg='white')
        j3.place(x=10,y=120)

        j4=Label(ff3,text='Pineapple Juice',font=("tajawal",11),bg='#0B4C5F',fg='white')
        j4.place(x=10,y=160)

        j5=Label(ff3,text='Pomegranate Juice',font=("tajawal",11),bg='#0B4C5F',fg='white')
        j5.place(x=10,y=200)

        j6=Label(ff3,text='Mixed Berry Juice',font=("tajawal",11),bg='#0B4C5F',fg='white')
        j6.place(x=10,y=240)

        j7=Label(ff3,text='Kiwi Juice',font=("tajawal",11),bg='#0B4C5F',fg='white')
        j7.place(x=10,y=280)

        j8=Label(ff3,text='Sahlab',font=("tajawal",11),bg='#0B4C5F',fg='white')
        j8.place(x=10,y=320)

        j9=Label(ff3,text='Tea',font=("tajawal",11),bg='#0B4C5F',fg='white')
        j9.place(x=10,y=360)

        j10=Label(ff3,text='Hot Chocolate',font=("tajawal",11),bg='#0B4C5F',fg='white')
        j10.place(x=10,y=400)

        j11=Label(ff3,text='White Hot Chocolate',font=("tajawal",11),bg='#0B4C5F',fg='white')
        j11.place(x=10,y=440)

        j12=Label(ff3,text='Mocha',font=("tajawal",11),bg='#0B4C5F',fg='white')
        j12.place(x=10,y=480)

        j13=Label(ff3,text='Latte',font=("tajawal",11),bg='#0B4C5F',fg='white')
        j13.place(x=10,y=520)

        j14=Label(ff3,text='Espresso ',font=("tajawal",11),bg='#0B4C5F',fg='white')
        j14.place(x=10,y=560)

        j15=Label(ff3,text='Cappuccino',font=("tajawal",11),bg='#0B4C5F',fg='white')
        j15.place(x=10,y=600)

        je1=Entry(ff3,width=12,textvariable=self.Purposes31,justify="center")
        je1.place(x=120,y=40)

        je2=Entry(ff3,width=12,textvariable=self.Purposes32,justify="center")
        je2.place(x=170,y=80)

        je3=Entry(ff3,width=12,textvariable=self.Purposes33,justify="center")
        je3.place(x=170,y=120)

        je4=Entry(ff3,width=12,textvariable=self.Purposes34,justify="center")
        je4.place(x=120,y=160)

        je5=Entry(ff3,width=12,textvariable=self.Purposes35,justify="center")
        je5.place(x=170,y=200)

        je6=Entry(ff3,width=12,textvariable=self.Purposes36,justify="center")
        je6.place(x=170,y=240)

        j7=Entry(ff3,width=12,textvariable=self.Purposes37,justify="center")
        j7.place(x=120,y=280)

        j8=Entry(ff3,width=12,textvariable=self.Purposes38,justify="center")
        j8.place(x=120,y=320)

        j9=Entry(ff3,width=12,textvariable=self.Purposes29,justify="center")
        j9.place(x=120,y=360)

        j10=Entry(ff3,width=12,textvariable=self.Purposes40,justify="center")
        j10.place(x=120,y=400)

        j11=Entry(ff3,width=12,textvariable=self.Purposes41,justify="center")
        j11.place(x=170,y=440)

        j12=Entry(ff3,width=12,textvariable=self.Purposes42,justify="center")
        j12.place(x=120,y=480)

        j13=Entry(ff3,width=12,textvariable=self.Purposes43,justify="center")
        j13.place(x=120,y=520)

        j14=Entry(ff3,width=12,textvariable=self.Purposes44,justify="center")
        j14.place(x=300,y=560)

        j15=Entry(ff3,width=12,textvariable=self.Purposes45,justify="center")
        j15.place(x=120,y=600)
        self.welcome()
    def tot(self):
        self.p1 = self.Purposes1.get() * 10
        self.p2 = self.Purposes2.get() * 10
        self.p3 = self.Purposes3.get() * 10
        self.p4 = self.Purposes4.get() * 10
        self.p5 = self.Purposes5.get() * 10
        self.p6 = self.Purposes6.get() * 10
        self.p7 = self.Purposes7.get() * 10
        self.p8 = self.Purposes8.get() * 10
        self.p9 = self.Purposes9.get() * 10
        self.p10 = self.Purposes10.get() * 10
        self.p11 = self.Purposes11.get() * 10
        self.p12 = self.Purposes12.get() * 10
        self.p13 = self.Purposes13.get() * 10
        self.p14 = self.Purposes14.get() * 10
        self.p15 = self.Purposes15.get() * 10
        self.p16 = self.Purposes16.get() * 10
        self.p17 = self.Purposes17.get() * 10
        self.p18 = self.Purposes18.get() * 10
        self.p19 = self.Purposes19.get() * 10
        self.p20 = self.Purposes20.get() * 10
        self.p21 = self.Purposes21.get() * 10
        self.p22 = self.Purposes22.get() * 10
        self.p23 = self.Purposes23.get() * 10
        self.p24 = self.Purposes24.get() * 10
        self.p25 = self.Purposes25.get() * 10
        self.p26 = self.Purposes26.get() * 10
        self.p27 = self.Purposes27.get() * 10
        self.p28 = self.Purposes28.get() * 10
        self.p29 = self.Purposes29.get() * 10
        self.p30 = self.Purposes30.get() * 10
        self.p31 = self.Purposes31.get() * 10
        self.p32 = self.Purposes32.get() * 10
        self.p33 = self.Purposes33.get() * 10
        self.p34 = self.Purposes34.get() * 10
        self.p35 = self.Purposes35.get() * 10
        self.p36 = self.Purposes36.get() * 10
        self.p37 = self.Purposes37.get() * 10
        self.p38 = self.Purposes38.get() * 10
        self.p39 = self.Purposes39.get() * 10
        self.p40 = self.Purposes40.get() * 10
        self.p41 = self.Purposes41.get() * 10
        self.p42 = self.Purposes42.get() * 10
        self.p43 = self.Purposes43.get() * 10
        self.p44 = self.Purposes44.get() * 10
        self.p45 = self.Purposes45.get() * 10
        if self.Purposes1.get()>=0 and self.Purposes2.get()>=0 and self.Purposes3.get()>=0 and self.Purposes4.get()>=0 and self.Purposes5.get()>=0 and self.Purposes6.get()>=0 and self.Purposes7.get()>=0 and self.Purposes8.get()>=0 and self.Purposes9.get()>=0 and self.Purposes10.get()>=0 and self.Purposes11.get()>=0 and self.Purposes12.get()>=0 and self.Purposes13.get()>=0 and self.Purposes14.get()>=0 and self.Purposes15.get()>=0 and self.Purposes16.get()>=0 and self.Purposes17.get()>=0 and self.Purposes18.get()>=0 and self.Purposes19.get()>=0 and self.Purposes20.get()>=0 and self.Purposes21.get()>=0 and self.Purposes22.get()>=0 and self.Purposes23.get()>=0 and self.Purposes24.get()>=0 and self.Purposes25.get()>=0 and self.Purposes26.get()>=0 and self.Purposes27.get()>=0 and self.Purposes28.get()>=0 and self.Purposes29.get()>=0 and self.Purposes30.get()>=0 and self.Purposes31.get()>=0 and self.Purposes32.get()>=0 and self.Purposes33.get()>=0 and self.Purposes34.get()>=0 and self.Purposes35.get()>=0 and self.Purposes36.get()>=0 and self.Purposes37.get()>=0 and self.Purposes38.get()>=0 and self.Purposes39.get()>=0 and self.Purposes40.get()>=0 and self.Purposes41.get()>=0 and self.Purposes42.get()>=0 and self.Purposes43.get()>=0 and self.Purposes44.get()>=0 and self.Purposes45.get()>=0 :

            self.total2=float(self.p1 + self.p2 + self.p3 + self.p4 + self.p5 + self.p6 + self.p7 + self.p8 + self.p9 + self.p10 +
                            self.p11 + self.p12 + self.p13 + self.p14 + self.p15 + self.p16 + self.p17 + self.p18 + self.p19 + self.p20 +
                            self.p21 + self.p22 + self.p23 + self.p24 + self.p25 + self.p26 + self.p27 + self.p28 + self.p29 + self.p30 +
                            self.p31 + self.p32 + self.p33 + self.p34 + self.p35 + self.p36 + self.p37 + self.p38 + self.p39 + self.p40 +
                            self.p41 + self.p42 + self.p43 + self.p44 + self.p45)
            self.total.set(str(self.total2)+"$")

        else:
            messagebox.showerror("false","Incorrect number")  
    
    def welcome(self):
        self.textarea.delete('1.0',END)
        self.textarea.insert(END,"        Al Noor Sweets welcomes you  ")
        self.textarea.insert(END,"\n =======================================")
        self.textarea.insert(END,f"\n  B.NUM  :{self.fatora.get()}")
        self.textarea.insert(END,f"\n  Name   :{self.name.get()}")
        self.textarea.insert(END,f"\n  phone  :{self.phone.get()}")
        self.textarea.insert(END,"\n =======================================") 
        self.textarea.insert(END,f"\n the price\t    the number\t   Purchases \t ")
        self.textarea.insert(END,"\n =======================================")
    def clear(self):

        self.total.set("")
        self.Purposes1.set(0)
        self.Purposes2.set(0)
        self.Purposes3.set(0)
        self.Purposes4.set(0)
        self.Purposes5.set(0)
        self.Purposes6.set(0)
        self.Purposes7.set(0)
        self.Purposes8.set(0)
        self.Purposes9.set(0)
        self.Purposes10.set(0)
        self.Purposes11.set(0)
        self.Purposes12.set(0)
        self.Purposes13.set(0)
        self.Purposes14.set(0)
        self.Purposes15.set(0)
        self.Purposes16.set(0)
        self.Purposes17.set(0)
        self.Purposes18.set(0)
        self.Purposes19.set(0)
        self.Purposes20.set(0)
        self.Purposes21.set(0)
        self.Purposes22.set(0)
        self.Purposes23.set(0)
        self.Purposes24.set(0)
        self.Purposes25.set(0)
        self.Purposes26.set(0)
        self.Purposes27.set(0)
        self.Purposes28.set(0)
        self.Purposes29.set(0)
        self.Purposes30.set(0)
        self.Purposes31.set(0)
        self.Purposes32.set(0)
        self.Purposes33.set(0)
        self.Purposes34.set(0)
        self.Purposes35.set(0)
        self.Purposes36.set(0)
        self.Purposes37.set(0)
        self.Purposes38.set(0)
        self.Purposes39.set(0)
        self.Purposes40.set(0)
        self.Purposes41.set(0)
        self.Purposes42.set(0)
        self.Purposes43.set(0)
        self.Purposes44.set(0)
        self.Purposes45.set(0)
    def save(self):
        op=messagebox.askyesno("save","Do you want to save the invoice?")
        if op > 0:
            self.fatora2=self.textarea.get(1.0,END)
            f1=open("C:\\Users\\User\\OneDrive\\Desktop\\فواتير"+str(self.fatora.get())+".txt","w",encoding='utf-8')
            f1.write(self.fatora2)
            f1.close()
        else:
            return
    
    def billing (self):
            if self.name.get()=="" or self.phone.get()=="":
                messagebox.showerror("error","The name or number field must not be left blank.")
            elif self.total =="0.0 $":
                messagebox.showerror("You have not purchased anything. Please select the items you would like to purchase.")
            else:
                if self.Purposes1.get()>=0 and self.Purposes2.get()>=0 and self.Purposes3.get()>=0 and self.Purposes4.get()>=0 and self.Purposes5.get()>=0 and self.Purposes6.get()>=0 and self.Purposes7.get()>=0 and self.Purposes8.get()>=0 and self.Purposes9.get()>=0 and self.Purposes10.get()>=0 and self.Purposes11.get()>=0 and self.Purposes12.get()>=0 and self.Purposes13.get()>=0 and self.Purposes14.get()>=0 and self.Purposes15.get()>=0 and self.Purposes16.get()>=0 and self.Purposes17.get()>=0 and self.Purposes18.get()>=0 and self.Purposes19.get()>=0 and self.Purposes20.get()>=0 and self.Purposes21.get()>=0 and self.Purposes22.get()>=0 and self.Purposes23.get()>=0 and self.Purposes24.get()>=0 and self.Purposes25.get()>=0 and self.Purposes26.get()>=0 and self.Purposes27.get()>=0 and self.Purposes28.get()>=0 and self.Purposes29.get()>=0 and self.Purposes30.get()>=0 and self.Purposes31.get()>=0 and self.Purposes32.get()>=0 and self.Purposes33.get()>=0 and self.Purposes34.get()>=0 and self.Purposes35.get()>=0 and self.Purposes36.get()>=0 and self.Purposes37.get()>=0 and self.Purposes38.get()>=0 and self.Purposes39.get()>=0 and self.Purposes40.get()>=0 and self.Purposes41.get()>=0 and self.Purposes42.get()>=0 and self.Purposes43.get()>=0 and self.Purposes44.get()>=0 and self.Purposes45.get()>=0 :
                    self.welcome()
                    if self.Purposes1.get()!=0:
                        self.textarea.insert(END,f"\n {self.p1}\t{self.Purposes1.get()}\tCheesecake")
                    if self.Purposes2.get()!=0:
                        self.textarea.insert(END,f"\n {self.p2}\t{self.Purposes2.get()}\tBrownie")
                    if self.Purposes3.get()!=0:
                        self.textarea.insert(END,f"\n {self.p3}\t\t{self.Purposes3.get()}\t\tTiramisu")
                    if self.Purposes4.get()!=0:
                        self.textarea.insert(END,f"\n {self.p4}\t\t{self.Purposes4.get()}\t\tPavlova")
                    if self.Purposes5.get()!=0:
                        self.textarea.insert(END,f"\n {self.p5}\t\t{self.Purposes5.get()}\t\tMacarons")
                    if self.Purposes6.get()!=0:
                        self.textarea.insert(END,f"\n {self.p6}\t\t{self.Purposes6.get()}\t\tCupcake")
                    if self.Purposes7.get()!=0:
                        self.textarea.insert(END,f"\n {self.p7}\t\t{self.Purposes7.get()}\t\tEclair")
                    if self.Purposes8.get()!=0:
                        self.textarea.insert(END,f"\n {self.p8}\t\t{self.Purposes8.get()}\t\tMuffin")
                    if self.Purposes9.get()!=0:
                        self.textarea.insert(END,f"\n {self.p9}\t\t{self.Purposes9.get()}\t\tPanna Cotta")
                    if self.Purposes10.get()!=0: 
                        self.textarea.insert(END,f"\n {self.p10}\t\t{self.Purposes10.get()}\t\tDonuts")
                    if self.Purposes11.get()!=0: 
                        self.textarea.insert(END,f"\n {self.p11}\t\t{self.Purposes11.get()}\t\tCrepes")
                    if self.Purposes12.get()!=0: 
                        self.textarea.insert(END,f"\n {self.p12}\t\t{self.Purposes12.get()}\t\tChurros")
                    if self.Purposes13.get()!=0: 
                        self.textarea.insert(END,f"\n {self.p13}\t\t{self.Purposes13.get()}\t\tBaklava")
                    if self.Purposes14.get()!=0: 
                         self.textarea.insert(END,f"\n {self.p14}\t\t{self.Purposes14.get()}\t\tSoufflé")
                    if self.Purposes15.get()!=0: 
                        self.textarea.insert(END,f"\n {self.p15}\t\t{self.Purposes15.get()}\t\tFruit Tart")
                    if self.Purposes16.get()!=0:
                        self.textarea.insert(END,f"\n {self.p16}\t\t{self.Purposes16.get()}\t\tSoufflé")
                    if self.Purposes17.get()!=0:
                        self.textarea.insert(END,f"\n {self.p17}\t\t{self.Purposes17.get()}\t\tApple Pie")
                    if self.Purposes18.get()!=0:
                        self.textarea.insert(END,f"\n {self.p18}\t\t{self.Purposes18.get()}\t\tBread Pudding")
                    if self.Purposes19.get()!=0:
                        self.textarea.insert(END,f"\n {self.p19}\t\t{self.Purposes19.get()}\t\tSticky Toffee Pudding")
                    if self.Purposes20.get()!=0:
                        self.textarea.insert(END,f"\n {self.p20}\t\t{self.Purposes20.get()}\t\tChurros")
                    if self.Purposes21.get()!=0:
                        self.textarea.insert(END,f"\n {self.p21}\t\t{self.Purposes21.get()}\t\tCrepes Suzette")
                    if self.Purposes22.get()!=0:
                        self.textarea.insert(END,f"\n {self.p22}\t\t{self.Purposes22.get()}\t\tRice Pudding")
                    if self.Purposes23.get()!=0:
                        self.textarea.insert(END,f"\n {self.p23}\t\t{self.Purposes23.get()}\t\tHot Brownie with Ice Cream")
                    if self.Purposes24.get()!=0:
                        self.textarea.insert(END,f"\n {self.p24}\t\t{self.Purposes24.get()}\t\tMolten Lava Cake")
                    if self.Purposes25.get()!=0:
                        self.textarea.insert(END,f"\n {self.p25}\t\t{self.Purposes25.get()}\t\tCinnamon Rolls")
                    if self.Purposes26.get()!=0:
                        self.textarea.insert(END,f"\n {self.p26}\t\t{self.Purposes26.get()}\t\tBaked Alaska")
                    if self.Purposes27.get()!=0:
                        self.textarea.insert(END,f"\n {self.p27}\t{self.Purposes27.get()}\tHot Fudge Sundae")
                    if self.Purposes28.get()!=0:
                        self.textarea.insert(END,f"\n {self.p28}\t{self.Purposes28.get()}\tPeach Cobbler")
                    if self.Purposes29.get()!=0:
                        self.textarea.insert(END,f"\n {self.p29}\t\t{self.Purposes29.get()}\t\tBanana Foster")
                    if self.Purposes30.get()!=0:
                        self.textarea.insert(END,f"\n {self.p30}\t\t{self.Purposes30.get()}\t\tChip Cookie")
                    if self.Purposes31.get()!=0:
                        self.textarea.insert(END,f"\n {self.p31}\t\t{self.Purposes31.get()}\t\tOrange Juice")
                    if self.Purposes32.get()!=0:
                        self.textarea.insert(END,f"\n {self.p32}\t\t{self.Purposes32.get()}\t\tLemon Mint Juice")
                    if self.Purposes33.get()!=0:
                        self.textarea.insert(END,f"\n {self.p33}\t\t{self.Purposes33.get()}\t\tWatermelon Juice")
                    if self.Purposes34.get()!=0:
                        self.textarea.insert(END,f"\n {self.p34}\t\t{self.Purposes34.get()}\t\tPineapple Juice")
                    if self.Purposes34.get()!=0:
                        self.textarea.insert(END,f"\n {self.p34}\t\t{self.Purposes34.get()}\t\tPomegranate Juice")
                    if self.Purposes35.get()!=0:
                        self.textarea.insert(END,f"\n {self.p35}\t\t{self.Purposes35.get()}\t\tMixed Berry Juice")
                    if self.Purposes36.get()!=0:
                        self.textarea.insert(END,f"\n {self.p36}\t\t{self.Purposes36.get()}\t\tKiwi Juice")
                    if self.Purposes37.get()!=0:
                        self.textarea.insert(END,f"\n {self.p37}\t\t{self.Purposes37.get()}\t\tSahlab")
                    if self.Purposes38.get()!=0:
                        self.textarea.insert(END,f"\n {self.p38}\t\t{self.Purposes38.grt()}\t\tTea")
                    if self.Purposes39.get()!=0:
                        self.textarea.insert(END,f"\n {self.p39}\t\t{self.Purposes39.get()}\t\tHot Chocolate")
                    if self.Purposes40.get()!=0:
                        self.textarea.insert(END,f"\n {self.p40}\t\t{self.Purposes40.get()}\t\tWhite Hot Chocolate")
                    if self.Purposes41.get()!=0:
                        self.textarea.insert(END,f"\n {self.p41}\t\t{self.Purposes41.get()}\t\tMocha")
                    if self.Purposes42.get()!=0:
                        self.textarea.insert(END,f"\n {self.p42}\t\t{self.Purposes42.get()}\t\tLatte")
                    if self.Purposes43.get()!=0:
                        self.textarea.insert(END,f"\n {self.p43}\t\t{self.Purposes43.get()}\t\tEspresso")
                    if self.Purposes44.get()!=0:
                        self.textarea.insert(END,f"\n {self.p44}\t\t{self.Purposes44.get()}\t\tCappuccino")
                    if self.Purposes45.get()!=0:
                        self.textarea.insert(END,f"\n {self.p45}\t\t{self.Purposes45.get()}\t\tTiramisu")
                    self.textarea.insert(END,"\n =======================================")
                    self.textarea.insert(END,f"the total :\t\t{self.total.get()}$  ")
                    self.textarea.insert(END,"\n =======================================")
                    self.save()
                else:
                     messagebox.showerror("false","Incorrect number")  
                        

def open1():
    webbrowser.open_new(u1)

def open2():
    webbrowser.open_new(u2)

def open3():
    webbrowser.open_new(u3)

def about1():
    messagebox.showinfo("About the developer"," Developer Anwar Zidane ")

def about2():
     messagebox.showinfo(" About the program "," A project about a sweets shop that specializes in selling the most delicious and finest types of sweets ")

def log():
    user=en1.get()
    passw=en2.get()
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root", 
            password="",  
            database="user"  
        )
        cursor = conn.cursor()
        
       
        query = "SELECT * FROM users WHERE user_name = %s AND password = %s"
        cursor.execute(query, (user, passw))
        result = cursor.fetchone()
        if result:
            ob=sweet(pro)
        else:
            messagebox.showerror("false","Incorrect password or username")  
    except mysql.connector.Error as err:
        messagebox.showerror("خطأ في الاتصال", f"حدث خطأ: {err}")

def create():
    def connect_database():
        try:
            conn = mysql.connector.connect(
                host="localhost",     # عنوان السيرفر (في حال كنت تعمل على جهازك استخدم localhost)
                user="root",          # اسم المستخدم (تأكد من تغييره إذا كنت تستخدم اسم مستخدم آخر)
                password="",          # كلمة المرور (إذا كنت تستخدم كلمة مرور أدخلها هنا، إذا لا فاتركها فارغة)
                database="user"       # اسم قاعدة البيانات التي أنشأتها
            )
            return conn
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
            return None

    def check_fields():
        user = en1.get()
        phone = en2.get()
        password = en3.get()

        if not user or not phone or not password:
            messagebox.showwarning("Warning", "Please fill in all fields")
        else:
            # الاتصال بقاعدة البيانات
            conn = connect_database()
            if conn:
                store_data(conn, user, phone, password)
                messagebox.showinfo("Success", "Data saved successfully!")
                conn.close()
                var.quit()  # إغلاق النافذة تلقائيًا
    
    def store_data(conn, user, phone, password):
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (user_name, phone, password) VALUES (%s, %s, %s)", (user, phone, password))
            conn.commit()
            cursor.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to insert data: {e}")
    
    var=Tk()
    var.title('LOGIN SYSTEM')
    var.geometry('500x500')
    var.resizable(FALSE,FALSE)
    var.config(bg='#D5DBDB')
    var.iconbitmap("C:\\Users\\User\\OneDrive\\Desktop\\GUI PROJECT\\aaa.ico")
    #--------title--------- 
    title=Label(pro,text='LOGIN SYSTEM',font=('Consolas',15),bg='black',fg='white')
    title.pack(fill=X)
    #----------frame--------
    fr1=Frame(var,width=300,height=350,bg='whitesmoke')
    fr1.pack(pady=30)
    #---------LABEL-------
    label1=Label(fr1,text='USER NAME :',font=('Consolas',15),bg='whitesmoke')
    label1.place(x=10,y=140)
    label2=Label(fr1,text='phone :',font=('Consolas',15),bg='whitesmoke')
    label2.place(x=10,y=180)
    label3=Label(fr1,text='PASSWORD :',font=('Consolas',15),bg='whitesmoke')
    label3.place(x=10,y=210)
    #-------Entry----
    en1=Entry(fr1,bg='#bdc3c7')
    en1.place(x=134,y=145)
    en2=Entry(fr1,bg='#bdc3c7')
    en2.place(x=134,y=185)
    en3=Entry(fr1,bg='#bdc3c7')
    en3.place(x=134,y=225)
    #--------Button---------
    bt2=Button(fr1,text='SIGNIN',font=('Consolas',15),bg='#CD6155',width='11',command=check_fields)
    bt2.place(x=88,y=260)
    #------checkbox----------
    pw=Label(fr1,text='Devloped by ANWAR ZIDAN 2025',font=('Consolas',9),bg='whitesmoke')
    pw.place(x=35,y=330)



f1=Frame(pro,width=230,height=420,bg='#0B2F3A')
f1.place(x=570,y=30)

Title1=Label(f1,text="Project Sweet shop",bg='#0B2F3A',fg='white',font=('tajawal',12,'bold'))
Title1.place(x=43,y=10)
Title2=Label(f1,text='developer Anwar Zidan',bg='#0B2F3A',fg='white',font=('tajawal',12,'bold'))
Title2.place(x=32,y=42)
Title3=Label(f1,text='Contact us',bg='#0B2F3A',fg='white',font=('tajawal',12,'bold'))
Title3.place(x=67,y=74)

b1=Button(f1,text=' Our Facebook account ',width=26,fg='white',bg='#DBA901',font=('tajawal',11,'bold'),command=open1)
b1.place(x=-1,y=130)
b2=Button(f1,text=' Our Telgram account ',width=26,fg='white',bg='#DBA901',font=('tajawal',11,'bold'),command=open2)
b2.place(x=-1,y=170)
b3=Button(f1,text=' Our Instgram account ',width=26,fg='white',bg='#DBA901',font=('tajawal',11,'bold'),command=open3)
b3.place(x=-1,y=210)
b4=Button(f1,text=' About the developer ',width=26,fg='white',bg='#DBA901',font=('tajawal',11,'bold'),command=about1)
b4.place(x=-1,y=250)
b5=Button(f1,text=' Project Overview ',width=26,fg='white',bg='#DBA901',font=('tajawal',11,'bold'),command=about2)
b5.place(x=-1,y=290)
b6=Button(f1,text=' Create a user account ',width=26,fg='white',bg='#DBA901',font=('tajawal',11,'bold'),command=create)
b6.place(x=-1,y=330)
b7=Button(f1,text=' Close the program ',width=26,fg='white',bg='#DBA901',font=('tajawal',11,'bold'),command=quit)
b7.place(x=-1,y=370)

photo=PhotoImage(file="C:\\Users\\User\\OneDrive\\Desktop\\images.png")
imo=Label(pro,image=photo)
imo.place(x=120,y=43)

f2=Frame(pro,width=570,height=120,bg='#0B2F3A')
f2.place(x=0,y=330)

photo1=PhotoImage(file="C:\\Users\\User\\OneDrive\\Desktop\\download (1).png")
imo1=Label(pro,image=photo1)
imo1.place(x=450,y=350,width=90,height=90)
l1=Label(f2,text='user name',fg='gold',bg='#0B2F3A',font=('tajawal',12,'bold'))
l1.place(x=25,y=25)
l2=Label(f2,text='password',fg='gold',bg='#0B2F3A',font=('tajawal',12,'bold'))
l2.place(x=25,y=70)
l3=Label(f2,text="Create a user account",fg='gold',bg='#0B2F3A',font=('tajawal',15,'bold'))
l3.place(x=25,y=180)

en1=Entry(f2,font=('tajawal',12),justify='center')
en1.place(x=122,y=25)
en2=Entry(f2,font=('tajawal',12,),justify='center')
en2.place(x=122,y=70)

b=Button(f2,text='Login',bg='#DBA901',font=('tajawal',12,),width=12,height=3,command=log)
b.place(x=320,y=20)

pro.mainloop()
