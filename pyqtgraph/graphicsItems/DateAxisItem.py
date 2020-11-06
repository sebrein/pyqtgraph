<<<<<<< HEAD
import numpy as np
import time
from datetime import datetime
from .AxisItem import AxisItem

__all__ = ['DateAxisItem', 'ZoomLevel']
=======
import sys
import numpy as np
import time
from datetime import datetime, timedelta

from .AxisItem import AxisItem
from ..pgcollections import OrderedDict

__all__ = ['DateAxisItem']
>>>>>>> develop

MS_SPACING = 1/1000.0
SECOND_SPACING = 1
MINUTE_SPACING = 60
HOUR_SPACING = 3600
DAY_SPACING = 24 * HOUR_SPACING
WEEK_SPACING = 7 * DAY_SPACING
MONTH_SPACING = 30 * DAY_SPACING
YEAR_SPACING = 365 * DAY_SPACING

<<<<<<< HEAD
def getUtcFromTimestamp(val: float) -> datetime:
    try:
        ret = datetime.utcfromtimestamp(val)
    except:
        ret = datetime.utcfromtimestamp(0)
    return ret

def makeMSStepper(stepSize):
    def stepper(val, n):
=======
if sys.platform == 'win32':
    _epoch = datetime.utcfromtimestamp(0)
    def utcfromtimestamp(timestamp):
        return _epoch + timedelta(seconds=timestamp)
else:
    utcfromtimestamp = datetime.utcfromtimestamp

MIN_REGULAR_TIMESTAMP = (datetime(1, 1, 1) - datetime(1970,1,1)).total_seconds()
MAX_REGULAR_TIMESTAMP = (datetime(9999, 1, 1) - datetime(1970,1,1)).total_seconds()
SEC_PER_YEAR = 365.25*24*3600

def makeMSStepper(stepSize):
    def stepper(val, n):
        if val < MIN_REGULAR_TIMESTAMP or val > MAX_REGULAR_TIMESTAMP:
            return np.inf
        
