#!/bin/bash
#offline
#cd /workspace/FunASR/runtime
#nohup bash run_server.sh \
#  --download-model-dir /workspace/models \
#  --vad-dir damo/speech_fsmn_vad_zh-cn-16k-common-onnx \
#  --model-dir damo/speech_paraformer-large-contextual_asr_nat-zh-cn-16k-common-vocab8404-onnx  \
#  --punc-dir damo/punc_ct-transformer_cn-en-common-vocab471067-large-onnx \
#  --lm-dir damo/speech_ngram_lm_zh-cn-ai-wesp-fst \
#  --itn-dir thuduj12/fst_itn_zh \
#  --certfile 0 \
#  --io-thread-num 2 \
#  --decoder-thread-num 8 \
#  --model-thread-num 1 \
#  --hotword /workspace/models/hotwords.txt > log.out 2>&1 &
#tail -f log.out


#online
cd /workspace/FunASR/runtime
nohup bash run_server_2pass.sh \
  --download-model-dir /workspace/models \
  --vad-dir damo/speech_fsmn_vad_zh-cn-16k-common-onnx \
  --model-dir damo/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-onnx  \
  --online-model-dir damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online-onnx  \
  --punc-dir damo/punc_ct-transformer_zh-cn-common-vad_realtime-vocab272727-onnx \
  --lm-dir damo/speech_ngram_lm_zh-cn-ai-wesp-fst \
  --itn-dir thuduj12/fst_itn_zh \
  --certfile 0  \
  --hotword /workspace/models/hotwords.txt > log.out 2>&1 &
tail -f log.out
