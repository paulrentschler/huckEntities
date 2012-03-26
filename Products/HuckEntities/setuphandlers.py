import logging
logger = logging.getLogger('HuckEntities: setuphandlers')

import os
from Products.CMFCore.utils import getToolByName        


def isNotHuckEntitiesProfile(context):
    return context.readDataFile("huckentities_various.txt") is None


def importVersioningPolicy(context):
    """Set the versioning policy for our type(s)."""
    if isNotHuckEntitiesProfile(context):
        return
    return
    
def setupRelations(context):
    """Setup the Relations configuration."""
    if isNotHuckEntitiesProfile(context):
        return
    shortContext = context._profile_path.split(os.path.sep)[:-2]
    shortContext.append('relations.xml')
    xmlpath = os.path.sep.join(shortContext)

    relations_tool = getToolByName(context.getSite(), 'relations_library')

    try:
        f = open(xmlpath)
        xml = f.read()
        f.close()
        relations_tool.importXML(xml)
    except:
        print "File not found to import: %s\n" % xmlpath