>>>>>>> develop
        val *= 1000
        f = stepSize * 1000
        return (val // (n*f) + 1) * (n*f) / 1000.0
    return stepper

def makeSStepper(stepSize):
    def stepper(val, n):
<<<<<<< HEAD
=======
        if val < MIN_REGULAR_TIMESTAMP or val > MAX_REGULAR_TIMESTAMP:
            return np.inf
        
>>>>>>> develop
        return (val // (n*stepSize) + 1) * (n*stepSize)
    return stepper

def makeMStepper(stepSize):
    def stepper(val, n):
<<<<<<< HEAD
        d = getUtcFromTimestamp(val)
=======
        if val < MIN_REGULAR_TIMESTAMP or val > MAX_REGULAR_TIMESTAMP:
            return np.inf
        
        d = utcfromtimestamp(val)
>>>>>>> develop
        base0m = (d.month + n*stepSize - 1)
        d = datetime(d.year + base0m // 12, base0m % 12 + 1, 1)
        return (d - datetime(1970, 1, 1)).total_seconds()
    return stepper

def makeYStepper(stepSize):
    def stepper(val, n):
<<<<<<< HEAD
        d = getUtcFromTimestamp(val)
        next_date = datetime((d.year // (n*stepSize) + 1) * (n*stepSize), 1, 1)
        return (next_date - datetime(1970, 1, 1)).total_seconds()
    return stepper


=======
        if val < MIN_REGULAR_TIMESTAMP or val > MAX_REGULAR_TIMESTAMP:
            return np.inf
        
        d = utcfromtimestamp(val)
        next_year = (d.year // (n*stepSize) + 1) * (n*stepSize)
        if next_year > 9999:
            return np.inf
        next_date = datetime(next_year, 1, 1)
        return (next_date - datetime(1970, 1, 1)).total_seconds()
    return stepper

>>>>>>> develop
class TickSpec:
    """ Specifies the properties for a set of date ticks and computes ticks
    within a given utc timestamp range """
    def __init__(self, spacing, stepper, format, autoSkip=None):
        """
        ============= ==========================================================
        Arguments
        spacing       approximate (average) tick spacing
        stepper       a stepper function that takes a utc time stamp and a step
                      steps number n to compute the start of the next unit. You
                      can use the make_X_stepper functions to create common
                      steppers.
        format        a strftime compatible format string which will be used to
                      convert tick locations to date/time strings
        autoSkip      list of step size multipliers to be applied when the tick
                      density becomes too high. The tick spec automatically
                      applies additional powers of 10 (10, 100, ...) to the list
                      if necessary. Set to None to switch autoSkip off
        ============= ==========================================================

        """
        self.spacing = spacing
        self.step = stepper
        self.format = format
        self.autoSkip = autoSkip

    def makeTicks(self, minVal, maxVal, minSpc):
        ticks = []
        n = self.skipFactor(minSpc)
        x = self.step(minVal, n)
        while x <= maxVal:
            ticks.append(x)
            x = self.step(x, n)
        return (np.array(ticks), n)

    def skipFactor(self, minSpc):
        if self.autoSkip is None or minSpc < self.spacing:
            return 1
<<<<<<< HEAD
        factors = np.array(self.autoSkip)
=======
        factors = np.array(self.autoSkip, dtype=np.float)
>>>>>>> develop
        while True:
            for f in factors:
                spc = self.spacing * f
                if spc > minSpc:
<<<<<<< HEAD
                    return f
            factors *= 10


class ZoomLevel:
    """ Generates the ticks which appear in a specific zoom level """
    def __init__(self, tickSpecs):
=======
                    return int(f)
            factors *= 10
        

class ZoomLevel:
    """ Generates the ticks which appear in a specific zoom level """
    def __init__(self, tickSpecs, exampleText):
>>>>>>> develop
        """
        ============= ==========================================================
        tickSpecs     a list of one or more TickSpec objects with decreasing
                      coarseness
        ============= ==========================================================

        """
        self.tickSpecs = tickSpecs
        self.utcOffset = 0
<<<<<<< HEAD
        self.timestampOffset = 0
=======
        self.exampleText = exampleText
>>>>>>> develop

    def tickValues(self, minVal, maxVal, minSpc):
        # return tick values for this format in the range minVal, maxVal
        # the return value is a list of tuples (<avg spacing>, [tick positions])
        # minSpc indicates the minimum spacing (in seconds) between two ticks
        # to fullfill the maxTicksPerPt constraint of the DateAxisItem at the
        # current zoom level. This is used for auto skipping ticks.
        allTicks = []
        valueSpecs = []
        # back-project (minVal maxVal) to UTC, compute ticks then offset to
        # back to local time again
<<<<<<< HEAD
        utcMin = minVal - self.utcOffset + self.timestampOffset
        utcMax = maxVal - self.utcOffset + self.timestampOffset
        for spec in self.tickSpecs:
            ticks, skipFactor = spec.makeTicks(utcMin, utcMax, minSpc)
            # reposition tick labels to local time coordinates
            ticks += (self.utcOffset - self.timestampOffset)
=======
        utcMin = minVal - self.utcOffset
        utcMax = maxVal - self.utcOffset
        for spec in self.tickSpecs:
            ticks, skipFactor = spec.makeTicks(utcMin, utcMax, minSpc)
            # reposition tick labels to local time coordinates
            ticks += self.utcOffset
>>>>>>> develop
            # remove any ticks that were present in higher levels
            tick_list = [x for x in ticks.tolist() if x not in allTicks]
            allTicks.extend(tick_list)
            valueSpecs.append((spec.spacing, tick_list))
            # if we're skipping ticks on the current level there's no point in
            # producing lower level ticks
            if skipFactor > 1:
                break
        return valueSpecs


YEAR_MONTH_ZOOM_LEVEL = ZoomLevel([
    TickSpec(YEAR_SPACING, makeYStepper(1), '%Y', autoSkip=[1, 5, 10, 25]),
    TickSpec(MONTH_SPACING, makeMStepper(1), '%b')
<<<<<<< HEAD
])
MONTH_DAY_ZOOM_LEVEL = ZoomLevel([
    TickSpec(MONTH_SPACING, makeMStepper(1), '%b'),
    TickSpec(DAY_SPACING, makeSStepper(DAY_SPACING), '%d', autoSkip=[1, 5])
])
DAY_HOUR_ZOOM_LEVEL = ZoomLevel([
    TickSpec(DAY_SPACING, makeSStepper(DAY_SPACING), '%a %d'),
    TickSpec(HOUR_SPACING, makeSStepper(HOUR_SPACING), '%H:%M', autoSkip=[1, 6])
])
=======
], "YYYY")
MONTH_DAY_ZOOM_LEVEL = ZoomLevel([
    TickSpec(MONTH_SPACING, makeMStepper(1), '%b'),
    TickSpec(DAY_SPACING, makeSStepper(DAY_SPACING), '%d', autoSkip=[1, 5])
], "MMM")
DAY_HOUR_ZOOM_LEVEL = ZoomLevel([
    TickSpec(DAY_SPACING, makeSStepper(DAY_SPACING), '%a %d'),
    TickSpec(HOUR_SPACING, makeSStepper(HOUR_SPACING), '%H:%M', autoSkip=[1, 6])
], "MMM 00")
>>>>>>> develop
HOUR_MINUTE_ZOOM_LEVEL = ZoomLevel([
    TickSpec(DAY_SPACING, makeSStepper(DAY_SPACING), '%a %d'),
    TickSpec(MINUTE_SPACING, makeSStepper(MINUTE_SPACING), '%H:%M',
             autoSkip=[1, 5, 15])
<<<<<<< HEAD
])
HMS_ZOOM_LEVEL = ZoomLevel([
    TickSpec(SECOND_SPACING, makeSStepper(SECOND_SPACING), '%H:%M:%S',
             autoSkip=[1, 5, 15, 30])
])
=======
], "MMM 00")
HMS_ZOOM_LEVEL = ZoomLevel([
    TickSpec(SECOND_SPACING, makeSStepper(SECOND_SPACING), '%H:%M:%S',
             autoSkip=[1, 5, 15, 30])
], "99:99:99")
>>>>>>> develop
MS_ZOOM_LEVEL = ZoomLevel([
    TickSpec(MINUTE_SPACING, makeSStepper(MINUTE_SPACING), '%H:%M:%S'),
    TickSpec(MS_SPACING, makeMSStepper(MS_SPACING), '%S.%f',
             autoSkip=[1, 5, 10, 25])
<<<<<<< HEAD
])


class DateAxisItem(AxisItem):
    """ An AxisItem that displays dates from unix timestamps

    The display format is adjusted automatically depending on the current time
    density (seconds/point) on the axis.
    You can customize the behaviour by specifying a different set of zoom levels
    than the default one. The zoomLevels variable is a dictionary with the
    maximum number of seconds/point which are allowed for each ZoomLevel
    before the axis switches to the next coarser level.

    """

    def __init__(self, orientation, **kvargs):
        """
        ==============  ===============================================================
        **Arguments:**
        orientation     one of 'left', 'right', 'top', or 'bottom'

        **Handled Keyword arguments:**
        date_offset     Timestamp to add to the date before building tickStrings. The
                        same value has to be subtracted from x values of the plot.
                        This is usefull for single-precision floating point renderer
                        (like opengl) to increase the effective resolution (see
                        https://en.wikipedia.org/wiki/IEEE_754).

        **kargs          All extra keyword arguments become CSS style options for
                        the <span> tag which will surround the axis label and units.
        ==============  ===============================================================
        """

        super(DateAxisItem, self).__init__(orientation, **kvargs)
        self.timestampOffset = 0
        if 'date_offset' in kvargs:
            self.timestampOffset = kvargs['date_offset']
        self.utcOffset = time.timezone
        # Set the zoom level to use depending on the time density on the axis
        self.zoomLevel = YEAR_MONTH_ZOOM_LEVEL
        # we need about 60pt for our largest label
        self.maxTicksPerPt = 1/60.0
        self.zoomLevels = {
            self.maxTicksPerPt:               MS_ZOOM_LEVEL,
            30 * self.maxTicksPerPt:          HMS_ZOOM_LEVEL,
            15 * 60 * self.maxTicksPerPt:     HOUR_MINUTE_ZOOM_LEVEL,
            6 * 3600 * self.maxTicksPerPt:    DAY_HOUR_ZOOM_LEVEL,
            5 * 3600*24 * self.maxTicksPerPt: MONTH_DAY_ZOOM_LEVEL,
            3600*24*30 * self.maxTicksPerPt:  YEAR_MONTH_ZOOM_LEVEL
        }

    def tickStrings(self, values, scale, spacing):
        tickSpecs = self.zoomLevel.tickSpecs
        tickSpec = next((s for s in tickSpecs if s.spacing == spacing), None)
        dates = [datetime.utcfromtimestamp(v + self.timestampOffset - self.utcOffset) for v in values]
        formatStrings = []
        for x in dates:
            try:
                if '%f' in tickSpec.format:
                    # we only support ms precision
                    formatStrings.append(x.strftime(tickSpec.format)[:-3])
                else:
                    formatStrings.append(x.strftime(tickSpec.format))
=======
], "99:99:99")

