

class YawPitchSurvo:

    const float minDuty = 0.05f;
    const float maxDuty = 0.2f;
    const float normalDuty = 0.1f;

    PwmEmitter yawSurvoEmitter;
    PwmEmitter pitchSurvoEmitter;

    float _currentYawDuty = normalDuty;
    
    @currentYawDuty.getter
    def currentYawDuty(self)
        return self._currentYawDuty
    

    @currentYawDuty.setter
    def currentYawDuty(self, value)
        self._currentYawDuty = value
        if (self._currentYawDuty > maxDuty)
                self._currentYawDuty = maxDuty
        if (self._currentYawDuty < minDuty)
                self._currentYawDuty = minDuty



    float _currentPitchDuty = normalDuty;

    @currentPitchDuty.getter
    def currentPitchDuty(self)
        return self._currentPitchDuty

    @currentPitchDuty.setter
    def currentPitchDuty(self, value)
        self._currentPitchDuty = value
        if (self.currentPitchDuty > maxDuty)
            self.currentPitchDuty = maxDuty
        if (self.currentPitchDuty < minDuty)
            self.currentPitchDuty = minDuty



    def __init__ (	Action<bool,long> onYawEmit, Action<bool,long> onPitchEmit )
        yawSurvoEmitter = new PwmEmitter (onYawEmit)
        pitchSurvoEmitter = new PwmEmitter (onPitchEmit)

#		yawLarp = new FloatLerp( duty => Yaw(duty) );
#		pitchLerp = new FloatLerp( duty => Pitch(duty) );
    }

    def Dispose()
        yawSurvoEmitter.Dispose()
        pitchSurvoEmitter.Dispose()


    #region core methods
    def Yaw( float duty )
        currentYawDuty = duty
        yawSurvoEmitter.StartEmit (currentYawDuty)

    def Pitch( float duty )
        currentPitchDuty = duty
        pitchSurvoEmitter.StartEmit (currentPitchDuty)
    #endregion


    #region fixed control
    def FullYawRight()
        Yaw( minDuty )	# clockwise 90deg

    def NormalizeYaw()
        Yaw (normalDuty)

    def FullYawLeft()
        Yaw( maxDuty )	# anticlockwise 90deg


    def FullPitchUp()
        pitchSurvoEmitter.StartEmit( minDuty )	# clockwise 90deg


    def NromalizePitch()
        Pitch (normalDuty)


    def FullPitchDown()
        Pitch( maxDuty );	# anticlockwise 90deg


    def Fold()
        FullPitchDown ()
        NormalizeYaw ()

    #endregion

    #region step control
    const float stepDuty = 0.02f;

    def StepYawLeft( bool isSmooth )
        if (isSmooth)
            yawLarp.SetTarget ( currentYawDuty += stepDuty )
        else
            Yaw (currentYawDuty += stepDuty)


    def StepYawRight(bool isSmooth)
        if( isSmooth )
            yawLarp.SetTarget(currentYawDuty -= stepDuty)
        else		
            Yaw (currentYawDuty -= stepDuty)


    def StepPitchUp(bool isSmooth)
        if( isSmooth )
            pitchLerp.SetTarget(currentPitchDuty -= stepDuty)
        else
            Pitch (currentPitchDuty -= stepDuty)

    def StepPitchDown(self, bool isSmooth)
        if( isSmooth )
            pitchLerp.SetTarget(currentPitchDuty += stepDuty)
        else
            Pitch (currentPitchDuty += stepDuty)

    #endregion

    FloatLerp yawLarp
    FloatLerp pitchLerp
    def Update(self)
#		self.yawLarp.Update()
#		self.pitchLerp.Update()

  





class FloatLerp:

    float target
    float current

    Action<float> onCurrentChanged

    def __init__(Action<float> onCurrentChanged):
        this.onCurrentChanged = onCurrentChanged


    def SetTarget( float target ):
        this.target = target


    def Update():
        float rawDiff = target - current

        if (rawDiff == 0f):
            return

        print ( "hit!" )

        float diff = Math.Abs (rawDiff)
        float direction = diff / rawDiff	# -1 or 1 or 0 div

        print ( string.Format("diff {0} / rawDiff {1}",diff.ToString(), rawDiff.ToString()) )

        if( diff > 0.01f ):
            current = diff/2 * direction
            onCurrentChanged (current)







