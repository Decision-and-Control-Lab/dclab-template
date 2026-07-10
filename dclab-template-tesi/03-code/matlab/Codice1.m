% Solving M2N for solving the parametric_slant_hadamard_transform matrix%
function M=M2N(n) %n represents the power of 2
if n==1
M=eye(2);
else
    B=[1,1,1,1,1,1]; %input the values of parameters.Here in this example n=6
p=2^(n-1)-2; m=2^(2*n-2);
for i=1:n
a=sqrt(3*m/(4*m-B(i)));b=sqrt((m-B(i))/(4*m-B(i)));
M=[[1 0 ;a b] zeros(2,p) [1 0;-a b] zeros(2,p);   
zeros(p,2) eye(p) zeros(p,2) eye(p);
[0 1 ; -b a] zeros(2,p) [0 -1 ;b a] zeros(2,p);
zeros(p,2) eye(p) zeros(p,2) eye(p)];
end
end
end
