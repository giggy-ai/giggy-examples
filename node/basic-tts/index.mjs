import { randomUUID } from 'node:crypto';
import { writeFile } from 'node:fs/promises';

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
    'idempotency-key': randomUUID(),
  },
  body: JSON.stringify({
    text: 'Hello from Giggy.',
    voice_id: voiceId,
    model_id: 'giggyspeech',
    mode: 'batch',
    output_format: 'mp3_24000_160',
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

const outputUrl = new URL('./speech.mp3', import.meta.url);
const audio = Buffer.from(await response.arrayBuffer());

await writeFile(outputUrl, audio);

console.log(`Wrote ${audio.length} bytes to ${outputUrl.pathname}`);
