#ifndef MOD_FUNASR_H
#define MOD_FUNASR_H

#include <switch.h>
#include <speex/speex_resampler.h>
#include "buffer/ringbuffer.h"

#define MY_BUG_NAME "audio_stream"
#define MAX_SESSION_ID (256)
#define MAX_WS_URI (4096)
#define MAX_METADATA_LEN (8192)

#define EVENT_CONNECT           "funasr::connect"
#define EVENT_DISCONNECT        "funasr::disconnect"
#define EVENT_ERROR             "funasr::error"
#define EVENT_JSON              "funasr::json"
#define EVENT_PLAY              "funasr::play"

typedef void (*responseHandler_t)(switch_core_session_t* session, const char* eventName, const char* json);

struct private_data {
    switch_mutex_t *mutex;
    char sessionId[MAX_SESSION_ID];
    SpeexResamplerState *resampler;
    responseHandler_t responseHandler;
    void *pAudioStreamer;
    char ws_uri[MAX_WS_URI];
    int sampling;
    int channels;
    int audio_paused:1;
    int close_requested:1;
    char initialMetadata[8192];
    RingBuffer *buffer;
    switch_buffer_t *sbuffer;
    uint8_t *data;
    int rtp_packets;
};

typedef struct private_data private_t;

enum notifyEvent_t {
    CONNECT_SUCCESS,
    CONNECT_ERROR,
    CONNECTION_DROPPED,
    MESSAGE
};

#endif //MOD_FUNASR_H
