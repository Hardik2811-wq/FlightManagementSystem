import mysql.connector as m
import datetime
import time
from prettytable import PrettyTable

con = m.connect(host = 'localhost',user = 'root',password = 'Hdk11564')
obj = con.cursor()

obj.execute('CREATE DATABASE IF NOT EXISTS FLIGHTMANAGEMENTDB')
obj.execute('USE FLIGHTMANAGEMENTDB')


print()
print()
print('Project Name : Arwachin Flight Management System')
print('Prepared By  : Hardik and Ritvik')
print('Class        : XII - A')
print('Teacher      : Ms. Tripti Sharma')
print('Platform     : Python & MySQL')
print()
temp = input('Press any key to START....')


#DATA COLLECTOR

askfid = None
UserMob = None
PID = None
CurrDate = datetime.date.today()
CurrTime = time.strftime('%H:%M:%S') # String Format of Current time

#Date And Time Entry

def Date():
    try:
        date_entry = input('Enter a date in YYYY-MM-DD format: ')
        year,month,day = map(int, date_entry.split('-'))
        date = datetime.date(year, month, day)
        return date
    
    except:
        print('\nDate is Inavlid!!\n')
        Date()

def Time():
    try:
        time_entry = input('Enter a time in HH-MM-SS format: ')
        hour,minute,second = map(int, time_entry.split('-'))
        time1 = datetime.time(hour, minute, second)
        return time1
    
    except:
        print('\nDate is Inavlid!!\n')
        Time()


#EXIT INTERFACE

def ExitApp():
    ask_exit = input('Are you sure you want to EXIT(y/n): ')
    if ask_exit.lower() in ('y','n'):
        if ask_exit.lower() == 'y':
            print('\n--------------------------------------Thanks For Visiting Arwachin Flight Management System--------------------------------------\n')
            time.sleep(2)
            exit()
        if ask_exit.lower() == 'n':
            Login()
    else:
        print('\nInvalid Selection!!..\n')
        ExitApp()



#ADMIN INTERFACE
        
def Admin():
    print('   Admin Interface   '.center(120,'-'))
    print('\nHello Admin, What do you want to do?\n\n')
    print('1. Management Dashboard \n')
    print('2. Reporting Dashboard \n')
    print('3. Log Out \n')
    Opt1 = int(input("Enter Option Value : "))

    match Opt1:
        case 1:
            ManagementDashboard()

        case 2:
            print("----- REPORT DASHBOAD ---- \n\n")
            ReportingDashboard()

        case 3:
            print("Thanks for Visiting!! \n\n")
            Login()

                     
        case _:
            print("Wrong option selected.")
            Admin()



#Adding Flight(s)

def UpdFlight():
    print('Enter the following details to Add a Flight'.center(80,' '))
    operator = input('Enter the Flight Operator: ')
    Dep1 = input('Enter the Departure: ')
    Arv1 = input('Enter the Destination: ')
    print('Enter Departure date!!')
    Depdate = Date()
    print('Enter Departure time!!')
    Deptime = Time()
    print('Enter Arrival date!!')
    Arvdate = Date()
    print('Enter Arrival time!!')
    Arvtime = Time()
    obj.execute('SELECT * FROM SeatDetails')
    SD = obj.fetchall()
    t_sd = PrettyTable(['Seat ID','Economy','Business','Max EcoSeat','Max BizSeat'])
    for i in SD:
        t_sd.add_row([i[0],i[1],i[2],i[3],i[4]])
    print(t_sd,'\n')
    sid = int(input('Enter Seat ID for this Flight: '))
    obj.execute('SELECT SID FROM SeatDetails')
    S_ID = obj.fetchall()
    for i in S_ID:
        if sid in i:
            obj.execute("INSERT INTO FlightDetails(SID,Foperator,DepartureFrom,ArrivalTo,DepDate,DepTime,ArvDate,ArvTime,BookedBiz,BookedEco) VALUES({},'{}','{}','{}','{}','{}','{}','{}',0,0)".format(sid,operator,Dep1,Arv1,Depdate,Deptime,Arvdate,Arvtime))
            con.commit()
            ManagementDashboard()
    else:
        print('\nSeat ID not found!!\n')
        UpdFlight()
            

