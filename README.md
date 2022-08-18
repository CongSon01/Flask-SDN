# Flask-SDN
## Abstract
Nowadays, an ever-increasing number of network devices and ad-
vanced services leads to many obstacles for network management in
terms of scalability, programmability and so on. Software-Defined
Networking (SDN) with a separation between control and data
plane, is a potential solution to overcome these limitations. One of
popular applications in SDN is the routing algorithm, but it is chal-
lenging to implement this algorithm in inter-SDN domains where
each SDN domain is dedicated to an Internet Service Provider (ISP),
due to two main difficulties. First, each SDN domain does not have
a global view of other SDN domains, so that routing policies are
not optimal for the entire network. Second, without the global
view, ISPs select shortest path to forward packets in their networks,
bringing over-utilization to several links and under-utilization to
other links. This leads to a degradation of network performance
and Quality of Service (QoS). Therefore, in this paper, we propose
a QoS-based server and route selection for inter-SDN domains in
order to optimize network performance. To overcome the first limi-
tation, we take advantage of our recent work, SINA and an adaptive
consistency mechanism to guarantee information consistency be-
tween controllers of inter-SDN domains and intra-SDN domains.
To deal with the second one, we present QoS-based server and
route selection mechanism to select server and routing path with
appropriate cost in order to optimize network performance. The
experimental results illustrate that our proposal improves 15% of
link utilization and 13% percent of loss in comparison with the
first benchmark. The proposal also achieves a great reduction of
overhead and good response time compared with both benchmarks.
