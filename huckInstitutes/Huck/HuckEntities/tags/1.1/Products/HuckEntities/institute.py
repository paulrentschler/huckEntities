"""Definition of the Institute content type
"""

from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder, schemata
from Products.ATContentTypes.configuration import zconf
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.Relations.field import RelationField
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin

from Products.HuckEntities import HuckEntitiesMessageFactory as _
from Products.HuckEntities.interfaces import IInstitute

from Products.CMFCore.permissions import View, ModifyPortalContent
from AccessControl import ClassSecurityInfo


InstituteSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    
    atapi.TextField(
        name = 'body',
        required = False,
        searchable = True,
        validators = ('isTidyHtmlWithCleanup',),
        default_output_type = 'text/x-html-safe',
        widget = atapi.RichWidget(
            label = _(u'Body Text'),
            rows = 25,
            allow_file_upload = zconf.ATDocument.allow_document_upload
        ),
    ),

    atapi.ImageField(
        name = 'image',
        required = False,
        searchable = False,
        original_size = (768, 768),
        sizes = { 'large'       : (768, 768),
                  'preview'     : (400, 400),
                  'mediumLarge' : (350, 350),
                  'medium'      : (300, 300),
                  'small'       : (250, 250),
                  'mini'        : (200, 200),
                  'thumb'       : (128, 128),
                  'tile'        : (64, 64),
                  'icon'        : (32, 32),
                  'listing'     : (16, 16),
        },
        widget=atapi.ImageWidget(
            label = _(u'Image'),
            description = _(u'Will be shown in listings and on the page. Image will be scaled to a sensible size.'),
        ),
    ),
    
    atapi.StringField(
        name = 'imageCaption',
        required = False,
        searchable = False,
        widget = atapi.StringWidget(
            label = _(u'Image Caption'),
        ),
    ),

    atapi.StringField(
        name = 'campus',
        required = False,
        searchable = False,
        widget = atapi.MultiSelectionWidget(
            label = _(u'Campus'),
            description = _(u'Indicate the campus or campuses supported.'),
            format = 'checkbox',
        ),
        enforceVocabulary = True,
        vocabulary = [ 'University Park', 'Hershey' ],
    ),
    
    atapi.StringField(
        name = 'alternateWebSiteUrl',
        required = False,
        searchable = False,
        write_permission="Manage Site",
        widget = atapi.StringWidget(
            label = _(u'Alternate Web Site Address'),
            description = _(u'Web site to redirect users two instead of showing a locally hosted site.')
        ),
    ),
    
    RelationField(
        name = 'contentOwners',
        required = False,
        searchable = False,
        write_permission="Manage Site",
        widget = ReferenceBrowserWidget(
            label = _(u'Content Owners'),
            description = _(u'Indicate the people who have ownership over this area of the site.'),
            base_query = "_search_people_in_fsd",
            allow_browse = 0,
            allow_search = 1,
            show_results_without_query = 1,
            startup_directory_method = "_get_parent_fsd_path",
        ),
        allowed_types = ('FSDPerson'),
        multiValued = True,
        relationship = 'EntityContentOwners',
    ),

))

class Institute(folder.ATFolder, HistoryAwareMixin):
    """An Institute"""
    implements(IInstitute)

    meta_type = "Institute"
    schema = InstituteSchema
    security = ClassSecurityInfo()

    security.declareProtected(View, 'tag')
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        if 'title' not in kwargs:
            kwargs['title'] = self.getImageCaption()
        return self.getField('image').tag(self, **kwargs)

    def __bobo_traverse__(self, REQUEST, name):
        """Transparent access to image scales
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image

        return folder.ATFolder.__bobo_traverse__(self, REQUEST, name)

    ###
    # Methods to limit the referenceBrowserWidget start directory and search results    
    security.declareProtected(ModifyPortalContent, '_get_parent_fsd_path')
    def _get_parent_fsd_path(self):
        """ return the path to the Faculty Staff Directory object
        """
        # This method is taken from FSD 2.x
        fsd = self.portal_catalog(portal_type='FSDFacultyStaffDirectory')
        return '/'.join(fsd[0].getObject().getPhysicalPath())

    security.declareProtected(ModifyPortalContent, '_search_people_in_fsd')
    def _search_people_in_fsd(self):
        """ return a query dictionary to limit the search parameters for a reference browser
            widget query. Search only the FSD for only people.
        """
        # This method is taken from FSD 2.x
        path = self._get_parent_fsd_path()
        return {'portal_type': 'FSDPerson',
                'sort_on': 'sortable_title',
                'path': {'query': path}}



atapi.registerType(Institute, 'HuckEntities')