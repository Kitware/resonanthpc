"""Data shared among all writers"""


class SharedData:
    """Singleton class"""

    _instance = None

    def __init__(self):
        """A singleton storing data to be shared across all writers.

        Recommended usage:
        from .shared_data import instance as shared
        """
        if self.__class__._instance is not None:
            raise RuntimeError("Invalid to instantiate SharedData more than once")
            self.__class__._instance = self

        self._checked_attributes = set()
        self._sim_atts = None
        self._warning_messages = list()
        self._xml_doc = None

    def initialize(self, sim_atts, xml_doc):
        """Configure data for next xml document."""
        self._checked_attributes.clear()
        self._sim_atts = sim_atts
        del self._warning_messages[:]
        self._xml_doc = xml_doc

    @property
    def checked_attributes(self):
        return self._checked_attributes

    @property
    def sim_atts(self):
        return self._sim_atts

    @property
    def warning_messages(self):
        return self._warning_messages

    @property
    def xml_doc(self):
        return self._xml_doc

    @property
    def ats_version(self):
        ats_info = self.sim_atts.findAttribute("ATS Information")
        return ats_info.find("ATS Version").value()


instance = SharedData()
