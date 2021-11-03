import os, time;
from collections import namedtuple;
from Passenger import PassengerIdPair;
from Passenger import Passenger;

#region Properties
folderPath = os.path.dirname(os.path.normpath(__file__));
inputFilePath = os.path.join(folderPath, "allomas.be");
outputFilePath = os.path.join(folderPath, "allomas.ki");

Pair = namedtuple("Pair", ["Tick", "Count"]);
passengers = [];
passengersInLobby = 0;
leftPassangers = 0;
waitingBoardingPassengers = 0;
metroInPassengers = 0;
metroOutPassengers = 0;
incomingMetroIndex = 0;
metroAvailable = False;
#endregion Properties

def ReadInputFile():
    try:
        file = open(inputFilePath);
        firstRow = file.readline().split();
        
        global boardingTickCount;
        global escalatorLength;
        global lobbyCapacity;
        global metroFrequency;
        global boardingPassengerCount;
        
        boardingTickCount = int(firstRow[0]);
        escalatorLength = int(firstRow[1]);
        lobbyCapacity = int(firstRow[2]);
        metroFrequency = int(firstRow[3]);
        boardingPassengerCount = int(firstRow[4]);
        
        global boardingPassengers;
        boarding_passenger_ticks = [];
        
        for i in range(0, boardingPassengerCount):
            boarding_passenger_ticks.append(int(file.readline()));
        
        boardingPassengers = [];
        i = 0;
        while(i < len(boarding_passenger_ticks)):
            count = 1;
            for j in range(i + 1, len(boarding_passenger_ticks)):
                if(boarding_passenger_ticks[j] == boarding_passenger_ticks[i]):
                    count += 1;
                    i += 1;
                else:
                    break;
            boardingPassengers.append( Pair(boarding_passenger_ticks[i], count) );
            i += 1;
        
        global landing_passengers;
        landing_passengers = [];
        splittedLine = file.readline().split();
        for i in splittedLine:
            landing_passengers.append(int(i));
        
        file.close();
        return True;
    except Exception as exc:
        print("Something went wrong while trying to read input file!");
        print(exc);
        return False;

def PrintStuffToConsole():
    print("Időegységek száma: " + str(boardingTickCount));
    print("Mozgólépcső hossza: " + str(escalatorLength));
    print("Váróterem kapacitása: " + str(lobbyCapacity));
    print("Metrók követési távolsága: " + str(metroFrequency));
    print("Érkező utasok száma: " + str(boardingPassengerCount));
    print();
    print("Felszálló utasok érkezései: ");
    for i in boardingPassengers:
        print("\tTick: " + str(i.Tick) + " \tCount: " + str(i.Count));
    print();
    print("Érkező utasok számai: ");
    print(landing_passengers);

def PrintTickInfo(currentTick):
    os.system('cls');
    
    print(str(waitingBoardingPassengers) + "\t" + str(leftPassangers));
    print("--\t--");
    for i in range(0, len(passengersOnDownwardEscalator)):
        if(currentTick == 9):
            print();
        print(str(passengersOnDownwardEscalator[i]) + "\t" + str(passengersOnUpwardEscalator[-i-1]));
    
    print("    " + str(passengersInLobby));
    print("----------");
    print(str(metroOutPassengers) + "\t" + str(metroInPassengers));
    print();

def FillEmptyEscalatorSpaces():
    global passengersOnDownwardEscalator;
    global passengersOnUpwardEscalator;
    passengersOnDownwardEscalator = [];
    passengersOnUpwardEscalator = [];
    for i in range(0, escalatorLength):
        passengersOnDownwardEscalator.append(0);
        passengersOnUpwardEscalator.append(0);

