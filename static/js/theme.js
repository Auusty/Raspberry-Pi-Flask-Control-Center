// static/js/theme.js
/* ==================================================
   Motion presets
================================================== */
const MOTION_PRESETS = {
  instant: {
    pageIn: "0ms",
    pageOut: "0ms",
    fadeFast: "0ms",
    fadeMedium: "0ms",
    ease: "linear",
  },

  snappy: {
    pageIn: "90ms",
    pageOut: "80ms",
    fadeFast: "100ms",
    fadeMedium: "140ms",
    ease: "ease-out",
  },

  balanced: {
    pageIn: "100ms",
    pageOut: "90ms",
    fadeFast: "120ms",
    fadeMedium: "160ms",
    ease: "ease-out",
  },

  smooth: {
    pageIn: "140ms",
    pageOut: "120ms",
    fadeFast: "180ms",
    fadeMedium: "220ms",
    ease: "cubic-bezier(.25,.8,.25,1)",
  },

  floaty: {
    pageIn: "180ms",
    pageOut: "160ms",
    fadeFast: "240ms",
    fadeMedium: "300ms",
    ease: "cubic-bezier(.22,1,.36,1)",
  },
};

/* ==================================================
   Aurora accent animation colors
================================================== */
const AURORA_COLORS = [
  "#22d3ee", // cyan
  "#34d399", // green
  "#a78bfa", // violet
  "#60a5fa", // blue
  "#5eead4", // teal
];

/* ==================================================
   Surface definitions (material / gloss)
================================================== */
const SURFACES = {
  /* ===== Neutral / Base ===== */
  flat: {
    label: "Flat",
    vars: { gloss: 0, blur: 0, softness: 0, hardness: 0, glow: 0 },
  },

  soft_matte: {
    label: "Soft Matte",
    vars: { gloss: 0.15, blur: 0, softness: 0.5, hardness: 0, glow: 0 },
  },

  satin: {
    label: "Satin",
    vars: { gloss: 0.6, blur: 0, softness: 0.2, hardness: 0.1, glow: 0 },
  },

  clay: {
    label: "Clay",
    vars: { gloss: 0, blur: 0, softness: 1, hardness: 0, glow: 0 },
  },

  /* ===== Hardware / Industrial ===== */
  brushed: {
    label: "Brushed",
    vars: { gloss: 0.35, blur: 0, softness: 0.1, hardness: 0.4, glow: 0 },
  },

  oled_black: {
    label: "OLED Black",
    vars: { gloss: 0, blur: 0, softness: 0, hardness: 0.6, glow: 0 },
  },

  /* ===== Gloss / Premium ===== */
  glossy: {
    label: "Glossy",
    vars: { gloss: 1, blur: 0, softness: 0.1, hardness: 0.2, glow: 0 },
  },

  deep_gloss: {
    label: "Deep Gloss",
    vars: { gloss: 1.2, blur: 0, softness: 0.05, hardness: 0.3, glow: 0 },
  },

  /* ===== Glass / Translucent ===== */
  glass: {
    label: "Glass",
    vars: { gloss: 0.85, blur: 10, softness: 0.15, hardness: 0, glow: 0 },
  },

  frosted: {
    label: "Frosted",
    vars: { gloss: 0.35, blur: 16, softness: 0.45, hardness: 0, glow: 0 },
  },

    opaque_glass: {
    label: "Opaque Glass",
    vars: {gloss: 0.75, blur: 20, softness: 0.3, hardness: 0.12, glow: 0.2,},
  },

  liquid_glass: {
    label: "Liquid Glass",
    vars: { gloss: 1, blur: 14, softness: 0.35, hardness: 0, glow: 0 },
  },

  crystal: {
  label: "Crystal",
  vars: {gloss: 1, blur: 22, softness: 0.15, hardness: 0.2, glow: 0.25,},
  },

  /* ===== Glow / Accent ===== */
  soft_glow: {
    label: "Soft Glow",
    vars: { gloss: 0.3, blur: 0, softness: 0.25, hardness: 0, glow: 0.25 },
  },

  inner_glow: {
    label: "Inner Glow",
    vars: { gloss: 0.6, blur: 0, softness: 0.2, hardness: 0, glow: 0.6 },
  },

  neon: {
    label: "Neon",
    vars: { gloss: 0.55, blur: 0, softness: 0, hardness: 0.25, glow: 0.85 },
  },

  frosted_neon: {
    label: "Frosted Neon",
    vars: { gloss: 0.5, blur: 12, softness: 0.25, hardness: 0, glow: 0.75 },
  },

  /* ===== Light / Paper ===== */
  paper_card: {
    label: "Paper",
    vars: { gloss: 0, blur: 0, softness: 0.8, hardness: 0, glow: 0 },
  },
};

