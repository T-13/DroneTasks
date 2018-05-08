%% personalized parameters

%% simulation variables
snr_dB = 33.0; % power of signal over noise

%% object variables
% properties
objectMass = 0.54; % kg
objectMaxThrust = 16.3500; % N (force of engines)
% state
startHeight = 6.2; % meters (initial height)

%% Kalman variables
processVariance = 1e-6;
estimatedMeasurementVariance = 0.1 ** 2;

%% P.I.D. variables
Kp = 10; % proportional parameter
Ki = -4.435; % integral parameter
Kd = 40; % derivative parameter
desiredHeight = 0; % target value
