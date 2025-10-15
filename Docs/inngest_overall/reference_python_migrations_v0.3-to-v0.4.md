#### On this page

- [Python SDK migration guide: v0.3 to v0.4](\docs\reference\python\migrations\v0.3-to-v0.4#python-sdk-migration-guide-v0-3-to-v0-4)
- [Middleware](\docs\reference\python\migrations\v0.3-to-v0.4#middleware)
- [Constructor](\docs\reference\python\migrations\v0.3-to-v0.4#constructor)
- [transform\_input](\docs\reference\python\migrations\v0.3-to-v0.4#transform-input)
- [transform\_output](\docs\reference\python\migrations\v0.3-to-v0.4#transform-output)
- [Removed exports](\docs\reference\python\migrations\v0.3-to-v0.4#removed-exports)
- [Removed async\_mode arg in inngest.django.serve](\docs\reference\python\migrations\v0.3-to-v0.4#removed-async-mode-arg-in-inngest-django-serve)
- [NonRetriableError](\docs\reference\python\migrations\v0.3-to-v0.4#non-retriable-error)

References [Python SDK](\docs\reference\python) [Migrations](\docs\reference\python\migrations\v0.4-to-v0.5)

# Python SDK migration guide: v0.3 to v0.4

This guide will help you migrate your Inngest Python SDK from v0.3 to v0.4 by providing a summary of the breaking changes.

## [Middleware](\docs\reference\python\migrations\v0.3-to-v0.4#middleware)

### [Constructor](\docs\reference\python\migrations\v0.3-to-v0.4#constructor)

Added the `raw_request` arg to the constructor. This is the raw HTTP request received by the `serve` function. Its usecase is predominately for platforms that include critical information in the request, like environment variables in Cloudflare Workers.

### [transform\_input](\docs\reference\python\migrations\v0.3-to-v0.4#transform-input)

Added the `steps` arg, which was previous in `ctx._steps` . This is useful in encryption middleware.

Added the `function` arg, which is the `inngest.Function` object. This is useful for middleware that needs to know the function's metadata (like error reporting).

Its return type is now `None` since modifying data should happen by mutating args.

### [transform\_output](\docs\reference\python\migrations\v0.3-to-v0.4#transform-output)

Replaced the `output` arg with `result` arg. Its type is the new `inngest.TransformOutputResult` class:

Copy Copied

```
class TransformOutputResult :
# Mutations to these fields within middleware will be kept after running
# middleware
error : typing . Optional [ Exception ]
output : object

# Mutations to these fields within middleware will be discarded after
# running middleware
step : typing . Optional [ TransformOutputStepInfo ]

class TransformOutputStepInfo :
id : str
op : Opcode
opts : typing . Optional [ dict [ str , object ]]
```

Its return type is now `None` since modifying data should happen by mutating args.

## [Removed exports](\docs\reference\python\migrations\v0.3-to-v0.4#removed-exports)

- `inngest.FunctionID` -- No use case.
- `inngest.Output` -- Replaced by `inngest.TransformOutputResult` .

## [Removed async\_mode arg in inngest.django.serve](\docs\reference\python\migrations\v0.3-to-v0.4#removed-async-mode-arg-in-inngest-django-serve)

This argument is no longer needed since async mode is inferred based on the Inngest functions you declare. If you have one or more `async` Inngest functions then async mode is enabled.

## [NonRetriableError](\docs\reference\python\migrations\v0.3-to-v0.4#non-retriable-error)

Removed the `cause` arg since it wasn't actually used. We'll eventually reintroduce it in a proper way.