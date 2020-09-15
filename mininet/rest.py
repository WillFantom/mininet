"""
A simple REST interface for Mininet.

The Mininet REST API provides a simple way to control nodes when 
running mininet headless.
"""
from bottle import Bottle, HTTPResponse, request
import threading
import json
import os.path

from mininet.log import info, output, error

class REST( Bottle ):
    "Simple RESTful interface to talk to nodes."

    def __init__( self, mininet, port=8080, *args, **kwargs ):
        """Start and run REST API for host interaction
           mininet: Mininet network object
           port: port to serve from"""
        super( REST, self ).__init__()
        self.mn = mininet
        self.port = port
        thread = threading.Thread( target=self.run_server, args=(self.port,), daemon=True )
        thread.start()
        info( '*** Starting API\n' )

    def run_server( self, port ):
        self.route( '/nodes', callback=self.get_nodes )
        try:
            self.run( host='0.0.0.0', port=port, quiet=True )
        except Exception:
            error( 'Error starting rest api\n' )

    def build_response( self, data, code=200 ):
        if not isinstance( data, dict ):
            data = json.dumps( { "error": "could not create json response" } )
            return HTTPResponse( status=500, body=data )
        return HTTPResponse( status=code, body=data )

    def get_nodes( self ):
        """Get a list of nodes that exist within a topo"""
        data = { "nodes": [ node for node in self.mn ] }
        return self.build_response( data )