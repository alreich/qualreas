<?xml version='1.0' encoding='utf-8'?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd"><key id="d3" for="edge" attr.name="fruit" attr.type="string"/>
<key id="d2" for="node" attr.name="alpha" attr.type="string"/>
<key id="d1" for="graph" attr.name="what" attr.type="string"/>
<key id="d0" for="graph" attr.name="name" attr.type="string"/>
<graph edgedefault="directed"><data key="d0">Foo</data>
<data key="d1">test1</data>
<node id="nd1">
  <data key="d2">ABC</data>
</node>
<node id="nd2">
  <data key="d2">DEF</data>
</node>
<node id="nd3">
  <data key="d2">GHI</data>
</node>
<edge source="nd1" target="nd2">
  <data key="d3">apple</data>
</edge>
<edge source="nd1" target="nd3">
  <data key="d3">pear</data>
</edge>
<edge source="nd2" target="nd1">
  <data key="d3">APPLE</data>
</edge>
<edge source="nd2" target="nd3">
  <data key="d3">banana</data>
</edge>
<edge source="nd3" target="nd1">
  <data key="d3">PEAR</data>
</edge>
<edge source="nd3" target="nd2">
  <data key="d3">BANANA</data>
</edge>
</graph></graphml>