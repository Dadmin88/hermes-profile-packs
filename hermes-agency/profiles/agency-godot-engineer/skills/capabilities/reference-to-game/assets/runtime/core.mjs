/** Engine-neutral helpers. No palette, camera, genre, framework or render loop assumptions. */
export class FixedStep {
  constructor(step = 1 / 60, maxSteps = 8) {
    if (!(step > 0 && Number.isFinite(step)) || !Number.isInteger(maxSteps) || maxSteps < 1) throw new RangeError('Invalid fixed step');
    this.step = step; this.maxSteps = maxSteps; this.accumulator = 0; this.time = 0;
  }
  advance(seconds, update) {
    if (!Number.isFinite(seconds) || seconds < 0) throw new RangeError('Invalid elapsed time');
    this.accumulator += Math.min(seconds, this.step * this.maxSteps);
    let count = 0;
    while (this.accumulator + 1e-12 >= this.step && count < this.maxSteps) {
      update(this.step, this.time); this.time += this.step;
      this.accumulator = Math.max(0, this.accumulator - this.step); count++;
    }
    return Math.min(1, this.accumulator / this.step);
  }
  reset() { this.accumulator = 0; this.time = 0; }
}

export class OnceLedger {
  constructor(ids = []) { this.ids = new Set(ids); }
  claim(id) {
    if (typeof id !== 'string' || !id) throw new TypeError('Use a nonempty stable string ID');
    if (this.ids.has(id)) return false;
    this.ids.add(id); return true;
  }
  has(id) { return this.ids.has(id); }
  snapshot() { return [...this.ids].sort(); }
  reset() { this.ids.clear(); }
}

/** Returns first time of impact in [0,1] for a moving circle vs a fixed circle, or null. */
export function sweepCircle(start, end, center, combinedRadius) {
  if (![...start, ...end, ...center, combinedRadius].every(Number.isFinite) || combinedRadius < 0) throw new RangeError('Invalid sweep');
  const px = start[0] - center[0], py = start[1] - center[1];
  const dx = end[0] - start[0], dy = end[1] - start[1];
  const c = px * px + py * py - combinedRadius * combinedRadius;
  if (c <= 0) return 0;
  const a = dx * dx + dy * dy;
  if (a < 1e-20) return null;
  const b = 2 * (px * dx + py * dy), discriminant = b * b - 4 * a * c;
  if (discriminant < 0) return null;
  const t = (-b - Math.sqrt(discriminant)) / (2 * a);
  return t >= 0 && t <= 1 ? t : null;
}

/** Frame-rate-independent exponential approach; use for visual follow, not gameplay truth. */
export function damp(current, target, halfLife, dt) {
  if (![current, target, halfLife, dt].every(Number.isFinite) || halfLife <= 0 || dt < 0) throw new RangeError('Invalid damping');
  return target + (current - target) * 2 ** (-dt / halfLife);
}

/** Explicit event binding and cleanup; attachment is opt-in. */
export class InputState {
  constructor(target, documentTarget, onSuspend = () => {}) {
    this.held = new Set(); this.pressed = new Set(); this.target = target; this.documentTarget = documentTarget;
    this.down = e => { if (!this.held.has(e.code)) this.pressed.add(e.code); this.held.add(e.code); };
    this.up = e => this.held.delete(e.code);
    this.blur = () => { this.clear(); onSuspend(); };
    this.hidden = () => { if (documentTarget.hidden) this.blur(); };
    target.addEventListener('keydown', this.down); target.addEventListener('keyup', this.up);
    target.addEventListener('blur', this.blur); documentTarget.addEventListener('visibilitychange', this.hidden);
  }
  consume(code) { const present = this.pressed.has(code); this.pressed.delete(code); return present; }
  clear() { this.held.clear(); this.pressed.clear(); }
  dispose() {
    this.target.removeEventListener('keydown', this.down); this.target.removeEventListener('keyup', this.up);
    this.target.removeEventListener('blur', this.blur); this.documentTarget.removeEventListener('visibilitychange', this.hidden); this.clear();
  }
}

/** A deterministic sequence for reproducible scenery and repro cases; not cryptographic. */
export function seededRandom(seed) {
  let a = seed >>> 0;
  return () => { a += 0x6D2B79F5; let t = a; t = Math.imul(t ^ t >>> 15, t | 1); t ^= t + Math.imul(t ^ t >>> 7, t | 61); return ((t ^ t >>> 14) >>> 0) / 4294967296; };
}
