# Paul Jensen Jr. 010398334
import datetime
import csv
packageList = []
packageIDList = []
loadedPackages = []

class ChainingHashTable:
    def __init__(self,size):
        #create a 2-d array with a "size" number of buckets
        self.Table = []
        self.size = size
        for each in range(size):
            self.Table.append([])
    def insert(self,key,item):
        # Use a key, item pair to insert an object into the hashtable with an easy key to retrive it
        bucket = hash(key)%self.size
        bucket_item = self.Table[bucket]
        bucket_item.append([key, item])

    def search(self,key):
        #search for the key and return the item
        bucket = hash(key)%self.size
        bucket_item = self.Table[bucket]
        for each in bucket_item:

            if key == each[0]:
                return each[1]
        return None

    def remove(self, key):
        #search for the item, and if it exists return it and remove it otherwise return none
        bucket = hash(key) % len(self.Table)
        bucket_list = self.Table[bucket]
        for each in bucket_list:
            if key == each[0]:
                return each[1]
            else:
                return None
# Chaining HashTable From Course Material.
# InLine Citation
# (Lysecky, R., & Vahid, F., Figure 7.8.2: Hash table using chaining.)
packageHash = ChainingHashTable(20)
class Truck:
    #The truck class stores it's packages as well as the start and stop times for the truck.
    def __init__(self,startTime=0,onlyEOD=0):
        self.deliveredList = []
        self.specialDeliveredList = []
        self.miles = 0
        self.deliveryQueue = []
        self.time = startTime
        self.onlyEOD = onlyEOD
        self.startTime = self.time
        self.stopTime = self.time
    def deliverPackages(self):
        for each in self.deliveryQueue:
            time = each[1]/18.*60.#time is equal to miles/18 mph*60/hour to get it in minutes, each[1] is the distance of the current element.
            self.time += datetime.timedelta(minutes=time)
            each[0].deliveryTime=self.time
        self.stopTime=self.time
    def returnToHub(self):
        distance = float(distanceLookup[addressList.index(self.deliveryQueue[-1][0].address)][0])#the truck only returns to the hub after all packages have been delivered in it's routine.
        time = distance/18*60
        self.time += datetime.timedelta(minutes=time)
        self.stopTime=self.time
    def queuePackages(self, current=""):
        global newPackage
        if current != "": #this allows a starting package to be selected otherwise it finds the closest package to the hub
            self.deliveryQueue.append((current, float(distanceLookup[0][addressList.index(current.address)])))
        else:
            closest = 1000000 # both current and closest are set to a high number to make sure the will be lowered
            newPackage = current
            for each in self.deliveredList: #loop through all remaining packages
                distance = float(distanceLookup[0][addressList.index(each.address)]) #get distance from closest to furthest
                if distance < closest: #check if package is closer than the previous
                    closest = distance
                    newPackage = each
            self.deliveryQueue.append((newPackage, closest)) #add the closest package after the whole loop to the queue
            current = newPackage
        loop_count = 1
        #repeat above steps for all packages
        while len(self.deliveredList)>1:
            self.deliveredList.remove(current)
            closest = 1000000000000
            for each in self.deliveredList:
                distance = distanceLookup[addressList.index(current.address)][addressList.index(each.address)]
                if float(distance) <= closest:
                    closest = float(distance)
                    newPackage = each
            self.deliveryQueue.append([newPackage,closest])
            current = newPackage
        if self.specialDeliveredList!=[]:
            self.deliveryQueue.append((self.specialDeliveredList[0],float(distanceLookup[addressList.index(current.address)][addressList.index(self.specialDeliveredList[0].address)])))

class Package:
    def __init__(self,ID,Address,City,State,Zip,DeliveryDeadline,Mass,specialNotes):
        self.id = ID
        self.address = Address
        self.city = City
        self.state = State
        self.zip = Zip
        self.deadline = DeliveryDeadline
        self.mass = Mass
        self.notes = specialNotes
        self.deliveryTime = 0
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s"%(self.id,self.address,self.city,self.state,self.zip,self.deadline,self.mass,self.notes)
def loadPackages(fileName):
    global packageList,packageHash

    with open(fileName) as Packages:
        packageData = csv.reader(Packages, delimiter = ",") #open packages
        for package in packageData:
            packageList.append(Package(package[0],package[1],package[2],package[3],package[4],package[5],package[6],package[7]))
            packageHash.insert(int(package[0]), Package(package[0],package[1],package[2],package[3],package[4],package[5],package[6],package[7]))
            packageIDList.append(int(package[0]))
def distanceFrom(address1,address2):
    return distanceLookup[address1][address2]
def loadTrucks(truck1,truck2,truck3):
    truck1PackageList = (1,4,7,13,14,15,16,19,20,27,29,30,31,34,39,40)
    truck2PackageList = (3,5,6,25,26,32,36,37,38)
    for each in truck1PackageList:
        truck1.deliveredList.append(packageHash.search(each))
    for each in truck2PackageList:
        truck2.deliveredList.append(packageHash.search(each))
    truck2.specialDeliveredList.append(packageHash.search(18))
    packageList[17] = "loaded package"
    for each in truck1PackageList:
        packageList[each-1]="loaded package"
    for each in truck2PackageList:
        packageList[each-1]="loaded package"
    for each in range(len(packageList)):
        try:
            if packageList[each].deadline == "EOD" and len(truck3.deliveredList) < 16:
                truck3.deliveredList.append(packageList[each])
                packageList[each]="loaded package"
        except:
            pass # this will only raise an error when the item is loaded package. Stings have no attribute deadline.
