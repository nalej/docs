# More about MetalLB

## General concepts

### Address Allocation

In a cloud-enabled Kubernetes cluster, you request a load-balancer, and your cloud platform assigns an IP address to you. In a bare metal cluster, MetalLB is responsible for that allocation.

MetalLB cannot create IP addresses out of thin air, so you do have to give it pools of IP addresses that it can use. MetalLB will take care of **assigning and unassigning individual addresses** as services come and go, but it will only ever hand out IPs that are part of its configured pools.

How you get IP address pools for MetalLB depends on your environment. If you’re running a bare metal cluster in a colocation facility, your hosting provider probably offers **IP addresses for lease**. In that case, you would lease, say, a /26 of IP space (64 addresses), and provide that range to MetalLB for cluster services.

Alternatively, your cluster might be purely private, providing services to a nearby LAN but not exposed to the internet. In that case, you could pick a range of IPs from one of the **private address spaces** (so-called RFC1918 addresses), and assign those to MetalLB. Such addresses are free, and work fine as long as you’re only providing cluster services to your LAN.

Or, you could do **both**. MetalLB lets you define as many address pools as you want, and doesn’t care what “kind” of addresses you give it.

### External Announcement

Once MetalLB has assigned an external IP address to a service, it needs to make the network beyond the cluster aware that the IP “lives” in the cluster. MetalLB uses standard routing protocols to achieve this: ARP, NDP, or BGP.

#### Layer 2 mode (ARP/NDP)

