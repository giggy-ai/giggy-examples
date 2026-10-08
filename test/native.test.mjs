import assert from 'node:assert/strict';
import { readFile, rm } from 'node:fs/promises';
import test from 'node:test';

const voiceId = '00000000-0000-0000-0000-000000000000';
const apiKey = 'offline-test-key';

async function runWithMockFetch(modulePath, contentType) {
  const previousFetch = globalThis.fetch;
  const previousKey = process.env.GIGGY_API_KEY;
  const previousVoice = process.env.GIGGY_VOICE_ID;

  let request;

  process.env.GIGGY_API_KEY = apiKey;
  process.env.GIGGY_VOICE_ID = voiceId;

  globalThis.fetch = async (url, init) => {
    request = { url: String(url), init };

    return new Response(
      new Uint8Array([1, 2, 3, 4]),
      {
        status: 200,
        headers: { 'content-type': contentType },
      },
    );
  };

  try {
    await import(new URL(modulePath, import.meta.url).href);
    return request;
  } finally {
    globalThis.fetch = previousFetch;

    if (previousKey === undefined) {
      delete process.env.GIGGY_API_KEY;
    } else {
      process.env.GIGGY_API_KEY = previousKey;
    }

    if (previousVoice === undefined) {
      delete process.env.GIGGY_VOICE_ID;
    } else {
      process.env.GIGGY_VOICE_ID = previousVoice;
    }
  }
}

test('native Batch example generates an authenticated MP3 request', async () => {
  const output = new URL('../node/basic-tts/speech.mp3', import.meta.url);

  try {
    const request = await runWithMockFetch(
      '../node/basic-tts/index.mjs',
      'audio/mpeg',
    );

    assert.equal(
      request.url,
      'https://giggy.ai/v1/text-to-speech',
    );

    const headers = new Headers(request.init.headers);
    const payload = JSON.parse(request.init.body);

    assert.equal(headers.get('xi-api-key'), apiKey);
    assert.ok(headers.get('idempotency-key'));
    assert.equal(payload.mode, 'batch');
    assert.equal(payload.voice_id, voiceId);
    assert.equal(payload.output_format, 'mp3_24000_160');

    const bytes = await readFile(output);
    assert.deepEqual([...bytes], [1, 2, 3, 4]);
  } finally {
    await rm(output, { force: true });
  }
});

test('native Streaming example handles progressive PCM response', async () => {
  const output = new URL('../node/streaming-tts/speech.pcm', import.meta.url);

  try {
    const request = await runWithMockFetch(
      '../node/streaming-tts/index.mjs',
      'audio/pcm',
    );

    assert.equal(
      request.url,
      'https://giggy.ai/v1/text-to-speech',
    );

    const headers = new Headers(request.init.headers);
    const payload = JSON.parse(request.init.body);

    assert.equal(headers.get('xi-api-key'), apiKey);
    assert.equal(headers.get('idempotency-key'), null);
    assert.equal(payload.mode, 'streaming');
    assert.equal(payload.output_format, 'pcm_24000');

    const bytes = await readFile(output);
    assert.deepEqual([...bytes], [1, 2, 3, 4]);
  } finally {
    await rm(output, { force: true });
  }
});
