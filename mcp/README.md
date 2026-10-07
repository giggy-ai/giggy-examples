# Giggy MCP

Giggy exposes a remote Streamable HTTP MCP server at:

```text
https://giggy.ai/mcp
```

Authentication:

```text
Authorization: Bearer $GIGGY_API_KEY
```

The speech tools documented for Giggy MCP are:

```text
list_voices
list_my_voices
generate_speech
get_speech_generation
```

Use the dedicated MCP repository for client configuration and raw MCP examples:

```text
https://github.com/GRQDigitalCapital/giggy-mcp
```

Giggy MCP returns generation metadata rather than live audio bytes.

For progressive PCM audio, use the REST streaming endpoint.
