# BUDDY AI - GGUF MODELS DIRECTORY

This directory holds offline GGUF Large Language Models for Buddy.

## Automatic Model Setup
When running `install_requirements.bat` or starting Buddy on a new device, the local GGUF LLM model is **automatically downloaded** into this folder via `tools/model_downloader.py`.

## Manual Setup
If you want to use a custom GGUF model (e.g. Qwen, Llama 3, Mistral, or Phi), simply place your `.gguf` file here:
`c:\buddy\models\Qwen3-1.7B-Q4_K_M.gguf`
