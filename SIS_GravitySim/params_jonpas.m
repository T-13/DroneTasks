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
processVariance = 1e-5;
estimatedMeasurementVariance = 0.1 ** 2;

%% P.I.D. variables
Kp = 1.2; % proportional parameter
Ki = 1; % integral parameter
Kd = 0.8; % derivative parameter
desiredHeight = 0; % target value
