%% Noise generator - do not touch!!!
function y = awgn_noise_single_element(x, SNR_dB)
    rand('seed'); % set the random generator seed to default (for comparison only)
    L = length(x);
    SNR = 10^(SNR_dB/10); % SNR to linear scale
    Esym = sum(abs(x).^2)/(L); % Calculate actual symbol energy
    N0 = Esym / SNR; % Find the noise spectral density
    if(isreal(x))
        noiseSigma = sqrt(N0); % Standard deviation for AWGN Noise when x is real
        n = noiseSigma * randn(1,L);
    else
        noiseSigma = sqrt(N0/2);  % Standard deviation for AWGN Noise when x is complex
        n = noiseSigma *(randn(1,L)+1i * randn(1,L));
    end
    y = n(end);
endfunction
