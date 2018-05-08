%% personalized parameters

%% simulation variables
snr_dB = 30.0; % power of signal over noise

%% object variables
% properties
objectMass = 0.4; % kg
objectMaxThrust = 13.08; % N (force of engines)
% state
startHeight = 5; % meters (initial height)

%% Kalman variables
processVariance = 1e-5;
estimatedMeasurementVariance = 0.1 ** 2;

%% P.I.D. variables
Kp = 1.2; % proportional parameter
Ki = 1; % integral parameter
Kd = 0.8; % derivative parameter
desiredHeight = 0; % target value