const SURFACE_ORDER = [
  // Base
  "flat",
  "soft_matte",
  "satin",
  "clay",

  // Hardware
  "brushed",
  "oled_black",

  // Gloss
  "glossy",
  "deep_gloss",

  // Glass
  "glass",
  "frosted",
  "opaque_glass",
  "liquid_glass",
  "crystal",

  // Glow
  "soft_glow",
  "inner_glow",
  "neon",
  "frosted_neon",

  // Paper
  "paper_card",
];

/* ==================================================
   Theme definitions (motion-enabled + gradients)
================================================== */
const THEMES = {
  midnight: {
    bg: "#141221",
    panel: "#221f36",
    tile: "#221f36",
    text: "#ffffff",
    muted: "#9a93b4",
    accent: "#4caf50",
    powerOn: "#27ae60",
    powerOff: "#e74c3c",
    motion: "balanced",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(76,175,80,0.14), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(76,175,80,0.14), rgba(76,175,80,0.03), rgba(76,175,80,0.14))",
  },

  slate: {
    bg: "#161a1f",
    panel: "#1f242b",
    tile: "#1f242b",
    text: "#e6e6e6",
    muted: "#9aa4b2",
    accent: "#4fc3f7",
    powerOn: "#2ecc71",
    powerOff: "#e74c3c",
    motion: "snappy",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(79,195,247,0.14), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(79,195,247,0.14), rgba(79,195,247,0.03), rgba(79,195,247,0.14))",
  },

  graphite: {
    bg: "#0f1115",
    panel: "#171a20",
    tile: "#171a20",
    text: "#f5f5f5",
    muted: "#8a8f98",
    accent: "#90caf9",
    powerOn: "#66bb6a",
    powerOff: "#ef5350",
    motion: "snappy",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(144,202,249,0.16), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(144,202,249,0.16), rgba(144,202,249,0.04), rgba(144,202,249,0.16))",
  },

  deep_space: {
    bg: "#05070c",
    panel: "#0b1020",
    tile: "#0b1020",
    text: "#e6ecff",
    muted: "#7f89b5",
    accent: "#5c7cfa",
    powerOn: "#4ade80",
    powerOff: "#f87171",
    motion: "smooth",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(92,124,250,0.18), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(92,124,250,0.18), rgba(92,124,250,0.05), rgba(92,124,250,0.18))",
  },

  frost: {
    bg: "#0f172a",
    panel: "#162036",
    tile: "#162036",
    text: "#f1f5f9",
    muted: "#94a3b8",
    accent: "#38bdf8",
    powerOn: "#22c55e",
    powerOff: "#ef4444",
    motion: "smooth",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(56,189,248,0.18), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(56,189,248,0.16), rgba(56,189,248,0.04), rgba(56,189,248,0.16))",
  },

  forest: {
    bg: "#0f1b14",
    panel: "#15261c",
    tile: "#15261c",
    text: "#e6f4ea",
    muted: "#9fb5a8",
    accent: "#34d399",
    powerOn: "#22c55e",
    powerOff: "#ef4444",
    motion: "floaty",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(52,211,153,0.2), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(52,211,153,0.18), rgba(52,211,153,0.05), rgba(52,211,153,0.18))",
  },

  ember: {
    bg: "#140a0a",
    panel: "#1f0f0f",
    tile: "#1f0f0f",
    text: "#fff1f1",
    muted: "#b89a9a",
    accent: "#fb7185",
    powerOn: "#f97316",
    powerOff: "#ef4444",
    motion: "smooth",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(251,113,133,0.22), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(251,113,133,0.2), rgba(251,113,133,0.06), rgba(251,113,133,0.2))",
  },

  synthwave: {
    bg: "#120018",
    panel: "#1e0030",
    tile: "#1e0030",
    text: "#f8f7ff",
    muted: "#b3a1c7",
    accent: "#e879f9",
    powerOn: "#22d3ee",
    powerOff: "#fb7185",
    motion: "floaty",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(232,121,249,0.22), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(232,121,249,0.22), rgba(232,121,249,0.06), rgba(232,121,249,0.22))",
  },

  mocha: {
    bg: "#140f0a",
    panel: "#1f1812",
    tile: "#1f1812",
    text: "#f5efe8",
    muted: "#b8a99a",
    accent: "#c08457",
    powerOn: "#65a30d",
    powerOff: "#dc2626",
    motion: "smooth",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(192,132,87,0.2), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(192,132,87,0.18), rgba(192,132,87,0.05), rgba(192,132,87,0.18))",
  },

  stone: {
    bg: "#121212",
    panel: "#1e1e1e",
    tile: "#1e1e1e",
    text: "#f5f5f5",
    muted: "#a3a3a3",
    accent: "#a3a3a3",
    powerOn: "#4ade80",
    powerOff: "#f87171",
    motion: "instant",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(163,163,163,0.12), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02), rgba(255,255,255,0.06))",
  },

  obsidian: {
    bg: "#0b0d10",
    panel: "#12151a",
    tile: "#12151a",
    text: "#e5e7eb",
    muted: "#9ca3af",
    accent: "#60a5fa",
    powerOn: "#22c55e",
    powerOff: "#ef4444",
    motion: "balanced",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(96,165,250,0.18), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(96,165,250,0.16), rgba(96,165,250,0.04), rgba(96,165,250,0.16))",
  },

  night_ocean: {
    bg: "#020617",
    panel: "#020b2d",
    tile: "#020b2d",
    text: "#e0f2fe",
    muted: "#7dd3fc",
    accent: "#38bdf8",
    powerOn: "#4ade80",
    powerOff: "#f87171",
    motion: "smooth",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(56,189,248,0.22), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(56,189,248,0.18), rgba(56,189,248,0.05), rgba(56,189,248,0.18))",
  },

  aurora: {
    bg: "#031712",
    panel: "#04261d",
    tile: "#04261d",
    text: "#ecfdf5",
    muted: "#6ee7b7",
    accent: "#34d399",
    powerOn: "#22c55e",
    powerOff: "#fb7185",
    motion: "floaty",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(52,211,153,0.25), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(52,211,153,0.22), rgba(52,211,153,0.06), rgba(52,211,153,0.22))",
  },

  dusk: {
    bg: "#120d0a",
    panel: "#1c1410",
    tile: "#1c1410",
    text: "#fef3c7",
    muted: "#fcd34d",
    accent: "#fb923c",
    powerOn: "#f59e0b",
    powerOff: "#ef4444",
    motion: "smooth",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(251,146,60,0.24), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(251,146,60,0.2), rgba(251,146,60,0.06), rgba(251,146,60,0.2))",
  },

  cyberpunk: {
    bg: "#05010d",
    panel: "#0d0221",
    tile: "#0d0221",
    text: "#fdf4ff",
    muted: "#c084fc",
    accent: "#ec4899",
    powerOn: "#22d3ee",
    powerOff: "#fb7185",
    motion: "snappy",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(236,72,153,0.26), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(236,72,153,0.24), rgba(236,72,153,0.07), rgba(236,72,153,0.24))",
  },

  matrix: {
    bg: "#020a02",
    panel: "#031703",
    tile: "#031703",
    text: "#bbf7d0",
    muted: "#4ade80",
    accent: "#22c55e",
    powerOn: "#16a34a",
    powerOff: "#dc2626",
    motion: "instant",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(34,197,94,0.22), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(34,197,94,0.2), rgba(34,197,94,0.06), rgba(34,197,94,0.2))",
  },

  paper: {
    bg: "#fafafa",
    panel: "#f0f0f0",
    tile: "#f0f0f0",
    text: "#111827",
    muted: "#6b7280",
    accent: "#2563eb",
    powerOn: "#16a34a",
    powerOff: "#dc2626",
    motion: "instant",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(37,99,235,0.12), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(0,0,0,0.04), rgba(0,0,0,0.02), rgba(0,0,0,0.04))",
  },

  steel: {
    bg: "#0f172a",
    panel: "#1e293b",
    tile: "#1e293b",
    text: "#e5e7eb",
    muted: "#94a3b8",
    accent: "#64748b",
    powerOn: "#22c55e",
    powerOff: "#ef4444",
    motion: "balanced",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(100,116,139,0.18), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(148,163,184,0.14), rgba(148,163,184,0.04), rgba(148,163,184,0.14))",
  },

  vapor_gray: {
    bg: "#18181b",
    panel: "#27272a",
    tile: "#27272a",
    text: "#fafafa",
    muted: "#a1a1aa",
    accent: "#a78bfa",
    powerOn: "#4ade80",
    powerOff: "#f87171",
    motion: "balanced",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(167,139,250,0.18), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(167,139,250,0.16), rgba(167,139,250,0.04), rgba(167,139,250,0.16))",
  },

  blood_moon: {
    bg: "#0a0202",
    panel: "#160404",
    tile: "#160404",
    text: "#fee2e2",
    muted: "#fca5a5",
    accent: "#dc2626",
    powerOn: "#f97316",
    powerOff: "#991b1b",
    motion: "smooth",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(220,38,38,0.28), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(220,38,38,0.24), rgba(220,38,38,0.07), rgba(220,38,38,0.24))",
  },
};

