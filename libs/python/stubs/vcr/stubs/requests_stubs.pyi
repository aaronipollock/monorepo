from ..stubs import VCRHTTPConnection as VCRHTTPConnection, VCRHTTPSConnection as VCRHTTPSConnection
from urllib3.connection import HTTPConnection, VerifiedHTTPSConnection

class VCRRequestsHTTPConnection(VCRHTTPConnection, HTTPConnection): ...
class VCRRequestsHTTPSConnection(VCRHTTPSConnection, VerifiedHTTPSConnection): ...