#Add Seat Class

def AddSeat():
    print('\nEnter the following details to add a new Seat Class\n')
    EcoPrice = int(input('\tEnter the price of Economic class seat: '))
    BizPrice = int(input('\tEnter the price of Business class seat: '))
    EcoSeat = int(input('\tEnter the max no. of Economic class seat: '))
    BizSeat = int(input('\tEnter the max no. of Business class seat: '))
    obj.execute("INSERT INTO SeatDetails(Economy,Business,MaxEcoSeat,MaxBizSeat) VALUES({},{},{},{})".format(EcoPrice,BizPrice,EcoSeat,BizSeat))
    con.commit()
    print('\nSeatc Class Addedd Successfully!!\n')
    temp = input('Press any key to continue....')
    ManagementDashboard()
    
    
def UpdSeat():
    print('\n\tHere is the List of all the Seat Classes\n')
    obj.execute("SELECT * FROM SeatDetails")
    seatdetails = obj.fetchall()
    t_SD = PrettyTable(['Seat ID','Economy','Business','Max. EcoSeat','Max. BizSeat'])
    for i in seatdetails:
        t_SD.add_row([i[0],i[1],i[2],i[3],i[4]])
    print(t_SD)
    
    S_id = int(input('Enter the Seat ID you want to update: '))
    
    for x in seatdetails:
        if S_id in x:
            n_ecop = int(input('\tEnter new Economy price: '))
            n_bizp = int(input('\tEnter new Business price: '))
            n_ecos = int(input('\tEnter new Economy Seats: '))
            n_bizs = int(input('\tEnter new Business Seats: '))
            obj.execute("UPDATE SeatDetails SET Economy = {}, Business = {}, MaxEcoSeat = {}, MaxBizSeat = {} WHERE SID = {}".format(n_ecop,n_bizp,n_ecos,n_bizs,S_id))
            con.commit()
            print("\n\nOperation sucessfully Executed!!\n\n")
            print('\n\tHere is the Updated List of Seat Classes\n')
            obj.execute("SELECT * FROM SeatDetails")
            seatdetails = obj.fetchall()
            t_SD = PrettyTable(['Seat ID','Economy','Business','Max. EcoSeat','Max. BizSeat'])
            for i in seatdetails:
                t_SD.add_row([i[0],i[1],i[2],i[3],i[4]])
            print(t_SD)
            temp = input('\nPress Any key to continue...')
            ManagementDashboard()
            break
    else:
        print('Seat ID not found!!')
        temp = input('\nPress Any key to continue...')
        ManagementDashboard()


#Management Dashboard Interface
      
def ManagementDashboard():
    print()
    print()
    cstr = "    ADMIN MANAGEMENT DASHBOARD   "
    print(cstr.center(120, '-'))
    print('\n\nSelect a management task to perform:  \n\n')
    print('1. Add Flight \n')
    print('2. Add Seat Class\n')
    print('3. Update Seat Class\n')
    print('4. Go back \n')
    Opt2 = int(input("Enter your choice: "))
    

    match Opt2:
       
       case 1:
           UpdFlight()
           
       case 2:
           AddSeat()

       case 3:
           UpdSeat()
                                
       case 4:
           Admin()
                     
       case _:
           print("Wrong option selected.")
           ManagementDashboard()


#Expired Booking Details

def ExpBooking():
    obj.execute("SELECT * FROM BookingDetails WHERE BStatus = 'Expired'")
    Exp_BD = obj.fetchall()
    t_expBD = PrettyTable(['Booking ID','Passenger ID','Flight ID','Booking Date','Booking Time','Class','Status'])
    for i in Exp_BD:
        t_expBD.add_row([i[0],i[1],i[2],i[3],i[4],i[6],i[5]])
    print(t_expBD)
    temp = input('\nPress Any key to continue...')
    ReportingDashboard()



#Confirmed Booking Details
def ConBooking():
    obj.execute("SELECT * FROM BookingDetails WHERE BStatus = 'Confirmed'")
    con_BD = obj.fetchall()
    t_conBD = PrettyTable(['Booking ID','Passenger ID','Flight ID','Name','Mobile No.','Class'])
    for i in con_BD:
        t_conBD.add_row([i[0],i[1],i[2],i[3],i[4],i[5]])
    print(t_conBD)
    temp = input('\nPress Any key to continue...')
    ReportingDashboard()


