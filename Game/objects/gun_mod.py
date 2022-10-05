
class Gun_mod():
    def __init__(self, mid_pos):
        self.lazer_type = 0
        self.lazer_timer = Timer()
        self.mid_pos = mid_pos
        
    def shoot(self, angle):
        if self.lazer_type == 0:
            Lazer([mid_pos[0] - 8, mid_pos[1] - 2], -5, angle, engine_vars.lazer_group, self.lazer_type)
            Lazer([mid_pos[0] + 8, mid_pos[1] - 2], -5, angle, engine_vars.lazer_group, self.lazer_type)
            engine_funcs.play_sound(engine_vars.lazer_shooting, engine_vars.LAZER_CHANNEL)
