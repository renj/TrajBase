clear;
cd ./Slashburn;
ls;
[A] = LoadAdjacentMat('../out.txt',1500,2313,1500,1);
[niter, gccsize, Ak, I, J] = SlashBurn(A,10,1);
cd ..;
save('transform.mat','J');
%exit