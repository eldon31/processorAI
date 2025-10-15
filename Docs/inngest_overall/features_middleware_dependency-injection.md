#### On this page

- [Using Middleware for Dependency Injection](\docs\features\middleware\dependency-injection#using-middleware-for-dependency-injection)
- [Advanced mutation](\docs\features\middleware\dependency-injection#advanced-mutation)
- [Ordering middleware and types](\docs\features\middleware\dependency-injection#ordering-middleware-and-types)
- [Advanced mutation](\docs\features\middleware\dependency-injection#advanced-mutation-2)
- [Ordering middleware and types](\docs\features\middleware\dependency-injection#ordering-middleware-and-types-2)

Features [Middleware](\docs\features\middleware)

# Using Middleware for Dependency Injection

Inngest Functions running in the same application often need to share common clients instances such as database clients or third-party

libraries.

The following is an example of adding a OpenAI client to all Inngest functions, allowing them immediate access without needing to create the client themselves.

TypeScript (v 3.34.0+) TypeScript (v 2.0.0+) Python (v 0.3.0+)

We can use the `dependencyInjectionMiddleware` to add arguments to a

function's input.

Check out the [TypeScript example](\docs\features\middleware\dependency-injection?guide=typescript) for a customized middleware.

Copy Copied

```
import { dependencyInjectionMiddleware } from "inngest" ;
import OpenAI from 'openai' ;

const openai = new OpenAI ();

const inngest = new Inngest ({
id : 'my-app' ,
middleware : [
dependencyInjectionMiddleware ({ openai }) ,
] ,
});
```

Our Inngest Functions can now access the OpenAI client through the context:

Copy Copied

```
inngest .createFunction (
{ name : "user-create" } ,
{ event : "app/user.create" } ,
async ({ openai }) => {
const chatCompletion = await openai . chat . completions .create ({
messages : [{ role : "user" , content : "Say this is a test" }] ,
model : "gpt-3.5-turbo" ,
});

// ...
} ,
);
```

💡 Types are inferred from middleware outputs, so your Inngest functions will see an appropriately-typed `openai` property in their input.

Explore other examples in the [TypeScript SDK Middleware examples page](\docs\reference\middleware\examples) .

### [Advanced mutation](\docs\features\middleware\dependency-injection#advanced-mutation)

When the middleware runs, the types and data within the passed `ctx` are merged on top of the default provided by the library. This means that you can use a few tricks to overwrite data and types safely and more accurately.

For example, here we use a `const` assertion to infer the literal value of our `foo` example above.

Copy Copied

```
// In middleware
dependencyInjectionMiddleware ({
foo : "bar" ,
} as const )

// In a function
async ({ event , foo }) => {
//             ^? (parameter) foo: "bar"
}
```

## [Ordering middleware and types](\docs\features\middleware\dependency-injection#ordering-middleware-and-types)

Middleware runs in the order specified when registering it (see [Middleware - Lifecycle - Registering and order](\docs\reference\middleware\lifecycle#registering-and-order) ), which affects typing too.

When inferring a mutated input or output, the SDK will apply changes from each middleware in sequence, just as it will at runtime. This means that for two middlewares that add a `foo` value to input arguments, the last one to run will be what it seen both in types and at runtime.