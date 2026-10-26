# WORK w-belt-cube-mechanism

lane: openrouter model: stealth/space-bunny-alpha
ts: 2026-10-05T16:03:17.240151+00:00
finish: stop cached_tokens: 151
ask: The belt-driven forever-rotating cube: design the actual mechanism. Three orthogonal belt loops, six face-panels with corner pinions, phase-lock tuning. What real-world components (stepper motors, GT2 belts, 3D-printed corner gears) would you use? Return a parts list and build sequence.

---

1. FINDING

The description is not yet a complete mechanism. A closed GT2 belt circulating around a square frame does not by itself rotate that frame. Each orthogonal assembly therefore needs a defined rotor, support structure, output path, and clearance envelope. Six panels also need attachment points; “corner pinions” do nothing unless each pinion meshes with a specified gear or rack.

A feasible interpretation is a three-axis nested-gimbal sculpture:

- Outer rotor: two panels on the ±X faces.
- Middle rotor: two panels on the ±Y faces.
- Inner rotor: two panels on the ±Z faces.
- Each rotor is carried by its own toothed belt.
- One stepper drives each belt.
- Panel phase is adjusted mechanically through indexed panel-to-rotor mounting positions.
- Corner pinions can index the panels, but they cannot simultaneously phase-lock three independent axes without differential gearing. Closed-loop stepper control is the safer synchronization method.

**Reference prototype parts list**

These are architecture-level choices, not a verified production BOM:

- 3 × NEMA 17 stepper motors, 1.8° or 0.9°, with rated current specified by the motor datasheet.
- 3 × GT2/HTD-3M timing belts.
- 3 × 20-tooth HTD-3M drive pulleys, one per motor.
- 3 × 20-tooth HTD-3M idler pulleys, one per belt.
- 3 × printable or commercial two-pulley belt tensioners with M3 hardware.
- 3 × rigid aluminum or acetal rotor frames.
- 6 × printed face panels, initially nonstructural.
- 24 × corner pinions if every panel has four corners.
- 24 × mating output gears or equivalent sector racks.
- For printed gearing: module 1, 20° pressure-angle geometry, at least 8 teeth per pinion, with generous backlash and steel reinforcement at hubs.
- 3 × magnetic or optical rotor sensors.
- 3 × closed-loop stepper drivers.
- 12 × M3 shoulder screws or equivalent for rotor retention.
- 1 × rigid base sized from the calculated rotor radii.
- M3 fasteners, washers, and printed belt guards.

The printed pinions are not suitable as primary load-bearing drive gears without material, tooth-root, hub, and layer-direction testing. Aluminum or acetal gears should be used for the first torque-producing prototype.

**Build sequence**

1. Choose the maximum panel size and calculate the required radius for each of the three nested rotors. Add clearance for belts, hubs, fasteners, and neighboring rotors.
2. Build three independent belt-drive cartridges. Mount each NEMA 17 to a rigid plate, fit a 20T pulley, tension the GT2/3M belt, and verify one complete pulley revolution per one belt circuit.
3. Instrument each motor with a sensor. Tune motor current and acceleration using the motor and driver datasheets, not nominal holding-current ratings.
4. Run each cartridge for at least one hour at the intended speed. Check belt tension, heat, skipped teeth, bearing play, and frame deformation.
5. Build the largest outer rotor with two opposing panels. Keep the inner rotor absent so interference is easy to inspect.
6. Add the middle rotor while leaving the inner rotor absent. Run all three axes through slow, medium, and maximum planned speeds.
7. Add the inner rotor and nonfunctional panel shells first. Measure the minimum safe angle for every axis. Stop if the physical clearance envelope has not been calculated.
8. Install the panels. Use indexed mounting positions so the centerlines of the ±X, ±Y, and ±Z panels can be established.
9. Replace the decorative corner pinions with printed prototype pinions. Use matching module, pressure angle, tooth count, and center distance. Add a removable cover before running at speed.
10. Synchronize the axes from position sensors. Do not depend on open-loop step counts for long-term phase lock.
11. Add guards, emergency stopping, current limits, and software travel or speed limits.
12. Perform a fatigue test at the intended duty cycle and record motor torque, belt tension, rotor center error, panel phase error, and temperature.

**Still owed before a final drawing or purchasable BOM**

- Overall cube dimensions.
- Panel dimensions and mass.
- Intended RPM and motion pattern.
- Belt lengths and center distances.
- Each rotor’s torque and inertia.
- Exact pinion and mating-gear tooth counts.
- Gear module, material, pressure angle, and center distances.
- Nesting radii and minimum angular clearance.
- Whether “phase-lock” means identical speed, fixed angular offset, or a repeating six-panel sequence.
- Whether the panels rotate individually or move with their supporting rotor.

2. ONE STEALABLE IDEA WORTH KEEPING

Use sensor-closed stepper control for all three axes and use the corner gears only for local panel indexing or visual synchronization. This separates motor control from gear backlash and avoids asking fragile printed pinions to hold three-dimensional phase accuracy.

3. ONE TESTABLE HYPOTHESIS

If three independently driven nested rotors use direct toothed-belt reduction, matched pulley pitches, and rotor position feedback, the sculpture can maintain a chosen fixed angular relationship among all six panel centerlines to within 0.5° while one rotor runs continuously for 24 hours, provided the measured rotor inertia remains inside each motor’s verified torque envelope.

4. EVIDENCE OR OWED

**EVIDENCE:** A closed toothed belt can transmit rotary motion between parallel shafts, and a two-pulley belt drive changes rotational speed according to pulley tooth count. An open-loop stepper can lose position after disturbance; closed-loop position feedback is therefore the appropriate research direction.

**OWED:** No specific motor, belt, printed gear, torque, clearance, belt length, phase accuracy, or endurance claim has been verified here. No dimensional design or “forever-running” claim can be made from the supplied description. **Sources: none cited; no external source verification was performed in this response.**
