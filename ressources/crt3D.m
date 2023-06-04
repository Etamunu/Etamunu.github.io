%Auteur : Jean Peyen
%Date   : 08/03/2017

%representation en 3D et avec des couleurs variant selon "l'age" des branches
%d'un arbre brownien approche un l'algorithme de David Aldous (The Continuum Random Tree)

%%%%nombre de points%%%
n       = 1000;
%%%%%%%%%%%%%%%%%%%%%%%

v = zeros(3,n);
M = zeros(n,n);

%construction de l'arbre sous forme de matrice d'adjacence
for i=2:n
  r(i-1)=unidrnd(n);
  m=min(i-1,r(i-1));
  M(i,m)=1;
  M(m,i)=1;
endfor

%constructon de la representation 3D associee
J(1)=1;
for i = 2:n
  if (r(i-1)<i-1)
    J(i)= J(i-1)+1;
  else
    J(i)= J(i-1);
  endif
endfor


for i = 2:n
  v(1,i)=v(1,min(r(i-1),i-1));
  v(2,i)=v(2,min(r(i-1),i-1));
  v(3,i)=v(3,min(r(i-1),i-1));
  if (mod(J(i),3)==1)
    v(1,i)=v(1,i)+1;
  else
    if (mod(J(i),3)==2)
    v(2,i)=v(2,i)+1;
    else
      v(3,i)=v(3,i)+1;
    endif
  endif
endfor

%affichage
view(-60,-30)
for i = 1:n
   hold on;
   pause(0.01)
  for j = i+1:n
    if(M(i,j)==1)
      plot3([v(1,i) v(1,j)],[v(2,i) v(2,j)],[v(3,i) v(3,j)],'linewidth',2,'Color',[0,0.5,i/n]);
    hold on;
    endif
  endfor
endfor