def createDistanceTable(fileName,AddressList, distanceLookup):
    with open(fileName) as Addresses:
        Address = csv.reader(Addresses,delimiter = ",")
        next(Address)
        placeCounter = 2
        for Addy in Address:
            beans=Addy[0].split("\n")
            beans= beans[1].split(",")
            AddressList.append(beans[0][1:])

            i=2
            while i<=placeCounter:
                #creates a 2d array where the order of I and J don't matter and find the listed address
                distanceLookup[i-2][placeCounter-2]=Addy[i]
                distanceLookup[placeCounter-2][i-2] = Addy[i]
                i+=1
            placeCounter+=1
def checkStatusAtTime(time):
    #Check to see if the truck has started, or compare times to see if they have been dilvered or not
    if time<=truck1.startTime:
        for each in truck1.deliveryQueue:
            print(each[0], " At The Hub")
    if time<=truck2.startTime:
        for each in truck2.deliveryQueue:
            print(each[0],"At The Hub")
    if time<=truck3.startTime:
        for each in truck3.deliveryQueue:
            print(each[0],"At The Hub")
    if time>truck1.startTime:
        for each in truck1.deliveryQueue:
            if each[0].deliveryTime>=time:
                print(each[0],"En route")
            else:

                print(each[0],"Delivered",each[0].deliveryTime)
    if time > truck2.startTime:
        for each in truck2.deliveryQueue:
            if each[0].deliveryTime >= time:
                print(each[0], "En route")
            else:
                print(each[0], "Delivered", each[0].deliveryTime)
    if time > truck3.startTime:
        for each in truck3.deliveryQueue:
            if each[0].deliveryTime >= time:
                print(each[0], "En route")
            else:
                print(each[0], "Delivered", each[0].deliveryTime)
def truckMileage(time):
    #calculate how far the trucks have gone at the given time by checking how far they have moved since they started. If the truck has stopped just take the time the truck was moving
    miles1=0
    miles2=0
    miles3=0
    time1=(time-truck1.startTime).total_seconds()
    time2 =(time-truck2.startTime).total_seconds()
    time3 =(time-truck3.startTime).total_seconds()
    if time1>=0 and time<truck1.stopTime:
        miles1=time1/3600.*18.
    elif time1>0:
        miles1=(truck1.stopTime-truck1.startTime).total_seconds()/3600.*18.
    if time2>0 and time<truck2.stopTime:
        miles2=time2/3600.*18.
    elif time2>0:
        miles2=(truck2.stopTime - truck2.startTime).total_seconds()/3600.*18.
    if time3>0 and time<truck3.stopTime:
        miles3=time3/3600.*18.
    elif time3>0:
        miles3=(truck3.stopTime - truck3.startTime).total_seconds()/3600.*18.
    print("Truck 1 has gone: ",miles1," miles")
    print("Truck 2 has gone: ", miles2, " miles")
    print("Truck 3 has gone: ", miles3, " miles")
    print("the trucks have traveled: ", miles1+miles2+miles3," miles")
if __name__ == '__main__':
    truck1 = Truck(startTime=datetime.datetime.combine(datetime.datetime.today(),datetime.time(hour=8)))
    truck2 = Truck(startTime=datetime.datetime.combine(datetime.datetime.today(),datetime.time(hour=9,minute=5)))
    truck3 = Truck(onlyEOD=1,startTime=datetime.datetime.combine(datetime.datetime.today(),datetime.time(hour=10,minute=20)))
    loadPackages("WGUPS Package File - Sheet1.csv")
    loadTrucks(truck1,truck2,truck3)
    distanceLookup=[]
    #create lookup array
    for each in range(27):
        distanceLookup.append([])
        for every in range(27):
            distanceLookup[each].append([])
    addressList = []
    createDistanceTable("WGUPS Distance Table .csv",addressList,distanceLookup)
    truck1.queuePackages(truck1.deliveredList[4])
    sum =0
    truck2.queuePackages(truck2.deliveredList[5])
    truck1.deliverPackages()
    truck1.returnToHub()
    for each in truck3.deliveredList:

        if int(each.id)==9:
            each.address="410 S State St"
            each.zip="84111"

    truck3.queuePackages(truck3.deliveredList[0])
    truck2.deliverPackages()
    truck3.deliverPackages()
    while True:
        try:
            choice = input("1. mileage of the trucks:\n2. status of packages:\n")
            if int(choice) == 1:
                trucktime = datetime.time(hour=15)
                trucktime = datetime.datetime.combine(datetime.datetime.today(), trucktime)
                truckMileage(trucktime)
                break
            elif int(choice) == 2:
                yourtime = input("enter your time here as H:MM; type anything else to stop: ")
                yourtime = yourtime.split(":")
                yourtime = datetime.time(hour=int(yourtime[0]), minute=int(yourtime[1]))
                yourtime = datetime.datetime.combine(datetime.datetime.today(), yourtime)
                checkStatusAtTime(yourtime)
            else:
                print("invaild choice try again")
        except:
            print("\nfinished")
            break
