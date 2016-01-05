"""Contains classes for TimeML tags.

Author: Roser
Last Modified: April 14, 2005

NOT YET PROPERLY DOCUMENTED
"""


from library.timeMLspec import EVENT, INSTANCE, TIMEX, ALINK, SLINK, TLINK
from library.timeMLspec import EID, EIID, EVENTID
from library.timeMLspec import CLASS, TENSE, ASPECT, EPOS, MOD, POL, FORM, STEM, POS
from components.common_modules.constituent import Constituent
from utilities import logger

# just here for now to track when __getattr__ is used (MV)
trackGetAttrUse = False
trackGetAttrUse = True


class Tag(Constituent):

    """Abstract class for all tags."""

    def pretty_print(self, indent=0):
        """Generic pretty printer for tags, prints tag name between angled
        brackets."""
        print indent * ' ' + '<' + self.name + '>'


class EventTag(Tag):

    """Class for TimeML EVENT tags."""
    
    def __init__(self, attrs):
        """ The nodeType attribute is set to the same value as name because some methods
        ask for a nodeType attribute."""
        self.name = EVENT
        self.nodeType = EVENT
        self.dtrs = []
        self.begin = None
        self.end = None
        self.attrs = attrs
        self.eid = attrs[EID]
        self.eClass = attrs[CLASS]
        self.token = None

    def __len__(self):
        """Returns the lenght of the dtrs variable."""
        return len(self.dtrs)

    def __getitem__(self, index):
        """Returns an element from the dtrs variable."""
        return self.dtrs[index]

    def XXX__getattr__(self, name):
        # TODO: remove this once it is established that blinker and s2t work, it
        # does not appear to be used for Evita and for Slinket the attributes
        # that this is used for are just __nonzero__, __str__ and __repr__.
        if trackGetAttrUse:
            print "*** EventTag.__getattr__", name
        doc = self.tree()
        if name == 'eventStatus':
            return '1'
        elif name == TENSE:
            #print "TENSE:", doc.events[self.eid][TENSE]
            return doc.events[self.eid][TENSE]
        elif name == ASPECT:
            return doc.events[self.eid][ASPECT]
        elif name == EPOS: #NF_MORPH:
            return doc.events[self.eid][EPOS]#[NF_MORPH]
        elif name == MOD:
            try: mod = doc.events[self.eid][MOD]
            except: mod = 'NONE'
            return mod
        elif name == POL:
            try: pol = doc.events[self.eid][POL]
            except: pol = 'POS'
            return pol
        elif name == EVENTID:
            return doc.events[self.eid][EVENTID]
        elif name == EIID:
            return doc.events[self.eid][EIID]
        elif name == CLASS:
            return doc.events[self.eid][CLASS]
        elif name == 'text' or name == FORM:
            return doc.events[self.eid][FORM]
        elif name == STEM:
            return doc.events[self.eid][STEM]
        elif name == POS:
            try:
                return doc.events[self.eid][POS]
            except:
                # I don't remember whether POS has a particular use here
                # or is a left over from prior times
                logger.warn("Returning 'epos' instead of 'pos' value")  
                return doc.events[self.eid][EPOS]
        else:
            raise AttributeError, name

    def isEvent(self):
        return True

    def addTokenInfo(self, token):   
        #logger.debug("MY CURRENT attrs: "+str(self.attrs))
        self.token = token
        self._addValueToAttr(POS, self.token.pos)
        self._addValueToAttr(FORM, self.token.getText())

    def _addValueToAttr(self, attr, value):
        if not self._isValueAlreadySet(attr):
            self.attrs[attr] = value
        else:
            logger.debug( "VALUE already ASSIGNED to event: "+str(self.attrs[POS]))
            pass

    def _isValueAlreadySet(self, att):
        try:
            val = self.attrs[att]
            return 1
        except:
            return 0
        
    def pretty_print(self, indent=0):
        (eid, eiid, cl) = (self.attrs.get('eid'), self.attrs.get('eiid'), self.attrs.get('class'))
        print "%s<%s position=%s eid=%s eiid=%s class=%s>" % \
              ( indent * ' ', self.name, self.position, str(eid), str(eiid), str(cl) )
        for dtr in self.dtrs:
            dtr.pretty_print(indent+2)


    
class InstanceTag(Tag):

    """The class for MAKEINSTANCE tags. Used by S2T.

    Instance variables
       name - a string
       attrs - a dictionary of attributes"""
    
    def __init__(self, attrs):
        """Initialize name and attributes."""
        self.name = INSTANCE
        self.attrs = attrs



class TimexTag(Tag):

    """There is something fishy about this class because it all breaks when you try to
    print an instance. The problem probably stems from __getattr__."""
    
    def __init__(self, attrs):
        # NOTE: need to standardize on using name or nodeType
        self.nodeType = TIMEX
        self.name = TIMEX
        self.attrs = attrs
        self.dtrs = []
        self.begin = None
        self.end = None
        self.checkedEvents = False

    def __len__(self):
        """Returns the lenght of the dtrs variable."""
        return len(self.dtrs)

    def __getitem__(self, index):
        """Returns an element from the dtrs variable."""
        return self.dtrs[index]

    def __getslice__(self, i, j):
        """Get a slice from the dtrs variable."""
        return self.dtrs[i:j]

    def XXX__getattr__(self, name):
        # TODO. This method caused weird problems. The code seems to run okay
        # without it, but it is used, typically for nodeType. Investigate what
        # it is used for and eliminate that use, which was already done for
        # nodeType.
        if trackGetAttrUse:
            print "*** TimexTag.__getattr__", name
        if name == 'eventStatus':
            return '0'
        elif name in ['text', FORM, STEM, POS, TENSE, ASPECT, EPOS, MOD, POL,
                      EVENTID, EIID, CLASS]: #NF_MORPH, 
            return None
        else:
            raise AttributeError, name

    def isTimex(self):
        return True
        
    def nodeType(self):
        return self.name
    
    def add(self, chunkOrToken):
        chunkOrToken.setParent(self)
        self.dtrs.append(chunkOrToken)

    def setParent(self, parent):
        self.parent = parent

    def getText(self):
        string = ""
        for dtr in self.dtrs:
            if dtr.nodeType[-5:] == 'Token':
                string += ' '+str(dtr.getText())
            elif dtr.nodeType[-5:] == 'Chunk':
                string += ' '+str(dtr.getText())
        return string

    def pretty_print(self, indent=0):
        (tid, type, val) = (self.attrs.get('tid'), self.attrs.get('TYPE'), self.attrs.get('VAL'))
        print "%s<%s tid=%s TYPE=%s VAL=%s>" % \
              ( indent * ' ', self.name, str(tid), str(type), str(val) )
        for dtr in self.dtrs:
            dtr.pretty_print(indent+2)

        
class TlinkTag(Tag):

    """
    Instance variables
       name - a string
       attrs - a dictionary of attributes"""

    def __init__(self, attrs):
        """Initialize name and attributes."""
        self.name = TLINK
        self.attrs = attrs

        
class SlinkTag(Tag):
    """
    Instance variables
       name - a string
       attrs - a dictionary of attributes"""

    def __init__(self, attrs):
        """Initialize name and attributes."""
        self.name = SLINK
        self.attrs = attrs

        
class AlinkTag(Tag):
    """
    Instance variables
       name - a string
       attrs - a dictionary of attributes"""

    def __init__(self, attrs):
        """Initialize name and attributes."""
        self.name = ALINK
        self.attrs = attrs
