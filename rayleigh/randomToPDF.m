% Takes randome numbers and makes them into a nice looking pdf
% Makes it nice looking by convoluting it with a functin, convFunction
% EXAMPLE: 
%{
	xc = normrnd(mu,sigma,SAMPLES,1);
	times = linspace(PLOT_MIN,PLOT_MAX,PLOT_POINTS);
	[ yXc ] = randomToPDF( xc,conv,times );
	plot(times,yXc,'-k');
%}
function [ y ] = randomToPDF( randomSignal,convFunction,times )
randomSignal=sort(randomSignal);

y=zeros(1,numel(times));

for i=1:numel(times)
	y(i) = sum(convFunction(randomSignal-times(i)));
end

% Normalize the PDF
integral = (times(2)-times(1))*sum(y);
y = y./integral;
end