# Source and review

- Hub ID: `official/creative/pixel-art`
- Reviewed source: https://github.com/NousResearch/hermes-agent/tree/787ee808ae898e5aca55e519379ff6842d6a0911/optional-skills/creative/pixel-art
- MIT notices and original palette and animation attribution are bundled.
- Reviewed every shipped file. Python uses Pillow and local files; video uses argv-based ffmpeg with temporary local frames. No network calls, account access, or dependency installation. Use trusted inputs, bounded previews, and new output paths. The conversion discards alpha and is for studies or treatments. Animation here is a scene overlay.
- The video script clamps particle margins on small canvases and pads odd MP4 dimensions for H.264 encoding. Conversion code, palette data, and original attribution are unchanged.
