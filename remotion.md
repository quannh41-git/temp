# Code Hike × Remotion — Project Guide

> An animated code walkthrough video template built with [Remotion](https://www.remotion.dev/) and [Code Hike](https://codehike.org/).  
> Each file in the `public/` folder becomes one "step" in the video.  
> TypeScript files are processed through [TwoSlash](https://twoslash.netlify.app/) to produce live type callouts and error annotations.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [How It Works — Overview](#how-it-works--overview)
3. [Project Structure](#project-structure)
4. [Data Flow](#data-flow)
5. [Source Files In Depth](#source-files-in-depth)
   - [Entry & Composition](#entry--composition)
   - [Main Video Component](#main-video-component)
   - [Code Transition](#code-transition)
   - [Progress Bar](#progress-bar)
   - [Hot Reload](#hot-reload)
   - [Utilities & Font](#utilities--font)
   - [Annotations](#annotations)
   - [Calculate Metadata](#calculate-metadata)
6. [Public Folder — Code Snippets](#public-folder--code-snippets)
7. [Configuration](#configuration)
8. [Customization Guide](#customization-guide)
9. [Adding Scenes & Audio](#adding-scenes--audio)
10. [Rendering](#rendering)

---

## Quick Start

```bash
# Install dependencies
npm i

# Launch Remotion Studio (interactive preview)
npm run dev

# Render to video
npx remotion render
```

---

## How It Works — Overview

```
public/code1.tsx  ─┐
public/code2.tsx  ─┤─► getFiles() ─► processSnippet() ─► calculateMetadata()
public/code3.tsx  ─┤                        │
public/code4.swift─┘              TwoSlash + CodeHike
                                            │
                                    HighlightedCode[]
                                            │
                              ┌─────────────▼─────────────┐
                              │     Main.tsx (Series)      │
                              │  ┌─────────────────────┐  │
                              │  │  CodeTransition      │  │
                              │  │  (token animations)  │  │
                              │  └─────────────────────┘  │
                              │  ProgressBar               │
                              └───────────────────────────┘
```

1. **Build time** — `calculateMetadata` reads every `code*` file from `public/`, runs TypeScript files through TwoSlash, highlights all of them with Code Hike, and computes the video width and duration.
2. **Render time** — `Main` splits the video into N equal segments using `Series`. Each segment renders a `CodeTransition` that smoothly animates token positions, colors, and opacity between the previous and current code step.
3. **Studio time** — `RefreshOnCodeChange` watches the `public/` folder and hot-reloads the composition whenever a snippet file changes.

---

## Project Structure

```
template-code-hike-main/
│
├── public/                          # ← YOUR CODE SNIPPETS LIVE HERE
│   ├── code1.tsx
│   ├── code2.tsx
│   ├── code3.tsx
│   └── code4.swift
│
├── src/
│   ├── index.ts                     # Remotion entry point
│   ├── Root.tsx                     # Composition registration
│   ├── Main.tsx                     # Top-level video component
│   ├── CodeTransition.tsx           # Animated code diff renderer
│   ├── ProgressBar.tsx              # Step indicator bar
│   ├── ReloadOnCodeChange.tsx       # Studio hot-reload watcher
│   ├── font.ts                      # Font + sizing constants
│   ├── utils.ts                     # Token style interpolation
│   │
│   ├── annotations/
│   │   ├── Callout.tsx              # ^? type query popover
│   │   ├── Error.tsx                # @errors underline + message block
│   │   └── InlineToken.tsx          # Token transition base handler
│   │
│   └── calculate-metadata/
│       ├── calculate-metadata.tsx   # Main metadata calculation function
│       ├── get-files.ts             # Reads code* files from public/
│       ├── process-snippet.ts       # TwoSlash + CodeHike highlight pipeline
│       ├── schema.ts                # Zod schema for composition props
│       └── theme.tsx                # Theme enum, Context, ThemeProvider
│
├── remotion.config.ts               # Remotion output settings
├── tsconfig.json                    # TypeScript configuration
├── eslint.config.mjs                # ESLint configuration
└── package.json
```

---

## Data Flow

```
                    ┌────────────────────────────────────┐
                    │         calculateMetadata()        │
                    │                                    │
  public/code*.ext  │  1. getFiles()                     │
       files   ────►│     Filter files named "code*"     │
                    │     Fetch text content              │
                    │                                    │
                    │  2. processSnippet() per file      │
                    │     – TS/TSX → run TwoSlash        │
                    │     – highlight() via CodeHike     │
                    │     – attach callout annotations   │
                    │     – attach error annotations     │
                    │                                    │
                    │  3. measureText() → codeWidth      │
                    │  4. getThemeColors() → themeColors │
                    │  5. Compute video width & duration │
                    └─────────────┬──────────────────────┘
                                  │  returns HighlightedCode[]
                                  ▼
                    ┌────────────────────────────────────┐
                    │            Main.tsx                │
                    │                                    │
                    │  ThemeProvider (themeColors)       │
                    │  ┌──────────────────────────────┐ │
                    │  │ ProgressBar                  │ │
                    │  │ Series → N × Series.Sequence │ │
                    │  │   └── CodeTransition         │ │
                    │  │         oldCode / newCode    │ │
                    │  └──────────────────────────────┘ │
                    │  RefreshOnCodeChange               │
                    └────────────────────────────────────┘
```

---

## Source Files In Depth

### Entry & Composition

#### `src/index.ts`
```ts
registerRoot(RemotionRoot);
```
The Remotion entry point. Registers the root component so the bundler/renderer can discover the composition.

---

#### `src/Root.tsx`
Registers a single Remotion `<Composition>` with id `"Main"`.

| Prop | Default | Description |
|------|---------|-------------|
| `theme` | `"github-dark"` | Code highlight theme |
| `width.type` | `"auto"` | `"auto"` = fit content, `"fixed"` = explicit pixel width |
| `fps` | `30` | Frames per second |
| `height` | `1080` | Video height in pixels |

`calculateMetadata` is called at build/preview time to compute width, duration, and highlighted code.

---

### Main Video Component

#### `src/Main.tsx`

The top-level React component rendered for each frame.

**Key responsibilities:**
- Validates `steps` and `themeColors` are present (provided by `calculateMetadata`).
- Uses `useVideoConfig()` to get `durationInFrames` and distributes time equally across steps: `stepDuration = durationInFrames / steps.length`.
- Sets `transitionDuration = 30` frames for each code-to-code animation.
- Renders a `<Series>` where each `<Series.Sequence>` corresponds to one code file.
- Each sequence renders `<CodeTransition oldCode={steps[n-1]} newCode={steps[n]} />`.
- `<ProgressBar>` is absolutely positioned at the top, outside the `<Series>`.
- `<RefreshOnCodeChange>` is a side-effect-only component for Studio hot reload.

---

### Code Transition

#### `src/CodeTransition.tsx`

The core animation engine. Wraps Code Hike's `<Pre>` component and drives per-token animations using Remotion's frame-based timeline.

**Lifecycle:**
1. First render — captures a DOM snapshot of the *previous* code layout via `getStartingSnapshot()`.
2. Subsequent renders — calls `calculateTransitions()` which produces a list of `{ element, keyframes, options }` per token.
3. Each frame — `useCurrentFrame()` produces a `progress` value; `applyStyle()` interpolates position/color/opacity for each token.

**Animation curve:** Bezier `(0.17, 0.67, 0.76, 0.91)` — snappy ease-out.

**Annotation handlers used:**

| Handler | Source | Purpose |
|---------|--------|---------|
| `tokenTransitions` | `annotations/InlineToken.tsx` | Makes tokens `inline-block` so transforms work |
| `callout` | `annotations/Callout.tsx` | Renders `^?` TwoSlash type queries |
| `errorInline` | `annotations/Error.tsx` | Wavy red underline on error tokens |
| `errorMessage` | `annotations/Error.tsx` | Block below line with error description |

**Rendering delay:** Uses `useDelayRender` / `continueRender` to hold the frame until DOM measurements are complete.

---

### Progress Bar

#### `src/ProgressBar.tsx`

Renders a row of pill-shaped progress indicators — one per step — fixed at the top of the video (`top: 48px`).

- **Completed steps** — fully filled with `themeColors.icon.foreground`.
- **Current step** — partially filled, proportional to `(frame % stepDuration) / stepDuration`.
- **Upcoming steps** — empty background (`themeColors.editor.lineHighlightBackground`).

---

### Hot Reload

#### `src/ReloadOnCodeChange.tsx`

Invisible component that only activates inside Remotion Studio (`env.isStudio && !env.isReadOnlyStudio`). Calls `watchPublicFolder()` to detect file changes, then calls `reevaluateComposition()` to re-run `calculateMetadata` automatically.

---

### Utilities & Font

#### `src/font.ts`

Loads **Roboto Mono** via `@remotion/google-fonts` and exports layout constants:

| Export | Value | Purpose |
|--------|-------|---------|
| `fontFamily` | Roboto Mono | Used in `CodeTransition` |
| `waitUntilDone` | Promise | Must resolve before `measureText` |
| `fontSize` | `40` | Code font size (px) |
| `tabSize` | `3` | Tab → space character count |
| `horizontalPadding` | `60` | Left/right padding (px) |
| `verticalPadding` | `84` | Top/bottom padding (px) |

#### `src/utils.ts` — `applyStyle()`

Applies interpolated transforms to a DOM element each frame:

| Property | Interpolation |
|----------|--------------|
| `opacity` | Linear progress (fade in) |
| `color` | `interpolateColors` over bezier progress |
| `translate` | `translateX` / `translateY` keyframes |

---

### Annotations

All annotation handlers are registered in `CodeTransition` and integrate with Code Hike's `<Pre>` rendering pipeline.

#### `src/annotations/InlineToken.tsx` — `tokenTransitions`

Wraps every token in `display: inline-block` so CSS `translate` transforms work correctly during token position animations.

#### `src/annotations/Callout.tsx` — `callout`

Triggered by TwoSlash `^?` comments. Renders an animated popover below the line showing the inferred type.

- **Positioning** — uses `column` (midpoint of `fromColumn`/`toColumn`) and `indentation` offsets.
- **Animation** — fades in from frame 25→35 using `interpolate`.
- **Styling** — background is `mix(0.08, readable, bg)` for subtle contrast.

#### `src/annotations/Error.tsx` — `errorInline` + `errorMessage`

Triggered by TwoSlash `// @errors: <code>` comments.

- `errorInline` — applies `text-decoration: underline wavy red` via a CSS custom property.
- `errorMessage` — renders a block below the affected line with a left red border, fading in at frames 25→35.

---

### Calculate Metadata

#### `src/calculate-metadata/schema.ts`

Zod schema for the composition's user-configurable props exposed in Remotion Studio:

```ts
schema = z.object({
  theme: themeSchema,   // one of 22 named themes
  width: discriminatedUnion("type", [
    { type: "auto" },               // fit to longest line
    { type: "fixed", value: number } // explicit width
  ])
})
```

#### `src/calculate-metadata/theme.tsx`

- Exports `themeSchema` — a `z.enum` of 22 supported themes (github-dark, dracula, monokai, nord, etc.).
- Exports `ThemeProvider` and `useThemeColors()` hook — React context that distributes `themeColors` to all child components without prop drilling.

#### `src/calculate-metadata/get-files.ts`

Calls `getStaticFiles()` from `@remotion/studio`, filters for files whose name starts with `"code"`, fetches their text content, and returns `{ filename, value }[]`.

**Ordering:** Files are returned in the order `getStaticFiles()` provides them — typically alphabetical. Name your files `code1`, `code2`, `code3`… to control step order.

#### `src/calculate-metadata/process-snippet.ts`

Processes one code file into a `HighlightedCode` object:

```
file { filename, value }
   │
   ├─ extension === "ts" | "tsx"?
   │     Yes → twoslash.run() → extract queries & errors → inject annotations
   │     No  → use raw value as-is
   │
   └─► highlight({ lang, value }, theme) → HighlightedCode
```

TwoSlash compiler options: `lib: ["dom", "es2023"]`, `jsx: ReactJSX`, `module: ESNext`.

#### `src/calculate-metadata/calculate-metadata.tsx`

Orchestrates the entire pre-render pipeline and returns Remotion metadata:

```ts
{
  durationInFrames: files.length * 90,  // 90 frames (3 s) per step
  width: Math.max(1080, codeWidth + 2 * horizontalPadding),
  props: { steps, themeColors, codeWidth, theme, width }
}
```

Width is calculated by measuring a single character (`"A"`) with `measureText()`, multiplying by the longest line (tabs expanded), and rounding up to an even number (MP4 requirement).

---

## Public Folder — Code Snippets

Files in `public/` are the **only content you need to edit** to create a new video.

### Naming Convention

| Pattern | Effect |
|---------|--------|
| `code1.tsx` | Step 1 — parsed with TwoSlash |
| `code2.tsx` | Step 2 — parsed with TwoSlash |
| `code4.swift` | Step 4 — syntax-highlighted, no TwoSlash |

Any file starting with `code` is picked up automatically. Use numeric suffixes to control order.

### TwoSlash Annotations (TypeScript only)

```ts
// Show inferred type as a callout popover
const x = 42;
//    ^?

// Show a TypeScript error inline
// @errors: 2339
console.log(user.location);
```

### Supported Languages

Any language supported by Code Hike's `highlight()` function works. TwoSlash processing only activates for `.ts` and `.tsx` files.

---

## Configuration

### `remotion.config.ts`

```ts
Config.setVideoImageFormat('jpeg');   // frame image format during render
Config.setOverwriteOutput(true);       // overwrite output file if it exists
```

### `tsconfig.json`

- Target: ES2021, module resolution: Bundler.
- `public/` and `remotion.config.ts` are excluded from type checking.
- `noUnusedLocals: true` — keep imports clean.

---

## Customization Guide

### Change the theme

Open Remotion Studio (`npm run dev`), select the `Main` composition, and use the **Props panel** to pick from 22 built-in themes:

`dark-plus` · `dracula` · `dracula-soft` · `github-dark` · `github-dark-dimmed` · `github-light` · `light-plus` · `material-darker` · `material-default` · `material-lighter` · `material-ocean` · `material-palenight` · `min-dark` · `min-light` · `monokai` · `nord` · `one-dark-pro` · `poimandres` · `slack-dark` · `slack-ochin` · `solarized-dark` · `solarized-light`

To change the default, edit the `theme` defaultProp in [src/Root.tsx](src/Root.tsx).

### Change step duration

In [src/calculate-metadata/calculate-metadata.tsx](src/calculate-metadata/calculate-metadata.tsx), change:

```ts
const defaultStepDuration = 90; // frames — currently 3 s at 30 fps
```

### Change transition duration

In [src/Main.tsx](src/Main.tsx), change:

```ts
const transitionDuration = 30; // frames — currently 1 s at 30 fps
```

### Change font size or padding

Edit the constants in [src/font.ts](src/font.ts):

```ts
export const fontSize = 40;
export const horizontalPadding = 60;
export const verticalPadding = 84;
export const tabSize = 3;
```

### Fix video width

In Remotion Studio props panel, set `width.type` to `"fixed"` and specify a pixel value. Or change the default in [src/Root.tsx](src/Root.tsx):

```ts
width: { type: "fixed", value: 1920 }
```

### Add a new code step

1. Create a new file in `public/` named `codeN.<ext>` (e.g. `code5.ts`).
2. Remotion Studio will hot-reload and add the step automatically.

---

## Adding Scenes & Audio

### Where scenes are defined

A **scene** (step) is simply one `code*` file in the `public/` folder. The entire video timeline is built inside `src/Main.tsx` using Remotion's `<Series>` primitive:

```tsx
// src/Main.tsx — annotated structure
<Series>
  {steps.map((step, index) => (
    //  ↑ one Series.Sequence per code* file
    <Series.Sequence
      key={index}
      layout="none"
      durationInFrames={stepDuration}   // ← duration of this scene in frames
      name={step.meta}                   // ← label shown in Studio timeline
    >
      {/* ── SCENE CONTENT starts here ── */}
      <CodeTransition
        oldCode={steps[index - 1]}
        newCode={step}
        durationInFrames={transitionDuration}
      />
      {/* ── Add anything else inside this Sequence ── */}
    </Series.Sequence>
  ))}
</Series>
```

Each `Series.Sequence` has its own local frame counter starting at `0`, so every component inside it (including `<Audio>`) measures time relative to the **start of that scene**.

---

### Where to place audio files

Audio files must go in the `public/` folder and be referenced with `staticFile()` from `remotion`.

```
public/
├── code1.tsx          ← scene 1 code
├── code2.tsx          ← scene 2 code
├── code3.tsx          ← scene 3 code
├── audio1.mp3         ← audio for scene 1  (NEW)
├── audio2.mp3         ← audio for scene 2  (NEW)
├── audio3.mp3         ← audio for scene 3  (NEW)
└── background.mp3     ← global background music (NEW, optional)
```

The naming `audio1`, `audio2`, … mirrors `code1`, `code2`, … so they pair by index.

---

### Option A — Per-scene audio (sync each clip to its scene)

Edit `src/Main.tsx`. Import `Audio` and `staticFile`, then add `<Audio>` **inside** each `<Series.Sequence>`:

```tsx
// src/Main.tsx
import { AbsoluteFill, Audio, Series, staticFile, useVideoConfig } from "remotion";

// inside the JSX:
<Series>
  {steps.map((step, index) => (
    <Series.Sequence
      key={index}
      layout="none"
      durationInFrames={stepDuration}
      name={step.meta}
    >
      {/* 🔊 Audio for this scene — starts at frame 0 of this sequence */}
      <Audio src={staticFile(`audio${index + 1}.mp3`)} />

      <CodeTransition
        oldCode={steps[index - 1]}
        newCode={step}
        durationInFrames={transitionDuration}
      />
    </Series.Sequence>
  ))}
</Series>
```

> **Important:** The audio file length must be ≤ `stepDuration` frames (default 90 frames = 3 s at 30 fps).  
> If the audio is shorter, it stops automatically. If it's longer, Remotion clips it at the sequence boundary.

To trim or delay an audio clip inside a sequence:

```tsx
<Audio
  src={staticFile(`audio${index + 1}.mp3`)}
  startFrom={0}        // start reading from this offset (frames) in the file
  endAt={stepDuration} // stop reading at this frame relative to sequence start
/>
```

---

### Sync audio với scene — khoảng im lặng khi chuyển cảnh

#### Cơ chế thời gian

Timeline mỗi scene trông như sau (mặc định 90 frames = 3 s):

```
frame: 0                          60        75        90
       │────────────────────────────│─────────│─────────│
       │   Nội dung cảnh đang hiển thị        │ silence  │
       │   Code morph animation bắt đầu → 30f │          │
       │   🔊 Audio phát                      │ 🔇 tắt   │
       └──────────────────────────────────────└──────────┘
                                        ↑
                             endAt = stepDuration - silenceFrames
```

Phần `transitionDuration = 30` frames là animation hình ảnh (token di chuyển). Khoảng im lặng (`silenceFrames`) nên bắt đầu **trước** hoặc **cùng lúc** với animation để cảm giác tự nhiên.

---

#### Cách 1: Hard cutoff — dừng audio đột ngột (đơn giản nhất)

Dùng prop `endAt` trên `<Audio>`. Frame được đo từ đầu `Series.Sequence` hiện tại.

```tsx
// src/Main.tsx
import { AbsoluteFill, Audio, interpolate, Series, staticFile, useVideoConfig } from "remotion";

const silenceFrames = 15; // 0.5 s im lặng trước khi chuyển cảnh

<Series>
  {steps.map((step, index) => (
    <Series.Sequence
      key={index}
      layout="none"
      durationInFrames={stepDuration}
      name={step.meta}
    >
      <Audio
        src={staticFile(`audio${index + 1}.mp3`)}
        endAt={stepDuration - silenceFrames}  // ← dừng trước khi hết cảnh
      />
      <CodeTransition
        oldCode={steps[index - 1]}
        newCode={step}
        durationInFrames={transitionDuration}
      />
    </Series.Sequence>
  ))}
</Series>
```

---

#### Cách 2: Fade-out mượt mà trước khi chuyển cảnh

Dùng `volume` dạng function. Remotion gọi nó mỗi frame với số frame **tương đối** từ đầu Sequence.

```tsx
// src/Main.tsx
import { Audio, interpolate, Series, staticFile } from "remotion";

const silenceFrames = 15;   // khoảng im = 0.5s
const fadeFrames    = 10;   // fade out dần trong 10 frame trước khi im

<Series>
  {steps.map((step, index) => (
    <Series.Sequence
      key={index}
      layout="none"
      durationInFrames={stepDuration}
      name={step.meta}
    >
      <Audio
        src={staticFile(`audio${index + 1}.mp3`)}
        volume={(frame) =>
          interpolate(
            frame,
            [
              stepDuration - silenceFrames - fadeFrames,  // bắt đầu fade
              stepDuration - silenceFrames,               // tắt hoàn toàn
            ],
            [1, 0],
            { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
          )
        }
      />
      <CodeTransition
        oldCode={steps[index - 1]}
        newCode={step}
        durationInFrames={transitionDuration}
      />
    </Series.Sequence>
  ))}
</Series>
```

**Ví dụ với `stepDuration = 90`, `silenceFrames = 15`, `fadeFrames = 10`:**

```
frame:  0 ───────────── 65 ──── 75 ─── 90
volume: 1.0             1.0 → 0.0  0.0
        │  audio phát   │ fade  │ im   │
        └───────────────┘───────┘──────┘
                              ↑
                    code morph (30f) bắt đầu ở frame 0
```

---

#### Điều chỉnh `silenceFrames` theo cảm giác

| `silenceFrames` | Thời gian (30fps) | Cảm giác |
|---|---|---|
| `10` | 0.33 s | Chuyển nhanh, hơi giật |
| `15` | 0.5 s | Tự nhiên, khuyến nghị |
| `30` | 1.0 s | Rõ ràng nghỉ giữa các cảnh |

---

### Option B — Global background music

Add `<Audio>` **outside** `<Series>` but still inside the `<AbsoluteFill>` in `src/Main.tsx`:

```tsx
<ThemeProvider themeColors={themeColors}>
  <AbsoluteFill style={outerStyle}>
    {/* 🎵 Background music — plays for the entire video duration */}
    <Audio src={staticFile("background.mp3")} volume={0.3} />

    <AbsoluteFill style={{ width: codeWidth || "100%", margin: "auto" }}>
      <ProgressBar steps={steps} />
      <AbsoluteFill style={style}>
        <Series>
          {/* ... scenes ... */}
        </Series>
      </AbsoluteFill>
    </AbsoluteFill>
  </AbsoluteFill>
  <RefreshOnCodeChange />
</ThemeProvider>
```

---

### Option C — Per-scene audio with different durations per step

If each scene needs a different duration (matching its audio file), change `calculateMetadata` to accept per-step durations and pass them to `Main`:

**1. Add audio duration metadata in `src/calculate-metadata/calculate-metadata.tsx`:**

```ts
// Fetch audio files similarly to code files
const audioFiles = getStaticFiles().filter((f) => f.name.startsWith("audio"));

// Use a fixed duration per step or derive from audio metadata
const stepDurations = contents.map((_, i) => {
  // e.g. lookup a sidecar JSON, or just keep a manual array:
  return perStepDurations[i] ?? 90;
});

return {
  durationInFrames: stepDurations.reduce((a, b) => a + b, 0),
  props: { ..., stepDurations },
};
```

**2. In `src/Main.tsx`, replace the single `stepDuration` with the array:**

```tsx
<Series>
  {steps.map((step, index) => (
    <Series.Sequence
      key={index}
      layout="none"
      durationInFrames={stepDurations[index]}   // ← per-step value
      name={step.meta}
    >
      <Audio src={staticFile(`audio${index + 1}.mp3`)} />
      <CodeTransition ... />
    </Series.Sequence>
  ))}
</Series>
```

---

### Summary map

```
File to add/edit                    What it controls
────────────────────────────────────────────────────────────────
public/codeN.ext                    Add a new scene (step N)
public/audioN.mp3                   Audio clip for scene N
public/background.mp3               Global background music

src/Main.tsx                        WHERE audio is wired in:
  <Audio> inside <Series.Sequence>  → per-scene sync
  <Audio> outside <Series>          → global background

src/calculate-metadata/
  calculate-metadata.tsx            Controls durationInFrames per step
                                    (change defaultStepDuration = 90)
```

---

## Rendering

```bash
# Render with default settings (outputs to out/Main.mp4)
npx remotion render

# Render with a specific theme and output path
npx remotion render Main --props='{"theme":"monokai"}' out/video.mp4

# Render a specific frame range
npx remotion render Main --frames=0-89
```

Rendered output is JPEG-encoded frames (set in `remotion.config.ts`) assembled into MP4.
