#### On this page

- [Encryption Middleware](\docs\features\middleware\encryption-middleware#encryption-middleware)
- [Installation](\docs\features\middleware\encryption-middleware#installation)
- [Changing the encrypted event.data field](\docs\features\middleware\encryption-middleware#changing-the-encrypted-event-data-field)
- [Decrypt only mode](\docs\features\middleware\encryption-middleware#decrypt-only-mode)
- [Fallback decryption keys](\docs\features\middleware\encryption-middleware#fallback-decryption-keys)
- [Cross-language support](\docs\features\middleware\encryption-middleware#cross-language-support)

Features [Middleware](\docs\features\middleware)

# Encryption Middleware

Encryption middleware provides end-to-end encryption for events, step output, and function output. **Only encrypted data is sent to Inngest servers** : encryption and decryption happen within your infrastructure.

TypeScript (v2.0.0+) Python (v0.3.0+)

## [Installation](\docs\features\middleware\encryption-middleware#installation)

Install the [`@inngest/middleware-encryption`](https://www.npmjs.com/package/@inngest/middleware-encryption) [package](https://www.npmjs.com/package/@inngest/middleware-encryption) ( [GitHub](https://github.com/inngest/inngest-js/tree/main/packages/middleware-encryption#readme) ) and configure it as follows:

Copy Copied

```
import { encryptionMiddleware } from "@inngest/middleware-encryption" ;

// Initialize the middleware
const mw = encryptionMiddleware ({
// your encryption key string should not be hard coded
key : process . env . MY_ENCRYPTION_KEY ,
});

// Use the middleware with Inngest
const inngest = new Inngest ({
id : "my-app" ,
middleware : [mw] ,
});
```

By default, the following will be encrypted:

- All step data
- All function output
- Event data placed inside `data.encrypted`

## [Changing the encrypted event.data field](\docs\features\middleware\encryption-middleware#changing-the-encrypted-event-data-field)

Only select pieces of event data are encrypted. By default, only the data.encrypted field.

This can be customized using the `eventEncryptionField: string` setting.

## [Decrypt only mode](\docs\features\middleware\encryption-middleware#decrypt-only-mode)

To disable encryption but continue decrypting, set `decryptOnly: true` . This is useful when you want to migrate away from encryption but still need to process older events.

## [Fallback decryption keys](\docs\features\middleware\encryption-middleware#fallback-decryption-keys)

To attempt decryption with multiple keys, set the `fallbackDecryptionKeys` parameter. This is useful when rotating keys, since older events may have been encrypted with a different key:

Copy Copied

```
// start out with the current key
encryptionMiddleware ({
key : process . env . MY_ENCRYPTION_KEY ,
});

// deploy all services with the new key as a decryption fallback
encryptionMiddleware ({
key : process . env . MY_ENCRYPTION_KEY ,
fallbackDecryptionKeys : [ "new" ] ,
});

// deploy all services using the new key for encryption
encryptionMiddleware ({
key : process . env . MY_ENCRYPTION_KEY_V2 ,
fallbackDecryptionKeys : [ "current" ] ,
});

// once you are sure all data using the "current" key has passed, phase it out
encryptionMiddleware ({
key : process . env . MY_ENCRYPTION_KEY_V2 ,
});
```

## [Cross-language support](\docs\features\middleware\encryption-middleware#cross-language-support)

This middleware is compatible with our encryption middleware in our TypeScript SDK. Encrypted events can be sent from Python and decrypted in TypeScript, and vice versa.