class DateAxisItem(AxisItem):
    """
    **Bases:** :class:`AxisItem <pyqtgraph.AxisItem>`
    
    An AxisItem that displays dates from unix timestamps.

    The display format is adjusted automatically depending on the current time
    density (seconds/point) on the axis. For more details on changing this
    behaviour, see :func:`setZoomLevelForDensity() <pyqtgraph.DateAxisItem.setZoomLevelForDensity>`.
    
    Can be added to an existing plot e.g. via 
    :func:`setAxisItems({'bottom':axis}) <pyqtgraph.PlotItem.setAxisItems>`.

    """

    def __init__(self, orientation='bottom', **kwargs):
        """
        Create a new DateAxisItem.
        
        For `orientation` and `**kwargs`, see
        :func:`AxisItem.__init__ <pyqtgraph.AxisItem.__init__>`.
        
        """

        super(DateAxisItem, self).__init__(orientation, **kwargs)
        # Set the zoom level to use depending on the time density on the axis
        self.utcOffset = time.timezone
        
        self.zoomLevels = OrderedDict([
            (np.inf,      YEAR_MONTH_ZOOM_LEVEL),
            (5 * 3600*24, MONTH_DAY_ZOOM_LEVEL),
            (6 * 3600,    DAY_HOUR_ZOOM_LEVEL),
            (15 * 60,     HOUR_MINUTE_ZOOM_LEVEL),
            (30,          HMS_ZOOM_LEVEL),
            (1,           MS_ZOOM_LEVEL),
            ])
    
    def tickStrings(self, values, scale, spacing):
        tickSpecs = self.zoomLevel.tickSpecs
        tickSpec = next((s for s in tickSpecs if s.spacing == spacing), None)
        try:
            dates = [utcfromtimestamp(v - self.utcOffset) for v in values]
        except (OverflowError, ValueError, OSError):
            # should not normally happen
            return ['%g' % ((v-self.utcOffset)//SEC_PER_YEAR + 1970) for v in values]
            
        formatStrings = []
        for x in dates:
            try:
                s = x.strftime(tickSpec.format)
                if '%f' in tickSpec.format:
                    # we only support ms precision
                    s = s[:-3]
                elif '%Y' in tickSpec.format:
                    s = s.lstrip('0')
                formatStrings.append(s)
>>>>>>> develop
            except ValueError:  # Windows can't handle dates before 1970
                formatStrings.append('')
        return formatStrings

    def tickValues(self, minVal, maxVal, size):
        density = (maxVal - minVal) / size
        self.setZoomLevelForDensity(density)
<<<<<<< HEAD
        minSpacing = density / self.maxTicksPerPt
        values = self.zoomLevel.tickValues(minVal, maxVal, minSpc=minSpacing)
        return values

    def setZoomLevelForDensity(self, density):
        keys = sorted(self.zoomLevels.keys())
        key = next((k for k in keys if density < k), keys[-1])
        self.zoomLevel = self.zoomLevels[key]
        self.zoomLevel.utcOffset = self.utcOffset
        self.zoomLevel.timestampOffset = self.timestampOffset
=======
        values = self.zoomLevel.tickValues(minVal, maxVal, minSpc=self.minSpacing)
        return values

    def setZoomLevelForDensity(self, density):
        """
        Setting `zoomLevel` and `minSpacing` based on given density of seconds per pixel
        
        The display format is adjusted automatically depending on the current time
        density (seconds/point) on the axis. You can customize the behaviour by 
        overriding this function or setting a different set of zoom levels
        than the default one. The `zoomLevels` variable is a dictionary with the
        maximal distance of ticks in seconds which are allowed for each zoom level
        before the axis switches to the next coarser level. To customize the zoom level
        selection, override this function.
        """
        padding = 10
        
        # Size in pixels a specific tick label will take
        if self.orientation in ['bottom', 'top']:
            def sizeOf(text):
                return self.fontMetrics.boundingRect(text).width() + padding*self.fontScaleFactor
        else:
            def sizeOf(text):
                return self.fontMetrics.boundingRect(text).height() + padding*self.fontScaleFactor
        
        # Fallback zoom level: Years/Months
        self.zoomLevel = YEAR_MONTH_ZOOM_LEVEL
        for maximalSpacing, zoomLevel in self.zoomLevels.items():
            size = sizeOf(zoomLevel.exampleText)

            # Test if zoom level is too fine grained
            if maximalSpacing/size < density:
                break
            
            self.zoomLevel = zoomLevel
        
        # Set up zoomLevel
        self.zoomLevel.utcOffset = self.utcOffset
        
        # Calculate minimal spacing of items on the axis
        size = sizeOf(self.zoomLevel.exampleText)
        self.minSpacing = density*size
        
    def linkToView(self, view):
        super(DateAxisItem, self).linkToView(view)
        
        # Set default limits
        _min = MIN_REGULAR_TIMESTAMP
        _max = MAX_REGULAR_TIMESTAMP
        
        if self.orientation in ['right', 'left']:
            view.setLimits(yMin=_min, yMax=_max)
        else:
            view.setLimits(xMin=_min, xMax=_max)
        
    def generateDrawSpecs(self, p):
        # Get font metrics from QPainter
        # Not happening in "paint", as the QPainter p there is a different one from the one here,
        # so changing that font could cause unwanted side effects
        if self.style['tickFont'] is not None:
            p.setFont(self.style['tickFont'])
        
        self.fontMetrics = p.fontMetrics()
        
        # Get font scale factor by current window resolution
        self.fontScaleFactor = p.device().logicalDpiX() / 96
        
        return super(DateAxisItem, self).generateDrawSpecs(p)
>>>>>>> develop
