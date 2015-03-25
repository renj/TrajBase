function [S C] = findGCC(A)
%The component label
C = 1:size(A,2);
%Find the connected components
[S,sizes,members] = networkComponents(A);

for i=1:S
    for v=members{i}
        C(v)=i;
    end
end