import matplotlib.pyplot as plt
import os
import mysql.connector
import numpy as np



# Database connection part
electiondb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

mycursor = electiondb.cursor()

#Create Database
mycursor.execute("CREATE DATABASE IF NOT EXISTS electiondb")
mycursor.execute("USE electiondb")

# Create tables
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS political_party(party_id varchar(10), party_name varchar(300), party_leader varchar(125), number_of_members int , primary key(party_id));")
mycursor.execute("CREATE TABLE IF NOT EXISTS provinces(province_id int(5), province_name varchar(100), primary key(province_id));")
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS citizen(citizen_nic varchar(12), citizen_name varchar(250), citizen_age int(2), province_id int, has_voted int default 0, foreign key(province_id) references provinces(province_id),primary key(citizen_nic)); ")
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS candidate(candidate_id int, candidate_name varchar(250), candidate_nic varchar(250), candidate_age int, candidate_education varchar(250), votes int default 0, primary key(candidate_id), province_id int, foreign key(province_id) references provinces(province_id),party_id varchar(100), foreign key(party_id) references political_party(party_id));")


# create classes
class Province:
    def init(self):
        self.province_id = ''
        self.province_name = ''

class PoliticalParty:
    def init(self):
        self.id = ''
        self.name = ''
        self.leader = ''
        self.number_of_members = 0

class Citizen(Province):
    def init(self):
        self.name = ''
        self.NIC = ''
        self.age = 0
        self.has_Voted = False

class Candidate(Citizen, Province):
    def init(self):
        super(Candidate, self).init()
        self.political_Party = ''
        self.votes = 0
        self.candidate_id = ''
        self.education = ''


#adding Province
def add_province():
    # get inputs from user
    province_obj = Province()
    province_obj.province_id = int(input("Enter Province ID : "))
    province_obj.province_name = input("Enter province name : ")
    sql = "INSERT INTO provinces (province_id, province_name) VALUES (%s, %s)"
    val = (province_obj.province_id, province_obj.province_name)
    mycursor.execute(sql, val)
    electiondb.commit()
    print("\n")
    print(mycursor.rowcount, "province record inserted...")
    to_exit = input("press ENTER key  to exit...")
    os.system('cls')

# FUNCTION (get province from user)
def getprovince():
    mycursor.execute("select province_id,province_name from provinces;")
    my_result = mycursor.fetchall()
    for x in my_result:
        print('     ' + str(x[0]) + "." + x[1])
    province = input("Select province(by number): ")
    return province


def political_Partyreg():
    # get inputs from user
    Party = PoliticalParty()

    Party.id = input("Enter ID of the Party : ")
    Party.name = input("Enter Name of the Party : ")
    Party.leader = input("Enter Party leader name : ")
    Party.number_of_members = int(input("Enter Number of members : "))

    # save input to database
    sql = "INSERT INTO political_Party (Party_id, Party_name, Party_leader, number_of_members) VALUES (%s, %s, %s, %s)"
    val = (Party.id, Party.name, Party.leader, Party.number_of_members)
    mycursor.execute(sql, val)
    electiondb.commit()
    print("\n")
    print(mycursor.rowcount, "political Party record inserted.")
    to_exit = input("press ENTER key to exit...")
    os.system('cls')

#FUNCTION (get political Party)
def getParty():
    mycursor.execute("select Party_id,Party_name from political_Party;")
    my_result = mycursor.fetchall()
    for x in my_result:
        print('     ' + x[0] + "." + x[1])
    political_Party = input("Select political Party (by number): ")
    return political_Party


 #FUNCTION (get candidate's details)
def CandidateReq():
    candidate = Candidate()
    candidate.candidate_id = input("Enter Candidate ID : ")
    candidate.name = input("Enter candidate's name: ")
    candidate.NIC = input("Enter candidate's NIC: ")
    candidate.age = int(input("Enter candidate's age: "))
    candidate.education = input("Enter candidate's education: ")
    candidate.political_Party = getParty()
    candidate.province_id = getprovince()

# save candidate details to database(G1_voting_system)
    sql = "INSERT INTO candidate (candidate_id, candidate_name, candidate_nic, candidate_age, candidate_education, province_id,Party_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (
    candidate.candidate_id, candidate.name, candidate.NIC, candidate.age, candidate.education, candidate.province_id,
    candidate.political_Party)
    mycursor.execute(sql, val)
    electiondb.commit()
    print(mycursor.rowcount, " candidate record inserted...")
    to_exit = input("press ENTER key to exit...")
    os.system('cls')

# FUNCTION  (get Citizen details)
def CitizenReq():
    citizen = Citizen()
    citizen.NIC = input("Enter your NIC number : ")
    citizen.name = input("Enter your Name : ")
    citizen.age = int(input("Enter your age : "))
    citizen.province_id = getprovince()

# save citizen details to database(G1_voting_system)
    sql = "INSERT INTO citizen(citizen_nic, citizen_name, citizen_age, province_id) VALUES (%s, %s, %s, %s)"
    val = (citizen.NIC, citizen.name, citizen.age, citizen.province_id)
    mycursor.execute(sql, val)
    electiondb.commit()
    print("\n")
    print(mycursor.rowcount, "citizen record inserted...")
    to_exit = input("press ENTER key to exit...")
    os.system('cls')

