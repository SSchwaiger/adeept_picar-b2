#!/usr/bin/env python3
# File name   : VoiceIdentify.py
# Author      : Adeept
# Date        : 2025/05/16
import os

user_home = os.path.expanduser('~')  # Get current user's home directory

def main():
    # cmd = "sudo  " + user_home +"/sherpa-ncnn/build/bin/sherpa-ncnn-microphone \
    #       " + user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/tokens.txt \
    #       " + user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/encoder_jit_trace-pnnx.ncnn.param \
    #       " + user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/encoder_jit_trace-pnnx.ncnn.bin \
    #       " + user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/decoder_jit_trace-pnnx.ncnn.param \
    #       " + user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/decoder_jit_trace-pnnx.ncnn.bin \
    #       " + user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/joiner_jit_trace-pnnx.ncnn.param \
    #       " + user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/joiner_jit_trace-pnnx.ncnn.bin "

    # If the above commands cannot be used, please use the following command. Use "arecord -l" to check the local audio input devices, and then replace the parameter "2" in "plughw:2,0". 
    cmd = "sudo " + user_home +"/sherpa-ncnn/build/bin/sherpa-ncnn-alsa \
            " + user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/tokens.txt \
            " + user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/encoder_jit_trace-pnnx.ncnn.param \
            " + user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/encoder_jit_trace-pnnx.ncnn.bin \
            " + user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/decoder_jit_trace-pnnx.ncnn.param \
            " + user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/decoder_jit_trace-pnnx.ncnn.bin \
            " + user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/joiner_jit_trace-pnnx.ncnn.param \
            " + user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/joiner_jit_trace-pnnx.ncnn.bin \
            plughw:2,0 \
            2 \
            greedy_search"
    os.system(f"{cmd} > output.txt 2>&1")
if __name__ == "__main__":
    main()

