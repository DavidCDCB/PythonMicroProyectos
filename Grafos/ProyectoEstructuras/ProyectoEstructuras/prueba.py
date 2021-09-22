
#C:\Users\David\AppData\Local\Programs\Python\Python38-32\Scripts\;C:\Users\David\AppData\Local\Programs\Python\Python38-32\;C:\Users\David\AppData\Roaming\npm;C:\Program Files\Graphviz2.44.1\bin;C:\Program Files\Graphviz2.44.1\bin\dot.exe
#C:\oraclexe\app\oracle\product\11.2.0\server\bin;;C:\Program Files (x86)\Common Files\Oracle\Java\javapath;%SystemRoot%\system32;%SystemRoot%;%SystemRoot%\System32\Wbem;%SYSTEMROOT%\System32\WindowsPowerShell\v1.0\;%systemroot%\idmu\common;C:\Program Files (x86)\Microchip\xc8\v2.10\bin;C:\Program Files\Git\cmd;C:\Program Files\nodejs\
#C:\oraclexe\app\oracle\product\11.2.0\server\bin;;C:\Program Files (x86)\Common Files\Oracle\Java\javapath;%SystemRoot%\system32;%SystemRoot%;%SystemRoot%\System32\Wbem;%SYSTEMROOT%\System32\WindowsPowerShell\v1.0\;%systemroot%\idmu\common;C:\Program Files (x86)\Microchip\xc8\v2.10\bin;C:\Program Files\Git\cmd;C:\Program Files\nodejs\;C:\Program Files\Graphviz2.44.1\bin;C:\Program Files\Graphviz2.44.1\bin\dot.exe
#C:\oraclexe\app\oracle\product\11.2.0\server\bin;;C:\Program Files (x86)\Common Files\Oracle\Java\javapath;%SystemRoot%\system32;%SystemRoot%;%SystemRoot%\System32\Wbem;%SYSTEMROOT%\System32\WindowsPowerShell\v1.0\;%systemroot%\idmu\common;C:\Program Files (x86)\Microchip\xc8\v2.10\bin;C:\Program Files\Git\cmd;C:\Program Files\nodejs;C:\Program Files\Graphviz2.44.1\bin;C:\Program Files\Graphviz2.44.1\bin\dot.exe


import os
os.environ["PATH"] += os.pathsep + 'C:\Program Files\Graphviz2.44.1\bin'

from graphviz import Digraph

f = Digraph('G', filename='grafo', format='png')
f.attr(rankdir='LR', size='8,5')

f.attr('node', shape='doublecircle')
f.node('LR_0')
f.node('LR_3')
f.node('LR_4')
f.node('LR_8')

f.attr('node', shape='circle')
f.edge('LR_0', 'LR_2', label='SS(B)')
f.edge('LR_0', 'LR_1', label='SS(S)')
f.edge('LR_1', 'LR_3', label='S($end)')
f.edge('LR_2', 'LR_6', label='SS(b)')
f.edge('LR_2', 'LR_5', label='SS(a)')
f.edge('LR_2', 'LR_4', label='S(A)')
f.edge('LR_5', 'LR_7', label='S(b)')
f.edge('LR_5', 'LR_5', label='S(a)')
f.edge('LR_6', 'LR_6', label='S(b)')
f.edge('LR_6', 'LR_5', label='S(a)')
f.edge('LR_7', 'LR_8', label='S(b)')
f.edge('LR_7', 'LR_5', label='S(a)')
f.edge('LR_8', 'LR_6', label='S(b)')
f.edge('LR_8', 'LR_5', label='S(a)')

f.view() 