In layer 2 mode, one machine in the cluster takes ownership of the service, and uses standard address discovery protocols ([ARP](https://en.wikipedia.org/wiki/Address_Resolution_Protocol) for IPv4, [NDP](https://en.wikipedia.org/wiki/Neighbor_Discovery_Protocol) for IPv6) to make those IPs reachable on the local network. From the LAN’s point of view, the announcing machine simply has multiple IP addresses. Under the hood, MetalLB responds to [ARP](https://en.wikipedia.org/wiki/Address_Resolution_Protocol) requests for IPv4 services, and [NDP](https://en.wikipedia.org/wiki/Neighbor_Discovery_Protocol) requests for IPv6.

The major advantage of the layer 2 mode is its universality: it will work on any ethernet network, with no special hardware required, not even fancy routers.

In layer 2 mode, all traffic for a service IP goes to one node. From there, kube-proxy spreads the traffic to all the service’s pods. In that sense, layer 2 does not implement a load-balancer. Rather, it implements a **failover mechanism** so that a different node can take over should the current leader node fail for some reason. If the leader node fails, failover is automatic: the old leader’s lease times out after 10 seconds, at which point another node becomes the leader and takes over ownership of the service IP.

Layer 2 mode has two main **limitations** you should be aware of: single-node bottlenecking, and potentially slow failover.

As explained above, a single leader-elected node receives all traffic for a service IP. This means that **your service’s ingress bandwidth is limited to the bandwidth of a single node**. This is a fundamental limitation of using ARP and NDP to steer traffic.

In the current implementation, failover between nodes depends on cooperation from the clients. When a failover occurs, MetalLB sends a number of gratuitous layer 2 packets (a bit of a misnomer - it should really be called “unsolicited layer 2 packets”) to notify clients that the MAC address associated with the service IP has changed. Most operating systems handle “gratuitous” packets correctly, and update their neighbor caches promptly; in that case, failover happens within a few seconds. However, **some systems either don’t implement gratuitous handling at all or have buggy implementations** that delay the cache update. All modern versions of major OSes (Windows, Mac, Linux) implement layer 2 failover correctly, so the only situation where issues may happen is with older or less common OSes.

To minimize the impact of planned failover on buggy clients, you should keep the old leader node up for a couple of minutes after flipping leadership, so that it can continue forwarding traffic for old clients until their caches refresh. During an unplanned failover, the service IPs will be unreachable until the buggy clients refresh their cache entries.

#### BGP - Not supported

In BGP mode, all machines in the cluster establish [BGP](https://en.wikipedia.org/wiki/Border_Gateway_Protocol) peering sessions with nearby routers that you control, and tell those routers how to forward traffic to the service IPs. Using BGP allows for true load balancing across multiple nodes, and fine-grained traffic control thanks to BGP’s policy mechanisms.

## MetalLB Config Map

The following is a manifest file that describes the configuration of MetalLB, so it can be installed in the system.

```python
apiVersion: v1
kind: ConfigMap
metadata:
  namespace: metallb-system
  name: config
data:
  config: |
    # The peers section tells MetalLB what BGP routers to connect to. There
    # is one entry for each router you want to peer with.
    peers:
    - # The target IP address for the BGP session.
      peer-address: 10.0.0.1
      # The BGP AS number that MetalLB expects to see advertised by
      # the router.
      peer-asn: 64512
      # The BGP AS number that MetalLB should speak as.
      my-asn: 64512
      # (optional) the TCP port to talk to. Defaults to 179, you shouldn't
      # need to set this in production.
      peer-port: 179
      # (optional) The proposed value of the BGP Hold Time timer. Refer to
      # BGP reference material to understand what setting this implies.
      hold-time: 120s
      # (optional) The router ID to use when connecting to this peer. Defaults
      # to the node IP address. Generally only useful when you need to peer with
      # another BGP router running on the same machine as MetalLB.
      router-id: 1.2.3.4
      # (optional) Password for TCPMD5 authenticated BGP sessions
      # offered by some peers.
      password: "yourPassword"
      # (optional) The nodes that should connect to this peer. A node
      # matches if at least one of the node selectors matches. Within
      # one selector, a node matches if all the matchers are
      # satisfied. The semantics of each selector are the same as the
      # label- and set-based selectors in Kubernetes, documented at
      # https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/.
      # By default, all nodes are selected.
      node-selectors:
      - # Match by label=value
        match-labels:
          kubernetes.io/hostname: prod-01
        # Match by 'key OP values' expressions
        match-expressions:
        - key: beta.kubernetes.io/arch
          operator: In
          values: [amd64, arm]
 
    # The address-pools section lists the IP addresses that MetalLB is
    # allowed to allocate, along with settings for how to advertise
    # those addresses over BGP once assigned. You can have as many
    # address pools as you want.
    address-pools:
    - # A name for the address pool. Services can request allocation
      # from a specific address pool using this name, by listing this
      # name under the 'metallb.universe.tf/address-pool' annotation.
      name: my-ip-space
      # Protocol can be used to select how the announcement is done.
      # Supported values are bgp and layer2.
      protocol: bgp
      
      # A list of IP address ranges over which MetalLB has
      # authority. You can list multiple ranges in a single pool, they
      # will all share the same settings. Each range can be either a
      # CIDR prefix, or an explicit start-end range of IPs.
      addresses:
      - 198.51.100.0/24
      - 192.168.0.150-192.168.0.200
      # (optional) If true, MetalLB will not allocate any address that
      # ends in .0 or .255. Some old, buggy consumer devices
      # mistakenly block traffic to such addresses under the guise of
      # smurf protection. Such devices have become fairly rare, but
      # the option is here if you encounter serving issues.
      avoid-buggy-ips: true
      # (optional, default true) If false, MetalLB will not automatically
      # allocate any address in this pool. Addresses can still explicitly
      # be requested via loadBalancerIP or the address-pool annotation.
      auto-assign: false
      # (optional) A list of BGP advertisements to make, when
      # protocol=bgp. Each address that gets assigned out of this pool
      # will turn into this many advertisements. For most simple
      # setups, you will probably just want one.
      #
      # The default value for this field is a single advertisement with
      # all parameters set to their respective defaults.
      bgp-advertisements:
      - # (optional) How much you want to aggregate up the IP address
        # before advertising. For example, advertising 1.2.3.4 with
        # aggregation-length=24 would end up advertising 1.2.3.0/24.
        # For the majority of setups, you will want to keep this at the
        # default of 32, which advertises the entire IP address
        # unmodified.
        aggregation-length: 32
        # (optional) The value of the BGP "local preference" attribute
        # for this advertisement. Only used with IBGP peers,
        # i.e. peers where peer-asn is the same as my-asn.
        localpref: 100
        # (optional) BGP communities to attach to this
        # advertisement. Communities are given in the standard
        # two-part form <asn>:<community number>. You can also use
        # alias names (see below).
        communities:
        - 64512:1
        - no-export
    # (optional) BGP community aliases. Instead of using hard to
    # read BGP community numbers in address pool advertisement
    # configurations, you can define alias names here and use those
    # elsewhere in the configuration. The "no-export" community used
    # above is defined below.
    bgp-communities:
      # no-export is a well-known BGP community that prevents
      # re-advertisement outside of the immediate autonomous system,
      # but people do not usually recognize its numerical value. :)
      no-export: 65535:65281

```

