# ActiveSonarEquation
Implementation of and experimentation with the Active Sonar Equation for underwater acoustics.

## Usage

`pip3 install -r requirements.txt`

`python3 sonar.py plot`

Plots a Echo Level vs. Range and Noise Masking Level vs. Range graph for the default acoustic parameters

## Example Output

### Default Parameters

![Default Parameters](/images/default.png)

With the default parameters, the equation predicts that the sonar will be able to detect signal from noise until a range of about 830 m.

### Calm Seas

`python3 sonar.py plot -ss 0`

![Sea State Zero](/images/calmsea.png)

With an inputted sea state of zero (completely calm and "glassy" ocean conditions), as opposed to the default sea state of 3, the equation predicts that the sonar will be able to detect signal from noise until a range of about 1080 m. This improvement is due to the decrease in noise masking level caused by a decrease in ocean swells and waves.

### Lowered Transmitter Frequency

`python3 sonar.py plot -f 20`

![Lower Frequency](/images/lowfreq.png)

With an acoustic frequency set at 20 kHz compared to the default frequency of 50 kHz, the equation predicts that the sonar will be able to detect signal from noise only up until a range of about 700 m. This decrease in range is due to the increased noise level implied by a lower acoustic frequency.