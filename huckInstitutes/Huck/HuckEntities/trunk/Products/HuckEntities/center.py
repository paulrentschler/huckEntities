"""Definition of the Center content type
"""

from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder, schemata
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin

from Products.HuckEntities import HuckEntitiesMessageFactory as _
from Products.HuckEntities.interfaces import ICenter
from Products.HuckEntities.institute import InstituteSchema, Institute


CenterSchema = InstituteSchema.copy() + atapi.Schema((

))

schemata.finalizeATCTSchema(CenterSchema, moveDiscussion = False)

class Center(Institute):
    """A Center"""
    implements(ICenter)
    
    meta_type = "Center"
    schema = CenterSchema



atapi.registerType(Center, 'HuckEntities')
