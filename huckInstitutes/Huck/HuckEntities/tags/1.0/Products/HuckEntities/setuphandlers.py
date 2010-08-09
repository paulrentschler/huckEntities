import logging
logger = logging.getLogger('HuckEntities: setuphandlers')

import os
from Products.CMFCore.utils import getToolByName        
from Products.CMFEditions.setuphandlers import VERSIONING_ACTIONS, ADD_POLICIES, DEFAULT_POLICIES


def isNotHuckEntitiesProfile(context):
    return context.readDataFile("huckentities_various.txt") is None


def importVersioningPolicy(context):
    """Set the versioning policy for our type(s)."""
    if context.readDataFile('huckentities_various.txt') is None:
        return
    
    portal = context.getSite()
    portal_repository = getToolByName(portal, 'portal_repository')
    portal_repository.setAutoApplyMode(True)
    vtypes = portal_repository.getVersionableContentTypes()
    newTypes = ['Institute', 'Center', 'GraduateProgram', 'Facility', 'Equipment']
    for newType in newTypes:
        if newType not in vtypes:
            vtypes.append(newType)
            portal_repository.setVersionableContentTypes(vtypes)
        for policy_id in DEFAULT_POLICIES:
            portal_repository.addPolicyForContentType(newType, policy_id)


def setupRelations(context):
    """Setup the Relations configuration."""
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
