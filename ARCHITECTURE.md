# Architecture & Workflow Diagrams

## System Architecture

### Desktop Version (Original)

```
┌─────────────────────────────────────┐
│      User's Computer                │
│                                     │
│  ┌──────────────────────────────┐  │
│  │    Python Interpreter        │  │
│  │      (Native)                │  │
│  └────────────┬─────────────────┘  │
│               │                     │
│  ┌────────────▼─────────────────┐  │
│  │    Pygame Library            │  │
│  │  (Native C Extensions)       │  │
│  └────────────┬─────────────────┘  │
│               │                     │
│  ┌────────────▼─────────────────┐  │
│  │  Undertale Clone Game Code   │  │
│  │    - main.py                 │  │
│  │    - globals.py              │  │
│  │    - rooms.py                │  │
│  │    - frisk.py                │  │
│  │    - etc.                    │  │
│  └────────────┬─────────────────┘  │
│               │                     │
│  ┌────────────▼─────────────────┐  │
│  │   Operating System           │  │
│  │   - Graphics (OpenGL/D3D)    │  │
│  │   - Audio (ALSA/DirectSound) │  │
│  │   - Input (Keyboard)         │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

### Browser Version (WebAssembly)

```
┌──────────────────────────────────────────────────────┐
│         User's Web Browser                           │
│                                                      │
│  ┌───────────────────────────────────────────────┐  │
│  │           HTML/CSS/JavaScript                 │  │
│  │  - Canvas element (640x480)                   │  │
│  │  - User interface                             │  │
│  │  - Loading screen                             │  │
│  └──────────────────┬────────────────────────────┘  │
│                     │                                │
│  ┌──────────────────▼────────────────────────────┐  │
│  │      Pyodide/Emscripten Runtime              │  │
│  │  - Python 3.11 in WebAssembly                │  │
│  │  - Virtual file system (MEMFS)               │  │
│  │  - Browser API bridges                       │  │
│  └──────────────────┬────────────────────────────┘  │
│                     │                                │
│  ┌──────────────────▼────────────────────────────┐  │
│  │         Pygame-ce Library                     │  │
│  │  - Compiled to WebAssembly                    │  │
│  │  - Canvas rendering backend                   │  │
│  │  - Web Audio API bridge                       │  │
│  └──────────────────┬────────────────────────────┘  │
│                     │                                │
│  ┌──────────────────▼────────────────────────────┐  │
│  │    Undertale Clone Game Code                  │  │
│  │      - main_web.py (async wrapper)            │  │
│  │      - main.py (original logic)               │  │
│  │      - All game modules                       │  │
│  └──────────────────┬────────────────────────────┘  │
│                     │                                │
│  ┌──────────────────▼────────────────────────────┐  │
│  │        Browser Web APIs                       │  │
│  │  - Canvas 2D Context (Graphics)               │  │
│  │  - Web Audio API (Sound)                      │  │
│  │  - Keyboard Events (Input)                    │  │
│  │  - LocalStorage (Save files)                  │  │
│  └───────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

## Build Process Flow

```
┌─────────────────┐
│  Source Files   │
│  - *.py files   │
│  - Assets       │
│  - Config       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Pygbag Tool    │
│  (Build Step)   │
└────────┬────────┘
         │
         ├──────────────────────────────┐
         │                              │
         ▼                              ▼
┌─────────────────┐          ┌─────────────────┐
│  Python Code    │          │  Asset Files    │
│  Compilation    │          │  Bundling       │
└────────┬────────┘          └────────┬────────┘
         │                            │
         ▼                            │
┌─────────────────┐                   │
│  Emscripten     │                   │
│  Compiler       │                   │
└────────┬────────┘                   │
         │                            │
         ├────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  Build Output   │
│  build/web/     │
│  - index.html   │
│  - *.wasm       │
│  - *.js         │
│  - assets.zip   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Deployment    │
│  (GitHub Pages) │
└─────────────────┘
```

## Development Workflow

```
┌─────────────┐
│  Developer  │
└──────┬──────┘
       │
       │ 1. Edit code
       ▼
┌──────────────────┐
│   Source Files   │
│   (*.py, etc.)   │
└──────┬───────────┘
       │
       │ 2. Run check
       ▼
┌──────────────────────┐
│ check_compatibility  │
│      .py             │
└──────┬───────────────┘
       │
       │ 3. Pass? ──No──┐
       ▼                │
      Yes               │
       │                │
       │ 4. Build       │
       ▼                │
┌──────────────┐        │
│  build.sh    │        │
└──────┬───────┘        │
       │                │
       │ 5. Success?    │
       ▼                │
      Yes               │
       │                │
       │ 6. Test        │
       ▼                │
┌──────────────┐        │
│  Local       │        │
│  Browser     │        │
│  Testing     │        │
└──────┬───────┘        │
       │                │
       │ 7. Works?      │
       ▼                │
      Yes               │
       │                │
       │ 8. Commit      │
       ▼                │
┌──────────────┐        │
│  Git Push    │        │
└──────┬───────┘        │
       │                │
       │ 9. Auto-deploy │
       ▼                │
┌──────────────┐        │
│  GitHub      │        │
│  Actions     │        │
└──────┬───────┘        │
       │                │
       │ 10. Deploy     │
       ▼                │
┌──────────────┐        │
│  GitHub      │        │
│  Pages       │        │
└──────────────┘        │
       │                │
       └────<Fix────────┘
```

