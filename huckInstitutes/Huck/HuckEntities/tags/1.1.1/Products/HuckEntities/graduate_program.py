"""Definition of the Graduate Program content type
"""

from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder, schemata
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin

from Products.HuckEntities import HuckEntitiesMessageFactory as _
from Products.HuckEntities.interfaces import IGraduateProgram
from Products.HuckEntities.institute import InstituteSchema, Institute


GraduateProgramSchema = InstituteSchema.copy() + atapi.Schema((

))

schemata.finalizeATCTSchema(GraduateProgramSchema, moveDiscussion = False)

class GraduateProgram(Institute):
    """A Graduate Program"""
    implements(IGraduateProgram)
    
    meta_type = "Graduate Program"
    schema = GraduateProgramSchema



atapi.registerType(GraduateProgram, 'HuckEntities')
