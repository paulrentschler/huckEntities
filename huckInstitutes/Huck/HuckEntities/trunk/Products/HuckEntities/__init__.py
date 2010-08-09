from zope.i18nmessageid import MessageFactory
from Products.Archetypes import atapi
from Products.CMFCore import utils
from Products.CMFCore.permissions import setDefaultRoles
from Products.CMFCore.DirectoryView import registerDirectory


# Define a message factory for when this product is internationalised.
# This will be imported with the special name "_" in most modules. Strings
# like _(u"message") will then be extracted by i18n tools for translation.
HuckEntitiesMessageFactory = MessageFactory('Products.HuckEntities')


registerDirectory('skins', globals())


import institute
import center
import graduate_program
import facility
import equipment


DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))

ADD_PERMISSIONS = {
    'Institute': DEFAULT_ADD_CONTENT_PERMISSION,
    'Center' : DEFAULT_ADD_CONTENT_PERMISSION,
    'GraduateProgram' : DEFAULT_ADD_CONTENT_PERMISSION,
    'Facility' : DEFAULT_ADD_CONTENT_PERMISSION,
    'Equipment' : DEFAULT_ADD_CONTENT_PERMISSION,
}

PRODUCT_NAME = 'HuckEntities'

def initialize(context):
    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(PRODUCT_NAME),
        PRODUCT_NAME)

    for atype, constructor in zip(content_types, constructors):
        utils.ContentInit('%s: %s' % (PRODUCT_NAME, atype.portal_type),
            content_types      = (atype,),
            permission         = ADD_PERMISSIONS[atype.portal_type],
            extra_constructors = (constructor,),
            ).initialize(context)
