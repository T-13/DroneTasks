%% personalized parameters

%% simulation variables
snr_dB = 30.0; % power of signal over noise

%% object variables
% properties
objectMass = 0.4; % kg
objectMaxThrust = 14.0143; % N (force of engines)
% state
startHeight = 4.8; % meters (initial height)

%% Kalman variables
processVariance = 1e-6;
estimatedMeasurementVariance = 0.1 ** 2;

%% P.I.D. variables
Kp = 5; % proportional parameter
Ki = -7; % integral parameter
Kd = 43; % derivative parameter
desiredHeight = 0; % target value