/* ==================================================
   Advanced / Signature Themes
================================================== */
const ADVANCED_THEMES = {
  terminal_green: {
    bg: "#020a02",
    panel: "#031703",
    tile: "#031703",
    text: "#bbf7d0",
    muted: "#4ade80",
    accent: "#22c55e",
    powerOn: "#16a34a",
    powerOff: "#dc2626",
    motion: "instant",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(34,197,94,0.22), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(34,197,94,0.2), rgba(34,197,94,0.06), rgba(34,197,94,0.2))",
  },

  ice_lab: {
    bg: "#020617",
    panel: "#0b1224",
    tile: "#0b1224",
    text: "#e0f2fe",
    muted: "#7dd3fc",
    accent: "#38bdf8",
    powerOn: "#22d3ee",
    powerOff: "#fb7185",
    motion: "smooth",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(56,189,248,0.24), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(56,189,248,0.22), rgba(56,189,248,0.06), rgba(56,189,248,0.22))",
  },

  sunset_glow: {
    bg: "#140c1c",
    panel: "#2a102e",
    tile: "#2a102e",
    text: "#fff7ed",
    muted: "#fdba74",
    accent: "#fb923c",
    powerOn: "#facc15",
    powerOff: "#ef4444",
    motion: "floaty",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(251,146,60,0.3), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(251,146,60,0.26), rgba(251,146,60,0.08), rgba(251,146,60,0.26))",
  },

  mono_accent: {
    bg: "#0a0a0a",
    panel: "#151515",
    tile: "#151515",
    text: "#f5f5f5",
    muted: "#a3a3a3",
    accent: "#facc15",
    powerOn: "#22c55e",
    powerOff: "#ef4444",
    motion: "snappy",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(250,204,21,0.22), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(250,204,21,0.18), rgba(250,204,21,0.05), rgba(250,204,21,0.18))",
  },

  aurora_dynamic: {
    bg: "#020617",
    panel: "#020b2d",
    tile: "#020b2d",
    text: "#e0f2fe",
    muted: "#7dd3fc",
    accent: "#22d3ee",
    powerOn: "#4ade80",
    powerOff: "#f87171",
    animatedAccent: true,
    motion: "floaty",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(34,211,238,0.28), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(34,211,238,0.24), rgba(34,211,238,0.07), rgba(34,211,238,0.24))",
  },

  noir_red: {
    bg: "#050505",
    panel: "#120606",
    tile: "#120606",
    text: "#fef2f2",
    muted: "#fca5a5",
    accent: "#dc2626",
    powerOn: "#f97316",
    powerOff: "#7f1d1d",
    motion: "snappy",

    bgGradient:
      "radial-gradient(140% 90% at 50% -30%, rgba(220,38,38,0.3), transparent 65%)",
    tileGradient:
      "linear-gradient(140deg, rgba(220,38,38,0.26), rgba(220,38,38,0.08), rgba(220,38,38,0.26))",
  },
};

