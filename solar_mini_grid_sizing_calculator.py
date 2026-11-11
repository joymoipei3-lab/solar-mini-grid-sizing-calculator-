
# SOLAR MINI-GRID SIZING CALCULATOR
# With an Intelligent Design Explainer
# Python 3.11.9

import math


def get_appliance_data():
    appliances = []

    print("\n--- ENTER APPLIANCE DETAILS ---")
    print("Enter 'done' when you have finished.\n")

    while True:
        name = input("Appliance name: ")

        if name.lower() == "done":
            break

        try:
            quantity = int(input("Quantity: "))
            power = float(input("Power rating per appliance (W): "))
            hours = float(input("Hours used per day: "))

            if quantity <= 0 or power <= 0 or hours < 0 or hours > 24:
                print("Invalid values. Please try again.\n")
                continue

            daily_energy = quantity * power * hours

            appliances.append({
                "name": name,
                "quantity": quantity,
                "power": power,
                "hours": hours,
                "energy": daily_energy
            })

        except ValueError:
            print("Please enter valid numerical values.\n")

    return appliances


def calculate_system(appliances):

    # System design assumptions
    peak_sun_hours = 5.0
    pv_derating_factor = 0.75
    battery_dod = 0.80
    inverter_efficiency = 0.90
    autonomy_days = 1
    safety_factor = 1.25
    panel_rating = 550

    # System voltage selection
    system_voltage = 48

    # Calculate energy requirements
    daily_energy = sum(a["energy"] for a in appliances)

    peak_load = sum(
        a["quantity"] * a["power"] for a in appliances
    )

    # Solar panel sizing
    pv_capacity = (
        daily_energy * safety_factor /
        (peak_sun_hours * pv_derating_factor)
    )

    number_of_panels = math.ceil(pv_capacity / panel_rating)

    actual_pv_capacity = number_of_panels * panel_rating

    # Battery sizing
    battery_capacity_wh = (
        daily_energy * autonomy_days /
        (battery_dod * inverter_efficiency)
    )

    battery_capacity_ah = battery_capacity_wh / system_voltage

    # Inverter sizing
    inverter_capacity = peak_load * safety_factor

    # Charge controller sizing
    controller_current = (
        actual_pv_capacity / system_voltage
    ) * safety_factor

    return {
        "daily_energy": daily_energy,
        "peak_load": peak_load,
        "pv_capacity": pv_capacity,
        "number_of_panels": number_of_panels,
        "actual_pv_capacity": actual_pv_capacity,
        "battery_wh": battery_capacity_wh,
        "battery_ah": battery_capacity_ah,
        "inverter": inverter_capacity,
        "controller": controller_current,
        "voltage": system_voltage
    }


def explain_results(results):

    print("\n========== INTELLIGENT DESIGN EXPLANATION ==========")

    print(
        f"\n1. ENERGY DEMAND:\n"
        f"The community requires {results['daily_energy']:.2f} Wh "
        f"of energy per day. This is the energy the mini-grid "
        f"must supply daily."
    )

    print(
        f"\n2. SOLAR PANELS:\n"
        f"The estimated PV requirement is "
        f"{results['pv_capacity']:.2f} W. "
        f"We recommend {results['number_of_panels']} panels "
        f"rated at 550 W each. The extra capacity helps "
        f"account for system losses and design margin."
    )

    print(
        f"\n3. BATTERY BANK:\n"
        f"The required nominal battery capacity is "
        f"{results['battery_wh'] / 1000:.2f} kWh "
        f"({results['battery_ah']:.2f} Ah at "
        f"{results['voltage']} V). "
        f"This provides approximately one day of autonomy "
        f"under the stated assumptions."
    )

    print(
        f"\n4. INVERTER:\n"
        f"The estimated peak load is "
        f"{results['peak_load']:.2f} W. "
        f"The recommended minimum inverter rating is "
        f"{results['inverter']:.2f} W, before checking "
        f"motor starting and other surge requirements."
    )

    print(
        f"\n5. CHARGE CONTROLLER:\n"
        f"The estimated minimum controller current is "
        f"{results['controller']:.2f} A at "
        f"{results['voltage']} V. "
        f"The actual controller must also satisfy "
        f"PV voltage and manufacturer specifications."
    )


def main():

    print("============================================")
    print("   SOLAR MINI-GRID SIZING CALCULATOR")
    print("       WITH AI EXPLAINER")
    print("============================================")

    appliances = get_appliance_data()

    if not appliances:
        print("No appliance data entered. Program stopped.")
        return

    results = calculate_system(appliances)

    print("\n========== SYSTEM SIZING RESULTS ==========")

    print(f"Daily energy demand: {results['daily_energy']:.2f} Wh")
    print(f"Peak load demand: {results['peak_load']:.2f} W")

    print(f"\nSolar PV capacity: {results['pv_capacity']:.2f} W")
    print(f"Recommended panels: {results['number_of_panels']}")
    print(f"Installed PV capacity: {results['actual_pv_capacity']} W")

    print(f"\nBattery capacity: {results['battery_wh'] / 1000:.2f} kWh")
    print(f"Battery capacity: {results['battery_ah']:.2f} Ah")
    print(f"System voltage: {results['voltage']} V")

    print(f"\nMinimum inverter rating: {results['inverter']:.2f} W")
    print(f"Charge controller current: {results['controller']:.2f} A")

    explain_results(results)

    print("\n============================================")
    print("       END OF SYSTEM DESIGN")
    print("============================================")


if __name__ == "__main__":
    main()
