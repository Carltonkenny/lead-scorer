#!/usr/bin/env python3
"""
Lead Prioritization Tool - Main Launcher
Streamlit application launcher with proper module paths
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))
sys.path.insert(0, str(src_path / "core"))
sys.path.insert(0, str(src_path / "modules"))
sys.path.insert(0, str(src_path / "utils"))

# Import and run the main app
if __name__ == "__main__":
    import streamlit.web.cli as stcli
    import streamlit as st
    
    # Set the path to the main app file
    app_path = str(src_path / "app.py")
    
    # Run streamlit
    sys.argv = ["streamlit", "run", app_path]
    stcli.main()