#Cancellation of Bookings

def CancelBooking():

    obj.execute("SELECT * From BookingDetails WHERE BStatus = 'Cancellation Requested'")
    cancbook = obj.fetchall()
    check_cancbook = len(cancbook)
    match check_cancbook:
        case 0:
            print('\nNo Cancel request found!!\n')
            temp = input('Press any key to continue...')
            ReportingDashboard()
        case _:
            print('\n\tHere is the List of all the Booking Cancellation Request')
            t_cancbook = PrettyTable(['Booking ID','Passenger ID','Flight ID','Date','Time','Status','Class'])
            for i in cancbook:
                t_cancbook.add_row([i[0],i[1],i[2],i[3],i[4],i[5],i[6]])
            print(t_cancbook)
            
            ask3 = input('\nDo you want to accept these requests(y/n): ')
            if ask3.lower() == 'y':
                obj.execute("UPDATE BookingDetails SET BStatus = 'Cancelled' WHERE BStatus = 'Cancellation Requested'")
                con.commit()
                temp = input('\nPress Any key to continue...')
                ReportingDashboard()
            elif ask3.lower() == 'n':
                ReportingDashboard()
            else:
                print('Kindly select an appropiate answer!!')
                CancelBooking()


#Active Flight Details

def ActFlight():
    print('\n\tHere is the Details of All the Active Flights!!\n')
    obj.execute("SELECT * FROM FlightDetails WHERE DepDate >= '{}'".format(CurrDate))
    ActFD = obj.fetchall()
    t_actfd = PrettyTable(['Flight ID','Seat ID','Operator','Departure','Destination','Depdate','DepTime','ArvDate','ArvTime','BookedBiz','BookedEco'])
    for i in ActFD:
        t_actfd.add_row([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]])
    print(t_actfd)
    temp = input('\nPress Any key to continue...')
    ReportingDashboard()


#Expired Flight Details

def ExpFlight():
    print('\n\tHere is the Details of All the Expired Flights!!\n')
    obj.execute("SELECT * FROM FlightDetails WHERE DepDate < '{}'".format(CurrDate))
    ExpFD = obj.fetchall()
    t_expfd = PrettyTable(['Flight ID','Seat ID','Operator','Departure','Destination','Depdate','DepTime','ArvDate','ArvTime','BookedBiz','BookedEco'])
    for i in ExpFD:
        t_expfd.add_row([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]])
    print(t_expfd)
    temp = input('\nPress Any key to continue...')
    ReportingDashboard()





# Passenger Details

def ViewPD():
    print('\n\tHere is the Details of the Passengers!!\n')
    obj.execute('SELECT * FROM PassengerDetails')
    Passenger_details = obj.fetchall()
    t_pd = PrettyTable(['Passenger ID','Name','Mobile Number'])
    for i in Passenger_details:
        t_pd.add_row([i[0],i[1],i[2]])
    print(t_pd)
    temp = input('\nPress Any key to continue...')
    ReportingDashboard()


#Reporting DashBoard
            

def ReportingDashboard():
    print()
    print()
    cstr = "    ADMIN REPORTS   "
    print(cstr.center(120, '-'))
    print()
    print()
    print('\n\n Select the Report Type :  \n\n')
    print('1. Show All Passengers \n')
    print('2. Show All Confirmed Bookings \n')
    print('3. Show All Cancel Requests \n')
    print('4. Show All Active Flights \n')
    print('5. Show All Expired Bookings \n')
    print('6. Show All Expired Flights \n')
    print('7. Go back \n')
    Opt3 = int(input("Enter your choice.. : "))
    

    match Opt3:
       
       case 1:
           print("Following Passenger Details: \n\n")
           ViewPD()

       case 2:
           print("Following Confirmed Booking Deatils: \n\n")
           ConBooking()

       case 3:
           print("Following Booking Cancellation Request: \n\n")
           CancelBooking()
                     
       case 4:
           print("Following Active Flight Deatils: \n\n")
           ActFlight()

       case 5:
           print("Following Expired Booking Details: \n\n")
           ExpBooking()
                   
       case 6:
           print("Following Expired Flight Details: \n\n")
           ExpFlight()
           
       case 7:
           print("Thanks for Visiting!! \n\n")
           Admin()
           
       case _:
           print("Wrong option selected.")
           ReportingDashboard()

