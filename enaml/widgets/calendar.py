#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import datetime

from traits.api import Date, Event, Instance, Property, TraitError

from .control import Control, IControlImpl
from ..util.trait_types import Bounded

class ICalendarImpl(IControlImpl):

    def parent_date_changed(self, obj, name, old_date, new_date):
        raise NotImplementedError

    def parent__minimum_date_changed(self, date):
        raise NotImplementedError

    def parent__maximum_date_changed(self, date):
        raise NotImplementedError


class Calendar(Control):
    """ A calendar widget.

    A Calendar displays a Python datetime.date using an appropriate
    toolkit specific control.

    Attributes
    ----------
    date : Bounded
        The currently selected date. This is only updated when the user
        *activates* the control via double-click or pressing enter. The
        value is bounded between :attr:`minimum_date` and :attr:`maximum_date`.
        Changing the boundary attributes might result in an update of
        :attr:`date` to fit in the new range. Attempts to assign a value outside
        of this range will result in a TraitError.

    minimum_date : Property(Date)
        The minimum date available in the date edit. If not defined then
        the default value is September 14, 1752. Extra checks take place to
        make sure that the user does not programmatically set
        :attr:`minimum_date` > :attr:`maximum_date`.

    maximum_date : Property(Date)
        The maximum date available in the date edit. If not defined then
        the default value is December 31, 7999. Extra checks take place to
        make sure that the user does not programmatically set
        :attr:`minimum_date` > :attr:`maximum_date`.

    selected : Event
        Triggered whenever the user clicks or changes the control. The
        event payload will be the date on the control. This is event is
        also fired when the value of :attr:`date` is set programmatically.

    activated : Event
        Triggered whenever the user activates a new date via double
        click or pressing enter. The event payload will be the date
        on the control.

    """
    minimum_date = Property(Date, depends_on ='_minimum_date')
    _minimum_date = Date(datetime.date(1752, 9, 14))

    maximum_date = Property(Date, depends_on ='_maximum_date')
    _maximum_date = Date(max(datetime.date(7999, 12, 31),
                            datetime.date.today()))

    date = Bounded(Date(datetime.date.today()),
                    low='minimum_date',
                    high='maximum_date')

    selected = Event

    activated = Event

    #---------------------------------------------------------------------------
    # Overridden parent traits
    #---------------------------------------------------------------------------
    toolkit_impl = Instance(ICalendarImpl)

    #---------------------------------------------------------------------------
    # Properties
    #---------------------------------------------------------------------------
    def _set_minimum_date(self, date):
        """ Set the minimum_date.

        Addtional checks are applied to make sure that
        :attr:`minimum_date` < :attr:`maximum_date`

        """
        if date > self._maximum_date:
            msg = ("The minimum date of Calendar should be smaller than the "
                   "current maximum date({0}), but a value of {1} was given ".\
                   format(self._maximum_date, date))
            raise TraitError(msg)
        self._minimum_date = date
        self._adapt_date()

    def _set_maximum_date(self, date):
        """ Set the maximum_date.

        Addtional checks are applied to make sure that
        :attr:`minimum_date` < :attr:`maximum_date`

        """
        if date < self._minimum_date:
            msg = ("The maximum date of Calendar should be larger than the "
                   "current minimum date({0}), but a value of {1} was given ".\
                   format(self._minimum_date, date))
            raise TraitError(msg)
        self._maximum_date = date
        self._adapt_date()

    def _get_maximum_date(self):
        """ The property getter for the Calendar maximum.

        """
        return self._maximum_date

    def _get_minimum_date(self):
        """ The property getter for the Calendar minimum.

        """
        return self._minimum_date

    # FIXME: I would like to have this method use the on_change decorator, but
    # it should not be run while the component is initialized so that an
    # exception is raised when the enaml source contains invalid values.
    def _adapt_date(self):
        """ Adapt the date to the bounderies

        """
        date = self.date
        date = max(date, self._minimum_date)
        date = min(date, self._maximum_date)
        self.date = date

Calendar.protect('selected', 'activated', 'minimum_date', '_minimum_date',
                 'maximum_date', '_maximum_date')
