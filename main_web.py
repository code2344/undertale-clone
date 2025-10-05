#!/usr/bin/python3
# coding=utf-8
"""
WebAssembly-compatible version of the Undertale Clone main file.
This file adds async/await support required for running in the browser via Pygbag/Emscripten.
"""
import asyncio
import sys
import os

# Platform detection for WebAssembly
try:
    import platform
    IS_WASM = platform.system() == "Emscripten"
except:
    IS_WASM = False

# Check if we're running in a Pygbag environment
try:
    import pygbag
    IS_PYGBAG = True
except ImportError:
    IS_PYGBAG = False

# Import the main module
import main

async def async_maincycle():
    """
    Async version of the main game loop for WebAssembly compatibility.
    In WebAssembly, the main loop must be async to allow the browser to handle events.
    """
    import globals
    import threading
    
    threading.Thread(target=globals.room.on_enter, name='on_enter runner for first room').start()
    
    while globals.running:
        if globals.room:
            globals.room.draw()
        
        # Yield control back to browser in WebAssembly environment
        # This prevents the browser from freezing during the game loop
        if IS_WASM or IS_PYGBAG:
            await asyncio.sleep(0)
        

async def async_main():
    """
    Async entry point for the game.
    """
    import globals
    
    try:
        main.init()
        await async_maincycle()
    except globals.UndertaleError as e:
        if len(e.args) > 0:
            main.invoke_dog("", e.args[0])
        else:
            main.invoke_dog()
    except (SystemExit, KeyboardInterrupt):
        globals.running = False
    except:
        import traceback
        exc_type, exc_value, exc_traceback = sys.exc_info()
        output = traceback.format_exception(exc_type, exc_value, exc_traceback)
        output = [i[:-1].translate({ord('\n'): ':'}) for i in output]
        output = list(reversed(output))[:-1]
        main.invoke_dog(output)
    finally:
        globals.running = False


if __name__ == "__main__":
    # Run async main loop
    if IS_WASM or IS_PYGBAG:
        # In WebAssembly/Pygbag, use asyncio
        asyncio.run(async_main())
    else:
        # Fallback to sync version for native execution
        try:
            main.init()
            main.maincycle()
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

