from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer

class IInstitute(Interface):
    """A research institute"""

class ICenter(Interface):
    """A center of excellence"""

class IGraduateProgram(Interface):
    """A graduate education program"""

class IFacility(Interface):
    """A facility that provides research instrumentation"""

class IEquipment(Interface):
    """A piece of research instrumentation"""

class IStartingPointLayer(IDefaultPloneLayer):
    """A Layer Specific to StartingPoint"""
    