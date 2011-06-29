"""Definition of the Equipment content type
"""

from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content import base, schemata
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.Relations.field import RelationField

from Products.HuckEntities import HuckEntitiesMessageFactory as _
from Products.HuckEntities.interfaces import IEquipment, IFacility

from Products.CMFCore.permissions import View, ModifyPortalContent
from AccessControl import ClassSecurityInfo


EquipmentSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.LinesField(
        name = 'equipmentType',
        required = True,
        searchable = True,
        widget = atapi.SelectionWidget(
            label = _(u'Equipment Type'),
            format = 'select',
        ),
        vocabulary = [ '-- Other --',
                       'Arrayer',
                       'Bioanalyzer',
                       'Bioreactor',
                       'Cell Sorter',
                       'Centrifuge',
                       'Confocal microscope',
                       'Cytometer',
                       'DNA sequencer',
                       'Electron microscope (scanning)',
                       'Electron microscope (transmission)',
                       'Fermentor',
                       'Fraction collector',
                       'High Protein Liquid Chromatography (HPLC) System'
                       'Homogenizer / Pump',
                       'Magnetic resonance imager',
                       'Mass Spectrometer',
                       'Microarrays',
                       'Microfluidizer processor',
                       'Microscope',
                       'Multiplex Bioassays',
                       'Research console',
                       'Robotics',
                       'X-ray crystallography',
                     ],
    ),
    
    atapi.LinesField(
        name = 'specifications',
        searchable = True,
        required = False,
        widget = atapi.LinesWidget(
            label = _(u'Specifications'),
            description = _(u'A list of equipment specs, one per line.'),
        ),
    ),
    
    atapi.LinesField(
        name = 'uses',
        searchable = True,
        required = False,
        widget = atapi.LinesWidget(
            label = _(u'Uses'),
            description = _(u'A list of uses for the equipment, one per line.'),
        ),
    ),

    atapi.TextField(
        name = 'body',
        required = False,
        searchable = True,
        default_output_type = 'text/x-html-safe',
        widget = atapi.RichWidget(
            label = _(u'Body Text'),
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
        name='externalUsers',
        required=True,
        searchable=False,
        widget = atapi.SelectionWidget(
            label = _(u'Available for non-facility employee use?'),
            description = _(u'Can researchers who do not work in the facility come in and use this piece of equipment? Will not be displayed if you select "Not sure."'),
        ),
        vocabulary = [ 
                       ('Not sure', 'Not sure (nothing displayed on page)'),
                       ('Yes', 'Yes, non-facility employees can use this instrument' ),
                       ('No', 'No, only facility employees can use this instrument')
                     ],
    ),

    RelationField(
        name = 'replacementEquipment',
        required = False,
        searchable = False,
        widget = ReferenceBrowserWidget(
            label = _(u'Replacement'),
            description = _(u'Select the piece of equipment that replaces this one.'),
            base_query = "_search_equipment",
            allow_browse = 1,
            allow_search = 1,
            show_results_without_query = 1,
            startup_directory_method = "_get_equipment_path",
        ),
        allowed_types = ('Equipment'),
        multiValued = False,
        relationship = 'FacilityEquipmentReplacementEquipment',
    ),

))

schemata.finalizeATCTSchema(EquipmentSchema, moveDiscussion=False)
EquipmentSchema['title'].widget.label = _(u'Model Number')
EquipmentSchema.moveField('equipmentType', after='title')

class Equipment(base.ATCTOrderedFolder):
    """A piece of equipment"""
    implements(IEquipment)

    meta_type = "Equipment"
    schema = EquipmentSchema
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

        return base.ATCTContent.__bobo_traverse__(self, REQUEST, name)

    security.declarePublic('getReplacementEquipment')
    def getReplacementEquipment(self):
        """Returns the referenced equipment that replaces this one
           """
        return self.getReferences(relationship='FacilityEquipmentReplacementEquipment')

    security.declarePublic('getParentFacility')
    def getParentFacility(self):
        """Traverse up the tree structure until a parent object of type Facility is found.
           Return None if a Facility is not found.
        """
        parent = self.aq_parent
        while not IFacility.providedBy(parent):
            try:
                parent = parent.aq_parent
            except AttributeError:
                parent = None
                break;
                
        return parent

    ###
    # Methods to limit the referenceBrowserWidget start directory and search results    
    security.declareProtected(ModifyPortalContent, '_search_equipment')
    def _search_equipment(self):
        """Return a query dictionary to limit the search parameters for a reference browser
           widget query. Search only for Equipment.
           """
        return {'portal_type': 'Equipment',
                'sort_on': 'sortable_title'}

    security.declareProtected(ModifyPortalContent, '_get_equipment_path')
    def _get_equipment_path(self):
        """Return the path to the object's parent
           """
        return '/'.join(self.getPhysicalPath())


atapi.registerType(Equipment, 'HuckEntities')

