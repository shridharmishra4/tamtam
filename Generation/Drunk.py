# Random:
# Randomly choose, within a certain range, a new next value
# arg 1: maxStepSize (negative value not allowed stepSize == 0)
# arg 2: maximum value allowed

import random

# TODO: replace magic numbers with constants
class Drunk:
    def __init__( self, maxValue ):
        self.lastValue = random.randint( 0, maxValue )

    def getNextValue( self, maxStepSize, maxValue ):
        if self.lastValue < 0 or self.lastValue > maxValue:
            return random.randint( 0, maxValue )

        direction = self.getDirection( maxValue )
        stepSize = self.getStepSize( direction, abs(maxStepSize), maxValue )
        
        if maxStepSize < 0:
            minStepSize = 1
        else:
            minStepSize = 0
  
        self.lastValue += direction * random.randint( minStepSize, stepSize )
        return self.lastValue

    def getDirection( self, maxValue ):
        if self.lastValue == 0:
            return 1
        elif self.lastValue == maxValue:
            return -1
        else:
            return random.choice( [ 1, -1 ] )

    def getStepSize( self, direction, maxStepSize, maxValue, ):
        if direction == -1:
            return min( maxStepSize, self.lastValue )
        else:
            return min( maxStepSize, maxValue - self.lastValue )

class DroneAndJump( Drunk ):
    def __init__( self, maxValue ):
        Drunk.__init__( self, maxValue )
        self.beforeLastValue = random.randint( 0, maxValue )
        self.lastValue = self.beforeLastValue + 1

    def getNextValue( self, maxStepSize, maxValue ):
        if self.beforeLastValue != self.lastValue:
            self.lastValue = self.beforeLastValue
            return self.beforeLastValue

        self.beforeLastValue = self.lastValue
        self.lastValue = Drunk.getNextValue( self, abs(maxStepSize), maxValue )
        return self.lastValue

    def getStepSize( self, direction, maxStepSize, maxValue ):
        if random.randint( 0, 100 ) < 25:
            return Drunk.getStepSize( self, direction, maxStepSize, maxValue )
        else:
            return Drunk.getStepSize( self, direction, 0, maxValue )

class Repeter( Drunk ):
    def __init__( self, maxValue ):
        Drunk.__init__( self, maxValue)
        self.lastValue = random.randint( 0, maxValue)

    def getNextValue( self, maxStepSize, maxValue ):
        self.lastValue = Drunk.getNextValue( self, abs(maxStepSize), maxValue )
        return self.lastValue

    def getStepSize( self, direction, maxStepSize, maxValue ):
        if random.randint( 0, 100 ) < 15:
            return Drunk.getStepSize( self, direction, maxStepSize, maxValue )
        else:
            return Drunk.getStepSize( self, direction, 0, maxValue )    

class Loopseg( Drunk ):
    def __init__( self, maxValue ):
        Drunk.__init__( self, maxValue )
        self.recordedValues = []
        self.recordState = 2
        self.recordPlayback = 0
        self.loopPlayback = 1
        self.recordLength = random.randint( 3, 6 ) 
        self.recordLoopTime = random.randint( 1, 4 )

    def getNextValue( self, maxStepSize, maxValue ):
        if self.recordState == 2:
            self.lastValue = Drunk.getNextValue( self, maxStepSize, maxValue )
            self.recordState = random.choice([2, 2, 2, 1])

        if len(self.recordedValues) != self.recordLength and self.recordState == 1:
            self.lastValue = Drunk.getNextValue( self, maxStepSize, maxValue )
            self.recordedValues.append( self.lastValue )
        elif self.recordState == 1 or self.recordState == 0:
            self.recordState = 0
            if self.recordPlayback < self.recordLength:
                self.loopAround()
            else:
                if self.loopPlayback < self.recordLoopTime:
                    self.recordPlayback = 0
                    self.loopPlayback += 1
                    self.loopAround()
                else:
                    self.recordedValues = []
                    self.recordState = 2
                    self.recordPlayback = 0
                    self.loopPlayback = 1
                    self.recordLength = random.randint( 3, 6 ) 
                    self.recordLoopTime = random.randint( 1, 4 )
                    self.lastValue = Drunk.getNextValue( self, maxStepSize, maxValue )
                    self.recordedValues = [self.lastValue]
        return self.lastValue  

    def loopAround( self ):
        self.lastValue = self.recordedValues[self.recordPlayback]
        self.recordPlayback += 1