def HandleNewBoardingPassengers(currentTick):
    currentPair = "";
    for i in boardingPassengers:
        if(i.Tick == currentTick):
            currentPair = i;
            break;
        
    if(currentPair == ""):
        return;
    
    global passengers;
    
    if(passengersOnDownwardEscalator[0] < 2):
        if(currentPair.Count == 0):
            return;
        elif(currentPair.Count == 1):
            global passengers;
            newPassenger = Passenger("boarding", "escalatorDown0", escalatorLength);
            passengers.append(PassengerIdPair(newPassenger.id, newPassenger));
            passengersOnDownwardEscalator[0] += 1;
            currentPair = Pair(currentPair.Tick, currentPair.Count - 1);
        else:
            newPassenger = Passenger("boarding", "escalatorDown0", escalatorLength);
            passengers.append(PassengerIdPair(newPassenger.id, newPassenger));
            newPassenger = Passenger("boarding", "escalatorDown0", escalatorLength);
            passengers.append(PassengerIdPair(newPassenger.id, newPassenger));
            passengersOnDownwardEscalator[0] += 2;
            currentPair = Pair(currentPair.Tick, currentPair.Count - 2);
    
    if(currentPair.Count > 0):
        for i in range(0, currentPair.Count):
            newPassenger = Passenger("boarding", "escalatorDownX", escalatorLength);
            passengers.append(PassengerIdPair(newPassenger.id, newPassenger));
    
    global passengersInLobby;
    UpdatePassengerCountOnLocations();

def HandleNewLandingPassengers(currentTick):
    global incomingMetroIndex;
    global metroAvailable;
    
    if(currentTick % metroFrequency != 0 or incomingMetroIndex > len(landing_passengers)):
        metroAvailable = False;
        return;
    
    newLandingPassengerCount = landing_passengers[incomingMetroIndex];
    metroAvailable = True;
    
    for i in range(0, newLandingPassengerCount):
        global passengers;
        newPassenger = Passenger("leaving", "metroIn", escalatorLength);
        passengers.append(PassengerIdPair(newPassenger.id, newPassenger));
    
    incomingMetroIndex += 1;
    UpdatePassengerCountOnLocations();

def UpdatePassengerCountOnLocations():
    for i in range(0, len(passengersOnDownwardEscalator)):
        passengersOnDownwardEscalator[i] = len(Passenger.GetPassengersByLocation("escalatorDown" + str(i)));
        passengersOnUpwardEscalator[i] = len(Passenger.GetPassengersByLocation("escalatorUp" + str(i)));
    
    global passengersInLobby;
    passengersInLobby = len(Passenger.GetPassengersByLocation("lobby"));
    global closeStation;
    if(passengersInLobby > lobbyCapacity):
        closeStation = True;
    global leftPassangers;
    leftPassangers = len(Passenger.GetPassengersByLocation("left"));
    global waitingBoardingPassengers;
    waitingBoardingPassengers = len(Passenger.GetPassengersByLocation("escalatorDownX"));
    global metroInPassengers;
    metroInPassengers = len(Passenger.GetPassengersByLocation("metroIn"));
    global metroOutPassengers;
    metroOutPassengers = len(Passenger.GetPassengersByLocation("metroOut"));

def HandleMoving():
    if(len(passengers) > 0):
        for id, passenger in passengers:
            if(passenger.position == "metroOut"):
                continue;
            elif(passenger.position == "escalatorDownX"):
                if(passengersOnDownwardEscalator[0] < 2):
                    passenger.Move();
            elif(passenger.position.startswith("escalatorDown") or passenger.position.startswith("escalatorUp")):
                passenger.Move();
            elif(passenger.position.startswith("lobby")):
                if(passenger.type.startswith("leaving")):
                    if(passengersOnUpwardEscalator[0] < 2):
                        passenger.Move();
                elif(passenger.type.startswith("boarding") and metroAvailable):
                    passenger.Move();
            elif(passenger.position.startswith("metroIn")):
                passenger.Move();
            UpdatePassengerCountOnLocations();

def StartSimulation():
    currentTick = 1;
    global closeStation;
    closeStation = False;
    FillEmptyEscalatorSpaces();
    
    while(currentTick <= boardingTickCount + escalatorLength + metroFrequency or closeStation):
        HandleMoving();
        HandleNewBoardingPassengers(currentTick);
        HandleNewLandingPassengers(currentTick);
        PrintTickInfo(currentTick);
        currentTick += 1;
        time.sleep(1);
        

#region Main
os.system('cls');
if(ReadInputFile()):
    # PrintStuffToConsole();
    StartSimulation();
#endregion Main