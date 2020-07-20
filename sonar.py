import numpy as np
import click
import math
import matplotlib.pyplot as plt

@click.group()
def cli():
    pass

# PARAMETERS
@cli.command()
@click.option("-sl", "--source-level", required=True, default="200.0", show_default=True, help="Source Level (dB re 1uPa @ 1m)")
@click.option("-f", "--frequency", required=True, default="50.0", show_default=True, help="Acoustic Frequency (kHz)")
@click.option("-ss", "--sea-state", required=True, default="3", show_default=True, help="Sea State (Douglas Scale 0 - 6)")
@click.option("-alpha", "--absorption-coefficient", required=True, default="13.0", show_default=True, help="Absorption Coefficient (dB / km)")
@click.option("-ts", "--target-strength", required=True, default="-40.0", show_default=True, help="Target Strength (dB)")
@click.option("-nl", "--beam-width", required=True, default="5.0", show_default=True, help="Beam Width (deg)")
@click.option("-dt", "--detection-threshold", required=True, default="20.0", show_default=True, help="Detection Threshold (dB)")
def plot(source_level, frequency, sea_state, absorption_coefficient, target_strength, beam_width, detection_threshold):

    # Calculate noise level from sea state and frequency (SS5 APPROXIMATED)
    Qs = [89, 281.8, 707.9, 891.3, 1259, 1500, 1778.3]
    f = float(frequency) * 1000
    noise_level = 20 * math.log10(2000 * Qs[int(sea_state)] / f + f * 5.6234 / 30000)

    # Calculate directivity index, assuming a circular piston receiver
    directivity_index = 10 * math.log10(36000 / float(beam_width) ** 2)

    # Calculate Transmission Loss as a function of range
    transmission_loss = lambda r: 20 * np.log10(r) + float(absorption_coefficient) * r / 1000

    # Calculate Echo Level as a function of range
    echo_level = lambda r: float(source_level) - 2 * transmission_loss(r) + float(target_strength)

    # Calculate Noise Masking Level
    noise_masking_level = noise_level - directivity_index + float(detection_threshold)

    x = np.linspace(0.1, 1500, 10000)
    el = echo_level(x)
    nml = np.full_like(x, noise_masking_level)

    # Calculate where lines cross
    eq_point = np.where(np.isclose(el, nml, 1e-3))[0][0]
    eq_point_m = x[eq_point]
    eq_point_db = el[eq_point]

    fig, ax = plt.subplots()
    plt.title("Echo Level and Noise Masking Level vs. Range")
    ax.plot(x, el, label = "Echo Level")
    ax.plot(x, nml, label = "Noise Masking Level")
    ax.plot(eq_point_m, eq_point_db, 'ro', label = f"Equivalence Point ({round(eq_point_db, 1)} dB @ {round(eq_point_m, 1)} meters)")
    ax.set_xlabel('Range (m)')
    ax.set_ylabel('Sound Pressure Level (dB re 1 uPa)')
    ax.legend()
    plt.ylim(0, 200)
    plt.show()

if __name__ == "__main__":
    cli()