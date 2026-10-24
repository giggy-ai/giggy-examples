import { randomUUID } from 'node:crypto';
import { writeFile } from 'node:fs/promises';

import { parseArgs } from 'node:util';

const { values } = parseArgs({ options: {
  stt: { type: 'string' }, mode: { type: 'string', default: 'batch' }, output: { type: 'string' },
} });
if (values.stt) {
  const { Giggy } = await import('@giggy-ai/sdk');
  const client = new Giggy({ apiKey: process.env.GIGGY_API_KEY });
  if (!['batch', 'fast', 'streaming'].includes(values.mode)) throw new TypeError('mode must be batch, fast or streaming');
  let id;
  if (values.mode === 'streaming') {
    for await (const { event, data } of client.transcriptions.stream({ audioPath: values.stt, signal: AbortSignal.timeout(1_800_000) })) {
      if (event === 'generation_created') { id = data.generation.generation_uuid; console.error('Generation:', id); }
      if (event === 'transcript_chunk') console.error('Preview:', data.text);
    }
    if (!id) throw new Error('No admission UUID received; inspect History before resubmitting');
  } else {
    const admission = await client.transcriptions.submit({ audioPath: values.stt, mode: values.mode, signal: AbortSignal.timeout(1_800_000) });
    id = admission.generation.generation_uuid;
    console.error('Generation:', id);
  }
  const signal = AbortSignal.timeout(1_800_000);
  let result;
  while (true) {
    const generation = await client.transcriptions.get(id, signal);
    if (generation.status === 'completed') { result = await client.transcriptions.result(id, signal); break; }
    if (['failed', 'cancelled', 'admission_failed'].includes(generation.status)) throw new Error('Generation '+id+': '+generation.status);
    await (await import('node:timers/promises')).setTimeout(2500, undefined, { signal });
  }
  console.log(result.text);
  if (values.output) await writeFile(values.output, result.text, 'utf8');
} else {
  const apiKey = process.env.GIGGY_API_KEY;
  const voiceId = process.env.GIGGY_VOICE_ID;

  if (!apiKey) {
    throw new Error('Set GIGGY_API_KEY before running this example.');
  }

  if (!voiceId) {
    throw new Error('Set GIGGY_VOICE_ID before running this example.');
  }

  const response = await fetch('https://api.giggy.ai/v1/text-to-speech', {
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
}
