from datetime import datetime, date, time, timedelta
from decimal import Decimal as D
import time as time_
from uuid import uuid1, uuid4
from uuid import UUID as _UUID

class Property(object):
    def __init__(self, value):
        self.value = value

    def to_python(self):
        return self.value

    def to_database(self):
        return self.value

    def __repr__(self):
        return "atlas.Property: %s" % str(self.to_python())


class String(Property):
    def __repr__(self):
        return "atlas.String: %s" % str(self.to_python())


Text = String


class Integer(Property):

    def __init__(self, value):
        if isinstance(value, Integer):
            self.value = value
        else:
            self.value = value
    def to_python(self):
        return int(self.value)

    def __repr__(self):
        return "atlas.Integer: %s" % str(self.to_python())


class DateTime(Property):

    def to_python(self):
        if isinstance(self.value, datetime):
            return self.value
        else:
            return datetime.fromtimestamp(float(self.value))

    def to_database(self):
        tmp = time_.mktime(self.value.timetuple()) # gives us a float with .0
        # microtime is a 6 digit int, so we bring it down to .xxx and add it to the float TS
        tmp = tmp + float(self.value.microsecond) / 1000000
        return tmp

    def __repr__(self):
        return "atlas.DateTime: %s" % str(self.to_python())


class Date(Property):

    def to_python(self):
        if isinstance(self.value, date):
            return self.value
        else:
            return date.fromordinal(self.value)

    def to_database(self):
        tmp = self.value.toordinal()
        return tmp

    def __repr__(self):
        return "atlas.Date: %s" % str(self.to_python())


class Time(Property):

    def to_python(self):
        if isinstance(self.value, time):
            return self.value
        else:
            return datetime.fromtimestamp(float(self.value)).time()

    def to_database(self):
        since_epoch = datetime.fromtimestamp(time_.mktime(time_.gmtime(0)))
        value_ = datetime.combine(since_epoch, self.value) #to have a datetime equivalent we combine with the Epoch
        tmp = time_.mktime(value_.timetuple()) # gives us a float with .0
        # microtime is a 6 digit int, so we bring it down to .xxx and add it to the float TS
        tmp = tmp + float(self.value.microsecond) / 1000000
        return tmp

    def __repr__(self):
        return "atlas.Time: %s" % str(self.to_python())


class TimeDelta(Property):

    def to_python(self):
        if isinstance(self.value, timedelta):
            return self.value
        else:
            return timedelta(seconds = float(self.value))

    def to_database(self):
        tmp = self.value.total_seconds()
        return tmp

    def __repr__(self):
        return "atlas.TimeDelta: %s" % str(self.to_python())


class UUID(Property):
    def __init__(self, value = None):
        if value == None:
            value = str(uuid4())
        self.value = value

    def to_python(self):
        return str(self.value)

    def to_database(self):
        return str(self.value)

    def __repr__(self):
        return "atlas.UUID: %s" % str(self.to_python())


class Boolean(Property):

    def to_python(self):
        return bool(self.value)

    def to_database(self):
        return int(self.value)

    def __repr__(self):
        return "atlas.Boolean: %s" % str(self.to_python())


class Double(Property):

    def to_python(self):
        return float(self.value)

    def to_database(self):
        return float(self.value)

    def __repr__(self):
        return "atlas.Double: %s" % str(self.to_python())


Float = Double


class Decimal(Property):

    def to_python(self):
        return D(self.value)

    def to_database(self):
        return str(self.value)

    def __repr__(self):
        return "atlas.Decimal: %s" % str(self.to_python())


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
