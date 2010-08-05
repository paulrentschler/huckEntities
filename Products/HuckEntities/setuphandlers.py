from Products.CMFCore.utils import getToolByName        
from Products.CMFEditions.setuphandlers import VERSIONING_ACTIONS, ADD_POLICIES, DEFAULT_POLICIES

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
