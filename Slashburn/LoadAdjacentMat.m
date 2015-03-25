
%Load undirected graph data(source_node connected_node pairs) from file and convert to its adjacent matrix
%vCount = vCount is the vertex number of the graph
%maxVNo = the maximum ID
function [A] = LoadAdjacentMat(fileName,vCount, edgeCount,maxVNo,fromLine)
%Map origional ID into converted ID
idMap = zeros(1,maxVNo);
idPos = 1;

A = zeros(vCount,vCount);

%A's entry will be set through A(x):x=rowCount*(ColumnID-1)+rowID
setIDs = zeros(1,edgeCount);
curEdgePos = 1 ;

curLine = 0;
fin = fopen( fileName,'r');
while ~feof(fin)
    curLine = curLine + 1 ;
    theLine = fgetl(fin);
    if(curLine<fromLine)
        continue ;
    end
    if mod(curLine,1000)==0
    	fprintf('Run for line %d...\n', curLine);
    end
    %Analyze the line
    pair = regexp( theLine,'[0-9]\d*','match');
    l = str2double(pair{1})+1;
    r = str2double(pair{2})+1;
    fprintf('%d %d\n',l,r); 

%     if(idMap(l)==0)
%         idMap(l) = idPos;
%         idPos = idPos + 1 ;
%     end
%     
%     if(idMap(r)==0)
%         idMap(r) = idPos;
%         idPos = idPos + 1 ;
%     end
%     l = idMap(l);
%     r = idMap(r);
%     fprintf('%d %d\n',l,r);
    
    setIDs(curEdgePos) = vCount*(r-1) + l ;
    curEdgePos = curEdgePos + 1 ;
end

A(setIDs) = true; 
A=A|A';
