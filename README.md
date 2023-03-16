# whisper-transcriber
Custom personal cli interface implementation of OpenAI Whisper.

---------------

## Installation

Install the cli tool by running:
```bash
  $ pip install -e .
```
in the root project folder.

Other requirements are:
- ffmpeg executable on cli

Tips:
- use a conda environment, be sure to support cuda, using `torch.cuda.is_available()` in your conda env, to speed up the process.

---------------
## CLI Usage

To transcript: 

```bash
  $ whisper-transcriber model <audio-file-1> <audio-file-1> ... -o <file-name>.txt -f <output-format>
```

It runs using PyTorch inference, so it will select 'cuda' by default if available. It will run on the CPU otherwise. Keep in mind that the larger the model you select, the more time it will take to transcribe (same for audio length), but the quality of transcription will increase.


Run:
```bash
  $ whisper-transcriber -h
```
for more info.

---------------
## Credits

Thanks to the amazing work at OpenAI, check their repo at [Whisper Repo](https://github.com/openai/whisper) for more.