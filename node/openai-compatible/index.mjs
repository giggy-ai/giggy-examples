import { writeFile } from 'node:fs/promises';
import OpenAI from 'openai';

const apiKey = process.env.GIGGY_API_KEY;
const voiceId = process.env.GIGGY_VOICE_ID;

if (!apiKey) {
  throw new Error('Set GIGGY_API_KEY before running this example.');
}

if (!voiceId) {
  throw new Error('Set GIGGY_VOICE_ID before running this example.');
}

const client = new OpenAI({
  apiKey,
  baseURL: 'https://giggy.ai/v1',
  maxRetries: 0,
});

const response = await client.audio.speech.create({
  model: 'giggyspeech',
  voice: voiceId,
  input: 'Hello from the Giggy OpenAI-compatible speech endpoint.',
  response_format: 'mp3',
});

const audio = Buffer.from(await response.arrayBuffer());
const outputUrl = new URL('./speech.mp3', import.meta.url);

await writeFile(outputUrl, audio);

console.log(`Wrote ${audio.length} bytes to ${outputUrl.pathname}`);