const THEME_ORDER = [
  // Core dark
  "midnight",
  "obsidian",
  "slate",
  "graphite",
  "deep_space",
  "night_ocean",

  // Nature
  "forest",
  "aurora",

  // Warm / moody
  "mocha",
  "ember",
  "dusk",
  "blood_moon",

  // Neon / cyber
  "synthwave",
  "cyberpunk",
  "matrix",

  // Clean
  "stone",
  "steel",
  "paper",

  // Experimental
  "vapor_gray",

  // Advanced / Signature
  "terminal_green",
  "ice_lab",
  "sunset_glow",
  "mono_accent",
  "aurora_dynamic",
  "noir_red",
];

const THEME_GROUPS = [
  {
    label: "Core Dark",
    themes: ["midnight", "obsidian", "slate", "graphite", "deep_space", "night_ocean"],
  },
  {
    label: "Nature",
    themes: ["forest", "aurora"],
  },
  {
    label: "Warm / Moody",
    themes: ["mocha", "ember", "dusk", "blood_moon"],
  },
  {
    label: "Neon / Cyber",
    themes: ["synthwave", "cyberpunk", "matrix"],
  },
  {
    label: "Clean / Minimal",
    themes: ["stone", "steel", "paper"],
  },
  {
    label: "Experimental",
    themes: ["vapor_gray"],
  },
  {
    label: "Signature",
    themes: [
      "terminal_green",
      "ice_lab",
      "sunset_glow",
      "mono_accent",
      "aurora_dynamic",
      "noir_red",
    ],
  },
];

