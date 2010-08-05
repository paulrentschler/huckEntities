"""Definition of the Institute content type
"""

from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content import base, schemata
from Products.HuckEntities import HuckEntitiesMessageFactory as _
from Products.HuckEntities.interfaces import ICaseStudy
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin

InstituteSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    
    #TODO: fields to add: body, image, campus, outsideWebSiteUrl, contentOwner (relationship)
    atapi.TextField('institution',
        widget = atapi.StringWidget(
            label = _(u'Institution'),
            description = _(u'Name of the institution.'),
        ),
    ),
    
    atapi.DateTimeField('dateJoined',
        widget = atapi.CalendarWidget(
            label = _(u'Date Joined'),
            description = _(u'Date the institution joined our case study site.'),
        ),
    ),
    
    atapi.ImageField('screenshot',
        widget = atapi.ImageWidget(
            label = _(u'Screenshot'),
            description = _(u'Screenshot of the institution\'s web site.'),
        ),
    ),
    
    atapi.FixedPointField('moneySaved',
        widget = atapi.DecimalWidget(
            label = _(u'Money Saved'),
            description = _(u'Amount the institution has saved by switching to Plone.'),
        ),
    ),

    atapi.TextField('bodyText',
        widget = atapi.RichWidget(
            label = _(u'Body Text'),
            description = _(u'The text of the case study.'),
        ),
    ),

))

class Institute(base.ATCTContent, HistoryAwareMixin):
    """An Institute"""
    implements(IInstitute)

    meta_type = "Institute"
    schema = InstituteSchema

atapi.registerType(Institute, "HuckEntities")