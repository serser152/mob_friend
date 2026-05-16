#!/bin/bash
source venv/bin/activate
export PYTHONPATH=$(pwd)
streamlit run --server.port=8503 ui/app_ui.py
