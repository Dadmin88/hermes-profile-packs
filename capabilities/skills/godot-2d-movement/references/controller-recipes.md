# 2D controller recipes (Godot 4.7)

Depth companion to `godot-2d-movement`.

## Variable jump height (release to cut the jump short)

```gdscript
func _physics_process(delta: float) -> void:
    if not is_on_floor():
        velocity.y += gravity * delta
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity
    # Releasing jump early dampens upward velocity -> shorter hop.
    if Input.is_action_just_released("jump") and velocity.y < 0.0:
        velocity.y *= 0.5
    # ... horizontal + move_and_slide()
```

## Jump buffering (press slightly before landing still jumps)

```gdscript
@export var buffer_time := 0.1
var _buffer := 0.0

func _physics_process(delta: float) -> void:
    if Input.is_action_just_pressed("jump"):
        _buffer = buffer_time
    else:
        _buffer = max(_buffer - delta, 0.0)

    if _buffer > 0.0 and is_on_floor():
        velocity.y = jump_velocity
        _buffer = 0.0
    # ... gravity + horizontal + move_and_slide()
```

## One-way platforms

On the platform's `CollisionShape2D` / `CollisionPolygon2D`, enable **one-way collision**
(the editor draws an arrow). With the default `one_way_collision_direction` of
`Vector2(0, 1)` (added in 4.7; earlier versions always use this local-down direction) a
`CharacterBody2D` lands on top and passes through from below. Rotate the vector instead of
the node to make one-way walls. Raise `one_way_collision_margin` if fast bodies fall
through. To drop through deliberately, briefly clear the platform's layer from the body's
mask with `set_collision_mask_value()` for a few frames.

## Moving platforms

Make the platform an `AnimatableBody2D` (moves via animation/code, pushes bodies) and
animate it with an `AnimationPlayer` or a `Tween`. A `CharacterBody2D` standing on it
inherits the platform's velocity automatically through `move_and_slide()` (controlled by
`platform_floor_layers` and `platform_on_leave`).

## move_and_collide() — manual collision response

When you want full control (custom bounce, no sliding), use `move_and_collide()`:

```gdscript
func _physics_process(delta: float) -> void:
    var motion := velocity * delta                 # here you DO scale by delta
    var collision := move_and_collide(motion)
    if collision:
        # Reflect velocity off the surface normal (a simple bounce).
        velocity = velocity.bounce(collision.get_normal())
```

`KinematicCollision2D` exposes `get_normal()`, `get_collider()`, `get_position()`,
`get_remainder()`, and `get_travel()`.

## Acceleration-based feel

Instead of snapping `velocity.x` to `dir * speed`, ramp it for weightier movement:

```gdscript
@export var accel := 1500.0
@export var friction := 1800.0

func _physics_process(delta: float) -> void:
    var dir := Input.get_axis("move_left", "move_right")
    if dir != 0.0:
        velocity.x = move_toward(velocity.x, dir * speed, accel * delta)
    else:
        velocity.x = move_toward(velocity.x, 0.0, friction * delta)
    move_and_slide()
```

## Useful CharacterBody2D properties

- `floor_max_angle` (rad) — steepest slope still treated as floor (default 45°).
- `floor_snap_length` — keeps the body glued to downward slopes.
- `floor_stop_on_slope` — prevents sliding when idle on a slope.
- `max_slides` — iteration cap per `move_and_slide()` (default 4).
- `up_direction` — defines floor/wall/ceiling; `Vector2.UP` for side-scrollers.
- `slide_on_ceiling` — slide vs. stop when hitting a ceiling mid-jump.
