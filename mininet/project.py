from mininet.topo import Topo
class MyTopo( Topo ):    
    "Simple topology example."
    def __init__( self ):        
        "Create custom topo."
        # Initialize topology        
        Topo.__init__( self )
        # Add hosts and switches        
        leftHost = self.addHost( 'h3', ip='10.0.0.3' )        
        rightHost = self.addHost( 'h4', ip='10.0.0.4' )        
        badHost1 = self.addHost('h1', ip='10.0.0.1')
	badHost2 = self.addHost('h2', ip='10.0.0.1')
	NODE2_IP = '192.168.56.103'

	backHost1 = self.addHost('h5', ip='10.0.0.5')
	backHost2 = self.addHost('h6', ip='10.0.0.6')

	targetHost = self.addHost('h7', ip='10.0.0.7')
	fake_listener = self.addHost('h8', ip='10.0.0.8')
	
	#midHost = self.addHost( 'h3' )
	#midHost2 = self.addHost('h4')	
	leftSwitch = self.addSwitch( 's2' )
	rightSwitch = self.addSwitch('s1')
	backupSwitch = self.addSwitch('s3')
	#rightSwitch = self.addSwitch( 's2')        
        # Add links        
        self.addLink( leftSwitch, leftHost )        
        self.addLink( leftSwitch, rightHost )        
        self.addLink( leftSwitch, badHost1)
	self.addLink( leftSwitch, badHost2)

	self.addLink( backupSwitch, backHost1)
	self.addLink( backupSwitch, backHost2)
	
	self.addLink(rightSwitch, targetHost)
	self.addLink(rightSwitch, fake_listener) 
	

	self.addLink(leftSwitch, rightSwitch)
	self.addLink(rightSwitch, backupSwitch)
	self.addLink(leftSwitch, backupSwitch)
#leftSwitch.cmd('ovs-vsctl add-port s1 s1-gre1 -- set interface s1-gre1 type=gre options:remote_ip='+NODE2_IP)
	#self.addLink( leftSwitch, rightSwitch )
	#self.addLink( rightSwitch, midHost)
	#self.addLink(rightSwitch, midHost2)
topos = { 'mytopo': ( lambda: MyTopo() ) }