#Booking Flight Ticket

def BookingFlight():
    print()
    print()
    cstr = "    FLIGHT BOOKING   "
    print(cstr.center(120, '-'))
    print()
    print()
    global askfid
    obj.execute('SELECT flightdetails.fid, seatdetails.sid, seatdetails.Economy, seatdetails.Business From flightdetails LEFT JOIN seatdetails ON flightdetails.sid = seatdetails.sid WHERE flightdetails.fid = {}'.format(askfid))
    SeatDetails = obj.fetchall()
    t_sd = PrettyTable(['Flight ID','Seat ID','Economy','Business'])
    for i in SeatDetails:
       t_sd.add_row([i[0],i[1],i[2],i[3]])
    print('\n',t_sd,'\n')
    print('Select the Flight Class')
    print('1. Economy')
    print('2. Business')
    seat_class = int(input('Enter the Class of your Flight: '))
    if seat_class not in (1,2):
        print('Kindly Select appropiate option!!')
        User()
    else:
        ask1 = input('Are you sure (y/n)??: ')
        if ask1.lower() == 'y':
            match seat_class:
                case 1:
                    obj.execute("INSERT INTO BookingDetails(PID,FID,BDate,BTime,BClass,BStatus) VALUES({},{},'{}','{}','Economy','Confirmed')".format(PID,askfid,CurrDate,CurrTime))
                    con.commit()
                    obj.execute("SELECT BookedEco From flightdetails WHERE FID = {}".format(askfid))
                    BEco_tup = obj.fetchall()
                    Booked_Eco = BEco_tup[0][0]
                    obj.execute("UPDATE FlightDetails SET BookedEco = {} WHERE FID = {}".format(Booked_Eco+1,askfid))
                    con.commit()
                    print('Congratulations!! Your flight is successfully booked.')
                    temp = input('\nPress Any key to continue...')
                    User()
                 

                case 2:
                    obj.execute("INSERT INTO BookingDetails(PID,FID,BDate,BTime,BClass,BStatus) VALUES({},{},'{}','{}','Business','Confirmed')".format(PID,askfid,CurrDate,CurrTime))
                    con.commit()
                    obj.execute("SELECT BookedBiz From flightdetails WHERE FID = {}".format(askfid))
                    BBiz_tup = obj.fetchall()
                    Booked_Biz = BBiz_tup[0][0]
                    obj.execute("UPDATE FlightDetails SET BookedBiz = {} WHERE FID = {}".format(Booked_Biz+1,askfid))
                    con.commit()
                    print('Congratulations!! Your flight is successfully booked.')
                    temp = input('\nPress Any key to continue...')
                    User()
                   

        else:
            temp = input('\nPress Any key to continue...')
            User()
    

    
#USER INTERFACE

