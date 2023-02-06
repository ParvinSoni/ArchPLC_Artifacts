class Centroid(object):

    def _initialize_instance_fields(self):
        self.__coordinates = []
        self.__roundedCoordinates = []
        self.__centroidRule = ""
        self.__hasBeenPrinted = False
        self.__numOccurrences = 0
        self.__support = 0
        self.__confidence = 0


    def __init__(self, *args):
        if len(args) == 0:
            self._initialize_instance_fields()
            
            self.__coordinates = []
            self.__roundedCoordinates = []
            self.__hasBeenPrinted = False
            
            self.initSuppConf()
        if len(args) == 1:
            myCoordinates = args[0]
            self._initialize_instance_fields()
            self.__coordinates = []
            self.__roundedCoordinates = []
            self.__hasBeenPrinted = False
            i = 0
            while i<len(myCoordinates):
                self.__coordinates.append(myCoordinates[i])
                i += 1
            self.setRoundedCoordinates(self.__coordinates)
            self.initSuppConf()

            #############

            # self._initialize_instance_fields()
            # self.__coordinates = []
            # self.__roundedCoordinates = []
            # self.__coordinates = myCoordinates
            # self.setRoundedCoordinates(self.__coordinates)
            # self.__hasBeenPrinted = False
            # self.initSuppConf()

    def initSuppConf(self):
        self.__numOccurrences = 0
        self.__support = 0
        self.__confidence = 0

    def getCoordinates(self):
        return self.__coordinates

    def setRoundedCoordinates(self, myCoordinates):

        i = 0
        while i<len(myCoordinates):
            coordinate = myCoordinates[i]
            if isinstance(coordinate, float):
                numToAdd = (round(float(myCoordinates[i]) * 10)) / 10.0
                self.__roundedCoordinates.append(numToAdd)
            elif isinstance(coordinate, Double):
                numToAdd = (round(float(myCoordinates[i]) * 10)) / 10.0
                self.__roundedCoordinates.append(numToAdd)

            i += 1


    def getRoundedCoordinates(self):
        return self.__roundedCoordinates



    def setCoordinates(self, newCoordinates):
        if len(newCoordinates) >= len(self.__coordinates):
            i = 0
            while i<len(newCoordinates):
                self.__coordinates[i] = self.__coordinates
                i += 1

        self.setRoundedCoordinates(self.__coordinates)


    def toString(self):

        returnString = "Centroid cordinates: ["

        i = 0
        while i<len(self.__coordinates):
            returnString += self.__coordinates[i]
            if i != len(self.__coordinates) - 1:
                returnString += ", "
            i += 1

        returnString += "]"

        return returnString

    def setCentroidRule(self, newCentroidRule):
        self.__centroidRule = newCentroidRule

    def getCentroidRule(self):
        return self.__centroidRule

    def setHasBeenPrinted(self, hasBeen):
        self.__hasBeenPrinted = hasBeen

    def getHasBeenPrinted(self):
        return self.__hasBeenPrinted

    def setNumOccurrences(self, amount):
        self.__numOccurrences = amount

    def setSupport(self, mySupport):
        self.__support = mySupport

    def setConfidence(self, myConfidence):
        self.__confidence = myConfidence

    def getNumOccurrences(self):
        return self.__numOccurrences

    def getSupport(self):
        return self.__support

    def getConfidence(self):
        return self.__confidence

    #coordinates have elements = each i, i+1 pair (i even) is min and max of interval (i.e. x, y coordinate pair)
    #coordinates has float values, for precision for Euclidean Algorithm calculations
    #roundedCoordinates has double values, for rounded for printing out - rounded coordinates for a centroid



