#!/bin/bash

uvicorn --factory src.backend.main:setup_app --host 127.0.0.1 --port 8000 --reload
