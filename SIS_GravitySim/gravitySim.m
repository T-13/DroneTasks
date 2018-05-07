%% 1D phisycs simulation (defying gravity)
% simplified world, ignoring air resistance

%% simulation variables
timeDuration = 10;  % seconds
timeStep = 0.001;   % seconds

g = -9.81;          % meters / seconds * seconds (gravitational change of velocity)

snr_dB = 30.0;       % power of signal over noise


%% object variables
% properties
objectMass = 0.4;           % kg
objectMaxThrust = 13.08;    % N (force of engines)
objectNeutralThrust = (g / objectMaxThrust) * -1;
% state
startHeight = 5;            % meters (initial height)
startVelocity = 0;          % meters / seconds (initial velocity)
startThrust = 0;  % percentage of maxThrust (initial force)


%% Kalman variables
processVariance = 1e-5;
estimatedMeasurementVariance = 0.1 ** 2;

% initialize
posteriEstimate = 0.0;
posteriErrorEstimate = 1.0;


%% P.I.D. variables
Kp = 1.2; % proportional parameter
Ki = 1; % integral parameter
Kd = 0.8; % derivative parameter
desiredHeight = 0; % target value

% initialize
ITerm = 0;


%% Personalized parameters
%source('params_jonpas.m');
%source('params_nevith.m');
%source('params_planeer.m');
%source('params_askupek.m');


%% simulation

% prepare history
historyTime = timeStep:timeStep:timeDuration;

historyHeight = zeros(1,timeDuration/timeStep);
historyHeightWithNoise = zeros(1,timeDuration/timeStep);
historyHeightWithFilter = zeros(1,timeDuration/timeStep);

historyThrust = zeros(1,timeDuration/timeStep);
historyForce = zeros(1,timeDuration/timeStep);
historyVelocity = zeros(1,timeDuration/timeStep);
historyEnergy = zeros(1,timeDuration/timeStep);


% prepare model
currentHeight = startHeight;
currentVelocity = startVelocity;
currentThrust = startThrust;
currentEnergy = 0.5 * objectMass * power(currentVelocity,2);


% model loop
for ts = 1:1:(timeDuration/timeStep)
    %% prepare for new loop ...
    previousHeight = currentHeight;
    previousVelocity = currentVelocity;
    previousEnergy = currentEnergy;
    previousThrust = currentThrust;

    % simulate noise :P
    currentNoise = awgn_noise_single_element(historyHeight(1:ts), snr_dB);
	  currentHeight = currentHeight + currentNoise;



    %% Kalman filter
    prioriEstimate = posteriEstimate;
    posteriErrorEstimate += processVariance;
    blendingFactor = posteriErrorEstimate / (posteriErrorEstimate + estimatedMeasurementVariance);
    posteriEstimate = prioriEstimate + blendingFactor * (currentHeight - prioriEstimate);
    posteriErrorEstimate = (1 - blendingFactor) * posteriErrorEstimate;
    currentHeight = posteriEstimate;

    historyHeightWithFilter(ts) = currentHeight;


    %% P.I.D.
	  er = desiredHeight - currentHeight;
    PTerm = Kp * er;
    ITerm += er * timeStep;
    DTerm = Kp * (previousHeight - currentHeight) / timeStep;
    
    o = PTerm + (Ki * ITerm) + (Kd * DTerm);


    %% control logic here
    currentThrust = -o / 100;
    historyThrust(ts) = currentThrust;


    %% calculate new state ...
    % new force on object = force of gravity + current thrust
    currentForce = (objectMass * g) + (objectMass * currentThrust * objectMaxThrust);
    historyForce(ts) = currentForce;
    % new velocity of object = previous velocity + force * time / mass
    currentVelocity = previousVelocity + (currentForce * timeStep) / objectMass;
    historyVelocity(ts) = currentVelocity;
    % new displacement of object
    dH = (previousVelocity + currentVelocity) * 0.5 * timeStep;
    % new height of object
    currentHeight = previousHeight + dH;
    historyHeight(ts) = currentHeight;
    historyHeightWithNoise(ts) = currentHeight + currentNoise;
    % new kinetic energy of object (or force at distance 0)
    currentEnergy = 0.5 * objectMass * power(currentVelocity,2);
    historyEnergy(ts) = currentEnergy;

    %% exit conditions
    if currentHeight <= 0
        disp('Simulation results:')
        disp(['Landing time: ' num2str(historyTime(ts)) ' s']);
        disp(['Landing speed: ' num2str(historyVelocity(ts)) ' m/s']);
        disp(['Landing force: ' num2str(historyEnergy(ts)) ' N']);
        break
    end
end

% plot result
figure;
subplot(2,2,1); hold on;
title('Height of object');
plot(historyTime, historyHeightWithNoise, 'r');
plot(historyTime, historyHeightWithFilter, 'g');
plot(historyTime, historyHeight, 'b');
hold off;
xlabel('time (s)'); ylabel('height (m)');

subplot(2,2,2); hold on;
title('Force acted on object');
ax = plotyy(historyTime, historyForce, historyTime, historyThrust);
ylabel(ax(1), 'force (N)');
ylabel(ax(2), 'thrust (%)');
hold off;
xlabel('time (s)');

subplot(2,2,3);
title('Velocity of object');
plot(historyTime, historyVelocity);
xlabel('time (s)'); ylabel('velocity (m/s)');

subplot(2,2,4);
title('Kinectic energy of object');
plot(historyTime, historyEnergy);
xlabel('time (s)'); ylabel('energy (J)');
