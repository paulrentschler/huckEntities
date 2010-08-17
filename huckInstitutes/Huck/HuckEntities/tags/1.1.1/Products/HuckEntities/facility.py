"""Definition of the Facility content type
"""

from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder, schemata
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin

from Products.HuckEntities import HuckEntitiesMessageFactory as _
from Products.HuckEntities.interfaces import IFacility
from Products.HuckEntities.institute import InstituteSchema, Institute


FacilitySchema = InstituteSchema.copy() + atapi.Schema((

))

schemata.finalizeATCTSchema(FacilitySchema, moveDiscussion = False)

class Facility(Institute):
    """A Facility"""
    implements(IFacility)
    
    meta_type = "Facility"
    schema = FacilitySchema



atapi.registerType(Facility, 'HuckEntities')