/* ==================================================
   Merge advanced themes into main theme map
================================================== */
Object.assign(THEMES, ADVANCED_THEMES);

/* ==================================================
   Internal state
================================================== */
let currentThemeIndex = 0;
let themeToastTimeout = null;
let surfaceToastTimeout = null;

/* ==================================================
   Pretty name
================================================== */
function prettyThemeName(themeKey) {
  return themeKey.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase());
}

function prettySurfaceName(surfaceKey) {
  return SURFACES[surfaceKey]?.label || prettyThemeName(surfaceKey);
}

/* ==================================================
   Apply motion preset to :root
================================================== */
function applyMotionPreset(presetName) {
  const preset = MOTION_PRESETS[presetName];
  if (!preset) return;

  const root = document.documentElement;

  root.style.setProperty("--page-in", preset.pageIn);
  root.style.setProperty("--page-out", preset.pageOut);
  root.style.setProperty("--fade-fast", preset.fadeFast);
  root.style.setProperty("--fade-medium", preset.fadeMedium);
  root.style.setProperty("--motion-ease", preset.ease);

  const bgSpeedMap = {
    instant: "0s",
    snappy: "10s",
    balanced: "18s",
    smooth: "26s",
    floaty: "40s",
  };

  root.style.setProperty(
    "--bg-gradient-speed",
    bgSpeedMap[presetName] || "18s"
  );

  localStorage.setItem("ui-motion", presetName);
}

