"""
Malware Supply Chain Simulation - Demo Script
=============================================

HOW TO RUN:
VENV Has to be enabled for simulation torun

Basic run (all defaults):
    python demo.py

Change one parameter:
    python demo.py --rollout full_push
    python demo.py --devices 200
    python demo.py --detection_delay 20

Change multiple parameters:
    python demo.py --rollout full_push --detection_delay 20 --devices 100

All available parameters:
    --devices           Number of end-user devices       (default: 100)
    --rollout           staged OR full_push              (default: staged)
    --detection_delay   Steps before detection kicks in  (default: 5)
    --defence_level     Device defence capability 0-1    (default: random 0.3-0.8)
    --trust_score       Device trust in server 0-1       (default: random 0.4-0.9)
    --execution_prob    Probability malware executes 0-1 (default: 0.3)
    --attacker_skill    Attacker capability 0-1          (default: 0.6)
"""

import sys
import os
import argparse
import matplotlib.pyplot as plt
import pandas as pd

# Make sure the project root is on the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model.malware_model import MalwareModel


# 
# 1. PARSE COMMAND LINE ARGUMENTS
# 

def parse_args():
    parser = argparse.ArgumentParser(
        description="Malware Supply Chain Simulation Demo"
    )

    parser.add_argument(
        "--devices",
        type=int,
        default=100,
        help="Number of end-user devices (default: 100)"
    )
    parser.add_argument(
        "--rollout",
        type=str,
        default="staged",
        choices=["staged", "full_push"],
        help="Rollout strategy: staged or full_push (default: staged)"
    )
    parser.add_argument(
        "--detection_delay",
        type=int,
        default=5,
        help="Steps between infection and possible detection (default: 5)"
    )
    parser.add_argument(
        "--defence_level",
        type=float,
        default=None,
        help="Fixed defence level for all devices 0-1 (default: random per device)"
    )
    parser.add_argument(
        "--trust_score",
        type=float,
        default=None,
        help="Fixed trust score for all devices 0-1 (default: random per device)"
    )
    parser.add_argument(
        "--execution_prob",
        type=float,
        default=0.3,
        help="Probability that malware executes after exposure (default: 0.3)"
    )
    parser.add_argument(
        "--attacker_skill",
        type=float,
        default=0.6,
        help="Attacker skill level 0-1 (default: 0.6)"
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=50,
        help="Number of simulation steps to run (default: 50)"
    )

    return parser.parse_args()


# 
# 2. PRINT CONFIGURATION SUMMARY
# 

def print_config(args):
    print("\n" + "=" * 60)
    print("   MALWARE SUPPLY CHAIN SIMULATION")
    print("=" * 60)
    print(f"  Devices:           {args.devices}")
    print(f"  Rollout strategy:  {args.rollout}")
    print(f"  Detection delay:   {args.detection_delay} steps")
    print(f"  Execution prob:    {args.execution_prob}")
    print(f"  Attacker skill:    {args.attacker_skill}")

    if args.defence_level is not None:
        print(f"  Defence level:     {args.defence_level} (fixed for all devices)")
    else:
        print(f"  Defence level:     random per device (0.3 - 0.8)")

    if args.trust_score is not None:
        print(f"  Trust score:       {args.trust_score} (fixed for all devices)")
    else:
        print(f"  Trust score:       random per device (0.4 - 0.9)")

    print(f"  Simulation steps:  {args.steps}")
    print("=" * 60 + "\n")


# 
# 3. BUILD AND RUN THE MODEL
# 

def run_simulation(args):
    # devices_per_step: in full_push this doesn't matter,
    # in staged we use 5 as per the project baseline
    devices_per_step = args.devices if args.rollout == "full_push" else 5

    model = MalwareModel(
        number_of_devices=args.devices,
        rollout_strategy=args.rollout,
        devices_per_step=devices_per_step,
        execution_probability=args.execution_prob,
        detection_delay=args.detection_delay
    )

    # Override attacker skill
    model.attacker.skill_level = args.attacker_skill

    # Override device attributes if fixed values were given
    for device in model.devices:
        if args.defence_level is not None:
            device.defence_level = args.defence_level
        if args.trust_score is not None:
            device.trust_score = args.trust_score

    print("Running simulation", end="", flush=True)

    for i in range(args.steps):
        model.step()
        if (i + 1) % 10 == 0:
            print(".", end="", flush=True)

    print(" done!\n")
    return model


# 
# 4. PRINT RESULTS SUMMARY
# 

def print_results(model, args):
    df = model.datacollector.get_model_vars_dataframe()

    peak_exposed    = df['Exposed'].max()
    peak_infected   = df['Infected'].max()
    final_recovered = df['Recovered'].iloc[-1]
    final_infected  = df['Infected'].iloc[-1]

    compromise_step = model.update_server.compromise_step
    time_to_peak    = int(df['Infected'].idxmax()) if peak_infected > 0 else "N/A"

    print("=" * 60)
    print("   SIMULATION RESULTS")
    print("=" * 60)
    print(f"  Server compromised at step: {compromise_step}")
    print(f"  Peak devices exposed:       {peak_exposed}")
    print(f"  Peak devices infected:      {peak_infected}")
    print(f"  Time to peak infection:     step {time_to_peak}")
    print(f"  Devices recovered by end:   {final_recovered}")
    print(f"  Devices still infected:     {final_infected}")
    print("=" * 60 + "\n")

    return df


# 
# 5. PLOT THE SEIR CURVE
# 

def plot_results(df, args):
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(df.index, df['Susceptible'], label='Susceptible (S)',
            color='steelblue',  linewidth=2)
    ax.plot(df.index, df['Exposed'],    label='Exposed (E)',
            color='gold',       linewidth=2)
    ax.plot(df.index, df['Infected'],   label='Infected (I)',
            color='crimson',    linewidth=2)
    ax.plot(df.index, df['Recovered'],  label='Recovered (R)',
            color='seagreen',   linewidth=2)

    ax.set_xlabel('Simulation Step', fontsize=12)
    ax.set_ylabel('Number of Devices', fontsize=12)
    ax.set_title(
        f"SEIR Dynamics — {args.rollout.replace('_', ' ').title()} | "
        f"{args.devices} Devices | Detection Delay: {args.detection_delay}",
        fontsize=13
    )
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, args.devices + 5)

    plt.tight_layout()
    plt.savefig("demo_output.png", dpi=150)
    print("  Plot saved as: demo_output.png")
    plt.show()


# 
# 6. MAIN ENTRY POINT
# 

if __name__ == "__main__":
    args = parse_args()
    print_config(args)
    model = run_simulation(args)
    df = print_results(model, args)
    plot_results(df, args)