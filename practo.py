class Person(object):
    def __init__(self):
        self.calendar = Calendar()

    def is_available(self, slot):
        return self.calendar.is_available(slot)

    def make_appointment(self, slot, record):
        self.calendar.add_entry(slot, record)
        
    def remove_appointment(self,slot,record):
        self.calendar.remove_entry(slot,record)

    def get_public_record(self):
        return {
            'name': self.full_name,
            'booking_class': self.__class__.__name__
        }
    def login(self, username, password):
        check=0
        #self.username = input("Enter username: ")
        #self.password = input("Enter password: ")
        with open("register.txt", "r") as file:
            for line in file:
                #print(line)
                line=line.split()
                _,uname=line[0].split(":")
                _,passw=line[1].split(":")
                #_,speciality=line[3].split(":")
                #print(uname,passw)
                if username == uname and password == passw:
                    print("login successful!")
                    check=1
                    self.full_name=username
        #print(check)
        return check
                
    


class Patient(Person):
    def __init__(self):
        super(Patient, self).__init__()
        #self.ssn = ssn
        #self.patient_id = self.first_name[:1] + self.last_name + ssn
        
    def register(self, username, password,pass_check, email,age):
        self.username = username
        self.password = password
        self.pass_check = pass_check
        self.email = email
        self.age=age

        if password == pass_check:
            print("Password match, you are logging in")
            with open("register.txt", "a") as file:
                file.write('Username:'+username+' '+'Password:'+
                           password+' '+'email:'+email+' '+'Age:'+str(age)+'\n')
                return 1
        else:
            print("passwords don't match")
            return 0


class Doctor(Person):
    def __init__(self,username,speciality):
        super(Doctor, self).__init__()
        #super(Doctor,self).login(username,password)
        self.speciality = speciality
        self.full_name=username
    def login(self, username, password):
        check=0
        #self.username = input("Enter username: ")
        #self.password = input("Enter password: ")
        with open("register1.txt", "r") as file:
            for line in file:
                #print(line)
                line=line.split()
                _,uname=line[0].split(":")
                _,passw=line[1].split(":")
                _,speciality=line[3].split(":")
                #print(uname,passw)
                if username == uname and password == passw:
                    print("login successful!")
                    self.full_name=username
                    self.speciality=speciality
                    check=1
        return check
    def get_public_record(self):
        record = super(Doctor, self).get_public_record()
        record['specialty'] = self.speciality
        return record
    def available_slots(self):
        a_slots=[]
        for slot in SLOTS:
            if self.is_available(slot):
                a_slots.append(slot)
        return a_slots
            
        
		
class Calendar(object):
    def __init__(self):
        self.entries = {}

    def is_available(self, slot):
        return slot not in self.entries

    def add_entry(self, slot, record):
        if not self.is_available(slot):
            raise DoubleBookingException
        self.entries[slot] = record
        #print(self.entries)
    
    def remove_entry(self,slot,record):
        if self.is_available(slot):
            try:
                del self.entries[slot]
            except:
                pass

    def __str__(self):
        return str(self.entries)


class DoubleBookingException(Exception):
    pass		
		
def schedule(doctor, patient, slot):
    if not doctor.is_available(slot):
        print('Cannot schedule, doctor is not available:', doctor)
        return
    if not patient.is_available(slot):
        print('Cannot schedule, patient is not available:', patient)
        return

    doctor.make_appointment(slot, patient.get_public_record())
    patient.make_appointment(slot, doctor.get_public_record())
    
