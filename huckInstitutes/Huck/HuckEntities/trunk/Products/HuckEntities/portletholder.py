"""Definition of the Portlet Holder content type
"""

from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content import base, schemata
from Products.ATContentTypes.configuration import zconf

from Products.HuckEntities import HuckEntitiesMessageFactory as _
from Products.HuckEntities.interfaces import IPortletHolder

from Products.CMFCore.permissions import View, ModifyPortalContent
from AccessControl import ClassSecurityInfo


PortletHolderSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

))

class PortletHolder(base.ATCTContent):
    """A portlet holder"""
    implements(IPortletHolder)

    meta_type = "Portlet Holder"
    schema = PortletHolderSchema
    security = ClassSecurityInfo()

    def Title(self):
        return self.aq_parent.Title()
        
    def Description(self):
        return self.aq_parent.Description()
        
    def getBody(self):
        return self.aq_parent.getBody()
        
    def getImage(self):
        return self.aq_parent.getImage()
        
    def getImageCaption(self):
        return self.aq_parent.getImageCaption()
        
    def getCampus(self):
        return self.aq_parent.getCampus()
        
    def getAlternateWebSiteUrl(self):
        return self.aq_parent.getAlternateWebSiteUrl()
        
    def getContentOwners(self):
        return self.aq_parent.getContentOwners()
        

atapi.registerType(PortletHolder, 'HuckEntities')