/* ==================================================
   Apply theme to :root
================================================== */
function applyTheme(themeName) {
  const theme = THEMES[themeName];
  if (!theme) return;

  const root = document.documentElement;

  // Apply motion preset (safe)
  if (theme.motion && MOTION_PRESETS[theme.motion]) {
    applyMotionPreset(theme.motion);
  }

  root.dataset.theme = themeName;

  root.style.setProperty("--bg", theme.bg);

  // Background gradient
  if (theme.bgGradient) {
    root.style.setProperty("--bg-gradient", theme.bgGradient);
  }

  if (theme.tileGradient) {
    root.style.setProperty("--tile-gradient", theme.tileGradient);
  }

  root.style.setProperty(
    "--tile-gradient-size",
    theme.tileGradientSize || "600% 600%"
  );

  root.style.setProperty("--panel", theme.panel);
  root.style.setProperty("--tile", theme.tile);
  root.style.setProperty("--text", theme.text);
  root.style.setProperty("--muted", theme.muted);

  if (!theme.animatedAccent) {
    root.style.setProperty("--accent", theme.accent);
  }

  root.style.setProperty("--power-on", theme.powerOn);
  root.style.setProperty("--power-off", theme.powerOff);

  localStorage.setItem("ui-theme", themeName);

  if (theme.animatedAccent) {
    startAuroraAccent();
  } else {
    stopAuroraAccent();
  }
}

/* ==================================================
   Apply surface to :root
================================================== */
function applySurface(surfaceName) {
  const surface = SURFACES[surfaceName];
  if (!surface) return;

  const root = document.documentElement;

  root.dataset.surface = surfaceName;

  root.style.setProperty("--tile-gloss", surface.vars.gloss);
  root.style.setProperty("--tile-blur", surface.vars.blur);
  root.style.setProperty("--tile-softness", surface.vars.softness);
  root.style.setProperty("--tile-hardness", surface.vars.hardness);
  root.style.setProperty("--tile-glow", surface.vars.glow);

  localStorage.setItem("ui-surface", surfaceName);
}

/* ==================================================
   Toasts
================================================== */
function showThemeToast(themeName) {
  let toast = document.getElementById("theme-toast");

  if (!toast) {
    toast = document.createElement("div");
    toast.id = "theme-toast";
    document.body.appendChild(toast);
  }

  toast.textContent = `Theme: ${prettyThemeName(themeName)}`;
  toast.classList.add("show");

  clearTimeout(themeToastTimeout);
  themeToastTimeout = setTimeout(() => toast.classList.remove("show"), 1000);
}

function showSurfaceToast(surfaceName) {
  let toast = document.getElementById("surface-toast");

  if (!toast) {
    toast = document.createElement("div");
    toast.id = "surface-toast";
    document.body.appendChild(toast);
  }

  toast.textContent = `Surface: ${prettySurfaceName(surfaceName)}`;
  toast.classList.add("show");

  clearTimeout(surfaceToastTimeout);
  surfaceToastTimeout = setTimeout(() => toast.classList.remove("show"), 1000);
}

/* ==================================================
   Inject styles (toast + dropdown) once
================================================== */
(function injectThemeStyles() {
  if (document.getElementById("theme-style")) return;

  const style = document.createElement("style");
  style.id = "theme-style";
  style.textContent = `
    /* ===== Toasts ===== */
    #theme-toast, #surface-toast {
      position: fixed;
      left: 50%;
      transform: translateX(-50%) translateY(10px);
      padding: 10px 18px;

      background: var(--panel);
      color: var(--text);
      border-radius: 999px;

      font-size: 0.95rem;
      font-weight: 700;
      letter-spacing: 0.04em;

      box-shadow:
        0 6px 18px rgba(0,0,0,0.6),
        inset 0 0 0 1px rgba(255,255,255,0.06);

      opacity: 0;
      pointer-events: none;
      transition: opacity 0.25s ease, transform 0.25s ease;

      z-index: 9999;
    }

    #theme-toast { bottom: 28px; }
    #surface-toast { bottom: 76px; }

    #theme-toast.show, #surface-toast.show {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }

    /* ===== Dropdown overlay ===== */
    #theme-dropdown, #surface-dropdown {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.45);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 9998;
    }

    #theme-dropdown.hidden,
    #surface-dropdown.hidden { display: none; }

    #theme-dropdown .panel,
    #surface-dropdown .panel {
      background: var(--tile);
      border-radius: 16px;
      padding: 12px;
      width: 80%;
      max-height: 60vh;
      overflow-y: auto;
      box-shadow: 0 18px 40px rgba(0,0,0,0.55);
    }

    #theme-dropdown .item,
    #surface-dropdown .item {
      padding: 12px;
      border-radius: 10px;
      cursor: pointer;
      user-select: none;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }

    #theme-dropdown .item:active,
    #surface-dropdown .item:active {
      background: rgba(255,255,255,.08);
    }

    #theme-dropdown .item .name {
      font-weight: 800;
      color: var(--text);
    }

    #theme-dropdown .item .dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--muted);
      opacity: 0.6;
    }

    #theme-dropdown .item.active,
    #surface-dropdown .item.active {
      outline: 2px solid color-mix(in srgb, var(--accent) 90%, transparent);
      outline-offset: -2px;
      box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--accent) 35%, transparent);
    }

    /* Hide scrollbar but keep scroll */
    #theme-dropdown .panel,
    #surface-dropdown .panel {
      scrollbar-width: none;
      -ms-overflow-style: none;
    }
    #theme-dropdown .panel::-webkit-scrollbar,
    #surface-dropdown .panel::-webkit-scrollbar {
      width: 0;
      height: 0;
      display: none;
    }
  `;
  document.head.appendChild(style);
})();

