"""
A simple REST interface for Mininet.

The Mininet REST API provides a simple way to control nodes when 
running mininet headless.
"""

import json
import os.path
import threading

try:
    from bottle import Bottle, HTTPResponse, request
except ImportError as e:
    pass

from mininet.log import debug, info, output, error

class REST( Bottle ):
    "Simple ReSTful interface to talk to nodes."

    apiPrefix = '/api/v1/'

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
        self.route( self.apiPrefix + 'nodes', callback=self.get_nodes )
        self.route( self.apiPrefix + 'switches', callback=self.get_switches )
        self.route( self.apiPrefix + 'hosts', callback=self.get_hosts )
        self.route( self.apiPrefix + 'controllers', callback=self.get_controllers )
        self.route( self.apiPrefix + 'links', callback=self.get_links )
        try:
            self.run( host='0.0.0.0', port=port, quiet=True )
        except Exception:
            error( 'Error starting rest api\n' )
        info( port )

    def build_response( self, data, code=200 ):
        if not isinstance( data, dict ):
            data = json.dumps( { "error": "could not create json response" } )
            return HTTPResponse( status=500, body=data )
        return HTTPResponse( status=code, body=data )

    def get_nodes( self ):
        """Get a list of nodes that exist within a topo"""
        data = { "nodes": [ node for node in self.mn ] }
        return self.build_response( data )

    def get_switches( self ):
        """Get a list of switches that exist within a topo"""
        data = { "switches": [ node.name for node in self.mn.switches ] }
        return self.build_response( data )
    
    def get_hosts( self ):
        """Get a list of hosts that exist within a topo"""
        data = { "hosts": [ node.name for node in self.mn.hosts ] }
        return self.build_response( data )

    def get_controllers( self ):
        """Get a list of controllers that exist within a topo"""
        data = { "controllers": [ node.name for node in self.mn.controllers ] }
        return self.build_response( data )

    def get_links( self ):
        """Get a list of links that exist within a topo"""
        data = { "links": [ ( link.intf1.name, link.intf2.name ) for link in self.mn.links ] }
        return self.build_response( data )