## CI/CD Pipeline (GitHub Actions)

```
┌─────────────────┐
│   Git Push      │
│  (master/main)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  GitHub Actions │
│   Triggered     │
└────────┬────────┘
         │
         ├──── Step 1: Checkout Code
         │
         ├──── Step 2: Setup Python 3.11
         │
         ├──── Step 3: Install Pygbag
         │
         ├──── Step 4: Run Compatibility Check
         │             └─> check_compatibility.py
         │
         ├──── Step 5: Build WebAssembly
         │             └─> pygbag --build
         │
         ├──── Step 6: Verify Build
         │             └─> ls build/web/
         │
         ├──── Step 7: Upload Artifact
         │             └─> build/web/
         │
         ▼
┌─────────────────┐
│  Deploy Job     │
└────────┬────────┘
         │
         ├──── Step 8: Deploy to Pages
         │
         ▼
┌─────────────────┐
│  Live Website   │
│  GitHub Pages   │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  Users Play     │
│   in Browser    │
└─────────────────┘
```

## File Organization

```
undertale-clone/
│
├── 📄 Core Game Files
│   ├── main.py              # Original desktop entry
│   ├── main_web.py          # WebAssembly wrapper
│   ├── globals.py           # Game globals
│   ├── frisk.py             # Player character
│   ├── rooms.py             # Game rooms
│   ├── draw.py              # Rendering
│   ├── input.py             # Input handling
│   └── ...                  # Other game modules
│
├── 🎨 Assets
│   ├── sprites/             # Graphics
│   ├── fonts/               # Fonts
│   ├── mus/                 # Music
│   └── sfx/                 # Sound effects
│
├── 🔧 Build & Config
│   ├── build.sh             # Build script
│   ├── pygbag.toml          # Build config
│   ├── requirements.txt     # Python deps
│   ├── .gitignore          # Git config
│   └── __init__.py          # Package metadata
│
├── 📖 Documentation
│   ├── README.md            # Main readme
│   ├── BROWSER_BUILD.md     # Build guide
│   ├── WASM_NOTES.md        # Technical notes
│   ├── QUICKSTART.md        # Quick guide
│   ├── IMPLEMENTATION_SUMMARY.md
│   └── ARCHITECTURE.md      # This file
│
├── 🧪 Testing & Development
│   ├── check_compatibility.py
│   ├── test.html
│   └── index.html
│
├── 🤖 CI/CD
│   └── .github/
│       └── workflows/
│           └── deploy.yml   # GitHub Actions
│
└── 📦 Build Output (generated)
    └── build/
        └── web/             # Deploy this!
            ├── index.html
            ├── pygame.js
            ├── python.wasm
            └── ...
```

## Data Flow: Game Loop

### Desktop Version
```
User Input (Keyboard)
         │
         ▼
   Input Module
         │
         ▼
   Game Logic
         │
    ┌────┴────┐
    ▼         ▼
Globals    Rooms
    │         │
    └────┬────┘
         ▼
    Draw Module
         │
         ▼
  Pygame Render
         │
         ▼
   Screen Output
```

### Browser Version (with Async)
```
User Input (Keyboard Events)
         │
         ▼
Browser Event Handler
         │
         ▼
   Input Module
         │
         ▼
   Game Logic (async)
         │
    ┌────┴────┐
    ▼         ▼
Globals    Rooms
    │         │
    └────┬────┘
         ▼
    Draw Module
         │
         ▼
  Pygame-ce Render
         │
         ▼
 Canvas 2D Context
         │
         ├──> await asyncio.sleep(0)
         │    (Yield to browser)
         │
         ▼
   Screen Output
```

## Save File Flow

### Desktop
```
Game State
    │
    ▼
Python File I/O
    │
    ▼
Operating System
    │
    ▼
Physical Disk
(file0, undertale.ini)
```

### Browser
```
Game State
    │
    ▼
Python File I/O
    │
    ▼
Emscripten MEMFS
(Virtual File System)
    │
    ▼
Browser IndexedDB
(LocalStorage backend)
    │
    ▼
Browser Storage
(Persistent, per-domain)
```

## Deployment Options Comparison

```
┌─────────────────────────────────────────────────────┐
│                 Deployment Options                  │
├─────────────────┬───────────────┬───────────────────┤
│  GitHub Pages   │   Netlify     │   Custom Server   │
├─────────────────┼───────────────┼───────────────────┤
│  ✅ Free        │   ✅ Free     │   ⚠️ Paid          │
│  ✅ Auto-deploy │   ✅ Auto     │   ❌ Manual        │
│  ✅ HTTPS       │   ✅ HTTPS    │   ⚠️ Configure     │
│  ⚠️ GitHub only │   ✅ Any Git  │   ✅ Full control  │
│  ⚠️ Public only │   ✅ Private  │   ✅ Private       │
└─────────────────┴───────────────┴───────────────────┘
```

## Legend

- 📄 = Source code files
- 🎨 = Asset files
- 🔧 = Configuration/build files
- 📖 = Documentation
- 🧪 = Testing/development files
- 🤖 = Automation/CI/CD
- 📦 = Generated/build outputs
- ✅ = Available/Supported
- ⚠️ = Partial/Conditional
- ❌ = Not available

---

This architecture enables running a desktop Python/Pygame game in the browser with minimal code changes while maintaining full compatibility with the original version.
