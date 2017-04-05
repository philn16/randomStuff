clear variables
close all
%% Configurable bariables
SAMPLES = 2^16;
PLOT_POINTS = 1024;
CONV_SPAN = 1.5;
PLOT_MIN = -40;
PLOT_MAX = 40;
mu = 0;
sigma = 10;

% End of config
%% Start of main script

% Desired pdf domain convolution
conv = @(t) exp(-(t/CONV_SPAN).^2);
% PDF values to get points.
times = linspace(PLOT_MIN,PLOT_MAX,PLOT_POINTS);

%% Get the random values
xc = normrnd(mu,sigma,SAMPLES,1);
xs = normrnd(mu,sigma,SAMPLES,1);
xComb = sqrt(xc.^2+xs.^2);

[ yXc ] = randomToPDF( xc,conv,times );
[ yXs ] = randomToPDF( xs,conv,times );
[ yXComb ] = randomToPDF( xComb,conv,times );

%% Finds the mean and standard deviation of the distributions
dt = times(2)-times(1);
fprintf('c) Xc mean is %7g\n',sum(yXc .* times)*dt)
fprintf('c) Xs mean is %7g\n',sum(yXs .* times)*dt)

fprintf('c) Xc standard deviation is %7g\n',sqrt(sum(yXc .* times.^2 *dt )) )
fprintf('c) Xs standard deviation is %7g\n',sqrt(sum(yXs .* times.^2 *dt )) )

fprintf('e) Combined mean is %7g\n',sum(yXComb .* times)*dt)
varComb=sum(yXComb .* times.^2 *dt );
fprintf('e) Combined standard deviation is %7g\n',sqrt(varComb) )
fprintf('e) Combined variance is %7g\n',varComb )

%% Plots

%% a
figure
hold on
normalExpected = 1/sqrt(2*pi*sigma^2)*exp(-(times/sigma).^2/2);
plot(times,normalExpected,'-k');
plot(times,normalExpected,':r');
title(sprintf('a) Expected Pdf of Xc and Xs: ~~ $\\displaystyle f(t) = \\frac{1}{\\sqrt{2 \\pi \\sigma^2}} \\cdot \\exp \\left[-\\frac{t^2}{2 \\sigma^2}\\right]$'),'interpreter','LaTex');
xlabel('Value');
ylabel('Probubility Density');

%% b
figure
hold on
plot(times,yXc,':k');
plot(times,yXs,'--k');
plot(times,normalExpected,'-r');
title(sprintf('b) Simmulated Pdf of Xc and Xs from %d point simmulation\n',SAMPLES));
legend('Xc','Xs','Expected');
xlabel('Value');
ylabel('Probubility Density');

%% d,e,f
minT=min(find(times>=0));
timePoints=minT:numel(times);
timez=times(timePoints);
rayleighPoints=2*timez / varComb .* exp(-timez .^ 2 / varComb);

%% d
figure
plot(times(timePoints),yXComb(timePoints),'-k');
title(sprintf('d) Simmulated Pdf of $\\displaystyle \\sqrt{X_c^2 + X_s^2}$ from %d point simmulation',SAMPLES),'interpreter','LaTex');
xlabel('Value');
ylabel('Probubility Density');

%% e
figure
plot(timez,rayleighPoints,'-k');
title(sprintf('e) Expected Rayleigh PDF for $\\sigma = $%7g:~~~ $\\displaystyle f(t) = 2 \\frac{t}{\\sigma^2} \\cdot \\exp \\left[ - \\frac{t^2}{\\sigma^2} \\right]$',sqrt(varComb)),'interpreter','LaTex');
xlabel('Value');
ylabel('Probubility Density');

%% f
figure
hold on
plot(times(timePoints),yXComb(timePoints),'-k');
plot(timez,rayleighPoints,'--r');
title(sprintf('f) Simmulated Rayleigh distribution with expected distribution\n%d random numbers, $\\sigma = $%7g',SAMPLES,sqrt(varComb)),'interpreter','LaTex');
xlabel('Value');
ylabel('Probubility Density');
legend('Simmulated Distribution','Actual Distribution');
