import ca_chung_lib

rocket = ca_chung_lib.rocket_systems()
rocket.spoof_current_accel = True
print(rocket.current_accel)
