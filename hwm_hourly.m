% MATLAB: calculate the quiet horizontal wind model versus localtime (LST)
% for a latitute of 42.618 degrees north, longitude of 71.498 degrees west, 
% and an altitude of 95 km above mean sea level (msl).

% setup plot ranges
xplot = -6:6;
yplot = [];

% sample UT-6 to UT+0 and bin by one-hour intervals
for s = 64800:3600:86400
    sum3 = 0;
    sum4 = 0;
    
    % sample over all 365 days
    for d = 1:365
        w = atmoshwm07(42.618, -71.498, 95000, 'day', d, 'seconds', s);
        sum3 = sum3 + w(1);
        sum4 = sum4 + 1; 
    end
    
    y2(d) = sum3/sum4;
    yplot = [yplot y2(d)];
end

% sample UT+1 to UT+6 and bin by one-hour intervals
for s = 3600:3600:21600
    sum1 = 0;
    sum2 = 0;
    
    % sample over all 365 days
    for d = 1:365
        w = atmoshwm07(42.618, -71.498, 95000, 'day', d, 'seconds', s);
        sum1 = sum1 + w(1);
        sum2 = sum2 + 1; 
    end
    
    y1(d) = sum1/sum2;
    yplot = [yplot y1(d)];
end

% plot data
figure
plot(xplot,yplot)
title('Hourly Trend in the Horizontal Wind Model (HWM)')
xlabel('Localtime (LST)')
ylabel('Meridional Wind Velocity (m/s)')
axis([-6 6 inf inf])