#Voting
def vote():

    def hasVote(nic):
        sql = "UPDATE citizen SET has_voted = 1 WHERE citizen_nic = %s"
        val = (nic,)
        mycursor.execute(sql, val)
        electiondb.commit()

    def GetVoterProvince(nic):
        sql = "SELECT province_id FROM citizen where citizen_nic = %s;"
        val = (nic,)
        mycursor.execute(sql, val)
        my_result = mycursor.fetchall()
        for x in my_result:
            province = x[0]
            return province

    def GetCandidateList(province):
        sql = "SELECT candidate_id, candidate_name from candidate WHERE province_id=%s;"
        val = (province,)
        mycursor.execute(sql, val)
        my_result = mycursor.fetchall()
        for x in my_result:
            print('     ' + str(x[0]) + " - " + str(x[1]))

# check ,citizen voted or not
    def voted(nic):
        sql = "SELECT has_voted FROM citizen where citizen_nic = %s;"
        val = (nic,)
        mycursor.execute(sql, val)
        my_result = mycursor.fetchall()
        for x in my_result:
            if x[0] == 0:
                return True
            else:
                return False
#  check , paticular person citizen or not
    def if_citizen(nic):
        mycursor.execute("SELECT citizen_nic FROM citizen;")
        my_result = mycursor.fetchall()
        for x in my_result:
            if x[0] == nic:
                return True
# check  citizen old enough to vote or not
    def check_age(nic):
        sql = "SELECT citizen_age FROM citizen where citizen_nic = %s;"
        val = (nic,)
        mycursor.execute(sql, val)
        my_result = mycursor.fetchall()
        age = 0
        for x in my_result:
            age = x[0]
        if age > 18:
            return True

#  check whether all condition true or not
    def check_conditions(nic):
        age = check_age(nic)
        vote = voted(nic)
        chk_citizen = if_citizen(nic)
        if chk_citizen != True:
            print("Invalid Citizen ID or Not a valid citizen.")
        if age != True:
            print("You are not old enough to vote!(Only citizens above the age of 18 can place a vote.)")
        if vote == False:
            print("You voted once!")
        if age == True and vote == True and chk_citizen == True:
            return True
        else:
            return False

    CitizenNIC = input("Enter your NIC : ")

    conditions = check_conditions(CitizenNIC)

    if conditions == True:
        province = GetVoterProvince(CitizenNIC)
        for i in range(3):
            GetCandidateList(province)
            count = str(i + 1)
            preferense = input("Enter Candidate id to vote : ")
            # get vote count belong to that candidate
            sql = "SELECT votes FROM candidate where candidate_id = %s;"
            val = (preferense,)
            mycursor.execute(sql, val)
            result = mycursor.fetchall()
            for x in result:
                str_result = x[0]
            vote_count = int(str_result) + 1
            # save new votes to database
            sql = "UPDATE candidate SET votes = %s where candidate_id = %s"
            val = (vote_count, preferense)
            mycursor.execute(sql, val)
            electiondb.commit()
            print("\n")
        hasVote(CitizenNIC)

    to_exit = input("press ENTER key to exit...")
    os.system('cls')


# display result
def display_result():
    def get_result(province):
        sql = "SELECT candidate_name, votes FROM candidate where province_id = %s"
        val = (province,)
        mycursor.execute(sql, val)
        my_result = mycursor.fetchall()
        names = []
        votes = []
        for x in my_result:
            names.append(x[0])
            votes.append(x[1])
        return names, votes

    province = getprovince()
    name_array, vote_array = get_result(province)

    x = np.array(name_array)
    y = np.array(vote_array)

    plt.bar(x, y)
    plt.show()

 #menu selection
def main_menu():
    print('========================================================')
    print('*   WELCOME TO THE ELECTION VOTE CALCULATING SYSTEM    *')
    print('========================================================')
    print('     1.Add province')
    print('     2.Add Political Party')
    print('     3.Add Candidate')
    print('     4.Add Citizen')
    print('     5.Vote')
    print('     6.Display Result')
    print('     7.exit')

    choise = int(input("What do you want to choose? (1,2,3,4,5,6,7 ) : "))
    return choise

while (True):
    choise = main_menu()
    if choise == 1:
        how_many = int(input("Enter number of provinces(provinces) you want to include : "))
        for i in range(how_many):
            add_province()

    elif choise == 2:
        how_many = int(input("Enter  number of Political parties, you want to include : "))
        for i in range(how_many):
            political_Partyreg()

    elif choise == 3:
        how_many = int(input("Enter number of candidates, you want to include : "))
        for i in range(how_many):
            CandidateReq()

    elif choise == 4:
        how_many = int(input("Enter number of citizens,  you want to include : "))
        for i in range(how_many):
            CitizenReq()
    elif choise == 5:
        vote()
    elif choise == 6:
        display_result()
    elif choise == 7:
        os.system('cls')
        break
    else:
        print("Invalid choice !")

