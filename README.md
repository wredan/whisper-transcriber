# whisper-transcriber
Custom personal cli interface implementation of OpenAI Whisper.

## CLI Usage

You can use it with python by running:
```bash
  $ python ./whisper_transcriber.py model <audio-file-1> <audio-file-2> ...
```
but first be sure to check [how to install section](#installation) below.

To transcript: 

```bash
  $ whisper-transcriber model <audio-file-1> <audio-file-2> ...
```

Whisper runs with PyTorch inference, so it will automatically choose 'cuda' if available. If not, it will run on the CPU. It's important to note that the larger the model you select, the more time it will take to transcribe (this is also true for the length of the audio), but the quality of the transcription will improve. To use larger models, a GPU with at least 10GB VRAM is needed.

Run:
```bash
  $ whisper-transcriber -h
```
for more info.

<a name="installation"></a>
## How To Install

Install the cli tool by running:
```bash
  $ pip install -e .
```
in the root project folder.

Other requirements are:
- ffmpeg executable on cli

Tips:
- Download PyTorch and use a conda environment, be sure to support cuda, using `torch.cuda.is_available()` in your conda env, to speed up the process.

## Credits

Thanks to the amazing work at OpenAI, check their repo at [Whisper Repo](https://github.com/openai/whisper) for more.