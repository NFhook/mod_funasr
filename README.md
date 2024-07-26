#### FunASR
> [funasr](https://github.com/modelscope/FunASR) 

```bash
cd funasr-online-cpu
docker build -t funasr-online-cpu:v0.1.10 .
docker-compose up -d
```
> can use hotwords version, add hotwords.txt  


#### mod_funasr


```
export PKG_CONFIG_PATH=/usr/local/freeswitch/lib/pkgconfig
```
```
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make
sudo make install
```
```
cp mod_funasr.so /usr/local/freeswitch/mod/
fs_cli
>load mod_funasr
```

#### dialpan
```
<action application="python" data="demo"/>
```

#### command
> when answer.
```
uuid_funasr <uuid> start <wss-url> <mix-type> <sampling-rate> <metadata>
uuid_funasr 8cf9ebf1-a2db-454a-a49e-57ab68798815 start ws://10.10.10.30:10095 stereo 8k {"chunk_size":[5,10,5],"wav_name":"h5","is_speaking":true,"chunk_interval":10,"itn":true,"mode":"offline","hotwords":null}
```
Attaches a media bug and starts streaming audio (in L16 format) to the websocket server. FS default is 8k. If sampling-rate is other than 8k it will be resampled.
- `uuid` - Freeswitch channel unique id
- `wss-url` - websocket url `ws://` or `wss://`
- `mix-type` - choice of 
  - "mono" - single channel containing caller's audio
  - "mixed" - single channel containing both caller and callee audio
  - "stereo" - two channels with caller audio in one and callee audio in the other.
- `sampling-rate` - choice of
  - "8k" = 8000 Hz sample rate will be generated
  - "16k" = 16000 Hz sample rate will be generated
- `metadata` - (optional) a valid `utf-8` text to send. It will be sent the first before audio streaming starts.

```
uuid_funasr <uuid> send_text <metadata>
```
Sends a text to the websocket server. Requires a valid `utf-8` text.

```
uuid_funasr <uuid> stop <metadata>
```
Stops audio stream and closes websocket connection. If _metadata_ is provided it will be sent before the connection is closed.

```
uuid_funasr <uuid> pause
```
Pauses audio stream

```
uuid_funasr <uuid> resume
```
Resumes audio stream

## Events
Module will generate the following event types:
- `mod_funasr::json`
- `mod_funasr::connect`
- `mod_funasr::disconnect`
- `mod_funasr::error`
- `mod_funasr::play`

### response
Message received from websocket endpoint. Json expected, but it contains whatever the websocket server's response is.
#### Freeswitch event generated
**Name**: mod_funasr::json
**Body**: WebSocket server response

### connect
Successfully connected to websocket server.
#### Freeswitch event generated
**Name**: mod_funasr::connect
**Body**: JSON
```json
{
	"status": "connected"
}
```

### disconnect
Disconnected from websocket server.
#### Freeswitch event generated
**Name**: mod_funasr::disconnect
**Body**: JSON
```json
{
	"status": "disconnected",
	"message": {
		"code": 1000,
		"reason": "Normal closure"
	}
}
```
- code: `<int>`
- reason: `<string>`

### error
There is an error with the connection. Multiple fields will be available on the event to describe the error.
#### Freeswitch event generated
**Name**: mod_funasr::error
**Body**: JSON
```json
{
	"status": "error",
	"message": {
		"retries": 1,
		"error": "Expecting status 101 (Switching Protocol), got 403 status connecting to wss://localhost, HTTP Status line: HTTP/1.1 403 Forbidden\r\n",
		"wait_time": 100,
		"http_status": 403
	}
}
```
- retries: `<int>`, error: `<string>`, wait_time: `<int>`, http_status: `<int>`

### play
**Name**: mod_funasr::play
**Body**: JSON

Websocket server may return JSON object containing base64 encoded audio to be played by the user. To use this feature, response must follow the format:
```json
{
  "type": "streamAudio",
  "data": {
    "audioDataType": "raw",
    "sampleRate": 8000,
    "audioData": "base64 encoded audio"
  }
}
```
- audioDataType: `<raw|wav|mp3|ogg>`

Event generated by the module (subclass: _mod_funasr::play_) will be the same as the `data` element with the **file** added to it representing filePath:
```json
{
  "audioDataType": "raw",
  "sampleRate": 8000,
  "file": "/path/to/the/file"
}
```
If printing to the log is not suppressed, `response` printed to the console will look the same as the event. The original response containing base64 encoded audio is replaced because it can be quite huge.

All the files generated by this feature will reside at the temp directory and will be deleted when the session is closed.