/* ==================================================
   Cycle theme (tap)
================================================== */
function cycleTheme() {
  currentThemeIndex = (currentThemeIndex + 1) % THEME_ORDER.length;
  const nextTheme = THEME_ORDER[currentThemeIndex];
  applyTheme(nextTheme);
  showThemeToast(nextTheme);
}

/* ==================================================
   Cycle surface (tap)
================================================== */
function cycleSurface() {
  const current = localStorage.getItem("ui-surface") || SURFACE_ORDER[0];
  const next =
    SURFACE_ORDER[(SURFACE_ORDER.indexOf(current) + 1) % SURFACE_ORDER.length];

  applySurface(next);
  showSurfaceToast(next);
}

/* ==================================================
   Theme dropdown (hold)
================================================== */
function ensureThemeDropdown() {
  let wrap = document.getElementById("theme-dropdown");
  if (wrap) return wrap;

  wrap = document.createElement("div");
  wrap.id = "theme-dropdown";
  wrap.className = "hidden";
  wrap.innerHTML = `<div class="panel" id="theme-dropdown-panel"></div>`;
  document.body.appendChild(wrap);

  wrap.addEventListener("click", () => wrap.classList.add("hidden"));
  wrap.querySelector(".panel").addEventListener("click", (e) => e.stopPropagation());

  return wrap;
}

function openThemePicker() {
  const wrap = ensureThemeDropdown();
  const panel = document.getElementById("theme-dropdown-panel");
  if (!panel) return;

  const active = localStorage.getItem("ui-theme") || THEME_ORDER[0];
  panel.innerHTML = "";

  THEME_GROUPS.forEach((group) => {
    const header = document.createElement("div");
    header.textContent = group.label.toUpperCase();
    header.style.cssText = `
      margin: 14px 6px 6px;
      font-size: 0.7rem;
      font-weight: 900;
      letter-spacing: 0.12em;
      color: var(--muted);
      opacity: 0.8;
    `;
    panel.appendChild(header);

    group.themes.forEach((key) => {
      const row = document.createElement("div");
      row.className = "item" + (key === active ? " active" : "");

      row.innerHTML = `
        <div class="name">${prettyThemeName(key)}</div>
        <div class="dot" style="background:${THEMES[key].accent}"></div>
      `;

      row.onclick = () => {
        wrap.classList.add("hidden");
        applyTheme(key);
        showThemeToast(key);
      };

      panel.appendChild(row);
    });
  });

  wrap.classList.remove("hidden");
}

/* ==================================================
   Surface dropdown (hold)
================================================== */
function ensureSurfaceDropdown() {
  let wrap = document.getElementById("surface-dropdown");
  if (wrap) return wrap;

  wrap = document.createElement("div");
  wrap.id = "surface-dropdown";
  wrap.className = "hidden";
  wrap.innerHTML = `<div class="panel" id="surface-dropdown-panel"></div>`;
  document.body.appendChild(wrap);

  wrap.addEventListener("click", () => wrap.classList.add("hidden"));
  wrap.querySelector(".panel").addEventListener("click", (e) => e.stopPropagation());

  return wrap;
}

