import calendar

class TemporalObject(object):
    pass

class TimePoint(calendar.datetime, TemporalObject):
    pass

class TimeInterval(TemporalObject):
    
    def __init__(self, startTimePoint = None, endTimePoint = None):
        __start = startTimePoint
        __end = endTimePoint
        if (startTimePoint and endTimePoint):
            __duration = endTimePoint - startTimePoint
        