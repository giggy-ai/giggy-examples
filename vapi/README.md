# Use Giggy custom TTS with Vapi

Giggy exposes a Vapi-compatible custom TTS webhook:

```text
POST https://giggy.ai/v1/integrations/vapi/text-to-speech/{voiceId}
```

This is a Vapi custom TTS integration.

Giggy is not claiming a native Vapi provider listing.

## 1. Choose a Giggy voice

Get a public voice UUID from:

```text
GET https://giggy.ai/v1/integrations/voices
```

or use a Giggy voice UUID you already own.

## 2. Configure the URL

Replace:

```text
VOICE_ID
```

in:

```text
assistant-config.json
```

with the Giggy voice UUID.

Example:

```text
https://giggy.ai/v1/integrations/vapi/text-to-speech/00000000-0000-0000-0000-000000000000
```

## 3. Store the Giggy key in Vapi

Create a Vapi Custom Credential.

Configure that credential so requests send:

```text
Authorization: Bearer giggy_sk_...
```

Do not place the Giggy API key directly inside the assistant configuration.

## 4. Reference the credential

Set:

```json
{
  "credentialId": "YOUR_VAPI_CUSTOM_CREDENTIAL_ID"
}
```

to the Vapi credential ID.

## Audio contract

Vapi sends a `voice-request` containing text and a requested `sampleRate`.

The current public Giggy V17 contract accepts **24000 Hz only**. Vapi can request other sample rates; those requests are unsupported by this adapter and return HTTP 422. The server does not resample. Do not claim telephone/sample-rate compatibility until the actual Vapi route has been qualified.

Giggy responds with:

```text
signed PCM16 little-endian
mono
no WAV header
the exact requested sample rate
```

## Complete configuration

```json
{
  "voice": {
    "provider": "custom-voice",
    "server": {
      "url": "https://giggy.ai/v1/integrations/vapi/text-to-speech/VOICE_ID",
      "credentialId": "YOUR_VAPI_CUSTOM_CREDENTIAL_ID",
      "timeoutSeconds": 30
    }
  }
}
```
## Verify a real Vapi call

1. Configure a Vapi Custom Credential containing the Giggy API key.
2. Replace `VOICE_ID` with a valid Giggy voice UUID.
3. Create or update a test assistant using `assistant-config.json`.
4. Place an authorized test call.
5. Confirm Giggy receives a custom TTS request.
6. Confirm Vapi receives a nonempty PCM audio response.
7. Record the result without storing credentials or call audio in Git.

This repository has not performed an authorized Vapi test call.

Contract source: [Giggy OpenAPI](https://giggy.ai/v1/openapi.json). See [Vapi custom TTS documentation](https://docs.vapi.ai/customization/custom-voices/custom-tts) for the platform's PCM requirements. A real Vapi call and requested sample-rate verification remain approval-gated; this repository does not change Vapi or Giggy production services.
