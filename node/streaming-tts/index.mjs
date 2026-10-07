import { createWriteStream } from 'node:fs';
import { Readable } from 'node:stream';
import { pipeline } from 'node:stream/promises';

const apiKey = process.env.GIGGY_API_KEY;
const voiceId = process.env.GIGGY_VOICE_ID;

if (!apiKey) {
  throw new Error('Set GIGGY_API_KEY before running this example.');
}

if (!voiceId) {
  throw new Error('Set GIGGY_VOICE_ID before running this example.');
}

const response = await fetch('https://giggy.ai/v1/text-to-speech', {
  method: 'POST',
  headers: {
    'xi-api-key': apiKey,
    'content-type': 'application/json',
  },
  body: JSON.stringify({
    text: 'This audio is streaming from Giggy.',
    voice_id: voiceId,
    model_id: 'giggyspeech',
    mode: 'streaming',
    output_format: 'pcm_24000',
    voice_settings: {
      speed: 1,
    },
  }),
});

if (!response.ok) {
  const errorBody = await response.text();

  throw new Error(
    `Giggy returned HTTP ${response.status}: ${errorBody}`,
  );
}

if (!response.body) {
  throw new Error('Giggy returned an empty response body.');
}

const contentType = response.headers.get('content-type') ?? '';

if (!contentType.startsWith('audio/pcm')) {
  throw new Error(
    `Expected an audio/pcm response but received "${contentType || 'unknown'}".`,
  );
}

const outputUrl = new URL('./speech.pcm', import.meta.url);
const output = createWriteStream(outputUrl);

await pipeline(
  Readable.fromWeb(response.body),
  output,
);

console.log(
  `Wrote streaming PCM to ${outputUrl.pathname} ` +
    '(PCM16 little-endian, mono, 24000 Hz)',
);
