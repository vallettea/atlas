from datetime import datetime, date, time, timedelta
from decimal import Decimal as D
import time as time_
from uuid import uuid1, uuid4
from uuid import UUID as _UUID


class String(object):

    def __init__(self, value):
        if isinstance(value, unicode):
            value = value.encode(self.encoding)
        self.value = value
    def to_python(self):
        return self.value
    def to_database(self):
        return "'" + self.value + "'"

Text = String

class Integer(object):

    def __init__(self, value):
        self.value = long(value)
    def to_python(self):
        return self.value
    def to_database(self):
        return self.value


class DateTime(object):

    def __init__(self, value):
        self.value = value
    def to_python(self):
        return datetime.fromtimestamp(float(self.value))

    def to_database(self):
        tmp = time_.mktime(self.value.timetuple()) # gives us a float with .0
        # microtime is a 6 digit int, so we bring it down to .xxx and add it to the float TS
        tmp = tmp + float(self.value.microsecond) / 1000000
        return tmp

class Date(object):

    def __init__(self, value):
        self.value = value

    def to_python(self):
        return date.fromordinal(self.value)

    def to_database(self):
        tmp = self.value.toordinal()
        return long(tmp)

class Time(object):

    def __init__(self, value):
        self.value = value

    def to_python(self):
        return datetime.fromtimestamp(float(self.value)).time()

    def to_database(self):
        since_epoch = datetime.fromtimestamp(time_.mktime(time_.gmtime(0)))
        value_ = datetime.combine(since_epoch, self.value) #to have a datetime equivalent we combine with the Epoch
        tmp = time_.mktime(value_.timetuple()) # gives us a float with .0
        # microtime is a 6 digit int, so we bring it down to .xxx and add it to the float TS
        tmp = tmp + float(self.value.microsecond) / 1000000
        return tmp

class TimeDelta(object):

    def __init__(self, value):
        self.value = value

    def to_python(self):
        return timedelta(seconds = float(self.value))

    def to_database(self):
        tmp = self.value.total_seconds()
        return tmp

class UUID(object):
    def __init__(self, value = None):
        if value == None:
            value = str(uuid4())
        self.value = value

    def to_python(self):
        return str(self.value)

    def to_database(self):
        return "'" + str(self.value) + "'"


class Boolean(object):
    def __init__(self, value):
        self.value = value

    def to_python(self):
        return bool(self.value)

    def to_database(self):
        return int(self.value)


class Double(object):

    def __init__(self, value):
        self.value = value

    def to_python(self):
        return float(self.value)

    def to_database(self):
        return float(self.value)

Float = Double

class Decimal(object):
    def __init__(self, value):
        self.value = value

    def to_python(self):
        return D(self.value)

    def to_database(self):
        return str(self.value)


# dictionnay that makes the correspondance

label_type = {"string" : String,
              "text" : Text,
              "integer" : Integer,
              "datetime" : DateTime,
              "date" : Date,
              "time" : Time,
              "timedelta" : TimeDelta,
              "uuid" : UUID,
              "boolean" : Boolean,
              "double" : Double,
              "float" : Float,
              "decimal" : Decimal
              }