def User():
    print()
    cstr = "    USER DASHBOARD   "
    print(cstr.center(120, '-'))
    print()
    print()
    global askfid
    print('\n')
    print('1. Show my bookings')
    print('2. Book my flight')
    print('3. Send Booking Cancellation Request')
    print('4. Log Out')
    Opt = int(input("\n\nEnter your choice.. : "))
    

    match Opt:
       
       case 1:
            obj.execute('SELECT  bookingdetails.bid ,bookingdetails.BDate,flightdetails.Foperator,bookingdetails.BClass,flightdetails.departurefrom,flightdetails.arrivalto, flightdetails.depdate, flightdetails.deptime, flightdetails.arvdate ,flightdetails.arvtime,bookingdetails.BStatus FROM flightdetails LEFT JOIN BookingDetails  ON bookingdetails.fid = flightdetails.fid WHERE bookingdetails.pid = {}'.format(PID))
            Bdetails = obj.fetchall()
            if len(Bdetails) != 0:
                t_bd = PrettyTable(['Booking ID','Booking Date','Operator','Class','Departure From','Arriving To','Departure Date','Departure Time','Arrival Date','Arrival Time','Status'])
                for i in Bdetails:
                    t_bd.add_row([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]])
                print(t_bd)
                temp = input('\nPress Any key to continue...')
                User()
            else:
                print('No Prior Booking records found!!')
                temp = input('\nPress Any key to continue...')
                User()

       case 2:
           print('\nHere is the List of the Available Flights:\n')
           obj.execute("SELECT FID, FOperator, DepartureFrom, ArrivalTo, DepDate, DepTime, ArvDate, ArvTime From flightdetails WHERE DepDate > '{}'".format(CurrDate))
           AvailF = obj.fetchall()
           t_fd = PrettyTable(['Flight ID','Operator','Departure From','Arriving To','Departure Date','Departure Time','Arrival Date','Arrival Time'])
           for i in AvailF:
               t_fd.add_row([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]])
           print('\n',t_fd,'\n')

           Dep = input('Enter your Departure: ')
           Dest = input('Enter your Destination: ')

           obj.execute("SELECT FID, FOperator, DepartureFrom, ArrivalTo, DepDate, DepTime, ArvDate, ArvTime From flightdetails WHERE DepartureFrom = '{}' AND ArrivalTo = '{}' AND DepDate > '{}'".format(Dep,Dest,CurrDate))
           AvailF1 = obj.fetchall()
           if len(AvailF1) != 0:
               t_fd1 = PrettyTable(['Flight ID','Operator','Departure From','Arriving To','Departure Date','Departure Time','Arrival Date','Arrival Time'])
               for i in AvailF1:
                   t_fd1.add_row([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]])
               print('\n',t_fd1,'\n')
               print('\nKindly select the flight via Flight ID!!\n')
               askfid = int(input('Enter the Flight ID: '))
               obj.execute("SELECT FID FROM FlightDetails WHERE DepDate > '{}' AND DepartureFrom = '{}' AND ArrivalTo = '{}'".format(CurrDate,Dep,Dest))
               F_iDs = obj.fetchall()
               for i in F_iDs:
                   if askfid in i:
                       BookingFlight()
                       break
                   else:
                       print('\nFlight ID not found!!\n')
                       User()
           else:
               print('No Flight Available')
               temp = input('\nPress Any key to continue...')
               User()


       case 3:
            obj.execute("SELECT  bookingdetails.bid ,bookingdetails.BDate,bookingdetails.BClass,flightdetails.Foperator, flightdetails.departurefrom, flightdetails.arrivalto, flightdetails.depdate, flightdetails.deptime, flightdetails.arvdate ,flightdetails.arvtime, bookingdetails.BClass , bookingdetails.BStatus FROM flightdetails LEFT JOIN BookingDetails  ON bookingdetails.fid = flightdetails.fid WHERE bookingdetails.pid = {} AND flightdetails.DepDate > '{}' AND bookingdetails.BStatus = 'Confirmed'".format(PID,CurrDate))
            Bdetails = obj.fetchall()
            if len(Bdetails) != 0:
                t_bd = PrettyTable(['Booking ID','Booking Date','Operator','Departure From','Arriving To','Departure Date','Departure Time','Arrival Date','Arrival Time','Class','Status'])
                for i in Bdetails:
                    t_bd.add_row([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10]])
                print(t_bd)
                print()
                req_id = int(input('Enter the Booking ID: '))
                obj.execute("SELECT BookingDetails.BID FROM BookingDetails LEFT JOIN PassengerDetails ON BookingDetails.PID = PassengerDetails.PID WHERE PassengerDetails.PID = {} AND BStatus = 'Confirmed'".format(PID))
                req_BD = obj.fetchall()
                for i in req_BD:
                    if req_id in i:
                        obj.execute("UPDATE Bookingdetails SET Bstatus = 'Cancellation Requested' WHERE BID = {}".format(req_id))
                        con.commit()
                        print('\nRequest For Cancellation has been sent\n')
                        User()
                        break
                else:
                    print('\nNo such Booking ID exist\n')
                    temp = input('\nPress Any key to continue...')
                    User()
                
            else:
                print('No Prior Booking records found!!')
                temp = input('\nPress Any key to continue...')
                User()
                
       case 4:
           Login()
       
       case _:
           print("Invalid option ...")
           User()
           
            


