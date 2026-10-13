extends Node2D
## Player — the shepherd. Follows the mouse (the catch mechanic is
## pixel-proximity tuned: CATCH_RADIUS 3.5 in flock.gd assumes cursor
## precision, same as the swarm.html DNA). Clamped to the board.

const BOARD := Rect2(16, 16, 1120, 616)


func _process(_delta: float) -> void:
    var target := get_global_mouse_position()
    global_position = target.clamp(BOARD.position, BOARD.end)
