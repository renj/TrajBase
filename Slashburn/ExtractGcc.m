function [cur_gccind,cur_disind] = ExtractGcc(B)

%The number of components found is returned in S, and C is a vector
%indicating to which component each node belongs.
%[S,C]=graphconncomp(B, 'WEAK', true);%where is the function? http://www.mathworks.cn/cn/help/bioinfo/ref/graphconncomp.html
[S,C] = findGCC(B);

maxind=-1;
maxsize=0;

size_v = zeros(0, S);

for k=1:S
    size_v(k)=size(find(C == k), 2);% For a row vector X for size, size(X,2) is the size along X's column
end

[size_sort,I]=sort(size_v, 'descend');

cur_gccind = find(C == I(1));

cur_disind = zeros(0,0);

for k=2:S
    curind = find(C == I(k));
    cur_disind = [cur_disind curind];
end

% fprintf('\tgccsize\t%d\n', size(cur_gccind,2));