#Admin Login

def AdminLogin():
    print()
    print()
    cstr = "    ADMIN LOGIN   "
    print(cstr.center(120, '-'))
    print()
    print()
    pswd = input('Enter Admin Password to log in: ')
    if pswd == 'Admin@123':
        print('\nWelcome Admin!!\n\n')
        Admin()
    else:
        print('Incorrect Password!!')
        print('Do you want to try again?')
        print('Type 1 to try again ')
        ask2 = int(input('Select an option: '))
        if ask2 == 1:
            print()
            AdminLogin()
        else:
            print()
            Login()





#User Login Interface

def UserLogin():
    global UserMob
    global PID
    print()
    cstr = "    USER LOGIN   "
    print(cstr.center(120, '-'))
    print()
    print()
    n = int(input(('Enter your mobile number to log in: ')))
    obj.execute('SELECT * FROM PassengerDetails')
    mob = obj.fetchall()       
    for i in mob:
        if n in i:
            UserMob = n
            PID = i[0]
            print('\nWelcome ',i[1],' !\n\n')
            User()
            break
    else:
        print('\n\nUser not found.. TRY AGAIN!!\n')
        temp = input('Press any Key to continue...\n')
        UserSignIn()


#User Sign Up Interface

def UserSignUp():
    global UserMob
    global PID
    print()
    print()
    cstr = "    NEW USER SIGNUP   "
    print(cstr.center(120, '-'))
    print()
    print()
    U_name = input('Enter your name: ')
    U_mob = int(input('Enter your mobile number: '))
    if len(str(U_mob)) == 10 or str(U_mob).startswith('0'):
        obj.execute("SELECT PMob FROM PassengerDetails")
        PMob = obj.fetchall()
        for i in PMob:
            if U_mob in i:
                print('\nAn user account with this mobile number already exists. Kindly use different mobile number. Thanks !!\n')
                UserSignUp()
                break
        else:
            obj.execute("INSERT INTO PassengerDetails(PName,PMob) VALUES('{}',{})".format(U_name,U_mob))
            con.commit()
            UserMob = U_mob
            obj.execute("SELECT PID FROM PassengerDetails WHERE PMob = {}".format(UserMob))
            PID = obj.fetchall()[0][0]
            print('\nNew User Account Created Sucessfully\n')
            print('\tUser Details:')
            print('\tName:',U_name)
            print('\tMob. No.:',U_mob)
            print('\tUse your Mobile number for login next time...')
            temp = input('\nPress Any key to continue...')
            print('\nWelcome ',U_name, ' !')
            User()
    else:
        print('\nInvalid Mobile number!! Try Again\n')
        UserSignIn()
    

           
    
#User Signing InterFace

def UserSignIn():
    print()
    cstr = "    USER MENU   "
    print(cstr.center(120, '-'))
    print()
    print()
    print('\n\n1. Login')
    print('2. SignUp')
    print('3. Exit')
    ask_user = int(input('\nSelect an option: '))
    if ask_user == 1:
        UserLogin()
    elif ask_user == 2:
        UserSignUp()
    elif ask_user == 3:
        Login()
    else:
        print('Kindly Select an appropiate option!!')
        UserSignIn()



#MAIN INTERFACE

def Login():                       
    print()
    cstr = "    MAIN MENU   "
    print(cstr.center(120, '-'))
    print('\n\nSelect your Role ..')
    print('\t1. Admin')
    print('\t2. User')
    print('\t3. Exit\n')
    n = int(input('Kindly select an option: '))
    if n in (1,2,3):
        
        if n == 1:
            AdminLogin()
        if n == 2:
            UserSignIn()
        if n == 3:
            print()
            ExitApp()
    else:
        print('Invalid option!! Try again..')
        print()
        Login()


#Refresher Function

def Refresher():
    obj.execute("UPDATE BookingDetails as bd LEFT JOIN flightdetails as fd ON bd.fid = fd.fid SET bd.BStatus = 'Expired' WHERE fd.DepDate < '{}'".format(CurrDate))
    con.commit()


Refresher()
   
Login()
