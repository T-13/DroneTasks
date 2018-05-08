%% personalized parameters

%% simulation variables
snr_dB = 33.0; % power of signal over noise

%% object variables
% properties
objectMass = 0.58; % kg
objectMaxThrust = 17.8364; % N (force of engines)
% state
startHeight = 4.4; % meters (initial height)

%% Kalman variables
processVariance = 1e-6;
estimatedMeasurementVariance = 0.1 ** 2;

%% P.I.D. variables
Kp = 24; % proportional parameter
Ki = -8; % integral parameter
Kd = 45; % derivative parameter
desiredHeight = 0; % target value
