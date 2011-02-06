import os
import sys
import json

from dec import VizDecor

@VizDecor({list: lambda x:True})
def table(obj):
    s = '<div><table class="viz_list"><tr><br>'
    for item in obj:
        s += '<td>'
        if isinstance(item,list):
            # two dimensional
            s += Viz(item)
        else:
            # still one dimensional
            s += '%s'%(str(item))
        s += '</td>'
    s+='</tr></table></div></br>'
    return(s)

@VizDecor({dict: lambda x:True})
def vizdict(d):
    import json
    s='\n'
    s+="""
    <script type="text/javascript" src="../../protovis-d3.2.js"></script>
    <script type="text/javascript+protovis">
    var data = %s;
    var root = pv.dom(data)
        .root("data")
        .sort(function(a, b) pv.naturalOrder(a.nodeName, b.nodeName));

    /* Recursively compute the package sizes. */
    root.visitAfter(function(n) {
      if (n.firstChild) {
        n.nodeValue = pv.sum(n.childNodes, function(n) n.nodeValue);
      }
    });

    var vis = new pv.Panel()
        .width(260)
        .height(function() (root.nodes().length + 1) * 12)
        .margin(5);

    var layout = vis.add(pv.Layout.Indent)
        .nodes(function() root.nodes())
        .depth(12)
        .breadth(12);

    layout.link.add(pv.Line);

    var node = layout.node.add(pv.Panel)
        .top(function(n) n.y - 6)
        .height(12)
        .right(6)
        .strokeStyle(null)
        .events("all")
        .event("mousedown", toggle);

    node.anchor("left").add(pv.Dot)
        .strokeStyle("#1f77b4")
        .fillStyle(function(n) n.toggled ? "#1f77b4" : n.firstChild ? "#aec7e8" : "#ff7f0e")
        .title(function t(d) d.parentNode ? (t(d.parentNode) + "." + d.nodeName) : d.nodeName)
      .anchor("right").add(pv.Label)
        .text(function(n) n.nodeName);

    node.anchor("right").add(pv.Label)
        .textStyle(function(n) n.firstChild || n.toggled ? "#aaa" : "#000")
        .text(function(n) (n.nodeValue));

    vis.render();

    /* Toggles the selected node, then updates the layout. */
    function toggle(n) {
        n.toggle(pv.event.altKey);
        return layout.reset().root;
    }
    </script>
     """ %(json.dumps(d),)
    return(s)


#@VizDecor({dict: lambda x:True})

if __name__ == '__main__':
    a = range(5)
    b = ['a',[1,2],'b']
    print table(a)
    print table(b)
