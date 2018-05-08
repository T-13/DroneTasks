%% personalized parameters

%% simulation variables
snr_dB = 29.0; % power of signal over noise

%% object variables
% properties
objectMass = 0.5; % kg
objectMaxThrust = 13.08; % N (force of engines)
% state
startHeight = 6.8; % meters (initial height)

%% Kalman variables
processVariance = 1e-6;
estimatedMeasurementVariance = 0.1 ** 2;

%% P.I.D. variables
Kp = 20; % proportional parameter
Ki = -8.435; % integral parameter
Kd = 85; % derivative parameter
desiredHeight = 0; % target value
