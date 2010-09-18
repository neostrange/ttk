
import time

from docmodel.xml_parser import Parser
from docmodel.document import SuperDoc


    
class DefaultParser:

    """The simplest parser, much like the SimpleXml parser for the old simple-xml
    doctype. Gets the TEXT tag and the associated source string. Then creates an
    XmlDocument for that string and simple metadata for the document by setting the DCT to
    today. """
    
    def __init__(self):
        
        """This could be used to hand in specific metadata parsers or other functionality that
        cuts through genres."""

        pass


    def parse(self, docsource):

        """Get the TEXT tag and the associated source string. Then create an XmlDocument
        for that string and simple metadata for the document by setting the DCT to
        today. Return an instance of SuperDoc."""
            
        target_tag = self._find_target_tag(docsource)
        text = docsource.source[target_tag.begin:target_tag.end]
        xmldoc = Parser().parse_string("<TEXT>%s</TEXT>" % text)
        dct = get_today()
        metadata = { 'dct': dct }
        return SuperDoc(docsource, xmldoc, metadata)


    def _find_target_tag(self, docsource):
        
        for t in docsource.tags:
            if t.name == 'TEXT':
                return t
        raise DocParserError('Cannot parse docsource, no target_tag')


class TimebankParser:

    """Preliminary class for Timebank parsing. Will likely not work, but is stroing some DCT
    processing functionality (which probably needs to be moved out of the class). """
    

    def __init__(self):
        
        """This could be used to hand in specific metadata parsers or other functionality that
        cuts through genres."""

        pass


    def parse(self, docsource):

        """Get the TEXT tag and the associated source string. Then create an XmlDocument
        for that string and simple metadata for the document by setting the DCT to
        today. Return an instance of SuperDoc."""

        target_tag = self._find_target_tag(docsource)
        text = docsource.source[target_tag.begin:target_tag.end]
        xmldoc = Parser().parse_string("<TEXT>%s</TEXT>" % text)
        dct = self.parse_dct()
        metadata = { 'dct': dct }
        return SuperDoc(docsource, xmldoc, metadata)


    def _find_target_tag(self, docsource):
        
        for t in docsource.tags:
            if t.name == 'TEXT':
                return t
        raise DocParserError('Cannot parse docsource, no target_tag')


    def parse_dct(self, xmldoc):

        """Takes an XmlDocument, extracts the document creation time, and returns it as a
        string of the form YYYYMMDD.

        TODO: update for use with DocSource class."""

        # set DCT default
        dct = get_today()

        docsource = self._get_doc_source(xmldoc)

        if docsource == 'ABC':
            docno = xmldoc.tags['DOCNO'][0].collect_content().strip()
            dct = docno[3:11]
            
        elif docsource == 'AP':
            fileid = xmldoc.tags['FILEID'][0].collect_content().strip()
            result = re.compile("(AP-NR-)?(\d+)-(\d+)-(\d+)").match(fileid)
            if result:
                (crap, month, day, year) = result.groups()
                dct = "19%s%s%s" % (year, month, day)
            else:
                logger.warn("Could not get date from %s" % fileid)
                
        elif docsource == 'APW':
            date_time = xmldoc.tags['DATE_TIME'][0].collect_content().strip()
            result = re.compile("(\d+)/(\d+)/(\d+)").match(date_time)
            if result:
                (month, day, year) = result.groups()
                dct = "%s%s%s" % (year, month, day)
            else:
                logger.warn("Could not get date from %s" % fileid)
            
        elif docsource == 'CNN':
            docno = xmldoc.tags['DOCNO'][0].collect_content().strip()
            dct = docno[3:11]

        elif docsource == 'NYT':
            date_time = xmldoc.tags['DATE_TIME'][0].collect_content().strip()
            result = re.compile("(\d+)/(\d+)/(\d+)").match(date_time)
            if result:
                (month, day, year) = result.groups()
                dct = "%s%s%s" % (year, month, day)
            else:
                logger.warn("Could not get date from %s" % fileid)

        elif docsource == 'PRI':
            docno = xmldoc.tags['DOCNO'][0].collect_content().strip()
            dct = docno[3:11]

        elif docsource == 'SJMN':
            pubdate = xmldoc.tags['PUBDATE'][0].collect_content().strip()
            dct = '19' + pubdate

        elif docsource == 'VOA':
            docno = xmldoc.tags['DOCNO'][0].collect_content().strip()
            dct = docno[3:11]

        elif docsource == 'WSJ':
            docno = xmldoc.tags['DOCNO'][0].collect_content().strip()
            dct = '19' + docno[3:9]

        elif docsource == 'eaX':
            docno = xmldoc.tags['DOCNO'][0].collect_content().strip()
            dct = '19' + docno[2:8]

        elif docsource == 'ea':
            docno = xmldoc.tags['DOCNO'][0].collect_content().strip()
            dct = '19' + docno[2:8]

        return dct

    
    def _get_doc_source(self, xmldoc):
        
        """Returns the name of the content provider."""

        tag_DOCNO = xmldoc.tags['DOCNO'][0]
        content = tag_DOCNO.collect_content().strip()
        # TimeBank has only these providers
        for str in ('ABC', 'APW', 'AP', 'CNN', 'NYT', 'PRI', 'SJMN', 'VOA', 'WSJ', 'ea', 'ed'):
            if content.startswith(str):
                return str
        logger.warn("Could not determine document source from DOCNO tag")
        return 'GENERIC'



class MetaDataParser_ATEE:

    """This is how DCT parsing was done for ATEE document. Must decide whether neta data
    parsers are separate classes (like here) or are part of the Parser (see
    TimebankParser)."""
    
    def parse_dct(self, xmldoc):
        """All ATEE documents have a DATE tag with a value attribute, the value of that attribute
        is returned."""
        date_tag = xmldoc.tags['DATE'][0]
        return date_tag.attrs['value']

    
def get_today():
    """Return today's date in YYYYMMDD format."""
    return time.strftime("%Y%m%d", time.localtime());


class DocParserError(Exception): pass