import re
import smtplib
from socket import *
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
server='localhost'
server_port=2000
SLOTS=['8:00AM','8:30AM','9:00AM','9:30AM','10:00AM','10:30AM','11:00AM','11:30AM','1:00PM','1:30PM','2:00PM','2:30PM','3:00PM','3:30PM','4:00PM']
print()
print("------Welcome to Online Consultation-------")
print()
while(1):
    print("Are you:")
    print("1.Doctor")
    print("2.Patient")
    print("3.To Quit")
    choice=int(input())
    if choice==3:
        break
    if choice==2:
        while(1):
            P1=Patient()
            Doctors={}
            with open("register1.txt","r") as file:
                for line in file:
                    line=line.split()
                    _,doctor=line[0].split(":")
                    _,speciality=line[3].split(":")
                    doctor11=doctor+speciality
                    Doctors[doctor11]=Doctor(doctor,speciality)
            #print(Doctors)
            print("Did you already Register?")
            print("1.Yes")
            print("2.No")
            print("3.Go back")
            choice1=int(input())
            if choice1==3:
                break
            if choice1==1:
                while(1):
                    uname=input("Enter Your Username:")
                    passw=input("Enter Your Password:")
                    check=P1.login(uname,passw)
                    #print(check)
                    if check==0:
                        print("Invalid")
                    else:
                        break
            if choice1==2:
                while(1):
                    uname=input("Enter Your Name: ")
                    age=int(input("Enter Your Age: "))
                    email=input("Enter Your e-mail-id: ")
                    passw=input("Enter Your Password: ")
                    passw1=input("Re-enter Your Password: ")
                    check=P1.register(uname,passw,passw1,email,age)
                    if check==0:
                        print("Invalid")
                    else:
                        check=P1.login(uname,passw)
                        break
            
            while(1):
                print()
                print("Select a service you need:")
                print("1.Make an appointment")
                print("2.Modify an appointment")
                print("3.Cancel an appointment")
                print("4.View all appointments")
                print("5.Chat with our officials")
                print("6.Go back")
                choice2=int(input())
                if choice2==1:
                    print("Select Doctor for appointment:")
                    print()
                    count=1
                    with open("register1.txt", "r") as file:
                        print("Doctor\t\tSpeciality")
                        print("-----------------------")
                        for line in file:
                            line=line.split()
                            _,doctor=line[0].split(":")
                            _,speciality=line[3].split(":")
                            print(doctor+'\t\t'+speciality) 
                    print("Please enter the doctor name for your appointment")
                    doctor=input()
                    filled_slots=[]
                    #print(filled_slots)
                    with open("appointments.txt","r") as file:
                        for line in file:
                            #print(line)
                            line=line.split()
                            _,doc=line[1].split(":")
                            _,slo=line[2].split(":",1)
                            if doc==doctor:
                                filled_slots.append(slo)
                    
                    avail_slots=[i for i in SLOTS if i not in filled_slots]
                    #print(avail_slots)
                    with open("register1.txt", "r") as file:
                        for line in file:
                            line=line.split()
                            _,uname=line[0].split(":")
                            #_,passw=line[1].split(":")
                            _,speciality=line[3].split(":")
                            if uname==doctor:
                                print("Pick a time slot:")
                                print()
                                D1=Doctors[uname+speciality]
                                #avail_slots=D1.available_slots()
                                for i in avail_slots:
                                    print(i)
                                print()
                                while(1):
                                    slot=input()
                                    if slot not in avail_slots:
                                        print("Please enter correct Slot\n")
                                    else:
                                        break
                                schedule(D1,P1,slot)
                                with open("appointments.txt","a") as file:
                                    file.write("Patient:"+P1.full_name+' '+"Doctor:"+D1.full_name+' '+"Slot:"+slot+"\n")
                                message="Greetings\n\n This is Confirmation of your Appointment.\n Your appointment is scheduled as follows\n\n\nDoctor:"+D1.full_name+' Patient:'+P1.full_name+' Slot:'+slot
                                print("Appointment Successfull!")
                                print("Do you want to receive Email confirmation?")
                                print("1.Yes")
                                print("2.No")
                                mail=int(input())
                                if mail==1:
                                    id=input("Enter mail-id to receive confirmation: ")
                                    if re.search(regex,id):
                                        s = smtplib.SMTP('smtp.gmail.com', 587)
                                        s.starttls()
                                        s.login("sender-mail-id","sender-password")
                                        s.sendmail("pavankumardesai39@gmail.com", id, message)
                                        s.quit()
                                    else:
                                        print("Invalid Email-id")
                                    
                                #print(D1.calendar)
                                #print(P1.calendar)
                if choice2==2:
                    print("Select the appointment you wish to modify:")
                    print()
                    slots=[]
                    print("Patient\t\tDoctor\t\tSlot\t\t")
                    print("----------------------------------------------------------------")
                    with open("appointments.txt","r") as file:
                        for line in file:
                            #print(line)
                            line=line.split()
                            _,patient=line[0].split(":")
                            _,doctor=line[1].split(":")
                            _,slot=line[2].split(":",1)
                            if patient==P1.full_name:
                                Dct=doctor
                                slt=slot
                                patient22=patient
                                print(patient22+'\t\t'+Dct+'\t\t'+slt)
                        file.seek(0)
                        for line in file:
                            line=line.split()
                            _,doctor=line[1].split(":")
                            _,slot=line[2].split(":",1)
                            if doctor==Dct:
                                slots.append(slot)
                                
                    print()
                    avail_slots=[]
                    print("Select from available_slots:")
                    for slot in SLOTS:
                        if slot not in slots:
                            avail_slots.append(slot)
                    for i in avail_slots:
                        print(i)
                    print()
                    while(1):
                        slot=input("Enter the new slot: ")
                        if slot not in avail_slots:
                            print("Please enter correct Slot\n")
                        else:
                            break
                    
                    with open("register1.txt") as file:
                        for line in file:
                            line=line.split()
                            _,doctor=line[0].split(":")
                            if doctor==Dct:
                                _,speciality=line[3].split(":")
                    D2=Doctors[Dct+speciality]
                    D2.remove_appointment(slt,P1.get_public_record())
                    D2.make_appointment(slot,P1.get_public_record())
                    P1.remove_appointment(slt,D2.get_public_record())
                    P1.make_appointment(slot,D2.get_public_record())
                    
                    with open("appointments.txt","r") as file:
                        lines=file.readlines()
                    with open("appointments.txt","w") as file:
                        for line in lines:
                            line1=line.split()
                            _,patient1=line1[0].split(":")
                            _,doctor1=line1[1].split(":")
                            if patient1==patient22 and doctor1==Dct:
                                file.write("Patient:"+patient1+' '+"Doctor:"+Dct+' '+"Slot:"+slot+"\n")
                            else:
                                file.write(line)
                        print("Appointment modified Successfully!")
                        message="Greetings\n\n This is Confirmation of your Appointment.\n Your appointment is modified as follows\n\n\nDoctor:"+D2.full_name+' Patient:'+P1.full_name+' Slot:'+slot                                
                        print("Do you want to receive Email confirmation?")
                        print("1.Yes")
                        print("2.No")
                        mail=int(input())
                        if mail==1:
                            id=input("Enter mail-id to receive confirmation: ")
                            if re.search(regex,id):
                                s = smtplib.SMTP('smtp.gmail.com', 587)
                                s.starttls()
                                s.login("sender-mail-id","sender-password")
                                s.sendmail("pavankumardesai39@gmail.com", id, message)
                                s.quit()
                            else:
                                print("Invalid Email-id")
                if choice2==3:
                    print("Select the appointment you wish to cancel:")
                    print()
                    slots=[]
                    print("Patient\t\t"+"Doctor\t\t"+"Slot\t\t")
                    print("-------------------------------------------------------------")
                    with open("appointments.txt","r") as file:
                        for line in file:
                            #print(line)
                            line=line.split()
                            _,patient=line[0].split(":")
                            _,doctor=line[1].split(":")
                            _,slot=line[2].split(":",1)
                            if patient==P1.full_name:
                                Dct=doctor
                                slt=slot
                                print(patient+'\t\t'+doctor+'\t\t'+slot)
                        file.seek(0)
                        for line in file:
                            line=line.split()
                            _,doctor=line[1].split(":")
                            _,slot=line[2].split(":",1)
                            if doctor==Dct:
                                slots.append(slot)
                                
                    '''
                    print()
                    print("Select from available_slots:")
                    for slot in SLOTS:
                        if slot not in slots:
                            print(slot)
                    print()
                    '''
                    Dct=input("Enter the doctor  with which you wish to cancel appointment: ")
                    with open("appointments.txt","r") as file:
                        lines=file.readlines()
                    with open("appointments.txt","w") as file:
                        for line in lines:
                            line1=line.split()
                            _,patient1=line1[0].split(":")
                            _,doctor1=line1[1].split(":")
                            _,slot=line1[2].split(":",1)
                            if patient1==patient and doctor1==Dct:
                                slt=slot
                                pass
                            else:
                                file.write(line)
                    with open("register1.txt") as file:
                        for line in file:
                            line=line.split()
                            _,doctor=line[0].split(":")
                            if doctor==Dct:
                                _,speciality=line[3].split(":")
                    D2=Doctors[Dct+speciality]
                    P1.remove_appointment(slt,D2)
                    D2.remove_appointment(slt,P1)
                    print("Appointment cancelled Successfully!")            
                if choice2==4:
                    print("Patient\t\t"+"Doctor\t\t"+"Slot\t\t")
                    print("-------------------------------------------------------------")
                    with open("appointments.txt","r") as file:
                        for line in file:
                            #print(line)
                            line=line.split()
                            _,patient=line[0].split(":")
                            _,doctor=line[1].split(":")
                            _,slot=line[2].split(":",1)
                            if patient==P1.full_name:
                                Dct=doctor
                                print(patient+'\t\t'+doctor+'\t\t'+slot)
                                
                if choice2==5:
                    client_socket=socket(AF_INET,SOCK_STREAM)
                    client_socket.connect((server,server_port))
                    print("Press 'q' to exit")
                    while 1:
                        sen=input(">>")
                        client_socket.send(sen.encode())
                        msg=client_socket.recv(1024)
                        print(">>",msg.decode())
                        if sen=='q':
                            client_socket.close()
                            break
                if choice2==6:
                    break
                        
                    
            
    if choice==1:
        while(1):
            uname=input("Enter Your Username:")
            passw=input("Enter Your Password:")
            speciality=input("Enter Your Speciality:")
            D1=Doctor(uname,speciality)
            check=D1.login(uname,passw)
            if check==0:
                print("Invalid")
            else:
                break
        print("The scheduled appointments for today are:")
        print()
        with open("appointments.txt","r") as file:
            for line in file:
                #print(line)
                line=line.split()
                _,patient=line[0].split(":")
                _,doctor=line[1].split(":")
                _,slot=line[2].split(":",1)
                if doctor==uname:
                    print(patient,doctor,slot)
        print()
    

#schedule(D1,P1,SLOT_1)
#print(D1.calendar)
#print(P1.calendar)