function openSurfacePicker() {
  const wrap = ensureSurfaceDropdown();
  const panel = document.getElementById("surface-dropdown-panel");
  if (!panel) return;

  const active = localStorage.getItem("ui-surface") || SURFACE_ORDER[0];
  panel.innerHTML = "";

  // simple list (no groups)
  SURFACE_ORDER.forEach((key) => {
    const row = document.createElement("div");
    row.className = "item" + (key === active ? " active" : "");

    row.innerHTML = `
      <div class="name">${prettySurfaceName(key)}</div>
      <div class="dot" style="background: var(--accent)"></div>
    `;

    row.onclick = () => {
      wrap.classList.add("hidden");
      applySurface(key);
      showSurfaceToast(key);
    };

    panel.appendChild(row);
  });

  wrap.classList.remove("hidden");
}

/* ==================================================
   Attach long-press behavior
================================================== */
(function attachButtons() {
  const themeButtons = [
    ...document.querySelectorAll(".theme-btn"),
    ...document.querySelectorAll("#themeToggleBtn"),
  ];

  const surfaceButtons = [
    ...document.querySelectorAll(".surface-btn"),
    ...document.querySelectorAll("#surfaceToggleBtn"),
  ];

  const HOLD_MS = 450;

  function attachHold(btn, onHoldOpen) {
    let timer = null;
    let held = false;

    function start() {
      held = false;
      timer = setTimeout(() => {
        held = true;
        onHoldOpen();
      }, HOLD_MS);
    }

    function cancel() {
      clearTimeout(timer);
    }

    btn.addEventListener(
      "click",
      (e) => {
        if (held) {
          e.preventDefault();
          e.stopPropagation();
          held = false;
        }
      },
      true
    );

    btn.addEventListener("mousedown", start);
    btn.addEventListener("mouseup", cancel);
    btn.addEventListener("mouseleave", cancel);

    btn.addEventListener("touchstart", start, { passive: true });
    btn.addEventListener("touchend", cancel);
    btn.addEventListener("touchcancel", cancel);

    btn.addEventListener("contextmenu", (e) => e.preventDefault());
  }

  themeButtons.forEach((btn) => btn && attachHold(btn, openThemePicker));
  surfaceButtons.forEach((btn) => btn && attachHold(btn, openSurfacePicker));
})();

/* ==================================================
   Aurora accent animation
================================================== */
let auroraTimer = null;
let auroraIndex = 0;

function startAuroraAccent() {
  stopAuroraAccent();

  const root = document.documentElement;

  auroraTimer = setInterval(() => {
    auroraIndex = (auroraIndex + 1) % AURORA_COLORS.length;
    root.style.setProperty("--accent", AURORA_COLORS[auroraIndex]);
  }, 2200);
}

function stopAuroraAccent() {
  if (auroraTimer) {
    clearInterval(auroraTimer);
    auroraTimer = null;
  }
}

/* ==================================================
   Load saved theme/surface on startup
================================================== */
(function init() {
  // Theme
  const savedTheme = localStorage.getItem("ui-theme");
  if (savedTheme && THEME_ORDER.includes(savedTheme)) {
    currentThemeIndex = THEME_ORDER.indexOf(savedTheme);
    applyTheme(savedTheme);
  } else {
    applyTheme(THEME_ORDER[0]);
  }

  // Surface
  const savedSurface = localStorage.getItem("ui-surface");
  if (savedSurface && SURFACE_ORDER.includes(savedSurface)) {
    applySurface(savedSurface);
  } else {
    applySurface(SURFACE_ORDER[0]);
  }
})();

console.log("Theme + Surface system loaded");

// (optional) debug
window.openThemePicker = openThemePicker;
window.openSurfacePicker = openSurfacePicker;
window.applyTheme = applyTheme;
window.applySurface = applySurface;
window.prettyThemeName = prettyThemeName;
window.prettySurfaceName = prettySurfaceName;
window.cycleTheme = cycleTheme;
window.cycleSurface = cycleSurface;
