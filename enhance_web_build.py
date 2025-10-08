#!/usr/bin/env python3
"""
Post-build script to enhance the Pygbag-generated HTML with:
- Loading bar with progress indicator
- Error console for debugging
"""

import os
import sys
from pathlib import Path

def inject_loading_and_console(html_path):
    """Inject loading bar and error console into the generated HTML."""
    
    if not os.path.exists(html_path):
        print(f"❌ HTML file not found: {html_path}")
        return False
    
    print(f"📝 Enhancing {html_path}...")
    
    # Read the original HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # CSS for loading bar and error console
    enhanced_css = """
    <style id="enhanced-ui-styles">
        /* Enhanced Loading Screen */
        #loading-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            transition: opacity 0.5s ease-out;
        }

        #loading-screen.hidden {
            opacity: 0;
            pointer-events: none;
        }

        .loading-content {
            text-align: center;
            max-width: 500px;
            padding: 20px;
        }

        .loading-title {
            font-size: 2.5em;
            margin-bottom: 30px;
            color: #f0f0f0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            font-family: 'Courier New', monospace;
            animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        .loading-status {
            font-size: 1.1em;
            margin-bottom: 25px;
            color: #aaa;
            min-height: 30px;
            font-family: 'Courier New', monospace;
        }

        .loading-bar-container {
            width: 100%;
            height: 30px;
            background: rgba(0,0,0,0.3);
            border: 2px solid #555;
            border-radius: 15px;
            overflow: hidden;
            position: relative;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
        }

        .loading-bar {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
            width: 0%;
            transition: width 0.3s ease-out;
            position: relative;
            box-shadow: 0 0 10px rgba(76, 175, 80, 0.5);
        }

        .loading-bar::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, 
                transparent 0%, 
                rgba(255,255,255,0.3) 50%, 
                transparent 100%);
            animation: shimmer 1.5s infinite;
        }

        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }

        .loading-percentage {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 0.9em;
            font-weight: bold;
            color: #fff;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
            z-index: 1;
        }

        /* Error Console */
        #error-console {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            max-height: 250px;
            background: rgba(20, 20, 20, 0.95);
            border-top: 2px solid #ff4444;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            color: #ff6666;
            padding: 10px;
            display: none;
            z-index: 9999;
            box-shadow: 0 -5px 15px rgba(0,0,0,0.5);
        }

        #error-console.visible {
            display: block;
        }

        .console-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 5px 10px;
            background: rgba(255, 68, 68, 0.1);
            border-bottom: 1px solid #ff4444;
            margin: -10px -10px 10px -10px;
        }

        .console-title {
            font-weight: bold;
            color: #ff8888;
        }

        .console-toggle {
            background: transparent;
            border: 1px solid #ff4444;
            color: #ff6666;
            padding: 3px 10px;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            border-radius: 3px;
            transition: all 0.2s;
        }

        .console-toggle:hover {
            background: rgba(255, 68, 68, 0.2);
            border-color: #ff6666;
        }

        .error-message {
            margin: 5px 0;
            padding: 8px;
            background: rgba(255, 68, 68, 0.05);
            border-left: 3px solid #ff4444;
            word-wrap: break-word;
        }

        .error-timestamp {
            color: #888;
            font-size: 0.9em;
            margin-right: 10px;
        }

        .error-level-error {
            border-left-color: #ff4444;
        }

        .error-level-warning {
            border-left-color: #ffaa44;
            color: #ffcc66;
        }

        .error-level-info {
            border-left-color: #4444ff;
            color: #6666ff;
        }

        #error-toggle-btn {
            position: fixed;
            bottom: 10px;
            right: 10px;
            background: rgba(255, 68, 68, 0.8);
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 20px;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            z-index: 10001;
            display: none;
            transition: all 0.3s;
        }

        #error-toggle-btn:hover {
            background: rgba(255, 68, 68, 1);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(255, 68, 68, 0.4);
        }

        #error-toggle-btn.has-errors {
            display: block;
            animation: attention 2s ease-in-out infinite;
        }

        @keyframes attention {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        .error-count {
            background: #fff;
            color: #ff4444;
            border-radius: 10px;
            padding: 2px 6px;
            font-size: 0.8em;
            margin-left: 5px;
            font-weight: bold;
        }
    </style>
    """
    
    # HTML for loading bar and error console
    enhanced_html = """
    <!-- Enhanced Loading Screen -->
    <div id="loading-screen">
        <div class="loading-content">
            <div class="loading-title">🎮 UNDERTALE CLONE 🎮</div>
            <div class="loading-status" id="loading-status">Initializing...</div>
            <div class="loading-bar-container">
                <div class="loading-bar" id="loading-bar"></div>
                <div class="loading-percentage" id="loading-percentage">0%</div>
            </div>
        </div>
    </div>

    <!-- Error Console -->
    <div id="error-console">
        <div class="console-header">
            <span class="console-title">⚠️ Error Console</span>
            <button class="console-toggle" onclick="toggleConsole()">Hide</button>
        </div>
        <div id="error-log"></div>
    </div>

    <!-- Error Toggle Button -->
    <button id="error-toggle-btn" onclick="toggleConsole()">
        Errors <span class="error-count" id="error-count">0</span>
    </button>
    """
    
    # JavaScript for managing loading and errors
    enhanced_js = """
    <script id="enhanced-ui-script">
        // Loading Manager
        class LoadingManager {
            constructor() {
                this.progress = 0;
                this.loadingBar = document.getElementById('loading-bar');
                this.loadingPercentage = document.getElementById('loading-percentage');
                this.loadingStatus = document.getElementById('loading-status');
                this.loadingScreen = document.getElementById('loading-screen');
            }

            setProgress(percent) {
                this.progress = Math.min(100, Math.max(0, percent));
                if (this.loadingBar) this.loadingBar.style.width = this.progress + '%';
                if (this.loadingPercentage) this.loadingPercentage.textContent = Math.round(this.progress) + '%';
            }

            setStatus(status) {
                if (this.loadingStatus) this.loadingStatus.textContent = status;
            }

            complete() {
                this.setProgress(100);
                this.setStatus('Ready!');
                setTimeout(() => {
                    if (this.loadingScreen) this.loadingScreen.classList.add('hidden');
                }, 500);
            }
        }

        // Error Console Manager
        class ErrorConsole {
            constructor() {
                this.errors = [];
                this.console = document.getElementById('error-console');
                this.errorLog = document.getElementById('error-log');
                this.errorToggleBtn = document.getElementById('error-toggle-btn');
                this.errorCount = document.getElementById('error-count');
                this.isVisible = false;
                this.captureErrors();
            }

            captureErrors() {
                const self = this;
                const originalError = console.error;
                console.error = function(...args) {
                    self.addError('error', args.join(' '));
                    originalError.apply(console, args);
                };

                const originalWarn = console.warn;
                console.warn = function(...args) {
                    self.addError('warning', args.join(' '));
                    originalWarn.apply(console, args);
                };

                window.addEventListener('error', (event) => {
                    self.addError('error', `${event.message} (${event.filename}:${event.lineno})`);
                });

                window.addEventListener('unhandledrejection', (event) => {
                    self.addError('error', `Unhandled Promise: ${event.reason}`);
                });
            }

            addError(level, message) {
                const timestamp = new Date().toLocaleTimeString();
                this.errors.push({ level, message, timestamp });
                
                const errorDiv = document.createElement('div');
                errorDiv.className = `error-message error-level-${level}`;
                const safeMessage = String(message).replace(/</g, '&lt;').replace(/>/g, '&gt;');
                errorDiv.innerHTML = `<span class="error-timestamp">[${timestamp}]</span><span>${safeMessage}</span>`;
                
                if (this.errorLog) {
                    this.errorLog.appendChild(errorDiv);
                    this.errorLog.scrollTop = this.errorLog.scrollHeight;
                }

                if (this.errorCount) this.errorCount.textContent = this.errors.length;
                if (this.errorToggleBtn) this.errorToggleBtn.classList.add('has-errors');

                if (this.errors.length === 1) this.show();
            }

            show() {
                if (this.console) this.console.classList.add('visible');
                this.isVisible = true;
            }

            hide() {
                if (this.console) this.console.classList.remove('visible');
                this.isVisible = false;
            }

            toggle() {
                if (this.isVisible) this.hide();
                else this.show();
            }

            log(message, level = 'info') {
                this.addError(level, message);
            }
        }

        // Initialize
        let loadingManager, errorConsole;
        
        function initEnhancedUI() {
            loadingManager = new LoadingManager();
            errorConsole = new ErrorConsole();
            window.loadingManager = loadingManager;
            window.errorConsole = errorConsole;

            // Expose API
            window.gameAPI = {
                setLoadingProgress: (percent, status) => {
                    if (loadingManager) {
                        loadingManager.setProgress(percent);
                        if (status) loadingManager.setStatus(status);
                    }
                },
                completeLoading: () => {
                    if (loadingManager) loadingManager.complete();
                },
                logError: (msg) => {
                    if (errorConsole) errorConsole.log(msg, 'error');
                },
                logWarning: (msg) => {
                    if (errorConsole) errorConsole.log(msg, 'warning');
                },
                logInfo: (msg) => {
                    if (errorConsole) errorConsole.log(msg, 'info');
                }
            };
        }

        function toggleConsole() {
            if (errorConsole) errorConsole.toggle();
        }

        // Wait for DOM before initializing
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initEnhancedUI);
        } else {
            initEnhancedUI();
        }
    </script>
    """
    
    # Inject CSS into <head>
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', f'{enhanced_css}\n</head>')
    
    # Inject HTML elements at the beginning of <body>
    if '<body' in html_content:
        # Find the end of the <body> tag
        body_start = html_content.find('<body')
        body_tag_end = html_content.find('>', body_start)
        if body_tag_end != -1:
            html_content = html_content[:body_tag_end+1] + f'\n{enhanced_html}\n' + html_content[body_tag_end+1:]
    
    # Inject JavaScript before </body>
    if '</body>' in html_content:
        html_content = html_content.replace('</body>', f'{enhanced_js}\n</body>')
    
    # Write the enhanced HTML
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Enhanced HTML with loading bar and error console")
    return True

def main():
    """Main entry point."""
    build_dir = Path('build/web')
    
    if not build_dir.exists():
        print("❌ Build directory not found. Run ./build.sh first.")
        return 1
    
    # Find index.html
    index_path = build_dir / 'index.html'
    
    if not index_path.exists():
        print("❌ index.html not found in build directory")
        return 1
    
    # Enhance the HTML
    if inject_loading_and_console(str(index_path)):
        print("\n🎉 Success! The web build now has:")
        print("   • Loading bar with progress indicator")
        print("   • Error console for debugging")
        print("\nTest it by running:")
        print("   cd build/web && python3 -m http.server 8000")
        return 0
    else:
        print("\n❌ Failed to enhance HTML")
        return 1

if __name__ == '__main__':
    sys.exit(main())
