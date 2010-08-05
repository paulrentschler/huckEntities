from zope.i18nmessageid import MessageFactory
from Products.Archetypes import atapi
from Products.CMFCore import utils
from Products.CMFCore.permissions import setDefaultRoles

HuckEntitiesMessageFactory = MessageFactory('Products.HuckEntities')

import institute
import center
import graduate_program
import facility
import equipment

# TODO: do I need this?
ADD_PERMISSIONS = {
    'SimpleNewsItem': 'SimpleNewsItem: Add SimpleNewsItem',
    'CaseStudy': 'CaseStudy: Add CaseStudy'
}

PRODUCT_NAME = 'HuckEntities'

def initialize(context):
    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(PRODUCT_NAME),
        PRODUCT_NAME)

    for atype, constructor in zip(content_types, constructors):
        utils.ContentInit('%s: %s' % (PRODUCT_NAME, atype.portal_type),
            content_types      = (atype,),
            # TODO: do I need this next line?
            permission         = ADD_PERMISSIONS[atype.portal_type],
            extra_constructors = (constructor,),
            ).initialize(context)