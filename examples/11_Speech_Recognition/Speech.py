#!/usr/bin/env/python
# File name   : Speech.py
# Website     : www.Adeept.com
# Author      : Adeept
# Date        : 2025/03/13
import os

user_home = 'roboterauto'

def main():
    # cmd = "sudo  "+ user_home +"/sherpa-ncnn/build/bin/sherpa-ncnn-microphone \
    #       "+ user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/tokens.txt \
    #       "+ user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/encoder_jit_trace-pnnx.ncnn.param \
    #       "+ user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/encoder_jit_trace-pnnx.ncnn.bin \
    #       "+ user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/decoder_jit_trace-pnnx.ncnn.param \
    #       "+ user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/decoder_jit_trace-pnnx.ncnn.bin \
    #       "+ user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/joiner_jit_trace-pnnx.ncnn.param \
    #       "+ user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/joiner_jit_trace-pnnx.ncnn.bin"

    # You can also use the `sherpa-ncnn-alsa` command for speech recognition. Note that you need to replace the `plughw:3,0` parameter with the serial number of your own sound card.
    cmd = "sudo "+ user_home +"/sherpa-ncnn/build/bin/sherpa-ncnn-alsa \
            "+ user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/tokens.txt \
            "+ user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/encoder_jit_trace-pnnx.ncnn.param \
            "+ user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/encoder_jit_trace-pnnx.ncnn.bin \
            "+ user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/decoder_jit_trace-pnnx.ncnn.param \
            "+ user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/decoder_jit_trace-pnnx.ncnn.bin \
            "+ user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/joiner_jit_trace-pnnx.ncnn.param \
            "+ user_home +"/sherpa-ncnn/sherpa-ncnn-streaming-zipformer-bilingual-zh-en-2023-02-13/joiner_jit_trace-pnnx.ncnn.bin \
            plughw:3,0 \
            4 \
            greedy_search"
    os.system(f"{cmd} > output.txt 2>&1") #Run a command-line program and save the output results to a file named 'output. txt'
if __name__ == "__main__":
    main()