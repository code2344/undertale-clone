#!/usr/bin/python3
# coding=utf-8
"""
WebAssembly-compatible version of the Undertale Clone main file.
This file adds async/await support required for running in the browser via Pygbag/Emscripten.
Enhanced with loading progress and error logging for better user experience.
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

# Loading progress helper for web UI
class LoadingProgress:
    """Helper class to report loading progress to the web UI."""
    
    @staticmethod
    def set_progress(percent, status=""):
        """Update loading progress in the web UI."""
        if IS_WASM or IS_PYGBAG:
            try:
                # Call JavaScript function to update loading bar
                js_code = f"if(window.gameAPI){{window.gameAPI.setLoadingProgress({percent},'{status}');}}"
                # In Pygbag, we can execute JS via platform module
                if 'platform' in sys.modules:
                    try:
                        platform.window.eval(js_code)
                    except:
                        pass
            except:
                pass
    
    @staticmethod
    def complete():
        """Mark loading as complete."""
        if IS_WASM or IS_PYGBAG:
            try:
                js_code = "if(window.gameAPI){window.gameAPI.completeLoading();}"
                if 'platform' in sys.modules:
                    try:
                        platform.window.eval(js_code)
                    except:
                        pass
            except:
                pass

# Error logging helper for web UI
class WebConsole:
    """Helper class to log errors to the web console."""
    
    @staticmethod
    def log_error(message):
        """Log an error message to the web console."""
        if IS_WASM or IS_PYGBAG:
            try:
                safe_msg = str(message).replace("'", "\\'").replace("\n", "\\n")
                js_code = f"if(window.gameAPI){{window.gameAPI.logError('{safe_msg}');}}"
                if 'platform' in sys.modules:
                    try:
                        platform.window.eval(js_code)
                    except:
                        pass
            except:
                pass
    
    @staticmethod
    def log_warning(message):
        """Log a warning message to the web console."""
        if IS_WASM or IS_PYGBAG:
            try:
                safe_msg = str(message).replace("'", "\\'").replace("\n", "\\n")
                js_code = f"if(window.gameAPI){{window.gameAPI.logWarning('{safe_msg}');}}"
                if 'platform' in sys.modules:
                    try:
                        platform.window.eval(js_code)
                    except:
                        pass
            except:
                pass
    
    @staticmethod
    def log_info(message):
        """Log an info message to the web console."""
        if IS_WASM or IS_PYGBAG:
            try:
                safe_msg = str(message).replace("'", "\\'").replace("\n", "\\n")
                js_code = f"if(window.gameAPI){{window.gameAPI.logInfo('{safe_msg}');}}"
                if 'platform' in sys.modules:
                    try:
                        platform.window.eval(js_code)
                    except:
                        pass
            except:
                pass

async def async_maincycle():
    """
    Async version of the main game loop for WebAssembly compatibility.
    In WebAssembly, the main loop must be async to allow the browser to handle events.
    """
    import globals
    import threading
    
    try:
        LoadingProgress.set_progress(95, "Starting game loop...")
        threading.Thread(target=globals.room.on_enter, name='on_enter runner for first room').start()
        
        # Mark loading as complete once game loop starts
        LoadingProgress.complete()
        WebConsole.log_info("Game started successfully")
        
        while globals.running:
            if globals.room:
                globals.room.draw()
            
            # Yield control back to browser in WebAssembly environment
            # This prevents the browser from freezing during the game loop
            if IS_WASM or IS_PYGBAG:
                await asyncio.sleep(0)
    except Exception as e:
        WebConsole.log_error(f"Game loop error: {str(e)}")
        raise
        

async def async_main():
    """
    Async entry point for the game.
    Enhanced with loading progress and error logging.
    """
    import globals
    
    try:
        LoadingProgress.set_progress(10, "Initializing game...")
        WebConsole.log_info("Starting Undertale Clone...")
        
        LoadingProgress.set_progress(30, "Loading game modules...")
        main.init()
        
        LoadingProgress.set_progress(70, "Initializing game systems...")
        await async_maincycle()
        
    except globals.UndertaleError as e:
        error_msg = str(e.args[0]) if len(e.args) > 0 else "Unknown game error"
        WebConsole.log_error(f"Game Error: {error_msg}")
        if len(e.args) > 0:
            main.invoke_dog("", e.args[0])
        else:
            main.invoke_dog()
    except (SystemExit, KeyboardInterrupt):
        WebConsole.log_info("Game closed by user")
        globals.running = False
    except Exception as e:
        import traceback
        exc_type, exc_value, exc_traceback = sys.exc_info()
        output = traceback.format_exception(exc_type, exc_value, exc_traceback)
        output = [i[:-1].translate({ord('\n'): ':'}) for i in output]
        output = list(reversed(output))[:-1]
        
        # Log error to web console
        error_summary = f"{exc_type.__name__}: {str(exc_value)}"
        WebConsole.log_error(error_summary)
        for line in output[:5]:  # Log first 5 lines of traceback
            WebConsole.log_error(line)
        
        main.invoke_dog(output)
    finally:
        globals.running = False
        WebConsole.log_info("Game stopped")


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

