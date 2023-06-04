%Young diagram script
%Author: Jean Peyen
%First version: 29/05/22


%This function takes a sequence of natural numbers and produces an eps file
%with the corresponding Young diagram (with the French convention)

function young_plot(lambda)
  lambda = flip(sort(lambda));
  m = length(lambda); %height of the diagram (total number of parts)
  L = max(lambda);  %length of the diagram (maximal parts)
  Y = zeros(1,L); %y coordinates of the upper bound
  X = zeros(1,L); %x coordinates of the upper bound

  hold on;

%draw the boxes
  for(i=1:m)
    for(j=1:lambda(i))
      rectangle("position", [j-1, i-1, 1, 1], "FaceColor", [0.9, 0.9, 0.9]);
    endfor
  endfor

%draw the upper bound
  for(i=1:L)
    Y(i) = cumsum(lambda>i-1)(m);
    X(i) = i-1;
  endfor

  for(i=1:L)
    line([X(i),X(i)+1], [Y(i),Y(i)], "linewidth", 1, "color", "r");
  endfor

  line([X(L)+1, X(L)+2], [0,0], "linewidth", 1, "color", "r");

  plot(lambda(1),0, 'o', 'markersize', 5, 'markeredgecolor', 'r', 'markerfacecolor', 'w');
  for(i=2:L)
    if(Y(i-1)>Y(i))
      plot(X(i),Y(i), 'o', 'markersize', 5, 'markeredgecolor', 'r', 'markerfacecolor', 'w');
    endif
  endfor

  plot(lambda(1),1, 'o', 'markersize', 5, 'markeredgecolor', 'r', 'markerfacecolor', 'r');
  for(i=1:L-1)
    if(Y(i+1)<Y(i))
      plot(X(i)+1,Y(i), 'o', 'markersize', 5, 'markeredgecolor', 'r', 'markerfacecolor', 'r');
    endif
  endfor

  plot(0,m, 'o', 'markersize', 5, 'markeredgecolor', 'r', 'markerfacecolor', 'r');

%set the axis at the right scale
  set(gca, "fontsize", 14)
  axis("equal", [0,lambda(1)+0.5,0,m+0.5]);

%save the picture in the eps format
  print -color -depsc young.eps
endfunction
